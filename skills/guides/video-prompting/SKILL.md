---
name: video-prompting
description: Use when crafting video or motion prompts for any generative model — dramaturgy, camera, physics-safe motion, frame anchors, and clip chaining.
license: MIT
metadata:
  version: "1.0.12"
  package: pruna-skills
---

# Video prompting

Vendor-neutral craft for **short video / motion** generation. Works with Pruna `p-video-2` / `p-video` family, Runway, Kling, Luma, Veo, and similar APIs.

## Install

| Skill | Description | Install |
| --- | --- | --- |
| `video-prompting` | Use when crafting video or motion prompts for any generative model — dramaturgy, camera, physics-safe motion, frame anchors, and clip chaining. | `npx skills add PrunaAI/pruna-skills@video-prompting -y` |
| `generation-diversity` | Use when writing any generative prompt — ritual seed, explicit structure, scenario axes, and quality gates before paid API calls. | `npx skills add PrunaAI/pruna-skills@generation-diversity -y` |

## When to use

- Text-to-video or image-to-video prompts
- Start/end frame (anchor pair) or narrated beat (anchor triple) specs
- Camera and lighting vocabulary in motion lines
- Physics-safe subject motion
- Multi-clip continuity / clip chaining
- Talking-head, motion-transfer, slot-replace, or instruction-based video-edit prompts

## Works with

Pruna `p-video-2` / `p-video` / `p-video-avatar` / `p-video-animate` / `p-video-replace` / `p-video-edit`, Runway Gen-3, Kling, Luma Dream Machine, Veo, and other video models. Best quality: `p-video-2`. Simpler clips: `p-video`.

## When NOT to use

Use a different skill instead:

| Skill | Description | Install |
| --- | --- | --- |
| `image-prompting` | Use when crafting still-image prompts for any generative model — composition, identity sheets, edits, try-on, and photoreal personas. | `npx skills add PrunaAI/pruna-skills@image-prompting -y` |
| `audio-prompting` | Use when crafting TTS, music, or bed prompts for any generative audio model — director style, song structure, and post-production layering. | `npx skills add PrunaAI/pruna-skills@audio-prompting -y` |
| `music-video` | Use when someone wants a full music video — original song or vocals, performance clips, B-roll, and lyric-synced edits. | `npx skills add PrunaAI/pruna-skills@music-video -y` |
| `narrated-multi-scene` | Use when someone wants a multi-part story with voiceover — episodic B-roll, chaptered promo, or several linked video scenes without on-camera dialogue. | `npx skills add PrunaAI/pruna-skills@narrated-multi-scene -y` |
| `p-video-2` | Use when someone wants the best-quality short clip from text, images, or audio — polished B-roll, start/end frame animation, or a motion shot with stronger lip-sync. Not for full multi-scene films or talking-head-only hosts. | `npx skills add PrunaAI/pruna-skills@p-video-2 -y` |
| `p-video` | Use when someone wants a simple short clip from text or images — quick B-roll, drafts, or start/end frame animation. Not when the brief needs the highest quality or tight lip-sync. | `npx skills add PrunaAI/pruna-skills@p-video -y` |
| `video-editing` | Use when assembling or polishing already-rendered clips with ffmpeg — concat, crossfades, burned captions and subtitles, text/logo overlays, before/after sliders, background music beds, platform export — or when composing a multi-layer HTML combination video with Hyperframes. Not for AI video generation, prompt craft, or model-based video edits. | `npx skills add PrunaAI/pruna-skills@video-editing -y` |

## Guide habit

In the **first reply**, name `` `video-prompting` `` in backticks. When aspect, resolution, duration, or embed-vs-post audio are open, open intake → **`generation-diversity`** clarification intake. For `p-video-2` / `p-video` motion lines, cite OPEN/MID/CLOSE dramaturgy and **Worked example — product B-roll** in [prompt-dramaturgy.md](./references/prompt-dramaturgy.md). Quality path: `p-video-2` (`p-video-2-prompting`). Simpler clips: `p-video`. Audio-led clips: **≤ ~19s** TTS before embed — see [audio-in-video-prompting.md](./references/audio-in-video-prompting.md).

## Before generating

1. Follow `generation-diversity` first.
2. Read in order:
   - [prompt-dramaturgy.md](./references/prompt-dramaturgy.md) — Details Law, OPEN/MID/CLOSE
   - [camera-lighting-vocabulary.md](./references/camera-lighting-vocabulary.md)
   - [physics-safe-motion.md](./references/physics-safe-motion.md)
   - [audio-in-video-prompting.md](./references/audio-in-video-prompting.md) when sound matters
   - [clip-chaining.md](./references/clip-chaining.md) for multi-clip continuity
   - [scene-anchor-pair.md](./references/scene-anchor-pair.md) / [scene-anchor-triple.md](./references/scene-anchor-triple.md) for frame (+ audio) payloads
3. Tool-specific craft when needed:
   - [p-video-2-prompting.md](./references/p-video-2-prompting.md)
   - [p-video-avatar-prompting.md](./references/p-video-avatar-prompting.md)
   - [p-video-animate-prompting.md](./references/p-video-animate-prompting.md)
   - [p-video-replace-prompting.md](./references/p-video-replace-prompting.md)
   - [p-video-edit-prompting.md](./references/p-video-edit-prompting.md)
4. Validate with the matching `*-quality-checklist.md` in `./references/`.

Product B-roll and OPEN/MID/CLOSE samples: **Worked example — product B-roll** in [prompt-dramaturgy.md](./references/prompt-dramaturgy.md).

## Pruna tools

Matching install for every model named above. Pick what you need:

| Skill | Description | Install |
| --- | --- | --- |
| `p-video-2` | Use when someone wants the best-quality short clip from text, images, or audio — polished B-roll, start/end frame animation, or a motion shot with stronger lip-sync. Not for full multi-scene films or talking-head-only hosts. | `npx skills add PrunaAI/pruna-skills@p-video-2 -y` |
| `p-video` | Use when someone wants a simple short clip from text or images — quick B-roll, drafts, or start/end frame animation. Not when the brief needs the highest quality or tight lip-sync. | `npx skills add PrunaAI/pruna-skills@p-video -y` |
| `p-video-avatar` | Use when someone wants a person on camera speaking a script — lip-synced host, spokesperson, or narrated avatar from a portrait photo. | `npx skills add PrunaAI/pruna-skills@p-video-avatar -y` |
| `p-video-animate` | Use when someone wants a photo to move like another video — motion transfer, dance remixes, or performance variations from a template clip. | `npx skills add PrunaAI/pruna-skills@p-video-animate -y` |
| `p-video-replace` | Use when someone wants to swap a person, outfit, or product inside existing footage while keeping the camera move and audio. | `npx skills add PrunaAI/pruna-skills@p-video-replace -y` |
| `p-video-edit` | Use when someone wants to edit an existing video with a text instruction — recolor, restyle, remove or add objects, change environment or lighting, update on-screen text, or apply optional reference-guided product and accessory edits. Not for a new clip from scratch or ffmpeg assembly. | `npx skills add PrunaAI/pruna-skills@p-video-edit -y` |
| `pruna-api` | Use before any Pruna or Replicate HTTP call — credentials, upload/poll/download, parallel batches, and agent safety. | `npx skills add PrunaAI/pruna-skills@pruna-api -y` |

Or install the full suite once: `npx skills add PrunaAI/pruna-skills@pruna -y`

