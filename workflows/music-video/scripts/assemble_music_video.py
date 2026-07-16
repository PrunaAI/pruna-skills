#!/usr/bin/env python3
"""Concat music-video clips and mux the full song (trim clips to cut timings)."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
_workflows = SCRIPT_DIR.parent
while _workflows.name != "workflows" and _workflows.parent != _workflows:
    _workflows = _workflows.parent
SHARED = _workflows / "_shared" / "scripts"
sys.path.insert(0, str(SHARED))

from concat_clips import probe_duration  # noqa: E402

sys.path.insert(0, str(SCRIPT_DIR))
from cut_timing import clip_duration_sec  # noqa: E402


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def trim_clip(src: Path, duration: float, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(src),
            "-t",
            str(duration),
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
            str(dest),
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--cuts", type=Path, help="cut_manifest.json (overrides plan.cuts if set)")
    parser.add_argument("--clips-dir", type=Path, required=True)
    parser.add_argument("--song", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--output-name", default="music_video.mp4")
    args = parser.parse_args()

    plan = json.loads(args.plan.read_text())
    if args.cuts:
        cuts_data = json.loads(args.cuts.read_text())
        cuts = cuts_data.get("cuts", cuts_data)
    else:
        cuts = plan.get("cuts", [])

    if not cuts:
        raise SystemExit("No cuts — run parse_lyric_cuts.py first")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    work = args.out_dir / ".assemble_work"
    work.mkdir(parents=True, exist_ok=True)

    trimmed: list[Path] = []
    for cut in cuts:
        if cut.get("skip_clip"):
            continue
        cut_id = cut["id"]
        clip_name = cut.get("clip") or f"{cut_id}.mp4"
        src = args.clips_dir / clip_name
        if not src.exists():
            raise SystemExit(f"Missing clip: {src}")

        duration = clip_duration_sec(cut)
        dest = work / f"{cut_id}_trim.mp4"
        actual = probe_duration(src)
        trim_to = min(duration, actual)
        if actual > duration + 0.08:
            print(
                f"  {cut_id}: trimming clip {actual:.2f}s → {trim_to:.2f}s "
                f"(manifest {cut.get('start_sec')}–{cut.get('end_sec')}s)"
            )
        trim_clip(src, trim_to, dest)
        trimmed.append(dest)

    concat_list = work / "concat.txt"
    concat_list.write_text("\n".join(f"file '{p.resolve()}'" for p in trimmed) + "\n")

    silent_video = args.out_dir / "video_silent.mp4"
    run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_list),
            "-c",
            "copy",
            str(silent_video),
        ]
    )

    final = args.out_dir / args.output_name
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(silent_video),
            "-i",
            str(args.song),
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            str(final),
        ]
    )
    print(f"Wrote {final}")


if __name__ == "__main__":
    main()
