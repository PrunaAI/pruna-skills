---
name: p-image-upscale
description: Upscales images with Pruna P-API model p-image-upscale (target megapixels, detail and realism enhancement, output format). Use when improving resolution of photos or AI-generated frames before video or print.
license: MIT
metadata:
  pruna_model: p-image-upscale
---

# p-image-upscale (Pruna)

AI upscaling with configurable target resolution. Full parameters: [p-image-upscale model docs](https://docs.api.pruna.ai/guides/models/p-image-upscale).

Shared HTTP patterns: [references/pruna-api.md](../../references/pruna-api.md)

## Before generating

Confirm **`target`** MP (1–8), **`enhance_details`** / **`enhance_realism`**, and **`output_format`** with the user so upscale matches how the image will be used (print vs video plate). Validate outputs with [p-image-upscale-quality-checklist.md](../../../references/p-image-upscale-quality-checklist.md).

## Prerequisites

`image` must be a reachable URL (upload via `POST /v1/files` first if needed).

## Required input

- `image` (string URL)

## Common optional fields

- `target`: integer megapixels **1–8** (default 4)
- `output_format`: `jpg`, `png`, `webp`
- `output_quality`: 0–100 (not used for PNG)
- `enhance_details`, `enhance_realism` (booleans; realism can drift more from source)
- `disable_safety_checker`

## Example: synchronous

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-image-upscale' \
  -H 'Try-Sync: true' \
  -d '{
    "input": {
      "image": "https://api.pruna.ai/v1/files/FILE_ID",
      "target": 4,
      "enhance_details": true,
      "enhance_realism": false,
      "output_format": "png"
    }
  }'
```

## Typical next steps

- Use the upscaled URL as `image` / `images` for [p-image-edit](../p-image-edit/SKILL.md), [p-video](../../video/p-video/SKILL.md), or [p-video-avatar](../../video/p-video-avatar/SKILL.md)
