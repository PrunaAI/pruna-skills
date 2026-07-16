---
name: pruna-run
description: Use when someone wants a quick one-off generation — one image, video clip, edit, or speaking avatar from a prompt, with minimal intake.
license: MIT
metadata:
  version: "1.0.4"
---

# pruna-run (fast entrypoint)

Use this when the user wants immediate execution from one incoming prompt — **agent routing only** (no bundled CLI runner).

**Before any API call:** [generation-diversity.md](../../../references/shared/generation-diversity.md) (random seed ritual / SSoT + axis rotation).

**Before paid calls:** [requesting-generation-feedback](../requesting-generation-feedback/SKILL.md).

## When NOT to use

- Multi-scene plans with approval gates → use a workflow skill (`avatar-multi-scene`, `music-video`, …)
- Editing an existing image → `p-image-edit`
- Recipe menus or multi-step chains → [pruna-generative-pipeline](../pruna-generative-pipeline/SKILL.md)

## What it does

Read the user's prompt and pick the shortest chain:

| Route | When | Chain |
|-------|------|-------|
| **image** | Still only | [p-image](../../../../tools/image/p-image/SKILL.md) |
| **i2v** | Motion from a still | `p-image` → [p-video](../../../../tools/video/p-video/SKILL.md) |
| **avatar** | Talking head | `p-image` → [p-video-avatar](../../../../tools/video/p-video-avatar/SKILL.md) |

## Agent execution

1. Confirm `PRUNA_API_KEY` is set (and `REPLICATE_API_TOKEN` only if the chosen route needs Replicate).
2. Apply [generation-diversity.md](../../../references/shared/generation-diversity.md) — ritual seed + axis rotation before the first generation.
3. Route from the table above; follow the linked tool skill for HTTP payloads and async polling.
4. For **avatar**: draft natural `voice_script` + realistic `voice_prompt`; get user approval before `p-video-avatar`.
5. Log prompts, seeds, and output URLs in a short `manifest.json` beside outputs for reproducibility.

## Notes

- Prefer **async parallel** for video/avatar — poll until `succeeded` per [pruna-api.md](../../../references/shared/pruna-api.md).
- Multi-scene work: use dedicated workflow skills — narrated films use [scene-anchor-triple.md](../../../references/video/scene-anchor-triple.md) ([narrated-multi-scene](../core/narrated-multi-scene/SKILL.md)).
