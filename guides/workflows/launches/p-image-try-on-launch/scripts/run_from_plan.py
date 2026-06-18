#!/usr/bin/env python3
"""Run a p-image-try-on launch reel from a JSON scene plan.

Phases: stills → video → tts → assemble (+ optional background music).
Default motion is ``showcase`` — garment ref → person → slider → try-on hold (one aspect ratio).

Single-scene redo: set ``force_rerender`` on one scene, delete its clip/audio, ``--phase video``.
See SKILL.md § Redo one scene and § CTA avatar.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

try:
    from PIL import Image
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Pillow required: pip install Pillow") from exc

_SCRIPT_DIR = Path(__file__).resolve().parent
_workflows = _SCRIPT_DIR.parent
while _workflows.name != "workflows" and _workflows.parent != _workflows:
    _workflows = _workflows.parent
_SHARED = _workflows / "_shared" / "scripts"
if str(_SHARED) not in sys.path:
    sys.path.insert(0, str(_SHARED))
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from concat_clips import concat_clips, probe_duration  # noqa: E402
from generate_tryon_showcase import (  # noqa: E402
    FlashSwapTiming,
    ShowcaseJob,
    Timing,
    fit_pose_timing_for_narration,
    flash_timing_for_narration,
    garment_flash_timing_for_narration,
    render_fit_poses,
    render_flash_swaps,
    render_garment_flash_montage,
    render_garment_reel,
    render_ladder,
    render_rapid,
    render_showcase,
)
from generation_gate import (  # noqa: E402
    apply_approve_flags,
    ensure_phase_a_allowed,
    ensure_phase_b_allowed,
    load_generation_status,
    write_generation_status,
)
from launch_background_music import apply_background_music, music_config_from_plan, video_has_audio  # noqa: E402
from pruna_api import download_file, require_api_key, run_prediction, upload_file  # noqa: E402
from pruna_paths import default_out_dir, repo_root  # noqa: E402
from replicate_api import download_url, require_replicate_token, run_model_prediction  # noqa: E402

DEFAULT_TEMPLATE = _SCRIPT_DIR.parent / "templates/scene-plan.template.json"
DEFAULT_OUT = default_out_dir("p-image-try-on-launch")
NARRATION_MODEL = "google/gemini-3.1-flash-tts"
VOICE_BY_GENDER = {
    "female": "Zephyr (Female)",
    "male": "Puck (Male)",
}
AVATAR_TTS_VOICE = {
    "female": "Kore",
    "male": "Charon",
}
DEFAULT_AVATAR_VIDEO_PROMPT = (
    "Medium close-up speaking directly to camera for the entire clip. "
    "Clear visible lip movement matching speech, natural jaw and mouth articulation, "
    "subtle continuous handheld push-in, eyes to lens, expressive but stable face."
)


def canvas_size(plan: dict) -> tuple[int, int]:
    defaults = plan.get("defaults", {})
    if "output_width" in defaults and "output_height" in defaults:
        return int(defaults["output_width"]), int(defaults["output_height"])
    ratio = defaults.get("aspect_ratio", "9:16")
    if ratio == "9:16":
        return 1080, 1920
    if ratio == "16:9":
        return 1920, 1080
    if ratio == "1:1":
        return 1080, 1080
    return 1080, 1920


def normalize_image(path: Path, width: int, height: int) -> None:
    with Image.open(path) as raw:
        src_w, src_h = raw.size
        if (src_w, src_h) == (width, height):
            return
        scale = max(width / src_w, height / src_h)
        new_w = max(1, int(round(src_w * scale)))
        new_h = max(1, int(round(src_h * scale)))
        resized = raw.convert("RGB").resize((new_w, new_h), Image.Resampling.LANCZOS)
        left = (new_w - width) // 2
        top = (new_h - height) // 2
        cropped = resized.crop((left, top, left + width, top + height))
        cropped.save(path)


def crop_avatar_portrait(src: Path, dest: Path, width: int, height: int, *, crop_top_ratio: float = 0.62) -> Path:
    """Upper-body portrait crop from full-body try-on — larger face for lip sync."""
    with Image.open(src) as raw:
        img = raw.convert("RGB")
        w, h = img.size
        crop_h = max(1, int(h * crop_top_ratio))
        cropped = img.crop((0, 0, w, crop_h))
        scale = max(width / cropped.width, height / cropped.height)
        new_w = max(1, int(round(cropped.width * scale)))
        new_h = max(1, int(round(cropped.height * scale)))
        resized = cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)
        left = (new_w - width) // 2
        top = 0  # ponytail: anchor top — lip-sync needs face, not center crop
        framed = resized.crop((left, top, left + width, top + height))
    dest.parent.mkdir(parents=True, exist_ok=True)
    framed.save(dest)
    return dest


def normalize_video(path: Path, width: int, height: int) -> None:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg not found")
    tmp = path.with_suffix(".norm.mp4")
    subprocess.run(
        [
            ffmpeg,
            "-y",
            "-i",
            str(path),
            "-vf",
            f"scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height}",
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "18",
            "-c:a",
            "copy",
            "-movflags",
            "+faststart",
            str(tmp),
        ],
        check=True,
        capture_output=True,
    )
    shutil.move(tmp, path)


def ensure_audio_track(path: Path) -> None:
    """Add a silent AAC track so crossfade concat works on video-only clips."""
    if video_has_audio(path):
        return
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg not found")
    dur = probe_duration(path)
    tmp = path.with_suffix(".audiomux.mp4")
    subprocess.run(
        [
            ffmpeg,
            "-y",
            "-i",
            str(path),
            "-f",
            "lavfi",
            "-i",
            "anullsrc=r=24000:cl=mono",
            "-t",
            f"{dur:.3f}",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-movflags",
            "+faststart",
            str(tmp),
        ],
        check=True,
        capture_output=True,
    )
    shutil.move(tmp, path)


def style_wrap(plan: dict, prompt: str, *, bible_key: str = "style_bible", scene: dict | None = None) -> str:
    if scene and scene.get("style_bible"):
        bible = str(scene["style_bible"])
    else:
        bible = plan.get(bible_key) or plan.get("style_bible") or ""
    return f"{prompt.strip()} {bible.strip()}".strip()


def aspect_hint(plan: dict) -> str:
    ratio = plan.get("defaults", {}).get("aspect_ratio", "9:16")
    if ratio == "9:16":
        return "9:16 vertical portrait frame, full-bleed composition."
    if ratio == "16:9":
        return "16:9 horizontal landscape frame, full-bleed composition."
    return f"{ratio} frame, full-bleed composition."


def scene_dir(out_dir: Path, scene_id: str) -> Path:
    path = out_dir / "stills" / f"scene_{scene_id}"
    path.mkdir(parents=True, exist_ok=True)
    return path


def gen_p_image(
    prompt: str,
    plan: dict,
    dest: Path,
    api_key: str,
    *,
    seed: int | None,
    label: str,
    bible_key: str = "style_bible",
    scene: dict | None = None,
) -> None:
    width, height = canvas_size(plan)
    if dest.exists() and dest.stat().st_size > 0:
        normalize_image(dest, width, height)
        print(f"Reusing {dest.name}")
        return
    aspect = plan.get("defaults", {}).get("aspect_ratio", "9:16")
    full_prompt = f"{style_wrap(plan, prompt, bible_key=bible_key, scene=scene)} {aspect_hint(plan)}"
    payload: dict = {"prompt": full_prompt, "aspect_ratio": aspect}
    if seed is not None:
        payload["seed"] = seed
    result = run_prediction("p-image", payload, api_key, label=label)
    download_file(result["generation_url"], dest, api_key)
    normalize_image(dest, width, height)
    print(f"Wrote {dest}")


def gen_try_on(
    person: Path,
    garments: list[Path],
    dest: Path,
    plan: dict,
    api_key: str,
    label: str,
    *,
    garment_meta: list[dict] | None = None,
) -> None:
    width, height = canvas_size(plan)
    if dest.exists() and dest.stat().st_size > 0:
        normalize_image(dest, width, height)
        print(f"Reusing {dest.name}")
        return
    person_url = upload_file(person, api_key)
    garment_urls = [upload_file(g, api_key) for g in garments]
    payload = {
        "person_image": person_url,
        "garment_images": garment_urls,
        "output_format": "png",
        "preserve_input_size": True,
    }
    # ponytail: garment_types removed — API auto-classifies; field returns 400 if sent
    result = run_prediction("p-image-try-on", payload, api_key, label=label)
    download_file(result["generation_url"], dest, api_key)
    normalize_image(dest, width, height)
    print(f"Wrote {dest}")


def apply_garment_gender(prompt: str, gender: str | None, *, garment: dict | None = None) -> str:
    """Prefix garment still prompts when cut is not already gender-tagged."""
    if garment and garment.get("gender"):
        gender = str(garment["gender"]).lower()
    if not gender:
        return prompt
    lower = prompt.lower()
    male_markers = ("men's", "mens ", "men ", "male ", "man ", "boy's", "boys ")
    female_markers = ("women's", "womens ", "women ", "female ", "woman ", "girl's", "ladies ")
    if gender == "male":
        if any(m in lower for m in male_markers):
            return prompt
        return f"Men's {prompt[0].lower()}{prompt[1:]}" if prompt else prompt
    if gender == "female":
        if any(m in lower for m in female_markers):
            return prompt
        return f"Women's {prompt[0].lower()}{prompt[1:]}" if prompt else prompt
    return prompt


def resolve_garment_paths(scene: dict, sdir: Path, plan: dict, api_key: str) -> list[Path]:
    paths: list[Path] = []
    gender = scene.get("persona_gender")
    for i, garment in enumerate(scene.get("garments") or []):
        dest = sdir / f"garment_{i:02d}.png"
        prompt = apply_garment_gender(garment["prompt"], gender, garment=garment)
        gen_p_image(
            prompt,
            plan,
            dest,
            api_key,
            seed=garment.get("seed"),
            label=f"scene {scene['id']} garment {i}",
            bible_key="garment_bible",
            scene=scene,
        )
        paths.append(dest)
    return paths


def previous_still_source_scene(scenes: list[dict], scene: dict) -> str | None:
    idx = next(i for i, s in enumerate(scenes) if s["id"] == scene["id"])
    for prior in reversed(scenes[:idx]):
        if prior.get("person") and prior.get("garments"):
            return str(prior["id"])
    return None


def resolve_avatar_source_id(scene: dict, scenes: list[dict]) -> str:
    if scene.get("still_from_previous"):
        src_id = previous_still_source_scene(scenes, scene)
        if not src_id:
            raise RuntimeError(f"Scene {scene['id']}: no prior showcase scene for still_from_previous")
        return src_id
    if scene.get("still_from"):
        return str(scene["still_from"])
    return str(scene["id"])


def resolve_avatar_try_on_index(scene: dict, try_on_count: int) -> int:
    if "use_try_on_index" in scene:
        raw = int(scene["use_try_on_index"])
        if raw < 0:
            raw = try_on_count + raw
        return max(0, min(raw, try_on_count - 1))
    if scene.get("use_final_try_on") or scene.get("still_from_previous"):
        return max(0, try_on_count - 1)
    return max(0, try_on_count - 1)


def resolve_avatar_try_on_path(entry: dict, scene: dict) -> Path:
    if scene.get("use_try_on_all") and entry.get("try_on_all"):
        return Path(entry["try_on_all"])
    try_idx = int(
        entry.get("avatar_try_on_index", resolve_avatar_try_on_index(scene, len(entry["try_on"])))
    )
    return Path(entry["try_on"][try_idx])


def resolve_person_from_scene(scene: dict, manifest: dict, dest: Path, plan: dict) -> None:
    src_id = str(scene["person_from_scene"])
    src = manifest.get(src_id)
    if not src:
        raise RuntimeError(f"Scene {scene['id']}: person_from_scene {src_id} not in manifest yet")
    if scene.get("person_from_try_on_all"):
        if not src.get("try_on_all"):
            raise RuntimeError(f"Scene {scene['id']}: source {src_id} has no try_on_all")
        src_path = Path(src["try_on_all"])
    else:
        idx = int(scene.get("person_from_try_on_index", -1))
        if idx < 0:
            idx = len(src["try_on"]) + idx
        idx = max(0, min(idx, len(src["try_on"]) - 1))
        src_path = Path(src["try_on"][idx])
    shutil.copy2(src_path, dest)
    width, height = canvas_size(plan)
    normalize_image(dest, width, height)
    print(f"Scene {scene['id']} person ← {src_id} {src_path.name}")


def persona_gender_for_avatar(scene: dict, scenes: list[dict], src_id: str) -> str:
    for row in scenes:
        if row["id"] == src_id and row.get("persona_gender"):
            return str(row["persona_gender"]).lower()
    if scene.get("persona_gender"):
        return str(scene["persona_gender"]).lower()
    return "female"


def resolve_avatar_voice(scene: dict, plan: dict, gender: str) -> str:
    voice_map = {**VOICE_BY_GENDER, **(plan.get("voice_map") or {})}
    expected = voice_map.get(gender, VOICE_BY_GENDER.get(gender, "Zephyr (Female)"))
    scene_voice = scene.get("voice")
    if scene_voice:
        if gender == "male" and "(Male)" in scene_voice:
            return scene_voice
        if gender == "female" and "(Female)" in scene_voice:
            return scene_voice
        print(
            f"Warning: scene {scene['id']} voice {scene_voice!r} mismatches persona_gender {gender!r}; "
            f"using {expected!r}"
        )
    return expected


def resolve_avatar_voice_prompt(scene: dict, plan: dict, gender: str) -> str:
    if scene.get("voice_prompt"):
        return str(scene["voice_prompt"])
    cast = plan.get("cast", {})
    if gender == "male":
        return str(
            cast.get(
                "voice_prompt_male",
                "Casual male creator energy, UGC direct-to-camera, clear lip sync, conversational not announcer.",
            )
        )
    return str(cast.get("voice_prompt", ""))


def phase_stills(scenes: list[dict], plan: dict, out_dir: Path, api_key: str) -> None:
    manifest: dict = {}
    need_stills = [
        s
        for s in scenes
        if (s.get("person") or s.get("poses") or s.get("person_from_scene"))
        and not s.get("still_from")
        and not s.get("still_from_previous")
    ]

    def stills_job(scene: dict, manifest_snapshot: dict) -> tuple[str, dict]:
        sid = scene["id"]
        sdir = scene_dir(out_dir, sid)
        if scene.get("force_rerender") and sdir.exists():
            shutil.rmtree(sdir)
            sdir = scene_dir(out_dir, sid)

        if scene.get("poses"):
            cast = str(scene.get("person_cast") or (scene.get("person") or {}).get("prompt", ""))
            garment_paths = resolve_garment_paths(scene, sdir, plan, api_key)
            person_paths: list[str] = []
            try_on_paths: list[str] = []
            pose_labels: list[str] = []
            for i, pose in enumerate(scene["poses"]):
                person_path = sdir / f"person_{i:02d}.png"
                pose_prompt = f"{cast} {pose['prompt']}"
                gen_p_image(
                    pose_prompt,
                    plan,
                    person_path,
                    api_key,
                    seed=pose.get("seed"),
                    label=f"scene {sid} person pose {i}",
                    scene=scene,
                )
                dest = sdir / f"try_on_{i:02d}.png"
                garment_list = scene.get("garments") or []
                gen_try_on(
                    person_path,
                    [garment_paths[0]],
                    dest,
                    plan,
                    api_key,
                    label=f"scene {sid} try-on pose {i}",
                    garment_meta=[garment_list[0]] if garment_list else None,
                )
                person_paths.append(str(person_path))
                try_on_paths.append(str(dest))
                pose_labels.append(str(pose.get("output_label") or f"Pose {i + 1}"))
            return sid, {
                "persons": person_paths,
                "person": person_paths[0],
                "garments": [str(p) for p in garment_paths],
                "try_on": try_on_paths,
                "pose_labels": pose_labels,
            }

        person_path = sdir / "person.png"
        if scene.get("person_from_scene"):
            resolve_person_from_scene(scene, manifest_snapshot, person_path, plan)
        else:
            gen_p_image(
                scene["person"]["prompt"],
                plan,
                person_path,
                api_key,
                seed=scene["person"].get("seed"),
                label=f"scene {sid} person",
                scene=scene,
            )
        garment_paths = resolve_garment_paths(scene, sdir, plan, api_key)
        garment_list = scene.get("garments") or []
        try_on_paths: list[Path] = []
        for i, garment in enumerate(garment_list):
            dest = sdir / (f"try_on_{i:02d}.png" if len(garment_paths) > 1 else "try_on.png")
            gen_try_on(
                person_path,
                [garment_paths[i]],
                dest,
                plan,
                api_key,
                label=f"scene {sid} try-on {i}",
                garment_meta=[garment],
            )
            try_on_paths.append(dest)
        entry: dict = {
            "person": str(person_path),
            "garments": [str(p) for p in garment_paths],
            "try_on": [str(p) for p in try_on_paths],
        }
        if scene.get("multi_garment_try_on") and len(garment_paths) > 1:
            dest_all = sdir / "try_on_all.png"
            all_indices = scene.get("try_on_all_indices")
            if all_indices is not None:
                selected_paths = [garment_paths[i] for i in all_indices]
                selected_meta = [garment_list[i] for i in all_indices]
                all_label = f"scene {sid} try-on garments {all_indices}"
            else:
                selected_paths = garment_paths
                selected_meta = garment_list
                all_label = f"scene {sid} try-on all garments"
            gen_try_on(
                person_path,
                selected_paths,
                dest_all,
                plan,
                api_key,
                label=all_label,
                garment_meta=selected_meta,
            )
            entry["try_on_all"] = str(dest_all)
        return sid, entry

    pending = list(need_stills)
    while pending:
        ready = [
            s
            for s in pending
            if not s.get("person_from_scene") or str(s["person_from_scene"]) in manifest
        ]
        if not ready:
            raise RuntimeError(
                f"Unresolved person_from_scene dependencies for scenes: {[s['id'] for s in pending]}"
            )
        with ThreadPoolExecutor(max_workers=3) as pool:
            futures = {pool.submit(stills_job, s, manifest): s["id"] for s in ready}
            for fut in as_completed(futures):
                sid, data = fut.result()
                manifest[sid] = data
        for s in ready:
            pending.remove(s)

    for scene in scenes:
        motion = scene.get("motion")
        if motion not in ("avatar", "showcase_flash", "showcase_garments", "showcase_garment_flash"):
            continue
        if not (scene.get("still_from") or scene.get("still_from_previous")):
            continue
        src_id = resolve_avatar_source_id(scene, scenes)
        src = manifest[src_id]
        entry: dict = {
            "person": src["person"],
            "garments": src["garments"],
            "try_on": list(src["try_on"]),
            "reused_from": src_id,
        }
        if src.get("try_on_all"):
            entry["try_on_all"] = src["try_on_all"]
        if src.get("persons"):
            entry["persons"] = src["persons"]
        if src.get("pose_labels"):
            entry["pose_labels"] = src["pose_labels"]
        if motion == "avatar":
            if scene.get("use_try_on_all") and src.get("try_on_all"):
                entry["avatar_try_on_path"] = src["try_on_all"]
            else:
                entry["avatar_try_on_index"] = resolve_avatar_try_on_index(scene, len(src["try_on"]))
        manifest[scene["id"]] = entry

    (out_dir / "manifest_stills.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Stills manifest → {out_dir / 'manifest_stills.json'}")


def showcase_timing(plan: dict, scene: dict) -> Timing:
    key = scene.get("showcase_timing_key", "showcase_timing")
    raw = plan.get(key) or plan.get("showcase_timing") or {}
    scene_raw = scene.get("showcase_timing") or {}
    merged = {**raw, **scene_raw}
    return Timing(
        garment_seconds=float(merged.get("garment_seconds", 2.0)),
        person_seconds=float(merged.get("person_seconds", 1.5)),
        compare_seconds=float(merged.get("compare_seconds", 2.2)),
        slider_seconds=float(merged.get("slider_seconds", 2.5)),
        hold_seconds=float(merged.get("hold_seconds", 2.5)),
        flash_seconds=float(merged.get("flash_seconds", 0.8)),
    )


def flash_swap_timing(plan: dict, scene: dict) -> FlashSwapTiming:
    key = scene.get("flash_timing_key", "flash_swap_timing")
    raw = plan.get(key) or plan.get("flash_swap_timing") or {}
    scene_raw = scene.get("flash_timing") or {}
    merged = {**raw, **scene_raw}
    return FlashSwapTiming(
        hold_seconds_min=float(merged.get("hold_seconds_min", 0.5)),
        hold_seconds_max=float(merged.get("hold_seconds_max", 1.0)),
        wipe_seconds=float(merged.get("wipe_seconds", 0.08)),
        shuffle=bool(merged.get("shuffle", True)),
        cycles=int(merged.get("cycles", 1)),
        style=str(merged.get("style", "crossfade")),
        beat_frames=int(merged.get("beat_frames", 2)),
        zoom_peak=float(merged.get("zoom_peak", 1.14)),
        staccato_frames=int(merged.get("staccato_frames", 3)),
        crossfade_seconds=float(merged.get("crossfade_seconds", merged.get("fade_seconds", 0.3))),
    )


def avatar_tts_config(plan: dict, scene: dict, gender: str) -> tuple[str, str]:
    cfg = plan.get("avatar_tts") or {}
    row = scene.get("avatar_tts") or cfg.get(gender) or {}
    voice = str(row.get("voice") or AVATAR_TTS_VOICE.get(gender, "Kore"))
    style = str(
        row.get("style_prompt")
        or cfg.get("style_prompt")
        or plan.get("cast", {}).get(
            "avatar_tts_prompt",
            "Natural conversational UGC delivery, clear diction, relaxed pacing with real pauses, not announcer.",
        )
    )
    return voice, style


def build_avatar_video_prompt(scene: dict, plan: dict) -> str:
    if scene.get("avatar_video_prompt_mode") == "replace":
        return str(
            scene.get("video_prompt")
            or plan.get("defaults", {}).get("avatar_video_prompt")
            or DEFAULT_AVATAR_VIDEO_PROMPT
        )
    base = str(plan.get("defaults", {}).get("avatar_video_prompt") or DEFAULT_AVATAR_VIDEO_PROMPT)
    extra = str(scene.get("video_prompt") or "").strip()
    if extra and extra.lower() not in base.lower():
        return f"{base} {extra}"
    return base


def ensure_avatar_audio(
    scene: dict,
    plan: dict,
    token: str,
    audio_dir: Path,
    *,
    gender: str,
) -> Path:
    sid = scene["id"]
    dest = audio_dir / f"avatar_{sid}.mp3"
    if dest.exists() and dest.stat().st_size > 0 and not scene.get("force_rerender"):
        print(f"Reusing {dest.name}")
        return dest
    voice, style_prompt = avatar_tts_config(plan, scene, gender)
    cast = plan.get("cast", {})
    result = run_model_prediction(
        NARRATION_MODEL,
        {
            "text": scene["voice_script"],
            "voice": voice,
            "prompt": style_prompt,
            "language_code": scene.get("voice_language")
            or cast.get("voice_language_code")
            or plan.get("narration", {}).get("language_code", "en-US"),
        },
        token,
        label=f"avatar TTS scene {sid}",
    )
    output = result.get("output")
    if not output:
        raise RuntimeError(f"No avatar TTS output for scene {sid}")
    download_url(str(output), dest)
    print(f"Wrote {dest}")
    return dest


def show_labels_for(scene: dict, plan: dict) -> bool:
    if "show_labels" in scene:
        return bool(scene["show_labels"])
    return bool(plan.get("defaults", {}).get("show_labels", True))


def scene_seed(plan: dict, scene: dict) -> int:
    sid = str(scene["id"])
    if sid.isdigit():
        return int(plan.get("project_seed", 0)) + int(sid)
    return int(plan.get("project_seed", 0)) + abs(hash(sid)) % 100_000


def render_avatar(
    scene: dict,
    try_on: Path,
    plan: dict,
    clip: Path,
    api_key: str,
    *,
    scenes: list[dict],
    src_id: str,
    out_dir: Path,
    replicate_token: str | None = None,
) -> None:
    width, height = canvas_size(plan)
    if clip.exists() and clip.stat().st_size > 0 and not scene.get("force_rerender"):
        normalize_video(clip, width, height)
        print(f"Reusing {clip.name}")
        return
    gender = persona_gender_for_avatar(scene, scenes, src_id)
    defaults = plan.get("defaults", {})
    use_full = scene.get("avatar_use_full_frame")
    if use_full is None:
        use_full = defaults.get("avatar_use_full_frame", False)
    if use_full:
        image_path = try_on
    else:
        portrait_dir = out_dir / "stills" / ".avatar_portraits"
        portrait_dir.mkdir(parents=True, exist_ok=True)
        portrait = portrait_dir / f"scene_{scene['id']}_portrait.png"
        crop_ratio = float(
            scene.get("avatar_crop_top_ratio") or defaults.get("avatar_crop_top_ratio", 0.62)
        )
        crop_avatar_portrait(try_on, portrait, width, height, crop_top_ratio=crop_ratio)
        image_path = portrait

    avatar_model = str(scene.get("avatar_model") or defaults.get("avatar_model", "p-video-avatar"))
    use_audio = scene.get("avatar_use_uploaded_audio")
    if use_audio is None:
        use_audio = defaults.get("avatar_use_uploaded_audio", True)
    if avatar_model != "p-video-avatar":
        raise RuntimeError(f"Scene {scene['id']}: avatar lip-sync requires p-video-avatar, got {avatar_model}")

    payload: dict = {
        "image": upload_file(image_path, api_key),
        "video_prompt": build_avatar_video_prompt(scene, plan),
        "resolution": scene.get("avatar_resolution") or defaults.get("avatar_resolution", "720p"),
        "seed": int(scene.get("avatar_seed") or scene_seed(plan, scene)),
    }
    if use_audio:
        if not replicate_token:
            replicate_token = require_replicate_token()
        audio_dir = out_dir / "audio"
        audio_dir.mkdir(parents=True, exist_ok=True)
        audio_path = ensure_avatar_audio(scene, plan, replicate_token, audio_dir, gender=gender)
        payload["audio"] = upload_file(audio_path, api_key)
    else:
        cast = plan.get("cast", {})
        voice = resolve_avatar_voice(scene, plan, gender)
        voice_prompt = resolve_avatar_voice_prompt(scene, plan, gender)
        payload.update(
            {
                "voice_script": scene["voice_script"],
                "voice": voice,
                "voice_language": scene.get("voice_language") or cast.get("voice_language", "English (US)"),
                "voice_prompt": voice_prompt,
            }
        )

    result = run_prediction(avatar_model, payload, api_key, label=f"scene {scene['id']} avatar ({avatar_model})")
    download_file(result["generation_url"], clip, api_key)
    normalize_video(clip, width, height)
    mode = "uploaded-audio lip-sync" if use_audio else resolve_avatar_voice(scene, plan, gender)
    print(f"Wrote {clip} (try-on from scene {src_id}, {gender} · {mode})")


def render_showcase_scene(
    scene: dict,
    entry: dict,
    plan: dict,
    clip: Path,
    *,
    scenes: list[dict],
    out_dir: Path | None = None,
) -> None:
    width, height = canvas_size(plan)
    motion = scene.get("motion", "showcase")
    timing = showcase_timing(plan, scene)
    labels = scene.get("showcase_labels") or {}
    compare_title = str(labels.get("compare", "Same person · new outfit"))
    fps = int(plan.get("defaults", {}).get("fps", 24))

    if clip.exists() and clip.stat().st_size > 0 and not scene.get("force_rerender"):
        normalize_video(clip, width, height)
        print(f"Reusing {clip.name}")
        return

    if motion == "showcase_ladder":
        pairs = []
        garments = entry["garments"]
        try_ons = entry["try_on"]
        for i, try_on in enumerate(try_ons):
            label = scene.get("garments", [{}])[i].get("output_label") or f"Look {i + 1}"
            pairs.append((Path(garments[i]), Path(try_on), str(label)))
        render_ladder(
            person=Path(entry["person"]),
            pairs=pairs,
            output=clip,
            width=width,
            height=height,
            fps=fps,
            timing=timing,
            person_label=str(labels.get("person", "Input · person photo")),
            before_label=str(labels.get("before", "Before · base outfit")),
            after_label=str(labels.get("after", "After · try-on")),
            compare_title=compare_title,
        )
    elif motion == "showcase_rapid":
        pairs = []
        garments = entry["garments"]
        try_ons = entry["try_on"]
        for i, try_on in enumerate(try_ons):
            label = scene.get("garments", [{}])[i].get("output_label") or f"Look {i + 1}"
            pairs.append((Path(garments[i]), Path(try_on), str(label)))
        render_rapid(
            person=Path(entry["person"]),
            pairs=pairs,
            output=clip,
            width=width,
            height=height,
            fps=fps,
            person_label=str(labels.get("person", "Input · person photo")),
            before_label=str(labels.get("before", "Before · base outfit")),
            after_label=str(labels.get("after", "After · try-on")),
            compare_title=compare_title,
            timing=timing,
        )
    elif motion == "showcase_fit_poses":
        labels = scene.get("showcase_labels") or {}
        compare_title = str(labels.get("compare", "Same garment · every fit angle"))
        persons = entry.get("persons") or [entry["person"]]
        try_ons = entry["try_on"]
        pose_labels = entry.get("pose_labels") or [
            (scene.get("poses") or [{}])[i].get("output_label") or f"Pose {i + 1}"
            for i in range(len(try_ons))
        ]
        pairs = [
            (Path(persons[i]), Path(try_ons[i]), str(pose_labels[i]))
            for i in range(len(try_ons))
        ]
        if scene.get("align_to_narration") and out_dir is not None:
            narr_path = out_dir / "audio" / f"narration_{scene['id']}.mp3"
            if narr_path.exists() and narr_path.stat().st_size > 0:
                tail = float(scene.get("narration_tail_pad", 0.2))
                narr_dur = probe_duration(narr_path)
                timing = fit_pose_timing_for_narration(narr_dur + tail, len(pairs))
                print(
                    f"Scene {scene['id']} fit poses aligned to narration ({narr_dur:.2f}s + {tail:.2f}s tail)"
                )
        render_fit_poses(
            garment=Path(entry["garments"][0]),
            pairs=pairs,
            output=clip,
            width=width,
            height=height,
            fps=fps,
            timing=timing,
            garment_label=str(labels.get("garment", "Product · garment ref")),
            person_label=str(labels.get("person", "Model · base pose")),
            fit_label=str(labels.get("after", "On-model fit")),
            compare_title=compare_title,
        )
    elif motion == "showcase_garments":
        src_id = str(entry.get("reused_from", scene.get("still_from", scene["id"])))
        src_scene = next((s for s in scenes if s["id"] == src_id), scene)
        garment_paths = [Path(p) for p in entry["garments"]]
        labels = scene.get("garment_reel_labels") or [
            (src_scene.get("garments") or [{}])[i].get("output_label") or f"Product {i + 1}"
            for i in range(len(garment_paths))
        ]
        if src_scene.get("poses") and len(garment_paths) == 1:
            labels = [str((src_scene.get("garments") or [{}])[0].get("output_label") or "Product ref")]
        reel_cfg = plan.get("garment_reel_timing", {})
        sec = float(scene.get("garment_reel_seconds") or reel_cfg.get("seconds_per_garment", 0.55))
        grid_sec = 0.0
        if scene.get("garment_grid", True) and len(garment_paths) > 1:
            grid_sec = float(scene.get("garment_grid_seconds") or reel_cfg.get("grid_intro_seconds", 1.1))
        render_garment_reel(
            garments=garment_paths,
            labels=labels,
            output=clip,
            width=width,
            height=height,
            fps=fps,
            seconds_per_garment=sec,
            title=scene.get("title"),
            grid_intro_seconds=grid_sec,
            show_labels=show_labels_for(scene, plan),
        )
    elif motion == "showcase_garment_flash":
        src_id = str(entry.get("reused_from", scene.get("still_from", scene["id"])))
        src_scene = next((s for s in scenes if s["id"] == src_id), scene)
        garment_paths = [Path(p) for p in entry["garments"]]
        try_on_paths = [Path(p) for p in entry["try_on"]]
        if entry.get("try_on_all"):
            try_on_paths = try_on_paths + [Path(entry["try_on_all"])]
        reel_cfg = plan.get("garment_reel_timing", {})
        grid_sec = 0.0
        sec_per = float(scene.get("garment_reel_seconds") or reel_cfg.get("seconds_per_garment", 0.45))
        if scene.get("garment_grid", True) and len(garment_paths) > 1:
            grid_sec = float(scene.get("garment_grid_seconds") or reel_cfg.get("grid_intro_seconds", 0.9))
        flash_timing = flash_swap_timing(plan, scene)
        if scene.get("align_to_narration") and out_dir is not None:
            narr_path = out_dir / "audio" / f"narration_{scene['id']}.mp3"
            if narr_path.exists() and narr_path.stat().st_size > 0:
                tail = float(scene.get("narration_tail_pad", 0.15))
                narr_dur = probe_duration(narr_path)
                crossfade = float((scene.get("flash_timing") or {}).get("crossfade_seconds", 0.28))
                grid_sec, sec_per, flash_timing = garment_flash_timing_for_narration(
                    narr_dur + tail,
                    len(garment_paths),
                    len(try_on_paths),
                    crossfade_seconds=crossfade,
                )
                print(
                    f"Scene {scene['id']} garment+flash aligned to narration ({narr_dur:.2f}s, "
                    f"grid {grid_sec:.2f}s, {len(try_on_paths)} try-ons)"
                )
        render_garment_flash_montage(
            garments=garment_paths,
            try_ons=try_on_paths,
            output=clip,
            width=width,
            height=height,
            fps=fps,
            grid_intro_seconds=grid_sec,
            seconds_per_garment=sec_per,
            flash_timing=flash_timing,
            seed=scene_seed(plan, scene),
            show_labels=show_labels_for(scene, plan),
        )
    elif motion == "showcase_flash":
        try_on_paths = [Path(p) for p in entry["try_on"]]
        src_id = str(entry.get("reused_from", scene.get("still_from", scene["id"])))
        src_scene = next((s for s in scenes if s["id"] == src_id), scene)
        if src_scene.get("poses"):
            labels = entry.get("pose_labels") or [
                (src_scene.get("poses") or [{}])[i].get("output_label") or f"Pose {i + 1}"
                for i in range(len(try_on_paths))
            ]
        else:
            labels = [
                (src_scene.get("garments") or [{}])[i].get("output_label") or f"Look {i + 1}"
                for i in range(len(try_on_paths))
            ]
        timing = flash_swap_timing(plan, scene)
        if scene.get("align_to_narration") and out_dir is not None:
            narr_path = out_dir / "audio" / f"narration_{scene['id']}.mp3"
            if narr_path.exists() and narr_path.stat().st_size > 0:
                tail = float(scene.get("narration_tail_pad", 0.15))
                narr_dur = probe_duration(narr_path)
                crossfade = float((scene.get("flash_timing") or {}).get("crossfade_seconds", 0.32))
                timing = flash_timing_for_narration(
                    narr_dur + tail,
                    len(try_on_paths),
                    crossfade_seconds=crossfade,
                    tail_pad=0,
                )
                print(
                    f"Scene {scene['id']} flash aligned to narration ({narr_dur:.2f}s, "
                    f"{len(try_on_paths)} looks, hold {timing.hold_seconds_min:.2f}s)"
                )
        render_flash_swaps(
            try_ons=try_on_paths,
            output=clip,
            width=width,
            height=height,
            fps=fps,
            timing=timing,
            seed=scene_seed(plan, scene),
            labels=labels,
            show_labels=show_labels_for(scene, plan),
        )
    else:
        job = ShowcaseJob(
            person=Path(entry["person"]),
            garment=Path(entry["garments"][0]),
            try_on=Path(entry["try_on"][0]),
            output=clip,
            width=width,
            height=height,
            fps=fps,
            title=scene.get("title", "Try-on"),
            garment_label=str(labels.get("garment", "Input · garment ref")),
            person_label=str(labels.get("person", "Input · person photo")),
            before_label=str(labels.get("before", "Before · base outfit")),
            after_label=str(labels.get("after", "After · try-on")),
            compare_title=compare_title,
            timing=timing,
        )
        render_showcase(job)
    normalize_video(clip, width, height)
    print(f"Wrote {clip}")


def phase_video(scenes: list[dict], plan: dict, out_dir: Path, api_key: str) -> list[Path]:
    manifest = json.loads((out_dir / "manifest_stills.json").read_text(encoding="utf-8"))
    clips_dir = out_dir / "clips"
    clips_dir.mkdir(parents=True, exist_ok=True)
    clip_paths: list[Path] = []
    replicate_token: str | None = None
    if plan.get("defaults", {}).get("avatar_use_uploaded_audio", True) and any(
        s.get("motion") == "avatar" for s in scenes
    ):
        replicate_token = require_replicate_token()

    align_scenes = [
        s
        for s in scenes
        if s.get("align_to_narration")
        and s.get("narration")
        and s.get("motion") in ("showcase_fit_poses", "showcase_flash", "showcase_garment_flash")
    ]
    if align_scenes:
        if not replicate_token:
            replicate_token = require_replicate_token()
        audio_dir = out_dir / "audio"
        audio_dir.mkdir(parents=True, exist_ok=True)
        for scene in align_scenes:
            run_tts(scene, plan, replicate_token, audio_dir)

    audio_dir = out_dir / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)

    def render_scene_clip(scene: dict) -> Path | None:
        sid = scene["id"]
        motion = scene.get("motion", "showcase")
        if motion == "stills_source":
            return None
        entry = manifest[sid]
        clip = clips_dir / f"scene_{sid}.mp4"
        if motion == "avatar":
            src_id = resolve_avatar_source_id(scene, scenes)
            if entry.get("avatar_try_on_path"):
                try_on = Path(entry["avatar_try_on_path"])
            else:
                try_on = resolve_avatar_try_on_path(entry, scene)
            render_avatar(
                scene,
                try_on,
                plan,
                clip,
                api_key,
                scenes=scenes,
                src_id=src_id,
                out_dir=out_dir,
                replicate_token=replicate_token,
            )
        else:
            render_showcase_scene(scene, entry, plan, clip, scenes=scenes, out_dir=out_dir)
        return clip

    render_scenes = [s for s in scenes if s.get("motion") != "stills_source"]
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(render_scene_clip, s): s["id"] for s in render_scenes}
        for fut in as_completed(futures):
            clip = fut.result()
            if clip is not None:
                clip_paths.append(clip)
    clip_paths.sort(key=lambda p: next(i for i, s in enumerate(scenes) if f"scene_{s['id']}.mp4" == p.name))

    if replicate_token:
        width, height = canvas_size(plan)
        for scene in scenes:
            if scene.get("motion") not in ("showcase_flash", "showcase_garment_flash") or not scene.get("narration"):
                continue
            sid = scene["id"]
            clip = clips_dir / f"scene_{sid}.mp4"
            if not clip.exists():
                continue
            narr_path = audio_dir / f"narration_{sid}.mp3"
            if not narr_path.exists() or narr_path.stat().st_size == 0:
                run_tts(scene, plan, replicate_token, audio_dir)
            if narr_path.exists() and narr_path.stat().st_size > 0:
                muxed = clips_dir / f"scene_{sid}_vo.mp4"
                mux_narration_on_clip(clip, narr_path, muxed, width, height)
                normalize_video(muxed, width, height)
                shutil.move(muxed, clip)
                print(f"Muxed narration onto {clip.name}")

    (out_dir / "manifest_clips.json").write_text(
        json.dumps([str(p) for p in clip_paths], indent=2),
        encoding="utf-8",
    )
    return clip_paths


def run_tts(scene: dict, plan: dict, token: str, audio_dir: Path) -> Path | None:
    text = scene.get("narration")
    if not text:
        return None
    sid = scene["id"]
    dest = audio_dir / f"narration_{sid}.mp3"
    if dest.exists() and dest.stat().st_size > 0 and not scene.get("force_rerender"):
        print(f"Reusing {dest.name}")
        return dest
    narration_cfg = plan.get("narration", {})
    scene_tts = scene.get("narration_tts") or {}
    voice = scene_tts.get("voice") or narration_cfg.get("voice", "Kore")
    style_prompt = scene_tts.get("style_prompt") or narration_cfg.get("style_prompt", "")
    language_code = scene_tts.get("language_code") or narration_cfg.get("language_code", "en-US")
    fallbacks: list[str] = []
    for v in (voice, "Sulafat", "Kore", "Achird"):
        if v and v not in fallbacks:
            fallbacks.append(v)
    last_err: Exception | None = None
    for attempt, try_voice in enumerate(fallbacks[:3]):
        try:
            result = run_model_prediction(
                NARRATION_MODEL,
                {
                    "text": text,
                    "voice": try_voice,
                    "prompt": style_prompt,
                    "language_code": language_code,
                },
                token,
                label=f"TTS scene {sid}" + (f" voice {try_voice}" if attempt else ""),
            )
            output = result.get("output")
            if not output:
                raise RuntimeError(f"No TTS output for scene {sid}")
            download_url(str(output), dest)
            print(f"Wrote {dest}" + (f" ({try_voice})" if try_voice != voice else ""))
            return dest
        except RuntimeError as exc:
            last_err = exc
            if "E005" not in str(exc) or attempt >= 2:
                raise
            print(f"TTS scene {sid} flagged — retrying with {fallbacks[attempt + 1]}...")
    if last_err:
        raise last_err
    return None


def _video_scale_filter(width: int, height: int, *, hold_seconds: float = 0.0) -> str:
    scale_crop = f"scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height}"
    if hold_seconds > 0.01:
        return f"tpad=stop_mode=clone:stop_duration={hold_seconds:.3f},{scale_crop}"
    return scale_crop


def mux_narration_on_clip(
    clip: Path,
    narration: Path,
    out: Path,
    width: int,
    height: int,
    *,
    tail_pad: float = 0.2,
) -> Path:
    """Mux narration over a silent showcase clip; extends video if VO runs longer."""
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg not found")
    clip_dur = probe_duration(clip)
    narr_dur = probe_duration(narration)
    target = max(clip_dur, narr_dur) + tail_pad
    hold = max(0.0, target - clip_dur)
    vf = _video_scale_filter(width, height, hold_seconds=hold)
    subprocess.run(
        [
            ffmpeg,
            "-y",
            "-i",
            str(clip),
            "-i",
            str(narration),
            "-filter_complex",
            f"[0:v]{vf}[v];[1:a]apad=whole_dur={target:.3f},atrim=duration={target:.3f}[a]",
            "-map",
            "[v]",
            "-map",
            "[a]",
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
            "-t",
            f"{target:.3f}",
            str(out),
        ],
        check=True,
        capture_output=True,
    )
    return out


def phase_tts(scenes: list[dict], plan: dict, out_dir: Path, token: str) -> None:
    width, height = canvas_size(plan)
    audio_dir = out_dir / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    clips_dir = out_dir / "clips"

    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = {pool.submit(run_tts, s, plan, token, audio_dir): s for s in scenes}
        for fut in as_completed(futures):
            scene = futures[fut]
            narration = fut.result()
            if not narration:
                continue
            sid = scene["id"]
            clip = clips_dir / f"scene_{sid}.mp4"
            if not clip.exists():
                continue
            muxed = clips_dir / f"scene_{sid}_vo.mp4"
            mux_narration_on_clip(clip, narration, muxed, width, height)
            normalize_video(muxed, width, height)
            shutil.move(muxed, clip)


def phase_assemble(plan: dict, out_dir: Path, *, background_music: bool) -> Path:
    width, height = canvas_size(plan)
    manifest_clips = json.loads((out_dir / "manifest_clips.json").read_text(encoding="utf-8"))
    clip_paths = [Path(p) for p in manifest_clips]
    for clip in clip_paths:
        normalize_video(clip, width, height)
        ensure_audio_track(clip)
    assemble_cfg = plan.get("assemble", {})
    output_name = assemble_cfg.get("output_name", "try_on_launch.mp4")
    output = out_dir / output_name
    crossfade = float(assemble_cfg.get("crossfade_seconds", 0.25))
    concat_clips(clip_paths, output, crossfade_seconds=crossfade)
    normalize_video(output, width, height)
    print(f"Wrote {output}")

    music_cfg = music_config_from_plan(plan)
    if background_music or music_cfg.get("enabled"):
        output = apply_background_music(output, out_dir, plan=plan)
        normalize_video(output, width, height)
        print(f"Wrote {output}")
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, default=DEFAULT_TEMPLATE)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument(
        "--phase",
        choices=("stills", "video", "tts", "assemble", "all"),
        default="stills",
    )
    parser.add_argument("--approve-stills", action="store_true")
    parser.add_argument("--approve-audio", action="store_true")
    parser.add_argument("--approve-clips", action="store_true")
    parser.add_argument("--yes-skip-stills-gate", action="store_true")
    parser.add_argument("--yes-skip-clips-gate", action="store_true")
    parser.add_argument("--background-music", action="store_true")
    parser.add_argument("--assemble-only", action="store_true")
    parser.add_argument("--fresh", action="store_true")
    parser.add_argument("--force-video", action="store_true", help="Re-render showcase clips even if they exist")
    parser.add_argument("--force-avatar", action="store_true", help="Re-render avatar clips even if they exist")
    args = parser.parse_args()

    if args.approve_clips and not args.approve_audio:
        args.approve_audio = True

    args.out_dir.mkdir(parents=True, exist_ok=True)
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    plan_copy = args.out_dir / "plan.json"
    if args.fresh or not plan_copy.exists():
        if args.plan.resolve() != plan_copy.resolve():
            shutil.copy2(args.plan, plan_copy)

    scenes = plan["scenes"]
    apply_approve_flags(args, args.out_dir)

    run_phase = "assemble" if args.assemble_only else args.phase

    if run_phase in ("video", "tts", "assemble", "all"):
        ensure_phase_a_allowed(
            args.out_dir,
            approve_flag=args.approve_stills,
            skip_gate=args.yes_skip_stills_gate,
            label=f"Phase {run_phase}",
        )
    if run_phase in ("assemble", "all"):
        ensure_phase_b_allowed(
            args.out_dir,
            approve_flag=args.approve_audio,
            skip_gate=args.yes_skip_clips_gate,
            label="Assembly",
        )

    if run_phase in ("stills", "all"):
        if args.fresh:
            for sub in ("stills", "clips", "audio"):
                shutil.rmtree(args.out_dir / sub, ignore_errors=True)
        api_key = require_api_key()
        phase_stills(scenes, plan, args.out_dir, api_key)
        status = load_generation_status(args.out_dir)
        status["phase_a_approved"] = False
        status["phase_b_approved"] = False
        write_generation_status(args.out_dir, status)
        if run_phase == "stills":
            print(f"Phase stills complete — review {args.out_dir / 'stills'}")
            print("Re-run with --approve-stills --phase video")
            return

    if run_phase in ("video", "all"):
        if args.force_video:
            for scene in scenes:
                if scene.get("motion") != "avatar":
                    scene["force_rerender"] = True
        if args.force_avatar:
            for scene in scenes:
                if scene.get("motion") == "avatar":
                    scene["force_rerender"] = True
        phase_video(scenes, plan, args.out_dir, require_api_key())
        status = load_generation_status(args.out_dir)
        status["phase_b_approved"] = False
        write_generation_status(args.out_dir, status)
        if run_phase == "video":
            print(f"Phase video complete — review {args.out_dir / 'clips'}")
            print("Re-run with --approve-audio --phase tts")
            return

    if run_phase in ("tts", "all"):
        token = require_replicate_token()
        phase_tts(scenes, plan, args.out_dir, token)
        if run_phase == "tts":
            print(f"Phase tts complete — review {args.out_dir / 'audio'} and muxed clips")
            print("Re-run with --approve-audio --phase assemble --background-music")
            return

    if run_phase in ("assemble", "all"):
        phase_assemble(plan, args.out_dir, background_music=args.background_music)


if __name__ == "__main__":
    main()
