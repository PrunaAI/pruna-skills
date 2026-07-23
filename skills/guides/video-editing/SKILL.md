---
name: video-editing
description: Use when assembling or polishing already-rendered clips with ffmpeg — concat, crossfades, burned captions and subtitles, text/logo overlays, before/after sliders, background music beds, platform export — or when composing a multi-layer HTML combination video with Hyperframes. Not for AI video generation, prompt craft, or model-based video edits.
license: MIT
metadata:
  version: "@VERSION"
  package: pruna-skills
---

# Video editing

Vendor-neutral craft for **local post-production** on finished media. Works with any clips, stills, VO, or beds you already have — Pruna-generated or not.

**This skill is not AI video editing.** It does not write motion prompts, call `p-video`, or replace people in footage. Generate first with Pruna tools or workflows; assemble and polish here.

## Install

| Skill | Description | Install |
| --- | --- | --- |
| `video-editing` | Use when assembling or polishing already-rendered clips with ffmpeg — concat, crossfades, burned captions and subtitles, text/logo overlays, before/after sliders, background music beds, platform export — or when composing a multi-layer HTML combination video with Hyperframes. Not for AI video generation, prompt craft, or model-based video edits. | `npx skills add PrunaAI/pruna-skills@video-editing -y` |
| `generation-diversity` | Use when writing any generative prompt — ritual seed, explicit structure, scenario axes, and quality gates before paid API calls. | `npx skills add PrunaAI/pruna-skills@generation-diversity -y` |

## When to use

- Stitch multiple rendered clips (hard cut or crossfade)
- Burn in **phrase-bar + word-accent captions** (stable white line + purple spoken word, launch-style) or line-block subtitles on finished video
- Add title cards, lower-thirds, or logo watermarks
- Build before/after or side-by-side comparison clips
- Mix an instrumental bed under dialogue or VO (~20% default for launch/promo)
- Export for social aspect ratios (9:16, 1:1, 16:9) with loudness normalization
- Compose a **combination video** with UI chrome, chat mocks, or multi-panel layouts via [Hyperframes](https://github.com/heygen-com/hyperframes) (optional — see [combination-hyperframes.md](./references/combination-hyperframes.md))

## Works with

Any finished MP4/MOV/WebM plus local ffmpeg/ffprobe. Caption alignment via Replicate `whisperx`. Bed generation via `stable-audio-2.5`. Credentials and uploads via `pruna-api`.

## When NOT to use

Use a different skill instead:

| Skill | Description | Install |
| --- | --- | --- |
| `video-prompting` | Use when crafting video or motion prompts for any generative model — dramaturgy, camera, physics-safe motion, frame anchors, and clip chaining. | `npx skills add PrunaAI/pruna-skills@video-prompting -y` |
| `p-video` | Use when someone wants one short video clip from text or images — B-roll, start/end frame animation, or a quick motion shot. Not for full multi-scene films or lip-synced hosts. | `npx skills add PrunaAI/pruna-skills@p-video -y` |
| `p-video-avatar` | Use when someone wants a person on camera speaking a script — lip-synced host, spokesperson, or narrated avatar from a portrait photo. | `npx skills add PrunaAI/pruna-skills@p-video-avatar -y` |
| `p-video-animate` | Use when someone wants a photo to move like another video — motion transfer, dance remixes, or performance variations from a template clip. | `npx skills add PrunaAI/pruna-skills@p-video-animate -y` |
| `p-video-replace` | Use when someone wants to swap a person, outfit, or product inside existing footage while keeping the camera move and audio. | `npx skills add PrunaAI/pruna-skills@p-video-replace -y` |
| `p-image-edit` | Use when someone wants to edit an existing photo — change outfits or backgrounds, compose from reference images, or apply prompt-driven edits. | `npx skills add PrunaAI/pruna-skills@p-image-edit -y` |
| `music-video` | Use when someone wants a full music video — original song or vocals, performance clips, B-roll, and lyric-synced edits. | `npx skills add PrunaAI/pruna-skills@music-video -y` |
| `narrated-multi-scene` | Use when someone wants a multi-part story with voiceover — episodic B-roll, chaptered promo, or several linked video scenes without on-camera dialogue. | `npx skills add PrunaAI/pruna-skills@narrated-multi-scene -y` |

## Guide habit

In the **first reply**, name `` `video-editing` `` in backticks. Confirm inputs exist on disk (clips, optional bed, optional logo). Confirm **`ffmpeg`** / **`ffprobe`** are available. Do **not** call generative APIs from this skill unless the user explicitly needs a missing bed (`stable-audio-2.5`) or caption alignment (`whisperx`).

## Before assembling

Read in order for the task at hand:

1. [assembly-concat.md](./references/assembly-concat.md) — concat, normalize, mux
2. [transitions.md](./references/transitions.md) — `xfade` / `acrossfade`
3. [captions.md](./references/captions.md) — `whisperx` → phrase-bar + word-accent ASS (default) or line-block → burn-in
4. [overlays.md](./references/overlays.md) — `drawtext`, logo watermark
5. [comparison-sliders.md](./references/comparison-sliders.md) — side-by-side / before-after
6. [background-music.md](./references/background-music.md) — bed under VO
7. [combination-hyperframes.md](./references/combination-hyperframes.md) — HTML combo videos (optional)
8. [export-presets.md](./references/export-presets.md) — aspect ratios, loudnorm, web export

Bed **prompts** and embed-vs-post policy: `audio-prompting`.

## Combination videos (Hyperframes)

When the deliverable needs **designed frames** — chat UI mocks, kinetic type, multi-panel grids, product montages — install **`hyperframes`** (optional external — see [Related skills](#optional--combination-videos-external) below) and follow [combination-hyperframes.md](./references/combination-hyperframes.md).

**Pattern:** HyperFrames render (motion + VO, no burned captions) → post-render ffmpeg (whisperx → phrase-bar + word-accent burn → optional bed mux → export). See [captions.md](./references/captions.md) for caption craft.

## Related skills

Install related skills when the job needs them:

| Skill | Description | Install |
| --- | --- | --- |
| `whisperx` | Use when someone needs word-level timestamps from audio — lyric alignment, cut-safe line boundaries, or caption source timing before burn-in with video-editing. | `npx skills add PrunaAI/pruna-skills@whisperx -y` |
| `stable-audio-2.5` | Use when someone wants light instrumental background music — an ambient bed under dialogue or underscore for reels and explainers. | `npx skills add PrunaAI/pruna-skills@stable-audio-2.5 -y` |
| `gemini-3.1-flash-tts` | Use when someone needs spoken narration or voiceover — explainer tracks, documentary lines, or voice to pair with generated video. | `npx skills add PrunaAI/pruna-skills@gemini-3.1-flash-tts -y` |
| `audio-prompting` | Use when crafting TTS, music, or bed prompts for any generative audio model — director style, song structure, and post-production layering. | `npx skills add PrunaAI/pruna-skills@audio-prompting -y` |
| `pruna-api` | Use before any Pruna or Replicate HTTP call — credentials, upload/poll/download, parallel batches, and agent safety. | `npx skills add PrunaAI/pruna-skills@pruna-api -y` |

Or install the full suite once: `npx skills add PrunaAI/pruna-skills@pruna -y`

