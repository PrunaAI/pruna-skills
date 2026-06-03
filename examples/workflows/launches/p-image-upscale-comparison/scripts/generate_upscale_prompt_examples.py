#!/usr/bin/env python3
"""Generate prompt examples with 32 / 64 / 128 MP upscale tier comparisons."""

from __future__ import annotations

import argparse
import html
import json
import os
import textwrap
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
DEFAULT_OUT = REPO_ROOT / "output/launches/p-image-upscale-comparison/prompt-examples"
DEFAULT_TARGETS = (32, 64, 128)
Image.MAX_IMAGE_PIXELS = 200_000_000

EXAMPLES: list[dict[str, object]] = [
    {
        "id": "perfume-product",
        "title": "Product hero",
        "prompt": (
            "Real product photograph, not CGI. Luxury perfume bottle on black marble "
            "with soft studio rim light, condensation droplets, crisp glass reflections, "
            "minimal composition, commercial packshot, 16:9"
        ),
        "seed": 12001,
        "aspect_ratio": "16:9",
    },
    {
        "id": "street-portrait",
        "title": "Documentary portrait",
        "prompt": (
            "Real documentary portrait photograph, not CGI, not illustration. Elderly "
            "bookshop owner in Tokyo alley, natural window light, shallow depth of field, "
            "visible skin texture and fabric weave, candid moment, 16:9"
        ),
        "seed": 12002,
        "aspect_ratio": "16:9",
    },
    {
        "id": "rainforest-macro",
        "title": "Nature macro",
        "prompt": (
            "Real macro nature photograph, not CGI. Dew-covered fern fronds and mushroom "
            "cluster on forest floor, soft overcast light, extreme fine organic detail, "
            "shallow focus falloff, 16:9"
        ),
        "seed": 12003,
        "aspect_ratio": "16:9",
    },
    {
        "id": "sushi-counter",
        "title": "Food detail",
        "prompt": (
            "Real food photograph, not CGI. Omakase sushi counter close view, glistening fish "
            "texture, rice grain detail, chef hands blurred in background, warm tungsten "
            "restaurant light, editorial food photography, 16:9"
        ),
        "seed": 12005,
        "aspect_ratio": "16:9",
    },
    {
        "id": "fabric-fashion",
        "title": "Fabric and fashion",
        "prompt": (
            "Real fashion editorial photograph, not CGI. Model in emerald silk dress, visible "
            "thread weave and fold highlights, soft window light, textured stone wall "
            "background, shallow depth of field, 16:9"
        ),
        "seed": 12006,
        "aspect_ratio": "16:9",
    },
]


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
    with urllib.request.urlopen(request, timeout=900) as response:
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


def poll_prediction(get_url: str, api_key: str, *, label: str, timeout_seconds: int = 7200) -> dict:
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


def poll_jobs(jobs: list[dict[str, object]], api_key: str, *, timeout_seconds: int = 7200) -> dict[str, dict]:
    pending = {str(job["label"]): str(job["get_url"]) for job in jobs}
    deadline = time.time() + timeout_seconds
    completed: dict[str, dict] = {}

    while pending and time.time() < deadline:
        for label, get_url in list(pending.items()):
            status, payload = api_request("GET", get_url, headers={"apikey": api_key})
            if status >= 400:
                raise RuntimeError(f"Poll failed ({status}): {payload}")
            data = json.loads(payload)
            state = data.get("status")
            if state == "succeeded":
                completed[label] = data
                del pending[label]
                print(f"{label}: succeeded")
            elif state == "failed":
                raise RuntimeError(f"{label} failed: {payload}")
            else:
                print(f"{label}: {state}...")
        if pending:
            time.sleep(5)

    if pending:
        raise TimeoutError(f"Timed out waiting for: {', '.join(pending)}")
    return completed


def generation_url(data: dict) -> str:
    url = data["generation_url"]
    if url.startswith("http"):
        return url
    return f"https://api.pruna.ai{url}"


def megapixels(path: Path) -> float:
    with Image.open(path) as image:
        width, height = image.size
    return round((width * height) / 1_000_000, 2)


def fit_height(image: Image.Image, height: int) -> Image.Image:
    width, src_h = image.size
    scale = height / src_h
    return image.resize((max(1, int(width * scale)), height), Image.Resampling.LANCZOS)


def after_path_for(example_dir: Path, target_mp: int) -> Path:
    return example_dir / f"after_{target_mp}mp.jpg"


def write_tier_preview(
    example_dir: Path,
    *,
    title: str,
    prompt: str,
    before_path: Path,
    tiers: list[dict[str, object]],
    before_mp: float,
) -> Path:
    preview_path = example_dir / "tier_comparison_preview.jpg"
    tile_h = 360
    gutter = 16
    header_h = 130
    tiles: list[Image.Image] = []

    with Image.open(before_path) as before_img:
        before_tile = fit_height(before_img.convert("RGB"), tile_h)
        tiles.append(before_tile)

    for tier in tiers:
        with Image.open(Path(str(tier["path"]))) as after_img:
            tiles.append(fit_height(after_img.convert("RGB"), tile_h))

    canvas_w = sum(tile.size[0] for tile in tiles) + gutter * (len(tiles) - 1)
    canvas = Image.new("RGB", (canvas_w, tile_h + header_h), (22, 22, 22))

    x = 0
    labels = [f"Before {before_mp:g} MP"]
    labels.extend(f"{tier['target_mp']} MP" for tier in tiers)
    for tile, label in zip(tiles, labels):
        canvas.paste(tile, (x, header_h))
        x += tile.size[0] + gutter

    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default()
    draw.text((8, 8), title, fill=(240, 240, 240), font=font)
    draw.text((8, 28), " · ".join(labels), fill=(180, 180, 180), font=font)
    draw.text((8, 48), textwrap.fill(prompt, width=110), fill=(150, 150, 150), font=font)
    canvas.save(preview_path, quality=92)
    return preview_path


def write_gallery_html(out_dir: Path, entries: list[dict[str, object]]) -> Path:
    gallery_path = out_dir / "gallery.html"
    cards: list[str] = []
    for entry in entries:
        rel_before = Path(entry["before"]).relative_to(out_dir).as_posix()
        rel_preview = Path(entry["preview"]).relative_to(out_dir).as_posix()
        tier_figures = []
        for tier in entry["tiers"]:
            rel_after = Path(tier["path"]).relative_to(out_dir).as_posix()
            tier_figures.append(
                f"""
                <figure>
                  <img src="{html.escape(rel_after)}" alt="{tier['target_mp']} MP" />
                  <figcaption>{tier['target_mp']} MP · {tier['actual_mp']} MP actual</figcaption>
                </figure>
                """
            )
        cards.append(
            f"""
            <section class="card">
              <h2>{html.escape(str(entry["title"]))}</h2>
              <p class="meta">seed {entry["seed"]} · before {entry["before_mp"]} MP</p>
              <blockquote>{html.escape(str(entry["prompt"]))}</blockquote>
              <img class="hero" src="{html.escape(rel_preview)}" alt="{html.escape(str(entry["title"]))} tier preview" />
              <div class="tiers">
                <figure>
                  <img src="{html.escape(rel_before)}" alt="before" />
                  <figcaption>Before ({entry["before_mp"]} MP)</figcaption>
                </figure>
                {"".join(tier_figures)}
              </div>
            </section>
            """
        )

    gallery_path.write_text(
        f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>P-Image-Upscale prompt examples</title>
  <style>
    body {{ font-family: system-ui, sans-serif; background: #141414; color: #eee; margin: 0; padding: 32px; }}
    h1 {{ margin-top: 0; }}
    .card {{ background: #1f1f1f; border-radius: 12px; padding: 24px; margin-bottom: 28px; }}
    .meta {{ color: #aaa; margin-top: -8px; }}
    blockquote {{ color: #ccc; border-left: 3px solid #00ff88; margin: 16px 0; padding-left: 12px; }}
    .hero {{ width: 100%; border-radius: 8px; margin: 12px 0 18px; }}
    .tiers {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; }}
    img {{ max-width: 100%; border-radius: 8px; }}
    figcaption {{ color: #aaa; font-size: 13px; margin-top: 8px; }}
    @media (max-width: 1100px) {{ .tiers {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }} }}
  </style>
</head>
<body>
  <h1>P-Image-Upscale · prompt examples</h1>
  <p>Prompt samples with raw <code>p-image</code> output compared across <strong>32 / 64 / 128 MP</strong> upscales.</p>
  {"".join(cards)}
</body>
</html>
""",
        encoding="utf-8",
    )
    return gallery_path


def parse_targets(raw: str) -> list[int]:
    values = [int(part.strip()) for part in raw.split(",") if part.strip()]
    if not values:
        raise SystemExit("Provide at least one target MP, e.g. --targets 32,64,128")
    return values


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument(
        "--targets",
        default="32,64,128",
        help="Comma-separated upscale targets in MP (default: 32,64,128)",
    )
    parser.add_argument("--limit", type=int, default=5, help="Number of prompt examples")
    parser.add_argument("--skip-generate", action="store_true", help="Reuse existing before images")
    parser.add_argument(
        "--force-regenerate",
        action="store_true",
        help="Regenerate p-image even when before already exists",
    )
    parser.add_argument("--skip-upscale", action="store_true", help="Rebuild previews/gallery only")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    api_key = require_api_key()
    out_dir = args.out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    targets = parse_targets(args.targets)

    selected = EXAMPLES[: max(1, min(args.limit, len(EXAMPLES)))]
    entries: list[dict[str, object]] = []
    upscale_jobs: list[dict[str, object]] = []

    for spec in selected:
        example_id = str(spec["id"])
        example_dir = out_dir / example_id
        example_dir.mkdir(parents=True, exist_ok=True)
        before_path = example_dir / "before_p-image.jpg"
        p_image_response: dict = {}

        if not args.skip_generate:
            if before_path.exists() and not args.force_regenerate:
                print(f"[{example_id}] Reusing existing before")
            else:
                print(f"[{example_id}] Generating p-image...")
                p_image_response = create_prediction(
                    "p-image",
                    {
                        "prompt": spec["prompt"],
                        "aspect_ratio": spec["aspect_ratio"],
                        "seed": spec["seed"],
                        "prompt_upsampling": True,
                    },
                    api_key,
                    sync=True,
                )
                if p_image_response.get("status") != "succeeded":
                    p_image_response = poll_prediction(
                        p_image_response["get_url"],
                        api_key,
                        label=f"p-image/{example_id}",
                    )
                download_file(generation_url(p_image_response), before_path, api_key)
        elif not before_path.exists():
            raise SystemExit(f"Missing before image for {example_id}: {before_path}")

        if args.skip_upscale:
            continue

        missing_targets = [
            target
            for target in targets
            if not after_path_for(example_dir, target).exists()
        ]
        if missing_targets:
            file_url = upload_file(before_path, api_key)
            for target_mp in missing_targets:
                print(f"[{example_id}] Queue upscale {target_mp} MP...")
                response = create_prediction(
                    "p-image-upscale",
                    {
                        "image": file_url,
                        "target": target_mp,
                        "enhance_details": True,
                        "enhance_realism": True,
                        "output_format": "jpg",
                        "output_quality": 95,
                    },
                    api_key,
                    sync=False,
                )
                if response.get("status") == "succeeded":
                    download_file(
                        generation_url(response),
                        after_path_for(example_dir, target_mp),
                        api_key,
                    )
                    print(f"[{example_id}] {target_mp} MP succeeded (sync)")
                    continue
                upscale_jobs.append(
                    {
                        "label": f"{example_id}/{target_mp}mp",
                        "get_url": response["get_url"],
                        "example_id": example_id,
                        "example_dir": example_dir,
                        "target_mp": target_mp,
                    }
                )

    if upscale_jobs and not args.skip_upscale:
        print(f"Polling {len(upscale_jobs)} upscale jobs...")
        completed = poll_jobs(upscale_jobs, api_key)
        for job in upscale_jobs:
            label = str(job["label"])
            result = completed[label]
            destination = after_path_for(Path(job["example_dir"]), int(job["target_mp"]))
            download_file(generation_url(result), destination, api_key)
            print(f"[{label}] downloaded")

    for spec in selected:
        example_id = str(spec["id"])
        example_dir = out_dir / example_id
        before_path = example_dir / "before_p-image.jpg"
        if not before_path.exists():
            continue

        tier_rows: list[dict[str, object]] = []
        for target_mp in targets:
            after_path = after_path_for(example_dir, target_mp)
            if not after_path.exists():
                print(f"Warning: missing {after_path}")
                continue
            tier_rows.append(
                {
                    "target_mp": target_mp,
                    "path": str(after_path),
                    "actual_mp": megapixels(after_path),
                }
            )

        if not tier_rows:
            continue

        before_mp = megapixels(before_path)
        preview_path = write_tier_preview(
            example_dir,
            title=str(spec["title"]),
            prompt=str(spec["prompt"]),
            before_path=before_path,
            tiers=tier_rows,
            before_mp=before_mp,
        )

        meta_path = example_dir / "meta.json"
        existing: dict = {}
        if meta_path.exists():
            existing = json.loads(meta_path.read_text(encoding="utf-8"))

        entry = {
            "id": example_id,
            "title": spec["title"],
            "prompt": spec["prompt"],
            "seed": spec["seed"],
            "before": str(before_path),
            "preview": str(preview_path),
            "before_mp": before_mp,
            "targets": targets,
            "tiers": tier_rows,
            "p_image_prediction": existing.get("p_image_prediction", {}),
        }
        meta_path.write_text(json.dumps(entry, indent=2) + "\n", encoding="utf-8")
        entries.append(entry)
        tier_summary = ", ".join(
            f"{tier['target_mp']}→{tier['actual_mp']} MP" for tier in tier_rows
        )
        print(f"[{example_id}] gallery ready · {tier_summary}")

    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps({"targets": targets, "examples": entries}, indent=2) + "\n",
        encoding="utf-8",
    )
    gallery_path = write_gallery_html(out_dir, entries)
    print(f"Wrote manifest {manifest_path}")
    print(f"Wrote gallery {gallery_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
