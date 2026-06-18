#!/usr/bin/env python3
"""Side-by-side virtual try-on: P-Image-Try-On vs Replicate openai/gpt-image-2.

Downloads playground example inputs, runs both models, renders comparison stills
with measured latency and published per-run pricing.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.request
from dataclasses import dataclass
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Pillow required: pip install Pillow") from exc

_SCRIPT_DIR = Path(__file__).resolve().parent
_workflows = _SCRIPT_DIR.parent
while _workflows.name != "workflows" and _workflows.parent != _workflows:
    _workflows = _workflows.parent
_SHARED = _workflows / "_shared" / "scripts"
if str(_SHARED) not in sys.path:
    sys.path.insert(0, str(_SHARED))

from pruna_api import (  # noqa: E402
    create_prediction,
    download_file,
    require_api_key,
    run_prediction,
    upload_file,
)
from replicate_api import (  # noqa: E402
    download_url,
    require_replicate_token,
    run_model_prediction,
    upload_file as replicate_upload,
)

PLAYGROUND_BASE = "https://pruna-playground-production-861e.up.railway.app/api/hf-try-on-doc"
DEFAULT_EXAMPLES = (
    ("dom_vfr_boutique_womens_office", "Virtual fitting room · boutique"),
    ("feat_b2b_art_blazer_set", "B2B catalog · blazer set"),
)
GPT_TRYON_PROMPT = (
    "Virtual clothing try-on. Dress the person in image 1 using the garment reference images. "
    "Change only the outfit — preserve the subject's face, identity, pose, hair, background, "
    "and scene lighting. Photorealistic fit with accurate garment colors and textures."
)
PRUNA_PRICE_FIRST = 0.015
PRUNA_PRICE_EXTRA = 0.008
GPT_PRICE = {"low": 0.012, "medium": 0.047, "high": 0.128, "auto": 0.128}


@dataclass(frozen=True)
class ExampleRun:
    slug: str
    title: str
    person: Path
    garments: list[Path]
    pruna_out: Path
    gpt_out: Path
    pruna_seconds: float
    gpt_seconds: float
    garment_count: int


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for name in ("DejaVuSans-Bold.ttf", "Arial Bold.ttf", "Helvetica.ttc"):
        try:
            return ImageFont.truetype(name, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def cover_resize(image: Image.Image, width: int, height: int) -> Image.Image:
    src_w, src_h = image.size
    scale = max(width / src_w, height / src_h)
    new_w = max(1, int(round(src_w * scale)))
    new_h = max(1, int(round(src_h * scale)))
    resized = image.resize((new_w, new_h), Image.Resampling.LANCZOS)
    left = (new_w - width) // 2
    top = (new_h - height) // 2
    return resized.crop((left, top, left + width, top + height))


def fetch_playground_asset(slug: str, name: str, dest: Path, *, attempts: int = 3) -> bool:
    url = f"{PLAYGROUND_BASE}/{slug}/{name}"
    dest.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(1, attempts + 1):
        request = urllib.request.Request(url, method="GET")
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                if response.status != 200:
                    continue
                dest.write_bytes(response.read())
                if dest.stat().st_size > 0:
                    return True
        except Exception:
            if attempt < attempts:
                time.sleep(1.5 * attempt)
    return False


def discover_garments(slug: str, inputs_dir: Path) -> list[Path]:
    garments: list[Path] = []
    for index in range(12):
        dest = inputs_dir / f"garment_{index}_compressed"
        if not fetch_playground_asset(slug, f"garment_{index}_compressed", dest):
            break
        garments.append(dest)
    return garments


def download_example(slug: str, out_dir: Path) -> tuple[Path, list[Path]]:
    inputs = out_dir / slug / "inputs"
    person = inputs / "person_compressed"
    if not fetch_playground_asset(slug, "person_compressed", person):
        raise SystemExit(f"Missing person image for {slug}")
    garments = discover_garments(slug, inputs)
    if not garments:
        raise SystemExit(f"No garments found for {slug}")
    return person, garments


def pruna_price(garment_count: int) -> float:
    return PRUNA_PRICE_FIRST + max(0, garment_count - 1) * PRUNA_PRICE_EXTRA


def run_pruna_tryon(person: Path, garments: list[Path], dest: Path, api_key: str) -> float:
    person_url = upload_file(person, api_key)
    garment_urls = [upload_file(g, api_key) for g in garments]
    payload = {"person_image": person_url, "garment_images": garment_urls, "preserve_input_size": True}
    started = time.perf_counter()
    # ponytail: sync header for wall-clock latency; falls back to poll if needed
    create = create_prediction("p-image-try-on", payload, api_key)
    if create.get("status") != "succeeded":
        create = run_prediction("p-image-try-on", payload, api_key, label="p-image-try-on")
    elapsed = time.perf_counter() - started
    download_file(create["generation_url"], dest, api_key)
    return elapsed


def run_gpt_tryon(
    person: Path,
    garments: list[Path],
    dest: Path,
    token: str,
    *,
    quality: str,
) -> float:
    image_urls = [replicate_upload(person, token)] + [replicate_upload(g, token) for g in garments]
    payload = {
        "prompt": GPT_TRYON_PROMPT,
        "input_images": image_urls,
        "aspect_ratio": "2:3",
        "quality": quality,
        "number_of_images": 1,
        "output_format": "png",
    }
    started = time.perf_counter()
    result = run_model_prediction("openai/gpt-image-2", payload, token, label="gpt-image-2", timeout_seconds=900)
    elapsed = time.perf_counter() - started
    output = result.get("output")
    if isinstance(output, list):
        url = output[0]
    elif isinstance(output, str):
        url = output
    else:
        raise RuntimeError(f"Unexpected gpt-image-2 output: {json.dumps(result)}")
    download_url(url, dest)
    return elapsed


def render_pair_panel(
    left: Image.Image,
    right: Image.Image,
    *,
    left_title: str,
    right_title: str,
    left_stats: str,
    right_stats: str,
    header: str,
    width: int,
    height: int,
) -> Image.Image:
    half_w = width // 2
    panel_h = height - 120
    canvas = Image.new("RGB", (width, height), (12, 12, 18))
    draw = ImageDraw.Draw(canvas)
    font_hdr = load_font(max(28, width // 42))
    font_lbl = load_font(max(22, width // 52))
    font_stat = load_font(max(18, width // 60))

    bbox = draw.textbbox((0, 0), header, font=font_hdr)
    tw = bbox[2] - bbox[0]
    draw.text(((width - tw) // 2, 16), header, fill=(245, 245, 250), font=font_hdr)

    for idx, (img, title, stats) in enumerate(
        ((left, left_title, left_stats), (right, right_title, right_stats))
    ):
        x0 = idx * half_w
        fitted = cover_resize(img.convert("RGB"), half_w - 24, panel_h - 24)
        canvas.paste(fitted, (x0 + 12, 72))
        draw.text((x0 + 16, panel_h + 78), title, fill=(220, 220, 235), font=font_lbl)
        draw.text((x0 + 16, panel_h + 108), stats, fill=(143, 83, 255) if idx == 0 else (120, 200, 255), font=font_stat)
        if idx == 1:
            draw.line([(half_w, 60), (half_w, height - 8)], fill=(255, 255, 255), width=3)
    return canvas


def render_board(runs: list[ExampleRun], out_path: Path, *, gpt_quality: str) -> None:
    panel_w, panel_h = 1080, 960
    panels: list[Image.Image] = []
    for run in runs:
        with Image.open(run.pruna_out) as pruna_img, Image.open(run.gpt_out) as gpt_img:
            panels.append(
                render_pair_panel(
                    pruna_img,
                    gpt_img,
                    left_title="P-Image-Try-On",
                    right_title="GPT Image 2",
                    left_stats=f"{run.pruna_seconds:.1f}s · ${pruna_price(run.garment_count):.3f} · {run.garment_count} garments",
                    right_stats=f"{run.gpt_seconds:.1f}s · ${GPT_PRICE[gpt_quality]:.3f} · medium edit",
                    header=run.title,
                    width=panel_w,
                    height=panel_h,
                )
            )
    board_h = panel_h * len(panels)
    board = Image.new("RGB", (panel_w, board_h), (12, 12, 18))
    for index, panel in enumerate(panels):
        board.paste(panel, (0, index * panel_h))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    board.save(out_path, quality=95)
    print(f"Wrote {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=Path("output/comparisons/p-image-try-on-vs-gpt-image-2"))
    parser.add_argument("--slug", action="append", dest="slugs", help="Playground example slug (repeatable)")
    parser.add_argument("--gpt-quality", default="medium", choices=sorted(GPT_PRICE))
    parser.add_argument("--skip-generate", action="store_true", help="Reuse existing outputs in out-dir")
    args = parser.parse_args()

    slugs = args.slugs or [slug for slug, _ in DEFAULT_EXAMPLES]
    titles = {slug: title for slug, title in DEFAULT_EXAMPLES}
    api_key = require_api_key()
    token = require_replicate_token()
    runs: list[ExampleRun] = []

    for slug in slugs:
        title = titles.get(slug, slug.replace("_", " "))
        person, garments = download_example(slug, args.out_dir)
        run_dir = args.out_dir / slug
        pruna_out = run_dir / "p_image_try_on.png"
        gpt_out = run_dir / "gpt_image_2.png"

        if args.skip_generate and pruna_out.exists() and gpt_out.exists():
            meta_path = run_dir / "run_meta.json"
            if meta_path.exists():
                meta = json.loads(meta_path.read_text())
                pruna_seconds = float(meta["pruna_seconds"])
                gpt_seconds = float(meta["gpt_seconds"])
            else:
                pruna_seconds = gpt_seconds = 0.0
        else:
            print(f"\n=== {slug} ({len(garments)} garments) ===")
            pruna_seconds = run_pruna_tryon(person, garments, pruna_out, api_key)
            print(f"p-image-try-on: {pruna_seconds:.1f}s")
            gpt_seconds = run_gpt_tryon(person, garments, gpt_out, token, quality=args.gpt_quality)
            print(f"gpt-image-2: {gpt_seconds:.1f}s")
            (run_dir / "run_meta.json").write_text(
                json.dumps(
                    {
                        "slug": slug,
                        "title": title,
                        "garment_count": len(garments),
                        "pruna_seconds": round(pruna_seconds, 2),
                        "gpt_seconds": round(gpt_seconds, 2),
                        "pruna_price_usd": pruna_price(len(garments)),
                        "gpt_price_usd": GPT_PRICE[args.gpt_quality],
                        "gpt_quality": args.gpt_quality,
                    },
                    indent=2,
                )
                + "\n"
            )

        runs.append(
            ExampleRun(
                slug=slug,
                title=title,
                person=person,
                garments=garments,
                pruna_out=pruna_out,
                gpt_out=gpt_out,
                pruna_seconds=pruna_seconds,
                gpt_seconds=gpt_seconds,
                garment_count=len(garments),
            )
        )

    render_board(runs, args.out_dir / "tryon_comparison_board.png", gpt_quality=args.gpt_quality)
    for run in runs:
        with Image.open(run.pruna_out) as pruna_img, Image.open(run.gpt_out) as gpt_img:
            panel = render_pair_panel(
                pruna_img,
                gpt_img,
                left_title="P-Image-Try-On",
                right_title="GPT Image 2",
                left_stats=f"{run.pruna_seconds:.1f}s · ${pruna_price(run.garment_count):.3f} · {run.garment_count} garments",
                right_stats=f"{run.gpt_seconds:.1f}s · ${GPT_PRICE[args.gpt_quality]:.3f} · {args.gpt_quality} edit",
                header=run.title,
                width=1080,
                height=960,
            )
            out = args.out_dir / run.slug / "comparison_side_by_side.png"
            panel.save(out, quality=95)
            print(f"Wrote {out}")
    manifest = {
        "models": {
            "pruna": "p-image-try-on",
            "competitor": "openai/gpt-image-2",
        },
        "gpt_quality": args.gpt_quality,
        "runs": [
            {
                "slug": run.slug,
                "title": run.title,
                "garments": run.garment_count,
                "pruna_seconds": round(run.pruna_seconds, 2),
                "gpt_seconds": round(run.gpt_seconds, 2),
                "pruna_price_usd": pruna_price(run.garment_count),
                "gpt_price_usd": GPT_PRICE[args.gpt_quality],
                "pruna_output": str(run.pruna_out),
                "gpt_output": str(run.gpt_out),
            }
            for run in runs
        ],
    }
    (args.out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Wrote {args.out_dir / 'manifest.json'}")


if __name__ == "__main__":
    main()
