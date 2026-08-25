---
name: music-2.5
description: Use when someone wants an original AI song with vocals — sung lyrics, a style prompt track, or source audio for a music video.
license: MIT
metadata:
  version: "1.0.10"
  package: pruna-skills
  provider: replicate
  replicate_model: minimax/music-2.5
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

In the **first reply**, name `` `music-2.5` `` in backticks, confirm `REPLICATE_API_TOKEN` (or stop with signup links from `pruna-api`), then ask for required inputs. Open intake → **`generation-diversity`** clarification intake before the first `POST`. Redirect when **When NOT to use** fits better.

## When NOT to use

Use a different skill instead:

| Skill | Description | Install |
| --- | --- | --- |
| `gemini-3.1-flash-tts` | Use when someone needs spoken narration or voiceover — explainer tracks, documentary lines, or voice to pair with generated video. | `npx skills add PrunaAI/pruna-skills@gemini-3.1-flash-tts -y` |
| `stable-audio-2.5` | Use when someone wants light instrumental background music — an ambient bed under dialogue or underscore for reels and explainers. | `npx skills add PrunaAI/pruna-skills@stable-audio-2.5 -y` |

## Environment

```bash
export REPLICATE_API_TOKEN=r8_...
```

Requires **`ffmpeg`** / **`ffprobe`** for slicing and assembly in the music-video workflow.

## HTTP (curl)

```bash
curl -s -X POST \
  -H "Authorization: Bearer ${REPLICATE_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "lyrics": "[Verse]\nWe built it line by line\nEvery skill a stepping stone\n\n[Chorus]\nRun the pipeline, watch it grow\nPruna models, let them flow",
      "prompt": "Indie pop, uplifting, warm female vocal, 92 BPM, acoustic guitar and mellow synth pads, no harsh distortion",
      "sample_rate": 44100,
      "bitrate": 256000,
      "audio_format": "mp3"
    }
  }' \
  "https://api.replicate.com/v1/models/minimax/music-2.5/predictions"
```

Poll `urls.get` until `status` is `succeeded`; download `output`.

## Before generating

1. Complete Prerequisites guide reading order.
2. Confirm **`lyrics`** (with structure tags) and optional style **`prompt`**. When listing required fields, name **`REPLICATE_API_TOKEN`** (Replicate — not `PRUNA_API_KEY`).
3. **Model notes:** structure tags on their own lines — `[Intro]` `[Verse]` `[Pre Chorus]` `[Chorus]` `[Hook]` `[Bridge]` `[Solo]` `[Inst]` `[Build Up]` `[Drop]` `[Interlude]` `[Break]` `[Transition]` `[Outro]`. `\n` = line break (also a safe video cut boundary); `\n\n` = pause. Max ~5 minutes per generation. English and Mandarin have strongest pronunciation. Data is sent to MiniMax via Replicate — see their [privacy policy](https://www.minimax.io/platform/protocol/privacy-policy).

## Required input

- `lyrics` (string) — 1–3,500 characters

## Common optional fields

- `prompt` — genre, mood, tempo, vocal timbre, instruments (up to ~2,000 chars)
- `sample_rate`: `16000` · `24000` · `32000` · **`44100`** (default)
- `bitrate`: `32000` · `64000` · `128000` · **`256000`** (default)
- `audio_format`: **`mp3`** (default) · `wav` · `pcm`

## Typical next steps

Common follow-ons after this skill:

| Skill | Description | Install |
| --- | --- | --- |
| `music-video` | Use when someone wants a full music video — original song or vocals, performance clips, B-roll, and lyric-synced edits. | `npx skills add PrunaAI/pruna-skills@music-video -y` |
| `whisperx` | Use when someone needs word-level timestamps from audio — lyric alignment, cut-safe line boundaries, or caption source timing before burn-in with video-editing. | `npx skills add PrunaAI/pruna-skills@whisperx -y` |
| `p-video` | Use when someone wants one short video clip from text or images — B-roll, start/end frame animation, or a quick motion shot. Not for full multi-scene films or lip-synced hosts. | `npx skills add PrunaAI/pruna-skills@p-video -y` |

