---
name: audio-prompting
description: Use when crafting TTS, music, or bed prompts for any generative audio model — director style, song structure, and post-production layering.
license: MIT
metadata:
  version: "1.0.10"
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

## When NOT to use

Use a different skill instead:

| Skill | Description | Install |
| --- | --- | --- |
| `music-2.5` | Use when someone wants an original AI song with vocals — sung lyrics, a style prompt track, or source audio for a music video. | `npx skills add PrunaAI/pruna-skills@music-2.5 -y` |
| `stable-audio-2.5` | Use when someone wants light instrumental background music — an ambient bed under dialogue or underscore for reels and explainers. | `npx skills add PrunaAI/pruna-skills@stable-audio-2.5 -y` |
| `gemini-3.1-flash-tts` | Use when someone needs spoken narration or voiceover — explainer tracks, documentary lines, or voice to pair with generated video. | `npx skills add PrunaAI/pruna-skills@gemini-3.1-flash-tts -y` |
| `video-prompting` | Use when crafting video or motion prompts for any generative model — dramaturgy, camera, physics-safe motion, frame anchors, and clip chaining. | `npx skills add PrunaAI/pruna-skills@video-prompting -y` |
| `image-prompting` | Use when crafting still-image prompts for any generative model — composition, identity sheets, edits, try-on, and photoreal personas. | `npx skills add PrunaAI/pruna-skills@image-prompting -y` |
| `video-editing` | Use when assembling or polishing already-rendered clips with ffmpeg — concat, crossfades, burned captions and subtitles, text/logo overlays, before/after sliders, background music beds, platform export — or when composing a multi-layer HTML combination video with Hyperframes. Not for AI video generation, prompt craft, or model-based video edits. | `npx skills add PrunaAI/pruna-skills@video-editing -y` |

## Guide habit

In the **first reply**, name `` `audio-prompting` `` in backticks. When VO vs bed vs full song, locale, or embed-vs-post are open, open intake → **`generation-diversity`** clarification intake. For embed-vs-post questions, cite [audio-post-production.md](./references/audio-post-production.md) — prefer embed in the video model; post-mux only as fallback.

## Before generating

1. Follow `generation-diversity` first.
2. TTS → [tts-style-prompting.md](./references/tts-style-prompting.md).
3. Songs / beds → [music-and-bed-prompting.md](./references/music-and-bed-prompting.md).
4. Tool picker + layering → [audio-post-production.md](./references/audio-post-production.md).

## Song structure (vocals)

Original tracks with sung vocals → **`music-2.5`**, not Stable Audio. In the **first reply**, say you will draft **lyrics** (verse / chorus / bridge as needed) plus a separate **music** style prompt per [music-and-bed-prompting.md](./references/music-and-bed-prompting.md). Stable Audio is instrumental beds only — **not** for sung vocals. See **Worked examples** in that reference for full lyrics + style samples.

## Layered explainer audio

VO + bed: TTS (`gemini-3.1-flash-tts`) for narration; Stable Audio for **instrumental** underscore only. When asked embed vs post: prefer **embed** in `p-video`; **post-mux** / **assembly** mix under VO is fallback only — [audio-post-production.md](./references/audio-post-production.md).

## Related skills

Install related skills when the job needs them:

| Skill | Description | Install |
| --- | --- | --- |
| `video-prompting` | Use when crafting video or motion prompts for any generative model — dramaturgy, camera, physics-safe motion, frame anchors, and clip chaining. | `npx skills add PrunaAI/pruna-skills@video-prompting -y` |
| `pruna-api` | Use before any Pruna or Replicate HTTP call — credentials, upload/poll/download, parallel batches, and agent safety. | `npx skills add PrunaAI/pruna-skills@pruna-api -y` |
| `video-editing` | Use when assembling or polishing already-rendered clips with ffmpeg — concat, crossfades, burned captions and subtitles, text/logo overlays, before/after sliders, background music beds, platform export — or when composing a multi-layer HTML combination video with Hyperframes. Not for AI video generation, prompt craft, or model-based video edits. | `npx skills add PrunaAI/pruna-skills@video-editing -y` |

## Pruna / Replicate tools

Matching install for every model named above. Pick what you need:

| Skill | Description | Install |
| --- | --- | --- |
| `gemini-3.1-flash-tts` | Use when someone needs spoken narration or voiceover — explainer tracks, documentary lines, or voice to pair with generated video. | `npx skills add PrunaAI/pruna-skills@gemini-3.1-flash-tts -y` |
| `music-2.5` | Use when someone wants an original AI song with vocals — sung lyrics, a style prompt track, or source audio for a music video. | `npx skills add PrunaAI/pruna-skills@music-2.5 -y` |
| `stable-audio-2.5` | Use when someone wants light instrumental background music — an ambient bed under dialogue or underscore for reels and explainers. | `npx skills add PrunaAI/pruna-skills@stable-audio-2.5 -y` |
| `whisperx` | Use when someone needs word-level timestamps from audio — lyric alignment, cut-safe line boundaries, or caption source timing before burn-in with video-editing. | `npx skills add PrunaAI/pruna-skills@whisperx -y` |
| `p-video` | Use when someone wants one short video clip from text or images — B-roll, start/end frame animation, or a quick motion shot. Not for full multi-scene films or lip-synced hosts. | `npx skills add PrunaAI/pruna-skills@p-video -y` |

Or install the full suite once: `npx skills add PrunaAI/pruna-skills@pruna -y`

