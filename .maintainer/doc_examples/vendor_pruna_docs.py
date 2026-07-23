"""Vendor doc examples from Pruna's official documentation media (no API calls)."""

from __future__ import annotations

import json
import shutil
import urllib.request
from pathlib import Path

HF_BASE = "https://huggingface.co/datasets/pruna-test/documentation-media/resolve/main"

KNIGHT_STILL_HF = (
    "prompt_guide/p-video/"
    "002_A_photorealistic_shot_of_a_knight_walking_through_a_medieval_village_then_entering_a_castle_gates.jpeg"
)
KNIGHT_VIDEO_HF = "prompt_guide/p-video/not-draft.mp4"
KNIGHT_IMAGE_PROMPT = (
    "A photorealistic image of a knight standing in a medieval village near the entrance of castle "
    "gates, detailed surroundings, natural lighting, realistic textures"
)
KNIGHT_VIDEO_PROMPT = (
    "A photorealistic shot of a knight walking through a medieval village, then entering a castle gates"
)

P_IMAGE_ADVANCED_HF = "pruna-endpoints/p_image_advanced.jpeg"
P_IMAGE_EDIT_HF = "pruna-endpoints/image_edit.jpeg"
P_IMAGE_EDIT_PROMPT = "State-of-the-art multi-image edit example from Pruna P-Image-Edit documentation."

UPSCALE_SRC_HF = "prompt_guide/p-image-upscale/p-image-upscale/source/p_image_advanced.jpeg"
UPSCALE_OUT_HF = "prompt_guide/p-image-upscale/p-image-upscale/upscaled/p_image_advanced.jpg"


def _download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "pruna-skills-doc-vendor/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        dest.write_bytes(resp.read())


def _write_meta(path: Path, payload: dict) -> None:
    meta = path.parent / f"{path.stem}.meta.json"
    meta.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _link_or_copy(src: Path, dest: Path) -> None:
    if dest.exists() or dest.is_symlink():
        dest.unlink()
    try:
        dest.symlink_to(src.resolve())
    except OSError:
        shutil.copy2(src, dest)


OBSOLETE_PREFIXES = (
    "quickstart-bloom",
    "quickstart-panda",
    "quickstart-wokflare",
    "readme-quickstart-bloom",
    "readme-quickstart-panda",
    "p-image-brass-hummingbird",
    "p-image-otter-dj",
    "p-image-upscale-hummingbird",
    "p-image-upscale-otter-dj",
    "chain-rooftop",
    "image-to-video-subway",
    "p-video-animate-otter-dj",
)


def _remove_obsolete(out: Path) -> None:
    for prefix in OBSOLETE_PREFIXES:
        for path in out.glob(f"{prefix}*"):
            path.unlink(missing_ok=True)


def vendor_pruna_docs(out: Path) -> None:
    """Refresh Pruna-docs-aligned examples under docs/assets/examples/."""
    out.mkdir(parents=True, exist_ok=True)
    _remove_obsolete(out)

    knight_still = out / "quickstart-knight-still.png"
    _download(f"{HF_BASE}/{KNIGHT_STILL_HF}", knight_still)
    _write_meta(
        knight_still,
        {
            "model": "p-image",
            "tool": "p-image",
            "prompt": KNIGHT_IMAGE_PROMPT,
            "aspect_ratio": "16:9",
            "source": "pruna-docs",
            "source_url": "https://docs.pruna.ai/en/stable/docs_pruna_endpoints/performance_models/p-video.html",
        },
    )

    edit_demo = out / "p-image-edit-demo.png"
    _download(f"{HF_BASE}/{P_IMAGE_EDIT_HF}", edit_demo)
    _write_meta(
        edit_demo,
        {
            "model": "p-image-edit",
            "tool": "p-image-edit",
            "prompt": P_IMAGE_EDIT_PROMPT,
            "source": "pruna-docs",
            "source_url": "https://docs.pruna.ai/en/stable/docs_pruna_endpoints/index.html",
        },
    )

    knight_clip = out / "quickstart-knight-clip.mp4"
    _download(f"{HF_BASE}/{KNIGHT_VIDEO_HF}", knight_clip)
    _write_meta(
        knight_clip,
        {
            "model": "p-video",
            "tool": "p-video",
            "prompt": KNIGHT_VIDEO_PROMPT,
            "image": knight_still.name,
            "duration": 10,
            "resolution": "1080p",
            "source": "pruna-docs",
            "source_url": "https://docs.pruna.ai/en/stable/docs_pruna_endpoints/performance_models/p-video.html",
        },
    )

    advanced = out / "p-image-advanced.png"
    _download(f"{HF_BASE}/{P_IMAGE_ADVANCED_HF}", advanced)
    _write_meta(
        advanced,
        {
            "model": "p-image",
            "tool": "p-image",
            "prompt": "Advanced P-Image example from Pruna documentation.",
            "source": "pruna-docs",
            "source_url": "https://docs.pruna.ai/en/stable/docs_pruna_endpoints/index.html",
        },
    )

    upscale_src = out / "p-image-upscale-source.png"
    upscale_out = out / "p-image-upscale-advanced.png"
    _download(f"{HF_BASE}/{UPSCALE_SRC_HF}", upscale_src)
    _download(f"{HF_BASE}/{UPSCALE_OUT_HF}", upscale_out)
    _write_meta(
        upscale_out,
        {
            "model": "p-image-upscale",
            "tool": "p-image-upscale",
            "prompt": "Upscale P-Image advanced example for print polish.",
            "image": upscale_src.name,
            "target": 8,
            "enhance_details": True,
            "source": "pruna-docs",
            "source_url": "https://docs.pruna.ai/en/stable/docs_pruna_endpoints/index.html",
        },
    )

    i2v_still = out / "image-to-video-knight-still.png"
    i2v_clip = out / "image-to-video-knight-clip.mp4"
    _link_or_copy(knight_still, i2v_still)
    _link_or_copy(knight_clip, i2v_clip)
    _write_meta(
        i2v_still,
        {
            "model": "p-image",
            "tool": "p-image",
            "prompt": KNIGHT_IMAGE_PROMPT,
            "workflow": "image-to-video",
            "source": "pruna-docs",
            "source_url": "https://docs.pruna.ai/en/stable/docs_pruna_endpoints/performance_models/workflows/image_to_video.html",
        },
    )
    _write_meta(
        i2v_clip,
        {
            "model": "p-video",
            "tool": "p-video",
            "prompt": KNIGHT_VIDEO_PROMPT,
            "image": i2v_still.name,
            "duration": 10,
            "workflow": "image-to-video",
            "source": "pruna-docs",
            "source_url": "https://docs.pruna.ai/en/stable/docs_pruna_endpoints/performance_models/workflows/image_to_video.html",
        },
    )

    print("vendored pruna-docs examples (knight i2v, p-image advanced, p-image-edit demo, upscale)")
