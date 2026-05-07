---
name: p-image-edit
description: Edits or composes 1–5 reference images with Pruna P-API model p-image-edit (prompt + images array, aspect ratio, turbo). Use when the user asks for Pruna image editing, inpainting-style edits, multi-image compose, or p-image-edit API usage.
license: MIT
metadata:
  pruna_model: p-image-edit
---

# p-image-edit (Pruna)

Premium edit and multi-image composition. Full parameters: [p-image-edit model docs](https://docs.api.pruna.ai/guides/models/p-image-edit).

Shared HTTP patterns: [references/pruna-api.md](../../references/pruna-api.md)

## Before generating

Confirm **`prompt`**, which **reference files** to upload (1–5), **`aspect_ratio`**, and **`turbo`** on/off with the user. Run [p-image-edit-quality-checklist.md](../../../references/p-image-edit-quality-checklist.md) on outputs. For avatar pipelines, also ensure the frame passed [p-video-avatar-quality-checklist.md](../../../references/p-video-avatar-quality-checklist.md) before downstream **`p-video-avatar`**.

## Prerequisites

Upload each reference to `POST https://api.pruna.ai/v1/files` (multipart `content=@file`). Use each file’s `urls.get` value in `input.images`.

## Required input

- `prompt` (string)
- `images` (array of 1–5 URLs, typically `https://api.pruna.ai/v1/files/{id}`)

## Common optional fields

- `aspect_ratio`: `match_input_image`, `1:1`, `16:9`, `9:16`, etc.
- `turbo` (boolean, default true; turn off for harder edits)
- `seed`, `disable_safety_checker`

## Example: synchronous single-image edit

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-image-edit' \
  -H 'Try-Sync: true' \
  -d '{
    "input": {
      "prompt": "Change background to soft gradient, keep subject identical",
      "images": ["https://api.pruna.ai/v1/files/FILE_ID"],
      "aspect_ratio": "9:16"
    }
  }'
```

## Typical next steps

- Upscale for delivery: [p-image-upscale](../p-image-upscale/SKILL.md)
- Motion: [p-video](../../video/p-video/SKILL.md) or [p-video-avatar](../../video/p-video-avatar/SKILL.md)
- Pipeline: [pruna-generative-pipeline](../../../guides/workflows/pruna-generative-pipeline/SKILL.md)
