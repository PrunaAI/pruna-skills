---
name: p-image
description: Use when someone wants a fast AI image — product shots, hero visuals, mood boards, or draft photos from a text prompt.
license: MIT
metadata:
  version: "1.0.6"
  package: pruna-skills
  pruna_model: p-image
---

## Prerequisites

Install and load these skills before generating (skip if already in context via `@pruna`):

| Skill | Description | Install |
| --- | --- | --- |
| `generation-diversity` | Use when writing any generative prompt — ritual seed, explicit structure, scenario axes, and quality gates before paid API calls. | `npx skills add PrunaAI/pruna-skills@generation-diversity -y` |
| `image-prompting` | Use when crafting still-image prompts for any generative model — composition, identity sheets, edits, try-on, and photoreal personas. | `npx skills add PrunaAI/pruna-skills@image-prompting -y` |
| `pruna-api` | Use before any Pruna or Replicate HTTP call — credentials, upload/poll/download, parallel batches, and agent safety. | `npx skills add PrunaAI/pruna-skills@pruna-api -y` |

Or install the full suite once: `npx skills add PrunaAI/pruna-skills@pruna -y`

Follow each skill's **Before generating** / craft sections — do not restate guide content here.

## When NOT to use

Use a different skill instead:

| Skill | Description | Install |
| --- | --- | --- |
| `p-image-edit` | Use when someone wants to edit an existing photo — change outfits or backgrounds, compose from reference images, or apply prompt-driven edits. | `npx skills add PrunaAI/pruna-skills@p-image-edit -y` |
| `p-image-try-on` | Use when someone wants virtual try-on — dress a person in clothes from reference photos for fashion or ecommerce. | `npx skills add PrunaAI/pruna-skills@p-image-try-on -y` |

## HTTP (curl)

### Create (async — recommended)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-image' \
  -d '{
    "input": {
      "prompt": "Disco ball reflections on an otter DJ scratching vinyl at a packed 1970s roller rink, fish-eye lens, glitter confetti mid-air, funky energy",
      "aspect_ratio": "9:16"
    }
  }'
```

Poll and download: follow `pruna-api`.

Complete the random seed ritual from `generation-diversity` before writing prompts — **do not** pass the ritual string as API `seed`. Optional `api_seed` only when the user requests reproducibility.

### Create (sync — quick test only)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-image' \
  -H 'Try-Sync: true' \
  -d '{"input":{"prompt":"Corgi cowboy lassoing a runaway taco truck through Monument Valley dust storm, pulp western poster energy, dynamic diagonal composition","aspect_ratio":"16:9"}}'
```

## Before generating

1. Complete Prerequisites guide reading order.
2. Confirm **`prompt`** and **`aspect_ratio`** with the user. Multi-example batches: different **`aspect_ratio`** per still.
3. **Pruna note:** `p-image` has **no prompt upsampling** — keep prompts concrete. Avoid dense readable typography.

## Required input

- `prompt` (string)

## Common optional fields

- `aspect_ratio`: `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`, `custom` (with `width` / `height` multiples of 16, 256–1440)
- `seed`, `lora_weights`, `lora_scale`, `hf_api_token`, `disable_safety_checker`

## Typical next steps

Common follow-ons after this skill:

| Skill | Description | Install |
| --- | --- | --- |
| `p-image-edit` | Use when someone wants to edit an existing photo — change outfits or backgrounds, compose from reference images, or apply prompt-driven edits. | `npx skills add PrunaAI/pruna-skills@p-image-edit -y` |
| `p-image-try-on` | Use when someone wants virtual try-on — dress a person in clothes from reference photos for fashion or ecommerce. | `npx skills add PrunaAI/pruna-skills@p-image-try-on -y` |
| `p-image-upscale` | Use when someone wants to upscale or sharpen an existing image for print, large crops, or higher-quality delivery. | `npx skills add PrunaAI/pruna-skills@p-image-upscale -y` |
| `p-video` | Use when someone wants one short video clip from text or images — B-roll, start/end frame animation, or a quick motion shot. Not for full multi-scene films or lip-synced hosts. | `npx skills add PrunaAI/pruna-skills@p-video -y` |
| `avatar-single-scene` | Use when someone wants one polished host-on-camera beat — a speaking person with intake and approval gates before generation. | `npx skills add PrunaAI/pruna-skills@avatar-single-scene -y` |
| `avatar-multi-scene` | Use when someone wants the same person hosting several clips — multi-segment UGC, comparison reels, or mixed speaking and animated scenes with continuity. | `npx skills add PrunaAI/pruna-skills@avatar-multi-scene -y` |

