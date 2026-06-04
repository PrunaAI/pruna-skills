---
name: p-image-edit
description: Use when the user asks for Pruna image editing, inpainting-style edits, multi-reference compose, or p-image-edit API usage.
license: MIT
metadata:
  version: "0.0.1"
  pruna_model: p-image-edit
---

# p-image-edit (Pruna)

Premium edit and multi-image composition. Full parameters: [p-image-edit model docs](https://docs.api.pruna.ai/guides/models/p-image-edit).

Shared HTTP patterns: [references/shared/pruna-api.md](../../references/shared/pruna-api.md) (upload, [poll](#poll), [download](#download))

## HTTP (curl)

### Upload references

```bash
curl -X POST "https://api.pruna.ai/v1/files" \
  -H "apikey: ${PRUNA_API_KEY}" \
  -F "content=@/path/to/reference.png"
```

Use each response `urls.get` in `input.images`.

### Create (async — recommended)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-image-edit' \
  -d '{
    "input": {
      "prompt": "Change background to soft gradient, keep subject identical",
      "images": ["https://api.pruna.ai/v1/files/FILE_ID"],
      "aspect_ratio": "9:16"
    }
  }'
```

Poll and download: [pruna-api.md](../../references/shared/pruna-api.md#poll).

## Before generating

Confirm **`prompt`**, which **reference files** to upload (1–5), **`aspect_ratio`**, and **`turbo`** on/off with the user. Run [p-image-edit-quality-checklist.md](../../../references/image/p-image-edit-quality-checklist.md) on outputs.

**Avatar pipelines:** edit from the locked **upscaled** hero URL. Chain: **`p-image-edit` → `p-image-upscale` → slop gate → `p-video-avatar`**. Never pass raw edit URLs to video models. See [multi-scene-avatar-video](../../../guides/workflows/core/avatar-multi-scene/SKILL.md).

**Multi-scene narrated films:** generate **start still** (`edit_prompt`) and **end still** (`last_frame_edit_prompt`) per scene for the [scene anchor triple](../../../references/video/scene-anchor-triple.md). Run all scene edits **in parallel** after the hero anchor exists ([parallel-execution.md](../../../references/shared/parallel-execution.md)). See [multi-scene-ai-video](../../../guides/workflows/core/narrated-multi-scene/SKILL.md).

**Visual transition reels:** same start/end still pattern for the [scene anchor pair](../../../references/video/scene-anchor-pair.md) — see [scene-transition-video](../../../guides/workflows/core/visual-transition-reel/SKILL.md).

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
- Motion: [p-video](../../video/p-video/SKILL.md) with [scene anchor pair](../../../references/video/scene-anchor-pair.md), [scene anchor triple](../../../references/video/scene-anchor-triple.md), or [p-video-avatar](../../video/p-video-avatar/SKILL.md)
- Pipeline: [pruna-generative-pipeline](../../../guides/workflows/router/pruna-generative-pipeline/SKILL.md)

## Related workflow

Multi-scene avatar + animate reels: [multi-scene-avatar-video](../../../guides/workflows/core/avatar-multi-scene/SKILL.md) — phased curl or local slider script (not in this tool skill).
