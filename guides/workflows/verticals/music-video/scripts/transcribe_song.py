#!/usr/bin/env python3
"""Transcribe a song with Replicate victor-upmeet/whisperx (word-level timestamps)."""

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

from replicate_api import require_replicate_token, run_version_prediction, upload_file  # noqa: E402
from whisperx_to_srt import write_srt_from_transcript  # noqa: E402

MODEL_VERSION = "655845d6190ef70573c669245f245892cd039df4b880a1e3a65852c09252f5cc"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--song", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True, help="Write whisperx_transcript.json")
    parser.add_argument(
        "--srt-out",
        type=Path,
        help="Write YouTube-ready .srt (default: same stem as --out)",
    )
    parser.add_argument("--no-srt", action="store_true", help="Skip automatic .srt export")
    parser.add_argument("--language", default="en")
    parser.add_argument("--initial-prompt", default="", help="Optional lyric hint for WhisperX")
    args = parser.parse_args()

    if not args.song.exists():
        raise SystemExit(f"Missing {args.song}")

    token = require_replicate_token()
    print(f"Uploading {args.song.name}...")
    audio_url = upload_file(args.song, token)

    payload = {
        "audio_file": audio_url,
        "language": args.language,
        "align_output": True,
        "diarization": False,
    }
    if args.initial_prompt.strip():
        payload["initial_prompt"] = args.initial_prompt.strip()

    print("Running whisperx...")
    result = run_version_prediction(
        MODEL_VERSION,
        payload,
        token,
        label="whisperx",
        timeout_seconds=900,
    )
    output = result.get("output")
    if not output:
        raise RuntimeError(f"No whisperx output: {result}")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2) + "\n")
    segments = output.get("segments") or []
    word_count = sum(len(seg.get("words") or []) for seg in segments)
    print(f"Wrote {args.out} ({len(segments)} segments, {word_count} words)")

    if not args.no_srt:
        srt_path = args.srt_out or args.out.with_suffix(".srt")
        cue_count = write_srt_from_transcript(output, srt_path)
        print(f"Wrote {srt_path} ({cue_count} cues, YouTube-ready UTF-8 SRT)")


if __name__ == "__main__":
    main()
