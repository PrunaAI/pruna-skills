#!/usr/bin/env python3
"""Educational explainer — narrator p-video + character p-video-avatar, p-image/edit stills."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
_workflows = SCRIPT_DIR.parent
while _workflows.name != "workflows" and _workflows.parent != _workflows:
    _workflows = _workflows.parent
SHARED = _workflows / "_shared" / "scripts"
sys.path.insert(0, str(SHARED))

from concat_clips import concat_clips, extract_last_frame  # noqa: E402
from launch_background_music import generate_bed, mix_bed_under_video, probe_duration_seconds  # noqa: E402
from p_video_payload import (  # noqa: E402
    P_VIDEO_NARRATION_SAFE_MAX_SECONDS,
    build_p_video_payload,
    probe_media_duration_seconds,
    validate_narration_duration,
)
from pruna_api import create_prediction, download_file, require_api_key, upload_file  # noqa: E402
from replicate_api import download_url, require_replicate_token, run_model_prediction  # noqa: E402

NARRATION_MODEL = "google/gemini-3.1-flash-tts"
BED_MODEL = "stability-ai/stable-audio-2.5"
DEFAULT_RESOLUTION = "1080p"
DEFAULT_FPS = 48

# Motion prompts — see references/workflows/interactive-explainer-motion.md
PHYSICS_TRAP_WORDS = (
    " throw ",
    " throws ",
    " throw.",
    " catch ",
    " catches ",
    " toss ",
    " tosses ",
    " pour ",
    " pours ",
    " spill ",
    " splash ",
    " walk across ",
    " walks across ",
    " run toward ",
    " runs toward ",
    " jump ",
    " jumps ",
    " fall ",
    " falls ",
    " collide ",
    " grab ",
    " grabs ",
    " pick up ",
    " set down ",
    " slam ",
    " handoff ",
    "gesture with",
)

def apply_plan_defaults(plan: dict) -> None:
    defaults = plan.setdefault("defaults", {})
    if defaults.get("resolution", DEFAULT_RESOLUTION) != DEFAULT_RESOLUTION:
        print(
            f"Warning: defaults.resolution is {defaults.get('resolution')!r}; "
            f"educational-explainer recommends {DEFAULT_RESOLUTION!r}."
        )
    defaults.setdefault("resolution", DEFAULT_RESOLUTION)
    if defaults.get("fps", DEFAULT_FPS) != DEFAULT_FPS:
        print(
            f"Warning: defaults.fps is {defaults.get('fps')!r}; "
            f"educational-explainer recommends {DEFAULT_FPS}."
        )
    defaults.setdefault("fps", DEFAULT_FPS)
    defaults.setdefault("aspect_ratio", "16:9")


def validate_video_prompt(scene_id: str, prompt: str) -> None:
    if not prompt.strip():
        print(f"Warning: {scene_id}: missing video_prompt")
        return
    lower = f" {prompt.lower()} "
    if "mid:" not in lower:
        print(
            f"Warning: {scene_id}: video_prompt missing MID: beat — "
            "add dynamic camera/light motion (see educational-explainer-motion.md)."
        )
    for trap in PHYSICS_TRAP_WORDS:
        if trap in lower:
            print(
                f"Warning: {scene_id}: video_prompt may use physics-trap {trap.strip()!r} — "
                "prefer camera dolly, pan, light shift, atmosphere."
            )
            break


VOICE_BY_GENDER = {
    "female": "Zephyr (Female)",
    "male": "Puck (Male)",
}

# Substrings that often cause text overlays or multi-panel stills (see p-video-replace-comparison SKILL).
STILL_PROMPT_TRIGGERS = (
    "side by side",
    "before and after",
    "comparison",
    "collage",
    "montage",
    "contact sheet",
    "grid",
    "split composition",
    "split ",
    " labeled",
    "labeled ",
    "facing camera",
    "to camera",
    "speaks to camera",
    "no text",
    "no cartoon",
    "no rain",
    "graphic tee",
    "neon signs",
    "packshot",
    "flat lay",
)

CHARACTER_STILL_TRIGGERS = (
    "facing camera",
    "to camera",
    "speaks to camera",
    "ready to speak",
)


def poll_all(jobs: list[dict], api_key: str) -> list[dict]:
    from pruna_api import api_request

    results: list[dict | None] = [None] * len(jobs)
    pending = {i: job for i, job in enumerate(jobs)}
    while pending:
        for i, job in list(pending.items()):
            status, payload = api_request("GET", job["get_url"], headers={"apikey": api_key})
            if status >= 400:
                raise RuntimeError(f"{job['label']} poll failed ({status}): {payload}")
            data = json.loads(payload)
            state = data.get("status", "unknown")
            if state == "succeeded":
                results[i] = data
                del pending[i]
                print(f"{job['label']}: succeeded")
            elif state == "failed":
                raise RuntimeError(f"{job['label']} failed: {payload}")
            else:
                print(f"{job['label']}: {state}...")
        if pending:
            time.sleep(8)
    return results  # type: ignore[return-value]


def create_all(model: str, payloads: list[tuple[str, dict]], api_key: str) -> list[dict]:
    def submit(label: str, payload: dict) -> dict:
        create = create_prediction(model, payload, api_key)
        if create.get("status") == "succeeded":
            return {"label": label, "get_url": None, "result": create}
        get_url = create.get("get_url")
        if not get_url:
            raise RuntimeError(f"{label} missing get_url: {json.dumps(create)}")
        return {"label": label, "get_url": get_url, "result": None}

    with ThreadPoolExecutor(max_workers=min(8, len(payloads))) as pool:
        futures = {pool.submit(submit, label, p): i for i, (label, p) in enumerate(payloads)}
        ordered: list[dict | None] = [None] * len(payloads)
        for future in as_completed(futures):
            ordered[futures[future]] = future.result()
    jobs = ordered  # type: ignore[assignment]
    to_poll = [j for j in jobs if j["get_url"]]
    if to_poll:
        polled = poll_all(to_poll, api_key)
        idx = 0
        for j in jobs:
            if j["get_url"]:
                j["result"] = polled[idx]
                idx += 1
    return jobs


def style_wrap(plan: dict, prompt: str) -> str:
    bible = plan.get("style_bible", "")
    return f"{prompt}. {bible}" if bible else prompt


def scene_type(scene: dict) -> str:
    return scene.get("type", "narrator")


def is_narrator_scene(scene: dict) -> bool:
    return scene_type(scene) == "narrator"


def is_character_scene(scene: dict) -> bool:
    return scene_type(scene) == "character"


def cast_for_scene(scene: dict, plan: dict) -> dict:
    key = scene.get("cast")
    if not key:
        raise RuntimeError(f"Character scene {scene['id']} missing cast key")
    cast = plan.get("cast", {}).get(key)
    if not cast:
        raise RuntimeError(f"Missing cast.{key} for scene {scene['id']}")
    return cast


def persona_gender_for(scene: dict, cast: dict) -> str:
    raw = scene.get("persona_gender") or cast.get("persona_gender") or ""
    return str(raw).strip().lower()


def cast_voice_for(scene: dict, cast: dict) -> str:
    """Lock avatar TTS to persona gender; plan voice is fallback only."""
    gender = persona_gender_for(scene, cast)
    if gender in VOICE_BY_GENDER:
        return VOICE_BY_GENDER[gender]
    return cast["voice"]


def character_still_body(scene: dict, plan: dict) -> str:
    cast = cast_for_scene(scene, plan)
    parts: list[str] = []
    if cast.get("character_descriptor"):
        parts.append(cast["character_descriptor"].strip())
    parts.append(scene["edit_prompt"].strip())
    return ", ".join(parts)


def character_still_prompt(scene: dict, plan: dict) -> str:
    return style_wrap(plan, character_still_body(scene, plan))


def still_prompt_fields(plan: dict, scenes: list[dict]) -> list[tuple[str, str]]:
    """Raw still lines only (excludes style_bible) for trigger-word validation."""
    fields: list[tuple[str, str]] = [("hero_prompt", plan.get("hero_prompt", ""))]
    for scene in scenes:
        sid = scene["id"]
        if is_character_scene(scene):
            fields.append((f"{sid}.edit_prompt", character_still_body(scene, plan)))
        else:
            fields.append((f"{sid}.edit_prompt", scene.get("edit_prompt", "")))
        if scene.get("last_frame_edit_prompt"):
            fields.append((f"{sid}.last_frame_edit_prompt", scene["last_frame_edit_prompt"]))
    return fields


def voice_script_for_scene(scene: dict, plan: dict) -> str:
    if scene.get("voice_script"):
        return scene["voice_script"]
    scripts = plan.get("voice_scripts", {})
    if scene["id"] in scripts:
        return scripts[scene["id"]]
    raise RuntimeError(f"Missing voice_script for character scene {scene['id']}")


def narration_for_scene(scene: dict, plan: dict) -> str:
    if scene.get("narration"):
        return scene["narration"]
    return plan.get("narration", {}).get("scene_lines", {}).get(scene["id"], "")


def ensure_hero(plan: dict, stills: Path, api_key: str) -> Path:
    hero = stills / "hero.png"
    if hero.exists():
        print(f"Reusing hero: {hero}")
        return hero
    stills.mkdir(parents=True, exist_ok=True)
    print("=== Phase 0: p-image hero ===")
    defaults = plan["defaults"]
    payload: dict = {
        "prompt": style_wrap(plan, plan["hero_prompt"]),
        "aspect_ratio": defaults["aspect_ratio"],
    }
    if plan.get("project_seed") is not None:
        payload["seed"] = plan["project_seed"]
    job = create_all("p-image", [("hero", payload)], api_key)[0]
    url = job["result"].get("generation_url")
    if not url:
        raise RuntimeError("Hero generation failed")
    download_file(url, hero, api_key)
    print(f"Saved hero: {hero}")
    return hero


def ensure_start_stills(scenes: list[dict], plan: dict, stills: Path, api_key: str) -> None:
    missing = [s for s in scenes if not (stills / f"{s['id']}.png").exists()]
    if not missing:
        return
    hero_url = upload_file(ensure_hero(plan, stills, api_key), api_key)
    print(f"=== Phase 1: start stills ({len(missing)}) ===")
    defaults = plan["defaults"]
    payloads = [
        (
            s["id"],
            {
                "prompt": character_still_prompt(s, plan)
                if is_character_scene(s)
                else style_wrap(plan, s["edit_prompt"]),
                "images": [hero_url],
                "aspect_ratio": defaults["aspect_ratio"],
            },
        )
        for s in missing
    ]
    jobs = create_all("p-image-edit", payloads, api_key)
    for scene, job in zip(missing, jobs):
        url = job["result"].get("generation_url")
        if not url:
            raise RuntimeError(f"No start still for {scene['id']}")
        download_file(url, stills / f"{scene['id']}.png", api_key)
        print(f"  start: {stills / f'{scene['id']}.png'}")


def ensure_end_stills(scenes: list[dict], plan: dict, stills: Path, api_key: str) -> None:
    narrator = [s for s in scenes if is_narrator_scene(s)]
    missing = [
        s
        for s in narrator
        if s.get("last_frame_edit_prompt") and not (stills / f"{s['id']}_last.png").exists()
    ]
    if not missing:
        return
    print(f"=== Phase 2: end stills ({len(missing)} narrator scenes) ===")
    defaults = plan["defaults"]
    start_urls = {s["id"]: upload_file(stills / f"{s['id']}.png", api_key) for s in missing}
    payloads = [
        (
            f"{s['id']}_last",
            {
                "prompt": style_wrap(plan, s["last_frame_edit_prompt"]),
                "images": [start_urls[s["id"]]],
                "aspect_ratio": defaults["aspect_ratio"],
            },
        )
        for s in missing
    ]
    jobs = create_all("p-image-edit", payloads, api_key)
    for scene, job in zip(missing, jobs):
        url = job["result"].get("generation_url")
        if not url:
            raise RuntimeError(f"No end still for {scene['id']}")
        download_file(url, stills / f"{scene['id']}_last.png", api_key)
        print(f"  end: {stills / f'{scene['id']}_last.png'}")


def run_tts(scene_id: str, text: str, plan: dict, voice: str, token: str, audio_dir: Path) -> Path:
    dest = audio_dir / f"narration_{scene_id}.mp3"
    if dest.exists():
        print(f"Reusing TTS: {dest.name}")
        return dest
    style = plan.get("narration", {}).get("style_prompt", "")
    result = run_model_prediction(
        NARRATION_MODEL,
        {"text": text, "voice": voice, "prompt": style, "language_code": "en-US"},
        token,
        label=f"TTS {scene_id}",
    )
    output = result.get("output")
    if not output:
        raise RuntimeError(f"No TTS for {scene_id}")
    download_url(str(output), dest)
    return dest


def chain_from_previous(scene: dict, index: int) -> bool:
    if index == 0:
        return False
    return bool(scene.get("chain_from_previous", False))


def join_crossfades(scenes: list[dict], plan: dict) -> list[float]:
    assembly = plan.get("assembly", {})
    chain_fade = float(assembly.get("chain_crossfade_seconds", 0.12))
    hard_fade = float(assembly.get("hard_cut_crossfade_seconds", 0.0))
    return [chain_fade if chain_from_previous(scenes[i], i) else hard_fade for i in range(1, len(scenes))]


def normalize_clip_for_concat(src: Path, dst: Path) -> None:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg not found")
    dst.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            ffmpeg, "-y", "-i", str(src),
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
            "-movflags", "+faststart", str(dst),
        ],
        check=True,
        capture_output=True,
    )


def assemble_movie(
    clip_paths: list[Path], scenes: list[dict], plan: dict, out_dir: Path, output: Path
) -> Path:
    norm_dir = out_dir / "clips_norm"
    normalized: list[Path] = []
    for src in clip_paths:
        dst = norm_dir / src.name
        if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
            normalize_clip_for_concat(src, dst)
        normalized.append(dst)
    concat_clips(normalized, output, crossfades=join_crossfades(scenes, plan))
    return output


def render_scene(
    i: int,
    scene: dict,
    scenes: list[dict],
    plan: dict,
    stills: Path,
    clips: Path,
    chain: Path,
    audio_dir: Path,
    api_key: str,
    *,
    prev_clip: Path | None = None,
    chain_mode: str = "parallel_vignettes",
) -> tuple[int, Path]:
    sid = scene["id"]
    stype = scene_type(scene)
    dest = clips / f"{sid}.mp4"
    if dest.exists():
        print(f"  reusing: {dest.name} ({stype})")
        return i, dest

    defaults = plan["defaults"]

    if is_character_scene(scene):
        still_path = stills / f"{sid}.png"
        if not still_path.exists():
            raise SystemExit(f"Missing character still: {still_path}")
        cast = cast_for_scene(scene, plan)
        voice = cast_voice_for(scene, cast)
        payload: dict = {
            "image": upload_file(still_path, api_key),
            "voice_script": voice_script_for_scene(scene, plan),
            "voice": voice,
            "voice_language": cast.get("voice_language", "English (US)"),
            "voice_prompt": cast.get("voice_prompt", ""),
            "video_prompt": scene.get("video_prompt", "Medium close-up speaking to camera"),
            "resolution": defaults.get("resolution", DEFAULT_RESOLUTION),
        }
        if plan.get("project_seed") is not None:
            payload["seed"] = plan["project_seed"]
        model = "p-video-avatar"
    else:
        chain_mode_plan = plan.get("frame_chain_mode", chain_mode)
        use_chain = chain_from_previous(scene, i) and chain_mode_plan == "extract_last_frame" and prev_clip
        if use_chain:
            start_path = chain / f"into_{sid}.png"
            extract_last_frame(prev_clip, start_path)
        else:
            start_path = stills / f"{sid}.png"
        end_path = stills / f"{sid}_last.png"
        if not start_path.exists() or not end_path.exists():
            raise SystemExit(f"Missing narrator stills for {sid}")
        audio_path = audio_dir / f"narration_{sid}.mp3"
        payload = build_p_video_payload(
            prompt=style_wrap(plan, scene["video_prompt"]),
            image_url=upload_file(start_path, api_key),
            audio_url=upload_file(audio_path, api_key),
            last_frame_image_url=upload_file(end_path, api_key),
            resolution=defaults["resolution"],
            fps=defaults.get("fps", DEFAULT_FPS),
            save_audio=True,
        )
        model = "p-video"
        print(f"  {sid}: narrator p-video ({probe_media_duration_seconds(audio_path):.1f}s)")

    result = create_all(model, [(sid, payload)], api_key)[0]["result"]
    url = result.get("generation_url")
    if not url:
        raise RuntimeError(f"No video for {sid}")
    download_file(url, dest, api_key)
    print(f"  clip ({stype}): {dest.name}")
    return i, dest


def render_videos(
    scenes: list[dict],
    plan: dict,
    stills: Path,
    clips: Path,
    chain: Path,
    audio_dir: Path,
    api_key: str,
    *,
    only: list[str] | None = None,
) -> list[Path]:
    chain_mode = plan.get("frame_chain_mode", "parallel_vignettes")
    sequential = chain_mode == "extract_last_frame" and any(
        chain_from_previous(scenes[i], i) for i in range(1, len(scenes))
    )
    n_narr = sum(1 for s in scenes if is_narrator_scene(s))
    n_char = sum(1 for s in scenes if is_character_scene(s))
    print(f"=== Phase 4: video ({'sequential' if sequential else 'parallel'}) — {n_narr} narrator, {n_char} character ===")

    if sequential:
        clip_paths: list[Path] = []
        prev_clip: Path | None = None
        for i, scene in enumerate(scenes):
            if only and scene["id"] not in only:
                p = clips / f"{scene['id']}.mp4"
                if p.exists():
                    clip_paths.append(p)
                    prev_clip = p
                continue
            _, dest = render_scene(
                i, scene, scenes, plan, stills, clips, chain, audio_dir, api_key,
                prev_clip=prev_clip, chain_mode=chain_mode,
            )
            clip_paths.append(dest)
            prev_clip = dest
        return clip_paths

    results: dict[int, Path] = {}
    to_render: list[tuple[int, dict]] = []
    for i, scene in enumerate(scenes):
        if only and scene["id"] not in only:
            p = clips / f"{scene['id']}.mp4"
            if p.exists():
                results[i] = p
            continue
        if (clips / f"{scene['id']}.mp4").exists() and not only:
            results[i] = clips / f"{scene['id']}.mp4"
        else:
            to_render.append((i, scene))

    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = [
            pool.submit(
                render_scene, i, s, scenes, plan, stills, clips, chain, audio_dir, api_key,
                chain_mode=chain_mode,
            )
            for i, s in to_render
        ]
        for fut in as_completed(futures):
            i, dest = fut.result()
            results[i] = dest
    return [results[i] for i in range(len(scenes))]


def validate_plan(plan: dict, scenes: list[dict]) -> None:
    if not any(is_character_scene(s) for s in scenes):
        print("Warning: no character scenes — plan is narrator-only; see educational-explainer skill for interaction mix.")

    cast_keys = {s.get("cast") for s in scenes if is_character_scene(s)}
    for key in cast_keys:
        if not key:
            continue
        cast = plan.get("cast", {}).get(key, {})
        gender = str(cast.get("persona_gender", "")).lower()
        if gender not in VOICE_BY_GENDER:
            raise RuntimeError(
                f"cast.{key} must set persona_gender to 'female' or 'male' "
                f"(avatar voice is derived from gender)."
            )
        expected = VOICE_BY_GENDER[gender]
        if cast.get("voice") and cast["voice"] != expected:
            print(
                f"Warning: cast.{key}.voice is {cast['voice']!r}; "
                f"runner will use {expected!r} from persona_gender={gender!r}."
            )
        desc = cast.get("character_descriptor", "").lower()
        if gender == "female" and not any(w in desc for w in ("woman", "female", "girl")):
            print(
                f"Warning: cast.{key}.character_descriptor should name a woman/female "
                f"presenter to match persona_gender={gender!r}."
            )
        if gender == "male" and not any(w in desc for w in ("man", "male", "boy")):
            print(
                f"Warning: cast.{key}.character_descriptor should name a man/male "
                f"presenter to match persona_gender={gender!r}."
            )

    for label, text in still_prompt_fields(plan, scenes):
        lower = text.lower()
        for trig in STILL_PROMPT_TRIGGERS:
            if trig in lower:
                raise RuntimeError(
                    f"{label} contains still trigger {trig!r} — use positive single-frame "
                    f"wording; see guides/workflows/launches/p-video-replace-comparison/SKILL.md"
                )
        scene_id = label.split(".", 1)[0] if "." in label else None
        if scene_id and any(s["id"] == scene_id and is_character_scene(s) for s in scenes):
            for trig in CHARACTER_STILL_TRIGGERS:
                if trig in lower:
                    raise RuntimeError(
                        f"{label} contains character-still trigger {trig!r} — use slight angle "
                        f"from the side, lips in frame; keep speaks-to-camera in video_prompt only."
                    )

    for scene in scenes:
        vp = scene.get("video_prompt", "")
        if vp:
            validate_video_prompt(scene["id"], vp)
        if not is_character_scene(scene):
            continue
        ep = scene.get("edit_prompt", "").lower()
        if not any(m in ep for m in ("mouth", "lips")):
            print(
                f"Warning: {scene['id']}: character edit_prompt should mention lips in frame for lip sync."
            )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--final-name", default="explainer_final.mp4")
    parser.add_argument("--only", nargs="+", metavar="SCENE_ID")
    parser.add_argument("--regen-stills", action="store_true")
    parser.add_argument("--regen-tts", action="store_true")
    parser.add_argument("--regen-clips", action="store_true")
    parser.add_argument("--skip-assembly", action="store_true")
    parser.add_argument("--skip-narration-check", action="store_true")
    args = parser.parse_args()

    plan = json.loads(args.plan.read_text())
    apply_plan_defaults(plan)
    out_dir = args.out_dir
    stills = out_dir / "stills"
    clips = out_dir / "clips"
    chain = out_dir / "chain_frames"
    audio_dir = out_dir / "audio"
    for d in (stills, clips, chain, audio_dir):
        d.mkdir(parents=True, exist_ok=True)

    if args.regen_stills:
        shutil.rmtree(stills, ignore_errors=True)
        shutil.rmtree(chain, ignore_errors=True)
        stills.mkdir(parents=True, exist_ok=True)
    if args.regen_tts and audio_dir.exists():
        for f in audio_dir.glob("narration_*.mp3"):
            f.unlink()
    if args.regen_clips and clips.exists():
        for f in clips.glob("*.mp4"):
            f.unlink()

    scenes = plan["scenes"]
    validate_plan(plan, scenes)
    narration_max = float(
        plan.get("narration", {}).get("max_seconds_per_scene", P_VIDEO_NARRATION_SAFE_MAX_SECONDS)
    )
    api_key = require_api_key()
    replicate_token = require_replicate_token()
    voice = plan.get("narration", {}).get("voice", "Charon")

    ensure_start_stills(scenes, plan, stills, api_key)
    ensure_end_stills(scenes, plan, stills, api_key)

    narrator_scenes = [s for s in scenes if is_narrator_scene(s)]
    if narrator_scenes:
        print(f"=== Phase 3: Gemini TTS ({len(narrator_scenes)} narrator scenes) ===")
        tts_targets = [s for s in narrator_scenes if not args.only or s["id"] in args.only]
        with ThreadPoolExecutor(max_workers=6) as pool:
            futures = {
                pool.submit(
                    run_tts, s["id"], narration_for_scene(s, plan), plan, voice, replicate_token, audio_dir
                ): s["id"]
                for s in tts_targets
            }
            for fut in as_completed(futures):
                path = fut.result()
                if not args.skip_narration_check:
                    validate_narration_duration(
                        probe_media_duration_seconds(path),
                        scene_id=futures[fut],
                        max_seconds=narration_max,
                    )

    clip_paths = render_videos(
        scenes, plan, stills, clips, chain, audio_dir, api_key, only=args.only
    )

    if args.skip_assembly:
        print("Skipped assembly")
        return

    slug = args.final_name.replace("_final.mp4", "").replace(".mp4", "")
    movie = out_dir / f"{slug}.mp4"
    final = out_dir / args.final_name
    print("=== Phase 5: concat ===")
    assemble_movie(clip_paths, scenes, plan, out_dir, movie)

    bed_cfg = plan.get("background_music", {})
    if bed_cfg.get("enabled"):
        duration = int(probe_duration_seconds(movie) + 1)
        bed_path = audio_dir / "bed.mp3"
        print(f"=== Phase 6: bed ({duration}s) ===")
        generate_bed(
            prompt=bed_cfg.get("prompt", "Documentary bed, no vocals"),
            duration_seconds=min(190, duration),
            out_path=bed_path,
            token=replicate_token,
            model=bed_cfg.get("model", BED_MODEL),
        )
        mix_bed_under_video(
            video_path=movie,
            bed_path=bed_path,
            out_path=final,
            volume=float(bed_cfg.get("volume", 0.09)),
        )
    else:
        shutil.copy(movie, final)

    manifest = {
        "title": plan.get("title"),
        "final": str(final),
        "scene_types": {s["id"]: scene_type(s) for s in scenes},
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Done! {final}")


if __name__ == "__main__":
    main()
