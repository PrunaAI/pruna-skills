#!/usr/bin/env python3
"""Generate skills.sh.json groupings from source skill tree."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "skills.sh.json"
SCHEMA = "https://skills.sh/schemas/skills.sh.schema.json"

IMAGE = [
    "p-image",
    "p-image-edit",
    "p-image-upscale",
    "p-image-try-on",
]
VIDEO_TOOLS = ["p-video", "p-video-avatar", "p-video-animate", "p-video-replace"]
AUDIO = ["music-2.5", "gemini-3.1-flash-tts", "stable-audio-2.5", "whisperx"]
GUIDES = ["generation-diversity", "generation-quality-checklists", "recipe-catalog"]
WORKFLOWS = [
    "pruna-generative-pipeline",
    "pruna-run",
    "requesting-generation-feedback",
    "image-to-video",
    "narrated-multi-scene",
    "visual-transition-reel",
    "avatar-single-scene",
    "avatar-multi-scene",
    "interactive-explainer",
    "music-video",
    "illustrated-story-reel",
]


def read_name(skill_md: Path) -> str | None:
    text = skill_md.read_text()
    m = re.search(r"^name:\s*(.+)$", text, re.M)
    return m.group(1).strip().strip('"') if m else None


def discover_skills() -> set[str]:
    names: set[str] = set()
    for base in (
        REPO / "tools",
        REPO / "guides",
        REPO / "workflows" / "router",
        REPO / "workflows" / "core",
        REPO / "workflows" / "verticals",
    ):
        if not base.is_dir():
            continue
        for skill_md in base.rglob("SKILL.md"):
            if name := read_name(skill_md):
                names.add(name)
    return names


def build_payload() -> dict:
    found = discover_skills()
    missing = [n for group in (IMAGE, VIDEO_TOOLS, AUDIO, GUIDES, WORKFLOWS) for n in group if n not in found]
    if missing:
        print(f"warn: skills.sh.json lists skills not in source tree: {missing}", file=sys.stderr)

    return {
        "$schema": SCHEMA,
        "notGrouped": "bottom",
        "groupings": [
            {
                "title": "Image Generation",
                "description": "Generate and edit images with Pruna API models.",
                "skills": [n for n in IMAGE if n in found],
            },
            {
                "title": "Video Generation",
                "description": "Generate and edit video with Pruna API models.",
                "skills": [n for n in VIDEO_TOOLS if n in found],
            },
            {
                "title": "Audio & Speech",
                "description": "Music, TTS, transcription, and background audio.",
                "skills": [n for n in AUDIO if n in found],
            },
            {
                "title": "Guides",
                "description": "Prompting, quality gates, and workflow routing — no API required.",
                "skills": [n for n in GUIDES if n in found],
            },
            {
                "title": "Workflows",
                "description": "Multi-step production pipelines for explainers, music videos, and reels.",
                "skills": [n for n in WORKFLOWS if n in found],
            },
        ],
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="exit 1 if skills.sh.json is stale")
    args = ap.parse_args()
    payload = build_payload()
    rendered = json.dumps(payload, indent=2) + "\n"
    if args.check:
        if not OUT.is_file() or OUT.read_text() != rendered:
            print("skills.sh.json is stale — run ./scripts/bundle_all_skills.sh", file=sys.stderr)
            sys.exit(1)
        print("skills.sh.json OK")
        return
    OUT.write_text(rendered)
    print(f"wrote {OUT.relative_to(REPO)}")


if __name__ == "__main__":
    main()
