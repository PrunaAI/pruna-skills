---
name: image-prompting
description: Use when crafting still-image prompts for any generative model — composition, identity sheets, edits, try-on, and photoreal personas.
license: MIT
metadata:
  version: "1.0.10"
  package: pruna-skills
---

# Image prompting

Vendor-neutral craft for **still-image** generation and editing. Works with Pruna `p-image` family, Flux, Midjourney, Ideogram, Stable Diffusion, and similar APIs.

## Install

| Skill | Description | Install |
| --- | --- | --- |
| `image-prompting` | Use when crafting still-image prompts for any generative model — composition, identity sheets, edits, try-on, and photoreal personas. | `npx skills add PrunaAI/pruna-skills@image-prompting -y` |
| `generation-diversity` | Use when writing any generative prompt — ritual seed, explicit structure, scenario axes, and quality gates before paid API calls. | `npx skills add PrunaAI/pruna-skills@generation-diversity -y` |

## When to use

- Writing photo generation prompts
- Building character identity / turnaround sheets
- Surgical edits (change/keep discipline)
- Virtual try-on garment prompts
- Photoreal or stylized persona plates for avatars

## Works with

Pruna `p-image` (simple quick photos), `p-image-ideogram` (controlled photo generation — text, JSON, hex/bbox), `p-image-edit` / `p-image-try-on` / `p-image-upscale`, Flux, Midjourney, Ideogram, SDXL, and other still models.

## When NOT to use

Use a different skill instead:

| Skill | Description | Install |
| --- | --- | --- |
| `video-prompting` | Use when crafting video or motion prompts for any generative model — dramaturgy, camera, physics-safe motion, frame anchors, and clip chaining. | `npx skills add PrunaAI/pruna-skills@video-prompting -y` |
| `audio-prompting` | Use when crafting TTS, music, or bed prompts for any generative audio model — director style, song structure, and post-production layering. | `npx skills add PrunaAI/pruna-skills@audio-prompting -y` |
| `pruna-api` | Use before any Pruna or Replicate HTTP call — credentials, upload/poll/download, parallel batches, and agent safety. | `npx skills add PrunaAI/pruna-skills@pruna-api -y` |
| `p-image` | Use when someone explicitly wants the fastest, cheapest photo generation — mood boards, bulk panels, or quick iterations — not when controlled photoreal or in-image text is needed. | `npx skills add PrunaAI/pruna-skills@p-image -y` |

## Guide habit

In the **first reply**, name `` `image-prompting` `` in backticks. When aspect, resolution, or media source are open, open intake → **`generation-diversity`** clarification intake. For Pruna still calls, cite the reading order: `generation-diversity` (ritual + **still-image prompt flow** reference) → golden rules → model-specific reference below.

## Before generating

1. Follow `generation-diversity` first — for `p-image-ideogram` / `p-image` / `p-image-edit`, run **still-image prompt flow** (brief lock → ritual → draft → fidelity check).
2. **[Prompt golden rules](./references/prompt-golden-rules.md)** — positive framing, no banned filler, params outside the prompt string.
3. Same character across shots → [character-turnaround-sheet.md](./references/character-turnaround-sheet.md).
4. Edits → [p-image-edit-prompting.md](./references/p-image-edit-prompting.md).
5. Try-on → [p-image-try-on-prompting.md](./references/p-image-try-on-prompting.md).
6. Upscale params → [p-image-upscale-guidance.md](./references/p-image-upscale-guidance.md).
7. Photoreal personas → [realistic-persona-showcase.md](./references/realistic-persona-showcase.md) · [realistic-persona-example-prompt.md](./references/realistic-persona-example-prompt.md).
8. Validate with the matching `*-quality-checklist.md` in `./references/`.

Complex edits and multi-ref composition: see **Worked example — three-reference composite** in [p-image-edit-prompting.md](./references/p-image-edit-prompting.md).

## Pruna tools

Matching install for every model named above. Pick what you need:

| Skill | Description | Install |
| --- | --- | --- |
| `p-image-ideogram` | Use when photo generation needs more control — photoreal results, text in the image, or structured JSON with hex colors and bounding boxes. Simpler photo generation, edits, and video use other skills in the suite. | `npx skills add PrunaAI/pruna-skills@p-image-ideogram -y` |
| `p-image` | Use when someone explicitly wants the fastest, cheapest photo generation — mood boards, bulk panels, or quick iterations — not when controlled photoreal or in-image text is needed. | `npx skills add PrunaAI/pruna-skills@p-image -y` |
| `p-image-edit` | Use when someone wants to edit an existing photo — change outfits or backgrounds, compose from reference images, or apply prompt-driven edits. | `npx skills add PrunaAI/pruna-skills@p-image-edit -y` |
| `p-image-try-on` | Use when someone wants virtual try-on — dress a person in clothes from reference photos for fashion or ecommerce. | `npx skills add PrunaAI/pruna-skills@p-image-try-on -y` |
| `p-image-upscale` | Use when someone wants to upscale or sharpen an existing image for print, large crops, or higher-quality delivery. | `npx skills add PrunaAI/pruna-skills@p-image-upscale -y` |
| `pruna-api` | Use before any Pruna or Replicate HTTP call — credentials, upload/poll/download, parallel batches, and agent safety. | `npx skills add PrunaAI/pruna-skills@pruna-api -y` |

Or install the full suite once: `npx skills add PrunaAI/pruna-skills@pruna -y`

