---
name: p-video-avatar
description: Generates talking-head video with Pruna P-API model p-video-avatar from a portrait plus voice_script or uploaded audio (voice, resolution, video_prompt, voice_prompt). Use when the user asks for Pruna avatar, lip-sync style video, talking head, or p-video-avatar API usage.
license: MIT
metadata:
  version: "0.0.1"
  pruna_model: p-video-avatar
---

# p-video-avatar (Pruna)

Talking-head video from one image plus **either** `voice_script` **or** `audio` (if both, audio wins). Full parameters: [p-video-avatar model docs](https://docs.api.pruna.ai/guides/models/p-video-avatar).

Shared HTTP patterns: [references/pruna-api.md](../../references/pruna-api.md) (upload, [poll](#poll), [download](#download))

## HTTP (curl)

### Upload portrait

```bash
curl -X POST "https://api.pruna.ai/v1/files" \
  -H "apikey: ${PRUNA_API_KEY}" \
  -F "content=@/path/to/portrait.png"
```

Use `urls.get` as `input.image`.

### Create (async — recommended)

See **Example: async** below. Poll and download: [pruna-api.md](../../references/pruna-api.md#poll).

## Before generating

Follow [single-scene-avatar-video](../../../guides/workflows/single-scene-avatar-video/SKILL.md) or [multi-scene-avatar-video](../../../guides/workflows/multi-scene-avatar-video/SKILL.md): **natural human `voice_script`**, **realistic conversational `voice_prompt`**, **per-scene dynamic `video_prompt`**, **locked `seed`**, **one fixed `voice` per recurring character**, **explicit user confirmation** before any **`POST /v1/predictions`**, then emit and run the agreed generation steps.

When calling the model directly for a small experiment, still confirm **`image`** URL (approved still from `/v1/files`), exact **`voice_script`**, **`voice`** / **`voice_language`**, **`voice_prompt`** (human delivery—not script text), **`video_prompt`** (camera/motion), **`resolution`**, and **`seed`** with the user. Run [p-video-avatar-quality-checklist.md](../../../references/p-video-avatar-quality-checklist.md) on stills and outputs.

**Multi-scene:** after confirmation, create **all** avatar jobs **in parallel** (async, no `Try-Sync`); batch-poll. Prefer **one subagent per clip** — see [parallel-execution.md](../../../references/parallel-execution.md).

## Realistic human voice (defaults for social / founder content)

| Field | Guidance |
|-------|----------|
| **`voice_script`** | Speakable copy: contractions, short sentences, light fillers (*"Hey —"*, *"right?"*). Avoid brochure language. |
| **`voice_prompt`** | How they *sound*: *"Natural conversational tone like a founder on LinkedIn, relaxed pacing, real pauses, honest not salesy."* Never paste product names or script lines here. |
| **`video_prompt`** | Unique camera grammar per clip: angle, push-in, gesture, setting motion—positive wording only. |
| **`seed`** | Lock at project start; reuse across clips from the same character for reproducibility. |

**Motion-template use case (for `p-video-animate` beats):** When this model generates a **source motion video**, prompts must explicitly request **speaking** — `clear lip movement`, explain gestures, `speaks directly to camera`. Motion-source stills need `mouth clearly visible ready to speak`. See [animate-beats.md](../../../guides/workflows/multi-scene-avatar-video/animate-beats.md).

Templates and good/bad pairs: [multi-scene-avatar-video/prompt-templates.md](../../../guides/workflows/multi-scene-avatar-video/prompt-templates.md).

## Field names (JSON)

Pruna P-API uses **snake_case** in `input`: `voice_script`, `video_prompt`, `voice_prompt`, `voice_language`. Some other products use camelCase; map accordingly.

## Required input

- `image` (string URL to jpg/jpeg/png/webp)

Plus **one of**:

- `voice_script` + optional `voice`, `voice_prompt`, `voice_language`, `video_prompt`, `resolution`, or
- `audio` (URL to flac/mp3/wav)

## Common optional fields

- `voice` (default `Zephyr (Female)`); see model doc for full voice list
- `resolution`: `720p` or `1080p`
- `video_prompt` (default `The person is talking.`)
- `voice_prompt` (style / tone; keep short—can leak into performance if too verbose)
- `seed`, `disable_safety_filter`, `disable_prompt_upsampling`

## Example: async (recommended — use for all production)

Omit `Try-Sync`. For multiple clips, **create all jobs in parallel**, then batch-poll every `get_url`. See [parallel-execution.md](../../../references/parallel-execution.md).

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
      "resolution": "1080p",
      "seed": 482901,
      "video_prompt": "Medium close-up speaking directly to lens, subtle push-in"
    }
  }'
```

## Example: sync (single quick test only)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video-avatar' \
  -H 'Try-Sync: true' \
  -d '{
    "input": {
      "image": "https://api.pruna.ai/v1/files/FILE_ID",
      "voice_script": "Hey — so we shipped something I've wanted for a while. Sub-second images, video in seconds, and it actually feels usable in a real workflow.",
      "voice": "Puck (Male)",
      "voice_language": "English (US)",
      "voice_prompt": "Natural conversational tone — like a founder on LinkedIn, relaxed pacing, real pauses, honest not salesy.",
      "resolution": "1080p",
      "seed": 482901,
      "video_prompt": "Medium close-up speaking directly to lens, subtle push-in, natural head motion, warm confident energy"
    }
  }'
```

## Example: uploaded narration

Upload audio to `/v1/files`, pass URL as `input.audio` (omit or ignore `voice_script`).

## Typical next steps

- One-scene avatar workflow: [single-scene-avatar-video](../../../guides/workflows/single-scene-avatar-video/SKILL.md)
- Multi-scene avatar workflow: [multi-scene-avatar-video](../../../guides/workflows/multi-scene-avatar-video/SKILL.md)
- Pipeline: [pruna-generative-pipeline](../../../guides/workflows/pruna-generative-pipeline/SKILL.md)

## Related workflow

Avatar + animate reels: [multi-scene-avatar-video](../../../guides/workflows/multi-scene-avatar-video/SKILL.md), [p-video-animate-comparison](../../../guides/workflows/p-video-animate-comparison/SKILL.md), [p-video-replace-comparison](../../../guides/workflows/p-video-replace-comparison/SKILL.md) — bundled plan runners (not in this tool skill).
