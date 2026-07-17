#!/usr/bin/env python3
"""Build compact GIF previews for MP4s embedded in docs/EXAMPLES.md."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "assets" / "examples"
EXAMPLES = ROOT / "docs" / "EXAMPLES.md"

MP4_IN_MD = re.compile(
    r"(?:examples/|assets/examples/)([a-z0-9][a-z0-9_-]*\.mp4)",
    re.IGNORECASE,
)

# ponytail: busy lip-sync clips need shorter previews to stay under ~1MB for GitHub
PREVIEW_OVERRIDES: dict[str, dict[str, float | int]] = {
    "p-video-replace-jacket.mp4": {"max_secs": 3.0, "fps": 8, "max_colors": 48},
    "music-video-garage-drummer-clip.mp4": {"max_secs": 4.0, "fps": 10, "max_colors": 56},
}


def mp4s_in_examples_md() -> list[str]:
    text = EXAMPLES.read_text(encoding="utf-8")
    return sorted(set(MP4_IN_MD.findall(text)))


def probe_duration(path: Path) -> float:
    proc = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(proc.stdout.strip())


def make_gif(
    mp4: Path,
    gif: Path,
    *,
    width: int,
    max_secs: float,
    fps: int,
    max_colors: int,
    force: bool,
) -> bool:
    if gif.exists() and not force:
        if gif.stat().st_mtime >= mp4.stat().st_mtime:
            print(f"skip {gif.name} (up to date)")
            return False

    duration = min(max_secs, probe_duration(mp4))
    vf = (
        f"fps={fps},scale={width}:-1:flags=lanczos,"
        f"split[s0][s1];[s0]palettegen=max_colors={max_colors}[p];"
        f"[s1][p]paletteuse=dither=bayer:bayer_scale=3"
    )
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-t",
            f"{duration:.3f}",
            "-i",
            str(mp4),
            "-an",
            "-vf",
            vf,
            str(gif),
        ],
        check=True,
        capture_output=True,
    )
    size_kb = gif.stat().st_size // 1024
    print(f"wrote {gif.name} ({size_kb}K, {duration:.1f}s @ {fps}fps)")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--width", type=int, default=320)
    parser.add_argument("--max-secs", type=float, default=5.0)
    parser.add_argument("--fps", type=int, default=10)
    parser.add_argument("--max-colors", type=int, default=64)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("mp4s", nargs="*", help="basenames (default: all mp4s referenced in EXAMPLES.md)")
    args = parser.parse_args()

    names = args.mp4s or mp4s_in_examples_md()
    if not names:
        raise SystemExit("no mp4 references found in EXAMPLES.md")

    missing: list[str] = []
    for name in names:
        mp4 = OUT / name
        if not mp4.is_file():
            missing.append(name)
            continue
        opts = {
            "width": args.width,
            "max_secs": args.max_secs,
            "fps": args.fps,
            "max_colors": args.max_colors,
            **PREVIEW_OVERRIDES.get(name, {}),
        }
        make_gif(
            mp4,
            OUT / f"{mp4.stem}.gif",
            width=int(opts["width"]),
            max_secs=float(opts["max_secs"]),
            fps=int(opts["fps"]),
            max_colors=int(opts["max_colors"]),
            force=args.force,
        )

    if missing:
        print(f"missing mp4: {', '.join(missing)}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
