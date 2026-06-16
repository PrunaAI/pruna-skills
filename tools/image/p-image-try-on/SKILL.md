---
name: p-image-try-on
description: Use when the user asks for virtual try-on, garment fitting, dressing a person photo in clothing, or p-image-try-on API usage.
license: MIT
metadata:
  version: "0.0.1"
  pruna_model: p-image-try-on
---

# p-image-try-on (Pruna)

Virtually fit one or more garments onto a person's photo. **Rate limit:** 500 requests/minute · **Category:** Image Editing.

Canonical API reference: [p-image-try-on model docs](https://docs.api.pruna.ai/guides/models/p-image-try-on)

Shared HTTP patterns: [references/shared/pruna-api.md](../../../references/shared/pruna-api.md) (upload, [poll](#poll), [download](#download))

## Pricing

Per generation (same for normal and turbo mode):

- **$0.015** for the first garment
- **$0.008** for each additional garment

Example: 3 garments → $0.015 + 2 × $0.008 = **$0.031**.

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
| `garment_images` | array of string | Up to **11** garment reference images (**≤6 recommended**); extra URLs beyond 11 are ignored |

### Optional

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `seed` | integer | — | Random seed. Leave blank for a random seed. |
| `output_format` | string | `jpg` | Format of the saved output image (`webp`, `jpg`, `png`). |
| `output_quality` | integer | `95` | Quality for jpg/webp outputs from 0 to 100. |
| `preserve_input_size` | boolean | `true` | Resize the final result back to the capped person image size. |

### Extended optional fields

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `turbo` | boolean | `false` | Faster multi-garment pass (~2.5–3.5 s); see [Turbo mode](#turbo-mode) |
| `reference_pose` | string | — | Optional person image URL; output pose matches this reference |
| `prompt` | string | — | **EXPERIMENTAL.** For non-flatlay garment images; names which garment to use from which image, e.g. `"the green t-shirt from image 1 and the trousers from image 2"` |

## Before generating

Confirm with the user:

- **`person_image`** — person photo with clear visibility of the body region to dress
- **`garment_images`** — up to **11** refs (**≤6 recommended**)
- **`turbo`**, **`reference_pose`**, **`prompt`** when relevant (see sections below)
- **`seed`**, **`output_format`**, **`output_quality`**, **`preserve_input_size`** when delivery format matters

Run [p-image-try-on-quality-checklist.md](../../../references/image/p-image-try-on-quality-checklist.md) on outputs before downstream steps.

## Garment inputs

The model accepts a broader range of garment images than flat-lay packshots alone:

| Input type | Notes |
|------------|--------|
| **Flat-lay / packshot** | Best default; no `prompt` needed |
| **On-model / lifestyle** | Supported; use `prompt` to identify the garment |
| **Multi-garment in one image** | Supported; use `prompt` to pick which items to apply |

When a garment image shows multiple items or the garment is worn by someone else, set **`prompt`** to disambiguate (EXPERIMENTAL).

## Garment categories

The model auto-classifies each garment image. Unsupported types are skipped (the run may still succeed with the remaining garments).

**Works well:** tops and shirts; sweaters, hoodies, and blazers; pants, jeans, shorts, and skirts; dresses, jumpsuits, and rompers; jackets and coats; underwear and swimwear; **footwear** (shoes, boots, sandals, socks — person photo must show feet); **headwear** (hats, caps, beanies, sunglasses, eyeglasses); **neckwear** (scarves, ties, necklaces); **bags** (handbags, totes, backpacks); **select jewelry** (watches, bracelets, rings, earrings).

**Does not work:** gloves and mittens; arm warmers; handheld props (phones, wallets, umbrellas, cups, keychains); pocket squares, suspenders, and brooches.

## Turbo mode

Turbo applies multiple garment edits in **one larger edit** instead of processing garments separately.

| | Normal (default) | Turbo (`turbo: true`) |
|--|------------------|------------------------|
| **Speed** | Scales with garment count | ~**2.5–3.5 s** regardless of garment count |
| **Quality** | Highest fidelity | May be slightly lower; some garments may not apply correctly |
| **Pricing** | Per-garment table above | **Same** pricing |
| **Best for** | Final assets, up to ~6 garments | Previews, batch catalogs, speed-critical flows (≤6 recommended) |

**Guidance:**

- Turbo is **disabled by default** — enable explicitly when the user prioritizes latency.
- Works with all other inputs (`reference_pose`, `prompt`, etc.).
- Performance tends to drop when dressing **more than 6 garments** at once — stay at **≤6** for final delivery, or use normal mode above that.

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

- Upscale for delivery: [p-image-upscale](../p-image-upscale/SKILL.md)
- Animate try-on still: [p-video](../../video/p-video/SKILL.md) (I2V) or [p-video-avatar](../../video/p-video-avatar/SKILL.md)
- Ecommerce pack workflows: [pruna-generative-pipeline](../../../guides/workflows/router/pruna-generative-pipeline/SKILL.md) recipe K
