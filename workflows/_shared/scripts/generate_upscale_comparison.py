#!/usr/bin/env python3
"""Generate a before/after P-Image-Upscale demo video with zoom stops and sliders."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError as exc:  # pragma: no cover
    _req = Path(__file__).resolve().parent / "requirements-comparison.txt"
    raise SystemExit(
        f"Pillow is required. Install with: pip install -r {_req}"
    ) from exc


Image.MAX_IMAGE_PIXELS = 200_000_000


REGION_PRESETS: dict[str, list[dict[str, Any]]] = {
    "generic": [
        {"label": "Center detail", "x": 0.35, "y": 0.30, "w": 0.30, "h": 0.35},
        {"label": "Left detail", "x": 0.05, "y": 0.35, "w": 0.28, "h": 0.35},
        {"label": "Right detail", "x": 0.62, "y": 0.30, "w": 0.30, "h": 0.35},
    ],
    "portrait": [
        {"label": "Eyes and skin", "x": 0.36, "y": 0.12, "w": 0.24, "h": 0.32},
        {"label": "Hair and edges", "x": 0.52, "y": 0.05, "w": 0.30, "h": 0.28},
        {"label": "Clothing texture", "x": 0.28, "y": 0.52, "w": 0.44, "h": 0.32},
    ],
    "product": [
        {"label": "Logo or label", "x": 0.30, "y": 0.25, "w": 0.40, "h": 0.35},
        {"label": "Material edge", "x": 0.08, "y": 0.40, "w": 0.30, "h": 0.35},
        {"label": "Surface texture", "x": 0.55, "y": 0.45, "w": 0.35, "h": 0.35},
    ],
    "landscape": [
        {"label": "Foreground detail", "x": 0.10, "y": 0.45, "w": 0.35, "h": 0.35},
        {"label": "Mid-frame texture", "x": 0.35, "y": 0.25, "w": 0.30, "h": 0.35},
        {"label": "Horizon or sky", "x": 0.45, "y": 0.05, "w": 0.45, "h": 0.30},
    ],
}


@dataclass(frozen=True)
class Rect:
    x: float
    y: float
    w: float
    h: float

    def clamp(self) -> Rect:
        w = max(0.05, min(1.0, self.w))
        h = max(0.05, min(1.0, self.h))
        x = max(0.0, min(1.0 - w, self.x))
        y = max(0.0, min(1.0 - h, self.y))
        return Rect(x, y, w, h)

    def lerp(self, other: Rect, t: float) -> Rect:
        t = max(0.0, min(1.0, t))
        return Rect(
            self.x + (other.x - self.x) * t,
            self.y + (other.y - self.y) * t,
            self.w + (other.w - self.w) * t,
            self.h + (other.h - self.h) * t,
        ).clamp()


@dataclass(frozen=True)
class Timing:
    hook_seconds: float = 2.0
    outro_seconds: float = 2.0
    zoom_seconds: float = 0.8
    slider_seconds: float = 1.2
    hold_after_seconds: float = 0.5
    transition_seconds: float = 0.6


@dataclass(frozen=True)
class Region:
    label: str
    rect: Rect


@dataclass(frozen=True)
class JobConfig:
    before_path: Path
    after_path: Path
    output_path: Path
    regions: list[Region]
    timing: Timing
    fps: int
    width: int
    height: int
    title: str
    before_mp: float
    after_mp: float
    preset: str | None = None


def ease_in_out(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


def estimate_megapixels(path: Path) -> float:
    with Image.open(path) as image:
        width, height = image.size
    return round((width * height) / 1_000_000, 2)


def resolve_path(base_dirs: list[Path], value: str) -> Path:
    candidate = Path(value).expanduser()
    if candidate.is_absolute():
        return candidate.resolve()
    for base in base_dirs:
        resolved = (base / candidate).resolve()
        if resolved.exists():
            return resolved
    return (base_dirs[0] / candidate).resolve()


def parse_regions(raw_regions: list[dict[str, Any]]) -> list[Region]:
    regions: list[Region] = []
    for item in raw_regions:
        rect = Rect(
            float(item["x"]),
            float(item["y"]),
            float(item["w"]),
            float(item["h"]),
        ).clamp()
        regions.append(Region(label=str(item.get("label", "Detail")), rect=rect))
    return regions


PROGRESSIVE_WIDTHS = (0.70, 0.38, 0.20, 0.10, 0.05)
PROGRESSIVE_LABELS = (
    "Overview",
    "Zoom in",
    "Closer",
    "Deep detail",
    "Maximum detail",
)


def regions_from_focal_point(
    focal_x: float,
    focal_y: float,
    *,
    levels: int = 4,
    labels: list[str] | None = None,
) -> list[Region]:
    count = max(1, min(levels, len(PROGRESSIVE_WIDTHS)))
    label_list = labels or list(PROGRESSIVE_LABELS[:count])
    regions: list[Region] = []
    for index in range(count):
        width = PROGRESSIVE_WIDTHS[index]
        height = width * 0.75 if index < count - 1 else width
        rect = Rect(focal_x - width / 2, focal_y - height / 2, width, height).clamp()
        regions.append(Region(label=label_list[index], rect=rect))
    return regions


def regions_from_preset(preset: str) -> list[Region]:
    key = preset.lower()
    if key not in REGION_PRESETS:
        choices = ", ".join(sorted(REGION_PRESETS))
        raise ValueError(f"Unknown preset '{preset}'. Choose one of: {choices}")
    return parse_regions(REGION_PRESETS[key])


def parse_timing(raw: dict[str, Any] | None) -> Timing:
    if not raw:
        return Timing()
    return Timing(
        hook_seconds=float(raw.get("hook_seconds", 2.0)),
        outro_seconds=float(raw.get("outro_seconds", 2.0)),
        zoom_seconds=float(raw.get("zoom_seconds", 0.8)),
        slider_seconds=float(raw.get("slider_seconds", 1.2)),
        hold_after_seconds=float(raw.get("hold_after_seconds", 0.5)),
        transition_seconds=float(raw.get("transition_seconds", 0.6)),
    )


def load_config_file(config_path: Path) -> dict[str, Any]:
    with config_path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    return data


def build_job_config(
    *,
    before: str,
    after: str,
    output: str,
    base_dirs: list[Path],
    regions: list[Region] | None = None,
    preset: str | None = None,
    timing: Timing | None = None,
    fps: int = 24,
    width: int = 1920,
    height: int = 1080,
    title: str = "P-Image-Upscale",
    before_mp: float | None = None,
    after_mp: float | None = None,
) -> JobConfig:
    before_path = resolve_path(base_dirs, before)
    after_path = resolve_path(base_dirs, after)
    output_path = resolve_path(base_dirs, output)

    if not before_path.exists():
        raise FileNotFoundError(f"Before image not found: {before_path}")
    if not after_path.exists():
        raise FileNotFoundError(f"After image not found: {after_path}")

    if regions is None:
        preset_name = preset or "generic"
        regions = regions_from_preset(preset_name)
    elif not regions:
        raise ValueError("At least one region is required")

    return JobConfig(
        before_path=before_path,
        after_path=after_path,
        output_path=output_path,
        regions=regions,
        timing=timing or Timing(),
        fps=fps,
        width=width,
        height=height,
        title=title,
        before_mp=before_mp if before_mp is not None else estimate_megapixels(before_path),
        after_mp=after_mp if after_mp is not None else estimate_megapixels(after_path),
        preset=preset,
    )


def job_from_dict(data: dict[str, Any], base_dirs: list[Path]) -> JobConfig:
    required = ("before", "after", "output")
    missing = [key for key in required if key not in data]
    if missing:
        raise ValueError(f"Config missing required keys: {', '.join(missing)}")

    preset = data.get("preset")
    focal_point = data.get("focal_point")
    if "regions" in data and data["regions"]:
        regions = parse_regions(data["regions"])
    elif focal_point:
        regions = regions_from_focal_point(
            float(focal_point["x"]),
            float(focal_point["y"]),
            levels=int(focal_point.get("levels", 4)),
            labels=focal_point.get("labels"),
        )
    elif preset:
        regions = regions_from_preset(str(preset))
    else:
        regions = regions_from_preset("generic")

    before_mp = float(data["before_mp"]) if "before_mp" in data else None
    after_mp = float(data["after_mp"]) if "after_mp" in data else None

    return build_job_config(
        before=data["before"],
        after=data["after"],
        output=data["output"],
        base_dirs=base_dirs,
        regions=regions,
        preset=str(preset) if preset else None,
        timing=parse_timing(data.get("timing")),
        fps=int(data.get("fps", 24)),
        width=int(data.get("width", 1920)),
        height=int(data.get("height", 1080)),
        title=str(data.get("title", "P-Image-Upscale")),
        before_mp=before_mp,
        after_mp=after_mp,
    )


def job_to_dict(job: JobConfig) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "before": str(job.before_path),
        "after": str(job.after_path),
        "output": str(job.output_path),
        "title": job.title,
        "before_mp": job.before_mp,
        "after_mp": job.after_mp,
        "fps": job.fps,
        "width": job.width,
        "height": job.height,
        "timing": {
            "hook_seconds": job.timing.hook_seconds,
            "outro_seconds": job.timing.outro_seconds,
            "zoom_seconds": job.timing.zoom_seconds,
            "slider_seconds": job.timing.slider_seconds,
            "hold_after_seconds": job.timing.hold_after_seconds,
            "transition_seconds": job.timing.transition_seconds,
        },
        "regions": [
            {
                "label": region.label,
                "x": region.rect.x,
                "y": region.rect.y,
                "w": region.rect.w,
                "h": region.rect.h,
            }
            for region in job.regions
        ],
    }
    if job.preset:
        payload["preset"] = job.preset
    return payload


def crop_image(image: Image.Image, rect: Rect) -> Image.Image:
    width, height = image.size
    left = int(rect.x * width)
    top = int(rect.y * height)
    right = int((rect.x + rect.w) * width)
    bottom = int((rect.y + rect.h) * height)
    right = max(right, left + 1)
    bottom = max(bottom, top + 1)
    return image.crop((left, top, right, bottom))


def fill_canvas(image: Image.Image, canvas_w: int, canvas_h: int) -> Image.Image:
    """Scale to cover the canvas with no letterbox borders."""
    src_w, src_h = image.size
    scale = max(canvas_w / src_w, canvas_h / src_h)
    target_w = max(1, int(src_w * scale))
    target_h = max(1, int(src_h * scale))
    resized = image.resize((target_w, target_h), Image.Resampling.LANCZOS)
    left = max(0, (target_w - canvas_w) // 2)
    top = max(0, (target_h - canvas_h) // 2)
    return resized.crop((left, top, left + canvas_w, top + canvas_h))


def fit_canvas(image: Image.Image, canvas_w: int, canvas_h: int) -> Image.Image:
    return fill_canvas(image, canvas_w, canvas_h)


def compose_slider_frame(
    before_crop: Image.Image,
    after_crop: Image.Image,
    split_ratio: float,
    canvas_w: int,
    canvas_h: int,
    title: str,
    before_mp: float,
    after_mp: float,
    region_label: str,
    show_slider: bool,
) -> Image.Image:
    before_fit = fill_canvas(before_crop, canvas_w, canvas_h)
    after_fit = fill_canvas(after_crop, canvas_w, canvas_h)

    split_x = int(canvas_w * max(0.0, min(1.0, split_ratio)))
    split_x = max(1, min(canvas_w - 1, split_x))

    # Slider moves left -> right: the clearer "after" image is revealed from the left edge.
    viewport = Image.new("RGB", (canvas_w, canvas_h))
    viewport.paste(after_fit.crop((0, 0, split_x, canvas_h)), (0, 0))
    viewport.paste(before_fit.crop((split_x, 0, canvas_w, canvas_h)), (split_x, 0))

    draw = ImageDraw.Draw(viewport)
    font = ImageFont.load_default()

    if show_slider:
        draw.line((split_x, 0, split_x, canvas_h), fill=(255, 255, 255), width=2)
        draw.ellipse(
            (split_x - 8, canvas_h // 2 - 8, split_x + 8, canvas_h // 2 + 8),
            fill=(255, 255, 255),
            outline=(40, 40, 40),
        )

    # Floating labels on the image — no outer border or letterbox chrome.
    for text, x, y in (
        ("After", 12, 12),
        ("Before", canvas_w - 56, 12),
    ):
        draw.text((x, y), text, fill=(235, 235, 235), font=font)

    badge = f"{before_mp:g} MP -> {after_mp:g} MP"
    draw.text((canvas_w - 170, canvas_h - 22), badge, fill=(220, 220, 220), font=font)
    draw.text((12, canvas_h - 22), region_label, fill=(220, 220, 220), font=font)
    return viewport


def estimate_duration(timing: Timing, region_count: int) -> float:
    detail = region_count * (
        timing.zoom_seconds + timing.slider_seconds + timing.hold_after_seconds
    )
    transitions = max(0, region_count - 1) * timing.transition_seconds
    return timing.hook_seconds + detail + transitions + timing.outro_seconds


def iter_segments(
    regions: list[Region],
    timing: Timing,
) -> list[tuple[str, Rect | None, float, str | None]]:
    full = Rect(0.0, 0.0, 1.0, 1.0)
    segments: list[tuple[str, Rect | None, float, str | None]] = [
        ("hook", full, timing.hook_seconds, None),
    ]

    for index, region in enumerate(regions):
        if index > 0:
            segments.append(("transition", region.rect, timing.transition_seconds, None))
        segments.append(("zoom", region.rect, timing.zoom_seconds, None))
        segments.append(
            ("slider", region.rect, timing.slider_seconds + timing.hold_after_seconds, region.label)
        )

    segments.append(("outro", full, timing.outro_seconds, None))
    return segments


def render_video(job: JobConfig, *, keep_frames: bool = False) -> None:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg not found on PATH")

    after_image = Image.open(job.after_path).convert("RGB")
    before_image = Image.open(job.before_path).convert("RGB")
    if before_image.size != after_image.size:
        before_image = before_image.resize(after_image.size, Image.Resampling.LANCZOS)

    job.output_path.parent.mkdir(parents=True, exist_ok=True)
    frame_dir = job.output_path.parent / f".{job.output_path.stem}_frames"
    if frame_dir.exists():
        shutil.rmtree(frame_dir)
    frame_dir.mkdir(parents=True, exist_ok=True)

    full_rect = Rect(0.0, 0.0, 1.0, 1.0)
    frame_index = 0
    current_rect = full_rect

    for segment_type, target_rect, duration, region_label in iter_segments(job.regions, job.timing):
        frame_count = max(1, int(round(duration * job.fps)))
        for step in range(frame_count):
            progress = step / max(1, frame_count - 1) if frame_count > 1 else 1.0

            if segment_type == "hook":
                rect = full_rect
                split_ratio = 0.0
                show_slider = False
                label = "Full frame"
            elif segment_type == "outro":
                rect = full_rect
                split_ratio = 1.0
                show_slider = False
                label = "Full frame · after upscale"
            elif segment_type == "transition":
                assert target_rect is not None
                rect = current_rect.lerp(target_rect, ease_in_out(progress))
                split_ratio = 1.0
                show_slider = False
                label = "Transition"
            elif segment_type == "zoom":
                assert target_rect is not None
                rect = current_rect.lerp(target_rect, ease_in_out(progress))
                split_ratio = 0.0
                show_slider = False
                label = "Zoom"
            else:
                assert target_rect is not None
                rect = target_rect
                slider_span = job.timing.slider_seconds
                elapsed = progress * duration
                if elapsed <= slider_span:
                    split_ratio = ease_in_out(elapsed / slider_span)
                    show_slider = True
                else:
                    split_ratio = 1.0
                    show_slider = False
                label = region_label or "Detail"

            before_crop = crop_image(before_image, rect)
            after_crop = crop_image(after_image, rect)
            frame = compose_slider_frame(
                before_crop,
                after_crop,
                split_ratio,
                job.width,
                job.height,
                job.title,
                job.before_mp,
                job.after_mp,
                label,
                show_slider,
            )
            frame.save(frame_dir / f"frame_{frame_index:05d}.png")
            frame_index += 1

            if segment_type in {"transition", "zoom", "slider"} and step == frame_count - 1:
                current_rect = rect

    pattern = str(frame_dir / "frame_%05d.png")
    cmd = [
        ffmpeg,
        "-y",
        "-framerate",
        str(job.fps),
        "-i",
        pattern,
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
        str(job.output_path),
    ]
    subprocess.run(cmd, check=True)

    if not keep_frames:
        shutil.rmtree(frame_dir)


def print_job_summary(job: JobConfig) -> None:
    duration = estimate_duration(job.timing, len(job.regions))
    print(f"Preset: {job.preset or '(custom regions)'}")
    print(f"Regions: {len(job.regions)}")
    for index, region in enumerate(job.regions, start=1):
        rect = region.rect
        print(
            f"  {index}. {region.label} "
            f"(x={rect.x:.2f}, y={rect.y:.2f}, w={rect.w:.2f}, h={rect.h:.2f})"
        )
    print(f"Estimated duration: {duration:.1f}s at {job.fps} fps")
    print(f"Before: {job.before_path} ({job.before_mp:g} MP)")
    print(f"After:  {job.after_path} ({job.after_mp:g} MP)")
    print(f"Output: {job.output_path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, help="JSON config path")
    parser.add_argument("--before", type=str, help="Pre-upscale still path")
    parser.add_argument("--after", type=str, help="Upscaled still path")
    parser.add_argument("--output", type=str, help="Output MP4 path")
    parser.add_argument(
        "--preset",
        choices=sorted(REGION_PRESETS),
        default="generic",
        help="Default zoom-stop layout when regions are not custom-defined",
    )
    parser.add_argument("--title", default="P-Image-Upscale", help="Top-bar title")
    parser.add_argument("--fps", type=int, default=24)
    parser.add_argument("--width", type=int, default=1920)
    parser.add_argument("--height", type=int, default=1080)
    parser.add_argument(
        "--write-config",
        type=Path,
        help="Write the resolved job config JSON and exit (unless rendering)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate inputs and print the render plan only",
    )
    parser.add_argument(
        "--keep-frames",
        action="store_true",
        help="Keep intermediate PNG frames next to the output video",
    )
    parser.add_argument(
        "--list-presets",
        action="store_true",
        help="Print available region presets and exit",
    )
    return parser


def resolve_job(args: argparse.Namespace) -> JobConfig:
    if args.config:
        config_path = args.config.resolve()
        data = load_config_file(config_path)
        base_dirs = [config_path.parent, Path.cwd()]
        return job_from_dict(data, base_dirs)

    missing = [name for name in ("before", "after", "output") if not getattr(args, name)]
    if missing:
        raise SystemExit(
            "Provide --config or all of --before, --after, and --output. "
            "Use --list-presets to see region presets."
        )

    return build_job_config(
        before=args.before,
        after=args.after,
        output=args.output,
        base_dirs=[Path.cwd()],
        preset=args.preset,
        timing=Timing(),
        fps=args.fps,
        width=args.width,
        height=args.height,
        title=args.title,
    )


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list_presets:
        for name, regions in REGION_PRESETS.items():
            labels = ", ".join(region["label"] for region in regions)
            print(f"{name}: {labels}")
        return 0

    job = resolve_job(args)
    print_job_summary(job)

    if args.write_config:
        args.write_config.parent.mkdir(parents=True, exist_ok=True)
        with args.write_config.open("w", encoding="utf-8") as handle:
            json.dump(job_to_dict(job), handle, indent=2)
            handle.write("\n")
        print(f"Wrote config {args.write_config}")

    if args.dry_run:
        return 0

    render_video(job, keep_frames=args.keep_frames)
    print(f"Wrote {job.output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
