---
name: p-image-upscale
description: Use when someone wants to upscale or sharpen an existing image for print, large crops, or higher-quality delivery.
license: MIT
metadata:
  version: "1.0.10"
  package: pruna-skills
  pruna_model: p-image-upscale
---

## Prerequisites

Install and load these skills before generating (skip if already in context via `@pruna`):

| Skill | Description | Install |
| --- | --- | --- |
| `generation-diversity` | Use when writing any generative prompt — ritual seed, explicit structure, scenario axes, and quality gates before paid API calls. | `npx skills add PrunaAI/pruna-skills@generation-diversity -y` |
| `image-prompting` | Use when crafting still-image prompts for any generative model — composition, identity sheets, edits, try-on, and photoreal personas. | `npx skills add PrunaAI/pruna-skills@image-prompting -y` |
| `pruna-api` | Use before any Pruna or Replicate HTTP call — credentials, upload/poll/download, parallel batches, and agent safety. | `npx skills add PrunaAI/pruna-skills@pruna-api -y` |

Or install the full suite once: `npx skills add PrunaAI/pruna-skills@pruna -y`

Follow each skill's **Before generating** / craft sections — do not restate guide content here.

## Agent habit

In the **first reply**, name `` `p-image-upscale` `` in backticks, confirm `PRUNA_API_KEY`, then ask for the source image + `target` megapixels (open intake → **`generation-diversity`** clarification intake if output size is unclear). Redirect new photo generation requests to `p-image`.

## When NOT to use

Use a different skill instead:

| Skill | Description | Install |
| --- | --- | --- |
| `p-image` | Use when someone explicitly wants the fastest, cheapest photo generation — mood boards, bulk panels, or quick iterations — not when controlled photoreal or in-image text is needed. | `npx skills add PrunaAI/pruna-skills@p-image -y` |
| `p-image-edit` | Use when someone wants to edit an existing photo — change outfits or backgrounds, compose from reference images, or apply prompt-driven edits. | `npx skills add PrunaAI/pruna-skills@p-image-edit -y` |
| `avatar-multi-scene` | Use when someone wants the same person hosting several clips — multi-segment UGC, comparison reels, or mixed speaking and animated scenes with continuity. | `npx skills add PrunaAI/pruna-skills@avatar-multi-scene -y` |
| `p-video-animate` | Use when someone wants a photo to move like another video — motion transfer, dance remixes, or performance variations from a template clip. | `npx skills add PrunaAI/pruna-skills@p-video-animate -y` |
| `p-video-replace` | Use when someone wants to swap a person, outfit, or product inside existing footage while keeping the camera move and audio. | `npx skills add PrunaAI/pruna-skills@p-video-replace -y` |

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

Poll and download: follow `pruna-api`.

### Create (sync — quick test only)

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

## Before generating

1. Complete Prerequisites guide reading order.
2. Confirm **`target`** MP (1–**128**), **`enhance_details`** / **`enhance_realism`**, and **`output_format`** with the user.
3. **Pruna note:** defaults — `enhance_details: true`, `enhance_realism: false`. Use `enhance_realism: true` only on already-photoreal sources; it can add waxy artifacts on synthetic edits. Source must already pass the slop gate.

**Print pipeline:** `p-image` hero → optional **`p-image-edit`** → **`p-image-upscale`** on the approved plate (upscale **after** edits). Typical large-crop target: **8** megapixels — confirm `target` with user.

## Required input

- `image` (string URL)

## Common optional fields

- `target`: integer megapixels **1–128** (default 4). Confirm current limits on [p-image-upscale model docs](https://docs.api.pruna.ai/guides/models/p-image-upscale).
- `output_format`: `jpg`, `png`, `webp`
- `output_quality`: 0–100 (not used for PNG)
- `enhance_details`, `enhance_realism` (booleans; realism can drift more from source)
- `disable_safety_checker`

## Typical next steps

Common follow-ons after this skill:

| Skill | Description | Install |
| --- | --- | --- |
| `p-image-edit` | Use when someone wants to edit an existing photo — change outfits or backgrounds, compose from reference images, or apply prompt-driven edits. | `npx skills add PrunaAI/pruna-skills@p-image-edit -y` |
| `avatar-multi-scene` | Use when someone wants the same person hosting several clips — multi-segment UGC, comparison reels, or mixed speaking and animated scenes with continuity. | `npx skills add PrunaAI/pruna-skills@avatar-multi-scene -y` |

