---
name: p-image
description: Generates images with Pruna P-API model p-image (text-to-image, aspect ratios, optional LoRA and seed). Use when the user asks for Pruna images, p-image, fast premium T2I, or API calls to the Pruna image model.
license: MIT
metadata:
  pruna_model: p-image
---

# p-image (Pruna)

Ultra-fast text-to-image via Pruna. Full parameters: [p-image model docs](https://docs.api.pruna.ai/guides/models/p-image).

Shared HTTP patterns: [references/pruna-api.md](../../references/pruna-api.md)

## Before generating

Confirm **`prompt`**, **`aspect_ratio`** (or `width`/`height` if `custom`), and optional **`seed`** / safety flags with the user. Run [p-image-quality-checklist.md](../../../references/p-image-quality-checklist.md) on outputs before downstream steps. If this still is for a scripted video, capture intent via [single-scene-ai-video](../../../guides/workflows/single-scene-ai-video/SKILL.md) or [multi-scene-ai-video](../../../guides/workflows/multi-scene-ai-video/SKILL.md) intake before burning credits.

## Required input

- `prompt` (string)

## Common optional fields

- `aspect_ratio`: `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`, `custom` (with `width` / `height` multiples of 16, 256–1440)
- `seed`, `prompt_upsampling`, `lora_weights`, `lora_scale`, `hf_api_token`, `disable_safety_checker`

## Example: synchronous

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-image' \
  -H 'Try-Sync: true' \
  -d '{
    "input": {
      "prompt": "Product hero shot, minimal studio lighting, 4k",
      "aspect_ratio": "9:16"
    }
  }'
```

## Example: asynchronous

Omit `Try-Sync`, then poll `get_url` until `status` is `succeeded`, then download from `generation_url`.

## Typical next steps

- Refine or composite: [p-image-edit](../p-image-edit/SKILL.md)
- Upscale output: [p-image-upscale](../p-image-upscale/SKILL.md)
- Animate still: [p-video](../../video/p-video/SKILL.md) or talking head [p-video-avatar](../../video/p-video-avatar/SKILL.md)
- Scripted workflows (intake first): [single-scene-avatar-video](../../../guides/workflows/single-scene-avatar-video/SKILL.md), [multi-scene-avatar-video](../../../guides/workflows/multi-scene-avatar-video/SKILL.md)
- Full pipeline: [pruna-generative-pipeline](../../../guides/workflows/pruna-generative-pipeline/SKILL.md)
