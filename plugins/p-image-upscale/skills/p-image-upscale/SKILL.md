---
name: p-image-upscale
description: Use when the user wants to upscale image resolution, enhance detail in an existing still, or prepare photos for print, large crops, or quality demos.
license: MIT
metadata:
  version: "0.0.2"
  pruna_model: p-image-upscale
---

# p-image-upscale (Pruna)

AI upscaling with configurable target resolution. Full parameters: [p-image-upscale model docs](https://docs.api.pruna.ai/guides/models/p-image-upscale).

Shared HTTP patterns: [pruna-api.md](./references/pruna-api.md) (upload, [poll](#poll), [download](#download))

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

Poll and download: [pruna-api.md](./references/pruna-api.md#poll).

## Before generating

1. **[Generation diversity](./references/generation-diversity.md)** — ritual seed + axis rotation (optional API `seed` if supported).
2. Confirm **`target`** MP (1–**128**), **`enhance_details`** / **`enhance_realism`**, and **`output_format`** with the user so upscale matches destination. Validate outputs with [p-image-upscale-quality-checklist.md](./references/p-image-upscale-quality-checklist.md).

## When to upscale

| Use case | Typical `target` MP | Notes |
|----------|---------------------|--------|
| Print / billboard / extreme crop | **8–128** | Confirm cost/latency with user |
| Mood board / packshot enlargement | **4–16** | Optional in [pruna-generative-pipeline](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/pruna-generative-pipeline/skills/pruna-generative-pipeline/SKILL.md) recipes A/B/C |
| Before/after slider video | [`generate_upscale_comparison.py`](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/_shared/scripts/generate_upscale_comparison.py) | Not used in avatar or motion-transfer pipelines |

**Video workflows** ([avatar-multi-scene](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/avatar-multi-scene/skills/avatar-multi-scene/SKILL.md), [p-video-animate](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/p-video-animate/skills/p-video-animate/SKILL.md), [p-video-replace](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/p-video-replace/skills/p-video-replace/SKILL.md)) feed **`p-image`** / **`p-image-edit`** outputs directly into video models after the slop gate—do **not** add an upscale step unless the user explicitly asks for print-scale stills.

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

- Further edit: upscaled URL → [p-image-edit](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/p-image-edit/skills/p-image-edit/SKILL.md) for layout or copy-safe tweaks.
- **Before/after demo:** zoom + slider from any still pair → [`generate_upscale_comparison.py`](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/_shared/scripts/generate_upscale_comparison.py).
- Avatar / motion video (no upscale): [avatar-multi-scene](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/avatar-multi-scene/skills/avatar-multi-scene/SKILL.md).

## Related workflow

Upscale comparison reels: [`generate_upscale_comparison.py`](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/_shared/scripts/generate_upscale_comparison.py).
