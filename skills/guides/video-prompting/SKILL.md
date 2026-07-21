---
name: video-prompting
description: Use when crafting video or motion prompts for any generative model — dramaturgy, camera, physics-safe motion, frame anchors, and clip chaining.
license: MIT
metadata:
  version: "1.0.6"
  package: pruna-skills
---

# Video prompting

Vendor-neutral craft for **short video / motion** generation. Works with Pruna `p-video` family, Runway, Kling, Luma, Veo, and similar APIs.

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
- Talking-head, motion-transfer, or slot-replace instruction prompts

## Works with

Pruna `p-video` / `p-video-avatar` / `p-video-animate` / `p-video-replace`, Runway Gen-3, Kling, Luma Dream Machine, Veo, and other video models.

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
   - [p-video-avatar-prompting.md](./references/p-video-avatar-prompting.md)
   - [p-video-animate-prompting.md](./references/p-video-animate-prompting.md)
   - [p-video-replace-prompting.md](./references/p-video-replace-prompting.md)
4. Validate with the matching `*-quality-checklist.md` in `./references/`.

## Pruna tools

Matching install for every model named above. Pick what you need:

| Skill | Description | Install |
| --- | --- | --- |
| `p-video` | Use when someone wants one short video clip from text or images — B-roll, start/end frame animation, or a quick motion shot. Not for full multi-scene films or lip-synced hosts. | `npx skills add PrunaAI/pruna-skills@p-video -y` |
| `p-video-avatar` | Use when someone wants a person on camera speaking a script — lip-synced host, spokesperson, or narrated avatar from a portrait photo. | `npx skills add PrunaAI/pruna-skills@p-video-avatar -y` |
| `p-video-animate` | Use when someone wants a photo to move like another video — motion transfer, dance remixes, or performance variations from a template clip. | `npx skills add PrunaAI/pruna-skills@p-video-animate -y` |
| `p-video-replace` | Use when someone wants to swap a person, outfit, or product inside existing footage while keeping the camera move and audio. | `npx skills add PrunaAI/pruna-skills@p-video-replace -y` |
| `pruna-api` | Use before any Pruna or Replicate HTTP call — credentials, upload/poll/download, parallel batches, and agent safety. | `npx skills add PrunaAI/pruna-skills@pruna-api -y` |

Or install the full suite once: `npx skills add PrunaAI/pruna-skills@pruna -y`

