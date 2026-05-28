#!/usr/bin/env python3
"""Prepare a Where's-Waldo-style P-Image-Upscale demo and render the comparison video."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Pillow is required. Install with: pip install -r scripts/requirements-comparison.txt"
    ) from exc


REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_OUT = REPO_ROOT / "output/p-image-upscale-comparison/nature-pruna-128mp"
P_IMAGE_PROMPT = (
    "Real documentary landscape photograph, not CGI, not illustration, not 3D render, "
    "not digital painting, not fantasy art. Pacific Northwest old-growth temperate "
    "rainforest, field photo from eye level, shot on Sony A7R V with 24mm lens at f/8, "
    "natural overcast light after rain, muted realistic colors, soft skylight, no golden "
    "hour glow, no oversaturation. Foreground tack-sharp: wet sword ferns, moss on decaying "
    "log, cedar bark texture, tiny mushrooms and leaf litter. Midground: elk partially hidden "
    "between trunks, black ravens on branch, dense understory with layered branches. "
    "Background: receding tree lines, valley fog and distant ridge with atmospheric "
    "perspective, believable depth falloff. Scene packed with complex organic detail at "
    "every distance, imperfect natural asymmetry like a real hike photo, no staging, no "
    "text, no logos, no people, 16:9"
)


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
        raise SystemExit("PRUNA_API_KEY is not set")
    return api_key


def download_file(url: str, destination: Path, api_key: str) -> None:
    request = urllib.request.Request(url, method="GET")
    request.add_header("apikey", api_key)
    with urllib.request.urlopen(request, timeout=600) as response:
        destination.write_bytes(response.read())


def upload_file(path: Path, api_key: str) -> str:
    boundary = f"----pruna-{int(time.time() * 1000)}"
    filename = path.name
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="content"; filename="{filename}"\r\n'
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
    data = json.loads(payload)
    return data["urls"]["get"]


def create_prediction(model: str, input_payload: dict[str, object], api_key: str, *, sync: bool) -> dict:
    headers = {
        "Content-Type": "application/json",
        "apikey": api_key,
        "Model": model,
    }
    if sync:
        headers["Try-Sync"] = "true"
    status, payload = api_request(
        "POST",
        "https://api.pruna.ai/v1/predictions",
        headers=headers,
        data=json.dumps({"input": input_payload}).encode("utf-8"),
    )
    if status >= 400:
        raise RuntimeError(f"Prediction failed ({status}): {payload}")
    return json.loads(payload)


def poll_prediction(get_url: str, api_key: str, *, label: str, timeout_seconds: int = 1800) -> dict:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        status, payload = api_request("GET", get_url, headers={"apikey": api_key})
        if status >= 400:
            raise RuntimeError(f"Poll failed ({status}): {payload}")
        data = json.loads(payload)
        state = data.get("status")
        if state == "succeeded":
            return data
        if state == "failed":
            raise RuntimeError(f"{label} failed: {payload}")
        print(f"{label}: {state}...")
        time.sleep(5)
    raise TimeoutError(f"{label} timed out after {timeout_seconds}s")


def generation_url(data: dict) -> str:
    url = data["generation_url"]
    if url.startswith("http"):
        return url
    return f"https://api.pruna.ai{url}"


def add_hidden_pruna_marker(
    image_path: Path,
    *,
    focal_x: float,
    focal_y: float,
    marker_size_px: int = 8,
) -> tuple[float, float]:
    """Place a tiny Pruna marker that is nearly invisible until extreme zoom."""
    image = Image.open(image_path).convert("RGB")
    width, height = image.size
    center_x = int(focal_x * width)
    center_y = int(focal_y * height)
    half = max(2, marker_size_px // 2)
    draw = ImageDraw.Draw(image)
    box = (
        center_x - half,
        center_y - half,
        center_x + half,
        center_y + half,
    )
    # Subtle moss-green chip that reads as natural clutter at full frame.
    draw.ellipse(box, fill=(34, 92, 58), outline=(18, 58, 36), width=1)
    font = ImageFont.load_default()
    draw.text((center_x - 3, center_y - 5), "P", fill=(210, 245, 220), font=font)
    image.save(image_path, quality=95)
    return focal_x, focal_y


def write_manifest(
    out_dir: Path,
    *,
    before_path: Path,
    after_path: Path,
    output_path: Path,
    focal_x: float,
    focal_y: float,
    target_mp: int,
    seed: int,
    p_image_response: dict,
    upscale_response: dict,
) -> Path:
    manifest = {
        "prompt": P_IMAGE_PROMPT,
        "seed": seed,
        "target_mp": target_mp,
        "upscale_input": {
            "target": target_mp,
            "enhance_details": True,
            "enhance_realism": True,
            "output_format": "jpg",
            "output_quality": 95,
        },
        "focal_point": {"x": focal_x, "y": focal_y, "levels": 4},
        "before": str(before_path),
        "after": str(after_path),
        "output": str(output_path),
        "p_image_prediction": p_image_response,
        "upscale_prediction": upscale_response,
    }
    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest_path


def write_comparison_config(
    out_dir: Path,
    *,
    before_path: Path,
    after_path: Path,
    output_path: Path,
    focal_x: float,
    focal_y: float,
    target_mp: int,
) -> Path:
    config = {
        "before": str(before_path),
        "after": str(after_path),
        "output": str(output_path),
        "title": "P-Image-Upscale · Find Pruna in Nature",
        "after_mp": target_mp,
        "fps": 24,
        "width": 1920,
        "height": 1080,
        "timing": {
            "hook_seconds": 2.0,
            "outro_seconds": 2.0,
            "zoom_seconds": 0.9,
            "slider_seconds": 1.3,
            "hold_after_seconds": 0.6,
            "transition_seconds": 0.7
        },
        "focal_point": {
            "x": focal_x,
            "y": focal_y,
            "levels": 4,
            "labels": [
                "Forest overview",
                "Midground textures",
                "Hidden in the foliage",
                "Found Pruna"
            ]
        }
    }
    config_path = out_dir / "nature-pruna-128mp.config.json"
    config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    return config_path


def render_comparison(config_path: Path, *, keep_frames: bool = False) -> None:
    python = sys.executable
    script = REPO_ROOT / "guides/workflows/_shared/scripts/generate_upscale_comparison.py"
    command = [python, str(script), "--config", str(config_path)]
    if keep_frames:
        command.append("--keep-frames")
    subprocess.run(command, check=True, cwd=REPO_ROOT)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=880042)
    parser.add_argument("--target-mp", type=int, default=128)
    parser.add_argument("--focal-x", type=float, default=0.612)
    parser.add_argument("--focal-y", type=float, default=0.668)
    parser.add_argument("--marker-size", type=int, default=8)
    parser.add_argument(
        "--skip-generate",
        action="store_true",
        help="Reuse existing before/after assets in --out-dir",
    )
    parser.add_argument(
        "--skip-upscale",
        action="store_true",
        help="Reuse existing after image (still requires before unless --skip-generate)",
    )
    parser.add_argument(
        "--skip-render",
        action="store_true",
        help="Prepare assets and config only",
    )
    parser.add_argument("--keep-frames", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    api_key = require_api_key()
    out_dir = args.out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    before_path = out_dir / "nature_before.jpg"
    after_path = out_dir / "nature_after_128mp.jpg"
    output_path = out_dir / "nature-pruna-128mp.mp4"
    base_image_path = out_dir / "nature_base_p-image.jpg"

    p_image_response: dict = {}
    upscale_response: dict = {}

    if not args.skip_generate:
        print("Generating photoreal layered nature scene with p-image...")
        p_image_response = create_prediction(
            "p-image",
            {
                "prompt": P_IMAGE_PROMPT,
                "aspect_ratio": "16:9",
                "seed": args.seed,
                "prompt_upsampling": True,
            },
            api_key,
            sync=True,
        )
        if p_image_response.get("status") != "succeeded":
            get_url = p_image_response["get_url"]
            p_image_response = poll_prediction(get_url, api_key, label="p-image")
        download_file(generation_url(p_image_response), base_image_path, api_key)
        before_path.write_bytes(base_image_path.read_bytes())
        focal_x, focal_y = add_hidden_pruna_marker(
            before_path,
            focal_x=args.focal_x,
            focal_y=args.focal_y,
            marker_size_px=args.marker_size,
        )
        print(f"Hidden Pruna marker placed at ({focal_x:.3f}, {focal_y:.3f})")
    else:
        if not before_path.exists():
            raise SystemExit(f"Missing before image: {before_path}")
        focal_x, focal_y = args.focal_x, args.focal_y

    if not args.skip_upscale:
        print(f"Uploading before image and upscaling to {args.target_mp} MP...")
        file_url = upload_file(before_path, api_key)
        upscale_response = create_prediction(
            "p-image-upscale",
            {
                "image": file_url,
                "target": args.target_mp,
                "enhance_details": True,
                "enhance_realism": True,
                "output_format": "jpg",
                "output_quality": 95,
            },
            api_key,
            sync=False,
        )
        if upscale_response.get("status") != "succeeded":
            upscale_response = poll_prediction(
                upscale_response["get_url"],
                api_key,
                label="p-image-upscale",
                timeout_seconds=3600,
            )
        download_file(generation_url(upscale_response), after_path, api_key)
        print(f"Downloaded upscaled image to {after_path}")
    elif not after_path.exists():
        raise SystemExit(f"Missing after image: {after_path}")

    config_path = write_comparison_config(
        out_dir,
        before_path=before_path,
        after_path=after_path,
        output_path=output_path,
        focal_x=focal_x,
        focal_y=focal_y,
        target_mp=args.target_mp,
    )
    manifest_path = write_manifest(
        out_dir,
        before_path=before_path,
        after_path=after_path,
        output_path=output_path,
        focal_x=focal_x,
        focal_y=focal_y,
        target_mp=args.target_mp,
        seed=args.seed,
        p_image_response=p_image_response,
        upscale_response=upscale_response,
    )
    print(f"Wrote config {config_path}")
    print(f"Wrote manifest {manifest_path}")

    if args.skip_render:
        return 0

    print("Rendering comparison video...")
    render_comparison(config_path, keep_frames=args.keep_frames)
    print(f"Done: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
