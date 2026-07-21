---
name: stable-audio-2.5
description: Use when someone wants light instrumental background music — an ambient bed under dialogue or underscore for reels and explainers.
license: MIT
metadata:
  version: "1.0.6"
  package: pruna-skills
  provider: replicate
  replicate_model: stability-ai/stable-audio-2.5
---

## Prerequisites

Install and load these skills before generating (skip if already in context via `@pruna`):

| Skill | Description | Install |
| --- | --- | --- |
| `generation-diversity` | Use when writing any generative prompt — ritual seed, explicit structure, scenario axes, and quality gates before paid API calls. | `npx skills add PrunaAI/pruna-skills@generation-diversity -y` |
| `audio-prompting` | Use when crafting TTS, music, or bed prompts for any generative audio model — director style, song structure, and post-production layering. | `npx skills add PrunaAI/pruna-skills@audio-prompting -y` |
| `pruna-api` | Use before any Pruna or Replicate HTTP call — credentials, upload/poll/download, parallel batches, and agent safety. | `npx skills add PrunaAI/pruna-skills@pruna-api -y` |

Or install the full suite once: `npx skills add PrunaAI/pruna-skills@pruna -y`

Follow each skill's **Before generating** / craft sections — do not restate guide content here.

## Environment

```bash
export REPLICATE_API_TOKEN=r8_...
```

Requires **`ffmpeg`** and **`ffprobe`** on PATH for the mix step.

## HTTP (curl)

```bash
curl -s -X POST \
  -H "Authorization: Bearer ${REPLICATE_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "prompt": "Instrumental light electronic pop bed, soft groove and mellow synth pads, calm positive tech atmosphere, understated background music, no vocals, 94 BPM",
      "duration": 90,
      "steps": 8,
      "cfg_scale": 1
    }
  }' \
  "https://api.replicate.com/v1/models/stability-ai/stable-audio-2.5/predictions"
```

Poll `urls.get` until `status` is `succeeded`; download `output` MP3.

## Before generating

1. Complete Prerequisites guide reading order.
2. Confirm **`prompt`**, **`duration`** (match or slightly exceed reel length), and mix **`volume`** (~0.08–0.15 under VO).
3. **Model notes:** lead with **Instrumental** and **no vocals**. Duration 1–190s. Prefer understated beds (BPM ~88–98 for tech launch reels) so music does not compete with dialogue.

## Required input

- `prompt` (string)

## Common optional fields

- `duration` — seconds, 1–190
- `steps` — 4–8 (default 8)
- `cfg_scale` — 1–25 (default 1)
- `seed` — optional integer

## Typical next steps

Common follow-ons after this skill:

| Skill | Description | Install |
| --- | --- | --- |
| `gemini-3.1-flash-tts` | Use when someone needs spoken narration or voiceover — explainer tracks, documentary lines, or voice to pair with generated video. | `npx skills add PrunaAI/pruna-skills@gemini-3.1-flash-tts -y` |
| `visual-transition-reel` | Use when someone wants a montage with transitions between shots — action-sequence reel or multi-scene piece where narration is optional. | `npx skills add PrunaAI/pruna-skills@visual-transition-reel -y` |

