#!/usr/bin/env python3
"""Concat video clips with optional crossfade and clean re-encode (avoids concat copy glitches)."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def probe_duration(video_path: Path) -> float:
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        raise RuntimeError("ffprobe not found")
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


def extract_last_frame(video_path: Path, out_png: Path) -> Path:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg not found")
    out_png.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            ffmpeg,
            "-y",
            "-sseof",
            "-1",
            "-i",
            str(video_path),
            "-update",
            "1",
            "-frames:v",
            "1",
            "-q:v",
            "2",
            str(out_png),
        ],
        check=True,
        capture_output=True,
    )
    if not out_png.exists() or out_png.stat().st_size == 0:
        raise RuntimeError(f"Failed to extract last frame from {video_path}")
    return out_png


def concat_clips(
    clip_paths: list[Path],
    output: Path,
    *,
    crossfade_seconds: float = 0.0,
    crossfades: list[float] | None = None,
    crf: int = 18,
) -> Path:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg not found")
    if not clip_paths:
        raise ValueError("No clips to concat")
    output.parent.mkdir(parents=True, exist_ok=True)

    if len(clip_paths) == 1:
        crossfade_seconds = 0.0
        crossfades = None

    if crossfades is None:
        crossfades = [crossfade_seconds] * max(0, len(clip_paths) - 1)

    if len(crossfades) != max(0, len(clip_paths) - 1):
        raise ValueError("crossfades length must be len(clip_paths) - 1")

    if not crossfades or all(f <= 0 for f in crossfades):
        list_file = output.parent / ".concat_list.txt"
        list_file.write_text("\n".join(f"file '{p.resolve()}'" for p in clip_paths) + "\n")
        subprocess.run(
            [
                ffmpeg,
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(list_file),
                "-c:v",
                "libx264",
                "-preset",
                "fast",
                "-crf",
                str(crf),
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                "-movflags",
                "+faststart",
                str(output),
            ],
            check=True,
        )
        return output

    current = clip_paths[0]
    temp_paths: list[Path] = []
    for i, nxt in enumerate(clip_paths[1:], start=1):
        fade = crossfades[i - 1]
        if fade <= 0:
            tmp = output.parent / f".pair_{i}.mp4"
            subprocess.run(
                [
                    ffmpeg,
                    "-y",
                    "-i",
                    str(current),
                    "-i",
                    str(nxt),
                    "-filter_complex",
                    "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]",
                    "-map",
                    "[v]",
                    "-map",
                    "[a]",
                    "-c:v",
                    "libx264",
                    "-preset",
                    "fast",
                    "-crf",
                    str(crf),
                    "-c:a",
                    "aac",
                    "-b:a",
                    "192k",
                    "-movflags",
                    "+faststart",
                    str(tmp),
                ],
                check=True,
            )
        else:
            tmp = output.parent / f".pair_{i}.mp4"
            dur_a = probe_duration(current)
            fade = min(fade, dur_a * 0.15, probe_duration(nxt) * 0.15)
            offset = max(0.0, dur_a - fade)
            subprocess.run(
                [
                    ffmpeg,
                    "-y",
                    "-i",
                    str(current),
                    "-i",
                    str(nxt),
                    "-filter_complex",
                    f"[0:v][1:v]xfade=transition=fade:duration={fade}:offset={offset}[v];"
                    f"[0:a][1:a]concat=n=2:v=0:a=1[a]",
                    "-map",
                    "[v]",
                    "-map",
                    "[a]",
                    "-c:v",
                    "libx264",
                    "-preset",
                    "fast",
                    "-crf",
                    str(crf),
                    "-c:a",
                    "aac",
                    "-b:a",
                    "192k",
                    "-movflags",
                    "+faststart",
                    str(tmp),
                ],
                check=True,
            )
        if current not in clip_paths:
            temp_paths.append(current)
        current = tmp
        temp_paths.append(tmp)

    shutil.copy2(current, output)
    for tmp in temp_paths:
        if tmp != output:
            tmp.unlink(missing_ok=True)
    return output


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("clips", nargs="+", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--crossfade", type=float, default=0.25)
    args = parser.parse_args()
    concat_clips(args.clips, args.output, crossfade_seconds=args.crossfade)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
