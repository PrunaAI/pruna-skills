---
name: p-image
description: Use when someone explicitly wants the fastest, cheapest photo generation — mood boards, bulk panels, or quick iterations — not when controlled photoreal or in-image text is needed.
license: MIT
metadata:
  version: "1.0.10"
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

## Agent habit

**Routing:** Use `` `p-image` `` for **simple, quick** photo generation from a short prompt. When photo generation needs **more control** (text in the image, structured JSON with hex/bbox, high-detail photoreal), use `` `p-image-ideogram` `` (defaults **`thinking: high`**, **`prompt_upsampling: true`**; **`low`** + **`prompt_upsampling: false`** + explicit prompt for a faster pass on the same model). For edits or video, use `` `p-image-edit` `` or `` `p-video` `` — not a new photo generation re-roll.

In the **first reply**, name `` `p-image` `` in backticks, confirm `PRUNA_API_KEY` is set (or stop with signup links from `pruna-api`), then ask for prompt / aspect ratio (open intake → **`generation-diversity`** clarification intake). When drafting the prompt, follow **Prompt craft (dynamic + faithful)** — do not paste skill examples.

## Prompt craft (dynamic + faithful)

Every `input.prompt` must be **fresh and specific**, and must **keep the user's request**. Diversity never overrides the brief.

| Do | Don't |
| --- | --- |
| Run the `generation-diversity` random seed ritual; state it; rotate ≥2 free axes (camera, lighting, setting texture, render category) | Copy curl examples from this skill (`otter DJ`, `corgi cowboy`, …) or reuse a prior session's prompt |
| Lock user-required facts first (subject, product, brand cues, must-keep props, readable text if asked) | Swap the subject for a “cooler” scene that ignores the request |
| Expand with concrete nouns, frozen action, materials, placement (`image-prompting` golden rules) | Vague mood-only strings (`cool product vibe, neon`) |
| Show the drafted prompt + `aspect_ratio` before `POST` when the user has not locked wording | Silent regen with a different subject than approved |

**Fidelity check (before pay):** if you remove the user’s named subject/product/setting from the prompt, the job is wrong — rewrite. Free axes only fill what the brief left open.

When showing a drafted prompt, still name `` `p-image` `` (guides help craft; this tool owns the call).

**Pruna note:** `p-image` has **no prompt upsampling** — concrete language is the whole craft. Avoid dense readable typography unless the user explicitly asked for copy on a surface.

## When NOT to use

Use a different skill instead:

| Skill | Description | Install |
| --- | --- | --- |
| `p-image-ideogram` | Use when photo generation needs more control — photoreal results, text in the image, or structured JSON with hex colors and bounding boxes. Simpler photo generation, edits, and video use other skills in the suite. | `npx skills add PrunaAI/pruna-skills@p-image-ideogram -y` |
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

## Generation flow

Follow `generation-diversity` **still-image prompt flow** every time:

1. **Lock brief** — user subject, product, format, any copy-on-surface.
2. **Ritual seed** — fresh string; derive free axes (camera, lighting, `render_category_tag`, **`aspect_ratio`** when unset).
3. **Draft explicit prompt** — **Prompt craft (dynamic + faithful)** + `image-prompting` golden rules; **fidelity check** before pay.
4. **Confirm** — show `prompt` + `aspect_ratio` unless wording is locked.
5. **POST** — async curl below; poll via `pruna-api`; run `p-image` quality checklist before upscale/video.

**Aspect ratio:** pass `aspect_ratio` in `input`; if output dimensions do not match (e.g. asked `16:9`, got portrait), retry once with explicit `horizontal wide` / `vertical` wording in the prompt.

**Mood board / batch:** new ritual per independent still; different **`aspect_ratio`** per panel when format not locked.

**Photo approved → edit:** hand off to `p-image-edit` on the output URL — do not run photo generation again for the same subject.

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

