---
name: p-video-animate
description: Use when someone wants a photo to move like another video — motion transfer, dance remixes, or performance variations from a template clip.
license: MIT
metadata:
  version: "1.0.6"
  package: pruna-skills
  pruna_model: p-video-animate
---

## Prerequisites

Install and load these skills before generating (skip if already in context via `@pruna`):

| Skill | Description | Install |
| --- | --- | --- |
| `generation-diversity` | Use when writing any generative prompt — ritual seed, explicit structure, scenario axes, and quality gates before paid API calls. | `npx skills add PrunaAI/pruna-skills@generation-diversity -y` |
| `video-prompting` | Use when crafting video or motion prompts for any generative model — dramaturgy, camera, physics-safe motion, frame anchors, and clip chaining. | `npx skills add PrunaAI/pruna-skills@video-prompting -y` |
| `pruna-api` | Use before any Pruna or Replicate HTTP call — credentials, upload/poll/download, parallel batches, and agent safety. | `npx skills add PrunaAI/pruna-skills@pruna-api -y` |

Or install the full suite once: `npx skills add PrunaAI/pruna-skills@pruna -y`

Follow each skill's **Before generating** / craft sections — do not restate guide content here.

## Skill boundary

| | **p-video-animate** (this skill) | **p-video-replace** |
|---|----------------------------------|---------------------|
| **User question** | *Animate this picture with some motion?* | *Replace this person in this video?* |
| **Inputs** | One **`image`** + motion-template **`video`** | Source **`video`** + **`images`** (1–4) |
| **Job** | Still performs using copied motion | People/props in footage swapped for refs |

**Use `p-video-replace`** for in-place identity swap. **Use this skill** for motion-transfer showcases and persona variants.

## When NOT to use

Use a different skill instead:

| Skill | Description | Install |
| --- | --- | --- |
| `p-image-edit` | Use when someone wants to edit an existing photo — change outfits or backgrounds, compose from reference images, or apply prompt-driven edits. | `npx skills add PrunaAI/pruna-skills@p-image-edit -y` |
| `p-video-replace` | Use when someone wants to swap a person, outfit, or product inside existing footage while keeping the camera move and audio. | `npx skills add PrunaAI/pruna-skills@p-video-replace -y` |
| `p-video-avatar` | Use when someone wants a person on camera speaking a script — lip-synced host, spokesperson, or narrated avatar from a portrait photo. | `npx skills add PrunaAI/pruna-skills@p-video-avatar -y` |

## HTTP (curl)

### Upload source assets

```bash
curl -X POST "https://api.pruna.ai/v1/files" \
  -H "apikey: ${PRUNA_API_KEY}" \
  -F "content=@/path/to/source-video.mp4"

curl -X POST "https://api.pruna.ai/v1/files" \
  -H "apikey: ${PRUNA_API_KEY}" \
  -F "content=@/path/to/reference-image.png"
```

Use each response `urls.get` in `input.video` and `input.image`.

### Create (async — recommended)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video-animate' \
  -d '{
    "input": {
      "video": "https://api.pruna.ai/v1/files/source-video-abc123",
      "image": "https://api.pruna.ai/v1/files/reference-image-def456",
      "resolution": "720p",
      "target_fps": "original",
      "instruction_prompt": "Animate the reference subject using the motion from the source video."
    }
  }'
```

Poll and download: follow `pruna-api`. Output duration follows the source video.

Complete the random seed ritual from `generation-diversity` before writing prompts.

### Create (sync — quick test only)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video-animate' \
  -H 'Try-Sync: true' \
  -d '{
    "input": {
      "video": "https://api.pruna.ai/v1/files/source-video-abc123",
      "image": "https://api.pruna.ai/v1/files/reference-image-def456"
    }
  }'
```

## Before generating

1. Complete Prerequisites guide reading order.
2. Confirm **`video`** (motion/audio source), **`image`** (subject), **`resolution`**, **`target_fps`**, and optional **`instruction_prompt`**.
3. **Pruna notes:** appearance from **image**, motion from **video**. Match framing/pose/limb visibility to the template’s first frame; repose with `p-image-edit` when close but not exact. Leave **`instruction_prompt`** blank unless you need one concrete end beat. Runware map: `referenceImages[0]` → `image`, `referenceVideos[0]` → `video`, `positivePrompt` → `instruction_prompt`, `settings.preserveAudio` → `save_audio`.

## Required input

- `video` (string URL): source RGB `.mp4`
- `image` (string URL): reference subject to animate

## Common optional fields

- `resolution`: `720p` (default) or `1080p`
- `target_fps`: `original` (default), `24`, or `48`
- `instruction_prompt` (string)
- `save_audio` (boolean, default `true`)
- `seed`, `disable_safety_checker`

## Typical next steps

Common follow-ons after this skill:

| Skill | Description | Install |
| --- | --- | --- |
| `p-image` | Use when someone wants a fast AI image — product shots, hero visuals, mood boards, or draft photos from a text prompt. | `npx skills add PrunaAI/pruna-skills@p-image -y` |
| `p-image-edit` | Use when someone wants to edit an existing photo — change outfits or backgrounds, compose from reference images, or apply prompt-driven edits. | `npx skills add PrunaAI/pruna-skills@p-image-edit -y` |
| `p-video-replace` | Use when someone wants to swap a person, outfit, or product inside existing footage while keeping the camera move and audio. | `npx skills add PrunaAI/pruna-skills@p-video-replace -y` |
| `avatar-multi-scene` | Use when someone wants the same person hosting several clips — multi-segment UGC, comparison reels, or mixed speaking and animated scenes with continuity. | `npx skills add PrunaAI/pruna-skills@avatar-multi-scene -y` |

