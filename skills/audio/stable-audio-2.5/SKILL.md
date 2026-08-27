---
name: stable-audio-2.5
description: Use when someone wants light instrumental background music — an ambient bed under dialogue or underscore for reels and explainers.
license: MIT
metadata:
  version: "1.0.10"
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

## Agent habit

In the **first reply**, name `` `stable-audio-2.5` `` in backticks, confirm `REPLICATE_API_TOKEN` (or stop with signup links from `pruna-api`), then ask for required inputs. Open intake → **`generation-diversity`** clarification intake before the first `POST`. Redirect when **When NOT to use** fits better.

## When NOT to use

Use a different skill instead:

| Skill | Description | Install |
| --- | --- | --- |
| `music-2.5` | Use when someone wants an original AI song with vocals — sung lyrics, a style prompt track, or source audio for a music video. | `npx skills add PrunaAI/pruna-skills@music-2.5 -y` |
| `gemini-3.1-flash-tts` | Use when someone needs spoken narration or voiceover — explainer tracks, documentary lines, or voice to pair with generated video. | `npx skills add PrunaAI/pruna-skills@gemini-3.1-flash-tts -y` |

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

1. Complete Prerequisites guide reading order — bed prompt craft: `audio-prompting` **Worked examples** (instrumental bed).
2. Confirm **`prompt`**, **`duration`** (match or slightly exceed reel length), and mix **`volume`** (~0.08–0.15 under VO). When listing fields, name **`REPLICATE_API_TOKEN`** (Replicate — not `PRUNA_API_KEY`).
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
| `video-editing` | Use when assembling or polishing already-rendered clips with ffmpeg — concat, crossfades, burned captions and subtitles, text/logo overlays, before/after sliders, background music beds, platform export — or when composing a multi-layer HTML combination video with Hyperframes. Not for AI video generation, prompt craft, or model-based video edits. | `npx skills add PrunaAI/pruna-skills@video-editing -y` |

