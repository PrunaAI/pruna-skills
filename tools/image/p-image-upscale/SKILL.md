---
name: p-image-upscale
description: Upscales images with Pruna P-API model p-image-upscale (target megapixels, detail and realism enhancement, output format). Use when improving resolution for print, large crops, or upscale comparison demos—not as a required step in avatar or video workflows.
license: MIT
metadata:
  version: "0.0.1"
  pruna_model: p-image-upscale
---

# p-image-upscale (Pruna)

AI upscaling with configurable target resolution. Full parameters: [p-image-upscale model docs](https://docs.api.pruna.ai/guides/models/p-image-upscale).

Shared HTTP patterns: [references/pruna-api.md](../../references/pruna-api.md) (upload, [poll](#poll), [download](#download))

## HTTP (curl)

### Upload source image

```bash
curl -X POST "https://api.pruna.ai/v1/files" \
  -H "apikey: ${PRUNA_API_KEY}" \
  -F "content=@/path/to/source.png"
```

Use `urls.get` as `input.image`.

### Create (async — recommended)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-image-upscale' \
  -d '{
    "input": {
      "image": "https://api.pruna.ai/v1/files/FILE_ID",
      "target": 8,
      "enhance_details": true,
      "output_format": "png"
    }
  }'
```

Poll and download: [pruna-api.md](../../references/pruna-api.md#poll).

## Before generating

Confirm **`target`** MP (1–**128**), **`enhance_details`** / **`enhance_realism`**, and **`output_format`** with the user so upscale matches destination. Validate outputs with [p-image-upscale-quality-checklist.md](../../../references/p-image-upscale-quality-checklist.md).

## When to upscale

| Use case | Typical `target` MP | Notes |
|----------|---------------------|--------|
| Print / billboard / extreme crop | **8–128** | Confirm cost/latency with user |
| Mood board / packshot enlargement | **4–16** | Optional in [pruna-generative-pipeline](../../../guides/workflows/pruna-generative-pipeline/SKILL.md) recipes A/B/C |
| Before/after marketing reel | pair with [p-image-upscale-comparison](../../../guides/workflows/p-image-upscale-comparison/SKILL.md) | Not used in avatar or motion-transfer pipelines |

**Video workflows** ([multi-scene-avatar-video](../../../guides/workflows/multi-scene-avatar-video/SKILL.md), [p-video-animate](../../../tools/video/p-video-animate/SKILL.md), [p-video-replace](../../../tools/video/p-video-replace/SKILL.md)) feed **`p-image`** / **`p-image-edit`** outputs directly into video models after the slop gate—do **not** add an upscale step unless the user explicitly asks for print-scale stills.

Recommended defaults: `enhance_details: true`, `enhance_realism: false`. Use `enhance_realism: true` only when the source is already photoreal and you need extra skin texture—it can add waxy artifacts on synthetic edits.

## Prerequisites

`image` must be a reachable URL (upload via `POST /v1/files` first if needed).

## Required input

- `image` (string URL)

## Common optional fields

- `target`: integer megapixels **1–128** (default 4). Model upscales toward this output size; confirm current limits on [p-image-upscale model docs](https://docs.api.pruna.ai/guides/models/p-image-upscale).
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

- Further edit: upscaled URL → [p-image-edit](../p-image-edit/SKILL.md) for layout or copy-safe tweaks.
- **Marketing demo:** before/after zoom + slider video from any still pair → [p-image-upscale-comparison](../../../guides/workflows/p-image-upscale-comparison/SKILL.md) + [`generate_upscale_comparison.py`](../../../guides/workflows/_shared/scripts/generate_upscale_comparison.py).
- Avatar / motion video (no upscale): [multi-scene-avatar-video](../../../guides/workflows/multi-scene-avatar-video/SKILL.md).

## Related workflow

Upscale comparison reels: [p-image-upscale-comparison](../../../guides/workflows/p-image-upscale-comparison/SKILL.md) — bundled `generate_upscale_comparison.py` (not in this tool skill).
