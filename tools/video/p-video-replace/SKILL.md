---
name: p-video-replace
description: Replaces people, clothing, products, or mixed slots in source video using 1–4 reference images and prompt-guided mapping with Pruna p-video-replace (preserves motion, audio, camera). Use for in-video recast, wardrobe swap, shelf SKU swap, prop/handheld product replace, or p-video-replace — NOT for animating a still from a motion template (use p-video-animate).
license: MIT
metadata:
  version: "0.0.1"
  pruna_model: p-video-replace
---

# p-video-replace (Pruna)

**P-Video-Replace** takes a source RGB video and one or more reference images, then swaps **characters**, **clothing**, **objects/props**, or a **combination** into the scene while preserving the original motion, acting, timing, camera movement, and scene structure.

Given a source video and reference images plus a clear **`instruction_prompt`**, the model places referenced identities into the video — not only face swap.

Full P-API parameters: [p-video-replace model docs](https://docs.api.pruna.ai/guides/models/p-video-replace).

Shared HTTP patterns: [references/pruna-api.md](../../../references/pruna-api.md)

## p-video-replace vs p-video-animate

Pick the model from what the user is trying to do — these are different jobs.

| | **p-video-replace** | **p-video-animate** |
|---|---------------------|---------------------|
| **User question** | *How can I replace this person in this video?* | *How can I animate this picture with some motion?* |
| **Goal** | Swap identity **into** existing footage | Drive a **still** with motion from another clip |
| **Source video** | The **final scene** (actors, audio, environment stay) | A **motion template** (acting, camera, timing only) |
| **Reference images** | **`images`** — **1 to 4** URLs in **one** call (multiple people) | **`image`** — **one** subject per call |
| **Output look** | Same video structure; new face/body from references | New video styled like the still, following template motion |

**Use p-video-replace** when the user has real footage and wants to swap **people**, **clothing/outfits**, **products/props**, or a **mix** in one call (recast, UGC refresh, wardrobe change, shelf SKU swap, in-hand product). Map each reference slot in `instruction_prompt`.

**Use [p-video-animate](../p-video-animate/SKILL.md)** when the user has a portrait or character still and wants it to **perform** using motion copied from a separate template video (meme remix, motion-transfer slider, persona variants).

## Key features

- Top visual quality; preserves source motion, timing, camera path, and audio
- **Multiple reference images in one request** — up to **4** images (multi-person, multi-SKU, or mixed slots)
- Efficient inference: **~3.58s generation per 1s of video** (directional; varies by settings)
- Pricing: **$0.03/s** (720p), **$0.06/s** (1080p) of output video

## What you can replace

| Swap type | Reference still shows | `instruction_prompt` must |
|-----------|----------------------|---------------------------|
| **Character** | New person / cast | Name who in the **source** is replaced; keep motion and scene |
| **Clothing** | Outfit on similar pose | **Replace only garments**; keep face, body motion, background |
| **Object / product** | Hero packshot or prop | **Replace only the object** (bottle, bag, shelf SKU); keep hands and camera |
| **Mixed** | 1–4 refs for people + props + wardrobe | Map **each** image index to a specific slot in the source |

**Anti-pattern:** Generic lines like *"Replace the person in the video"* without naming **what** in the source and **what** from each reference. Identity comes from **`images`**; correct **slot mapping** comes from **`instruction_prompt`**.

**Launch / showcase reels:** Prefer **`multi_job`** (one image per API call) with per-reference prompts; default **`p-video-avatar`** sources (product in hand, desk prop, solo talking head). See [p-video-replace-comparison](../../../guides/workflows/p-video-replace-comparison/SKILL.md) and [replace-beats.md](../../../guides/workflows/p-video-replace-comparison/replace-beats.md) for production-tested scene patterns and anti-patterns (I2V shelf, two-shot cafe, flat-lay-only clothing refs).

## Before generating

Confirm with the user:

- **`video`** URL — source RGB `.mp4` (motion + audio source; upload to `/v1/files` first)
- **`images`** — **1–4** identity reference URLs (upload each image first)
- **`resolution`**: `720p` or `1080p`
- **`target_fps`**: `original`, `24`, or `48`
- **`instruction_prompt`** — **required for production quality**: map each source slot (left person, white bottle, red dress) to reference cues; say what **not** to change (camera, audio, background)
- **Swap intent** — character vs clothing-only vs object vs mixed (decide before writing the prompt)
- Optional **`save_audio`**, **`seed`**, **`disable_safety_checker`**

Run [p-video-replace-quality-checklist.md](../../../references/p-video-replace-quality-checklist.md) on inputs and outputs.

**Batch runs:** when several independent source videos each need replacement, create **all** predictions in one parallel async batch, then batch-poll. See [parallel-execution.md](../../../references/parallel-execution.md).

## Making replacement work

**Two inputs matter:** (1) **`images`** — replacement look; (2) **`instruction_prompt`** — which source element each image replaces.

| Factor | Guidance |
|--------|----------|
| Reference count | One still per slot; **up to 4** per call |
| Multi-slot scenes | One `instruction_prompt` listing left/right, shelf order, or in-hand object |
| Variant rows | One image per API call; **per-call** `instruction_prompt` naming source subject + reference cues |
| Shot alignment | Match framing/scale between source and reference (especially products) |
| Audio | `save_audio: true` when dialogue or SFX matter |

**Character** (UGC recast):

```text
Replace the young man in the kitchen ad with the woman from the reference — coral linen shirt.
Keep pointing gesture, handheld drift, counter, and audio unchanged.
```

**Clothing only** (same model, new outfit):

```text
Replace only the clothing: swap white tee and jeans for the emerald evening gown and heels from the reference.
Keep the same face, walk cycle, and tracking camera.
```

**Object** (in-hand SKU):

```text
Replace only the plain white bottle in the creator's hand with the blue protein tub from the reference.
Preserve face, shake motion, and gym background.
```

**Mixed** (cafe — face + bag + jacket):

```text
Replace the woman with the first reference (face and burgundy bag). Replace the man's navy bomber with the olive suede jacket from the second reference.
Preserve table, cups, laughter timing, and camera orbit.
```

Prepare references with **`p-image`** / **`p-image-edit`** when the user only has loose photos.

## Required input

- `video` (string URL): source RGB video (`.mp4`); motion and audio source
- `images` (array of 1–4 string URLs): identity reference image(s) to place into the video

## Common optional fields

- `resolution`: `720p` (default) or `1080p`
- `target_fps`: `original` (default), `24`, or `48`
- `instruction_prompt` (string): how to place people from the reference images into the scene
- `save_audio` (boolean, default `true`)
- `seed` (integer)
- `disable_safety_checker` (boolean, default `false`)

## Example: upload source assets

```bash
curl -X POST "https://api.pruna.ai/v1/files" \
  -H "apikey: ${PRUNA_API_KEY}" \
  -F "content=@/path/to/source-video.mp4"

curl -X POST "https://api.pruna.ai/v1/files" \
  -H "apikey: ${PRUNA_API_KEY}" \
  -F "content=@/path/to/reference-person-a.png"

curl -X POST "https://api.pruna.ai/v1/files" \
  -H "apikey: ${PRUNA_API_KEY}" \
  -F "content=@/path/to/reference-person-b.png"
```

Use each response `urls.get` (or `https://api.pruna.ai/v1/files/{id}`) in `input.video` and `input.images`.

## Example: async (recommended) — two people, one call

Omit `Try-Sync`. Output duration follows the source video.

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video-replace' \
  -d '{
    "input": {
      "video": "https://api.pruna.ai/v1/files/source-video-abc123",
      "images": [
        "https://api.pruna.ai/v1/files/reference-person-a-def456",
        "https://api.pruna.ai/v1/files/reference-person-b-ghi789"
      ],
      "resolution": "720p",
      "target_fps": "original",
      "instruction_prompt": "Replace the woman on the left (olive coat) with the first reference. Replace the man on the right (navy jacket) with the second reference. Preserve walking pace, camera tracking, and audio."
    }
  }'
```

Poll and download: [pruna-api.md](../../../references/pruna-api.md#poll).

## Example: sync (single quick test only)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video-replace' \
  -H 'Try-Sync: true' \
  -d '{
    "input": {
      "video": "https://api.pruna.ai/v1/files/source-video-abc123",
      "images": [
        "https://api.pruna.ai/v1/files/reference-image-def456"
      ]
    }
  }'
```

## Typical next steps

- Motion-transfer from a still (different model): [p-video-animate](../p-video-animate/SKILL.md)
- Generate or edit reference portraits: [p-image](../../image/p-image/SKILL.md), [p-image-edit](../../image/p-image-edit/SKILL.md)
- New talking-head clip from script (not in-place replacement): [p-video-avatar](../p-video-avatar/SKILL.md)
- Multi-scene slider demos: [p-video-replace-comparison](../../../guides/workflows/p-video-replace-comparison/SKILL.md)
- Pipeline hub: [pruna-generative-pipeline](../../../guides/workflows/pruna-generative-pipeline/SKILL.md)

## Related workflow

Slider reels and plan runners: [p-video-replace-comparison](../../../guides/workflows/p-video-replace-comparison/SKILL.md) — bundled `run_from_plan.py` and `generate_video_comparison.py` (not in this tool skill).
