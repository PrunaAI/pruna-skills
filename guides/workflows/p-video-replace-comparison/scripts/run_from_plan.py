#!/usr/bin/env python3
"""Run a P-Video-Replace comparison reel from a JSON scene plan.

Plan contract (see templates/scene-plan.template.json):
- replace_target: character | clothing | object | mixed
- replace_mode: multi_job (per-reference instruction_prompt) | single_call
- source.subject_in_video: what in the clip gets swapped
- references[].instruction_prompt: required for multi_job mapping

Default phase is ``stills`` (Phase A only). See references/staged-generation-gate.md.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from pruna_api import (  # noqa: E402
    download_file,
    require_api_key,
    run_prediction,
    upload_file,
)
from pruna_paths import (  # noqa: E402
    default_out_dir,
    default_template,
    repo_root,
    sibling_script,
)

_SHARED_SCRIPTS = repo_root() / "guides/workflows/_shared/scripts"
if str(_SHARED_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SHARED_SCRIPTS))

from launch_background_music import apply_background_music, music_config_from_plan  # noqa: E402

_REPO = repo_root()
DEFAULT_PLAN = _REPO / "output/p-video-replace-announcement/announcement_plan.json"
DEFAULT_OUT = default_out_dir("p-video-replace-announcement")


VOICE_BY_GENDER = {
    "female": "Zephyr (Female)",
    "male": "Puck (Male)",
}

GENDER_REFERENCE_PREFIX = {
    "female": (
        "Adult woman only, clearly feminine face and presentation, not male, not androgynous. "
    ),
    "male": (
        "Adult man only, clearly masculine face and jawline, short or medium male grooming, "
        "not female, not androgynous. "
    ),
}

def is_object_only_reference(reference: dict) -> bool:
    beat = str(reference.get("beat_label", "")).lower()
    if beat in {
        "object",
        "product only",
        "sku a",
        "sku b",
        "bag only",
        "mug only",
        "gold sword",
        "ice sword",
        "greatsword",
    }:
        return True
    prompt = str(reference.get("prompt", "")).lower()
    if "weapon asset" in prompt and "no person" not in prompt:
        return "hand-scale" in prompt or "on dark neutral backdrop" in prompt
    return "no person" in prompt or "packshot" in prompt and "holding" not in prompt


def skip_swap_visual_bible(reference: dict) -> bool:
    """Stylized ladder refs and wardrobe rows carry their own look — loud swap bible causes collages."""
    beat = str(reference.get("beat_label", "")).lower()
    if beat.startswith("style ") or any(
        beat.startswith(prefix)
        for prefix in ("image ·", "motion ·", "video ·", "replace ·", "phase a ·")
    ) or beat in {
        "anthropomorphic",
        "fictional 3d",
        "workflow ugc",
        "recast",
        "recast a",
        "recast b",
        "wardrobe",
        "look a",
        "look b",
        "accessories",
    }:
        return True
    return False


def reference_image_prompt(
    scene: dict, reference: dict, *, swap_visual_bible: str = ""
) -> str:
    """Lock reference stills to scene persona_gender; optional loud swap styling."""
    prompt = str(reference["prompt"]).strip()
    object_only = is_object_only_reference(reference)
    if swap_visual_bible and not object_only and not skip_swap_visual_bible(reference):
        prompt = f"{swap_visual_bible.strip()} {prompt}"
    if object_only:
        return prompt
    gender = str(scene.get("persona_gender", "")).lower()
    prefix = GENDER_REFERENCE_PREFIX.get(gender, "")
    if prefix and not prompt.lower().startswith(prefix.strip().lower()[:12]):
        prompt = f"{prefix}{prompt}"
    return prompt


def voice_prompt_for(source: dict, cast: dict) -> str:
    return source.get("voice_prompt") or cast["voice_prompt"]


def source_cast_for(scene: dict, source: dict, cast: dict) -> dict[str, str]:
    voice = source.get("voice")
    if not voice:
        gender = str(scene.get("persona_gender", "")).lower()
        voice = VOICE_BY_GENDER.get(gender, cast["voice"])
    return {
        "voice": voice,
        "voice_language": source.get("voice_language") or cast["voice_language"],
        "voice_prompt": voice_prompt_for(source, cast),
    }


def validate_plan_scenes(plan: dict) -> None:
    """Ensure each replace scene has matched gender voice and multiple slider beats."""
    min_refs = int(plan.get("min_replacements_per_scene", 3))
    for scene in plan.get("scenes", []):
        if scene.get("type") != "replace":
            continue
        scene_id = scene["id"]
        gender = str(scene.get("persona_gender", "")).lower()
        source = scene.get("source") or {}
        voice = source.get("voice", "")
        if gender in VOICE_BY_GENDER and voice and voice != VOICE_BY_GENDER[gender]:
            raise ValueError(
                f"Scene {scene_id}: source.voice {voice!r} does not match "
                f"persona_gender {gender!r} (expected {VOICE_BY_GENDER[gender]!r})"
            )
        if scene.get("replace_mode") == "multi_job":
            ref_count = len(scene.get("references") or [])
            if ref_count < min_refs:
                raise ValueError(
                    f"Scene {scene_id}: multi_job needs at least {min_refs} references, got {ref_count}"
                )


def compare_timing_for_plan(plan: dict, *, multi_sample: bool) -> dict[str, float]:
    """Compare MP4 pacing from plan `compare_timing` (shorter slider = snappier beats)."""
    raw = plan.get("compare_timing") or {}
    if multi_sample:
        return {
            "hook_seconds": float(raw.get("hook_seconds", 0)),
            "slider_seconds": float(raw.get("slider_seconds", 1.75)),
            "hold_output_seconds": float(raw.get("hold_output_seconds", 0)),
            "outro_seconds": float(raw.get("outro_seconds", 0)),
            "transition_seconds": float(raw.get("transition_seconds", 0)),
        }
    return {
        "hook_seconds": float(raw.get("hook_seconds_single", raw.get("hook_seconds", 1.0))),
        "slider_seconds": float(raw.get("slider_seconds_single", raw.get("slider_seconds", 2.0))),
        "hold_output_seconds": float(raw.get("hold_output_seconds_single", raw.get("hold_output_seconds", 1.0))),
        "outro_seconds": float(raw.get("outro_seconds_single", raw.get("outro_seconds", 1.0))),
        "transition_seconds": float(raw.get("transition_seconds", 0)),
    }


def trim_video(source: Path, destination: Path, seconds: float) -> None:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg not found on PATH")
    destination.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [ffmpeg, "-y", "-i", str(source), "-t", str(seconds), "-c", "copy", str(destination)],
        check=True,
        capture_output=True,
    )


def generate_hero(path: Path, plan: dict, api_key: str, *, fresh: bool) -> str:
    if path.exists() and not fresh:
        print(f"Reusing hero {path}")
        return upload_file(path, api_key)
    result = run_prediction(
        "p-image",
        {
            "prompt": f"{plan['style_bible']} {plan['hero_prompt']}",
            "aspect_ratio": "16:9",
            "seed": plan.get("hero_seed", plan["project_seed"]),
        },
        api_key,
        label="hero p-image",
    )
    download_file(result["generation_url"], path, api_key)
    return upload_file(path, api_key)


def edit_still(
    *,
    hero_url: str,
    edit_prompt: str,
    plan: dict,
    out_path: Path,
    api_key: str,
    label: str,
) -> str:
    if out_path.exists():
        print(f"Reusing still {out_path}")
        return upload_file(out_path, api_key)
    result = run_prediction(
        "p-image-edit",
        {
            "prompt": f"{plan['style_bible']} {edit_prompt}",
            "images": [hero_url],
        },
        api_key,
        label=f"{label} edit",
    )
    download_file(result["generation_url"], out_path, api_key)
    return upload_file(out_path, api_key)


def generate_reference_still(
    *,
    prompt: str,
    seed: int,
    plan: dict,
    out_path: Path,
    api_key: str,
    label: str,
) -> str:
    if out_path.exists():
        print(f"Reusing reference {out_path}")
        return upload_file(out_path, api_key)
    result = run_prediction(
        "p-image",
        {
            "prompt": f"{plan['style_bible']} {prompt}",
            "aspect_ratio": "16:9",
            "seed": seed,
        },
        api_key,
        label=f"{label} p-image",
    )
    download_file(result["generation_url"], out_path, api_key)
    return upload_file(out_path, api_key)


def source_video_prompt(source: dict) -> str:
    prompt = source["video_prompt"].strip()
    if prompt.lower().startswith("camera moves continuously"):
        return prompt
    return (
        "Camera moves continuously for the full clip — never static or locked-off. "
        + prompt
    )


def render_avatar_scene(scene: dict, ctx: dict, api_key: str, *, run_phase: str = "all") -> dict:
    scene_id = scene["id"]
    out_dir = ctx["out_dir"]
    clip_path = out_dir / "clips" / f"{scene_id:02d}_avatar.mp4"
    if clip_path.exists() and clip_path.stat().st_size > 0 and run_phase != "stills":
        print(f"Reusing {clip_path}")
        return {"id": scene_id, "type": "avatar", "clip": str(clip_path)}

    still_path = out_dir / "stills" / f"scene{scene_id:02d}.jpeg"
    still_url = edit_still(
        hero_url=ctx["hero_url"],
        edit_prompt=scene["still_edit"],
        plan=ctx["plan"],
        out_path=still_path,
        api_key=api_key,
        label=f"scene {scene_id}",
    )
    if run_phase == "stills":
        return {"id": scene_id, "type": "avatar", "phase": "stills", "still": str(still_path)}

    result = run_prediction(
        "p-video-avatar",
        {
            "image": still_url,
            "voice_script": scene["voice_script"],
            "voice": ctx["cast"]["voice"],
            "voice_language": ctx["cast"]["voice_language"],
            "voice_prompt": ctx["cast"]["voice_prompt"],
            "video_prompt": source_video_prompt(scene),
            "resolution": ctx["avatar_resolution"],
            "seed": ctx["project_seed"] + scene_id,
        },
        api_key,
        label=f"scene {scene_id} avatar",
    )
    download_file(result["generation_url"], clip_path, api_key)
    return {"id": scene_id, "type": "avatar", "clip": str(clip_path), "still": str(still_path)}


def render_source_plate(scene: dict, ctx: dict, api_key: str) -> str:
    """Build the source still for p-video-avatar / I2V (hero edit or fresh p-image plate)."""
    scene_id = scene["id"]
    source = scene["source"]
    out_dir = ctx["out_dir"]
    still_path = out_dir / "stills" / f"scene{scene_id:02d}_source_plate.jpeg"
    plate_mode = source.get("plate_mode", "hero_edit")
    if plate_mode == "p-image":
        prompt = source.get("plate_prompt") or source.get("still_edit", "")
        if not prompt:
            raise ValueError(f"Scene {scene_id}: plate_mode p-image requires plate_prompt")
        seed = int(source.get("plate_seed", ctx["project_seed"] + scene_id * 1000))
        return generate_reference_still(
            prompt=reference_image_prompt(
                scene,
                {"prompt": prompt, "beat_label": "source plate"},
                swap_visual_bible=ctx.get("swap_visual_bible", ""),
            ),
            seed=seed,
            plan=ctx["plan"],
            out_path=still_path,
            api_key=api_key,
            label=f"scene {scene_id} source plate",
        )
    return edit_still(
        hero_url=ctx["hero_url"],
        edit_prompt=source["still_edit"],
        plan=ctx["plan"],
        out_path=still_path,
        api_key=api_key,
        label=f"scene {scene_id} source plate",
    )


def render_source_video(scene: dict, ctx: dict, api_key: str) -> Path:
    scene_id = scene["id"]
    source = scene["source"]
    out_dir = ctx["out_dir"]
    source_full = out_dir / "sources" / f"scene{scene_id:02d}_original_full.mp4"
    source_trim = out_dir / "sources" / f"scene{scene_id:02d}_original.mp4"
    if source_trim.exists() and source_trim.stat().st_size > 0:
        print(f"Reusing {source_trim}")
        return source_trim

    still_url = render_source_plate(scene, ctx, api_key)

    mode = source.get("mode", "avatar")
    if mode == "p-video-i2v":
        result = run_prediction(
            "p-video",
            {
                "prompt": f"{ctx['style_bible']} {source['video_prompt']}",
                "image": still_url,
                "duration": source.get("duration", 5),
                "resolution": source.get("resolution", ctx["replace_resolution"]),
                "fps": 24,
            },
            api_key,
            label=f"scene {scene_id} source p-video",
        )
        download_file(result["generation_url"], source_full, api_key)
    else:
        source_cast = source_cast_for(scene, source, ctx["cast"])
        result = run_prediction(
            "p-video-avatar",
            {
                "image": still_url,
                "voice_script": source["voice_script"],
                "voice": source_cast["voice"],
                "voice_language": source_cast["voice_language"],
                "voice_prompt": source_cast["voice_prompt"],
                "video_prompt": source_video_prompt(source),
                "resolution": ctx["avatar_resolution"],
                "seed": ctx["project_seed"] + scene_id * 1000,
            },
            api_key,
            label=f"scene {scene_id} source avatar",
        )
        download_file(result["generation_url"], source_full, api_key)

    trim_seconds = ctx.get("source_trim_seconds")
    if trim_seconds:
        trim_video(source_full, source_trim, trim_seconds)
    else:
        shutil.copy2(source_full, source_trim)
    return source_trim


def instruction_for_reference(
    scene: dict, reference: dict, *, index: int, lip_sync_policy: str = ""
) -> str:
    if reference.get("instruction_prompt"):
        prompt = reference["instruction_prompt"]
    elif scene.get("replace_mode") == "single_call":
        prompt = scene["instruction_prompt"]
    else:
        source = scene.get("source", {})
        subject = source.get("subject_in_video", "the person on camera")
        cues = reference.get("identity_cues", "").strip()
        prompt = (
            f"Replace {subject} with the identity shown in the reference image. "
            f"{cues + ' ' if cues else ''}"
            "Preserve exact motion, timing, camera movement, background, and audio."
        )
    policy = lip_sync_policy.strip()
    if policy and "lip sync" not in prompt.lower():
        prompt = f"{prompt.strip()} {policy}"
    return prompt.strip()


def instruction_for_multi_image_beat(scene: dict, beat: dict, *, lip_sync_policy: str = "") -> str:
    prompt = beat.get("instruction_prompt") or scene.get("instruction_prompt")
    if not prompt:
        raise ValueError("multi_image_beat requires instruction_prompt")
    policy = lip_sync_policy.strip()
    if policy and "lip sync" not in prompt.lower():
        prompt = f"{prompt.strip()} {policy}"
    return prompt.strip()


def append_multi_image_beat(
    *,
    scene: dict,
    scene_id: int,
    references: list,
    reference_urls: list[str],
    video_url: str,
    ctx: dict,
    api_key: str,
    out_dir: Path,
    plan: dict,
    replaced_paths: list[Path],
    sample_specs: list[dict],
) -> None:
    """Optional extra slider beat: one p-video-replace call with 2–4 reference images."""
    beat = scene.get("multi_image_beat")
    if not beat:
        return
    if ctx.get("only_ref") is not None:
        print(f"Skipping multi_image_beat for scene {scene_id} (--only-ref {ctx['only_ref']})")
        return

    indices = beat.get("reference_indices") or []
    if len(indices) < 2:
        raise ValueError(f"Scene {scene_id}: multi_image_beat needs at least 2 reference_indices")
    if len(indices) > 4:
        raise ValueError(f"Scene {scene_id}: multi_image_beat supports at most 4 reference_indices")
    for index in indices:
        if index < 1 or index > len(references):
            raise ValueError(
                f"Scene {scene_id}: multi_image_beat reference_indices must be 1..{len(references)}, got {index}"
            )

    image_urls = [reference_urls[index - 1] for index in indices]
    replaced_path = out_dir / "clips" / f"{scene_id:02d}_replaced_multi.mp4"
    if replaced_path.exists() and replaced_path.stat().st_size > 0:
        print(f"Reusing {replaced_path}")
    else:
        result = run_replace_job(
            video_url=video_url,
            image_urls=image_urls,
            instruction_prompt=instruction_for_multi_image_beat(
                scene, beat, lip_sync_policy=plan.get("lip_sync_policy", "")
            ),
            resolution=ctx["replace_resolution"],
            api_key=api_key,
            label=f"scene {scene_id} replace multi-image ({len(indices)} refs)",
        )
        download_file(result["generation_url"], replaced_path, api_key)
    replaced_paths.append(replaced_path)
    sample_specs.append(
        {
            "output": str(replaced_path.relative_to(out_dir)),
            "output_label": beat.get("output_label", "Multi-image"),
            "beat_label": beat.get("beat_label", "Multi-image"),
        }
    )


def run_replace_job(
    *,
    video_url: str,
    image_urls: list[str],
    instruction_prompt: str,
    resolution: str,
    api_key: str,
    label: str,
) -> dict:
    return run_prediction(
        "p-video-replace",
        {
            "video": video_url,
            "images": image_urls,
            "resolution": resolution,
            "target_fps": "original",
            "save_audio": True,
            "instruction_prompt": instruction_prompt,
        },
        api_key,
        label=label,
    )


def reference_images_for_compare(
    scene: dict,
    references: list[dict],
    reference_paths: list[Path],
    *,
    out_dir: Path,
) -> list[dict[str, str]]:
    """All scene reference stills for the top-right panel on compare MP4s."""
    if scene.get("reference_inset") == "none":
        return []
    images: list[dict[str, str]] = []
    for reference, path in zip(references, reference_paths):
        if reference.get("show_reference") is False:
            continue
        images.append(
            {
                "reference": str(path.relative_to(out_dir)),
                "label": reference.get(
                    "reference_label", reference.get("output_label", "Reference")
                ),
            }
        )
    return images


def resolve_python_for_compare() -> str:
    """Use a Python that has Pillow (bash/login shells often default to CLT python3)."""
    override = os.environ.get("PRUNA_PYTHON")
    if override:
        return override
    candidates: list[str] = []
    for path in (sys.executable, shutil.which("python3"), "/opt/homebrew/bin/python3", "/usr/local/bin/python3"):
        if path and path not in candidates:
            candidates.append(path)
    for candidate in candidates:
        try:
            subprocess.run(
                [candidate, "-c", "import PIL"],
                check=True,
                capture_output=True,
            )
            return candidate
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    return sys.executable


def render_slider(compare_config_path: Path, out_dir: Path, compare_path: Path) -> None:
    slider_script = sibling_script("generate_video_comparison.py")
    python = resolve_python_for_compare()
    config_arg = compare_config_path.resolve()
    subprocess.run(
        [python, str(slider_script), "--config", str(config_arg)],
        check=True,
        cwd=str(out_dir),
    )
    nested_compare = out_dir / "clips" / "clips" / compare_path.name
    if nested_compare.exists() and nested_compare != compare_path:
        compare_path.parent.mkdir(parents=True, exist_ok=True)
        if compare_path.exists():
            compare_path.unlink()
        nested_compare.replace(compare_path)
        nested_dir = nested_compare.parent
        if nested_dir.exists() and not any(nested_dir.iterdir()):
            nested_dir.rmdir()


def render_replace_scene(
    scene: dict, ctx: dict, api_key: str, *, plan: dict, run_phase: str = "all"
) -> dict:
    scene_id = scene["id"]
    out_dir = ctx["out_dir"]
    compare_path = out_dir / "clips" / f"{scene_id:02d}_compare.mp4"
    compare_config_path = out_dir / "clips" / f"{scene_id:02d}_compare_config.json"
    references = scene["references"]
    replace_mode = scene.get("replace_mode", "multi_job")

    if run_phase == "render":
        if not compare_config_path.exists():
            raise FileNotFoundError(
                f"Missing {compare_config_path} — run --phase video first"
            )
        render_slider(compare_config_path, out_dir, compare_path)
        return {
            "id": scene_id,
            "type": "replace",
            "compare": str(compare_path),
            "compare_config": str(compare_config_path),
        }

    if compare_path.exists() and compare_path.stat().st_size > 0 and scene_id < ctx.get("from_scene", 1):
        print(f"Reusing {compare_path}")
        return {"id": scene_id, "type": "replace", "compare": str(compare_path)}

    reference_paths: list[Path] = []
    reference_urls: list[str] = []

    for index, reference in enumerate(references, start=1):
        ref_path = out_dir / "references" / f"scene{scene_id:02d}_{index:02d}.jpeg"
        if ref_path.exists() and run_phase in ("stills", "video", "all"):
            print(f"Reusing reference {ref_path}")
        else:
            generate_reference_still(
                prompt=reference_image_prompt(
                    scene, reference, swap_visual_bible=ctx.get("swap_visual_bible", "")
                ),
                seed=reference["seed"],
                plan=ctx["plan"],
                out_path=ref_path,
                api_key=api_key,
                label=f"scene {scene_id} ref {index}",
            )
        reference_paths.append(ref_path)
        if run_phase != "stills":
            reference_urls.append(upload_file(ref_path, api_key))

    still_path = out_dir / "stills" / f"scene{scene_id:02d}_source_plate.jpeg"
    source_trim = out_dir / "sources" / f"scene{scene_id:02d}_original.mp4"
    if (
        not still_path.exists()
        or run_phase == "stills"
        or (run_phase in ("video", "all") and not source_trim.exists())
    ):
        render_source_plate(scene, ctx, api_key)

    if run_phase == "stills":
        return {
            "id": scene_id,
            "type": "replace",
            "phase": "stills",
            "references": [str(path) for path in reference_paths],
            "source_plate": str(still_path),
        }

    source_trim = render_source_video(scene, ctx, api_key)
    video_url = upload_file(source_trim, api_key)

    replaced_paths: list[Path] = []
    sample_specs: list[dict] = []

    if replace_mode == "single_call":
        replaced_path = out_dir / "clips" / f"{scene_id:02d}_replaced.mp4"
        if replaced_path.exists() and replaced_path.stat().st_size > 0:
            print(f"Reusing {replaced_path}")
        else:
            result = run_replace_job(
                video_url=video_url,
                image_urls=reference_urls,
                instruction_prompt=scene["instruction_prompt"],
                resolution=ctx["replace_resolution"],
                api_key=api_key,
                label=f"scene {scene_id} replace",
            )
            download_file(result["generation_url"], replaced_path, api_key)
        replaced_paths.append(replaced_path)
        ref_images = reference_images_for_compare(
            scene, references, reference_paths, out_dir=out_dir
        )
        compare_config = {
            "source": str(source_trim.relative_to(out_dir)),
            "output": str(replaced_path.relative_to(out_dir)),
            "render": str(compare_path.relative_to(out_dir)),
            "title": scene["slider_title"],
            "source_label": scene.get("source_label", "Original footage"),
            "output_label": scene.get("output_label", "Replaced"),
            "timing": compare_timing_for_plan(plan, multi_sample=False),
        }
        if ref_images:
            compare_config["reference_images"] = ref_images
    else:
        only_ref = ctx.get("only_ref")
        for index, reference in enumerate(references, start=1):
            replaced_path = out_dir / "clips" / f"{scene_id:02d}_replaced_{index:02d}.mp4"
            if only_ref is not None and index != only_ref:
                if replaced_path.exists() and replaced_path.stat().st_size > 0:
                    print(f"Skipping replace {index} (--only-ref {only_ref})")
                    replaced_paths.append(replaced_path)
                    sample_specs.append(
                        {
                            "output": str(replaced_path.relative_to(out_dir)),
                            "output_label": reference.get("output_label", "Replaced"),
                            "beat_label": reference.get("beat_label", f"Variant {index}"),
                        }
                    )
                else:
                    print(f"Warning: missing {replaced_path} (skipped by --only-ref {only_ref})")
                continue
            if replaced_path.exists() and replaced_path.stat().st_size > 0:
                print(f"Reusing {replaced_path}")
            else:
                result = run_replace_job(
                    video_url=video_url,
                    image_urls=[reference_urls[index - 1]],
                    instruction_prompt=instruction_for_reference(
                        scene, reference, index=index, lip_sync_policy=plan.get("lip_sync_policy", "")
                    ),
                    resolution=ctx["replace_resolution"],
                    api_key=api_key,
                    label=f"scene {scene_id} replace {index}",
                )
                download_file(result["generation_url"], replaced_path, api_key)
            replaced_paths.append(replaced_path)
            sample_specs.append(
                {
                    "output": str(replaced_path.relative_to(out_dir)),
                    "output_label": reference.get("output_label", "Replaced"),
                    "beat_label": reference.get("beat_label", f"Variant {index}"),
                }
            )
        append_multi_image_beat(
            scene=scene,
            scene_id=scene_id,
            references=references,
            reference_urls=reference_urls,
            video_url=video_url,
            ctx=ctx,
            api_key=api_key,
            out_dir=out_dir,
            plan=plan,
            replaced_paths=replaced_paths,
            sample_specs=sample_specs,
        )
        ref_images = reference_images_for_compare(
            scene, references, reference_paths, out_dir=out_dir
        )
        compare_config = {
            "source": str(source_trim.relative_to(out_dir)),
            "render": str(compare_path.relative_to(out_dir)),
            "title": scene["slider_title"],
            "source_label": scene.get("source_label", "Original footage"),
            "compare_mode": "single_pass_multi_slider",
            "samples": sample_specs,
            "timing": compare_timing_for_plan(plan, multi_sample=True),
        }
        if ref_images:
            compare_config["reference_images"] = ref_images

    compare_config_path.write_text(json.dumps(compare_config, indent=2) + "\n", encoding="utf-8")
    if run_phase == "video":
        return {
            "id": scene_id,
            "type": "replace",
            "phase": "video",
            "source": str(source_trim),
            "replaced": [str(path) for path in replaced_paths],
            "compare_config": str(compare_config_path),
        }
    render_slider(compare_config_path, out_dir, compare_path)

    return {
        "id": scene_id,
        "type": "replace",
        "use_case": scene.get("use_case"),
        "source": str(source_trim),
        "references": [str(path) for path in reference_paths],
        "replaced": [str(path) for path in replaced_paths],
        "compare": str(compare_path),
        "compare_config": str(compare_config_path),
    }


def scene_clip_path(out_dir: Path, scene: dict) -> Path:
    scene_id = scene["id"]
    if scene["type"] == "avatar":
        return out_dir / "clips" / f"{scene_id:02d}_avatar.mp4"
    return out_dir / "clips" / f"{scene_id:02d}_compare.mp4"


def all_scenes_ready(out_dir: Path, scenes: list[dict]) -> bool:
    for scene in scenes:
        clip = scene_clip_path(out_dir, scene)
        if not clip.exists() or clip.stat().st_size == 0:
            return False
    return True


def assemble_final(out_dir: Path, scenes: list[dict]) -> Path:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg not found on PATH")
    concat_list = out_dir / "concat_list.txt"
    lines: list[str] = []
    for scene in scenes:
        clip = scene_clip_path(out_dir, scene)
        if not clip.exists():
            raise FileNotFoundError(f"Missing clip for scene {scene['id']}: {clip}")
        lines.append(f"file '{clip.resolve()}'")
    concat_list.write_text("\n".join(lines) + "\n", encoding="utf-8")
    final_path = out_dir / "p_video_replace_announcement.mp4"
    copy_cmd = [
        ffmpeg,
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_list),
        "-c",
        "copy",
        str(final_path),
    ]
    result = subprocess.run(copy_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        reencode_cmd = [
            ffmpeg,
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_list),
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "18",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-movflags",
            "+faststart",
            str(final_path),
        ]
        subprocess.run(reencode_cmd, check=True)
    return final_path


def maybe_add_background_music(
    final_path: Path,
    out_dir: Path,
    plan: dict,
    *,
    enabled: bool,
    prompt: str | None,
    volume: float | None,
) -> Path | None:
    cfg = music_config_from_plan(plan)
    if not enabled and not cfg:
        return None
    if cfg and not cfg.get("enabled", True) and not enabled:
        return None
    return apply_background_music(
        final_path,
        out_dir,
        plan=plan,
        prompt=prompt,
        volume=volume,
    )


def write_manifest(out_dir: Path, plan: dict, final_path: Path, *, music_path: Path | None = None) -> Path:
    manifest_lines = [
        "# P-Video-Replace launch reel",
        "",
        f"- **Final:** `{final_path.name}`",
        f"- **Plan:** `announcement_plan.json`",
        "",
    ]
    if music_path:
        manifest_lines.extend(
            [
                f"- **With music:** `{music_path.name}`",
                "",
            ]
        )
    manifest_lines.extend(
        [
        "## Scenes",
        "",
        "| # | Type | Target | Use case |",
        "|---|------|--------|----------|",
        ]
    )
    for scene in plan["scenes"]:
        target = scene.get("replace_target", "—")
        use_case = scene.get("use_case", scene["type"])
        manifest_lines.append(
            f"| {scene['id']} | {scene['type']} | {target} | {use_case} |"
        )
    manifest_path = out_dir / "manifest.md"
    manifest_path.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")
    return manifest_path


def load_generation_status(out_dir: Path) -> dict:
    status_path = out_dir / "generation_status.json"
    if not status_path.exists():
        return {"phase_a_approved": False, "scenes": []}
    try:
        data = json.loads(status_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"phase_a_approved": False, "scenes": []}
    if isinstance(data, list):
        return {"phase_a_approved": False, "scenes": data}
    return data


def write_generation_status(out_dir: Path, status: dict) -> None:
    (out_dir / "generation_status.json").write_text(
        json.dumps(status, indent=2) + "\n", encoding="utf-8"
    )


def ensure_phase_b_allowed(out_dir: Path, *, approve_flag: bool, skip_gate: bool) -> None:
    if skip_gate or approve_flag:
        return
    status = load_generation_status(out_dir)
    if status.get("phase_a_approved"):
        return
    raise SystemExit(
        "Phase B blocked: review stills in references/ and stills/, then re-run with "
        "--approve-stills or set phase_a_approved in generation_status.json"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, default=None, help="Scene plan JSON path")
    parser.add_argument("--out-dir", type=Path, default=None, help="Output directory (default: ./output/...)")
    parser.add_argument(
        "--phase",
        choices=("stills", "video", "render", "all"),
        default="stills",
        help="Generation phase (default: stills)",
    )
    parser.add_argument(
        "--approve-stills",
        action="store_true",
        help="Mark Phase A approved and allow --phase video",
    )
    parser.add_argument(
        "--yes-skip-stills-gate",
        action="store_true",
        help="Allow --phase all without stills approval (use with care)",
    )
    parser.add_argument("--fresh", action="store_true", help="Delete generated assets before running")
    parser.add_argument("--from-scene", type=int, default=1, help="Start at this scene id")
    parser.add_argument("--through-scene", type=int, default=None, help="Stop after this scene id")
    parser.add_argument(
        "--only-ref",
        type=int,
        default=None,
        metavar="N",
        help="multi_job: only call p-video-replace for reference index N (reuse other clips)",
    )
    parser.add_argument(
        "--force-ref",
        type=int,
        default=None,
        metavar="N",
        help="multi_job: delete clips/NN_replaced_NN.mp4 before replace (pair with --only-ref)",
    )
    parser.add_argument(
        "--assemble-only",
        action="store_true",
        help="Concat existing scene clips and write manifest (no API calls)",
    )
    parser.add_argument(
        "--background-music",
        action="store_true",
        help="After assembly, generate Stable Audio 2.5 bed (Replicate) and mix under final MP4",
    )
    parser.add_argument(
        "--music-prompt",
        default=None,
        help="Override background_music.prompt from plan",
    )
    parser.add_argument(
        "--music-volume",
        type=float,
        default=None,
        help="Bed volume 0–1 (default 0.12 or plan background_music.volume)",
    )
    args = parser.parse_args()

    plan_path = args.plan
    if plan_path is None:
        env_plan = os.environ.get("REPLACE_PLAN", "").strip()
        plan_path = Path(env_plan) if env_plan else default_template("scene-plan.template.json")
        if not plan_path.exists():
            plan_path = Path(os.environ.get("REPLACE_PLAN", DEFAULT_PLAN))
    out_dir = args.out_dir or Path(os.environ.get("REPLACE_OUT", DEFAULT_OUT))
    out_dir.mkdir(parents=True, exist_ok=True)
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    validate_plan_scenes(plan)

    if args.assemble_only:
        if not all_scenes_ready(out_dir, plan["scenes"]):
            missing = [
                scene["id"]
                for scene in plan["scenes"]
                if not scene_clip_path(out_dir, scene).exists()
            ]
            raise SystemExit(f"Missing clips for scenes: {missing}")
        final_path = assemble_final(out_dir, plan["scenes"])
        music_path = maybe_add_background_music(
            final_path,
            out_dir,
            plan,
            enabled=args.background_music,
            prompt=args.music_prompt,
            volume=args.music_volume,
        )
        manifest_path = write_manifest(out_dir, plan, final_path, music_path=music_path)
        print(f"Wrote {final_path}")
        if music_path:
            print(f"Wrote {music_path}")
        print(f"Wrote {manifest_path}")
        return 0

    if args.fresh:
        for sub in ("clips", "stills", "references", "sources"):
            target = out_dir / sub
            if target.exists():
                shutil.rmtree(target)
        for name in (
            "generation_status.json",
            "concat_list.txt",
            "p_video_replace_announcement.mp4",
            "run.log",
        ):
            path = out_dir / name
            if path.exists():
                path.unlink()

    for sub in ("clips", "stills", "references", "sources"):
        (out_dir / sub).mkdir(exist_ok=True)

    if args.approve_stills:
        status = load_generation_status(out_dir)
        status["phase_a_approved"] = True
        write_generation_status(out_dir, status)
        print("Marked phase_a_approved=true in generation_status.json")
        if args.phase == "stills" and not args.fresh:
            return 0

    run_phase = args.phase
    if run_phase in ("video", "all"):
        ensure_phase_b_allowed(
            out_dir, approve_flag=args.approve_stills, skip_gate=args.yes_skip_stills_gate
        )

    needs_api = run_phase in ("stills", "video", "all")
    api_key = require_api_key() if needs_api else ""
    ctx = {
        "out_dir": out_dir,
        "plan": plan,
        "project_seed": plan["project_seed"],
        "style_bible": plan["style_bible"],
        "swap_visual_bible": plan.get("swap_visual_bible", ""),
        "cast": plan["cast"],
        "source_trim_seconds": plan.get("source_trim_seconds"),
        "avatar_resolution": plan["avatar_resolution"],
        "replace_resolution": plan["replace_resolution"],
        "from_scene": args.from_scene,
        "only_ref": args.only_ref,
    }

    status_doc = load_generation_status(out_dir)
    results: list[dict] = status_doc.get("scenes", [])

    if needs_api:
        hero_path = out_dir / "stills" / "hero.jpeg"
        print(f"Phase A/B — hero anchor ({run_phase})")
        ctx["hero_url"] = generate_hero(hero_path, plan, api_key, fresh=args.fresh)
    else:
        ctx["hero_url"] = ""

    print(f"Scenes — phase={run_phase} (sequential; resume supported)")
    sys.stdout.flush()
    effective_phase = run_phase if run_phase != "all" else "all"
    if args.force_ref is not None:
        for scene in plan["scenes"]:
            if scene.get("replace_mode", "multi_job") != "multi_job":
                continue
            forced = out_dir / "clips" / f"{scene['id']:02d}_replaced_{args.force_ref:02d}.mp4"
            if forced.exists():
                forced.unlink()
                print(f"Removed {forced} (--force-ref {args.force_ref})")

    for scene in plan["scenes"]:
        if scene["id"] < args.from_scene:
            print(f"Skipping scene {scene['id']} (before --from-scene {args.from_scene})")
            continue
        if args.through_scene is not None and scene["id"] > args.through_scene:
            print(f"Skipping scene {scene['id']} (after --through-scene {args.through_scene})")
            continue
        if scene["type"] == "avatar":
            if run_phase == "render":
                continue
            result = render_avatar_scene(scene, ctx, api_key, run_phase=effective_phase)
            print(f"Done scene {scene['id']} (avatar, {run_phase})")
        elif scene["type"] == "replace":
            result = render_replace_scene(
                scene, ctx, api_key, plan=plan, run_phase=effective_phase
            )
            print(f"Done scene {scene['id']} (replace, {run_phase})")
        else:
            raise ValueError(f"Scene {scene['id']} has unsupported type {scene['type']!r}")
        results = [item for item in results if item.get("id") != scene["id"]]
        results.append(result)
        status_doc["scenes"] = sorted(results, key=lambda x: x["id"])
        if run_phase == "stills":
            status_doc["phase_a_approved"] = False
        write_generation_status(out_dir, status_doc)
        sys.stdout.flush()

    if run_phase in ("stills", "video", "render"):
        print(f"Phase {run_phase} complete — review outputs under {out_dir}")
        if run_phase == "stills":
            print("Reply with fixes or re-run with --approve-stills --phase video")
        return 0

    print("Phase 3 — assembly")
    if not all_scenes_ready(out_dir, plan["scenes"]):
        print("Partial run — skipping final assembly until all scenes are complete")
        return 0
    final_path = assemble_final(out_dir, plan["scenes"])
    music_path = maybe_add_background_music(
        final_path,
        out_dir,
        plan,
        enabled=args.background_music,
        prompt=args.music_prompt,
        volume=args.music_volume,
    )
    manifest_path = write_manifest(out_dir, plan, final_path, music_path=music_path)
    print(f"Wrote {final_path}")
    if music_path:
        print(f"Wrote {music_path}")
    print(f"Wrote {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
