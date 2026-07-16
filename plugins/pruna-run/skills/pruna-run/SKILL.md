---
name: pruna-run
description: Use when the user wants a quick single-shot generation with minimal intake—one image, video clip, or avatar call from a prompt without a full multi-step plan.
license: MIT
metadata:
  version: "1.0.1"
---

# pruna-run (fast entrypoint)

Use this when the user wants immediate execution from one incoming prompt — **agent routing only** (no bundled CLI runner).

**Before any API call:** [generation-diversity.md](./references/generation-diversity.md) (random seed ritual / SSoT + axis rotation).

**Before paid calls:** [requesting-generation-feedback](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/requesting-generation-feedback/skills/requesting-generation-feedback/SKILL.md).

## When NOT to use

- Multi-scene plans with approval gates → use a workflow skill (`avatar-multi-scene`, `music-video`, …)
- Editing an existing image → `p-image-edit`
- Recipe menus or multi-step chains → [pruna-generative-pipeline](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/pruna-generative-pipeline/skills/pruna-generative-pipeline/SKILL.md)

## What it does

Read the user's prompt and pick the shortest chain:

| Route | When | Chain |
|-------|------|-------|
| **image** | Still only | [p-image](../../../../tools/image/p-image/SKILL.md) |
| **i2v** | Motion from a still | `p-image` → [p-video](../../../../tools/video/p-video/SKILL.md) |
| **avatar** | Talking head | `p-image` → [p-video-avatar](../../../../tools/video/p-video-avatar/SKILL.md) |

## Agent execution

1. Confirm `PRUNA_API_KEY` is set (and `REPLICATE_API_TOKEN` only if the chosen route needs Replicate).
2. Apply [generation-diversity.md](./references/generation-diversity.md) — ritual seed + axis rotation before the first generation.
3. Route from the table above; follow the linked tool skill for HTTP payloads and async polling.
4. For **avatar**: draft natural `voice_script` + realistic `voice_prompt`; get user approval before `p-video-avatar`.
5. Log prompts, seeds, and output URLs in a short `manifest.json` beside outputs for reproducibility.

## Notes

- Prefer **async parallel** for video/avatar — poll until `succeeded` per [pruna-api.md](./references/pruna-api.md).
- Multi-scene work: use dedicated workflow skills — narrated films use [scene-anchor-triple.md](https://github.com/PrunaAI/pruna-skills/tree/main/references/shared/scene-anchor-triple.md) ([narrated-multi-scene](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/narrated-multi-scene/skills/narrated-multi-scene/SKILL.md)).
