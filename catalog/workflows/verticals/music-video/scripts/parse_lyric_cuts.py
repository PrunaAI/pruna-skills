#!/usr/bin/env python3
"""Parse lyrics with Music 2.5 section tags into cut-safe video segments."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SECTION_TAG = re.compile(
    r"^\[(Intro|Verse|Pre Chorus|Post Chorus|Chorus|Hook|Drop|Bridge|Solo|Inst|Build Up|Interlude|Break|Transition|Outro)\]\s*$",
    re.IGNORECASE,
)
PAREN_ONLY = re.compile(r"^\([^)]+\)\s*$")


def parse_lyrics(text: str) -> list[dict]:
    sections: list[dict] = []
    current_tag = "Verse"
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_lines, current_tag
        if not current_lines:
            return
        lines = [ln.strip() for ln in current_lines if ln.strip()]
        if not lines:
            current_lines = []
            return
        sections.append(
            {
                "section_tag": current_tag,
                "lines": lines,
                "line_count": len(lines),
                "char_weight": sum(len(ln) for ln in lines),
                "is_instrumental": all(PAREN_ONLY.match(ln) for ln in lines),
            }
        )
        current_lines = []

    for raw in text.strip().splitlines():
        line = raw.rstrip()
        if not line.strip():
            flush()
            continue
        match = SECTION_TAG.match(line.strip())
        if match:
            flush()
            current_tag = match.group(1).title()
            if current_tag == "Pre Chorus":
                current_tag = "Pre Chorus"
            continue
        current_lines.append(line.strip())

    flush()
    return sections


def section_beat_type(tag: str, *, verse_index: int, default_beat: str) -> str:
    if tag in ("Inst", "Solo", "Interlude", "Break", "Transition"):
        return "broll"
    if tag == "Intro":
        return "broll"
    if tag == "Outro":
        return "broll"
    if tag == "Bridge":
        return "broll"
    if tag in ("Chorus", "Hook", "Verse", "Pre Chorus", "Build Up"):
        return "performance"
    return default_beat


def build_cut_manifest(
    sections: list[dict],
    *,
    default_beat: str,
    granularity: str = "line",
) -> list[dict]:
    cuts: list[dict] = []
    verse_index = 0
    for index, section in enumerate(sections, start=1):
        tag = section["section_tag"]
        lines: list[str] = section["lines"]
        instrumental = section["is_instrumental"]

        if granularity == "section":
            if instrumental or tag in ("Inst", "Solo", "Interlude", "Break", "Transition"):
                cuts.append(
                    {
                        "id": f"{index:02d}",
                        "section_tag": tag,
                        "beat_type": "broll",
                        "lines": lines,
                        "cut_rule": "section",
                        "notes": "Instrumental — one cinematic clip for whole section",
                    }
                )
                continue

            if tag == "Verse":
                verse_index += 1
                cast_id = "altman" if verse_index % 2 == 1 else "amodei"
            else:
                cast_id = None

            beat = section_beat_type(tag, verse_index=verse_index, default_beat=default_beat)
            entry = {
                "id": f"{index:02d}",
                "section_tag": tag,
                "beat_type": beat,
                "lines": lines,
                "cut_rule": "section",
                "notes": f"{tag} — one clip for whole section",
            }
            if cast_id:
                entry["cast_id"] = cast_id
            cuts.append(entry)
            continue

        if instrumental or tag in ("Inst", "Solo", "Interlude", "Break", "Transition"):
            cuts.append(
                {
                    "id": f"{index:02d}",
                    "section_tag": tag,
                    "beat_type": "broll",
                    "lines": lines,
                    "cut_rule": "section",
                    "notes": "Instrumental — use p-video with audio slice or I2V B-roll",
                }
            )
            continue

        if tag in ("Intro", "Outro") and len(lines) <= 2:
            cuts.append(
                {
                    "id": f"{index:02d}",
                    "section_tag": tag,
                    "beat_type": "broll" if tag == "Intro" else default_beat,
                    "lines": lines,
                    "cut_rule": "section",
                    "notes": f"{tag} — short; one clip for whole section",
                }
            )
            continue

        # Default (line granularity): one clip per lyric line
        for line_index, line in enumerate(lines, start=1):
            beat = default_beat
            if tag in ("Verse", "Pre Chorus", "Bridge", "Hook", "Chorus"):
                beat = "performance" if line_index % 2 == 1 else "broll"
            cuts.append(
                {
                    "id": f"{index:02d}_{line_index}",
                    "section_tag": tag,
                    "beat_type": beat,
                    "lines": [line],
                    "cut_rule": "line",
                    "notes": "One line per clip — cut on line boundary, never mid-word",
                }
            )
    return cuts


def allocate_timings(cuts: list[dict], duration_sec: float) -> list[dict]:
    weights = [max(1, sum(len(ln) for ln in c["lines"])) for c in cuts]
    total = sum(weights)
    cursor = 0.0
    out: list[dict] = []
    for cut, weight in zip(cuts, weights):
        seg = dict(cut)
        seg_duration = duration_sec * (weight / total)
        seg["start_sec"] = round(cursor, 3)
        seg["end_sec"] = round(cursor + seg_duration, 3)
        seg["duration_sec"] = round(seg_duration, 3)
        cursor += seg_duration
        out.append(seg)
    if out:
        out[-1]["end_sec"] = round(duration_sec, 3)
        out[-1]["duration_sec"] = round(duration_sec - out[-1]["start_sec"], 3)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lyrics", type=Path, help="Lyrics text file")
    parser.add_argument("--plan", type=Path, help="music_video_plan.json (uses plan.lyrics)")
    parser.add_argument(
        "--default-beat",
        choices=("performance", "broll"),
        default="performance",
        help="Default beat type for ambiguous sections",
    )
    parser.add_argument(
        "--granularity",
        choices=("line", "section"),
        default=None,
        help="line = one clip per lyric line; section = one clip per [Verse]/[Hook]/etc. (plan cut_granularity if omitted)",
    )
    parser.add_argument(
        "--song",
        type=Path,
        help="Optional MP3/WAV — ffprobe duration for proportional cut allocation",
    )
    parser.add_argument("--out", type=Path, required=True, help="Write cut_manifest.json")
    args = parser.parse_args()

    if args.plan:
        plan = json.loads(args.plan.read_text())
        lyrics = plan.get("lyrics", "")
        granularity = args.granularity or plan.get("cut_granularity", "line")
    elif args.lyrics:
        lyrics = args.lyrics.read_text()
        granularity = args.granularity or "line"
    else:
        parser.error("Provide --lyrics or --plan")

    sections = parse_lyrics(lyrics)
    cuts = build_cut_manifest(sections, default_beat=args.default_beat, granularity=granularity)

    manifest = {
        "sections_parsed": len(sections),
        "cut_count": len(cuts),
        "cut_granularity": granularity,
        "cut_rules": [
            "Cuts happen only at line boundaries — never split mid-word",
            "Section tags [Verse]/[Chorus] start new scene groups",
            "Refine start_sec/end_sec after listening to the generated song",
        ],
        "sections": sections,
        "cuts": cuts,
    }

    if args.song:
        import subprocess

        probe = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(args.song),
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        duration = float(probe.stdout.strip())
        manifest["song_duration_sec"] = duration
        manifest["cuts"] = allocate_timings(cuts, duration)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Wrote {args.out} ({len(manifest['cuts'])} cuts)", file=sys.stderr)


if __name__ == "__main__":
    main()
