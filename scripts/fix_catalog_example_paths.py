#!/usr/bin/env python3
"""Fix example paths after moving examples/ under catalog/."""

from __future__ import annotations

from pathlib import Path

CATALOG = Path(__file__).resolve().parents[1] / "catalog"


def main() -> None:
    n = 0
    for path in CATALOG.rglob("*"):
        if not path.is_file() or path.suffix not in {".md", ".py", ".sh"}:
            continue
        text = path.read_text()
        original = text
        text = text.replace("../../../../examples/", "../../../examples/")
        if "/tools/" in path.as_posix():
            text = text.replace("../../../examples/", "../../examples/")
        if text != original:
            path.write_text(text)
            n += 1
    print(f"fixed {n} catalog file(s)")


if __name__ == "__main__":
    main()
