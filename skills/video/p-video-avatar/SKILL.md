---
name: p-video-avatar
description: Use when someone wants a person on camera speaking a script — lip-synced host, spokesperson, or narrated avatar from a portrait photo.
license: MIT
metadata:
  version: "1.0.6"
  package: pruna-skills
  pruna_model: p-video-avatar
---

## Prerequisites

Install and load these skills before generating (skip if already in context via `@pruna`):

| Skill | Description | Install |
| --- | --- | --- |
| `generation-diversity` | Use when writing any generative prompt — ritual seed, explicit structure, scenario axes, and quality gates before paid API calls. | `npx skills add PrunaAI/pruna-skills@generation-diversity -y` |
| `video-prompting` | Use when crafting video or motion prompts for any generative model — dramaturgy, camera, physics-safe motion, frame anchors, and clip chaining. | `npx skills add PrunaAI/pruna-skills@video-prompting -y` |
| `image-prompting` | Use when crafting still-image prompts for any generative model — composition, identity sheets, edits, try-on, and photoreal personas. | `npx skills add PrunaAI/pruna-skills@image-prompting -y` |
| `pruna-api` | Use before any Pruna or Replicate HTTP call — credentials, upload/poll/download, parallel batches, and agent safety. | `npx skills add PrunaAI/pruna-skills@pruna-api -y` |

Or install the full suite once: `npx skills add PrunaAI/pruna-skills@pruna -y`

Follow each skill's **Before generating** / craft sections — do not restate guide content here.

## When NOT to use

Use a different skill instead:

| Skill | Description | Install |
| --- | --- | --- |
| `p-video` | Use when someone wants one short video clip from text or images — B-roll, start/end frame animation, or a quick motion shot. Not for full multi-scene films or lip-synced hosts. | `npx skills add PrunaAI/pruna-skills@p-video -y` |
| `p-video-animate` | Use when someone wants a photo to move like another video — motion transfer, dance remixes, or performance variations from a template clip. | `npx skills add PrunaAI/pruna-skills@p-video-animate -y` |
| `p-video-replace` | Use when someone wants to swap a person, outfit, or product inside existing footage while keeping the camera move and audio. | `npx skills add PrunaAI/pruna-skills@p-video-replace -y` |

## HTTP (curl)

### Upload portrait

```bash
curl -X POST "https://api.pruna.ai/v1/files" \
  -H "apikey: ${PRUNA_API_KEY}" \
  -F "content=@/path/to/portrait.png"
```

Use `urls.get` as `input.image`.

### Create (async — recommended)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video-avatar' \
  -d '{
    "input": {
      "image": "https://api.pruna.ai/v1/files/FILE_ID",
      "voice_script": "Hey — so we shipped something I've wanted for a while.",
      "voice": "Puck (Male)",
      "voice_language": "English (US)",
      "voice_prompt": "Natural conversational tone — relaxed pacing, real pauses.",
      "resolution": "720p",
      "video_prompt": "Medium close-up speaking directly to lens, subtle push-in",
      "negative_prompt": "subtitles, captions, on-screen text, watermark, logo, typography, letters, words",
      "negative_prompt_strength": 0.35
    }
  }'
```

Poll and download: follow `pruna-api`.

Complete the random seed ritual from `generation-diversity` before writing prompts — omit `seed` unless the user supplied **`api_seed`**. Confirm `voice_language` with the user.

For multiple clips: create **all** jobs in parallel (async, no `Try-Sync`), then batch-poll.

### Create (sync — quick test only)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video-avatar' \
  -H 'Try-Sync: true' \
  -d '{
    "input": {
      "image": "https://api.pruna.ai/v1/files/FILE_ID",
      "voice_script": "Hey — so we shipped something I've wanted for a while.",
      "voice": "Puck (Male)",
      "voice_language": "English (US)",
      "voice_prompt": "Natural conversational tone — relaxed pacing, real pauses.",
      "resolution": "720p",
      "video_prompt": "Medium close-up speaking directly to lens, subtle push-in"
    }
  }'
```

### Uploaded narration (audio wins over voice_script)

Generate `gemini-3.1-flash-tts` → upload to `/v1/files`. Pass as `input.audio` with portrait `image` (optional `last_frame_image`).

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video-avatar' \
  -d '{
    "input": {
      "image": "https://api.pruna.ai/v1/files/PORTRAIT_START",
      "last_frame_image": "https://api.pruna.ai/v1/files/PORTRAIT_END",
      "audio": "https://api.pruna.ai/v1/files/NARRATION_ID",
      "resolution": "720p",
      "video_prompt": "Medium close-up, natural head motion matching narration"
    }
  }'
```

## Before generating

1. Complete Prerequisites guide reading order.
2. Confirm **`image`** URL, **`voice_script`** (or **`audio`**), **`voice`** / **`voice_language`**, **`voice_prompt`**, **`video_prompt`**, and **`resolution`**. Explicit user confirmation before any paid call.
3. **Pruna notes:** P-API uses **snake_case** (`voice_script`, `video_prompt`, …). Mouth must be visible on the plate. Unique **`video_prompt`** per clip — do not reuse one string across a multi-scene reel. Default `The person is talking.` is quick-test only.

### Negative prompt (experimental — suppress on-screen text)

| Field | Default | Rule |
|-------|---------|------|
| `negative_prompt` | `""` | Comma-separated elements to **suppress** |
| `negative_prompt_strength` | `0` | Both must be set: non-empty prompt **and** strength **> 0** |

Starter: `subtitles, captions, on-screen text, burned-in text, watermark, logo, typography, letters, words`. Start strength around **0.3–0.4**. See `avatar-single-scene`
- Multi-scene: `avatar-multi-scene`
- Slider demos: `avatar-multi-scene`