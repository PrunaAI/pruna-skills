#!/usr/bin/env python3
"""Rewrite local example paths in markdown to Hugging Face dataset URLs."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from doc_examples_hf import rewrite_markdown  # noqa: E402

DEFAULT_FILES = (
    ROOT / "docs" / "EXAMPLES.md",
    ROOT / "README.md",
)


def rewrite_file(path: Path, *, check: bool = False) -> bool:
    original = path.read_text(encoding="utf-8")
    updated = rewrite_markdown(original)
    if updated == original:
        return False
    if check:
        print(f"would update {path.relative_to(ROOT)}")
        return True
    path.write_text(updated, encoding="utf-8")
    print(f"updated {path.relative_to(ROOT)}")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*", type=Path, help="markdown files (default: EXAMPLES.md + README.md)")
    parser.add_argument("--check", action="store_true", help="exit 1 if any file would change")
    args = parser.parse_args()

    paths = args.files or DEFAULT_FILES
    changed = any(rewrite_file(p.resolve(), check=args.check) for p in paths)
    if args.check and changed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
