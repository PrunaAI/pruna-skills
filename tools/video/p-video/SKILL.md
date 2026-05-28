---
name: p-video
description: Generates video with Pruna P-API model p-video (text-to-video, image-to-video, audio-conditioned, duration, resolution, draft). Use when the user asks for Pruna video, p-video, cinematic motion, or API usage for Pruna premium video.
license: MIT
metadata:
  version: "0.0.1"
  pruna_model: p-video
---

# p-video (Pruna)

Premium video from text, optional image, or optional audio. Full parameters: [p-video model docs](https://docs.api.pruna.ai/guides/models/p-video).

Shared HTTP patterns: [references/pruna-api.md](../../references/pruna-api.md) (upload, [poll](#poll), [download](#download))

## HTTP (curl)

### Create (async — recommended)

See **Example: async text-to-video** below. Poll and download: [pruna-api.md](../../references/pruna-api.md#poll).

### Upload for image-to-video

```bash
curl -X POST "https://api.pruna.ai/v1/files" \
  -H "apikey: ${PRUNA_API_KEY}" \
  -F "content=@/path/to/first-frame.png"
```

Pass `urls.get` as `input.image`, then create async as above with `"image": "https://api.pruna.ai/v1/files/FILE_ID"`.

## Before generating

Confirm **mode** (T2V / I2V / audio), **`duration`** (unless audio-driven), **`resolution`**, **`fps`**, **`draft`**, and **`prompt`** with the user—or run their documented intake from [single-scene-ai-video](../../../guides/workflows/single-scene-ai-video/SKILL.md) / [multi-scene-ai-video](../../../guides/workflows/multi-scene-ai-video/SKILL.md) before submitting. Validate renders with [p-video-quality-checklist.md](../../../references/p-video-quality-checklist.md).

## Required input

- `prompt` (string)

## Common optional fields

- `image` (URL): image-to-video; when set, `aspect_ratio` is ignored
- `audio` (URL): audio-conditioned; duration follows audio; formats flac, mp3, wav
- `duration`: 1–20 seconds (ignored if `audio` set)
- `resolution`: `720p` or `1080p`
- `fps`: 24 or 48
- `aspect_ratio` when no input image: `16:9`, `9:16`, etc.
- `draft`, `seed`, `save_audio`, `last_frame_image`, `prompt_upsampling`, `disable_safety_filter`

## Example: async text-to-video (recommended)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video' \
  -d '{
    "input": {
      "prompt": "Slow dolly in, rain on city street at night, cinematic",
      "duration": 5,
      "resolution": "720p",
      "aspect_ratio": "16:9"
    }
  }'
```

Poll and download: [pruna-api.md](../../references/pruna-api.md#poll).

**Multi-scene:** fire **all** scene predictions in one parallel async batch after shared uploads; batch-poll. See [parallel-execution.md](../../../references/parallel-execution.md).

## Example: image-to-video

Upload image to `/v1/files`, pass its `urls.get` as `input.image`.

## Typical next steps

- One-scene `p-video` workflow: [single-scene-ai-video](../../../guides/workflows/single-scene-ai-video/SKILL.md)
- Multi-scene `p-video` workflow: [multi-scene-ai-video](../../../guides/workflows/multi-scene-ai-video/SKILL.md)
- Talking portrait: [p-video-avatar](../p-video-avatar/SKILL.md)
- Pipeline: [pruna-generative-pipeline](../../../guides/workflows/pruna-generative-pipeline/SKILL.md)

## Related workflow

Multi-scene AI video: [multi-scene-ai-video](../../../guides/workflows/multi-scene-ai-video/SKILL.md) — phased curl (not in this tool skill).
