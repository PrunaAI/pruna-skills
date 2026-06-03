#!/usr/bin/env python3
"""Render long slider + zoom comparison videos for prompt-example pairs."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_MANIFEST = REPO_ROOT / "output/launches/p-image-upscale-comparison/prompt-examples/manifest.json"

# Progressive deep-zoom profiles: each stop tightens around the same focal point.
EXAMPLE_VIDEO_PROFILES: dict[str, dict[str, object]] = {
    "perfume-product": {
        "focal_point": {
            "x": 0.50,
            "y": 0.50,
            "levels": 5,
            "labels": [
                "Overview",
                "Bottle surface",
                "Glass reflections",
                "Condensation detail",
                "Maximum detail",
            ],
        },
    },
    "street-portrait": {
        "focal_point": {
            "x": 0.60,
            "y": 0.60,
            "levels": 5,
            "labels": [
                "Overview",
                "Face and expression",
                "Eyes and skin",
                "Book and fabric",
                "Maximum detail",
            ],
        },
    },
    "rainforest-macro": {
        "focal_point": {
            "x": 0.70,
            "y": 0.50,
            "levels": 5,
            "labels": [
                "Overview",
                "Fern structure",
                "Leaf texture",
                "Dew and pores",
                "Maximum detail",
            ],
        },
    },
    "sushi-counter": {
        "focal_point": {
            "x": 0.65,
            "y": 0.30,
            "levels": 5,
            "labels": [
                "Overview",
                "Plate composition",
                "Fish flesh",
                "Rice grains",
                "Maximum detail",
            ],
        },
    },
    "fabric-fashion": {
        "focal_point": {
            "x": 0.40,
            "y": 0.80,
            "levels": 5,
            "labels": [
                "Overview",
                "Silhouette and drape",
                "Silk folds",
                "Thread weave",
                "Maximum detail",
            ],
        },
    },
}

LONG_TIMING = {
    "hook_seconds": 2.5,
    "outro_seconds": 2.5,
    "zoom_seconds": 1.0,
    "slider_seconds": 1.5,
    "hold_after_seconds": 0.7,
    "transition_seconds": 0.8,
}


def load_comparison_module():
    script_path = REPO_ROOT / "guides/workflows/_shared/scripts/generate_upscale_comparison.py"
    spec = importlib.util.spec_from_file_location("generate_upscale_comparison", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {script_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def tier_path(example: dict, target_mp: int) -> Path:
    for tier in example.get("tiers", []):
        if int(tier["target_mp"]) == target_mp:
            return Path(str(tier["path"]))
    example_dir = Path(str(example["before"])).parent
    disk_path = example_dir / f"after_{target_mp}mp.jpg"
    if disk_path.exists():
        return disk_path
    raise KeyError(f"No {target_mp} MP tier for {example['id']}")


def tier_actual_mp(example: dict, target_mp: int, cmp) -> float:
    for tier in example.get("tiers", []):
        if int(tier["target_mp"]) == target_mp:
            return float(tier["actual_mp"])
    return cmp.estimate_megapixels(tier_path(example, target_mp))


def regions_for_profile(cmp, profile: dict[str, object]) -> list:
    focal = profile.get("focal_point")
    if focal:
        return cmp.regions_from_focal_point(
            float(focal["x"]),  # type: ignore[index]
            float(focal["y"]),  # type: ignore[index]
            levels=int(focal.get("levels", 5)),  # type: ignore[union-attr]
            labels=focal.get("labels"),  # type: ignore[union-attr]
        )
    if profile.get("regions"):
        return cmp.parse_regions(profile["regions"])  # type: ignore[arg-type]
    preset = str(profile.get("preset", "generic"))
    return cmp.regions_from_preset(preset)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--after-mp", type=int, default=128, help="Upscale tier to compare against")
    parser.add_argument("--ids", default="", help="Comma-separated example ids (default: all)")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true", help="Re-render even if MP4 exists")
    parser.add_argument("--keep-frames", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    manifest_path = args.manifest.resolve()
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    cmp = load_comparison_module()

    selected_ids = {part.strip() for part in args.ids.split(",") if part.strip()}
    examples = [
        example
        for example in data["examples"]
        if not selected_ids or str(example["id"]) in selected_ids
    ]
    if not examples:
        raise SystemExit("No examples matched")

    for example in examples:
        example_id = str(example["id"])
        profile = EXAMPLE_VIDEO_PROFILES.get(example_id)
        if profile is None:
            print(f"Skipping {example_id}: no video profile")
            continue

        example_dir = Path(str(example["before"])).parent
        before_path = Path(str(example["before"]))
        after_path = tier_path(example, args.after_mp)
        output_path = example_dir / f"comparison_{args.after_mp}mp.mp4"
        config_path = example_dir / f"comparison_{args.after_mp}mp.config.json"

        if output_path.exists() and not args.force:
            print(f"[{example_id}] Skipping existing {output_path.name}")
            continue

        regions = regions_for_profile(cmp, profile)
        job = cmp.build_job_config(
            before=str(before_path),
            after=str(after_path),
            output=str(output_path),
            base_dirs=[example_dir, REPO_ROOT],
            regions=regions,
            timing=cmp.parse_timing(LONG_TIMING),
            fps=24,
            width=1920,
            height=1080,
            title=f"P-Image-Upscale · {example['title']}",
            before_mp=float(example["before_mp"]),
            after_mp=tier_actual_mp(example, args.after_mp, cmp),
        )

        config_payload = cmp.job_to_dict(job)
        if profile.get("focal_point"):
            config_payload["focal_point"] = profile["focal_point"]
        config_path.write_text(json.dumps(config_payload, indent=2) + "\n", encoding="utf-8")
        cmp.print_job_summary(job)

        if args.dry_run:
            continue

        print(f"[{example_id}] Rendering {output_path.name} ...")
        cmp.render_video(job, keep_frames=args.keep_frames)
        print(f"[{example_id}] Wrote {output_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
