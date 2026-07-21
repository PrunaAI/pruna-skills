---
name: p-image-edit
description: Use when someone wants to edit an existing photo — change outfits or backgrounds, compose from reference images, or apply prompt-driven edits.
license: MIT
metadata:
  version: "1.0.6"
  package: pruna-skills
  pruna_model: p-image-edit
---

## Prerequisites

Install and load these skills before generating (skip if already in context via `@pruna`):

| Skill | Description | Install |
| --- | --- | --- |
| `generation-diversity` | Use when writing any generative prompt — ritual seed, explicit structure, scenario axes, and quality gates before paid API calls. | `npx skills add PrunaAI/pruna-skills@generation-diversity -y` |
| `image-prompting` | Use when crafting still-image prompts for any generative model — composition, identity sheets, edits, try-on, and photoreal personas. | `npx skills add PrunaAI/pruna-skills@image-prompting -y` |
| `video-prompting` | Use when crafting video or motion prompts for any generative model — dramaturgy, camera, physics-safe motion, frame anchors, and clip chaining. | `npx skills add PrunaAI/pruna-skills@video-prompting -y` |
| `pruna-api` | Use before any Pruna or Replicate HTTP call — credentials, upload/poll/download, parallel batches, and agent safety. | `npx skills add PrunaAI/pruna-skills@pruna-api -y` |

Or install the full suite once: `npx skills add PrunaAI/pruna-skills@pruna -y`

Follow each skill's **Before generating** / craft sections — do not restate guide content here.

## When NOT to use

Use a different skill instead:

| Skill | Description | Install |
| --- | --- | --- |
| `p-image` | Use when someone wants a fast AI image — product shots, hero visuals, mood boards, or draft photos from a text prompt. | `npx skills add PrunaAI/pruna-skills@p-image -y` |
| `p-image-try-on` | Use when someone wants virtual try-on — dress a person in clothes from reference photos for fashion or ecommerce. | `npx skills add PrunaAI/pruna-skills@p-image-try-on -y` |
| `p-image-upscale` | Use when someone wants to upscale or sharpen an existing image for print, large crops, or higher-quality delivery. | `npx skills add PrunaAI/pruna-skills@p-image-upscale -y` |

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

Poll and download: follow `pruna-api`.

Complete the random seed ritual from `generation-diversity` before writing prompts — **do not** pass the ritual string as API `seed`. Optional `seed` only when the user requests reproducibility.

### Create (sync — quick test only)

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

## Before generating

1. Complete Prerequisites guide reading order.
2. Confirm **`prompt`**, which **reference files** to upload (1–5), **`aspect_ratio`**, and **`turbo`** on/off with the user.
3. **Pruna note:** turn **`turbo` off** for harder edits. Avatar pipelines: edit from the locked **upscaled** hero URL, then upscale again before video — never pass raw edit URLs to video models.

## Required input

- `prompt` (string)
- `images` (array of 1–5 URLs, typically `https://api.pruna.ai/v1/files/{id}`)

## Common optional fields

- `aspect_ratio`: `match_input_image`, `1:1`, `16:9`, `9:16`, etc.
- `turbo` (boolean, default true; turn off for harder edits)
- `seed`, `disable_safety_checker`

## Typical next steps

Common follow-ons after this skill:

| Skill | Description | Install |
| --- | --- | --- |
| `p-image-upscale` | Use when someone wants to upscale or sharpen an existing image for print, large crops, or higher-quality delivery. | `npx skills add PrunaAI/pruna-skills@p-image-upscale -y` |
| `p-video` | Use when someone wants one short video clip from text or images — B-roll, start/end frame animation, or a quick motion shot. Not for full multi-scene films or lip-synced hosts. | `npx skills add PrunaAI/pruna-skills@p-video -y` |
| `p-video-avatar` | Use when someone wants a person on camera speaking a script — lip-synced host, spokesperson, or narrated avatar from a portrait photo. | `npx skills add PrunaAI/pruna-skills@p-video-avatar -y` |
| `avatar-multi-scene` | Use when someone wants the same person hosting several clips — multi-segment UGC, comparison reels, or mixed speaking and animated scenes with continuity. | `npx skills add PrunaAI/pruna-skills@avatar-multi-scene -y` |
| `narrated-multi-scene` | Use when someone wants a multi-part story with voiceover — episodic B-roll, chaptered promo, or several linked video scenes without on-camera dialogue. | `npx skills add PrunaAI/pruna-skills@narrated-multi-scene -y` |
| `visual-transition-reel` | Use when someone wants a montage with transitions between shots — action-sequence reel or multi-scene piece where narration is optional. | `npx skills add PrunaAI/pruna-skills@visual-transition-reel -y` |

