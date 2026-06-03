---
name: p-image
description: Generates images with Pruna P-API model p-image (text-to-image, aspect ratios, optional LoRA and seed). Use when the user asks for Pruna images, p-image, fast premium T2I, or API calls to the Pruna image model.
license: MIT
metadata:
  version: "0.0.1"
  pruna_model: p-image
---

# p-image (Pruna)

Ultra-fast text-to-image via Pruna. Full parameters: [p-image model docs](https://docs.api.pruna.ai/guides/models/p-image).

Shared HTTP patterns: [references/shared/pruna-api.md](../../references/shared/pruna-api.md) (upload, [poll](#poll), [download](#download))

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
      "seed": 482901
    }
  }'
```

Poll and download: [pruna-api.md](../../references/shared/pruna-api.md#poll).

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

Confirm **`prompt`**, **`aspect_ratio`**, and **`seed`** with the user. Run [p-image-quality-checklist.md](../../../references/image/p-image-quality-checklist.md) on outputs before downstream steps.

## Required input

- `prompt` (string)

## Common optional fields

- `aspect_ratio`: `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`, `custom` (with `width` / `height` multiples of 16, 256–1440)
- `seed`, `prompt_upsampling`, `lora_weights`, `lora_scale`, `hf_api_token`, `disable_safety_checker`

## Example: synchronous

(See **Create (sync)** above.)

## Example: asynchronous (batch / multi-panel)

Omit `Try-Sync`. For N panels with no shared dependency, **POST all jobs in parallel**, then poll every `get_url`. See [parallel-execution.md](../../../references/shared/parallel-execution.md).

## Typical next steps

- Refine or composite: [p-image-edit](../p-image-edit/SKILL.md)
- Upscale output: [p-image-upscale](../p-image-upscale/SKILL.md)
- Animate still: [p-video](../../video/p-video/SKILL.md) — prefer [scene anchor triple](../../../references/video/scene-anchor-triple.md) (`image` + `last_frame_image` + `audio`) for narrated beats; or [p-video-avatar](../../video/p-video-avatar/SKILL.md) for talking head
- Scripted workflows (intake first): [single-scene-avatar-video](../../../guides/workflows/core/avatar-single-scene/SKILL.md), [multi-scene-avatar-video](../../../guides/workflows/core/avatar-multi-scene/SKILL.md)
- Full pipeline: [pruna-generative-pipeline](../../../guides/workflows/router/pruna-generative-pipeline/SKILL.md)

## Related workflow

Replace / comparison reels: [p-video-replace-comparison](../../../guides/workflows/launches/p-video-replace-comparison/SKILL.md) · avatar + animate reels: [multi-scene-avatar-video](../../../guides/workflows/core/avatar-multi-scene/SKILL.md) — bundled scripts live in workflow skills, not here.
