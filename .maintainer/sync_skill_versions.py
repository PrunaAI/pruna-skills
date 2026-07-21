#!/usr/bin/env python3
"""Set metadata.version in every public SKILL.md from repo VERSION file."""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
VERSION = (REPO / "VERSION").read_text().strip()
SKILLS_ROOT = REPO / "skills"


def skill_files() -> list[Path]:
    if not SKILLS_ROOT.is_dir():
        return []
    return sorted(SKILLS_ROOT.rglob("SKILL.md"))


def sync(path: Path) -> bool:
    text = path.read_text()
    original = text
    if "metadata:" not in text:
        block = f'license: MIT\nmetadata:\n  version: "{VERSION}"\n  package: pruna-skills\n'
        if re.search(r"^license:", text, re.M):
            text = re.sub(
                r"^license:.*\n",
                lambda m: m.group(0) + block.replace("license: MIT\n", ""),
                text,
                count=1,
                flags=re.M,
            )
        else:
            text = re.sub(r"^---\n", f"---\n{block}", text, count=1)
    else:
        if re.search(r"^  version:", text, re.M):
            text = re.sub(r'^  version:.*$', f'  version: "{VERSION}"', text, count=1, flags=re.M)
        else:
            text = re.sub(r"^(metadata:\n)", rf'\1  version: "{VERSION}"\n', text, count=1, flags=re.M)
        if "package:" not in text.split("metadata:", 1)[-1].split("\n---", 1)[0]:
            text = re.sub(
                r'^(  version:.*\n)',
                rf'\1  package: pruna-skills\n',
                text,
                count=1,
                flags=re.M,
            )
    if text != original:
        path.write_text(text)
        return True
    return False


def main() -> None:
    n = 0
    for path in skill_files():
        if sync(path):
            n += 1
            print(f"updated {path.relative_to(REPO)}")
    print(f"sync_skill_versions: {n} files → {VERSION}")


if __name__ == "__main__":
    main()
