"""Minimal Replicate HTTP helpers (stdlib only)."""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


def require_replicate_token() -> str:
    token = os.environ.get("REPLICATE_API_TOKEN", "").strip()
    if not token:
        raise SystemExit("REPLICATE_API_TOKEN is not set")
    return token


def api_request(
    method: str,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    data: bytes | None = None,
    timeout: int = 300,
) -> tuple[int, str]:
    request = urllib.request.Request(url, data=data, method=method)
    for key, value in (headers or {}).items():
        request.add_header(key, value)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status, response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {url} failed ({error.code}): {body}") from error


def run_model_prediction(
    model: str,
    input_payload: dict,
    token: str,
    *,
    label: str,
    timeout_seconds: int = 600,
) -> dict:
    url = f"https://api.replicate.com/v1/models/{model}/predictions"
    status, payload = api_request(
        "POST",
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        data=json.dumps({"input": input_payload}).encode("utf-8"),
    )
    if status >= 400:
        raise RuntimeError(f"{label} create failed ({status}): {payload}")
    data = json.loads(payload)
    get_url = data.get("urls", {}).get("get")
    if not get_url:
        raise RuntimeError(f"{label} missing poll URL: {payload}")
    deadline = time.time() + timeout_seconds
    last_state = ""
    while time.time() < deadline:
        status, payload = api_request(
            "GET",
            get_url,
            headers={"Authorization": f"Bearer {token}"},
        )
        if status >= 400:
            raise RuntimeError(f"{label} poll failed ({status}): {payload}")
        data = json.loads(payload)
        state = data.get("status", "unknown")
        if state != last_state:
            print(f"{label}: {state}...")
            sys.stdout.flush()
            last_state = state
        if state == "succeeded":
            return data
        if state in ("failed", "canceled"):
            raise RuntimeError(f"{label} {state}: {payload}")
        time.sleep(4)
    raise TimeoutError(f"{label} timed out after {timeout_seconds}s")


def download_url(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=600) as response:
        destination.write_bytes(response.read())


def upload_file(path: Path, token: str) -> str:
    """Upload a local file to Replicate; return the file GET URL for model inputs."""
    import mimetypes

    content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    boundary = "----replicate-boundary"
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="content"; filename="{path.name}"\r\n'
        f"Content-Type: {content_type}\r\n\r\n"
    ).encode("utf-8") + path.read_bytes() + f"\r\n--{boundary}--\r\n".encode("utf-8")
    status, payload = api_request(
        "POST",
        "https://api.replicate.com/v1/files",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        data=body,
        timeout=600,
    )
    if status >= 400:
        raise RuntimeError(f"Replicate file upload failed ({status}): {payload}")
    data = json.loads(payload)
    url = data.get("urls", {}).get("get")
    if not url:
        raise RuntimeError(f"Replicate file upload missing URL: {payload}")
    return url


def run_version_prediction(
    version: str,
    input_payload: dict,
    token: str,
    *,
    label: str,
    timeout_seconds: int = 600,
) -> dict:
    """Create a prediction pinned to a model version hash."""
    status, payload = api_request(
        "POST",
        "https://api.replicate.com/v1/predictions",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        data=json.dumps({"version": version, "input": input_payload}).encode("utf-8"),
    )
    if status >= 400:
        raise RuntimeError(f"{label} create failed ({status}): {payload}")
    data = json.loads(payload)
    get_url = data.get("urls", {}).get("get")
    if not get_url:
        raise RuntimeError(f"{label} missing poll URL: {payload}")
    deadline = time.time() + timeout_seconds
    last_state = ""
    while time.time() < deadline:
        status, payload = api_request(
            "GET",
            get_url,
            headers={"Authorization": f"Bearer {token}"},
        )
        if status >= 400:
            raise RuntimeError(f"{label} poll failed ({status}): {payload}")
        data = json.loads(payload)
        state = data.get("status", "unknown")
        if state != last_state:
            print(f"{label}: {state}...")
            sys.stdout.flush()
            last_state = state
        if state == "succeeded":
            return data
        if state in ("failed", "canceled"):
            raise RuntimeError(f"{label} {state}: {payload}")
        time.sleep(4)
    raise TimeoutError(f"{label} timed out after {timeout_seconds}s")
