---
name: whisperx
description: Use when someone needs word-level lyric timestamps or cut-safe line boundaries before editing music-video clips.
license: MIT
metadata:
  version: "1.0.6"
  package: pruna-skills
  provider: replicate
  replicate_model: victor-upmeet/whisperx
---

## Prerequisites

Install and load these skills before generating (skip if already in context via `@pruna`):

| Skill | Description | Install |
| --- | --- | --- |
| `generation-diversity` | Use when writing any generative prompt — ritual seed, explicit structure, scenario axes, and quality gates before paid API calls. | `npx skills add PrunaAI/pruna-skills@generation-diversity -y` |
| `pruna-api` | Use before any Pruna or Replicate HTTP call — credentials, upload/poll/download, parallel batches, and agent safety. | `npx skills add PrunaAI/pruna-skills@pruna-api -y` |

Or install the full suite once: `npx skills add PrunaAI/pruna-skills@pruna -y`

Follow each skill's **Before generating** / craft sections — do not restate guide content here.

## When NOT to use

Use a different skill instead:

| Skill | Description | Install |
| --- | --- | --- |
| `gemini-3.1-flash-tts` | Use when someone needs spoken narration or voiceover — explainer tracks, documentary lines, or voice to pair with generated video. | `npx skills add PrunaAI/pruna-skills@gemini-3.1-flash-tts -y` |

## Environment

```bash
export REPLICATE_API_TOKEN=r8_...
```

## HTTP / pipeline

Prefer the repo helpers (they upload local audio and write JSON + SRT):

```bash
# Agent: follow phase table in this SKILL.md \
  --song output/my-mv/song.mp3 \
  --out output/my-mv/whisperx_transcript.json \
  --initial-prompt "First few lyric lines help recognition"

# Agent: follow phase table in this SKILL.md \
  --cuts output/my-mv/cut_manifest.json \
  --transcript output/my-mv/whisperx_transcript.json \
  --song output/my-mv/song.mp3
```

In a music-video workflow, run this skill during the **align** phase — see `music-video`.

## Before generating

1. Complete Prerequisites guide reading order.
2. Confirm **`audio_file`** (HTTPS URL — helpers upload local files), **`language`**, and **`align_output: true`** for cut alignment.
3. **Model notes:** set **`initial_prompt`** to the first lyric lines for better rap/sung recognition. Optional **`diarization`** for multi-voice battles.

## Required input

- `audio_file` (HTTPS URL)

## Common optional fields

- `language` — ISO code, e.g. `en`
- `align_output` — **`true`** for word-level timestamps (required for cut alignment)
- `initial_prompt` — first lyric lines
- `diarization` — speaker labels

## Typical next steps

Common follow-ons after this skill:

| Skill | Description | Install |
| --- | --- | --- |
| `music-video` | Use when someone wants a full music video — original song or vocals, performance clips, B-roll, and lyric-synced edits. | `npx skills add PrunaAI/pruna-skills@music-video -y` |
| `music-2.5` | Use when someone wants an original AI song with vocals — sung lyrics, a style prompt track, or source audio for a music video. | `npx skills add PrunaAI/pruna-skills@music-2.5 -y` |

