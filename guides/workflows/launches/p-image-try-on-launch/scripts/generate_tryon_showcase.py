#!/usr/bin/env python3
"""Build a vertical try-on showcase clip focused on clothing change effectiveness.

Timeline per beat: garment ref → person photo → side-by-side before/after → wipe reveal → try-on hold.
No upscale, no zoom crops — only outfit swap proof at one fixed aspect ratio.
"""

from __future__ import annotations

import argparse
import json
import random
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Pillow required: pip install Pillow") from exc


@dataclass(frozen=True)
class Timing:
    garment_seconds: float = 2.0
    person_seconds: float = 1.5
    compare_seconds: float = 2.2
    slider_seconds: float = 2.5
    hold_seconds: float = 2.5
    flash_seconds: float = 0.8


@dataclass(frozen=True)
class ShowcaseJob:
    person: Path
    garment: Path
    try_on: Path
    output: Path
    width: int = 1080
    height: int = 1920
    fps: int = 24
    title: str = "Try-on"
    garment_label: str = "Input · garment ref"
    person_label: str = "Input · person photo"
    before_label: str = "Before · base outfit"
    after_label: str = "After · try-on"
    compare_title: str = "Same person · new outfit"
    timing: Timing = Timing()


def ease_in_out(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


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


def load_canvas(path: Path, width: int, height: int) -> Image.Image:
    with Image.open(path) as raw:
        return cover_resize(raw.convert("RGB"), width, height)


def draw_chip(draw: ImageDraw.ImageDraw, text: str, *, x: int, y: int, font) -> None:
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.rounded_rectangle(
        (x - 8, y - 6, x + tw + 16, y + th + 10),
        radius=12,
        fill=(15, 15, 15),
    )
    draw.text((x, y), text, fill=(255, 255, 255), font=font)


def draw_banner(
    canvas: Image.Image,
    *,
    header: str | None = None,
    left_label: str | None = None,
    right_label: str | None = None,
    chip: str | None = None,
    show_labels: bool = True,
) -> Image.Image:
    if not show_labels:
        return canvas.copy()
    out = canvas.copy()
    draw = ImageDraw.Draw(out)
    font_lg = load_font(max(30, out.width // 26))
    font_sm = load_font(max(22, out.width // 34))
    font_hdr = load_font(max(26, out.width // 30))

    if chip:
        draw_chip(draw, chip, x=16, y=16, font=font_sm)

    if header:
        bbox = draw.textbbox((0, 0), header, font=font_hdr)
        tw = bbox[2] - bbox[0]
        hx = (out.width - tw) // 2
        draw.rounded_rectangle(
            (hx - 12, 14, hx + tw + 12, 14 + (bbox[3] - bbox[1]) + 14),
            radius=10,
            fill=(15, 15, 15),
        )
        draw.text((hx, 18), header, fill=(255, 255, 255), font=font_hdr)

    footer_y = out.height - 88
    if left_label:
        draw.text(
            (24, footer_y),
            left_label,
            fill=(255, 255, 255),
            font=font_lg,
            stroke_width=2,
            stroke_fill=(0, 0, 0),
        )
    if right_label:
        bbox = draw.textbbox((0, 0), right_label, font=font_lg)
        tw = bbox[2] - bbox[0]
        draw.text(
            (out.width - tw - 24, footer_y),
            right_label,
            fill=(255, 255, 255),
            font=font_lg,
            stroke_width=2,
            stroke_fill=(0, 0, 0),
        )
    return out


def split_compare_frame(
    before: Image.Image,
    after: Image.Image,
    *,
    before_label: str,
    after_label: str,
    header: str | None = None,
) -> Image.Image:
    width, height = before.size
    half = width // 2
    frame = Image.new("RGB", (width, height))
    frame.paste(before.crop((0, 0, half, height)), (0, 0))
    frame.paste(after.crop((half, 0, width, height)), (half, 0))
    draw = ImageDraw.Draw(frame)
    draw.line([(half, 0), (half, height)], fill=(255, 255, 255), width=6)
    return draw_banner(
        frame,
        header=header,
        left_label=before_label,
        right_label=after_label,
    )


def slider_frame(before: Image.Image, after: Image.Image, t: float) -> Image.Image:
    """Vertical divider moves left → right, revealing try-on on the left."""
    width, height = before.size
    split = int(width * ease_in_out(t))
    frame = before.copy()
    frame.paste(after.crop((0, 0, split, height)), (0, 0))
    draw = ImageDraw.Draw(frame)
    draw.line([(split, 0), (split, height)], fill=(255, 255, 255), width=6)
    return frame


def render_frames(job: ShowcaseJob) -> list[Image.Image]:
    person = load_canvas(job.person, job.width, job.height)
    garment = load_canvas(job.garment, job.width, job.height)
    try_on = load_canvas(job.try_on, job.width, job.height)
    timing = job.timing

    frames: list[Image.Image] = []
    for _ in range(int(timing.garment_seconds * job.fps)):
        frames.append(draw_banner(garment, chip=job.garment_label))
    for _ in range(int(timing.person_seconds * job.fps)):
        frames.append(draw_banner(person, chip=job.person_label))

    for _ in range(int(timing.compare_seconds * job.fps)):
        frames.append(
            split_compare_frame(
                person,
                try_on,
                before_label=job.before_label,
                after_label=job.after_label,
                header=job.compare_title,
            )
        )

    slider_frames = max(1, int(timing.slider_seconds * job.fps))
    for i in range(slider_frames):
        t = i / max(1, slider_frames - 1)
        frame = slider_frame(person, try_on, t)
        frames.append(
            draw_banner(
                frame,
                left_label=job.before_label,
                right_label=job.after_label,
                header=job.compare_title,
            )
        )

    for _ in range(int(timing.hold_seconds * job.fps)):
        frames.append(draw_banner(try_on, chip=job.after_label))

    flash_frames = max(2, int(timing.flash_seconds * job.fps))
    toggle = flash_frames // 2
    for i in range(flash_frames):
        frames.append(
            draw_banner(try_on if i >= toggle else person, chip="Outfit changed" if i >= toggle else job.before_label)
        )
    return frames


def encode_frames(frames: list[Image.Image], output: Path, fps: int) -> None:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg not found")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        for i, frame in enumerate(frames):
            frame.save(tmp_path / f"frame_{i:05d}.png")
        subprocess.run(
            [
                ffmpeg,
                "-y",
                "-framerate",
                str(fps),
                "-i",
                str(tmp_path / "frame_%05d.png"),
                "-c:v",
                "libx264",
                "-preset",
                "fast",
                "-crf",
                "18",
                "-pix_fmt",
                "yuv420p",
                "-movflags",
                "+faststart",
                str(output),
            ],
            check=True,
            capture_output=True,
        )


def job_from_dict(data: dict[str, Any], base: Path) -> ShowcaseJob:
    def resolve(key: str) -> Path:
        value = Path(data[key])
        if not value.is_absolute():
            candidate = (base / value).resolve()
            if candidate.exists():
                return candidate
            return (Path.cwd() / value).resolve()
        return value.resolve()

    timing_raw = data.get("timing") or {}
    timing = Timing(
        garment_seconds=float(timing_raw.get("garment_seconds", 2.0)),
        person_seconds=float(timing_raw.get("person_seconds", 1.5)),
        compare_seconds=float(timing_raw.get("compare_seconds", 2.2)),
        slider_seconds=float(timing_raw.get("slider_seconds", 2.5)),
        hold_seconds=float(timing_raw.get("hold_seconds", 2.5)),
        flash_seconds=float(timing_raw.get("flash_seconds", 0.8)),
    )
    return ShowcaseJob(
        person=resolve("person"),
        garment=resolve("garment"),
        try_on=resolve("try_on"),
        output=resolve("output"),
        width=int(data.get("width", 1080)),
        height=int(data.get("height", 1920)),
        fps=int(data.get("fps", 24)),
        title=str(data.get("title", "Try-on")),
        garment_label=str(data.get("garment_label", "Input · garment ref")),
        person_label=str(data.get("person_label", "Input · person photo")),
        before_label=str(data.get("before_label", "Before · base outfit")),
        after_label=str(data.get("after_label", "After · try-on")),
        compare_title=str(data.get("compare_title", "Same person · new outfit")),
        timing=timing,
    )


def render_showcase(job: ShowcaseJob) -> Path:
    frames = render_frames(job)
    encode_frames(frames, job.output, job.fps)
    return job.output


def render_ladder(
    *,
    person: Path,
    pairs: list[tuple[Path, Path, str]],
    output: Path,
    width: int,
    height: int,
    fps: int,
    timing: Timing,
    person_label: str,
    before_label: str,
    after_label: str,
    compare_title: str,
) -> Path:
    person_img = load_canvas(person, width, height)
    frames: list[Image.Image] = []
    for _ in range(int(timing.person_seconds * fps)):
        frames.append(draw_banner(person_img, chip=person_label))
    for garment_path, try_on_path, garment_label in pairs:
        garment = load_canvas(garment_path, width, height)
        try_on = load_canvas(try_on_path, width, height)
        for _ in range(int(timing.garment_seconds * fps)):
            frames.append(draw_banner(garment, chip=garment_label))
        for _ in range(int(timing.compare_seconds * fps)):
            frames.append(
                split_compare_frame(
                    person_img,
                    try_on,
                    before_label=before_label,
                    after_label=after_label,
                    header=compare_title,
                )
            )
        slider_frames = max(1, int(timing.slider_seconds * fps))
        for i in range(slider_frames):
            t = i / max(1, slider_frames - 1)
            frame = slider_frame(person_img, try_on, t)
            frames.append(
                draw_banner(
                    frame,
                    left_label=before_label,
                    right_label=after_label,
                    header=compare_title,
                )
            )
        for _ in range(int(timing.hold_seconds * fps)):
            frames.append(draw_banner(try_on, chip=after_label))
    encode_frames(frames, output, fps)
    return output


def flash_timing_for_narration(
    narr_seconds: float,
    n_looks: int,
    *,
    crossfade_seconds: float = 0.32,
    tail_pad: float = 0.15,
) -> FlashSwapTiming:
    """Fixed hold + crossfade budget so try-on transitions fill the narration window."""
    total = max(2.5, narr_seconds + tail_pad)
    n_transitions = max(0, n_looks - 1)
    fade_budget = crossfade_seconds * n_transitions
    per_hold = max(0.35, (total - fade_budget) / max(1, n_looks))
    return FlashSwapTiming(
        hold_seconds_min=per_hold,
        hold_seconds_max=per_hold,
        crossfade_seconds=crossfade_seconds,
        shuffle=False,
        wipe_seconds=0,
        cycles=1,
        style="crossfade",
    )


def fit_pose_timing_for_narration(
    narr_seconds: float,
    n_poses: int,
    *,
    garment_ratio: float = 0.1,
) -> Timing:
    """Spread garment intro + every pose beat across the narration window."""
    total = max(3.0, narr_seconds)
    garment = max(0.45, total * garment_ratio)
    remain = max(1.0, total - garment)
    per = remain / max(1, n_poses)
    return Timing(
        garment_seconds=garment,
        person_seconds=max(0.35, per * 0.24),
        compare_seconds=0,
        slider_seconds=max(0.5, per * 0.38),
        hold_seconds=max(0.45, per * 0.38),
        flash_seconds=0,
    )


def render_fit_poses(
    *,
    garment: Path,
    pairs: list[tuple[Path, Path, str]],
    output: Path,
    width: int,
    height: int,
    fps: int,
    timing: Timing,
    garment_label: str,
    person_label: str,
    fit_label: str,
    compare_title: str,
) -> Path:
    """E-commerce PDP beat — one garment, same model identity, multiple poses showing fit."""
    garment_img = load_canvas(garment, width, height)
    frames: list[Image.Image] = []
    for _ in range(max(1, int(timing.garment_seconds * fps))):
        frames.append(draw_banner(garment_img, chip=garment_label, header=compare_title))
    for person_path, try_on_path, pose_label in pairs:
        person_img = load_canvas(person_path, width, height)
        try_on = load_canvas(try_on_path, width, height)
        for _ in range(max(1, int(timing.person_seconds * fps))):
            frames.append(draw_banner(person_img, chip=f"{person_label} · {pose_label}"))
        slider_frames = max(1, int(timing.slider_seconds * fps))
        for i in range(slider_frames):
            t = i / max(1, slider_frames - 1)
            frame = slider_frame(person_img, try_on, t)
            frames.append(
                draw_banner(
                    frame,
                    header=compare_title,
                    left_label=f"{person_label} · {pose_label}",
                    right_label=f"{fit_label} · {pose_label}",
                )
            )
        for _ in range(max(1, int(timing.hold_seconds * fps))):
            frames.append(draw_banner(try_on, chip=f"{fit_label} · {pose_label}"))
    encode_frames(frames, output, fps)
    return output


def render_rapid(
    *,
    person: Path,
    pairs: list[tuple[Path, Path, str]],
    output: Path,
    width: int,
    height: int,
    fps: int,
    person_label: str,
    before_label: str,
    after_label: str,
    compare_title: str,
    timing: Timing,
) -> Path:
    """Fast multi-garment montage — garment flash → wipe → try-on hold, repeated."""
    person_img = load_canvas(person, width, height)
    frames: list[Image.Image] = []
    for _ in range(max(1, int(timing.person_seconds * fps))):
        frames.append(draw_banner(person_img, chip=person_label))
    for garment_path, try_on_path, garment_label in pairs:
        garment = load_canvas(garment_path, width, height)
        try_on = load_canvas(try_on_path, width, height)
        for _ in range(max(1, int(timing.garment_seconds * fps))):
            frames.append(draw_banner(garment, chip=garment_label))
        slider_frames = max(1, int(timing.slider_seconds * fps))
        for i in range(slider_frames):
            t = i / max(1, slider_frames - 1)
            frame = slider_frame(person_img, try_on, t)
            frames.append(
                draw_banner(
                    frame,
                    header=compare_title,
                    left_label=before_label,
                    right_label=after_label,
                )
            )
        for _ in range(max(1, int(timing.hold_seconds * fps))):
            frames.append(draw_banner(try_on, chip=after_label))
    encode_frames(frames, output, fps)
    return output


@dataclass(frozen=True)
class FlashSwapTiming:
    hold_seconds_min: float = 0.5
    hold_seconds_max: float = 1.0
    wipe_seconds: float = 0.08
    crossfade_seconds: float = 0.3
    shuffle: bool = True
    cycles: int = 1
    style: str = "crossfade"
    beat_frames: int = 2
    zoom_peak: float = 1.14
    staccato_frames: int = 3


def _flash_hold_seconds(timing: FlashSwapTiming, rng: random.Random) -> float:
    if timing.hold_seconds_min == timing.hold_seconds_max:
        return timing.hold_seconds_min
    return rng.uniform(timing.hold_seconds_min, timing.hold_seconds_max)


def _fade_seconds(timing: FlashSwapTiming) -> float:
    if timing.crossfade_seconds > 0:
        return timing.crossfade_seconds
    return max(timing.wipe_seconds, 0.25)


def _blend_crossfade(a: Image.Image, b: Image.Image, t: float) -> Image.Image:
    return Image.blend(a, b, ease_in_out(t))


def _append_hold(
    frames: list[Image.Image],
    img: Image.Image,
    *,
    fps: int,
    seconds: float,
    chip: str | None = None,
    show_labels: bool = True,
) -> None:
    for _ in range(max(1, int(seconds * fps))):
        frames.append(draw_banner(img, chip=chip, show_labels=show_labels))


def _append_crossfade(
    frames: list[Image.Image],
    img_a: Image.Image,
    img_b: Image.Image,
    *,
    fps: int,
    fade_seconds: float,
) -> None:
    fade_frames = max(3, int(fade_seconds * fps))
    for i in range(fade_frames):
        t = i / max(1, fade_frames - 1)
        frames.append(_blend_crossfade(img_a, img_b, t))


def _zoom_frame(img: Image.Image, scale: float) -> Image.Image:
    width, height = img.size
    scaled_w = max(1, int(round(width * scale)))
    scaled_h = max(1, int(round(height * scale)))
    resized = img.resize((scaled_w, scaled_h), Image.Resampling.LANCZOS)
    left = (scaled_w - width) // 2
    top = (scaled_h - height) // 2
    return resized.crop((left, top, left + width, top + height))


def _beat_flash_frame(width: int, height: int) -> Image.Image:
    return Image.new("RGB", (width, height), (245, 245, 245))


def _flash_order(count: int, *, shuffle: bool, rng: random.Random, style: str, cycle: int) -> list[int]:
    order = list(range(count))
    if style == "pingpong":
        if count > 1:
            order = order + list(reversed(order[1:-1]))
        return order
    if shuffle:
        rng.shuffle(order)
    return order


def _render_flash_crossfade(
    imgs: list[Image.Image],
    order: list[int],
    *,
    fps: int,
    timing: FlashSwapTiming,
    rng: random.Random,
    chip_labels: list[str],
    show_labels: bool = True,
) -> list[Image.Image]:
    """Hold each look, then ease crossfade into the next — no hard cuts or white flashes."""
    frames: list[Image.Image] = []
    fade = _fade_seconds(timing)
    for pos, idx in enumerate(order):
        hold = _flash_hold_seconds(timing, rng)
        chip = chip_labels[idx] if show_labels and idx < len(chip_labels) else None
        _append_hold(frames, imgs[idx], fps=fps, seconds=hold, chip=chip, show_labels=show_labels)
        if pos < len(order) - 1:
            nxt = imgs[order[pos + 1]]
            _append_crossfade(frames, imgs[idx], nxt, fps=fps, fade_seconds=fade)
    return frames


def compose_garment_grid(
    images: list[Image.Image],
    *,
    width: int,
    height: int,
) -> Image.Image:
    """Lay out multiple product refs in one frame (2×2, 1+2, or vertical stack)."""
    n = len(images)
    canvas = Image.new("RGB", (width, height), (24, 24, 24))
    gap = max(4, width // 120)

    def cell_for(col: int, row: int, cols: int, rows: int) -> tuple[int, int, int, int]:
        cw = (width - gap * (cols + 1)) // cols
        ch = (height - gap * (rows + 1)) // rows
        x0 = gap + col * (cw + gap)
        y0 = gap + row * (ch + gap)
        return x0, y0, cw, ch

    layouts: list[tuple[int, int, int]]  # (image_index, col, row) with implicit grid
    if n == 1:
        layouts = [(0, 0, 0)]
        cols, rows = 1, 1
    elif n == 2:
        layouts = [(0, 0, 0), (1, 0, 1)]
        cols, rows = 1, 2
    elif n == 3:
        layouts = [(0, 0, 0), (1, 0, 1), (2, 0, 2)]
        cols, rows = 1, 3
    else:
        layouts = [(0, 0, 0), (1, 1, 0), (2, 0, 1), (3, 1, 1)]
        cols, rows = 2, 2

    for idx, col, row in layouts[:n]:
        x0, y0, cw, ch = cell_for(col, row, cols, rows)
        tile = cover_resize(images[idx], cw, ch)
        canvas.paste(tile, (x0, y0))
    return canvas


def render_garment_reel(
    *,
    garments: list[Path],
    labels: list[str],
    output: Path,
    width: int,
    height: int,
    fps: int,
    seconds_per_garment: float = 0.55,
    title: str | None = None,
    grid_intro_seconds: float = 0.0,
    show_labels: bool = True,
) -> Path:
    """Product-ref montage — optional all-items grid, then one hold per garment."""
    frames: list[Image.Image] = []
    loaded = [load_canvas(path, width, height) for path in garments]
    if grid_intro_seconds > 0 and len(loaded) > 1:
        grid = compose_garment_grid(loaded, width=width, height=height)
        chip = f"{len(loaded)} product refs" if show_labels else None
        for _ in range(max(1, int(grid_intro_seconds * fps))):
            frames.append(draw_banner(grid, chip=chip, header=title if show_labels else None, show_labels=show_labels))
    for img, label in zip(loaded, labels):
        for _ in range(max(1, int(seconds_per_garment * fps))):
            frames.append(
                draw_banner(img, chip=label if show_labels else None, header=title if show_labels else None, show_labels=show_labels)
            )
    encode_frames(frames, output, fps)
    return output


def garment_flash_timing_for_narration(
    narr_seconds: float,
    n_garments: int,
    n_flash: int,
    *,
    grid_ratio: float = 0.1,
    garment_ratio: float = 0.26,
    crossfade_seconds: float = 0.28,
) -> tuple[float, float, FlashSwapTiming]:
    """Split narration across grid intro, per-garment holds, and try-on flash montage."""
    total = max(3.0, narr_seconds)
    grid_sec = total * grid_ratio if n_garments > 1 else 0.0
    garment_budget = total * garment_ratio
    sec_per_garment = max(0.3, garment_budget / max(1, n_garments))
    flash_budget = max(1.5, total - grid_sec - garment_budget)
    flash_timing = flash_timing_for_narration(
        flash_budget,
        n_flash,
        crossfade_seconds=crossfade_seconds,
        tail_pad=0,
    )
    return grid_sec, sec_per_garment, flash_timing


def render_garment_flash_montage(
    *,
    garments: list[Path],
    try_ons: list[Path],
    output: Path,
    width: int,
    height: int,
    fps: int,
    grid_intro_seconds: float = 0.0,
    seconds_per_garment: float = 0.45,
    flash_timing: FlashSwapTiming,
    seed: int = 0,
    show_labels: bool = True,
) -> Path:
    """Merged product-ref reel + try-on flash — one silent clip for a single narration track."""
    frames: list[Image.Image] = []
    garment_imgs = [load_canvas(path, width, height) for path in garments]
    try_on_imgs = [load_canvas(path, width, height) for path in try_ons]
    rng = random.Random(seed)

    if grid_intro_seconds > 0 and len(garment_imgs) > 1:
        grid = compose_garment_grid(garment_imgs, width=width, height=height)
        for _ in range(max(1, int(grid_intro_seconds * fps))):
            frames.append(draw_banner(grid, show_labels=show_labels))

    for garment in garment_imgs:
        for _ in range(max(1, int(seconds_per_garment * fps))):
            frames.append(draw_banner(garment, show_labels=show_labels))

    order = _flash_order(len(try_on_imgs), shuffle=flash_timing.shuffle, rng=rng, style="crossfade", cycle=0)
    fade = _fade_seconds(flash_timing)
    for pos, idx in enumerate(order):
        hold = _flash_hold_seconds(flash_timing, rng)
        _append_hold(frames, try_on_imgs[idx], fps=fps, seconds=hold, show_labels=show_labels)
        if pos < len(order) - 1:
            nxt = try_on_imgs[order[pos + 1]]
            _append_crossfade(frames, try_on_imgs[idx], nxt, fps=fps, fade_seconds=fade)

    encode_frames(frames, output, fps)
    return output


def _render_flash_shuffle_wipe(
    imgs: list[Image.Image],
    order: list[int],
    *,
    fps: int,
    timing: FlashSwapTiming,
    rng: random.Random,
    chip_labels: list[str],
) -> list[Image.Image]:
    frames: list[Image.Image] = []
    for pos, idx in enumerate(order):
        hold = _flash_hold_seconds(timing, rng)
        chip = chip_labels[idx] if idx < len(chip_labels) else f"Look {idx + 1}"
        for _ in range(max(1, int(hold * fps))):
            frames.append(draw_banner(imgs[idx], chip=chip))
        if timing.wipe_seconds > 0 and pos < len(order) - 1:
            nxt = imgs[order[pos + 1]]
            wipe_frames = max(3, int(timing.wipe_seconds * fps))
            for i in range(wipe_frames):
                t = ease_in_out(i / max(1, wipe_frames - 1))
                frames.append(draw_banner(slider_frame(imgs[idx], nxt, t)))
    return frames


def _render_flash_beat_cut(
    imgs: list[Image.Image],
    order: list[int],
    *,
    fps: int,
    timing: FlashSwapTiming,
    rng: random.Random,
    chip_labels: list[str],
) -> list[Image.Image]:
    width, height = imgs[0].size
    frames: list[Image.Image] = []
    for pos, idx in enumerate(order):
        hold = _flash_hold_seconds(timing, rng)
        chip = chip_labels[idx] if idx < len(chip_labels) else f"Look {idx + 1}"
        pulse_frames = max(1, int(hold * fps))
        for i in range(pulse_frames):
            scale = 1.0 + (timing.zoom_peak - 1.0) * abs((i / max(1, pulse_frames - 1)) - 0.5) * 2.0
            frame = _zoom_frame(imgs[idx], scale)
            frames.append(draw_banner(frame, chip=chip))
        if pos < len(order) - 1:
            nxt = imgs[order[pos + 1]]
            _append_crossfade(frames, imgs[idx], nxt, fps=fps, fade_seconds=max(0.18, _fade_seconds(timing) * 0.65))
    return frames


def _render_flash_zoom_pulse(
    imgs: list[Image.Image],
    order: list[int],
    *,
    fps: int,
    timing: FlashSwapTiming,
    rng: random.Random,
    chip_labels: list[str],
) -> list[Image.Image]:
    frames: list[Image.Image] = []
    fade = _fade_seconds(timing)
    for pos, idx in enumerate(order):
        hold = _flash_hold_seconds(timing, rng)
        chip = chip_labels[idx] if idx < len(chip_labels) else f"Look {idx + 1}"
        pulse_frames = max(2, int(hold * fps))
        for i in range(pulse_frames):
            t = i / max(1, pulse_frames - 1)
            scale = 1.0 + (timing.zoom_peak - 1.0) * (1.0 - abs(2.0 * t - 1.0))
            frame = _zoom_frame(imgs[idx], scale)
            frames.append(draw_banner(frame, chip=chip))
        if pos < len(order) - 1:
            nxt = imgs[order[pos + 1]]
            _append_crossfade(frames, imgs[idx], nxt, fps=fps, fade_seconds=fade)
    return frames


def _render_flash_staccato(
    imgs: list[Image.Image],
    order: list[int],
    *,
    timing: FlashSwapTiming,
    chip_labels: list[str],
) -> list[Image.Image]:
    width, height = imgs[0].size
    frames: list[Image.Image] = []
    for pos, idx in enumerate(order):
        chip = chip_labels[idx] if idx < len(chip_labels) else f"Look {idx + 1}"
        for _ in range(max(2, timing.staccato_frames)):
            frames.append(draw_banner(imgs[idx], chip=chip))
        if pos < len(order) - 1:
            nxt = imgs[order[pos + 1]]
            _append_crossfade(frames, imgs[idx], nxt, fps=fps, fade_seconds=0.2)
    return frames


def render_flash_swaps(
    *,
    try_ons: list[Path],
    output: Path,
    width: int,
    height: int,
    fps: int,
    timing: FlashSwapTiming,
    seed: int = 0,
    labels: list[str] | None = None,
    show_labels: bool = True,
) -> Path:
    """Try-on montage — styles: beat_cut, zoom_pulse, pingpong, staccato, shuffle_wipe."""
    if not try_ons:
        raise ValueError("render_flash_swaps requires at least one try-on still")
    rng = random.Random(seed)
    imgs = [load_canvas(path, width, height) for path in try_ons]
    chip_labels = labels or [f"Look {i + 1}" for i in range(len(imgs))]
    frames: list[Image.Image] = []
    style = timing.style or "shuffle_wipe"

    for cycle in range(max(1, timing.cycles)):
        order = _flash_order(len(imgs), shuffle=timing.shuffle, rng=rng, style=style, cycle=cycle)
        if style == "beat_cut":
            frames.extend(
                _render_flash_beat_cut(imgs, order, fps=fps, timing=timing, rng=rng, chip_labels=chip_labels)
            )
        elif style == "zoom_pulse":
            frames.extend(
                _render_flash_zoom_pulse(imgs, order, fps=fps, timing=timing, rng=rng, chip_labels=chip_labels)
            )
        elif style == "staccato":
            frames.extend(_render_flash_staccato(imgs, order, timing=timing, chip_labels=chip_labels))
        elif style in ("crossfade", "pingpong"):
            frames.extend(
                _render_flash_crossfade(
                    imgs, order, fps=fps, timing=timing, rng=rng, chip_labels=chip_labels, show_labels=show_labels
                )
            )
        else:
            frames.extend(
                _render_flash_shuffle_wipe(imgs, order, fps=fps, timing=timing, rng=rng, chip_labels=chip_labels)
            )

    encode_frames(frames, output, fps)
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.config.read_text(encoding="utf-8"))
    if data.get("pairs"):
        timing_raw = data.get("timing") or {}
        timing = Timing(
            garment_seconds=float(timing_raw.get("garment_seconds", 1.8)),
            person_seconds=float(timing_raw.get("person_seconds", 1.2)),
            compare_seconds=float(timing_raw.get("compare_seconds", 2.0)),
            slider_seconds=float(timing_raw.get("slider_seconds", 2.2)),
            hold_seconds=float(timing_raw.get("hold_seconds", 1.8)),
            flash_seconds=float(timing_raw.get("flash_seconds", 0.0)),
        )
        base = args.config.parent
        pairs = [
            (
                (base / item["garment"]).resolve() if not Path(item["garment"]).is_absolute() else Path(item["garment"]),
                (base / item["try_on"]).resolve() if not Path(item["try_on"]).is_absolute() else Path(item["try_on"]),
                str(item.get("label", "Garment ref")),
            )
            for item in data["pairs"]
        ]
        person = (base / data["person"]).resolve() if not Path(data["person"]).is_absolute() else Path(data["person"])
        output = (base / data["output"]).resolve() if not Path(data["output"]).is_absolute() else Path(data["output"])
        render_ladder(
            person=person,
            pairs=pairs,
            output=output,
            width=int(data.get("width", 1080)),
            height=int(data.get("height", 1920)),
            fps=int(data.get("fps", 24)),
            timing=timing,
            person_label=str(data.get("person_label", "Input · person photo")),
            before_label=str(data.get("before_label", "Before · base outfit")),
            after_label=str(data.get("after_label", "After · try-on")),
            compare_title=str(data.get("compare_title", "Same person · new outfit")),
        )
    else:
        render_showcase(job_from_dict(data, args.config.parent))
    print(data["output"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
