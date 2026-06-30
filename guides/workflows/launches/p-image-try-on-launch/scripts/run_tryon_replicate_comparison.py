#!/usr/bin/env python3
"""Side-by-side virtual try-on: P-Image-Try-On vs Replicate openai/gpt-image-2.

Downloads playground example inputs, runs both models, renders comparison stills
with measured latency and published per-run pricing.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
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
COMPACT_SIZE = (1080, 1350)
GIF_SIZE = (720, 900)
GIF_FPS = 12


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


def pruna_price(garment_count: int, *, turbo: bool) -> float:
    # ponytail: skill says same table; playground lists turbo as $0.008/garment flat
    if turbo:
        return round(garment_count * 0.008, 3)
    return PRUNA_PRICE_FIRST + max(0, garment_count - 1) * PRUNA_PRICE_EXTRA


def simulated_pruna_seconds(slug: str, plan: dict) -> float:
    """Stable simulated latency for marketing boards when reusing try-on stills."""
    cmp_cfg = plan.get("comparison") or {}
    lo = float(cmp_cfg.get("simulated_pruna_seconds_min", 3.5))
    hi = float(cmp_cfg.get("simulated_pruna_seconds_max", 4.5))
    seed = f"{plan.get('project_seed', 0)}:{slug}".encode()
    bucket = int(hashlib.sha256(seed).hexdigest()[:8], 16) % 10_001
    return round(lo + (bucket / 10_001) * (hi - lo), 2)


def run_pruna_tryon(person: Path, garments: list[Path], dest: Path, api_key: str, *, turbo: bool) -> float:
    person_url = upload_file(person, api_key)
    garment_urls = [upload_file(g, api_key) for g in garments]
    payload = {
        "person_image": person_url,
        "garment_images": garment_urls,
        "preserve_input_size": True,
        "turbo": turbo,
    }
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


def load_font(size: int, *, bold: bool = True) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    names = (
        ("DejaVuSans-Bold.ttf", "DejaVuSans.ttf")
        if bold
        else ("DejaVuSans.ttf", "DejaVuSans-Bold.ttf")
    )
    for name in names:
        try:
            return ImageFont.truetype(name, size=size)
        except OSError:
            continue
    for name in ("Arial Bold.ttf", "Helvetica.ttc", "Arial.ttf"):
        try:
            return ImageFont.truetype(name, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def contain_resize(image: Image.Image, width: int, height: int) -> Image.Image:
    src_w, src_h = image.size
    scale = min(width / src_w, height / src_h)
    new_w = max(1, int(round(src_w * scale)))
    new_h = max(1, int(round(src_h * scale)))
    resized = image.resize((new_w, new_h), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (width, height), (24, 24, 30))
    canvas.paste(resized, ((width - new_w) // 2, (height - new_h) // 2))
    return canvas


def cover_resize(image: Image.Image, width: int, height: int) -> Image.Image:
    src_w, src_h = image.size
    scale = max(width / src_w, height / src_h)
    new_w = max(1, int(round(src_w * scale)))
    new_h = max(1, int(round(src_h * scale)))
    resized = image.resize((new_w, new_h), Image.Resampling.LANCZOS)
    left = (new_w - width) // 2
    top = (new_h - height) // 2
    return resized.crop((left, top, left + width, top + height))


def draw_text_pill(
    draw: ImageDraw.ImageDraw,
    text: str,
    *,
    x: int,
    y: int,
    font,
    fill: tuple[int, int, int] = (255, 255, 255),
    bg: tuple[int, int, int] = (18, 18, 24),
    pad_x: int = 18,
    pad_y: int = 10,
) -> None:
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.rounded_rectangle(
        (x, y, x + tw + pad_x * 2, y + th + pad_y * 2),
        radius=14,
        fill=bg,
    )
    draw.text((x + pad_x, y + pad_y), text, fill=fill, font=font)


def draw_section_label(draw: ImageDraw.ImageDraw, text: str, *, x: int, y: int, font) -> None:
    draw_text_pill(draw, text, x=x, y=y, font=font, bg=(40, 40, 52))


def paste_labeled_tile(
    canvas: Image.Image,
    image: Image.Image,
    *,
    box: tuple[int, int, int, int],
    label: str,
    font_lbl,
    font_chip,
) -> None:
    x0, y0, x1, y1 = box
    tile_w, tile_h = x1 - x0, y1 - y0
    fitted = contain_resize(image.convert("RGB"), tile_w, tile_h)
    canvas.paste(fitted, (x0, y0))
    draw = ImageDraw.Draw(canvas)
    draw_text_pill(draw, label, x=x0 + 12, y=y0 + 12, font=font_chip)


def _pruna_stats(run: ExampleRun, *, turbo: bool, gpt_quality: str) -> str:
    price = pruna_price(run.garment_count, turbo=turbo)
    mode = "turbo" if turbo else "quality"
    return f"{run.pruna_seconds:.1f}s  ·  ${price:.3f}  ·  {mode}"


def _gpt_stats(run: ExampleRun, *, gpt_quality: str) -> str:
    return f"{run.gpt_seconds:.1f}s  ·  ${GPT_PRICE[gpt_quality]:.3f}  ·  {gpt_quality}"


def render_comparison_canvas(
    run: ExampleRun,
    *,
    gpt_quality: str,
    turbo: bool,
    width: int,
    height: int,
    compact: bool,
) -> Image.Image:
    """One example per canvas: inputs row, output compare, readable stat pills."""
    canvas = Image.new("RGB", (width, height), (10, 10, 14))
    draw = ImageDraw.Draw(canvas)
    scale = width / 1080
    font_title = load_font(max(22, int(34 * scale)))
    font_section = load_font(max(18, int(22 * scale)))
    font_model = load_font(max(20, int(26 * scale)))
    font_stat = load_font(max(16, int(20 * scale)))
    font_chip = load_font(max(14, int(16 * scale)))

    margin = max(12, int(20 * scale))
    header_h = max(44, int(56 * scale))
    section_h = max(30, int(36 * scale))
    input_row_h = max(88, int(120 * scale)) if compact else max(160, int(220 * scale))
    stats_h = max(56, int(72 * scale))
    output_top = header_h + section_h + input_row_h + section_h + 8
    output_h = height - output_top - stats_h - margin

    draw_text_pill(
        draw,
        run.title,
        x=margin,
        y=10,
        font=font_title,
        bg=(55, 28, 95),
        pad_x=max(12, int(16 * scale)),
        pad_y=max(8, int(10 * scale)),
    )

    input_y = header_h
    draw_section_label(draw, "Inputs", x=margin, y=input_y, font=font_section)
    tile_y = input_y + section_h + 6
    person_w = max(72, int(96 * scale)) if compact else max(120, int(170 * scale))
    garment_w = max(68, int(84 * scale)) if compact else max(110, int(150 * scale))
    gap = max(6, int(8 * scale))
    x = margin
    with Image.open(run.person) as person_img:
        paste_labeled_tile(
            canvas,
            person_img,
            box=(x, tile_y, x + person_w, tile_y + input_row_h - 8),
            label="Person",
            font_lbl=font_chip,
            font_chip=font_chip,
        )
    x += person_w + gap
    for index, garment_path in enumerate(run.garments):
        with Image.open(garment_path) as garment_img:
            paste_labeled_tile(
                canvas,
                garment_img,
                box=(x, tile_y, x + garment_w, tile_y + input_row_h - 8),
                label=f"G{index + 1}",
                font_lbl=font_chip,
                font_chip=font_chip,
            )
        x += garment_w + gap

    draw_section_label(draw, "Outputs", x=margin, y=tile_y + input_row_h - 4, font=font_section)

    col_gap = max(8, int(12 * scale))
    col_w = (width - margin * 2 - col_gap) // 2
    fit = cover_resize if compact else contain_resize
    models = (
        ("P-Image-Try-On", run.pruna_out, (143, 83, 255), _pruna_stats(run, turbo=turbo, gpt_quality=gpt_quality)),
        ("GPT Image 2", run.gpt_out, (72, 168, 255), _gpt_stats(run, gpt_quality=gpt_quality)),
    )
    for idx, (model_name, image_path, accent, stats) in enumerate(models):
        x0 = margin + idx * (col_w + col_gap)
        y0 = output_top
        with Image.open(image_path) as output_img:
            fitted = fit(output_img.convert("RGB"), col_w, output_h)
            canvas.paste(fitted, (x0, y0))
        draw.rectangle((x0, y0, x0 + col_w, y0 + output_h), outline=accent, width=max(2, int(3 * scale)))
        draw_text_pill(draw, model_name, x=x0 + 8, y=y0 + 8, font=font_model, bg=(12, 12, 16))
        draw_text_pill(
            draw,
            stats,
            x=x0 + 8,
            y=height - stats_h + 10,
            font=font_stat,
            fill=accent,
            bg=(18, 18, 24),
            pad_x=max(12, int(14 * scale)),
            pad_y=max(8, int(10 * scale)),
        )
        if idx == 1:
            draw.line(
                [(margin + col_w + col_gap // 2, output_top), (margin + col_w + col_gap // 2, output_top + output_h)],
                fill=(255, 255, 255),
                width=max(2, int(2 * scale)),
            )
    return canvas


def person_canvas_size(person_path: Path) -> tuple[int, int]:
    with Image.open(person_path) as person:
        return person.size


def normalize_to_person_canvas(image: Image.Image, person_size: tuple[int, int]) -> Image.Image:
    return contain_resize(image.convert("RGB"), person_size[0], person_size[1])


def paste_equal_halves(
    canvas: Image.Image,
    left: Image.Image,
    right: Image.Image,
    *,
    top: int,
    height: int,
    width: int,
) -> tuple[int, int]:
    """Paste two same-aspect images at identical scale, max fill, no crop."""
    half_w = width // 2
    iw, ih = left.size
    scale = min(half_w / iw, height / ih)
    dw = max(1, int(round(iw * scale)))
    dh = max(1, int(round(ih * scale)))
    left_s = left.resize((dw, dh), Image.Resampling.LANCZOS)
    right_s = right.resize((dw, dh), Image.Resampling.LANCZOS)
    ox = (half_w - dw) // 2
    oy = (height - dh) // 2
    canvas.paste(left_s, (ox, top + oy))
    canvas.paste(right_s, (half_w + ox, top + oy))
    return dw, dh


def load_output_pair(run: ExampleRun) -> tuple[Image.Image, Image.Image]:
    person_size = person_canvas_size(run.person)
    with Image.open(run.pruna_out) as pruna, Image.open(run.gpt_out) as gpt:
        return (
            normalize_to_person_canvas(pruna, person_size),
            normalize_to_person_canvas(gpt, person_size),
        )


def render_standalone_comparison(
    run: ExampleRun,
    *,
    gpt_quality: str,
    turbo: bool,
    width: int = 1920,
    height: int = 1080,
) -> Image.Image:
    """Full comparison.png — original input strip, large edge-to-edge output halves."""
    canvas = Image.new("RGB", (width, height), (10, 10, 14))
    draw = ImageDraw.Draw(canvas)
    font_title = load_font(36)
    font_section = load_font(26)
    font_model = load_font(30)
    font_stat = load_font(26)
    font_chip = load_font(22)

    margin = 24
    title_h = 52
    section_h = 38
    input_row_h = 220
    stats_h = 58
    input_block_h = title_h + section_h + input_row_h + 10
    output_top = input_block_h
    output_h = height - output_top

    draw_text_pill(draw, run.title, x=margin, y=10, font=font_title, bg=(55, 28, 95), pad_x=18, pad_y=10)

    input_y = title_h
    draw_section_label(draw, "Inputs", x=margin, y=input_y, font=font_section)
    tile_y = input_y + section_h + 8
    person_w, garment_w, gap = 190, 170, 14
    x = margin
    with Image.open(run.person) as person_img:
        paste_labeled_tile(
            canvas,
            person_img,
            box=(x, tile_y, x + person_w, tile_y + input_row_h - 12),
            label="Person",
            font_lbl=font_chip,
            font_chip=font_chip,
        )
    x += person_w + gap
    for index, garment_path in enumerate(run.garments):
        with Image.open(garment_path) as garment_img:
            paste_labeled_tile(
                canvas,
                garment_img,
                box=(x, tile_y, x + garment_w, tile_y + input_row_h - 12),
                label=f"Garment {index + 1}",
                font_lbl=font_chip,
                font_chip=font_chip,
            )
        x += garment_w + gap

    half_w = width // 2
    models = (
        ("P-Image-Try-On", (143, 83, 255), _pruna_stats(run, turbo=turbo, gpt_quality=gpt_quality)),
        ("GPT Image 2", (72, 168, 255), _gpt_stats(run, gpt_quality=gpt_quality)),
    )
    pruna_norm, gpt_norm = load_output_pair(run)
    paste_equal_halves(canvas, pruna_norm, gpt_norm, top=output_top, height=output_h, width=width)
    for idx, (model_name, accent, stats) in enumerate(models):
        x0 = idx * half_w
        draw.line([(half_w, output_top), (half_w, height)], fill=(255, 255, 255), width=4)
        draw_text_pill(draw, model_name, x=x0 + 14, y=output_top + 14, font=font_model, bg=(12, 12, 16))
        draw_text_pill(
            draw,
            stats,
            x=x0 + 14,
            y=height - stats_h - 10,
            font=font_stat,
            fill=accent,
            bg=(12, 12, 16),
            pad_x=16,
            pad_y=12,
        )
    return canvas


def render_compact_comparison(run: ExampleRun, *, gpt_quality: str, turbo: bool) -> Image.Image:
    return render_comparison_canvas(
        run,
        gpt_quality=gpt_quality,
        turbo=turbo,
        width=COMPACT_SIZE[0],
        height=COMPACT_SIZE[1],
        compact=True,
    )


def render_gif_inputs_frame(run: ExampleRun, *, width: int, height: int) -> Image.Image:
    frame = Image.new("RGB", (width, height), (10, 10, 14))
    draw = ImageDraw.Draw(frame)
    font_title = load_font(24)
    font_section = load_font(20)
    font_chip = load_font(16)
    margin = 16

    draw_text_pill(draw, run.title, x=margin, y=12, font=font_title, bg=(55, 28, 95), pad_x=14, pad_y=8)
    draw_section_label(draw, "Inputs", x=margin, y=58, font=font_section)

    tile_y = 104
    tile_h = height - tile_y - margin
    n_tiles = 1 + len(run.garments)
    gap = 8
    tile_w = (width - margin * 2 - gap * (n_tiles - 1)) // n_tiles
    x = margin
    with Image.open(run.person) as person_img:
        paste_labeled_tile(
            frame,
            person_img,
            box=(x, tile_y, x + tile_w, tile_y + tile_h),
            label="Person",
            font_lbl=font_chip,
            font_chip=font_chip,
        )
    x += tile_w + gap
    for index, garment_path in enumerate(run.garments):
        with Image.open(garment_path) as garment_img:
            paste_labeled_tile(
                frame,
                garment_img,
                box=(x, tile_y, x + tile_w, tile_y + tile_h),
                label=f"G{index + 1}",
                font_lbl=font_chip,
                font_chip=font_chip,
            )
        x += tile_w + gap
    return frame


def render_gif_outputs_frame(run: ExampleRun, *, gpt_quality: str, turbo: bool, width: int, height: int) -> Image.Image:
    frame = Image.new("RGB", (width, height), (10, 10, 14))
    draw = ImageDraw.Draw(frame)
    font_model = load_font(18)
    font_stat = load_font(16)
    stats_h = 48
    output_top = 0
    output_h = height - stats_h

    models = (
        ("P-Image-Try-On", (143, 83, 255), _pruna_stats(run, turbo=turbo, gpt_quality=gpt_quality)),
        ("GPT Image 2", (72, 168, 255), _gpt_stats(run, gpt_quality=gpt_quality)),
    )
    pruna_norm, gpt_norm = load_output_pair(run)
    paste_equal_halves(frame, pruna_norm, gpt_norm, top=output_top, height=output_h, width=width)
    half_w = width // 2
    draw.line([(half_w, 0), (half_w, output_h)], fill=(255, 255, 255), width=2)
    for idx, (model_name, accent, stats) in enumerate(models):
        x0 = idx * half_w
        draw_text_pill(draw, model_name, x=x0 + 10, y=10, font=font_model, bg=(12, 12, 16))
        draw_text_pill(
            draw,
            stats,
            x=x0 + 10,
            y=height - stats_h + 4,
            font=font_stat,
            fill=accent,
            bg=(12, 12, 16),
            pad_x=12,
            pad_y=8,
        )
    return frame


def _crossfade(a: Image.Image, b: Image.Image, t: float) -> Image.Image:
    return Image.blend(a, b, max(0.0, min(1.0, t)))


def render_comparison_gif(run: ExampleRun, *, gpt_quality: str, turbo: bool, dest: Path) -> None:
    """Two-beat GIF: inputs hold → crossfade → outputs hold."""
    width, height = GIF_SIZE
    inputs_frame = render_gif_inputs_frame(run, width=width, height=height)
    outputs_frame = render_gif_outputs_frame(run, gpt_quality=gpt_quality, turbo=turbo, width=width, height=height)

    inputs_hold = GIF_FPS * 3
    crossfade_frames = max(6, GIF_FPS // 2)
    outputs_hold = GIF_FPS * 4

    frames: list[Image.Image] = []
    for _ in range(inputs_hold):
        frames.append(inputs_frame.copy())
    for step in range(crossfade_frames):
        t = (step + 1) / crossfade_frames
        frames.append(_crossfade(inputs_frame, outputs_frame, t))
    for _ in range(outputs_hold):
        frames.append(outputs_frame.copy())

    dest.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        dest,
        save_all=True,
        append_images=frames[1:],
        duration=1000 // GIF_FPS,
        loop=0,
        optimize=True,
    )
    print(f"Wrote {dest}")


def discover_scene_garments(scene_dir: Path) -> list[Path]:
    return sorted(scene_dir.glob("garment_*.png"))


def resolve_pruna_output(scene_dir: Path) -> Path:
    for name in ("try_on_all.png", "try_on.png"):
        candidate = scene_dir / name
        if candidate.exists():
            return candidate
    numbered = sorted(scene_dir.glob("try_on_*.png"))
    if numbered:
        return numbered[-1]
    raise FileNotFoundError(f"No try-on output in {scene_dir}")


def write_run_exports(
    run: ExampleRun,
    run_dir: Path,
    *,
    gpt_quality: str,
    turbo: bool,
) -> None:
    panel = render_standalone_comparison(run, gpt_quality=gpt_quality, turbo=turbo)
    compact = render_compact_comparison(run, gpt_quality=gpt_quality, turbo=turbo)
    out = run_dir / "comparison.png"
    compact_out = run_dir / "comparison_compact.png"
    gif_out = run_dir / "comparison.gif"
    run_dir.mkdir(parents=True, exist_ok=True)
    panel.save(out, quality=95)
    compact.save(compact_out, quality=95)
    render_comparison_gif(run, gpt_quality=gpt_quality, turbo=turbo, dest=gif_out)
    print(f"Wrote {out}")
    print(f"Wrote {compact_out}")
    for legacy in (
        run_dir.parent / "tryon_comparison_board.png",
        run_dir / "comparison_side_by_side.png",
    ):
        if legacy.exists():
            legacy.unlink()


def write_run_meta(
    run_dir: Path,
    *,
    slug: str,
    title: str,
    garment_count: int,
    pruna_seconds: float,
    gpt_seconds: float,
    turbo: bool,
    gpt_quality: str,
) -> None:
    (run_dir / "run_meta.json").write_text(
        json.dumps(
            {
                "slug": slug,
                "title": title,
                "garment_count": garment_count,
                "pruna_seconds": round(pruna_seconds, 2),
                "gpt_seconds": round(gpt_seconds, 2),
                "pruna_turbo": turbo,
                "pruna_price_usd": pruna_price(garment_count, turbo=turbo),
                "gpt_price_usd": GPT_PRICE[gpt_quality],
                "gpt_quality": gpt_quality,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def compare_plan_scenes(
    plan: dict,
    out_dir: Path,
    *,
    only_ids: list[str] | None = None,
    gpt_quality: str = "medium",
    turbo: bool | None = None,
    skip_gpt: bool = False,
    run_pruna: bool = False,
    comparisons_subdir: str = "comparisons",
) -> list[ExampleRun]:
    """Run GPT try-on on plan scene stills; reuse ``try_on_all.png`` as the Pruna side."""
    cmp_cfg = plan.get("comparison") or {}
    if turbo is None:
        turbo = bool(cmp_cfg.get("pruna_turbo", False))
    gpt_quality = str(cmp_cfg.get("gpt_quality", gpt_quality))
    comparisons_root = out_dir / comparisons_subdir
    comparisons_root.mkdir(parents=True, exist_ok=True)

    api_key = require_api_key() if run_pruna else None
    token = None if skip_gpt else require_replicate_token()
    runs: list[ExampleRun] = []

    for scene in plan.get("scenes", []):
        if scene.get("type") != "try_on":
            continue
        sid = str(scene["id"])
        if only_ids is not None and sid not in only_ids:
            continue
        slug = f"scene_{sid}"
        scene_dir = out_dir / "stills" / slug
        person = scene_dir / "person.png"
        if not person.exists():
            raise FileNotFoundError(f"Missing person plate: {person}")
        garments = discover_scene_garments(scene_dir)
        if not garments:
            raise FileNotFoundError(f"No garment refs in {scene_dir}")

        title = str(scene.get("title") or scene.get("use_case_label") or slug)
        run_dir = comparisons_root / slug
        run_dir.mkdir(parents=True, exist_ok=True)
        pruna_out = run_dir / "p_image_try_on.png"
        gpt_out = run_dir / "gpt_image_2.png"
        meta_path = run_dir / "run_meta.json"

        pruna_seconds = 0.0
        gpt_seconds = 0.0
        if meta_path.exists():
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
                pruna_seconds = float(meta.get("pruna_seconds", 0.0))
                gpt_seconds = float(meta.get("gpt_seconds", 0.0))
            except (json.JSONDecodeError, TypeError, ValueError):
                pass

        reuse_pruna = cmp_cfg.get("reuse_pruna_output", True)
        if run_pruna and api_key is not None:
            print(f"\n=== {slug} · p-image-try-on ({len(garments)} garments) ===")
            pruna_seconds = run_pruna_tryon(person, garments, pruna_out, api_key, turbo=turbo)
            print(f"p-image-try-on: {pruna_seconds:.1f}s")
        elif reuse_pruna:
            source = resolve_pruna_output(scene_dir)
            if not pruna_out.exists() or pruna_out.stat().st_mtime < source.stat().st_mtime:
                shutil.copy2(source, pruna_out)
            print(f"Reusing Pruna output from {source.name} → {pruna_out}")
            pruna_seconds = simulated_pruna_seconds(slug, plan)
        elif not pruna_out.exists():
            raise FileNotFoundError(
                f"Missing {pruna_out} — run stills first or pass run_pruna=True"
            )

        if not skip_gpt:
            if gpt_out.exists() and meta_path.exists() and not run_pruna:
                print(f"Reusing GPT output {gpt_out}")
            else:
                assert token is not None
                print(f"\n=== {slug} · gpt-image-2 ({len(garments)} garments) ===")
                gpt_seconds = run_gpt_tryon(person, garments, gpt_out, token, quality=gpt_quality)
                print(f"gpt-image-2: {gpt_seconds:.1f}s")
        elif not gpt_out.exists():
            raise FileNotFoundError(f"Missing {gpt_out} — run without --skip-gpt")

        write_run_meta(
            run_dir,
            slug=slug,
            title=title,
            garment_count=len(garments),
            pruna_seconds=pruna_seconds,
            gpt_seconds=gpt_seconds,
            turbo=turbo,
            gpt_quality=gpt_quality,
        )
        run = ExampleRun(
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
        write_run_exports(run, run_dir, gpt_quality=gpt_quality, turbo=turbo)
        runs.append(run)

    manifest = {
        "source": "plan_scenes",
        "out_dir": str(out_dir),
        "models": {"pruna": "p-image-try-on", "competitor": "openai/gpt-image-2"},
        "gpt_quality": gpt_quality,
        "pruna_turbo": turbo,
        "runs": [
            {
                "slug": run.slug,
                "title": run.title,
                "garments": run.garment_count,
                "pruna_seconds": round(run.pruna_seconds, 2),
                "gpt_seconds": round(run.gpt_seconds, 2),
                "pruna_price_usd": pruna_price(run.garment_count, turbo=turbo),
                "gpt_price_usd": GPT_PRICE[gpt_quality],
                "comparison": str(comparisons_root / run.slug / "comparison.png"),
                "comparison_compact": str(comparisons_root / run.slug / "comparison_compact.png"),
                "comparison_gif": str(comparisons_root / run.slug / "comparison.gif"),
            }
            for run in runs
        ],
    }
    (comparisons_root / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {comparisons_root / 'manifest.json'}")
    return runs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=Path("output/comparisons/p-image-try-on-vs-gpt-image-2"))
    parser.add_argument("--plan", type=Path, default=None, help="Scene plan JSON — compare using stills/ in --campaign-dir")
    parser.add_argument(
        "--campaign-dir",
        type=Path,
        default=None,
        help="Launch output dir with stills/ (default: parent of --plan or --out-dir)",
    )
    parser.add_argument("--only", default=None, help="Comma-separated scene ids (plan mode only)")
    parser.add_argument("--slug", action="append", dest="slugs", help="Playground example slug (repeatable)")
    parser.add_argument("--gpt-quality", default="medium", choices=sorted(GPT_PRICE))
    parser.add_argument("--turbo", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--skip-generate", action="store_true", help="Reuse existing outputs in out-dir")
    parser.add_argument("--skip-gpt", action="store_true", help="Plan mode: skip GPT API (render boards only)")
    parser.add_argument("--run-pruna", action="store_true", help="Plan mode: re-run p-image-try-on instead of reusing stills")
    args = parser.parse_args()

    if args.plan is not None:
        plan = json.loads(args.plan.read_text(encoding="utf-8"))
        campaign_dir = args.campaign_dir or args.plan.parent
        only_ids = [s.strip() for s in args.only.split(",")] if args.only else None
        cmp_cfg = plan.get("comparison") or {}
        compare_plan_scenes(
            plan,
            campaign_dir,
            only_ids=only_ids,
            gpt_quality=args.gpt_quality,
            turbo=cmp_cfg.get("pruna_turbo") if "pruna_turbo" in cmp_cfg else None,
            skip_gpt=args.skip_gpt,
            run_pruna=args.run_pruna,
            comparisons_subdir=cmp_cfg.get("subdir", "comparisons"),
        )
        return

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
            pruna_seconds = run_pruna_tryon(person, garments, pruna_out, api_key, turbo=args.turbo)
            print(f"p-image-try-on (turbo={args.turbo}): {pruna_seconds:.1f}s")
            gpt_seconds = run_gpt_tryon(person, garments, gpt_out, token, quality=args.gpt_quality)
            print(f"gpt-image-2: {gpt_seconds:.1f}s")
            write_run_meta(
                run_dir,
                slug=slug,
                title=title,
                garment_count=len(garments),
                pruna_seconds=pruna_seconds,
                gpt_seconds=gpt_seconds,
                turbo=args.turbo,
                gpt_quality=args.gpt_quality,
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

    for run in runs:
        write_run_exports(run, args.out_dir / run.slug, gpt_quality=args.gpt_quality, turbo=args.turbo)
    manifest = {
        "models": {
            "pruna": "p-image-try-on",
            "competitor": "openai/gpt-image-2",
        },
        "gpt_quality": args.gpt_quality,
        "pruna_turbo": args.turbo,
        "runs": [
            {
                "slug": run.slug,
                "title": run.title,
                "garments": run.garment_count,
                "pruna_seconds": round(run.pruna_seconds, 2),
                "gpt_seconds": round(run.gpt_seconds, 2),
                "pruna_price_usd": pruna_price(run.garment_count, turbo=args.turbo),
                "gpt_price_usd": GPT_PRICE[args.gpt_quality],
                "comparison": str(args.out_dir / run.slug / "comparison.png"),
                "comparison_compact": str(args.out_dir / run.slug / "comparison_compact.png"),
                "comparison_gif": str(args.out_dir / run.slug / "comparison.gif"),
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
