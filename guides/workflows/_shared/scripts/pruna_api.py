"""Pruna P-API client helpers backed by the official pruna_client SDK."""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[4]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from pruna_client import PrunaClient
from pruna_client.models import PredictionStatus, Response


def _client(api_key: str) -> PrunaClient:
    return PrunaClient(api_key=api_key)


def _response_to_dict(response: Response) -> dict[str, Any]:
    data: dict[str, Any] = (
        dict(response.response) if isinstance(response.response, dict) else {}
    )
    data.setdefault("status", response.status.value)
    if response.id:
        data.setdefault("id", response.id)
    return data


def require_api_key() -> str:
    api_key = os.environ.get("PRUNA_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("PRUNA_API_KEY is not set")
    return api_key


def upload_file(path: Path, api_key: str) -> str:
    client = _client(api_key)
    try:
        url = client.upload_file(path)
        if not url:
            raise RuntimeError(f"Upload failed for {path}")
        return url
    finally:
        client.close()


def create_prediction(model: str, input_payload: dict, api_key: str) -> dict:
    client = _client(api_key)
    try:
        response = client.generate(model=model, input=input_payload, sync=False)
        if response.status == PredictionStatus.FAILED:
            raise RuntimeError(
                f"{model} create failed: {json.dumps(_response_to_dict(response))}"
            )
        return _response_to_dict(response)
    finally:
        client.close()


def poll_prediction(get_url: str, api_key: str, *, label: str, timeout_seconds: int = 3600) -> dict:
    client = _client(api_key)
    try:
        os.environ.setdefault("DEFAULT_PRUNA_MAX_WAIT", str(timeout_seconds))
        response = client.poll_status(status_url=get_url)
        if response.status == PredictionStatus.FAILED:
            raise RuntimeError(f"{label} failed: {json.dumps(_response_to_dict(response))}")
        if response.status != PredictionStatus.SUCCEEDED:
            raise TimeoutError(f"{label} timed out or ended in {response.status.value}")
        return _response_to_dict(response)
    finally:
        client.close()


def download_file(url: str, destination: Path, api_key: str) -> None:
    if not url.startswith("http"):
        url = f"https://api.pruna.ai{url}"
    client = _client(api_key)
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(client.download_content(url))
    finally:
        client.close()


def run_prediction(
    model: str,
    input_payload: dict,
    api_key: str,
    *,
    label: str,
    max_attempts: int = 3,
) -> dict:
    last_error: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            create = create_prediction(model, input_payload, api_key)
            if create.get("status") == "succeeded":
                return create
            get_url = create.get("get_url")
            if not get_url:
                raise RuntimeError(f"{label} missing get_url: {json.dumps(create)}")
            return poll_prediction(get_url, api_key, label=label)
        except (RuntimeError, TimeoutError) as error:
            last_error = error
            if attempt >= max_attempts:
                break
            wait_seconds = 15 * attempt
            print(f"{label}: attempt {attempt} failed ({error}), retrying in {wait_seconds}s...")
            sys.stdout.flush()
            time.sleep(wait_seconds)
    assert last_error is not None
    raise last_error
