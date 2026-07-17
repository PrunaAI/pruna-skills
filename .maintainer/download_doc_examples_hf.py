#!/usr/bin/env python3
"""Download doc examples from the PrunaAI/pruna-skills Hugging Face dataset."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

OUT = ROOT / "docs" / "assets" / "examples"

from doc_examples_hf import HF_DATASET, HF_PATH_PREFIX  # noqa: E402


def download(*, dry_run: bool) -> None:
    try:
        from huggingface_hub import snapshot_download
    except ImportError:
        print("Install: pip install huggingface_hub", file=sys.stderr)
        raise SystemExit(1) from None

    print(f"dataset: {HF_DATASET}")
    print(f"dest:    {OUT}")

    if dry_run:
        print(f"would download {HF_PATH_PREFIX}/* into {OUT}")
        return

    cache = Path(
        snapshot_download(
            repo_id=HF_DATASET,
            repo_type="dataset",
            allow_patterns=f"{HF_PATH_PREFIX}/*",
        )
    )
    src = cache / HF_PATH_PREFIX
    if not src.is_dir():
        raise SystemExit(f"missing {HF_PATH_PREFIX}/ in dataset cache")

    OUT.mkdir(parents=True, exist_ok=True)
    count = 0
    for path in sorted(src.iterdir()):
        if not path.is_file():
            continue
        shutil.copy2(path, OUT / path.name)
        count += 1

    print(f"downloaded {count} files")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    download(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
