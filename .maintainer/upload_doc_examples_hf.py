#!/usr/bin/env python3
"""Upload docs/assets/examples to the PrunaAI/pruna-skills Hugging Face dataset."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

OUT = ROOT / "docs" / "assets" / "examples"
TEMPLATE = ROOT / ".maintainer" / "templates" / "hf-dataset-README.md"

from doc_examples_hf import HF_DATASET, HF_PATH_PREFIX, hf_dataset_page  # noqa: E402

SKIP_NAMES = {".gitkeep", ".DS_Store"}


def _hf_api():
    try:
        from huggingface_hub import HfApi
    except ImportError:
        print("Install: pip install huggingface_hub", file=sys.stderr)
        raise SystemExit(1) from None
    return HfApi()


def _iter_files() -> list[Path]:
    if not OUT.is_dir():
        raise SystemExit(f"missing examples dir: {OUT}")
    files = sorted(
        p for p in OUT.iterdir()
        if p.is_file() and p.name not in SKIP_NAMES and not p.name.endswith(".tmp")
    )
    if not files:
        raise SystemExit(f"no files in {OUT}")
    return files


def upload(*, dry_run: bool, message: str, only: list[str] | None = None) -> None:
    files = _iter_files()
    if only:
        want = set(only)
        files = [p for p in files if p.name in want]
        missing = want - {p.name for p in files}
        if missing:
            raise SystemExit(f"missing local files: {', '.join(sorted(missing))}")

    print(f"dataset: {HF_DATASET}")
    print(f"source:  {OUT} ({len(files)} files)")
    print(f"dest:    {HF_PATH_PREFIX}/")
    print(f"page:    {hf_dataset_page()}")

    if dry_run:
        for p in files[:8]:
            print(f"  would upload {p.name}")
        if len(files) > 8:
            print(f"  … and {len(files) - 8} more")
        return

    # ponytail: XET write token 403 on some tokens — legacy upload still works
    os.environ.setdefault("HF_HUB_DISABLE_XET", "1")

    api = _hf_api()
    api.create_repo(HF_DATASET, repo_type="dataset", exist_ok=True)

    for path in files:
        api.upload_file(
            path_or_fileobj=str(path.resolve()),
            path_in_repo=f"{HF_PATH_PREFIX}/{path.name}",
            repo_id=HF_DATASET,
            repo_type="dataset",
            commit_message=message,
        )
        print(f"  uploaded {path.name}")

    if TEMPLATE.is_file():
        api.upload_file(
            path_or_fileobj=str(TEMPLATE.resolve()),
            path_in_repo="README.md",
            repo_id=HF_DATASET,
            repo_type="dataset",
            commit_message=message,
        )

    print("upload complete")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--only",
        nargs="*",
        metavar="FILE",
        help="upload only these basenames (default: all files in examples/)",
    )
    parser.add_argument(
        "--message",
        default="Sync doc examples from pruna-skills repo",
        help="HF commit message",
    )
    args = parser.parse_args()
    upload(dry_run=args.dry_run, message=args.message, only=args.only)


if __name__ == "__main__":
    main()
