#!/usr/bin/env python3
"""Generate a synced before/after P-Video-Animate demo with a left-to-right slider."""

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


@dataclass(frozen=True)
class Timing:
    hook_seconds: float = 0.0
    slider_seconds: float = 2.5
    hold_output_seconds: float = 0.0
    outro_seconds: float = 0.0
    transition_seconds: float = 0.4


@dataclass(frozen=True)
class ReferenceImageSpec:
    path: Path
    label: str


@dataclass(frozen=True)
class SampleSpec:
    output_path: Path
    output_label: str
    beat_label: str


@dataclass(frozen=True)
class SliderSideLabels:
    enabled: bool = False
    original: str = "Original video"
    replaced: str = "Replaced video"


@dataclass(frozen=True)
class JobConfig:
    source_path: Path
    render_path: Path
    timing: Timing
    fps: int
    width: int
    height: int
    title: str
    source_label: str
    include_audio: bool = True
    full_bleed: bool = True
    compare_mode: str = "single_pass_multi_slider"
    output_path: Path | None = None
    output_label: str = "Animated subject"
    samples: tuple[SampleSpec, ...] = ()
    reference_panel: tuple[ReferenceImageSpec, ...] = ()
    slider_side_labels: SliderSideLabels = SliderSideLabels()


def ease_in_out(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


def resolve_path(base_dirs: list[Path], value: str) -> Path:
    candidate = Path(value).expanduser()
    if candidate.is_absolute():
        return candidate.resolve()
    for base in base_dirs:
        resolved = (base / candidate).resolve()
        if resolved.exists():
            return resolved
    return (base_dirs[0] / candidate).resolve()


def require_tool(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise RuntimeError(f"{name} not found on PATH")
    return path


def probe_video(path: Path) -> dict[str, float]:
    ffprobe = require_tool("ffprobe")
    cmd = [
        ffprobe,
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=width,height,r_frame_rate,duration",
        "-show_entries",
        "format=duration",
        "-of",
        "json",
        str(path),
    ]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    payload = json.loads(result.stdout)
    stream = payload["streams"][0]
    width = float(stream["width"])
    height = float(stream["height"])
    rate = stream.get("r_frame_rate", "24/1")
    num, den = rate.split("/")
    fps = float(num) / float(den or 1)
    duration = float(stream.get("duration") or payload["format"].get("duration") or 0.0)
    return {"width": width, "height": height, "fps": fps, "duration": duration}


def extract_frames(
    *,
    video_path: Path,
    frame_dir: Path,
    fps: int,
    width: int,
    height: int,
    max_frames: int | None = None,
) -> list[Path]:
    ffmpeg = require_tool("ffmpeg")
    frame_dir.mkdir(parents=True, exist_ok=True)
    pattern = frame_dir / "frame_%05d.png"
    cmd = [
        ffmpeg,
        "-y",
        "-i",
        str(video_path),
        "-vf",
        f"fps={fps},scale={width}:{height}:force_original_aspect_ratio=increase,"
        f"crop={width}:{height}",
        "-frames:v",
        str(max_frames) if max_frames else "999999",
        str(pattern),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    frames = sorted(frame_dir.glob("frame_*.png"))
    if max_frames is not None:
        frames = frames[:max_frames]
    if not frames:
        raise RuntimeError(f"No frames extracted from {video_path}")
    return frames


def fit_frame(frame: Image.Image, canvas_w: int, canvas_h: int) -> Image.Image:
    if frame.size == (canvas_w, canvas_h):
        return frame
    return fit_canvas(frame, canvas_w, canvas_h)


def paste_reference_panel(
    viewport: Image.Image,
    references: list[tuple[Image.Image, str]],
    *,
    canvas_w: int,
    canvas_h: int,
    margin: int = 12,
    show_labels: bool = False,
) -> None:
    """Draw reference stills as small bordered thumbnails at the top-right (no panel chrome)."""
    if not references:
        return
    n = len(references)
    gap = 5
    border = 1
    inset = 2
    thumb_size = max(48, min(72, int(min(canvas_w, canvas_h) * 0.065)))
    row_w = n * thumb_size + (n - 1) * gap
    ox = canvas_w - margin - row_w
    oy = margin
    draw = ImageDraw.Draw(viewport)
    inner = max(8, thumb_size - 2 * (border + inset))
    for index, (image, _label) in enumerate(references):
        cell_x = ox + index * (thumb_size + gap)
        cell_y = oy
        thumb = image.copy()
        thumb.thumbnail((inner, inner), Image.Resampling.LANCZOS)
        tx = cell_x + (thumb_size - thumb.width) // 2
        ty = cell_y + (thumb_size - thumb.height) // 2
        viewport.paste(thumb, (tx, ty))
        box = (cell_x, cell_y, cell_x + thumb_size - 1, cell_y + thumb_size - 1)
        draw.rectangle(box, outline=(255, 255, 255), width=border)
        if show_labels:
            font = ImageFont.load_default()
            short = _label if len(_label) <= 14 else f"{_label[:12]}…"
            draw.text((cell_x + 2, cell_y + thumb_size + 2), short, fill=(220, 220, 220), font=font)


def fit_canvas(image: Image.Image, canvas_w: int, canvas_h: int) -> Image.Image:
    canvas = Image.new("RGB", (canvas_w, canvas_h), (26, 26, 26))
    src_w, src_h = image.size
    scale = min(canvas_w / src_w, canvas_h / src_h)
    target_w = max(1, int(src_w * scale))
    target_h = max(1, int(src_h * scale))
    resized = image.resize((target_w, target_h), Image.Resampling.LANCZOS)
    offset_x = (canvas_w - target_w) // 2
    offset_y = (canvas_h - target_h) // 2
    canvas.paste(resized, (offset_x, offset_y))
    return canvas


def load_side_label_font(size: int = 22) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
    ):
        try:
            return ImageFont.truetype(path, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def draw_slider_side_labels(
    viewport: Image.Image,
    *,
    offset_x: int,
    offset_y: int,
    compare_w: int,
    compare_h: int,
    split_ratio: float,
    labels: SliderSideLabels,
) -> None:
    """Fade side captions with the wipe: replaced on the left, original on the right."""
    replaced_alpha = ease_in_out(split_ratio)
    original_alpha = ease_in_out(1.0 - split_ratio)
    margin = 22
    font = load_side_label_font()
    draw = ImageDraw.Draw(viewport)
    y_base = offset_y + compare_h - margin

    def stamp(text: str, x: int, anchor: str, alpha: float) -> None:
        if alpha < 0.06:
            return
        fg = int(255 * alpha)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_h = bbox[3] - bbox[1]
        y = y_base - text_h
        if anchor == "right":
            x_pos = x - (bbox[2] - bbox[0])
        else:
            x_pos = x
        draw.text(
            (x_pos, y),
            text,
            fill=(fg, fg, fg),
            font=font,
            stroke_width=2,
            stroke_fill=(0, 0, 0),
        )

    stamp(
        labels.replaced,
        offset_x + margin,
        "left",
        replaced_alpha,
    )
    stamp(
        labels.original,
        offset_x + compare_w - margin,
        "right",
        original_alpha,
    )


def compose_slider_frame(
    source_frame: Image.Image,
    output_frame: Image.Image,
    split_ratio: float,
    canvas_w: int,
    canvas_h: int,
    title: str,
    source_label: str,
    output_label: str,
    beat_label: str,
    show_slider: bool,
    *,
    full_bleed: bool = True,
    before_frame: Image.Image | None = None,
    reference_panel: list[tuple[Image.Image, str]] | None = None,
    slider_side_labels: SliderSideLabels | None = None,
) -> Image.Image:
    if full_bleed:
        compare_w = canvas_w
        compare_h = canvas_h
        offset_x = 0
        offset_y = 0
        viewport = Image.new("RGB", (canvas_w, canvas_h), (0, 0, 0))
    else:
        compare_w = canvas_w - 96
        compare_h = canvas_h - 72
        offset_x = 48
        offset_y = 56
        viewport = Image.new("RGB", (canvas_w, canvas_h), (26, 26, 26))

    before = before_frame if before_frame is not None else source_frame
    before_fit = fit_frame(before, compare_w, compare_h)
    output_fit = fit_frame(output_frame, compare_w, compare_h)

    split_x = int(compare_w * max(0.0, min(1.0, split_ratio)))
    split_x = max(0, min(compare_w, split_x))

    compare = Image.new("RGB", (compare_w, compare_h), (0, 0, 0))
    compare.paste(output_fit.crop((0, 0, split_x, compare_h)), (0, 0))
    compare.paste(before_fit.crop((split_x, 0, compare_w, compare_h)), (split_x, 0))
    viewport.paste(compare, (offset_x, offset_y))

    if not full_bleed:
        draw = ImageDraw.Draw(viewport)
        font = ImageFont.load_default()
        draw.rectangle((0, 0, canvas_w, 40), fill=(18, 18, 18))
        draw.text((16, 12), title, fill=(240, 240, 240), font=font)
        draw.text((canvas_w - 250, 12), beat_label, fill=(180, 180, 180), font=font)
        draw.text((offset_x, compare_h + offset_y + 8), f"{source_label} -> {output_label}", fill=(200, 200, 200), font=font)
        draw.text((offset_x + 8, offset_y + 8), output_label, fill=(220, 220, 220), font=font)
        draw.text((offset_x + compare_w - 120, offset_y + 8), source_label, fill=(220, 220, 220), font=font)

    if show_slider:
        draw = ImageDraw.Draw(viewport)
        line_x = offset_x + split_x
        draw.line((line_x, offset_y, line_x, offset_y + compare_h), fill=(255, 255, 255), width=2)
        draw.ellipse(
            (line_x - 8, offset_y + compare_h // 2 - 8, line_x + 8, offset_y + compare_h // 2 + 8),
            fill=(255, 255, 255),
            outline=(40, 40, 40),
        )

    if reference_panel:
        paste_reference_panel(
            viewport,
            reference_panel,
            canvas_w=canvas_w,
            canvas_h=canvas_h,
        )

    side_labels = slider_side_labels or SliderSideLabels()
    if full_bleed and side_labels.enabled and before_frame is None:
        draw_slider_side_labels(
            viewport,
            offset_x=offset_x,
            offset_y=offset_y,
            compare_w=compare_w,
            compare_h=compare_h,
            split_ratio=split_ratio,
            labels=side_labels,
        )

    return viewport


def parse_timing(raw: dict[str, Any] | None) -> Timing:
    if not raw:
        return Timing()
    return Timing(
        hook_seconds=float(raw.get("hook_seconds", 0.0)),
        slider_seconds=float(raw.get("slider_seconds", 2.5)),
        hold_output_seconds=float(raw.get("hold_output_seconds", 0.0)),
        outro_seconds=float(raw.get("outro_seconds", 0.0)),
        transition_seconds=float(raw.get("transition_seconds", 0.4)),
    )


def parse_samples(data: dict[str, Any], base_dirs: list[Path]) -> tuple[SampleSpec, ...]:
    raw_samples = data.get("samples")
    if not raw_samples:
        if "output" not in data:
            raise ValueError("Config requires 'output' or non-empty 'samples'")
        return (
            SampleSpec(
                output_path=resolve_path(base_dirs, data["output"]),
                output_label=str(data.get("output_label", "Animated subject")),
                beat_label=str(data.get("beat_label", "Variation 1")),
            ),
        )
    samples: list[SampleSpec] = []
    for index, sample in enumerate(raw_samples, start=1):
        if "output" not in sample:
            raise ValueError(f"Sample {index} missing 'output'")
        samples.append(
            SampleSpec(
                output_path=resolve_path(base_dirs, sample["output"]),
                output_label=str(sample.get("output_label", f"Subject {index}")),
                beat_label=str(sample.get("beat_label", f"Variation {index}")),
            )
        )
    return tuple(samples)


def parse_reference_panel(
    data: dict[str, Any], base_dirs: list[Path]
) -> tuple[ReferenceImageSpec, ...]:
    raw = data.get("reference_images")
    if not raw:
        return ()
    specs: list[ReferenceImageSpec] = []
    for index, entry in enumerate(raw, start=1):
        ref_raw = entry.get("reference")
        if not ref_raw:
            raise ValueError(f"reference_images[{index}] missing 'reference' path")
        path = resolve_path(base_dirs, ref_raw)
        if not path.exists():
            raise FileNotFoundError(f"Reference image not found: {path}")
        specs.append(
            ReferenceImageSpec(
                path=path,
                label=str(entry.get("label", f"Ref {index}")),
            )
        )
    return tuple(specs)


def parse_slider_side_labels(data: dict[str, Any]) -> SliderSideLabels:
    raw = data.get("slider_side_labels")
    if raw is False:
        return SliderSideLabels(enabled=False)
    if raw is None:
        return SliderSideLabels(enabled=False)
    if not isinstance(raw, dict):
        return SliderSideLabels()
    return SliderSideLabels(
        enabled=bool(raw.get("enabled", True)),
        original=str(raw.get("original", "Original video")),
        replaced=str(raw.get("replaced", "Replaced video")),
    )


def build_job_config(
    *,
    source: str,
    render: str,
    base_dirs: list[Path],
    output: str | None = None,
    samples: list[dict[str, Any]] | None = None,
    timing: Timing | None = None,
    fps: int = 24,
    width: int = 1920,
    height: int = 1080,
    title: str = "P-Video-Animate",
    source_label: str = "Motion template",
    output_label: str = "Animated subject",
    include_audio: bool = True,
    full_bleed: bool = True,
) -> JobConfig:
    payload: dict[str, Any] = {
        "source": source,
        "render": render,
        "title": title,
        "source_label": source_label,
        "output_label": output_label,
        "include_audio": include_audio,
        "full_bleed": full_bleed,
    }
    if samples:
        payload["samples"] = samples
    elif output:
        payload["output"] = output
    else:
        raise ValueError("Provide output or samples")
    return job_from_dict(payload, base_dirs)


def job_from_dict(data: dict[str, Any], base_dirs: list[Path]) -> JobConfig:
    required = ("source", "render")
    missing = [key for key in required if key not in data]
    if missing:
        raise ValueError(f"Config missing required keys: {', '.join(missing)}")
    source_path = resolve_path(base_dirs, data["source"])
    render_path = resolve_path(base_dirs, data["render"])
    if not source_path.exists():
        raise FileNotFoundError(f"Source video not found: {source_path}")
    sample_specs = parse_samples(data, base_dirs)
    for sample in sample_specs:
        if not sample.output_path.exists():
            raise FileNotFoundError(f"Output video not found: {sample.output_path}")
    timing = parse_timing(data.get("timing"))
    if "transition_seconds" in data:
        timing = Timing(
            hook_seconds=timing.hook_seconds,
            slider_seconds=timing.slider_seconds,
            hold_output_seconds=timing.hold_output_seconds,
            outro_seconds=timing.outro_seconds,
            transition_seconds=float(data["transition_seconds"]),
        )
    first = sample_specs[0]
    compare_mode = str(data.get("compare_mode", "single_pass_multi_slider"))
    if len(sample_specs) == 1:
        compare_mode = str(data.get("compare_mode", "single"))
    return JobConfig(
        source_path=source_path,
        render_path=render_path,
        timing=timing,
        fps=int(data.get("fps", 24)),
        width=int(data.get("width", 1920)),
        height=int(data.get("height", 1080)),
        title=str(data.get("title", "P-Video-Animate")),
        source_label=str(data.get("source_label", "Motion template")),
        include_audio=bool(data.get("include_audio", True)),
        full_bleed=bool(data.get("full_bleed", True)),
        compare_mode=compare_mode,
        output_path=first.output_path,
        output_label=first.output_label,
        samples=sample_specs,
        reference_panel=parse_reference_panel(data, base_dirs),
        slider_side_labels=parse_slider_side_labels(data),
    )


def job_to_dict(job: JobConfig) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "source": str(job.source_path),
        "render": str(job.render_path),
        "title": job.title,
        "source_label": job.source_label,
        "include_audio": job.include_audio,
        "full_bleed": job.full_bleed,
        "fps": job.fps,
        "width": job.width,
        "height": job.height,
        "timing": {
            "hook_seconds": job.timing.hook_seconds,
            "slider_seconds": job.timing.slider_seconds,
            "hold_output_seconds": job.timing.hold_output_seconds,
            "outro_seconds": job.timing.outro_seconds,
            "transition_seconds": job.timing.transition_seconds,
        },
    }
    if len(job.samples) == 1 and job.output_path is not None:
        payload["output"] = str(job.output_path)
        payload["output_label"] = job.output_label
    else:
        payload["samples"] = [
            {
                "output": str(sample.output_path),
                "output_label": sample.output_label,
                "beat_label": sample.beat_label,
            }
            for sample in job.samples
        ]
    if job.reference_panel:
        payload["reference_images"] = [
            {"reference": str(spec.path), "label": spec.label}
            for spec in job.reference_panel
        ]
    if not job.slider_side_labels.enabled or (
        job.slider_side_labels.original != "Original video"
        or job.slider_side_labels.replaced != "Replaced video"
    ):
        payload["slider_side_labels"] = {
            "enabled": job.slider_side_labels.enabled,
            "original": job.slider_side_labels.original,
            "replaced": job.slider_side_labels.replaced,
        }
    return payload


def estimate_duration(job: JobConfig) -> float:
    source = probe_video(job.source_path)
    if job.compare_mode == "single_pass_multi_slider" and len(job.samples) > 1:
        return source["duration"] + job.timing.hook_seconds + job.timing.outro_seconds
    total = job.timing.hook_seconds + job.timing.outro_seconds
    transitions = max(0, len(job.samples) - 1) * job.timing.transition_seconds
    for sample in job.samples:
        output = probe_video(sample.output_path)
        play_seconds = min(source["duration"], output["duration"])
        total += play_seconds + job.timing.hold_output_seconds
    return total + transitions


def pick_frame(frames: list[Path], index: int) -> Image.Image:
    return Image.open(frames[min(index, len(frames) - 1)]).convert("RGB")


def load_reference_panel_images(
    job: JobConfig,
) -> list[tuple[Image.Image, str]]:
    panel: list[tuple[Image.Image, str]] = []
    for spec in job.reference_panel:
        if spec.path.exists():
            panel.append((Image.open(spec.path).convert("RGB"), spec.label))
    return panel


def append_play_segment(
    *,
    job: JobConfig,
    source_frames: list[Path],
    output_frames: list[Path],
    play_frames: int,
    hook_frames: int,
    hold_frames: int,
    outro_frames: int,
    slider_frames: int,
    frame_dir: Path,
    frame_index: int,
    output_label: str,
    beat_prefix: str,
    reference_panel: list[tuple[Image.Image, str]] | None = None,
) -> int:
    compose_kwargs = {
        "full_bleed": job.full_bleed,
        "reference_panel": reference_panel,
        "slider_side_labels": job.slider_side_labels,
    }

    for step in range(hook_frames):
        frame = compose_slider_frame(
            pick_frame(source_frames, step),
            pick_frame(output_frames, 0),
            split_ratio=0.0,
            canvas_w=job.width,
            canvas_h=job.height,
            title=job.title,
            source_label=job.source_label,
            output_label=output_label,
            beat_label=f"{beat_prefix} · motion template",
            show_slider=False,
            **compose_kwargs,
        )
        frame.save(frame_dir / f"frame_{frame_index:05d}.png")
        frame_index += 1

    for step in range(play_frames):
        if step < slider_frames:
            split_ratio = ease_in_out(step / max(1, slider_frames - 1))
            show_slider = True
            beat = f"{beat_prefix} · slider"
        else:
            split_ratio = 1.0
            show_slider = False
            beat = f"{beat_prefix} · animated"
        frame = compose_slider_frame(
            pick_frame(source_frames, hook_frames + step),
            pick_frame(output_frames, step),
            split_ratio=split_ratio,
            canvas_w=job.width,
            canvas_h=job.height,
            title=job.title,
            source_label=job.source_label,
            output_label=output_label,
            beat_label=beat,
            show_slider=show_slider,
            **compose_kwargs,
        )
        frame.save(frame_dir / f"frame_{frame_index:05d}.png")
        frame_index += 1

    hold_start = max(0, len(output_frames) - hold_frames - outro_frames)
    for step in range(hold_frames):
        frame = compose_slider_frame(
            pick_frame(source_frames, min(hook_frames + play_frames - 1, len(source_frames) - 1)),
            pick_frame(output_frames, hold_start + step),
            split_ratio=1.0,
            canvas_w=job.width,
            canvas_h=job.height,
            title=job.title,
            source_label=job.source_label,
            output_label=output_label,
            beat_label=f"{beat_prefix} · hold",
            show_slider=False,
            **compose_kwargs,
        )
        frame.save(frame_dir / f"frame_{frame_index:05d}.png")
        frame_index += 1

    outro_start = max(0, len(output_frames) - outro_frames)
    for step in range(outro_frames):
        frame = compose_slider_frame(
            pick_frame(source_frames, min(hook_frames + play_frames - 1, len(source_frames) - 1)),
            pick_frame(output_frames, outro_start + step),
            split_ratio=1.0,
            canvas_w=job.width,
            canvas_h=job.height,
            title=job.title,
            source_label=job.source_label,
            output_label=output_label,
            beat_label=f"{beat_prefix} · outro",
            show_slider=False,
            **compose_kwargs,
        )
        frame.save(frame_dir / f"frame_{frame_index:05d}.png")
        frame_index += 1

    return frame_index


def render_single_pass_multi_slider(
    job: JobConfig,
    *,
    source_info: dict[str, float],
    compare_w: int,
    compare_h: int,
    temp_root: Path,
    frame_dir: Path,
    hook_frames: int,
    outro_frames: int,
    slider_frames: int,
) -> int:
    """One motion-template timeline, split into N segments with a slider reveal each."""
    sample_count = len(job.samples)
    total_frames = max(1, int(round(source_info["duration"] * job.fps)))
    play_frames = max(sample_count, total_frames - hook_frames - outro_frames)
    base_segment = play_frames // sample_count
    remainder = play_frames % sample_count
    compose_kwargs_base = {
        "full_bleed": job.full_bleed,
        "reference_panel": load_reference_panel_images(job) or None,
        "slider_side_labels": job.slider_side_labels,
    }

    source_dir = temp_root / "source"
    source_frames = extract_frames(
        video_path=job.source_path,
        frame_dir=source_dir,
        fps=job.fps,
        width=compare_w,
        height=compare_h,
        max_frames=hook_frames + play_frames + outro_frames,
    )

    # Extract each animated output across the full play timeline so frame indices
    # stay locked to the motion template (variation N at source frame T uses output T).
    output_frame_sets: list[list[Path]] = []
    for sample_index, sample in enumerate(job.samples):
        output_dir = temp_root / f"output_{sample_index + 1:02d}"
        output_frame_sets.append(
            extract_frames(
                video_path=sample.output_path,
                frame_dir=output_dir,
                fps=job.fps,
                width=compare_w,
                height=compare_h,
                max_frames=hook_frames + play_frames + outro_frames,
            )
        )

    frame_index = 0
    source_cursor = 0

    for hook_step in range(hook_frames):
        compose_kwargs = compose_kwargs_base
        frame = compose_slider_frame(
            pick_frame(source_frames, hook_step),
            pick_frame(output_frame_sets[0], hook_step),
            split_ratio=0.0,
            canvas_w=job.width,
            canvas_h=job.height,
            title=job.title,
            source_label=job.source_label,
            output_label=job.samples[0].output_label,
            beat_label=f"{job.samples[0].beat_label} · motion template",
            show_slider=False,
            **compose_kwargs,
        )
        frame.save(frame_dir / f"frame_{frame_index:05d}.png")
        frame_index += 1
        source_cursor = hook_step + 1

    for sample_index, sample in enumerate(job.samples):
        segment_frames = base_segment + (1 if sample_index < remainder else 0)
        segment_frames = max(1, segment_frames)
        segment_slider = min(slider_frames, segment_frames)
        output_frames = output_frame_sets[sample_index]

        prev_output_frames = output_frame_sets[sample_index - 1] if sample_index > 0 else None

        for step in range(segment_frames):
            timeline_idx = source_cursor + step
            source_idx = min(timeline_idx, len(source_frames) - 1)
            output_idx = min(timeline_idx, len(output_frames) - 1)
            if step < segment_slider:
                split_ratio = ease_in_out(step / max(1, segment_slider - 1))
                show_slider = True
                beat = f"{sample.beat_label} · slider"
            else:
                split_ratio = 1.0
                show_slider = False
                beat = f"{sample.beat_label} · animated"
            # Only the first variation wipes against the motion template; later beats
            # wipe from the previous variation so the original does not reappear.
            before = None
            if sample_index > 0 and prev_output_frames is not None:
                before = pick_frame(prev_output_frames, output_idx)
            frame = compose_slider_frame(
                pick_frame(source_frames, source_idx),
                pick_frame(output_frames, output_idx),
                split_ratio=split_ratio,
                canvas_w=job.width,
                canvas_h=job.height,
                title=job.title,
                source_label=job.source_label,
                output_label=sample.output_label,
                beat_label=beat,
                show_slider=show_slider,
                before_frame=before,
                **compose_kwargs_base,
            )
            frame.save(frame_dir / f"frame_{frame_index:05d}.png")
            frame_index += 1

        source_cursor += segment_frames

    outro_start = max(0, len(source_frames) - outro_frames)
    last_sample = job.samples[-1]
    last_output_frames = output_frame_sets[-1]
    for step in range(outro_frames):
        timeline_idx = outro_start + step
        frame = compose_slider_frame(
            pick_frame(source_frames, timeline_idx),
            pick_frame(last_output_frames, timeline_idx),
            split_ratio=1.0,
            canvas_w=job.width,
            canvas_h=job.height,
            title=job.title,
            source_label=job.source_label,
            output_label=last_sample.output_label,
            beat_label=f"{last_sample.beat_label} · outro",
            show_slider=False,
            **compose_kwargs_base,
        )
        frame.save(frame_dir / f"frame_{frame_index:05d}.png")
        frame_index += 1

    return frame_index


def mux_source_audio(
    *,
    silent_path: Path,
    render_path: Path,
    source_path: Path,
    total_seconds: float,
    source_duration: float,
) -> None:
    ffmpeg = require_tool("ffmpeg")
    audio_end = min(total_seconds, source_duration)
    mux_cmd = [
        ffmpeg,
        "-y",
        "-i",
        str(silent_path),
        "-i",
        str(source_path),
        "-filter_complex",
        (
            f"[1:a]atrim=0:{audio_end:.3f},asetpts=PTS-STARTPTS,"
            f"apad=whole_dur={total_seconds:.3f}[aout]"
        ),
        "-map",
        "0:v:0",
        "-map",
        "[aout]",
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-t",
        f"{total_seconds:.3f}",
        str(render_path),
    ]
    result = subprocess.run(mux_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Audio mux failed: {result.stderr}", file=sys.stderr)
        shutil.copy2(silent_path, render_path)
    else:
        silent_path.unlink(missing_ok=True)


def append_transition_segment(
    *,
    job: JobConfig,
    source_frames: list[Path],
    output_frames: list[Path],
    transition_frames: int,
    frame_dir: Path,
    frame_index: int,
) -> int:
    compose_kwargs = {
        "full_bleed": job.full_bleed,
        "reference_panel": load_reference_panel_images(job) or None,
        "slider_side_labels": job.slider_side_labels,
    }
    for _ in range(transition_frames):
        frame = compose_slider_frame(
            pick_frame(source_frames, 0),
            pick_frame(output_frames, 0),
            split_ratio=0.0,
            canvas_w=job.width,
            canvas_h=job.height,
            title=job.title,
            source_label=job.source_label,
            output_label=job.output_label,
            beat_label="Next variation",
            show_slider=False,
            **compose_kwargs,
        )
        frame.save(frame_dir / f"frame_{frame_index:05d}.png")
        frame_index += 1
    return frame_index


def render_video(job: JobConfig, *, keep_frames: bool = False) -> None:
    ffmpeg = require_tool("ffmpeg")
    source_info = probe_video(job.source_path)
    compare_w = job.width if job.full_bleed else job.width - 96
    compare_h = job.height if job.full_bleed else job.height - 72
    temp_root = job.render_path.parent / f".{job.render_path.stem}_work"
    frame_dir = temp_root / "render"
    if temp_root.exists():
        shutil.rmtree(temp_root)
    temp_root.mkdir(parents=True, exist_ok=True)
    frame_dir.mkdir(parents=True, exist_ok=True)

    hook_frames = max(0, int(round(job.timing.hook_seconds * job.fps)))
    hold_frames = max(0, int(round(job.timing.hold_output_seconds * job.fps)))
    outro_frames = max(0, int(round(job.timing.outro_seconds * job.fps)))
    slider_frames = max(1, int(round(job.timing.slider_seconds * job.fps)))
    transition_frames = max(0, int(round(job.timing.transition_seconds * job.fps)))

    reference_panel = load_reference_panel_images(job) or None
    panel_kwargs = {"reference_panel": reference_panel}

    frame_index = 0
    if job.compare_mode == "single_pass_multi_slider" and len(job.samples) > 1:
        frame_index = render_single_pass_multi_slider(
            job,
            source_info=source_info,
            compare_w=compare_w,
            compare_h=compare_h,
            temp_root=temp_root,
            frame_dir=frame_dir,
            hook_frames=hook_frames,
            outro_frames=outro_frames,
            slider_frames=slider_frames,
        )
    else:
        max_play_frames = 1
        for sample in job.samples:
            output_info = probe_video(sample.output_path)
            play_seconds = min(source_info["duration"], output_info["duration"])
            max_play_frames = max(max_play_frames, int(round(play_seconds * job.fps)))

        source_dir = temp_root / "source"
        source_frames = extract_frames(
            video_path=job.source_path,
            frame_dir=source_dir,
            fps=job.fps,
            width=compare_w,
            height=compare_h,
            max_frames=hook_frames + max_play_frames + outro_frames,
        )

        for sample_index, sample in enumerate(job.samples):
            output_info = probe_video(sample.output_path)
            play_seconds = min(source_info["duration"], output_info["duration"])
            play_frames = max(1, int(round(play_seconds * job.fps)))
            output_dir = temp_root / f"output_{sample_index + 1:02d}"
            output_frames = extract_frames(
                video_path=sample.output_path,
                frame_dir=output_dir,
                fps=job.fps,
                width=compare_w,
                height=compare_h,
                max_frames=play_frames + hold_frames + outro_frames,
            )
            use_hook = hook_frames if sample_index == 0 else 0
            frame_index = append_play_segment(
                job=job,
                source_frames=source_frames,
                output_frames=output_frames,
                play_frames=play_frames,
                hook_frames=use_hook,
                hold_frames=hold_frames,
                outro_frames=outro_frames,
                slider_frames=slider_frames,
                frame_dir=frame_dir,
                frame_index=frame_index,
                output_label=sample.output_label,
                beat_prefix=sample.beat_label,
                reference_panel=reference_panel,
            )
            if sample_index < len(job.samples) - 1 and transition_frames > 0:
                frame_index = append_transition_segment(
                    job=job,
                    source_frames=source_frames,
                    output_frames=output_frames,
                    transition_frames=transition_frames,
                    frame_dir=frame_dir,
                    frame_index=frame_index,
                )

    job.render_path.parent.mkdir(parents=True, exist_ok=True)
    silent_path = job.render_path.with_suffix(".silent.mp4")
    pattern = str(frame_dir / "frame_%05d.png")
    encode_cmd = [
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
        str(silent_path),
    ]
    subprocess.run(encode_cmd, check=True)

    if job.include_audio:
        total_seconds = frame_index / job.fps
        mux_source_audio(
            silent_path=silent_path,
            render_path=job.render_path,
            source_path=job.source_path,
            total_seconds=total_seconds,
            source_duration=source_info["duration"],
        )
    else:
        silent_path.replace(job.render_path)

    if not keep_frames:
        shutil.rmtree(temp_root)


def render_batch(config_path: Path, *, keep_frames: bool = False) -> None:
    with config_path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    scenes = data.get("scenes")
    if not scenes:
        raise ValueError("Batch config requires a non-empty 'scenes' array")
    base_dirs = [Path.cwd(), config_path.parent]
    for index, scene in enumerate(scenes, start=1):
        scene_data = dict(scene)
        scene_data.setdefault("title", f"P-Video-Animate · Scene {index}")
        job = job_from_dict(scene_data, base_dirs)
        print(f"[{index}/{len(scenes)}] {job.render_path.name}")
        render_video(job, keep_frames=keep_frames)


def print_job_summary(job: JobConfig) -> None:
    duration = estimate_duration(job)
    print(f"Source: {job.source_path}")
    print(f"Render: {job.render_path}")
    print(f"Samples: {len(job.samples)}")
    print(f"Compare mode: {job.compare_mode}")
    for index, sample in enumerate(job.samples, start=1):
        print(f"  [{index}] {sample.output_path} ({sample.output_label})")
    print(f"Estimated duration: {duration:.1f}s at {job.fps} fps")
    print(
        "Timing: "
        f"hook={job.timing.hook_seconds}s, "
        f"slider={job.timing.slider_seconds}s, "
        f"hold={job.timing.hold_output_seconds}s, "
        f"outro={job.timing.outro_seconds}s, "
        f"transition={job.timing.transition_seconds}s"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, help="JSON config path (single scene or batch with scenes[])")
    parser.add_argument("--source", type=str, help="Motion template MP4")
    parser.add_argument("--output", type=str, help="Animated output MP4")
    parser.add_argument("--render", type=str, help="Comparison MP4 output path")
    parser.add_argument("--title", default="P-Video-Animate", help="Top-bar title")
    parser.add_argument("--source-label", default="Motion template")
    parser.add_argument("--output-label", default="Animated subject")
    parser.add_argument("--fps", type=int, default=24)
    parser.add_argument("--width", type=int, default=1920)
    parser.add_argument("--height", type=int, default=1080)
    parser.add_argument("--write-config", type=Path, help="Write resolved config JSON")
    parser.add_argument("--dry-run", action="store_true", help="Validate and print plan only")
    parser.add_argument("--keep-frames", action="store_true", help="Keep intermediate PNG frames")
    parser.add_argument("--no-audio", action="store_true", help="Do not mux audio from output video")
    parser.add_argument(
        "--chrome",
        action="store_true",
        help="Add title bar, margins, and labels (default is full-bleed video)",
    )
    return parser


def resolve_job(args: argparse.Namespace) -> JobConfig:
    if args.config:
        config_path = args.config.resolve()
        with config_path.open(encoding="utf-8") as handle:
            data = json.load(handle)
        if data.get("scenes"):
            raise SystemExit("Config contains 'scenes' — use batch mode without --source/--output/--render")
        return job_from_dict(data, [Path.cwd(), config_path.parent])

    missing = [name for name in ("source", "output", "render") if not getattr(args, name.replace("-", "_"), None)]
    if missing:
        raise SystemExit("Provide --config or all of --source, --output, and --render")

    return build_job_config(
        source=args.source,
        output=args.output,
        render=args.render,
        base_dirs=[Path.cwd()],
        timing=Timing(),
        fps=args.fps,
        width=args.width,
        height=args.height,
        title=args.title,
        source_label=args.source_label,
        output_label=args.output_label,
        include_audio=not args.no_audio,
        full_bleed=not args.chrome,
    )


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.config:
        config_path = args.config.resolve()
        with config_path.open(encoding="utf-8") as handle:
            data = json.load(handle)
        if data.get("scenes"):
            if args.dry_run:
                print(f"Batch config with {len(data['scenes'])} scenes: {config_path}")
                return 0
            render_batch(config_path, keep_frames=args.keep_frames)
            print(f"Rendered {len(data['scenes'])} comparison clips")
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
    print(f"Wrote {job.render_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
