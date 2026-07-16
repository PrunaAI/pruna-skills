---
name: p-image-try-on
description: Use when the user wants virtual try-on, dress a person in clothing from reference photos, garment fitting on a model still, or ecommerce fashion compositing.
license: MIT
metadata:
  version: "1.0.1"
  pruna_model: p-image-try-on
---

# p-image-try-on (Pruna)

Virtually fit one or more garments onto a person's photo. **Rate limit:** 500 requests/minute · **Category:** Image Editing.

The model's strength is **garment-only editing** — identity, pose, hair, background, and scene props stay intact. That supports **editorial fashion**, **complex prints / patchwork**, and **multi-garment stacks**, not just simple flat-lay tee swaps.

Canonical API reference: [p-image-try-on model docs](https://docs.api.pruna.ai/guides/models/p-image-try-on) · operational guide (Runware host): [virtual try-on](https://runware.ai/docs/models/prunaai-p-image-try-on/guides/virtual-try-on)

**Showcase quality bar:** [realistic-persona-showcase.md](../../../references/shared/realistic-persona-showcase.md) · try-on checklist: [p-image-try-on-quality-checklist.md](../../../references/image/p-image-try-on-quality-checklist.md) · examples: [example-prompt.md](./example-prompt.md)

Shared HTTP patterns: [pruna-api.md](../../../references/shared/pruna-api.md) (upload, [poll](#poll), [download](#download))

## Pricing

Per generation (same for normal and turbo mode):

- **$0.015** for the first garment
- **$0.008** for each additional garment

Example: 3 garments → $0.015 + 2 × $0.008 = **$0.031**.

## Request shape

One **`person_image`**, one **`garment_images[]` entry per piece** (up to 11), optional **`reference_pose`**. The model auto-classifies each garment — **array order does not matter** and you do not tag hat vs shoe. No composite garment image required; mixed categories (headwear + top + shoes + bag) belong in **one call**.

- **`prompt`** — only when a reference shows multiple garments or is worn on-model; clean flat-lays need no prompt.
- **`preserve_input_size: true`** (default) — output dimensions follow the **person** image.

Runware field map (same model, different host): `person` → `person_image`, `garment` → `garment_images[]`, `pose` → `reference_pose`, `positivePrompt` → `prompt`, `settings.turbo` → `turbo`.

## HTTP (curl)

Follow the [official quickstart](https://docs.api.pruna.ai/guides/models/p-image-try-on#quickstart): upload files, then call `POST /v1/predictions` with `Model: p-image-try-on`.

### Start with uploading your images

```bash
# Upload person photo
curl -X POST "https://api.pruna.ai/v1/files" \
  -H "apikey: ${PRUNA_API_KEY}" \
  -F "content=@/path/to/person.jpg"

# Upload garment image (repeat for each garment file)
curl -X POST "https://api.pruna.ai/v1/files" \
  -H "apikey: ${PRUNA_API_KEY}" \
  -F "content=@/path/to/garment.png"
```

Use `-F` (form) with `@` to upload from disk. Use each response `urls.get` in `input.person_image` and `input.garment_images[]`.

Optional uploads for extended fields: `reference_pose` (pose reference person image).

### Try On (Synchronous)

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

### Try On (Asynchronous)

Omit `Try-Sync` for production reliability; poll until `succeeded`:

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

Poll and download: [pruna-api.md](../../../references/shared/pruna-api.md#poll).

## Parameters

Tables follow the [official model page](https://docs.api.pruna.ai/guides/models/p-image-try-on#parameters). Extended fields (`turbo`, `reference_pose`, `prompt`) are listed below.

### Required

| Parameter | Type | Description |
|-----------|------|-------------|
| `person_image` | string | Image URL of the person to edit |
| `garment_images` | array of string | Up to **11** garment refs; **≤6** for reliable finals, **7–8** often lands all pieces, **9–11** may drop the last item(s); extra URLs beyond 11 are ignored |

### Optional

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `seed` | integer | — | Random seed. Leave blank for a random seed. |
| `output_format` | string | `jpg` | Format of the saved output image (`webp`, `jpg`, `png`). |
| `output_quality` | integer | `95` | Quality for jpg/webp outputs from 0 to 100. |
| `preserve_input_size` | boolean | `true` | Output matches **person_image** dimensions (model resizes internally). |

### Extended optional fields

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `turbo` | boolean | `false` | Faster multi-garment pass (~2.5–3.5 s); see [Turbo mode](#turbo-mode) |
| `reference_pose` | string | — | Optional person image URL; output pose matches this reference |
| `prompt` | string | — | **EXPERIMENTAL.** For non-flatlay garment images; names which garment to use from which image, e.g. `"the green t-shirt from image 1 and the trousers from image 2"` |

## Before generating

1. **[Generation diversity](../../../references/shared/generation-diversity.md)** — random seed ritual (SSoT) + axis rotation before each try-on job (reuse approved hero plate URL when dressing an approved plate).
2. Confirm with the user:

- **`person_image`** — person photo with clear visibility of the body region to dress
- **`garment_images`** — up to **11** refs (**≤6** finals; **7–8** reliable; one item per body spot — see [Multi-garment limits](#multi-garment-limits))
- **`turbo`**, **`reference_pose`**, **`prompt`** when relevant (see sections below)
- **`seed`**, **`output_format`**, **`output_quality`**, **`preserve_input_size`** when delivery format matters

Run [p-image-try-on-quality-checklist.md](../../../references/image/p-image-try-on-quality-checklist.md) on outputs before downstream steps.

## Production quality (not basic demos)

**Upstream person plate:** try-on fidelity is capped by **`person_image`**. Follow [realistic-persona-showcase.md](../../../references/shared/realistic-persona-showcase.md) for photoreal **`p-image`** plates — not generic catalog mannequins. Garment tiers: see **Showcase tiers** below and [p-image-try-on-quality-checklist.md](../../../references/image/p-image-try-on-quality-checklist.md).

**Showcase tiers to plan for:**

| Tier | Example capability |
|------|-------------------|
| Editorial still | Artistic prints, color-block sleeves, seated lifestyle poses |
| Complex garments | Collaged / patchwork suits, fine pleats, multi-panel streetwear |
| In-scene accessories | Hats, logo tees, glasses — mirror/street compositions preserved |
| Multi-garment stack | Jacket + tee + pants + hat + shoes in one pass (normal mode; plan ≤6 for finals) |

**Anti-slop:** avoid white-background-only demos, mushy AI person plates, turbo-only finals on complex stacks, and repeating one default face across examples. Rotate cast and settings per [visual-variety-bible.md](../../../references/shared/visual-variety-bible.md).

**Replicate playground:** diversify pinned examples on [p-image-try-on](https://replicate.com/prunaai/p-image-try-on) per [realistic-persona-showcase.md](../../../references/shared/realistic-persona-showcase.md).

## Garment inputs

The model accepts a broader range of garment images than flat-lay packshots alone:

| Input type | Notes |
|------------|--------|
| **Flat-lay / packshot** | Best default; no `prompt` needed |
| **On-model / lifestyle** | Supported; use `prompt` to identify the garment |
| **Multi-garment in one image** | Supported; use `prompt` to pick which items to apply |

When a garment image shows multiple items or the garment is worn by someone else, set **`prompt`** to disambiguate (EXPERIMENTAL).

## Multi-garment limits

| Rule | Guidance |
|------|----------|
| **One item per body spot** | Socks + shoes on the feet → expect **one** winner (usually shoes). Send socks alone if you need them. |
| **Reliable count** | **≤6** for delivery assets; **7–8** usually lands; **9–11** treat extras as bonus — last pieces not guaranteed. |
| **Restyling** | Fix person + base garments; swap **one** `garment_images[]` URL and rerun for variant tops (catalog A/B). |

**Person image:** full-body or three-quarter works best — the model needs the body region to dress. Tight crops can artifact.

## Garment categories

The model auto-classifies each garment image. Misclassified or unsupported refs may be **skipped** (run can still succeed) — **omit** known-bad types from `garment_images[]` rather than hoping they drop.

**Works well:** tops and shirts; sweaters, hoodies, and blazers; pants, jeans, shorts, and skirts; dresses, jumpsuits, and rompers; jackets and coats; underwear and swimwear; **footwear** (shoes, boots, sandals, socks — person photo must show feet); **headwear** (hats, caps, beanies, sunglasses, eyeglasses); **neckwear** (scarves, ties, necklaces); **bags** (handbags, totes, backpacks); **select jewelry** (watches, bracelets, rings, earrings).

**Omit from request:** gloves and mittens; arm warmers; handheld props (phones, wallets, umbrellas, cups, keychains); pocket squares, suspenders, and brooches.

## Turbo mode

Turbo applies multiple garment edits in **one larger edit** instead of processing garments separately.

| | Normal (default) | Turbo (`turbo: true`) |
|--|------------------|------------------------|
| **Speed** | Scales with garment count | ~**2.5–3.5 s** regardless of garment count |
| **Quality** | Highest fidelity | May be slightly lower; some garments may not apply correctly |
| **Pricing** | Per-garment table above | **Same** pricing |
| **Best for** | Final assets, **5+ garments** | Previews, batch catalogs, speed-critical flows (**~4 pieces** sweet spot) |

**Guidance:**

- Turbo is **disabled by default** — enable explicitly when the user prioritizes latency.
- Same price as normal; works with `reference_pose`, `prompt`, etc.
- Pruna docs: **not recommended above ~4 garments** in turbo — use normal mode for larger stacks and final delivery.

## Example: extended input (turbo + pose + prompt)

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

## Typical next steps

- **Restyle one piece:** keep `person_image` + unchanged garments; swap a single `garment_images[]` URL per variant.
- Upscale for delivery: [p-image-upscale](../p-image-upscale/SKILL.md)
- Animate try-on still: [p-video](../../video/p-video/SKILL.md) (I2V) or [p-video-avatar](../../video/p-video-avatar/SKILL.md)
- Ecommerce pack workflows: [pruna-generative-pipeline](../../../workflows/router/pruna-generative-pipeline/SKILL.md) recipe K
