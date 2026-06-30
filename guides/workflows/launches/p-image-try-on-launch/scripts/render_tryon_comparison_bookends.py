#!/usr/bin/env python3
"""Render intro/outro clips from existing P-Image-Try-On vs GPT Image 2 comparison assets.

Uses pre-generated comparison GIFs/PNGs under output/comparisons/ — no API calls.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

# GIF beat timing from run_tryon_replicate_comparison.py (12 fps)
_GIF_FPS = 12
_INPUTS_HOLD_S = 3.0
_CROSSFADE_S = 0.5
_OUTPUTS_START_S = _INPUTS_HOLD_S + _CROSSFADE_S
_OUTPUTS_FRAME_INDEX = int(_GIF_FPS * _INPUTS_HOLD_S) + max(6, _GIF_FPS // 2)


def resolve_comparison_dir(plan: dict, out_dir: Path) -> Path | None:
    cfg = plan.get("comparison_bookends")
    if not cfg or not cfg.get("enabled"):
        return None
    raw = Path(cfg["source_dir"])
    if raw.is_absolute():
        return raw
    local = (out_dir / raw).resolve()
    if local.is_dir():
        return local
    for base in (Path.cwd(), out_dir.parent.parent.parent, out_dir.parent):
        candidate = (base / raw).resolve()
        if candidate.is_dir():
            return candidate
    return (Path.cwd() / raw).resolve()


def _slug_dir(source_dir: Path, slug: str) -> Path:
    run_dir = source_dir / slug
    if not (run_dir / "comparison.gif").exists() and not (run_dir / "comparison_compact.png").exists():
        raise FileNotFoundError(f"Missing comparison assets in {run_dir}")
    return run_dir


def _vertical_vf(width: int, height: int, fps: int) -> str:
    pad_color = "0x0a0a0e"
    return (
        f"scale={width}:-1:flags=lanczos,"
        f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color={pad_color},"
        f"fps={fps}"
    )


def png_hold_clip(
    png_path: Path,
    dest: Path,
    *,
    width: int,
    height: int,
    fps: int,
    duration_seconds: float,
) -> Path:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg not found on PATH")
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            ffmpeg,
            "-y",
            "-loop",
            "1",
            "-i",
            str(png_path),
            "-t",
            f"{duration_seconds:.3f}",
            "-vf",
            _vertical_vf(width, height, fps),
            "-an",
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
            str(dest),
        ],
        check=True,
    )
    return dest


def gif_outputs_teaser_clip(
    gif_path: Path,
    dest: Path,
    *,
    width: int,
    height: int,
    fps: int,
    duration_seconds: float,
) -> Path:
    """Encode the outputs beat from a comparison GIF (frames after inputs crossfade)."""
    try:
        from PIL import Image
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("Pillow required: pip install Pillow") from exc

    frames: list[Image.Image] = []
    with Image.open(gif_path) as gif:
        try:
            while True:
                frames.append(gif.convert("RGB").copy())
                gif.seek(gif.tell() + 1)
        except EOFError:
            pass
    if len(frames) <= _OUTPUTS_FRAME_INDEX:
        raise RuntimeError(f"GIF too short for outputs teaser: {gif_path}")

    outputs_frames = frames[_OUTPUTS_FRAME_INDEX:]
    hold_count = max(1, int(round(duration_seconds * fps)))
    if len(outputs_frames) < hold_count:
        last = outputs_frames[-1]
        outputs_frames.extend([last.copy() for _ in range(hold_count - len(outputs_frames))])
    else:
        outputs_frames = outputs_frames[:hold_count]

    tmp_dir = dest.parent / ".bookend_frames"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    for old in tmp_dir.glob("frame_*.png"):
        old.unlink()
    for index, frame in enumerate(outputs_frames):
        frame.save(tmp_dir / f"frame_{index:04d}.png")

    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg not found on PATH")
    subprocess.run(
        [
            ffmpeg,
            "-y",
            "-framerate",
            str(fps),
            "-i",
            str(tmp_dir / "frame_%04d.png"),
            "-vf",
            _vertical_vf(width, height, fps),
            "-an",
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
            str(dest),
        ],
        check=True,
    )
    for old in tmp_dir.glob("frame_*.png"):
        old.unlink()
    return dest


def gif_full_clip(
    gif_path: Path,
    dest: Path,
    *,
    width: int,
    height: int,
    fps: int,
    duration_seconds: float | None,
) -> Path:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg not found on PATH")
    dest.parent.mkdir(parents=True, exist_ok=True)
    filters = [_vertical_vf(width, height, fps)]
    if duration_seconds is not None:
        filters.insert(0, f"trim=duration={duration_seconds:.3f}")
        filters.insert(1, "setpts=PTS-STARTPTS")
    vf = ",".join(filters)
    cmd = [
        ffmpeg,
        "-y",
        "-i",
        str(gif_path),
        "-vf",
        vf,
        "-an",
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
        str(dest),
    ]
    subprocess.run(cmd, check=True)
    return dest


def render_bookend_clips(
    plan: dict,
    out_dir: Path,
    *,
    width: int,
    height: int,
    fps: int = 24,
) -> tuple[Path | None, Path | None]:
    """Return (intro_clip, outro_clip) paths, reusing cached clips when config unchanged."""
    cfg = plan.get("comparison_bookends") or {}
    source_dir = resolve_comparison_dir(plan, out_dir)
    if source_dir is None:
        return None, None

    clips_dir = out_dir / "clips"
    clips_dir.mkdir(parents=True, exist_ok=True)
    cache_meta = clips_dir / "comparison_bookends.meta.json"
    intro_slug = cfg.get("intro_slug", "feat_b2b_art_blazer_set")
    outro_slug = cfg.get("outro_slug", "dom_vfr_boutique_womens_office")
    intro_mode = cfg.get("intro_mode", "teaser")
    outro_mode = cfg.get("outro_mode", "full")
    intro_seconds = float(cfg.get("intro_seconds", 3.5))
    outro_seconds = float(cfg.get("outro_seconds", 7.5))

    intro_dest = clips_dir / "comparison_intro.mp4"
    outro_dest = clips_dir / "comparison_outro.mp4"

    cache_payload = {
        "source_dir": str(source_dir),
        "intro_slug": intro_slug,
        "outro_slug": outro_slug,
        "intro_mode": intro_mode,
        "outro_mode": outro_mode,
        "intro_seconds": intro_seconds,
        "outro_seconds": outro_seconds,
        "width": width,
        "height": height,
        "fps": fps,
        "renderer": "v4",
    }
    if cache_meta.exists():
        try:
            cached = json.loads(cache_meta.read_text(encoding="utf-8"))
            if cached == cache_payload and intro_dest.exists() and outro_dest.exists():
                intro_ok = intro_dest.stat().st_size > 10_000
                outro_ok = outro_dest.stat().st_size > 10_000
                if intro_ok and outro_ok:
                    print(f"Reusing {intro_dest.name} and {outro_dest.name}")
                    return intro_dest, outro_dest
        except json.JSONDecodeError:
            pass

    intro_dir = _slug_dir(source_dir, intro_slug)
    outro_dir = _slug_dir(source_dir, outro_slug)

    if intro_mode in ("teaser", "compact"):
        compact = intro_dir / "comparison_compact.png"
        if not compact.exists():
            compact = intro_dir / "comparison.png"
        png_hold_clip(
            compact,
            intro_dest,
            width=width,
            height=height,
            fps=fps,
            duration_seconds=intro_seconds,
        )
    elif intro_mode == "gif_teaser":
        gif_outputs_teaser_clip(
            intro_dir / "comparison.gif",
            intro_dest,
            width=width,
            height=height,
            fps=fps,
            duration_seconds=intro_seconds,
        )
    elif intro_mode == "full":
        gif_full_clip(
            intro_dir / "comparison.gif",
            intro_dest,
            width=width,
            height=height,
            fps=fps,
            duration_seconds=intro_seconds,
        )
    else:
        raise ValueError(f"Unknown intro_mode: {intro_mode}")

    if outro_mode == "full":
        gif_full_clip(
            outro_dir / "comparison.gif",
            outro_dest,
            width=width,
            height=height,
            fps=fps,
            duration_seconds=outro_seconds,
        )
    elif outro_mode == "teaser":
        gif_outputs_teaser_clip(
            outro_dir / "comparison.gif",
            outro_dest,
            width=width,
            height=height,
            fps=fps,
            duration_seconds=outro_seconds,
        )
    elif outro_mode == "compact":
        compact = outro_dir / "comparison_compact.png"
        if not compact.exists():
            compact = outro_dir / "comparison.png"
        png_hold_clip(
            compact,
            outro_dest,
            width=width,
            height=height,
            fps=fps,
            duration_seconds=outro_seconds,
        )
    else:
        raise ValueError(f"Unknown outro_mode: {outro_mode}")

    cache_meta.write_text(json.dumps(cache_payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {intro_dest}")
    print(f"Wrote {outro_dest}")
    return intro_dest, outro_dest


def _comparisons_root(plan: dict, out_dir: Path) -> Path:
    cmp_cfg = plan.get("comparison") or {}
    return out_dir / str(cmp_cfg.get("subdir", "comparisons"))


def render_inline_comparison_clip(
    plan: dict,
    out_dir: Path,
    scene_id: str,
    *,
    width: int,
    height: int,
    fps: int,
) -> Path | None:
    cmp_cfg = plan.get("comparison") or {}
    slug = f"scene_{scene_id}"
    run_dir = _comparisons_root(plan, out_dir) / slug
    compact = run_dir / "comparison_compact.png"
    if not compact.exists():
        compact = run_dir / "comparison.png"
    if not compact.exists():
        return None

    clips_dir = out_dir / "clips"
    clips_dir.mkdir(parents=True, exist_ok=True)
    dest = clips_dir / f"comparison_after_{scene_id}.mp4"
    meta_path = clips_dir / f"comparison_after_{scene_id}.meta.json"
    duration = float(cmp_cfg.get("scene_seconds", 4.0))
    cache_payload = {
        "scene_id": scene_id,
        "compact": str(compact),
        "compact_mtime": compact.stat().st_mtime,
        "duration": duration,
        "width": width,
        "height": height,
        "fps": fps,
        "renderer": "v1",
    }
    if dest.exists() and meta_path.exists():
        try:
            if json.loads(meta_path.read_text(encoding="utf-8")) == cache_payload:
                print(f"Reusing {dest.name}")
                return dest
        except json.JSONDecodeError:
            pass

    png_hold_clip(
        compact,
        dest,
        width=width,
        height=height,
        fps=fps,
        duration_seconds=duration,
    )
    meta_path.write_text(json.dumps(cache_payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {dest}")
    return dest


def interleave_try_on_comparisons(
    plan: dict,
    out_dir: Path,
    clip_paths: list[Path],
    *,
    width: int,
    height: int,
    fps: int,
) -> list[Path]:
    cmp_cfg = plan.get("comparison") or {}
    if not cmp_cfg.get("after_each_try_on"):
        return clip_paths
    try_on_ids = {str(s["id"]) for s in plan.get("scenes", []) if s.get("type") == "try_on"}
    interleaved: list[Path] = []
    for clip in clip_paths:
        interleaved.append(clip)
        if not clip.name.startswith("scene_") or not clip.name.endswith(".mp4"):
            continue
        scene_id = clip.stem.removeprefix("scene_")
        if scene_id not in try_on_ids:
            continue
        inline = render_inline_comparison_clip(
            plan,
            out_dir,
            scene_id,
            width=width,
            height=height,
            fps=fps,
        )
        if inline is not None:
            interleaved.append(inline)
    return interleaved
