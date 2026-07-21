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
sys.path.insert(0, str(REPO / ".maintainer"))
from skill_catalog import load_catalog  # noqa: E402


def read_name(skill_md: Path) -> str | None:
    text = skill_md.read_text()
    m = re.search(r"^name:\s*(.+)$", text, re.M)
    return m.group(1).strip().strip('"') if m else None


def discover_skills() -> set[str]:
    names: set[str] = set()
    for base in (REPO / "skills",):
        if not base.is_dir():
            continue
        for skill_md in base.rglob("SKILL.md"):
            if "_shared" in skill_md.parts:
                continue
            if name := read_name(skill_md):
                names.add(name)
    return names


def build_payload() -> dict:
    catalog = load_catalog()
    found = discover_skills()
    guides = catalog.get("guides", [])
    image = catalog["tools"]["image"]
    video = catalog["tools"]["video"]
    audio = catalog["tools"]["audio"]
    workflows = catalog["workflows"]
    suite = catalog.get("suite", [])
    listed = guides + image + video + audio + workflows + suite
    missing = [n for n in listed if n not in found]
    if missing:
        print(f"warn: catalog lists skills not in source tree: {missing}", file=sys.stderr)

    return {
        "$schema": SCHEMA,
        "notGrouped": "bottom",
        "groupings": [
            {
                "title": "Suite",
                "description": "Install everything at once.",
                "skills": [n for n in suite if n in found],
            },
            {
                "title": "Guides",
                "description": "Vendor-neutral prompting and API craft.",
                "skills": [n for n in guides if n in found],
            },
            {
                "title": "Image Tools",
                "description": "Generate and edit images with Pruna API models.",
                "skills": [n for n in image if n in found],
            },
            {
                "title": "Video Tools",
                "description": "Generate and edit video with Pruna API models.",
                "skills": [n for n in video if n in found],
            },
            {
                "title": "Audio Tools",
                "description": "Music, TTS, transcription, and background audio.",
                "skills": [n for n in audio if n in found],
            },
            {
                "title": "Workflows",
                "description": "Multi-step production playbooks for explainers, music videos, and reels.",
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
            print("skills.sh.json is stale — run make bundle", file=sys.stderr)
            sys.exit(1)
        print("skills.sh.json OK")
        return
    OUT.write_text(rendered)
    print(f"wrote {OUT.relative_to(REPO)}")


if __name__ == "__main__":
    main()
