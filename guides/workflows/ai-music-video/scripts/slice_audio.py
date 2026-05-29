#!/usr/bin/env python3
"""Slice a segment from a song for p-video-avatar or p-video audio input."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--song", type=Path, required=True)
    parser.add_argument("--start", type=float, required=True, help="Start seconds")
    parser.add_argument("--end", type=float, required=True, help="End seconds")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    if args.end <= args.start:
        raise SystemExit("--end must be greater than --start")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    duration = args.end - args.start

    cmd = [
        "ffmpeg",
        "-y",
        "-ss",
        str(args.start),
        "-i",
        str(args.song),
        "-t",
        str(duration),
        "-vn",
        "-acodec",
        "libmp3lame",
        "-q:a",
        "2",
        str(args.out),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    print(f"Wrote {args.out} ({duration:.2f}s)")


if __name__ == "__main__":
    main()
