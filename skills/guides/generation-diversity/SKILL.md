---
name: generation-diversity
description: Use when writing any generative prompt — ritual seed, explicit structure, scenario axes, and quality gates before paid API calls.
license: MIT
metadata:
  version: "1.0.6"
  package: pruna-skills
---

# Generation diversity

Vendor-neutral playbook for **diverse, explicit prompts** and output QA. Apply before every generation on any model (Pruna, Flux, Midjourney, Runway, ElevenLabs, …).

## Install

| Skill | Description | Install |
| --- | --- | --- |
| `generation-diversity` | Use when writing any generative prompt — ritual seed, explicit structure, scenario axes, and quality gates before paid API calls. | `npx skills add PrunaAI/pruna-skills@generation-diversity -y` |

## When to use

- Starting a new image, video, or audio generation
- Outputs feel repetitive or “AI sloppy”
- Multi-example batches that need cast/setting/camera variety
- Before advancing a multi-step workflow past a phase gate

## Works with

Any generative model. Pruna tools (`p-image`, `p-video`, …) and third-party APIs alike.

## Before generating

1. **[Generation diversity](./references/generation-diversity.md)** — random seed ritual (SSoT), explicit prompt structure, rotate ≥2 scenario axes per session.
2. **[Quality checklists](./references/generation-quality-checklists.md)** — open outputs and judge pass/fail before the next paid step.
3. **Workflows:** [workflow-feedback-gates.md](./references/workflow-feedback-gates.md) — pause at plan / stills / clips before paid video.

## Related skills

Install related skills when the job needs them:

| Skill | Description | Install |
| --- | --- | --- |
| `image-prompting` | Use when crafting still-image prompts for any generative model — composition, identity sheets, edits, try-on, and photoreal personas. | `npx skills add PrunaAI/pruna-skills@image-prompting -y` |
| `video-prompting` | Use when crafting video or motion prompts for any generative model — dramaturgy, camera, physics-safe motion, frame anchors, and clip chaining. | `npx skills add PrunaAI/pruna-skills@video-prompting -y` |
| `audio-prompting` | Use when crafting TTS, music, or bed prompts for any generative audio model — director style, song structure, and post-production layering. | `npx skills add PrunaAI/pruna-skills@audio-prompting -y` |
| `pruna-api` | Use before any Pruna or Replicate HTTP call — credentials, upload/poll/download, parallel batches, and agent safety. | `npx skills add PrunaAI/pruna-skills@pruna-api -y` |
| `p-image` | Use when someone wants a fast AI image — product shots, hero visuals, mood boards, or draft photos from a text prompt. | `npx skills add PrunaAI/pruna-skills@p-image -y` |
| `p-video` | Use when someone wants one short video clip from text or images — B-roll, start/end frame animation, or a quick motion shot. Not for full multi-scene films or lip-synced hosts. | `npx skills add PrunaAI/pruna-skills@p-video -y` |

Or install the full suite once: `npx skills add PrunaAI/pruna-skills@pruna -y`

