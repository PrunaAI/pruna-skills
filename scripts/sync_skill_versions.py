#!/usr/bin/env python3
"""Set metadata.version in every public SKILL.md from repo VERSION file."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
VERSION = (REPO / "VERSION").read_text().strip()
SKIP = {".mine", ".agents", "skills", "plugins", ".git", "node_modules"}


def skill_files() -> list[Path]:
    out: list[Path] = []
    for path in REPO.rglob("SKILL.md"):
        if any(part in SKIP for part in path.parts):
            continue
        out.append(path)
    return sorted(out)


def sync(path: Path) -> bool:
    text = path.read_text()
    if "metadata:" not in text:
        block = f'license: MIT\nmetadata:\n  version: "{VERSION}"\n  package: pruna-skills\n'
        if re.search(r"^license:", text, re.M):
            text = re.sub(r"^license:.*\n", f'license: MIT\nmetadata:\n  version: "{VERSION}"\n  package: pruna-skills\n', text, count=1)
        else:
            text = re.sub(r"^(---\n.*?description:.*\n)", r"\1" + block, text, count=1, flags=re.S)
    else:
        text = re.sub(r'^(\s+version:\s*)"[^"]*"', rf'\1"{VERSION}"', text, flags=re.M)
        if "package:" not in text:
            text = re.sub(
                rf'^(\s+version:\s*"{re.escape(VERSION)}"\s*\n)',
                rf'\1  package: pruna-skills\n',
                text,
                count=1,
            )
    if text != path.read_text():
        path.write_text(text)
        return True
    return False


def main() -> None:
    changed = sum(sync(p) for p in skill_files())
    print(f"VERSION={VERSION} synced {changed} SKILL.md file(s)")


if __name__ == "__main__":
    main()
