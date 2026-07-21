---
name: p-video-replace
description: Use when someone wants to swap a person, outfit, or product inside existing footage while keeping the camera move and audio.
license: MIT
metadata:
  version: "1.0.6"
  package: pruna-skills
  pruna_model: p-video-replace
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

| | **p-video-replace** | **p-video-animate** |
|---|---------------------|---------------------|
| **User question** | *Replace this person in this video?* | *Animate this picture with some motion?* |
| **Goal** | Swap identity **into** existing footage | Drive a **still** with motion from another clip |
| **Source video** | The **final scene** | A **motion template** only |
| **Reference images** | **`images`** — **1 to 4** in **one** call | **`image`** — **one** subject per call |

**Use `p-video-animate`** when the user has a still and wants it to **perform** from a separate template video.

## When NOT to use

Use a different skill instead:

| Skill | Description | Install |
| --- | --- | --- |
| `p-video-animate` | Use when someone wants a photo to move like another video — motion transfer, dance remixes, or performance variations from a template clip. | `npx skills add PrunaAI/pruna-skills@p-video-animate -y` |
| `p-video-avatar` | Use when someone wants a person on camera speaking a script — lip-synced host, spokesperson, or narrated avatar from a portrait photo. | `npx skills add PrunaAI/pruna-skills@p-video-avatar -y` |

## HTTP (curl)

### Upload source assets

```bash
curl -X POST "https://api.pruna.ai/v1/files" \
  -H "apikey: ${PRUNA_API_KEY}" \
  -F "content=@/path/to/source-video.mp4"

curl -X POST "https://api.pruna.ai/v1/files" \
  -H "apikey: ${PRUNA_API_KEY}" \
  -F "content=@/path/to/reference-person-a.png"

curl -X POST "https://api.pruna.ai/v1/files" \
  -H "apikey: ${PRUNA_API_KEY}" \
  -F "content=@/path/to/reference-person-b.png"
```

Use each response `urls.get` in `input.video` and `input.images`.

### Create (async — recommended)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video-replace' \
  -d '{
    "input": {
      "video": "https://api.pruna.ai/v1/files/source-video-abc123",
      "images": [
        "https://api.pruna.ai/v1/files/reference-person-a-def456",
        "https://api.pruna.ai/v1/files/reference-person-b-ghi789"
      ],
      "resolution": "720p",
      "target_fps": "original",
      "instruction_prompt": "Replace the woman on the left (olive coat) with the first reference. Replace the man on the right (navy jacket) with the second reference. Preserve walking pace, camera tracking, and audio."
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
  -H 'Model: p-video-replace' \
  -H 'Try-Sync: true' \
  -d '{
    "input": {
      "video": "https://api.pruna.ai/v1/files/source-video-abc123",
      "images": [
        "https://api.pruna.ai/v1/files/reference-image-def456"
      ]
    }
  }'
```

## Before generating

1. Complete Prerequisites guide reading order.
2. Confirm **`video`**, **`images`** (1–4), **`resolution`**, **`target_fps`**, **`instruction_prompt`**, and swap intent (character / clothing-only / object / mixed).
3. **Pruna notes:** identity comes from **`images`**; slot mapping from **`instruction_prompt`** (name source element → map each ref → preserve-list → “only X changes”). Vague targets and tiny on-screen objects drop quality. Runware map: `inputs.video` → `video`, `referenceImages` → `images`, `positivePrompt` → `instruction_prompt`.

## Required input

- `video` (string URL): source RGB `.mp4`
- `images` (array of 1–4 string URLs): identity reference(s)

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
| `p-video-animate` | Use when someone wants a photo to move like another video — motion transfer, dance remixes, or performance variations from a template clip. | `npx skills add PrunaAI/pruna-skills@p-video-animate -y` |
| `p-image` | Use when someone wants a fast AI image — product shots, hero visuals, mood boards, or draft photos from a text prompt. | `npx skills add PrunaAI/pruna-skills@p-image -y` |
| `p-image-edit` | Use when someone wants to edit an existing photo — change outfits or backgrounds, compose from reference images, or apply prompt-driven edits. | `npx skills add PrunaAI/pruna-skills@p-image-edit -y` |

