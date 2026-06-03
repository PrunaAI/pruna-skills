"""First-party Pruna model registry (see references/pruna-models.md)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Literal

RouteKind = Literal[
    "text_to_image",
    "image_edit",
    "upscale",
    "text_to_video",
    "image_to_video",
    "video_edit",
    "avatar",
    "animate",
    "replace",
    "generic",
]


@dataclass(frozen=True)
class ModelSpec:
    model_id: str
    kind: RouteKind
    default_sync: bool
    output_ext: str
    description: str


MODELS: dict[str, ModelSpec] = {
    "p-image": ModelSpec(
        model_id="p-image",
        kind="text_to_image",
        default_sync=True,
        output_ext=".jpg",
        description="Text-to-image",
    ),
    "p-image-edit": ModelSpec(
        model_id="p-image-edit",
        kind="image_edit",
        default_sync=True,
        output_ext=".jpg",
        description="Image edit / compose (1–5 images)",
    ),
    "p-image-upscale": ModelSpec(
        model_id="p-image-upscale",
        kind="upscale",
        default_sync=True,
        output_ext=".jpg",
        description="Upscale with optional enhance",
    ),
    "p-video": ModelSpec(
        model_id="p-video",
        kind="text_to_video",
        default_sync=False,
        output_ext=".mp4",
        description="Text / image / audio video",
    ),
    "p-video-avatar": ModelSpec(
        model_id="p-video-avatar",
        kind="avatar",
        default_sync=False,
        output_ext=".mp4",
        description="Talking head from portrait + script or audio",
    ),
    "p-video-animate": ModelSpec(
        model_id="p-video-animate",
        kind="animate",
        default_sync=False,
        output_ext=".mp4",
        description="Animate still using source video motion",
    ),
    "p-video-replace": ModelSpec(
        model_id="p-video-replace",
        kind="replace",
        default_sync=False,
        output_ext=".mp4",
        description="Replace people/objects in source video",
    ),
}

# Aliases for pruna-run routing
ROUTE_ALIASES: dict[str, str] = {
    "image": "p-image",
    "i2v": "p-video",
    "avatar": "p-video-avatar",
    "animate": "p-video-animate",
    "replace": "p-video-replace",
    "upscale": "p-image-upscale",
    "edit": "p-image-edit",
    "video": "p-video",
}


def resolve_model(name: str) -> ModelSpec:
    key = ROUTE_ALIASES.get(name, name)
    if key not in MODELS:
        raise KeyError(f"Unknown model {name!r}. Known: {', '.join(sorted(MODELS))}")
    return MODELS[key]
