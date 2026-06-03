#!/usr/bin/env python3
"""Minimal pruna_client quickstart (requires PRUNA_API_KEY, Python 3.11+)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from pruna_client import PrunaClient
from pruna_client.models import PredictionStatus


def main() -> None:
    client = PrunaClient()
    response = client.generate_text_to_image(
        model="p-image",
        prompt="Product hero shot, minimal studio lighting",
        sync=True,
        aspect_ratio="16:9",
    )
    if response.status != PredictionStatus.SUCCEEDED:
        raise SystemExit(f"Generation failed: {response.response}")
    url = response.response.get("generation_url")
    if not url:
        raise SystemExit("No generation_url in response")
    data = client.download_content(url)
    out = Path("output/quickstart.jpg")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    print(out.resolve())
    client.close()


if __name__ == "__main__":
    main()
