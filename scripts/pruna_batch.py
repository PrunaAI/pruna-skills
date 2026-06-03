#!/usr/bin/env python3
"""Run parallel async predictions from a JSON batch file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from pruna_client.models import PredictionStatus  # noqa: E402

from scripts.pruna_sdk.helpers import (  # noqa: E402
    download_generation,
    get_client,
    poll_until_done,
    require_api_key,
    save_bytes,
    write_manifest,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Batch Pruna predictions (async parallel)")
    parser.add_argument("--batch", type=Path, required=True, help="JSON array of generate() request dicts")
    parser.add_argument("--out-dir", type=Path, default=Path.cwd() / "output" / "batch")
    args = parser.parse_args()

    require_api_key()
    requests = json.loads(args.batch.read_text(encoding="utf-8"))
    if not isinstance(requests, list):
        raise SystemExit("Batch file must be a JSON array")

    client = get_client()
    responses = client.generate_batch(requests)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    results = []

    for i, response in enumerate(responses):
        label = f"job-{i}"
        if response is None or response.status == PredictionStatus.FAILED:
            results.append({"index": i, "status": "failed", "response": getattr(response, "response", None)})
            continue
        if response.status != PredictionStatus.SUCCEEDED:
            response = poll_until_done(client, response, label=label)
        ext = ".mp4" if "video" in (response.model or "") else ".jpg"
        out_path = args.out_dir / f"{i:03d}{ext}"
        content = download_generation(client, response)
        save_bytes(content, out_path)
        results.append({"index": i, "status": "succeeded", "output": str(out_path), "model": response.model})

    manifest = {"batch": str(args.batch.resolve()), "results": results}
    write_manifest(args.out_dir, manifest)
    print(json.dumps(manifest, indent=2))
    client.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
