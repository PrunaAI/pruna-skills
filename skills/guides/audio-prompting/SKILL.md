---
name: audio-prompting
description: Use when crafting TTS, music, or bed prompts for any generative audio model — director style, song structure, and post-production layering.
license: MIT
metadata:
  version: "1.0.6"
  package: pruna-skills
---

# Audio prompting

Vendor-neutral craft for **speech, music, and beds**. Works with Gemini TTS, ElevenLabs, Music 2.5, Stable Audio, Suno, and similar APIs.

## Install

| Skill | Description | Install |
| --- | --- | --- |
| `audio-prompting` | Use when crafting TTS, music, or bed prompts for any generative audio model — director style, song structure, and post-production layering. | `npx skills add PrunaAI/pruna-skills@audio-prompting -y` |
| `generation-diversity` | Use when writing any generative prompt — ritual seed, explicit structure, scenario axes, and quality gates before paid API calls. | `npx skills add PrunaAI/pruna-skills@generation-diversity -y` |

## When to use

- Director-style TTS prompts and inline performance tags
- Full songs with vocals vs instrumental beds
- Choosing when to embed audio in a video model vs mix in post
- Narration + bed layering pipelines

## Works with

Gemini Flash TTS, ElevenLabs, Music 2.5, Stable Audio, Suno, Udio, and other audio models. Pair with `video-prompting` when uploading VO into a video model.

## Before generating

1. Follow `generation-diversity` first.
2. TTS → [tts-style-prompting.md](./references/tts-style-prompting.md).
3. Songs / beds → [music-and-bed-prompting.md](./references/music-and-bed-prompting.md).
4. Tool picker + layering → [audio-post-production.md](./references/audio-post-production.md).

## Related skills

Install related skills when the job needs them:

| Skill | Description | Install |
| --- | --- | --- |
| `video-prompting` | Use when crafting video or motion prompts for any generative model — dramaturgy, camera, physics-safe motion, frame anchors, and clip chaining. | `npx skills add PrunaAI/pruna-skills@video-prompting -y` |
| `pruna-api` | Use before any Pruna or Replicate HTTP call — credentials, upload/poll/download, parallel batches, and agent safety. | `npx skills add PrunaAI/pruna-skills@pruna-api -y` |

## Pruna / Replicate tools

Matching install for every model named above. Pick what you need:

| Skill | Description | Install |
| --- | --- | --- |
| `gemini-3.1-flash-tts` | Use when someone needs spoken narration or voiceover — explainer tracks, documentary lines, or voice to pair with generated video. | `npx skills add PrunaAI/pruna-skills@gemini-3.1-flash-tts -y` |
| `music-2.5` | Use when someone wants an original AI song with vocals — sung lyrics, a style prompt track, or source audio for a music video. | `npx skills add PrunaAI/pruna-skills@music-2.5 -y` |
| `stable-audio-2.5` | Use when someone wants light instrumental background music — an ambient bed under dialogue or underscore for reels and explainers. | `npx skills add PrunaAI/pruna-skills@stable-audio-2.5 -y` |
| `whisperx` | Use when someone needs word-level lyric timestamps or cut-safe line boundaries before editing music-video clips. | `npx skills add PrunaAI/pruna-skills@whisperx -y` |

Or install the full suite once: `npx skills add PrunaAI/pruna-skills@pruna -y`

