---
name: pruna
description: Use when installing the full Pruna generative media suite — all guides, tools, and workflows in one package.
license: MIT
metadata:
  version: "1.0.10"
  package: pruna-skills
depends:
  - generation-diversity
  - image-prompting
  - video-prompting
  - audio-prompting
  - video-editing
  - pruna-api
  - p-image
  - p-image-ideogram
  - p-image-edit
  - p-image-upscale
  - p-image-try-on
  - p-video
  - p-video-avatar
  - p-video-animate
  - p-video-replace
  - gemini-3.1-flash-tts
  - music-2.5
  - stable-audio-2.5
  - whisperx
  - image-to-video
  - narrated-multi-scene
  - visual-transition-reel
  - avatar-single-scene
  - avatar-multi-scene
  - interactive-explainer
  - music-video
  - illustrated-story-reel
---

# pruna

All Pruna generative media skills — **guides**, **tools**, and **workflows** — in one recommended install.

## Install

```bash
npx skills add PrunaAI/pruna-skills@pruna -y
```

After install, start a **new chat**. Your agent picks skills from the suite by name.

## What's included

### Guides

| Skill | Description | Install |
| --- | --- | --- |
| `generation-diversity` | Use when writing any generative prompt — ritual seed, explicit structure, scenario axes, and quality gates before paid API calls. | `npx skills add PrunaAI/pruna-skills@generation-diversity -y` |
| `image-prompting` | Use when crafting still-image prompts for any generative model — composition, identity sheets, edits, try-on, and photoreal personas. | `npx skills add PrunaAI/pruna-skills@image-prompting -y` |
| `video-prompting` | Use when crafting video or motion prompts for any generative model — dramaturgy, camera, physics-safe motion, frame anchors, and clip chaining. | `npx skills add PrunaAI/pruna-skills@video-prompting -y` |
| `audio-prompting` | Use when crafting TTS, music, or bed prompts for any generative audio model — director style, song structure, and post-production layering. | `npx skills add PrunaAI/pruna-skills@audio-prompting -y` |
| `video-editing` | Use when assembling or polishing already-rendered clips with ffmpeg — concat, crossfades, burned captions and subtitles, text/logo overlays, before/after sliders, background music beds, platform export — or when composing a multi-layer HTML combination video with Hyperframes. Not for AI video generation, prompt craft, or model-based video edits. | `npx skills add PrunaAI/pruna-skills@video-editing -y` |
| `pruna-api` | Use before any Pruna or Replicate HTTP call — credentials, upload/poll/download, parallel batches, and agent safety. | `npx skills add PrunaAI/pruna-skills@pruna-api -y` |

### Tools

| Skill | Description | Install |
| --- | --- | --- |
| `p-image` | Use when someone explicitly wants the fastest, cheapest photo generation — mood boards, bulk panels, or quick iterations — not when controlled photoreal or in-image text is needed. | `npx skills add PrunaAI/pruna-skills@p-image -y` |
| `p-image-ideogram` | Use when photo generation needs more control — photoreal results, text in the image, or structured JSON with hex colors and bounding boxes. Simpler photo generation, edits, and video use other skills in the suite. | `npx skills add PrunaAI/pruna-skills@p-image-ideogram -y` |
| `p-image-edit` | Use when someone wants to edit an existing photo — change outfits or backgrounds, compose from reference images, or apply prompt-driven edits. | `npx skills add PrunaAI/pruna-skills@p-image-edit -y` |
| `p-image-upscale` | Use when someone wants to upscale or sharpen an existing image for print, large crops, or higher-quality delivery. | `npx skills add PrunaAI/pruna-skills@p-image-upscale -y` |
| `p-image-try-on` | Use when someone wants virtual try-on — dress a person in clothes from reference photos for fashion or ecommerce. | `npx skills add PrunaAI/pruna-skills@p-image-try-on -y` |
| `p-video` | Use when someone wants one short video clip from text or images — B-roll, start/end frame animation, or a quick motion shot. Not for full multi-scene films or lip-synced hosts. | `npx skills add PrunaAI/pruna-skills@p-video -y` |
| `p-video-avatar` | Use when someone wants a person on camera speaking a script — lip-synced host, spokesperson, or narrated avatar from a portrait photo. | `npx skills add PrunaAI/pruna-skills@p-video-avatar -y` |
| `p-video-animate` | Use when someone wants a photo to move like another video — motion transfer, dance remixes, or performance variations from a template clip. | `npx skills add PrunaAI/pruna-skills@p-video-animate -y` |
| `p-video-replace` | Use when someone wants to swap a person, outfit, or product inside existing footage while keeping the camera move and audio. | `npx skills add PrunaAI/pruna-skills@p-video-replace -y` |
| `gemini-3.1-flash-tts` | Use when someone needs spoken narration or voiceover — explainer tracks, documentary lines, or voice to pair with generated video. | `npx skills add PrunaAI/pruna-skills@gemini-3.1-flash-tts -y` |
| `music-2.5` | Use when someone wants an original AI song with vocals — sung lyrics, a style prompt track, or source audio for a music video. | `npx skills add PrunaAI/pruna-skills@music-2.5 -y` |
| `stable-audio-2.5` | Use when someone wants light instrumental background music — an ambient bed under dialogue or underscore for reels and explainers. | `npx skills add PrunaAI/pruna-skills@stable-audio-2.5 -y` |
| `whisperx` | Use when someone needs word-level timestamps from audio — lyric alignment, cut-safe line boundaries, or caption source timing before burn-in with video-editing. | `npx skills add PrunaAI/pruna-skills@whisperx -y` |

### Workflows

| Skill | Description | Install |
| --- | --- | --- |
| `image-to-video` | Use when someone wants one short film beat from images — a narrated scene, story moment, or cinematic B-roll with optional voiceover. | `npx skills add PrunaAI/pruna-skills@image-to-video -y` |
| `narrated-multi-scene` | Use when someone wants a multi-part story with voiceover — episodic B-roll, chaptered promo, or several linked video scenes without on-camera dialogue. | `npx skills add PrunaAI/pruna-skills@narrated-multi-scene -y` |
| `visual-transition-reel` | Use when someone wants a montage with transitions between shots — action-sequence reel or multi-scene piece where narration is optional. | `npx skills add PrunaAI/pruna-skills@visual-transition-reel -y` |
| `avatar-single-scene` | Use when someone wants one polished host-on-camera beat — a speaking person with intake and approval gates before generation. | `npx skills add PrunaAI/pruna-skills@avatar-single-scene -y` |
| `avatar-multi-scene` | Use when someone wants the same person hosting several clips — multi-segment UGC, comparison reels, or mixed speaking and animated scenes with continuity. | `npx skills add PrunaAI/pruna-skills@avatar-multi-scene -y` |
| `interactive-explainer` | Use when someone wants an educational explainer with a host and characters — history or science shorts with dialogue, not voiceover-only B-roll. | `npx skills add PrunaAI/pruna-skills@interactive-explainer -y` |
| `music-video` | Use when someone wants a full music video — original song or vocals, performance clips, B-roll, and lyric-synced edits. | `npx skills add PrunaAI/pruna-skills@music-video -y` |
| `illustrated-story-reel` | Use when someone wants a slideshow story with narration or music — picture-book illustrated frames with Ken Burns or gentle p-video motion. | `npx skills add PrunaAI/pruna-skills@illustrated-story-reel -y` |

## Reading order

1. `generation-diversity` — ritual seed + QA before any paid call
2. Domain craft — `image-prompting` / `video-prompting` / `audio-prompting`
3. `pruna-api` — credentials, upload/poll/download
4. The **tool** skill for the API call
5. A **workflow** skill when the job is multi-step (agent runs curl + ffmpeg)

## Requirements

- `PRUNA_API_KEY` — https://dashboard.pruna.ai/ (see docs/api-setup.md)
- `REPLICATE_API_TOKEN` when using audio tools
- `curl`, `ffmpeg` / `ffprobe` for video assembly
