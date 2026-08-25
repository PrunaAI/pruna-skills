---
name: generation-diversity
description: Use when writing any generative prompt — ritual seed, explicit structure, scenario axes, and quality gates before paid API calls.
license: MIT
metadata:
  version: "1.0.10"
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

## Guide habit

In the **first reply**, name `` `generation-diversity` `` in backticks. When the brief leaves media source, brand, audio, structure, resolution, or approval unclear, **[ask before spending](./references/clarification-intake.md)** — every tool and workflow defers here for shared intake topics. For still-image jobs (`p-image`, `p-image-edit`), point agents at **[Still-image prompt flow](./references/still-image-prompt-flow.md)** — brief lock → ritual → axes → explicit prompt → fidelity check. **Mood boards:** new ritual per independent panel; user-locked brand hex / subject stays locked on every panel.

## Before generating

0. **[Clarification intake](./references/clarification-intake.md)** — generate vs existing assets, colors, narration/VO, music, captions, aspect/resolution (720p/1080p, canvas, MP), structure, approval (unless the user waived or already locked answers).
1. **[Generation diversity](./references/generation-diversity.md)** — random seed ritual (SSoT), explicit prompt structure, rotate ≥2 scenario axes per session.
2. **Still images (`p-image` family):** **[still-image-prompt-flow.md](./references/still-image-prompt-flow.md)** — generation flow, edit flow, mood-board rules, hero → edit handoff. Pair with `image-prompting` golden rules and edit craft.
3. **[Quality checklists](./references/generation-quality-checklists.md)** — open outputs and judge pass/fail before the next paid step.
4. **Workflows:** [workflow-feedback-gates.md](./references/workflow-feedback-gates.md) — pause at plan / stills / clips before paid video.

## Red flags

Stop and ask (or show assets) before the next paid step if any of these are true:

| Red flag | Required action |
| --- | --- |
| User says skip review / burn video credits / run everything now | Refuse same-turn plan+video; require **approve plan** (then stills/clips) unless they explicitly ask for automation |
| Using `--yes-skip-*-gate` without the user requesting automation | Confirm explicitly before bypassing gates |
| Outputs not opened / checklist not run | Open the file; run the matching quality checklist before the next `POST` |
| Ritual seed skipped or copied from docs | Fresh random seed ritual first; do **not** pass the ritual string as API `seed` |

## Related skills

Install related skills when the job needs them:

| Skill | Description | Install |
| --- | --- | --- |
| `image-prompting` | Use when crafting still-image prompts for any generative model — composition, identity sheets, edits, try-on, and photoreal personas. | `npx skills add PrunaAI/pruna-skills@image-prompting -y` |
| `video-prompting` | Use when crafting video or motion prompts for any generative model — dramaturgy, camera, physics-safe motion, frame anchors, and clip chaining. | `npx skills add PrunaAI/pruna-skills@video-prompting -y` |
| `audio-prompting` | Use when crafting TTS, music, or bed prompts for any generative audio model — director style, song structure, and post-production layering. | `npx skills add PrunaAI/pruna-skills@audio-prompting -y` |
| `pruna-api` | Use before any Pruna or Replicate HTTP call — credentials, upload/poll/download, parallel batches, and agent safety. | `npx skills add PrunaAI/pruna-skills@pruna-api -y` |
| `p-image` | Use when someone explicitly wants the fastest, cheapest photo generation — mood boards, bulk panels, or quick iterations — not when controlled photoreal or in-image text is needed. | `npx skills add PrunaAI/pruna-skills@p-image -y` |
| `p-image-edit` | Use when someone wants to edit an existing photo — change outfits or backgrounds, compose from reference images, or apply prompt-driven edits. | `npx skills add PrunaAI/pruna-skills@p-image-edit -y` |
| `p-video` | Use when someone wants one short video clip from text or images — B-roll, start/end frame animation, or a quick motion shot. Not for full multi-scene films or lip-synced hosts. | `npx skills add PrunaAI/pruna-skills@p-video -y` |

Or install the full suite once: `npx skills add PrunaAI/pruna-skills@pruna -y`

