#!/usr/bin/env python3
"""Sanity-check docs/assets/examples against EXAMPLES.md coverage (no API calls)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "assets" / "examples"

# Required paths per skill (file must exist under OUT)
REQUIRED: dict[str, list[str]] = {
    "p-image": ["p-image-brass-hummingbird.png", "p-image-brass-hummingbird.meta.json"],
    "p-image-edit": ["chain-monarch-02-end.png", "chain-monarch-02-end.meta.json"],
    "p-image-upscale": ["p-image-upscale-hummingbird.png", "p-image-upscale-hummingbird.meta.json"],
    "p-image-try-on": ["p-image-try-on-drummer.png", "p-image-try-on-garage-jacket.png"],
    "p-video": ["chain-monarch-clip.mp4", "image-to-video-aurora-clip.mp4"],
    "p-video-avatar": ["music-video-garage-drummer-clip.mp4"],
    "p-video-animate": ["p-video-animate-monarch.mp4", "chain-monarch-animate-template.mp4"],
    "p-video-replace": ["p-video-replace-jacket.mp4", "p-video-replace-source.mp4"],
    "gemini-3.1-flash-tts": ["illustrated-library-whale-narration.mp3", "illustrated-library-whale-narration.meta.json"],
    "music-2.5": ["music-video-garage-drummer-song.mp3", "music-video-garage-drummer-song.meta.json"],
    "stable-audio-2.5": ["stable-audio-library-bed.mp3", "stable-audio-library-bed.meta.json"],
    "whisperx": ["whisperx-drummer-song.json", "whisperx-drummer-song.meta.json"],
    "image-to-video": ["image-to-video-aurora-still.png", "image-to-video-aurora-clip.mp4"],
    "visual-transition-reel": ["chain-monarch-01-open.png", "chain-monarch-02-end.png", "chain-monarch-clip.mp4"],
    "narrated-multi-scene": [
        "narrated-multi-scene-demo.mp4",
        "narrated-multi-scene-demo.meta.json",
        "narrated-multi-scene-01-monarch.mp4",
        "narrated-multi-scene-02-aurora.mp4",
    ],
    "avatar-single-scene": ["music-video-garage-drummer-clip.mp4", "avatar-single-scene-drummer.meta.json"],
    "avatar-multi-scene": [
        "music-video-garage-drummer-clip.mp4",
        "avatar-multi-scene-02-count-in.mp4",
        "avatar-multi-scene-demo.meta.json",
    ],
    "music-video": [
        "music-video-garage-drummer.png",
        "music-video-garage-drummer-song.mp3",
        "music-video-garage-drummer-clip.mp4",
    ],
    "illustrated-story-reel": [
        "illustrated-library-whale.png",
        "illustrated-library-whale-narration.mp3",
        "illustrated-library-whale-reel.mp4",
    ],
}

# MP4s that must carry an audio stream
AUDIO_MP4 = {
    "music-video-garage-drummer-clip.mp4",
    "illustrated-library-whale-reel.mp4",
    "narrated-multi-scene-01-monarch.mp4",
    "narrated-multi-scene-02-aurora.mp4",
    "narrated-multi-scene-demo.mp4",
    "p-video-replace-jacket.mp4",
    "p-video-replace-source.mp4",
    "avatar-multi-scene-02-count-in.mp4",
}


def has_audio(path: Path) -> bool:
    proc = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "a:0",
            "-show_entries",
            "stream=codec_type",
            "-of",
            "csv=p=0",
            str(path),
        ],
        capture_output=True,
        text=True,
    )
    return proc.returncode == 0 and "audio" in proc.stdout


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    for skill, paths in REQUIRED.items():
        for rel in paths:
            p = OUT / rel
            if not p.exists():
                errors.append(f"{skill}: missing {rel}")

    for rel in AUDIO_MP4:
        p = OUT / rel
        if p.exists() and not has_audio(p):
            errors.append(f"expected audio stream: {rel}")

    nms_meta = OUT / "narrated-multi-scene-demo.meta.json"
    if nms_meta.exists():
        data = json.loads(nms_meta.read_text(encoding="utf-8"))
        if data.get("scene_count", 0) < 2:
            errors.append("narrated-multi-scene: scene_count < 2 in demo meta")
        if len(data.get("scenes") or []) < 2:
            errors.append("narrated-multi-scene: scenes[] must have 2 entries")

    bed_meta = OUT / "stable-audio-library-bed.meta.json"
    if bed_meta.exists():
        data = json.loads(bed_meta.read_text(encoding="utf-8"))
        if data.get("doc_fallback"):
            warnings.append(
                "stable-audio-2.5: bed is doc_fallback (song slice) — re-run "
                "`python3 .maintainer/generate_doc_examples.py --only stable-audio-library-bed`"
            )

    wx = OUT / "whisperx-drummer-song.json"
    if wx.exists():
        data = json.loads(wx.read_text(encoding="utf-8"))
        words = sum(len(s.get("words") or []) for s in data.get("segments") or [])
        if words < 5:
            errors.append(f"whisperx: expected word timestamps, got {words} words")

    src = OUT / "p-image-brass-hummingbird.png"
    up = OUT / "p-image-upscale-hummingbird.png"
    if src.exists() and up.exists():
        # ponytail: compare file size as cheap upscale signal
        if up.stat().st_size <= src.stat().st_size:
            warnings.append("p-image-upscale: output not larger than source — verify upscale ran")

    ams = OUT / "avatar-multi-scene-demo.meta.json"
    if ams.exists():
        data = json.loads(ams.read_text(encoding="utf-8"))
        if data.get("scene_count", 0) < 2:
            errors.append("avatar-multi-scene: scene_count < 2")

    for w in warnings:
        print(f"WARN: {w}")
    for e in errors:
        print(f"ERROR: {e}")

    if errors:
        print(f"validate_doc_examples: FAIL ({len(errors)} error(s), {len(warnings)} warning(s))")
        return 1
    print(f"validate_doc_examples: OK ({len(REQUIRED)} skills, {len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
