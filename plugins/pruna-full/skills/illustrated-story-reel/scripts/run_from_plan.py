#!/usr/bin/env python3
"""Illustrated story reel — p-image/edit stills + Ken Burns slideshow + narration or music.

No p-video. Phased: stills → tts|music → assemble. See illustrated-story-reel-gates.md
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
_workflows = SCRIPT_DIR.parent
while _workflows.name != "workflows" and _workflows.parent != _workflows:
    _workflows = _workflows.parent
SHARED = _workflows / "_shared" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SHARED))

from assemble_slideshow import assemble_from_plan  # noqa: E402
from generation_gate import (  # noqa: E402
    apply_approve_flags,
    ensure_phase_a_allowed,
    ensure_phase_b_allowed,
    load_generation_status,
    write_generation_status,
)
from launch_background_music import generate_bed, probe_duration_seconds  # noqa: E402
from pruna_api import api_seed_from_plan, require_api_key  # noqa: E402
from replicate_api import download_url, require_replicate_token, run_model_prediction  # noqa: E402
from stills_pipeline import ensure_chained_start_stills, style_wrap  # noqa: E402

NARRATION_MODEL = "google/gemini-3.1-flash-tts"
BED_MODEL = "stability-ai/stable-audio-2.5"


def run_tts(scene_id: str, text: str, plan: dict, voice: str, token: str, audio_dir: Path) -> Path:
    audio_dir.mkdir(parents=True, exist_ok=True)
    dest = audio_dir / f"narration_{scene_id}.mp3"
    if dest.exists():
        print(f"Reusing TTS: {dest.name}")
        return dest
    narration_cfg = plan.get("narration", {})
    result = run_model_prediction(
        NARRATION_MODEL,
        {
            "text": text,
            "voice": voice,
            "prompt": narration_cfg.get("style_prompt", ""),
            "language_code": narration_cfg.get("language_code", "en-US"),
        },
        token,
        label=f"TTS {scene_id}",
    )
    output = result.get("output")
    if not output:
        raise RuntimeError(f"No TTS for {scene_id}")
    download_url(str(output), dest)
    print(f"Wrote {dest}")
    return dest


def narration_for_scene(scene: dict, plan: dict) -> str:
    if scene.get("narration"):
        return scene["narration"]
    lines = plan.get("narration", {}).get("scene_lines", {})
    if scene["id"] in lines:
        return lines[scene["id"]]
    raise RuntimeError(f"Missing narration for scene {scene['id']}")


def phase_stills(scenes: list[dict], plan: dict, stills: Path, api_key: str) -> None:
    ensure_chained_start_stills(scenes, plan, stills, api_key, wrap_fn=style_wrap)


def phase_tts(scenes: list[dict], plan: dict, audio_dir: Path, token: str, *, only: list[str] | None) -> None:
    voice = plan.get("narration", {}).get("voice", "Kore")
    targets = [s for s in scenes if not only or s["id"] in only]
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = {
            pool.submit(run_tts, s["id"], narration_for_scene(s, plan), plan, voice, token, audio_dir): s["id"]
            for s in targets
        }
        for fut in as_completed(futures):
            fut.result()


def phase_music(plan: dict, out_dir: Path, token: str) -> Path:
    music_cfg = plan.get("music", {})
    audio_dir = out_dir / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    dest = audio_dir / "music.mp3"
    if dest.exists():
        print(f"Reusing music: {dest}")
        return dest

    user_track = music_cfg.get("track")
    if user_track:
        src = Path(user_track)
        if not src.is_absolute():
            src = out_dir / src
        if not src.exists():
            raise FileNotFoundError(f"music.track not found: {src}")
        shutil.copy(src, dest)
        print(f"Copied user track → {dest}")
        return dest

    scenes = plan["scenes"]
    defaults = plan.get("defaults", {})
    hold = float(defaults.get("hold_seconds", 4.0))
    pad = float(defaults.get("hold_pad_seconds", 0.0))
    total = sum(float(s.get("hold_seconds") or hold) + pad for s in scenes)
    total = int(min(190, max(10, total + 2)))
    generate_bed(
        prompt=music_cfg.get(
            "prompt",
            "Cinematic instrumental underscore, emotional arc, no vocals, gentle pulse",
        ),
        duration_seconds=total,
        out_path=dest,
        token=token,
        model=music_cfg.get("model", BED_MODEL),
        seed=api_seed_from_plan(plan),
    )
    print(f"Wrote {dest} ({total}s)")
    return dest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument(
        "--phase",
        choices=("stills", "tts", "music", "assemble", "all"),
        default="stills",
    )
    parser.add_argument("--approve-stills", action="store_true")
    parser.add_argument("--approve-audio", action="store_true", help="Mark audio approved (maps to phase_b)")
    parser.add_argument("--approve-clips", action="store_true", help="Alias for --approve-audio")
    parser.add_argument(
        "--yes-skip-stills-gate",
        action="store_true",
        help="CI/automation only — agents must not bypass stills approval",
    )
    parser.add_argument(
        "--yes-skip-clips-gate",
        action="store_true",
        help="CI/automation only — agents must not bypass audio approval",
    )
    parser.add_argument("--only", nargs="+", metavar="SCENE_ID")
    parser.add_argument("--output-name", default="story_reel.mp4")
    args = parser.parse_args()
    if args.approve_clips and not args.approve_audio:
        args.approve_audio = True

    args.out_dir.mkdir(parents=True, exist_ok=True)
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    scenes = plan["scenes"]
    mode = plan.get("audio_mode", "narration")
    stills = args.out_dir / "stills"
    audio_dir = args.out_dir / "audio"
    stills.mkdir(parents=True, exist_ok=True)

    apply_approve_flags(args, args.out_dir)
    if args.approve_audio:
        status = load_generation_status(args.out_dir)
        status["phase_b_approved"] = True
        write_generation_status(args.out_dir, status)
        print("Marked phase_b_approved=true (audio approved)")

    run_phase = args.phase
    audio_phase = "tts" if mode == "narration" else "music"

    if run_phase in (audio_phase, "assemble", "all"):
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
        api_key = require_api_key()
        phase_stills(scenes, plan, stills, api_key)
        status = load_generation_status(args.out_dir)
        status["phase_a_approved"] = False
        status["phase_b_approved"] = False
        write_generation_status(args.out_dir, status)
        if run_phase == "stills":
            print(f"Phase stills complete — review {stills}")
            print(f"Reply with fixes or re-run with --approve-stills --phase {audio_phase}")
            return

    if run_phase in ("tts", "music", "all"):
        token = require_replicate_token()
        if mode == "narration":
            phase_tts(scenes, plan, audio_dir, token, only=args.only)
        else:
            phase_music(plan, args.out_dir, token)
        status = load_generation_status(args.out_dir)
        status["phase_b_approved"] = False
        write_generation_status(args.out_dir, status)
        if run_phase in ("tts", "music"):
            print(f"Phase {run_phase} complete — listen under {audio_dir}")
            print("Reply with fixes or re-run with --approve-audio --phase assemble")
            return

    if run_phase in ("assemble", "all"):
        out = assemble_from_plan(args.plan, args.out_dir, output_name=args.output_name)
        dur = probe_duration_seconds(out)
        print(f"Done! {out} ({dur:.1f}s)")


if __name__ == "__main__":
    main()
