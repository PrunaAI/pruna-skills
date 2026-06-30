---
name: p-image
description: Use when the user wants to generate an image from text, create photos or illustrations from a prompt, or needs a new still for downstream video or avatar work.
license: MIT
metadata:
  version: "0.0.1"
  pruna_model: p-image
---

# p-image (Pruna)

Ultra-fast text-to-image via Pruna. Full parameters: [p-image model docs](https://docs.api.pruna.ai/guides/models/p-image).

**Dynamic persona & scenarios:** [realistic-persona-showcase.md](./references/realistic-persona-showcase.md) · examples: [example-prompt.md](../../examples/shared/realistic-persona/example-prompt.md)

Shared HTTP patterns: [pruna-api.md](./references/pruna-api.md) (upload, [poll](#poll), [download](#download))

## HTTP (curl)

### Create (async — recommended)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-image' \
  -d '{
    "input": {
      "prompt": "Product hero shot, minimal studio lighting, 4k",
      "aspect_ratio": "9:16",
      "seed": 518263
    }
  }'
```

Poll and download: [pruna-api.md](./references/pruna-api.md#poll).

Example `"seed": 518263` is illustrative — use a fresh [random seed ritual](./references/random-seed-ritual.md) integer for each new generation.

### Create (sync — quick test only)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-image' \
  -H 'Try-Sync: true' \
  -d '{"input":{"prompt":"Product hero shot","aspect_ratio":"9:16"}}'
```

## Before generating

1. **[Generation diversity](./references/generation-diversity.md)** — ritual seed + axis rotation (never copy example seeds). **Multi-example batches:** different **`aspect_ratio`** per still (`1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`).
2. Confirm **`prompt`**, **`aspect_ratio`**, and **`seed`** with the user. Run [p-image-quality-checklist.md](./references/image/p-image-quality-checklist.md) on outputs before downstream steps.

## Production quality — photoreal personas

Default demos often look **AI sloppy** (generic white background, plastic skin, same face). For **`p-video-avatar`**, **`p-image-try-on`**, or public playground examples, art-direct plates explicitly:

| Goal | Prompt discipline |
|------|-------------------|
| **Photoreal** | `documentary portrait, natural skin pores, not CGI, not illustration` |
| **Stylized / anime** | Named `visual_style_tag` — cinematic cel, cyberpunk anime, clay, CG 3D; mouth visible for avatars |
| **Diverse cast** | Specific age, ethnicity, archetype — rotate across example sets |
| **Dynamic worlds** | Named setting + lighting + **camera angle** — not one template repeated |
| **Scenario matrix** | Plan medium × angle × setting × **aspect_ratio** per row before generating |
| **Avatar-ready** | Face large; **mouth clearly visible**; hands away from mouth |
| **Try-on-ready** | Full-body or region coverage for garment type (feet for shoes, etc.) |

Full scenario generation (photographic styles, anime sub-styles, camera ladder, 8-slot matrix): [realistic-persona-showcase.md](./references/realistic-persona-showcase.md). Variety planning: [visual-variety-bible.md](./references/visual-variety-bible.md).

Lock **`seed`** at hero generation when the same identity continues to **`p-image-edit`**, **`p-image-try-on`**, or **`p-video-avatar`**.

## Required input

- `prompt` (string)

## Common optional fields

- `aspect_ratio`: `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`, `custom` (with `width` / `height` multiples of 16, 256–1440)
- `seed`, `prompt_upsampling`, `lora_weights`, `lora_scale`, `hf_api_token`, `disable_safety_checker`

## Example: synchronous

(See **Create (sync)** above.)

## Example: asynchronous (batch / multi-panel)

Omit `Try-Sync`. For N panels with no shared dependency, **POST all jobs in parallel**, then poll every `get_url`. See [parallel-execution.md](./references/parallel-execution.md).

## Typical next steps

- Refine or composite: [p-image-edit](../p-image-edit/SKILL.md)
- Virtual try-on on a photoreal person plate: [p-image-try-on](../p-image-try-on/SKILL.md) — see [realistic-persona-showcase.md](./references/realistic-persona-showcase.md)
- Upscale output: [p-image-upscale](../p-image-upscale/SKILL.md)
- Animate still: [p-video](../../video/p-video/SKILL.md) — prefer [scene anchor triple](./references/scene-anchor-triple.md) (`image` + `last_frame_image` + `audio`) for narrated beats; or [p-video-avatar](../../video/p-video-avatar/SKILL.md) for talking head
- Scripted workflows (intake first): [single-scene-avatar-video](../../../workflows/core/avatar-single-scene/SKILL.md), [multi-scene-avatar-video](../../../workflows/core/avatar-multi-scene/SKILL.md)
- Full pipeline: [pruna-generative-pipeline](../../../workflows/router/pruna-generative-pipeline/SKILL.md)

## Related workflow

Avatar + animate reels: [multi-scene-avatar-video](../../../workflows/core/avatar-multi-scene/SKILL.md) — bundled scripts live in workflow skills, not here.
