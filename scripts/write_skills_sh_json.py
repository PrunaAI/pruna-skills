#!/usr/bin/env python3
"""Generate skills.sh.json groupings from skills.catalog.json."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "skills.sh.json"
SCHEMA = "https://skills.sh/schemas/skills.sh.schema.json"
sys.path.insert(0, str(REPO / "scripts"))
from skill_catalog import load_catalog  # noqa: E402


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
    catalog = load_catalog()
    found = discover_skills()
    image = catalog["tools"]["image"]
    video = catalog["tools"]["video"]
    audio = catalog["tools"]["audio"]
    guides = catalog["guides"]
    workflows = (
        catalog["workflows"]["router"]
        + catalog["workflows"]["core"]
        + catalog["workflows"]["verticals"]
    )
    listed = image + video + audio + guides + workflows
    missing = [n for n in listed if n not in found]
    if missing:
        print(f"warn: catalog lists skills not in source tree: {missing}", file=sys.stderr)

    return {
        "$schema": SCHEMA,
        "notGrouped": "bottom",
        "groupings": [
            {
                "title": "Image Generation",
                "description": "Generate and edit images with Pruna API models.",
                "skills": [n for n in image if n in found],
            },
            {
                "title": "Video Generation",
                "description": "Generate and edit video with Pruna API models.",
                "skills": [n for n in video if n in found],
            },
            {
                "title": "Audio & Speech",
                "description": "Music, TTS, transcription, and background audio.",
                "skills": [n for n in audio if n in found],
            },
            {
                "title": "Guides",
                "description": "Prompting, quality gates, and workflow routing — no API required.",
                "skills": [n for n in guides if n in found],
            },
            {
                "title": "Workflows",
                "description": "Multi-step production pipelines for explainers, music videos, and reels.",
                "skills": [n for n in workflows if n in found],
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
