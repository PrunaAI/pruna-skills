#!/usr/bin/env python3
"""Write .claude-plugin/marketplace.json as a skills-only catalog (no plugins/)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / ".claude-plugin" / "marketplace.json"
sys.path.insert(0, str(REPO / ".maintainer"))
from skill_catalog import (  # noqa: E402
    all_primary_skills,
    description,
    find_skill_dir,
)


def version() -> str:
    return (REPO / "VERSION").read_text().strip()


def main() -> None:
    ver = version()
    entries = []
    for name in sorted(all_primary_skills()):
        skill_dir = find_skill_dir(name)
        if not skill_dir:
            continue
        rel = skill_dir.relative_to(REPO).as_posix()
        entries.append(
            {
                "name": name,
                "description": description(name),
                "version": ver,
                "source": f"./{rel}",
            }
        )
    payload = {
        "name": "pruna-skills",
        "owner": {"name": "Pruna AI"},
        "metadata": {
            "description": "Pruna Skills — generative media agent skills for the Pruna AI API",
            "version": ver,
            "pluginRoot": ".",
        },
        "plugins": entries,  # Claude marketplace schema key
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"wrote {OUT.relative_to(REPO)} ({len(entries)} entries)")


if __name__ == "__main__":
    main()
