#!/usr/bin/env python3
"""One-shot path rewrites after moving sources under catalog/. Idempotent-ish."""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "skills", ".mine", "node_modules", ".agents"}

REPLACEMENTS = [
    ("guides/workflows/", "catalog/workflows/"),
    ("../../../guides/workflows/", "../../../catalog/workflows/"),
    ("../../guides/workflows/", "../../catalog/workflows/"),
    ("../guides/workflows/", "../catalog/workflows/"),
    # Root-anchored paths (README, examples at repo root)
    ("references/shared/", "catalog/references/shared/"),
    ("references/image/", "catalog/references/image/"),
    ("references/video/", "catalog/references/video/"),
    ("references/audio/", "catalog/references/audio/"),
    ("references/workflows/", "catalog/references/workflows/"),
    ("references/README.md", "catalog/references/README.md"),
    ("tools/image/", "catalog/tools/image/"),
    ("tools/video/", "catalog/tools/video/"),
    ("tools/audio/", "catalog/tools/audio/"),
    # Plugin / install paths
    ('"./references/', '"./catalog/references/'),
    ('"./tools/', '"./catalog/tools/'),
    ('"./guides/workflows/', '"./catalog/workflows/'),
]


def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def migrate_file(path: Path) -> bool:
    text = path.read_text()
    original = text
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    # Fix double catalog prefix from idempotent runs
    text = text.replace("catalog/catalog/", "catalog/")
    if text != original:
        path.write_text(text)
        return True
    return False


def main() -> None:
    changed = 0
    for path in REPO.rglob("*"):
        if not path.is_file() or should_skip(path):
            continue
        if path.suffix not in {".md", ".py", ".sh", ".json", ".yaml", ".yml", ".toml"}:
            continue
        if path.name == "migrate_paths_to_catalog.py":
            continue
        if migrate_file(path):
            changed += 1
            print(path.relative_to(REPO))
    print(f"updated {changed} file(s)")


if __name__ == "__main__":
    main()
