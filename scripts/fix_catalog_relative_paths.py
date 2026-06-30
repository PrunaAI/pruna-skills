#!/usr/bin/env python3
"""Normalize relative links inside catalog/ (no catalog/ prefix in path segments)."""

from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CATALOG = REPO / "catalog"

REPLACEMENTS = [
    ("../../../catalog/references/", "../../../references/"),
    ("../../catalog/references/", "../../references/"),
    ("../catalog/references/", "../references/"),
    ("../../../catalog/workflows/", "../../../workflows/"),
    ("../../catalog/workflows/", "../../workflows/"),
    ("../catalog/workflows/", "../workflows/"),
    ("../../../catalog/tools/", "../../../tools/"),
    ("../../catalog/tools/", "../../tools/"),
    ("../catalog/tools/", "../tools/"),
    ("[catalog/references/", "["),
    ("[catalog/workflows/", "["),
    ("[catalog/tools/", "["),
    # tools/* are three levels below catalog/ (idempotent: skip if already ../../../)
    ("../../../../references/", "../../../references/"),
]


def main() -> None:
    n = 0
    for path in CATALOG.rglob("*"):
        if not path.is_file() or path.suffix not in {".md", ".py", ".sh", ".json"}:
            continue
        text = path.read_text()
        original = text
        for old, new in REPLACEMENTS:
            text = text.replace(old, new)
        if text != original:
            path.write_text(text)
            n += 1
    print(f"fixed {n} catalog file(s)")


if __name__ == "__main__":
    main()
