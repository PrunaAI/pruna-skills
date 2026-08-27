---
name: p-video-animate
description: Use when someone wants a photo to move like another video — motion transfer, dance remixes, or performance variations from a template clip.
license: MIT
metadata:
  version: "1.0.10"
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

## Agent habit

In the **first reply**, name `` `p-video-animate` `` in backticks, confirm `PRUNA_API_KEY` (or stop with signup links from `pruna-api`), then ask for required inputs. Open intake → **`generation-diversity`** clarification intake before the first `POST`. When drafting optional **`instruction_prompt`**, follow **Prompt craft (dynamic + faithful)** — do not paste skill examples. Redirect when **When NOT to use** fits better.

## Prompt craft (dynamic + faithful)

Appearance comes from **`image`**; motion from **`video`**. Optional **`instruction_prompt`** is **surgical** — one concrete end beat or pose fix, not a new scene.

| Do | Don't |
| --- | --- |
| Ritual seed before drafting; leave **`instruction_prompt`** blank when refs already align | Copy this skill's generic sample (`Animate the reference subject using the motion from the source video`) when the user named a specific beat |
| Lock the user's subject (from image) and motion source (from video); match framing/pose to the template's first frame | Invent a different performance or swap the subject |
| When needed, one concrete **`instruction_prompt`** beat (`hold landing pose on final frame`, `match arm raise at 0:03`) | Mood-only rewrites or vague `make it dance better` |
| Show **`instruction_prompt`** (if any) before `POST` when not locked | Silent regen that changes identity or ignores the template motion |

**Fidelity check (before pay):** still the user's still + template video. Repose with `p-image-edit` when close but not exact — do not compensate with a vague prompt.

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

1. Complete Prerequisites guide reading order (`generation-diversity` → `video-prompting`).
2. Ritual seed → draft optional **dynamic + faithful** **`instruction_prompt`** (section above) → confirm **`video`** (motion/audio source), **`image`** (subject), **`resolution`**, **`target_fps`**, and **`instruction_prompt`**.
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
| `p-image` | Use when someone explicitly wants the fastest, cheapest photo generation — mood boards, bulk panels, or quick iterations — not when controlled photoreal or in-image text is needed. | `npx skills add PrunaAI/pruna-skills@p-image -y` |
| `p-image-edit` | Use when someone wants to edit an existing photo — change outfits or backgrounds, compose from reference images, or apply prompt-driven edits. | `npx skills add PrunaAI/pruna-skills@p-image-edit -y` |
| `p-video-replace` | Use when someone wants to swap a person, outfit, or product inside existing footage while keeping the camera move and audio. | `npx skills add PrunaAI/pruna-skills@p-video-replace -y` |
| `avatar-multi-scene` | Use when someone wants the same person hosting several clips — multi-segment UGC, comparison reels, or mixed speaking and animated scenes with continuity. | `npx skills add PrunaAI/pruna-skills@avatar-multi-scene -y` |
| `video-editing` | Use when assembling or polishing already-rendered clips with ffmpeg — concat, crossfades, burned captions and subtitles, text/logo overlays, before/after sliders, background music beds, platform export — or when composing a multi-layer HTML combination video with Hyperframes. Not for AI video generation, prompt craft, or model-based video edits. | `npx skills add PrunaAI/pruna-skills@video-editing -y` |

