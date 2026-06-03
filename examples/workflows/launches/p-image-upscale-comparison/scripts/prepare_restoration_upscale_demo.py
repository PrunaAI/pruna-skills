#!/usr/bin/env python3
"""Option C: generate a master photo, degrade it to fake low-res, upscale, compare."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from io import BytesIO
from pathlib import Path

try:
    from PIL import Image, ImageFilter
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Pillow is required. Install with: pip install -r scripts/requirements-comparison.txt"
    ) from exc


REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_OUT = REPO_ROOT / "output/launches/p-image-upscale-comparison/restoration-vacation-busy-128mp"
P_IMAGE_PROMPT = (
    "Real documentary vacation travel photograph, not CGI, not illustration, not 3D render. "
    "Bustling Mediterranean harbor market on a summer morning, extremely busy and layered: "
    "foreground fish crates and lemon piles on wet cobblestones, midground crowded cafe "
    "tables with checkered cloths, striped awnings, hanging lanterns, tourists and locals "
    "walking between stalls, vendors grilling seafood, colorful boats moored in the harbor, "
    "sail masts and rigging, stacked ceramic bowls, laundry on balconies, cats on stone "
    "steps, distant hillside village and blue sea, every zone filled with small objects and "
    "texture, shot on Leica Q3 28mm f/5.6, natural daylight, realistic colors, chaotic "
    "crowded composition like a real holiday snapshot, slight handheld imperfection, no "
    "readable text, no logos, 16:9"
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
    return json.loads(payload)["urls"]["get"]


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


def make_fake_low_res(
    source_path: Path,
    dest_path: Path,
    *,
    max_width: int,
    jpeg_quality: int,
    blur_radius: float,
    double_compress: bool,
) -> dict[str, object]:
    """Simulate an old compressed phone/web photo from a sharper master."""
    with Image.open(source_path) as master:
        master_rgb = master.convert("RGB")
        orig_w, orig_h = master_rgb.size
        scale = max_width / orig_w
        new_w = max_width
        new_h = max(1, int(orig_h * scale))
        degraded = master_rgb.resize((new_w, new_h), Image.Resampling.BILINEAR)
        if blur_radius > 0:
            degraded = degraded.filter(ImageFilter.GaussianBlur(radius=blur_radius))

        buffer = BytesIO()
        degraded.save(buffer, format="JPEG", quality=jpeg_quality, optimize=True)
        if double_compress:
            buffer.seek(0)
            degraded = Image.open(buffer).convert("RGB")
            buffer = BytesIO()
            degraded.save(buffer, format="JPEG", quality=max(20, jpeg_quality - 8), optimize=True)

        dest_path.write_bytes(buffer.getvalue())

    with Image.open(dest_path) as saved:
        deg_w, deg_h = saved.size
    return {
        "original_size": [orig_w, orig_h],
        "degraded_size": [deg_w, deg_h],
        "max_width": max_width,
        "jpeg_quality": jpeg_quality,
        "blur_radius": blur_radius,
        "double_compress": double_compress,
    }


def write_comparison_config(
    out_dir: Path,
    *,
    before_path: Path,
    after_path: Path,
    output_path: Path,
    before_mp: float,
    target_mp: int,
) -> Path:
    config = {
        "before": str(before_path),
        "after": str(after_path),
        "output": str(output_path),
        "title": "P-Image-Upscale · Photo Restoration",
        "before_mp": before_mp,
        "after_mp": target_mp,
        "fps": 24,
        "width": 1920,
        "height": 1080,
        "timing": {
            "hook_seconds": 2.0,
            "outro_seconds": 2.0,
            "zoom_seconds": 0.8,
            "slider_seconds": 1.2,
            "hold_after_seconds": 0.5,
            "transition_seconds": 0.6,
        },
        "preset": "landscape",
    }
    config_path = out_dir / "restoration-vacation-busy.config.json"
    config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    return config_path


def render_comparison(config_path: Path, *, keep_frames: bool = False) -> None:
    script = REPO_ROOT / "guides/workflows/_shared/scripts/generate_upscale_comparison.py"
    command = [sys.executable, str(script), "--config", str(config_path)]
    if keep_frames:
        command.append("--keep-frames")
    subprocess.run(command, check=True, cwd=REPO_ROOT)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=990088)
    parser.add_argument("--target-mp", type=int, default=128)
    parser.add_argument("--degrade-max-width", type=int, default=512)
    parser.add_argument("--degrade-quality", type=int, default=38)
    parser.add_argument("--degrade-blur", type=float, default=0.7)
    parser.add_argument("--no-double-compress", action="store_true")
    parser.add_argument("--skip-generate", action="store_true")
    parser.add_argument("--skip-degrade", action="store_true")
    parser.add_argument("--skip-upscale", action="store_true")
    parser.add_argument("--skip-render", action="store_true")
    parser.add_argument("--keep-frames", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    api_key = require_api_key()
    out_dir = args.out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    master_path = out_dir / "master_p-image.jpg"
    before_path = out_dir / "fake_lowres_before.jpg"
    after_path = out_dir / f"restored_after_{args.target_mp}mp.jpg"
    output_path = out_dir / "restoration-vacation-busy.mp4"

    p_image_response: dict = {}
    upscale_response: dict = {}
    degrade_meta: dict[str, object] = {}

    if not args.skip_generate:
        print("Generating photoreal travel master with p-image...")
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
            p_image_response = poll_prediction(
                p_image_response["get_url"], api_key, label="p-image"
            )
        download_file(generation_url(p_image_response), master_path, api_key)
        print(f"Saved master {master_path}")
    elif not master_path.exists():
        raise SystemExit(f"Missing master image: {master_path}")

    if not args.skip_degrade:
        print(
            "Creating fake low-res before "
            f"({args.degrade_max_width}px wide, q={args.degrade_quality})..."
        )
        degrade_meta = make_fake_low_res(
            master_path,
            before_path,
            max_width=args.degrade_max_width,
            jpeg_quality=args.degrade_quality,
            blur_radius=args.degrade_blur,
            double_compress=not args.no_double_compress,
        )
        print(f"Saved fake low-res before {before_path} ({degrade_meta['degraded_size']})")
    elif not before_path.exists():
        raise SystemExit(f"Missing before image: {before_path}")

    if not args.skip_upscale:
        print(f"Upscaling fake low-res to {args.target_mp} MP...")
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
        print(f"Saved upscaled after {after_path}")
    elif not after_path.exists():
        raise SystemExit(f"Missing after image: {after_path}")

    with Image.open(before_path) as before_img:
        before_mp = round((before_img.size[0] * before_img.size[1]) / 1_000_000, 2)

    manifest = {
        "concept": "fake_low_res_restoration",
        "prompt": P_IMAGE_PROMPT,
        "seed": args.seed,
        "master": str(master_path),
        "before": str(before_path),
        "after": str(after_path),
        "output": str(output_path),
        "before_mp": before_mp,
        "target_mp": args.target_mp,
        "degrade": degrade_meta,
        "upscale_input": {
            "target": args.target_mp,
            "enhance_details": True,
            "enhance_realism": True,
            "output_format": "jpg",
            "output_quality": 95,
        },
        "p_image_prediction": p_image_response,
        "upscale_prediction": upscale_response,
    }
    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    config_path = write_comparison_config(
        out_dir,
        before_path=before_path,
        after_path=after_path,
        output_path=output_path,
        before_mp=before_mp,
        target_mp=args.target_mp,
    )
    print(f"Wrote manifest {manifest_path}")
    print(f"Wrote config {config_path}")

    if args.skip_render:
        return 0

    print("Rendering comparison video...")
    render_comparison(config_path, keep_frames=args.keep_frames)
    print(f"Done: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
