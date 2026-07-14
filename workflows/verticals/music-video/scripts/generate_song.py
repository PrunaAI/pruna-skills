#!/usr/bin/env python3
"""Generate a song with Replicate minimax/music-2.5 from a music video plan."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
_workflows = SCRIPT_DIR.parent
while _workflows.name != "workflows" and _workflows.parent != _workflows:
    _workflows = _workflows.parent
SHARED = _workflows / "_shared" / "scripts"
sys.path.insert(0, str(SHARED))

from replicate_api import download_url, require_replicate_token, run_model_prediction  # noqa: E402

MODEL = "minimax/music-2.5"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--output-name", default="song.mp3")
    args = parser.parse_args()

    plan = json.loads(args.plan.read_text())
    lyrics = plan.get("lyrics", "").strip()
    if not lyrics:
        raise SystemExit("plan.lyrics is empty")

    music = plan.get("music", {})
    style_prompt = music.get("prompt") or plan.get("music_prompt", "")
    if not style_prompt:
        raise SystemExit("Set music.prompt or music_prompt in plan")

    payload = {
        "lyrics": lyrics,
        "prompt": style_prompt,
        "sample_rate": music.get("sample_rate", 44100),
        "bitrate": music.get("bitrate", 256000),
        "audio_format": music.get("audio_format", "mp3"),
    }

    token = require_replicate_token()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Generating song ({MODEL})...")
    result = run_model_prediction(MODEL, payload, token, label="music-2.5", timeout_seconds=900)
    output = result.get("output")
    if not output:
        raise RuntimeError(f"No output URL: {result}")

    song_path = args.out_dir / args.output_name
    download_url(output, song_path)
    print(f"Wrote {song_path}")

    status_path = args.out_dir / "generation_status.json"
    status = {}
    if status_path.exists():
        status = json.loads(status_path.read_text())
    status["song_path"] = str(song_path)
    status["music_model"] = MODEL
    status_path.write_text(json.dumps(status, indent=2) + "\n")


if __name__ == "__main__":
    main()
