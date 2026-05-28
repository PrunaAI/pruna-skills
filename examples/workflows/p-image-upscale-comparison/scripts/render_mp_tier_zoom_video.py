#!/usr/bin/env python3
"""Render progressive zoom videos that reveal 1× → 8× → 32× → 64× → 128× MP tiers."""

from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Pillow is required. Install with: pip install -r scripts/requirements-comparison.txt"
    ) from exc

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_MANIFEST = REPO_ROOT / "output/p-image-upscale-comparison/prompt-examples/manifest.json"

TIER_TARGETS = (1, 8, 32, 64, 128)
TIER_MULTIPLIERS = ("1×", "8×", "32×", "64×", "128×")

FOCAL_PROFILES: dict[str, dict[str, float | str | list[str]]] = {
    "perfume-product": {
        "x": 0.50,
        "y": 0.45,
        "note": "Perfume bottle — centered",
        "labels": [
            "1× · base resolution",
            "8× · bottle surface",
            "32× · glass reflections",
            "64× · condensation detail",
            "128× · maximum detail",
        ],
    },
    "street-portrait": {
        "x": 0.60,
        "y": 0.45,
        "note": "Face, hands, and open book",
        "labels": [
            "1× · base resolution",
            "8× · face and expression",
            "32× · eyes and skin",
            "64× · book and fabric",
            "128× · maximum detail",
        ],
    },
    "rainforest-macro": {
        "x": 0.60,
        "y": 0.50,
        "note": "Fern and mushroom cluster",
        "labels": [
            "1× · base resolution",
            "8× · fern structure",
            "32× · leaf texture",
            "64× · dew and pores",
            "128× · maximum detail",
        ],
    },
    "sushi-counter": {
        "x": 0.70,
        "y": 0.65,
        "note": "Sushi plate and fish detail",
        "labels": [
            "1× · base resolution",
            "8× · plate composition",
            "32× · fish flesh",
            "64× · rice grains",
            "128× · maximum detail",
        ],
    },
    "fabric-fashion": {
        "x": 0.40,
        "y": 0.60,
        "note": "Silk blouse — lower drape and weave",
        "labels": [
            "1× · base resolution",
            "8× · silhouette and drape",
            "32× · silk folds",
            "64× · thread weave",
            "128× · maximum detail",
        ],
    },
}

MP_TIER_PROGRESSIVE_WIDTHS = (0.52, 0.24, 0.11, 0.05, 0.025)

TIMING = {
    "intro_seconds": 1.5,
    "outro_seconds": 2.0,
    "zoom_seconds": 1.2,
    "reveal_seconds": 1.4,
    "hold_seconds": 1.5,
}

BADGE_FONT_SIZE = 96
LABEL_FONT_SIZE = 24
FONT_CANDIDATES = (
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
)


@dataclass(frozen=True)
class TierStep:
    multiplier: str
    target_mp: int
    actual_mp: float
    image_path: Path
    region_label: str


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for candidate in FONT_CANDIDATES:
        path = Path(candidate)
        if not path.exists():
            continue
        try:
            return ImageFont.truetype(str(path), size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def blended_focal(profile: dict[str, float | str | list[str]]) -> tuple[float, float]:
    return float(profile["x"]), float(profile["y"])


def regions_for_mp_tier(cmp, focal_x: float, focal_y: float, labels: list[str]) -> list:
    regions = []
    for index, width in enumerate(MP_TIER_PROGRESSIVE_WIDTHS):
        height = width * 0.75 if index < len(MP_TIER_PROGRESSIVE_WIDTHS) - 1 else width
        rect = cmp.Rect(focal_x - width / 2, focal_y - height / 2, width, height).clamp()
        regions.append(cmp.Region(label=labels[index], rect=rect))
    return regions


def tier_rects(cmp, regions: list) -> list:
    """Map each tier to a monotonically tighter crop — 1× starts full frame."""
    full_rect = cmp.Rect(0.0, 0.0, 1.0, 1.0)
    return [
        full_rect,
        regions[0].rect,
        regions[1].rect,
        regions[2].rect,
        regions[4].rect,
    ]


def load_comparison_module():
    script_path = REPO_ROOT / "guides/workflows/_shared/scripts/generate_upscale_comparison.py"
    spec = importlib.util.spec_from_file_location("generate_upscale_comparison", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {script_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def tier_steps(example: dict, example_dir: Path, cmp, labels: list[str] | None = None) -> list[TierStep]:
    before_mp = float(example["before_mp"])
    manifest_tiers = {int(item["target_mp"]): item for item in example.get("tiers", [])}
    reveal_labels = labels or [
        "1× · base resolution",
        "8× · upscale reveal",
        "32× · upscale reveal",
        "64× · upscale reveal",
        "128× · maximum detail",
    ]
    steps: list[TierStep] = [
        TierStep(
            multiplier="1×",
            target_mp=1,
            actual_mp=before_mp,
            image_path=Path(str(example["before"])),
            region_label=str(reveal_labels[0]),
        )
    ]
    for index, target in enumerate(TIER_TARGETS[1:], start=1):
        path = example_dir / f"after_{target}mp.jpg"
        if not path.exists():
            manifest_entry = manifest_tiers.get(target)
            if manifest_entry is None:
                raise FileNotFoundError(f"Missing {target} MP tier for {example['id']}: {path}")
            path = Path(str(manifest_entry["path"]))
            actual_mp = float(manifest_entry["actual_mp"])
        else:
            actual_mp = cmp.estimate_megapixels(path)
        steps.append(
            TierStep(
                multiplier=TIER_MULTIPLIERS[index],
                target_mp=target,
                actual_mp=actual_mp,
                image_path=path,
                region_label=str(reveal_labels[index]),
            )
        )
    return steps


def compose_frame(
    cmp,
    *,
    lower_crop: Image.Image | None,
    higher_crop: Image.Image,
    split_ratio: float,
    canvas_w: int,
    canvas_h: int,
    target_mp: int,
    region_label: str,
    show_slider: bool,
) -> Image.Image:
    higher_fit = cmp.fill_canvas(higher_crop, canvas_w, canvas_h)

    if lower_crop is None:
        viewport = higher_fit.copy()
    else:
        lower_fit = cmp.fill_canvas(lower_crop, canvas_w, canvas_h)
        split_x = int(canvas_w * max(0.0, min(1.0, split_ratio)))
        split_x = max(1, min(canvas_w - 1, split_x))
        viewport = Image.new("RGB", (canvas_w, canvas_h))
        viewport.paste(higher_fit.crop((0, 0, split_x, canvas_h)), (0, 0))
        viewport.paste(lower_fit.crop((split_x, 0, canvas_w, canvas_h)), (split_x, 0))

    draw = ImageDraw.Draw(viewport)
    if lower_crop is not None and show_slider:
        split_x = int(canvas_w * max(0.0, min(1.0, split_ratio)))
        split_x = max(1, min(canvas_w - 1, split_x))
        draw.line((split_x, 0, split_x, canvas_h), fill=(255, 255, 255), width=3)
        draw.ellipse(
            (split_x - 12, canvas_h // 2 - 12, split_x + 12, canvas_h // 2 + 12),
            fill=(255, 255, 255),
            outline=(40, 40, 40),
        )

    badge_font = load_font(BADGE_FONT_SIZE)
    label_font = load_font(LABEL_FONT_SIZE)
    badge = f"{target_mp} MP"
    bbox = draw.textbbox((0, 0), badge, font=badge_font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    pad_x, pad_y = 36, 20
    box_w = text_w + pad_x * 2
    box_h = text_h + pad_y * 2
    box_x = (canvas_w - box_w) // 2
    box_y = 28
    draw.rectangle((box_x, box_y, box_x + box_w, box_y + box_h), fill=(0, 0, 0))
    draw.text((box_x + pad_x, box_y + pad_y - bbox[1]), badge, fill=(255, 255, 255), font=badge_font)
    draw.text((16, canvas_h - 34), region_label, fill=(235, 235, 235), font=label_font)
    if lower_crop is not None and show_slider:
        draw.text((16, 16), "Upscaled", fill=(235, 235, 235), font=label_font)
        draw.text((canvas_w - 96, 16), "Previous", fill=(235, 235, 235), font=label_font)
    return viewport


def render_mp_tier_video(
    cmp,
    *,
    steps: list[TierStep],
    regions: list,
    rects: list,
    output_path: Path,
    fps: int = 24,
    width: int = 1920,
    height: int = 1080,
    keep_frames: bool = False,
) -> None:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg not found on PATH")

    images = [Image.open(step.image_path).convert("RGB") for step in steps]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    frame_dir = output_path.parent / f".{output_path.stem}_frames"
    if frame_dir.exists():
        shutil.rmtree(frame_dir)
    frame_dir.mkdir(parents=True, exist_ok=True)

    frame_index = 0
    current_rect = rects[0]

    def save_frame(frame: Image.Image) -> None:
        nonlocal frame_index
        frame.save(frame_dir / f"frame_{frame_index:05d}.png")
        frame_index += 1

    def compose_at(
        *,
        lower_idx: int | None,
        higher_idx: int,
        rect,
        split_ratio: float,
        show_slider: bool,
        label_step_index: int,
    ) -> Image.Image:
        step = steps[label_step_index]
        lower_crop = None if lower_idx is None else cmp.crop_image(images[lower_idx], rect)
        higher_crop = cmp.crop_image(images[higher_idx], rect)
        return compose_frame(
            cmp,
            lower_crop=lower_crop,
            higher_crop=higher_crop,
            split_ratio=split_ratio,
            canvas_w=width,
            canvas_h=height,
            target_mp=step.target_mp,
            region_label=step.region_label,
            show_slider=show_slider,
        )

    def write_hold(*, step_index: int, rect, duration: float) -> None:
        nonlocal current_rect
        frame_count = max(1, int(round(duration * fps)))
        frame = compose_at(
            lower_idx=None,
            higher_idx=step_index,
            rect=rect,
            split_ratio=1.0,
            show_slider=False,
            label_step_index=step_index,
        )
        for _ in range(frame_count):
            save_frame(frame)
        current_rect = rect

    def write_zoom(
        *,
        start_rect,
        end_rect,
        duration: float,
        lower_idx: int,
        higher_idx: int,
        label_step_index: int,
    ) -> None:
        nonlocal current_rect
        frame_count = max(1, int(round(duration * fps)))
        for step_i in range(frame_count):
            progress = step_i / max(1, frame_count - 1) if frame_count > 1 else 1.0
            rect = start_rect.lerp(end_rect, cmp.ease_in_out(progress))
            save_frame(
                compose_at(
                    lower_idx=lower_idx,
                    higher_idx=higher_idx,
                    rect=rect,
                    split_ratio=0.0,
                    show_slider=True,
                    label_step_index=label_step_index,
                )
            )
        current_rect = end_rect

    def write_reveal(
        *,
        lower_idx: int,
        higher_idx: int,
        rect,
        duration: float,
    ) -> None:
        frame_count = max(1, int(round(duration * fps)))
        for step_i in range(frame_count):
            progress = step_i / max(1, frame_count - 1) if frame_count > 1 else 1.0
            split_ratio = cmp.ease_in_out(progress)
            save_frame(
                compose_at(
                    lower_idx=lower_idx,
                    higher_idx=higher_idx,
                    rect=rect,
                    split_ratio=split_ratio,
                    show_slider=True,
                    label_step_index=higher_idx,
                )
            )

    write_hold(step_index=0, rect=rects[0], duration=TIMING["intro_seconds"])

    for index in range(1, len(steps)):
        write_zoom(
            start_rect=current_rect,
            end_rect=rects[index],
            duration=TIMING["zoom_seconds"],
            lower_idx=index - 1,
            higher_idx=index,
            label_step_index=index,
        )
        write_reveal(
            lower_idx=index - 1,
            higher_idx=index,
            rect=rects[index],
            duration=TIMING["reveal_seconds"],
        )
        write_hold(step_index=index, rect=rects[index], duration=TIMING["hold_seconds"])

    outro_frames = max(1, int(round(TIMING["outro_seconds"] * fps)))
    final_step = steps[-1]
    frame = compose_frame(
        cmp,
        lower_crop=None,
        higher_crop=cmp.crop_image(images[-1], rects[-1]),
        split_ratio=1.0,
        canvas_w=width,
        canvas_h=height,
        target_mp=final_step.target_mp,
        region_label=f"{final_step.multiplier} · maximum detail",
        show_slider=False,
    )
    for _ in range(outro_frames):
        save_frame(frame)

    for image in images:
        image.close()

    pattern = str(frame_dir / "frame_%05d.png")
    subprocess.run(
        [
            ffmpeg,
            "-y",
            "-framerate",
            str(fps),
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
            str(output_path),
        ],
        check=True,
    )
    if not keep_frames:
        shutil.rmtree(frame_dir)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--ids", default="", help="Comma-separated example ids")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--keep-frames", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    cmp = load_comparison_module()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    selected = {part.strip() for part in args.ids.split(",") if part.strip()}

    for example in manifest["examples"]:
        example_id = str(example["id"])
        if selected and example_id not in selected:
            continue
        focal = FOCAL_PROFILES.get(example_id)
        if focal is None:
            print(f"Skipping {example_id}: no focal profile")
            continue

        example_dir = Path(str(example["before"])).parent
        output_path = example_dir / "mp_tier_zoom_ladder.mp4"
        if output_path.exists() and not args.force:
            print(f"[{example_id}] Skipping existing {output_path.name}")
            continue

        focal_x, focal_y = blended_focal(focal)
        profile_labels = focal.get("labels")
        label_list = (
            [str(item) for item in profile_labels]
            if isinstance(profile_labels, list)
            else [f"{mult} zoom" for mult in TIER_MULTIPLIERS]
        )
        steps = tier_steps(example, example_dir, cmp, labels=label_list)
        regions = regions_for_mp_tier(
            cmp,
            focal_x,
            focal_y,
            labels=label_list,
        )
        note = focal.get("note")
        if note:
            print(f"[{example_id}] focal ({focal_x:.2f}, {focal_y:.2f}) · {note}")
        rects = tier_rects(cmp, regions)
        duration = (
            TIMING["intro_seconds"]
            + TIMING["hold_seconds"]
            + (len(steps) - 1)
            * (TIMING["zoom_seconds"] + TIMING["reveal_seconds"] + TIMING["hold_seconds"])
            + TIMING["outro_seconds"]
        )
        print(f"[{example_id}] {output_path.name} · ~{duration:.1f}s · tiers: " + " → ".join(s.multiplier for s in steps))

        if args.dry_run:
            continue

        render_mp_tier_video(
            cmp,
            steps=steps,
            regions=regions,
            rects=rects,
            output_path=output_path,
            keep_frames=args.keep_frames,
        )
        print(f"[{example_id}] Wrote {output_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
