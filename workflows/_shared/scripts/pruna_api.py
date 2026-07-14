"""Minimal Pruna P-API client helpers (stdlib only)."""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


def api_request(
    method: str,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    data: bytes | None = None,
) -> tuple[int, str]:
    request = urllib.request.Request(url, data=data, method=method)
    for key, value in (headers or {}).items():
        request.add_header(key, value)
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            return response.status, response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {url} failed ({error.code}): {body}") from error


def require_api_key() -> str:
    api_key = os.environ.get("PRUNA_API_KEY", "").strip()
    if not api_key:
        raise SystemExit(
            "PRUNA_API_KEY is not set. Sign up at https://dashboard.pruna.ai/ "
            "and export PRUNA_API_KEY=your_key"
        )
    return api_key


def upload_file(path: Path, api_key: str) -> str:
    boundary = f"----pruna-{int(time.time() * 1000)}"
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="content"; filename="{path.name}"\r\n'
        f"Content-Type: application/octet-stream\r\n\r\n"
    ).encode("utf-8")
    body += path.read_bytes()
    body += f"\r\n--{boundary}--\r\n".encode("utf-8")
    status, payload = api_request(
        "POST",
        "https://api.pruna.ai/v1/files",
        headers={
            "apikey": api_key,
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        data=body,
    )
    if status >= 400:
        raise RuntimeError(f"Upload failed ({status}): {payload}")
    return json.loads(payload)["urls"]["get"]


def create_prediction(model: str, input_payload: dict, api_key: str) -> dict:
    status, payload = api_request(
        "POST",
        "https://api.pruna.ai/v1/predictions",
        headers={
            "Content-Type": "application/json",
            "apikey": api_key,
            "Model": model,
        },
        data=json.dumps({"input": input_payload}).encode("utf-8"),
    )
    if status >= 400:
        raise RuntimeError(f"{model} create failed ({status}): {payload}")
    return json.loads(payload)


def poll_prediction(get_url: str, api_key: str, *, label: str, timeout_seconds: int = 3600) -> dict:
    deadline = time.time() + timeout_seconds
    last_state = ""
    while time.time() < deadline:
        status, payload = api_request("GET", get_url, headers={"apikey": api_key})
        if status >= 400:
            raise RuntimeError(f"Poll failed ({status}): {payload}")
        data = json.loads(payload)
        state = data.get("status", "unknown")
        if state != last_state:
            print(f"{label}: {state}...")
            sys.stdout.flush()
            last_state = state
        if state == "succeeded":
            return data
        if state == "failed":
            raise RuntimeError(f"{label} failed: {payload}")
        time.sleep(8)
    raise TimeoutError(f"{label} timed out after {timeout_seconds}s")


def download_file(url: str, destination: Path, api_key: str) -> None:
    if not url.startswith("http"):
        url = f"https://api.pruna.ai{url}"
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, method="GET")
    request.add_header("apikey", api_key)
    with urllib.request.urlopen(request, timeout=600) as response:
        destination.write_bytes(response.read())


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
