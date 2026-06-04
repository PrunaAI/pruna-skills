---
name: p-video-animate
description: Use when the user wants motion transfer onto a still from a reference video, UGC variations from motion templates, or p-video-animate—not replacing a person inside existing footage.
license: MIT
metadata:
  version: "0.0.1"
  pruna_model: p-video-animate
---

# p-video-animate (Pruna)

**P-Video-Animate** animates a single image using the motion, timing, and camera movement from a given video.

**User question this answers:** *How can I animate this picture with some motion?*

Given a reference input image and video, the model generates a new video using **(1)** the style of the reference image, and **(2)** preserving the original motion, acting, timing, camera movement, and scene structure of the reference video.

Also on Replicate: [prunaai/p-video-animate](https://replicate.com/prunaai/p-video-animate). Full P-API parameters: [p-video-animate model docs](https://docs.api.pruna.ai/guides/models/p-video-animate).

Shared HTTP patterns: [references/shared/pruna-api.md](../../../references/shared/pruna-api.md)

## p-video-animate vs p-video-replace

| | **p-video-animate** (this skill) | **p-video-replace** |
|---|----------------------------------|---------------------|
| **User question** | *How can I animate this picture with some motion?* | *How can I replace this person in this video?* |
| **Inputs** | One **`image`** + motion-template **`video`** | Source **`video`** + **`images`** (1–4 identity refs in **one** call) |
| **Job** | Still performs using copied motion | People in footage swapped for reference identities |

**Use [p-video-replace](../p-video-replace/SKILL.md)** for in-place identity swap on real clips. **Use this skill** for motion-transfer showcases, persona variants, and slider before/after demos.

## Key features

- Top visual quality
- Most efficient inference
  - Speed: **5.24s generation time per 1s video**
  - Price: **$0.03 and $0.06 per 1s of 720p and 1080p video**

## Key examples

- **UGC ad variations** — Reuse winning video motions with different creator, customer, or persona images at large scale.
- **Viral meme remixes** — Turn trending clips into new animated image-based meme formats quickly.
- **Movie scene recasting** — Animate user-uploaded avatars, selfies, or character images using reusable motion templates.
- **Game cinematic variations** — Animate user-uploaded avatars, selfies, or character images using reusable motion templates.

## Before generating

Confirm with the user:

- **`video`** URL — motion/audio source (upload `.mp4` to `/v1/files` first)
- **`image`** URL — subject to animate (upload jpg/jpeg/png/webp first)
- **`resolution`**: `720p` or `1080p`
- **`target_fps`**: `original`, `24`, or `48`
- Optional **`instruction_prompt`** — how the reference subject should follow the source motion
- Optional **`save_audio`**, **`seed`**, **`disable_safety_checker`**

Run [p-video-animate-quality-checklist.md](../../../references/video/p-video-animate-quality-checklist.md) on inputs and outputs.

**Batch runs:** when several image+video pairs are independent, create **all** predictions in one parallel async batch, then batch-poll. See [parallel-execution.md](../../../references/shared/parallel-execution.md).

## Making motion transfer work

**Appearance from image, motion from video.** Quality depends on how well the reference image aligns with the motion template.

| Factor | Guidance |
|--------|----------|
| Shot size | Match close-up / medium / full between image and template |
| Facing | Front-facing still + profile motion → head/shoulder artifacts |
| Limbs | If template waves arms, still must show arms |
| Proportions | Human full-body motion on chibi/mascot subjects often breaks legs and gait |
| Speaking templates | When source video has dialogue, persona mouth must be clear and large enough |

**Before generate:** repose with **`p-image-edit`** when pose is close but not exact. Upscale reference stills for identity detail.

**`instruction_prompt`** — steer without fighting source motion:

```text
Animate the reference subject using the exact motion, timing, and camera movement from the source video. Keep identity and outfit from the reference image.
```

**Style variety:** photoreal, 3D, claymation, and anime/game personas can share one motion template when framing aligns — useful for slider demos showing range.

Mixed-reel context (motion templates, sliders, avatar CTA): [animate-beats.md](../../../guides/workflows/core/avatar-multi-scene/animate-beats.md).

## Required input

- `video` (string URL): source RGB video (`.mp4`); motion and audio source
- `image` (string URL): reference subject to animate

## Common optional fields

- `resolution`: `720p` (default) or `1080p`
- `target_fps`: `original` (default), `24`, or `48`
- `instruction_prompt` (string): extra guidance on how the subject should follow source motion
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
  -F "content=@/path/to/reference-image.png"
```

Use each response `urls.get` (or `https://api.pruna.ai/v1/files/{id}`) in `input.video` and `input.image`.

## Example: async (recommended)

Omit `Try-Sync`. Output duration follows the source video.

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video-animate' \
  -d '{
    "input": {
      "video": "https://api.pruna.ai/v1/files/source-video-abc123",
      "image": "https://api.pruna.ai/v1/files/reference-image-def456",
      "resolution": "720p",
      "target_fps": "original",
      "instruction_prompt": "Animate the reference subject using the motion from the source video."
    }
  }'
```

Poll and download: [pruna-api.md](../../../references/shared/pruna-api.md#poll).

## Example: sync (single quick test only)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video-animate' \
  -H 'Try-Sync: true' \
  -d '{
    "input": {
      "video": "https://api.pruna.ai/v1/files/source-video-abc123",
      "image": "https://api.pruna.ai/v1/files/reference-image-def456"
    }
  }'
```

## Typical next steps

- Generate or edit reference subjects: [p-image](../../image/p-image/SKILL.md), [p-image-edit](../../image/p-image-edit/SKILL.md)
- Replace people in existing footage (not motion transfer): [p-video-replace](../p-video-replace/SKILL.md)
- Talking-head clips (script-driven, not motion transfer): [p-video-avatar](../p-video-avatar/SKILL.md)
- Pipeline hub: [pruna-generative-pipeline](../../../guides/workflows/router/pruna-generative-pipeline/SKILL.md)
- Multi-scene motion transfer + slider demos: [multi-scene-avatar-video](../../../guides/workflows/core/avatar-multi-scene/SKILL.md) (`animate` rows)

## Related workflow

Animate slider reels: [p-video-animate-comparison](../../../guides/workflows/launches/p-video-animate-comparison/SKILL.md) — bundled `run_from_plan.py` and `generate_video_comparison.py` (not in this tool skill).
