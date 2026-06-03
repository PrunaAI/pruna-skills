#!/usr/bin/env python3
"""Single + batch p-image generation (official pruna_client quickstart)."""

from __future__ import annotations

from pathlib import Path

from pruna_client import PrunaClient
from pruna_client.models import PredictionStatus

OUT_DIR = Path(__file__).resolve().parent / "output"


def save_if_succeeded(client: PrunaClient, response, path: Path) -> bool:
    if response.status != PredictionStatus.SUCCEEDED:
        print(f"skip {path.name}: status={response.status}")
        return False
    generation_url = response.response.get("generation_url")
    if not generation_url:
        print(f"skip {path.name}: no generation_url")
        return False
    content = client.download_content(generation_url)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    print(path.resolve())
    return True


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    client = PrunaClient()

    response = client.generate(
        model="p-image",
        input={"prompt": "A beautiful sunset over a calm ocean"},
        sync=True,
    )
    save_if_succeeded(client, response, OUT_DIR / "output.jpg")

    responses = client.generate_batch(
        requests=[
            {"model": "p-image", "input": {"prompt": "A sunset"}, "sync": True},
            {"model": "p-image", "input": {"prompt": "A sunrise"}, "sync": True},
        ]
    )

    for i, batch_response in enumerate(responses):
        save_if_succeeded(client, batch_response, OUT_DIR / f"output_{i}.jpg")

    client.close()


if __name__ == "__main__":
    main()
