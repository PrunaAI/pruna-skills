"""Shared run/poll/download helpers for CLI and workflow scripts."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

from pruna_client import PrunaClient
from pruna_client.models import PredictionStatus, Response

from scripts.pruna_sdk.registry import MODELS, ModelSpec, resolve_model

_REPO_ROOT = Path(__file__).resolve().parents[2]


def repo_root() -> Path:
    return _REPO_ROOT


def require_api_key() -> str:
    api_key = os.environ.get("PRUNA_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("PRUNA_API_KEY is not set")
    return api_key


def get_client(api_key: str | None = None) -> PrunaClient:
    return PrunaClient(api_key=api_key or require_api_key())


def default_sync_for_model(model: str, override: bool | None = None) -> bool:
    if override is not None:
        return override
    return resolve_model(model).default_sync


def _generation_url(response: Response) -> str | None:
    data = response.response if isinstance(response.response, dict) else {}
    url = data.get("generation_url")
    if url and not str(url).startswith("http"):
        return f"https://api.pruna.ai{url}"
    return url


def poll_until_done(
    client: PrunaClient,
    response: Response,
    *,
    label: str = "job",
) -> Response:
    if response.status == PredictionStatus.SUCCEEDED:
        return response
    if response.status == PredictionStatus.FAILED:
        raise RuntimeError(f"{label} failed: {json.dumps(response.response)}")
    print(f"{label}: polling...", flush=True)
    final = client.poll_status(response=response)
    if final.status != PredictionStatus.SUCCEEDED:
        raise RuntimeError(f"{label} failed: {json.dumps(final.response)}")
    return final


def download_generation(client: PrunaClient, response: Response) -> bytes:
    url = _generation_url(response)
    if not url:
        raise RuntimeError(f"No generation_url in response: {json.dumps(response.response)}")
    return client.download_content(url)


def save_bytes(data: bytes, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path


def run_and_save(
    client: PrunaClient,
    *,
    model: str,
    input_payload: dict[str, Any],
    out_path: Path,
    sync: bool | None = None,
    label: str | None = None,
    upload_paths: dict[str, Path | str] | None = None,
    upload_lists: dict[str, list[Path | str]] | None = None,
) -> dict[str, Any]:
    """Run a prediction, poll if needed, download, and write output file."""
    spec = resolve_model(model)
    use_sync = default_sync_for_model(model, sync)
    label = label or spec.model_id

    payload = dict(input_payload)
    upload_paths = upload_paths or {}
    upload_lists = upload_lists or {}

    for field, path in upload_paths.items():
        url = client.upload_file(str(path))
        if not url:
            raise RuntimeError(f"Upload failed for {field}: {path}")
        payload[field] = url

    for field, paths in upload_lists.items():
        urls = client.upload_file_batch([str(p) for p in paths])
        if not urls or any(u is None for u in urls):
            raise RuntimeError(f"Upload failed for {field}")
        payload[field] = urls

    response = client.generate(model=model, input=payload, sync=use_sync)
    if not use_sync:
        response = poll_until_done(client, response, label=label)

    content = download_generation(client, response)
    if out_path.suffix == "":
        out_path = out_path.with_suffix(spec.output_ext)
    save_bytes(content, out_path)

    manifest = {
        "model": model,
        "sync": use_sync,
        "status": response.status.value,
        "output": str(out_path.resolve()),
        "generation_url": _generation_url(response),
        "input": payload,
    }
    return manifest


def write_manifest(out_dir: Path, manifest: dict[str, Any]) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "manifest.json"
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return path


def ensure_repo_on_path() -> None:
    root = str(repo_root())
    if root not in sys.path:
        sys.path.insert(0, root)
