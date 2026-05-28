#!/usr/bin/env python3
"""Generate chill background bed (Stable Audio 2.5) and mix under a launch reel."""

from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path

from replicate_api import download_url, require_replicate_token, run_model_prediction

DEFAULT_MODEL = "stability-ai/stable-audio-2.5"
DEFAULT_PROMPT = (
    "Instrumental chill lo-fi ambient bed, soft piano and warm pads, relaxed modern tech "
    "atmosphere, no vocals, understated background music, 85 BPM"
)
DEFAULT_VOLUME = 0.12
MAX_DURATION_SECONDS = 190


def probe_duration_seconds(video_path: Path) -> float:
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        raise RuntimeError("ffprobe not found on PATH")
    result = subprocess.run(
        [
            ffprobe,
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(video_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def video_has_audio(video_path: Path) -> bool:
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        return False
    result = subprocess.run(
        [
            ffprobe,
            "-v",
            "error",
            "-select_streams",
            "a",
            "-show_entries",
            "stream=codec_type",
            "-of",
            "csv=p=0",
            str(video_path),
        ],
        capture_output=True,
        text=True,
    )
    return bool(result.stdout.strip())


def generate_bed(
    *,
    prompt: str,
    duration_seconds: int,
    out_path: Path,
    token: str,
    model: str = DEFAULT_MODEL,
    seed: int | None = None,
    steps: int = 8,
    cfg_scale: float = 1.0,
) -> Path:
    payload: dict = {
        "prompt": prompt,
        "duration": duration_seconds,
        "steps": steps,
        "cfg_scale": cfg_scale,
    }
    if seed is not None:
        payload["seed"] = seed
    result = run_model_prediction(
        model,
        payload,
        token,
        label=f"{model} bed",
    )
    output = result.get("output")
    if not output:
        raise RuntimeError(f"No audio output from {model}: {json.dumps(result)}")
    download_url(str(output), out_path)
    return out_path


def mix_bed_under_video(
    *,
    video_path: Path,
    bed_path: Path,
    out_path: Path,
    volume: float,
) -> Path:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg not found on PATH")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    vol = max(0.0, min(volume, 1.0))
    if video_has_audio(video_path):
        filter_complex = (
            f"[1:a]volume={vol},aloop=loop=-1:size=2e+09[bed];"
            f"[0:a][bed]amix=inputs=2:duration=first:dropout_transition=0[aout]"
        )
        cmd = [
            ffmpeg,
            "-y",
            "-i",
            str(video_path),
            "-i",
            str(bed_path),
            "-filter_complex",
            filter_complex,
            "-map",
            "0:v",
            "-map",
            "[aout]",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            str(out_path),
        ]
    else:
        cmd = [
            ffmpeg,
            "-y",
            "-i",
            str(video_path),
            "-i",
            str(bed_path),
            "-filter_complex",
            f"[1:a]volume={vol}[bed]",
            "-map",
            "0:v",
            "-map",
            "[bed]",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            str(out_path),
        ]
    subprocess.run(cmd, check=True)
    return out_path


def music_config_from_plan(plan: dict) -> dict | None:
    raw = plan.get("background_music")
    if not raw:
        return None
    if raw is True:
        return {"enabled": True}
    if isinstance(raw, dict) and raw.get("enabled", True):
        return raw
    return None


def apply_background_music(
    video_path: Path,
    out_dir: Path,
    *,
    plan: dict | None = None,
    prompt: str | None = None,
    volume: float | None = None,
    token: str | None = None,
) -> Path:
    cfg = music_config_from_plan(plan or {}) or {}
    bed_prompt = prompt or cfg.get("prompt") or DEFAULT_PROMPT
    bed_volume = volume if volume is not None else float(cfg.get("volume", DEFAULT_VOLUME))
    model = cfg.get("model", DEFAULT_MODEL)
    seed = cfg.get("seed")
    api_token = token or require_replicate_token()

    duration = int(min(MAX_DURATION_SECONDS, math.ceil(probe_duration_seconds(video_path) + 1)))
    bed_path = out_dir / "audio" / "launch_bed.mp3"
    print(f"Generating {duration}s background bed ({model})...")
    generate_bed(
        prompt=bed_prompt,
        duration_seconds=duration,
        out_path=bed_path,
        token=api_token,
        model=model,
        seed=seed,
    )

    final_name = cfg.get("output_name") or f"{video_path.stem}_with_music.mp4"
    out_path = out_dir / final_name
    print(f"Mixing bed at volume {bed_volume:.2f} under {video_path.name}...")
    mix_bed_under_video(
        video_path=video_path,
        bed_path=bed_path,
        out_path=out_path,
        volume=bed_volume,
    )
    meta_path = out_dir / "audio" / "launch_bed.meta.json"
    meta_path.write_text(
        json.dumps(
            {
                "model": model,
                "prompt": bed_prompt,
                "duration_seconds": duration,
                "volume": bed_volume,
                "bed": str(bed_path.relative_to(out_dir)),
                "output": str(out_path.relative_to(out_dir)),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--out-dir", type=Path, default=None)
    parser.add_argument("--prompt", default=DEFAULT_PROMPT)
    parser.add_argument("--volume", type=float, default=DEFAULT_VOLUME)
    parser.add_argument("--duration", type=int, default=None)
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()

    token = require_replicate_token()
    out_dir = args.out_dir or args.video.parent
    duration = args.duration or int(
        min(MAX_DURATION_SECONDS, math.ceil(probe_duration_seconds(args.video) + 1))
    )
    bed_path = out_dir / "audio" / "launch_bed.mp3"
    generate_bed(
        prompt=args.prompt,
        duration_seconds=duration,
        out_path=bed_path,
        token=token,
        seed=args.seed,
    )
    out_path = args.out or out_dir / f"{args.video.stem}_with_music.mp4"
    mix_bed_under_video(
        video_path=args.video,
        bed_path=bed_path,
        out_path=out_path,
        volume=args.volume,
    )
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
