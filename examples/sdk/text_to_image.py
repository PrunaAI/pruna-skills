#!/usr/bin/env python3
"""p-image via generate_text_to_image (default + custom aspect ratio)."""

from __future__ import annotations

from pathlib import Path

from pruna_client import PrunaClient
from pruna_client.models import PredictionStatus

OUT_DIR = Path(__file__).resolve().parent / "output"


def save_image(client: PrunaClient, response, path: Path) -> None:
    if response.status != PredictionStatus.SUCCEEDED:
        raise RuntimeError(f"Generation failed: {response.status} — {response.response}")
    generation_url = response.response.get("generation_url")
    if not generation_url:
        raise RuntimeError(f"No generation_url in response: {response.response}")
    image_bytes = client.download_content(generation_url)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(image_bytes)
    print(path.resolve())


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    client = PrunaClient()

    response = client.generate_text_to_image(
        model="p-image",
        prompt="A beautiful sunset over a calm ocean",
        sync=True,
    )
    save_image(client, response, OUT_DIR / "generated_image.jpg")

    response = client.generate_text_to_image(
        model="p-image",
        prompt="A serene mountain landscape at dawn",
        sync=True,
        aspect_ratio="custom",
        width=512,
        height=512,
    )
    save_image(client, response, OUT_DIR / "generated_image_custom.jpg")

    client.close()


if __name__ == "__main__":
    main()
