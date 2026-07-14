"""Helpers for p-video-avatar API payloads (negative prompt suppression)."""

from __future__ import annotations

from typing import Any

# Pruna docs: experimental; both prompt and strength > 0 must be set.
# https://docs.pruna.ai/en/stable/docs_pruna_endpoints/performance_models/p-video-avatar.html
DEFAULT_AVATAR_NEGATIVE_PROMPT = (
    "subtitles, captions, on-screen text, burned-in text, watermark, logo, "
    "typography, letters, words, readable signage, UI overlay, lower third, "
    "chyron, title card, price tag, packaging label, menu text"
)

DEFAULT_AVATAR_NEGATIVE_PROMPT_STRENGTH = 0.35


def avatar_negative_from_plan(
    plan: dict[str, Any],
    scene: dict[str, Any] | None = None,
) -> tuple[str, float]:
    """Resolve negative_prompt + strength: scene overrides > plan.defaults > module defaults."""
    defaults = plan.get("defaults") or {}
    prompt = ""
    strength: float | int | None = None

    if scene:
        if "negative_prompt" in scene:
            prompt = str(scene.get("negative_prompt") or "")
        if "negative_prompt_strength" in scene:
            strength = scene.get("negative_prompt_strength")

    if not prompt:
        prompt = str(
            defaults.get("avatar_negative_prompt")
            or plan.get("avatar_negative_prompt")
            or DEFAULT_AVATAR_NEGATIVE_PROMPT
        )
    if strength is None:
        raw = defaults.get("avatar_negative_prompt_strength")
        if raw is None:
            raw = plan.get("avatar_negative_prompt_strength")
        if raw is None:
            strength = DEFAULT_AVATAR_NEGATIVE_PROMPT_STRENGTH
        else:
            strength = raw

    return prompt.strip(), float(strength)


def apply_avatar_negative_prompt(
    payload: dict[str, Any],
    plan: dict[str, Any],
    scene: dict[str, Any] | None = None,
) -> None:
    """Attach avatar negative-prompt fields when the P-API schema allows them.

    As of 2026-06, POST /v1/predictions (p-video-avatar) returns 400 for both
    negative_prompt and negative_prompt_strength (additional properties forbidden).
    Keep avatar_negative_from_plan() for plans/docs; do not send until schema restores.
    """
    _ = (payload, plan, scene)
