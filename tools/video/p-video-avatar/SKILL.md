---
name: p-video-avatar
description: Generates talking-head video with Pruna P-API model p-video-avatar from a portrait plus voice_script or uploaded audio (voice, resolution, video_prompt, voice_prompt). Use when the user asks for Pruna avatar, lip-sync style video, talking head, or p-video-avatar API usage.
license: MIT
metadata:
  pruna_model: p-video-avatar
---

# p-video-avatar (Pruna)

Talking-head video from one image plus **either** `voice_script` **or** `audio` (if both, audio wins). Full parameters: [p-video-avatar model docs](https://docs.api.pruna.ai/guides/models/p-video-avatar).

Shared HTTP patterns: [references/pruna-api.md](../../references/pruna-api.md)

## Before generating

Follow [single-scene-avatar-video](../../../guides/workflows/single-scene-avatar-video/SKILL.md) or [multi-scene-avatar-video](../../../guides/workflows/multi-scene-avatar-video/SKILL.md): **natural-language `voice_script`**, **one fixed `voice` per recurring character**, **explicit user confirmation** before any **`POST /v1/predictions`**, then emit and run the agreed generation steps.

When calling the model directly for a small experiment, still confirm **`image`** URL, exact **`voice_script`** (or uploaded **`audio`**), **`voice`** / **`voice_language`**, short **`voice_prompt`**, and **`video_prompt`** / **`resolution`** with the user. Run [p-video-avatar-quality-checklist.md](../../../references/p-video-avatar-quality-checklist.md) on stills and outputs.

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

## Example: sync with built-in TTS

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video-avatar' \
  -H 'Try-Sync: true' \
  -d '{
    "input": {
      "image": "https://api.pruna.ai/v1/files/FILE_ID",
      "voice_script": "Here is one crisp line about why teams ship faster.",
      "voice": "Puck (Male)",
      "voice_language": "English (US)",
      "resolution": "720p",
      "video_prompt": "Speaks to camera, subtle head motion, stable portrait framing, natural mouth movement"
    }
  }'
```

## Example: uploaded narration

Upload audio to `/v1/files`, pass URL as `input.audio` (omit or ignore `voice_script`).

## Typical next steps

- One-scene avatar workflow: [single-scene-avatar-video](../../../guides/workflows/single-scene-avatar-video/SKILL.md)
- Multi-scene avatar workflow: [multi-scene-avatar-video](../../../guides/workflows/multi-scene-avatar-video/SKILL.md)
- Pipeline: [pruna-generative-pipeline](../../../guides/workflows/pruna-generative-pipeline/SKILL.md)
