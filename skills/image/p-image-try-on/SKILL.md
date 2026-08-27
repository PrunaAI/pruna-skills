---
name: p-image-try-on
description: Use when someone wants virtual try-on — dress a person in clothes from reference photos for fashion or ecommerce.
license: MIT
metadata:
  version: "1.0.10"
  package: pruna-skills
  pruna_model: p-image-try-on
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

In the **first reply**, name `` `p-image-try-on` `` in backticks, confirm `PRUNA_API_KEY`, then ask for `person_image` + `garment_images`. Open intake → **`generation-diversity`** clarification intake when silent. When refs need disambiguation, draft with **Prompt craft (dynamic + faithful)** — do not paste skill examples. Redirect background-only / no-garment jobs to `p-image-edit`.

## Prompt craft (dynamic + faithful)

Identity and garments come from **`person_image`** + **`garment_images[]`**. Optional **`prompt`** only **disambiguates refs** — it does not invent a new person or outfit.

| Do | Don't |
| --- | --- |
| Lock **`person_image`** and every **`garment_images[]`** URL first; omit **`prompt`** on clean flat-lays | Describe a new scene, model, or garment the user did not supply |
| When refs are ambiguous: `the green t-shirt from image 1 and the trousers from image 2` (`image-prompting` try-on craft) | Mood-only prompts (`fashion editorial vibe`) or copy this skill's extended example when refs differ |
| Ritual seed before drafting disambiguation wording; vary phrasing when multiple valid mappings exist | Use **`prompt`** for background swaps — redirect to `p-image-edit` |
| Show **`prompt`** (if needed) before `POST` when refs are ambiguous | Silent try-on that changes pose, face, or garments beyond the brief |

**Fidelity check (before pay):** output must still be the user's person in the user's garment(s). If **`prompt`** could apply to a different ref set, rewrite the disambiguation.

## When NOT to use

Use a different skill instead:

| Skill | Description | Install |
| --- | --- | --- |
| `p-image` | Use when someone explicitly wants the fastest, cheapest photo generation — mood boards, bulk panels, or quick iterations — not when controlled photoreal or in-image text is needed. | `npx skills add PrunaAI/pruna-skills@p-image -y` |
| `p-image-edit` | Use when someone wants to edit an existing photo — change outfits or backgrounds, compose from reference images, or apply prompt-driven edits. | `npx skills add PrunaAI/pruna-skills@p-image-edit -y` |

## Pricing

Per generation (same for normal and turbo mode):

- **$0.015** for the first garment
- **$0.008** for each additional garment

Example: 3 garments → $0.015 + 2 × $0.008 = **$0.031**.

## Request shape

One **`person_image`**, one **`garment_images[]` entry per piece** (up to 11), optional **`reference_pose`**. The model auto-classifies each garment — **array order does not matter**. Mixed categories belong in **one call**.

- **`prompt`** — only when a reference shows multiple garments or is worn on-model; clean flat-lays need no prompt.
- **`preserve_input_size: true`** (default) — output dimensions follow the **person** image.

Runware field map: `person` → `person_image`, `garment` → `garment_images[]`, `pose` → `reference_pose`, `positivePrompt` → `prompt`, `settings.turbo` → `turbo`.

## HTTP (curl)

### Upload images

```bash
curl -X POST "https://api.pruna.ai/v1/files" \
  -H "apikey: ${PRUNA_API_KEY}" \
  -F "content=@/path/to/person.jpg"

curl -X POST "https://api.pruna.ai/v1/files" \
  -H "apikey: ${PRUNA_API_KEY}" \
  -F "content=@/path/to/garment.png"
```

Use each response `urls.get` in `input.person_image` and `input.garment_images[]`. Optional: `reference_pose`.

### Create (async — recommended)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-image-try-on' \
  -d '{
    "input": {
      "person_image": "https://api.pruna.ai/v1/files/PERSON_FILE_ID",
      "garment_images": ["https://api.pruna.ai/v1/files/GARMENT_FILE_ID"]
    }
  }'
```

Poll and download: follow `pruna-api`.

Complete the random seed ritual from `generation-diversity` before writing prompts — **do not** pass the ritual string as API `seed`.

### Create (sync — quick test only)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-image-try-on' \
  -H 'Try-Sync: true' \
  -d '{
    "input": {
      "person_image": "https://api.pruna.ai/v1/files/PERSON_FILE_ID",
      "garment_images": ["https://api.pruna.ai/v1/files/GARMENT_FILE_ID"]
    }
  }'
```

### Extended input (turbo + pose + prompt)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-image-try-on' \
  -d '{
    "input": {
      "person_image": "https://api.pruna.ai/v1/files/PERSON_FILE_ID",
      "garment_images": [
        "https://api.pruna.ai/v1/files/MULTI_GARMENT_SHOT_ID",
        "https://api.pruna.ai/v1/files/BOTTOM_ID"
      ],
      "reference_pose": "https://api.pruna.ai/v1/files/POSE_REF_ID",
      "prompt": "the green t-shirt from image 1 and the trousers from image 2",
      "turbo": true,
      "output_format": "jpg",
      "output_quality": 95,
      "preserve_input_size": true
    }
  }'
```

## Before generating

1. Complete Prerequisites guide reading order (`generation-diversity` → `image-prompting` try-on craft).
2. Ritual seed → draft optional **dynamic + faithful** disambiguation **`prompt`** (section above) → confirm **`person_image`**, **`garment_images`** (≤6 for finals; 7–8 usually lands; 9–11 may drop last items), and optional **`turbo`** / **`reference_pose`** / **`prompt`**.
3. **Pruna notes:** one item per body spot (socks + shoes → usually shoes win). **`turbo`** (~2.5–3.5 s) is off by default — not recommended above ~4 garments for finals. Full-body or three-quarter person crops work best. Omit gloves, mittens, handheld props, pocket squares, suspenders, brooches from `garment_images[]`.

## Required input

- `person_image` (string URL)
- `garment_images` (array of string URLs, up to **11**)

## Common optional fields

- `seed`, `output_format` (`webp` / `jpg` / `png`, default `jpg`), `output_quality` (0–100, default 95)
- `preserve_input_size` (boolean, default `true`)
- `turbo` (boolean, default `false`)
- `reference_pose` (person image URL)
- `prompt` (EXPERIMENTAL — disambiguate non-flatlay / multi-garment refs)

## Typical next steps

Common follow-ons after this skill:

| Skill | Description | Install |
| --- | --- | --- |
| `p-image-upscale` | Use when someone wants to upscale or sharpen an existing image for print, large crops, or higher-quality delivery. | `npx skills add PrunaAI/pruna-skills@p-image-upscale -y` |
| `p-video` | Use when someone wants one short video clip from text or images — B-roll, start/end frame animation, or a quick motion shot. Not for full multi-scene films or lip-synced hosts. | `npx skills add PrunaAI/pruna-skills@p-video -y` |
| `p-video-avatar` | Use when someone wants a person on camera speaking a script — lip-synced host, spokesperson, or narrated avatar from a portrait photo. | `npx skills add PrunaAI/pruna-skills@p-video-avatar -y` |

