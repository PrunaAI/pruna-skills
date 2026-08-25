---
name: p-image-edit
description: Use when someone wants to edit an existing photo — change outfits or backgrounds, compose from reference images, or apply prompt-driven edits.
license: MIT
metadata:
  version: "1.0.10"
  package: pruna-skills
  pruna_model: p-image-edit
---

## Prerequisites

Install and load these skills before generating (skip if already in context via `@pruna`):

| Skill | Description | Install |
| --- | --- | --- |
| `generation-diversity` | Use when writing any generative prompt — ritual seed, explicit structure, scenario axes, and quality gates before paid API calls. | `npx skills add PrunaAI/pruna-skills@generation-diversity -y` |
| `image-prompting` | Use when crafting still-image prompts for any generative model — composition, identity sheets, edits, try-on, and photoreal personas. | `npx skills add PrunaAI/pruna-skills@image-prompting -y` |
| `video-prompting` | Use when crafting video or motion prompts for any generative model — dramaturgy, camera, physics-safe motion, frame anchors, and clip chaining. | `npx skills add PrunaAI/pruna-skills@video-prompting -y` |
| `pruna-api` | Use before any Pruna or Replicate HTTP call — credentials, upload/poll/download, parallel batches, and agent safety. | `npx skills add PrunaAI/pruna-skills@pruna-api -y` |

Or install the full suite once: `npx skills add PrunaAI/pruna-skills@pruna -y`

Follow each skill's **Before generating** / craft sections — do not restate guide content here.

## Agent habit

In the **first reply**, name `` `p-image-edit` `` in backticks, confirm `PRUNA_API_KEY`, then ask for the source photo (and edit brief). Open intake → **`generation-diversity`** clarification intake when needed. Draft edits with **Prompt craft (dynamic + faithful)**. Redirect to `p-image-try-on` when the job is garment fit from packshots.

## Prompt craft (dynamic + faithful)

Edit prompts are **surgical** and **request-locked**. Change only what the user asked; keep everything else identical. Diversity applies to *how* you phrase the change — not to inventing a new scene.

| Do | Don't |
| --- | --- |
| Formula: `Change [specific thing]. Keep [identity / pose / lighting / background] identical.` (`image-prompting` edit craft) | `Make it better` / mood-only rewrites that ignore the brief |
| Name every **must-keep** from the user (face, outfit, pose, background, product) | Drop keep-clauses and hope the model preserves them |
| Fresh ritual seed from `generation-diversity` before drafting; vary free wording (materials, hex, camera nuance) when the brief allows | Copy this skill’s sample (`soft gradient`) when the user asked for something else |
| Point at refs when composing: `face from image 1, outfit from image 2` | Vague `combine these images` |
| Show the edit prompt before `POST` when wording is not locked | Silent edit that changes subject, species, age, or unrequested regions |

**Fidelity check (before pay):** the prompt must still satisfy the user’s change **and** every stated keep. If a keep is missing, add it. Do not “spice” the background/cast when they asked for a background-only swap.

## When NOT to use

Use a different skill instead:

| Skill | Description | Install |
| --- | --- | --- |
| `p-image` | Use when someone explicitly wants the fastest, cheapest photo generation — mood boards, bulk panels, or quick iterations — not when controlled photoreal or in-image text is needed. | `npx skills add PrunaAI/pruna-skills@p-image -y` |
| `p-image-try-on` | Use when someone wants virtual try-on — dress a person in clothes from reference photos for fashion or ecommerce. | `npx skills add PrunaAI/pruna-skills@p-image-try-on -y` |
| `p-image-upscale` | Use when someone wants to upscale or sharpen an existing image for print, large crops, or higher-quality delivery. | `npx skills add PrunaAI/pruna-skills@p-image-upscale -y` |

## HTTP (curl)

### Upload references

```bash
curl -X POST "https://api.pruna.ai/v1/files" \
  -H "apikey: ${PRUNA_API_KEY}" \
  -F "content=@/path/to/reference.png"
```

Use each response `urls.get` in `input.images`.

### Create (async — recommended)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-image-edit' \
  -d '{
    "input": {
      "prompt": "Change background to soft gradient, keep subject identical",
      "images": ["https://api.pruna.ai/v1/files/FILE_ID"],
      "aspect_ratio": "9:16"
    }
  }'
```

Poll and download: follow `pruna-api`.

Complete the random seed ritual from `generation-diversity` before writing prompts — **do not** pass the ritual string as API `seed`. Optional `seed` only when the user requests reproducibility.

### Create (sync — quick test only)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-image-edit' \
  -H 'Try-Sync: true' \
  -d '{
    "input": {
      "prompt": "Change background to soft gradient, keep subject identical",
      "images": ["https://api.pruna.ai/v1/files/FILE_ID"],
      "aspect_ratio": "9:16"
    }
  }'
```

## Edit flow

Follow `generation-diversity` **still-image prompt flow** (edit section):

1. **Lock change + keeps** — user’s surgical ask; formula in **Prompt craft (dynamic + faithful)**.
2. **Upload refs** — `POST /v1/files`; `urls.get` → `input.images` (1–5). Never invent file URLs.
3. **Ritual seed** → draft edit prompt (`image-prompting` edit craft) → **fidelity check** (every keep clause present).
4. **Confirm** — `prompt`, refs, **`aspect_ratio`**, **`turbo`** (off for hard edits).
5. **POST** — async curl below; checklist before upscale/video.

**Aspect ratio:** prefer `match_input_image` for edits; output should keep the plate aspect — if drift occurs, retry with the same ref URL and explicit keep clauses.

**Pruna note:** avatar pipelines — edit from locked **upscaled** hero URL; upscale again before `p-video*` — never pass raw edit URLs to video models.

**Not edit:** new subject from scratch → `p-image`. Garment fit from packshots → `p-image-try-on`.

**Multi-reference (up to 5):** index refs by role — e.g. three-reference composite: face from image 1, outfit from image 2, cafe from image 3; `turbo: false` for hard composites. Full pattern in `image-prompting` **p-image-edit-prompting**.

## Required input

- `prompt` (string)
- `images` (array of 1–5 URLs, typically `https://api.pruna.ai/v1/files/{id}`)

## Common optional fields

- `aspect_ratio`: `match_input_image`, `1:1`, `16:9`, `9:16`, etc.
- `turbo` (boolean, default true; turn off for harder edits)
- `seed`, `disable_safety_checker`

## Typical next steps

Common follow-ons after this skill:

| Skill | Description | Install |
| --- | --- | --- |
| `p-image-upscale` | Use when someone wants to upscale or sharpen an existing image for print, large crops, or higher-quality delivery. | `npx skills add PrunaAI/pruna-skills@p-image-upscale -y` |
| `p-video` | Use when someone wants one short video clip from text or images — B-roll, start/end frame animation, or a quick motion shot. Not for full multi-scene films or lip-synced hosts. | `npx skills add PrunaAI/pruna-skills@p-video -y` |
| `p-video-avatar` | Use when someone wants a person on camera speaking a script — lip-synced host, spokesperson, or narrated avatar from a portrait photo. | `npx skills add PrunaAI/pruna-skills@p-video-avatar -y` |
| `avatar-multi-scene` | Use when someone wants the same person hosting several clips — multi-segment UGC, comparison reels, or mixed speaking and animated scenes with continuity. | `npx skills add PrunaAI/pruna-skills@avatar-multi-scene -y` |
| `narrated-multi-scene` | Use when someone wants a multi-part story with voiceover — episodic B-roll, chaptered promo, or several linked video scenes without on-camera dialogue. | `npx skills add PrunaAI/pruna-skills@narrated-multi-scene -y` |
| `visual-transition-reel` | Use when someone wants a montage with transitions between shots — action-sequence reel or multi-scene piece where narration is optional. | `npx skills add PrunaAI/pruna-skills@visual-transition-reel -y` |

