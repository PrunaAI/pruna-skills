---
name: p-video-animate
description: Use when someone wants a photo to move like another video — motion transfer, dance remixes, or performance variations from a template clip.
license: MIT
metadata:
  version: "1.0.6"
  pruna_model: p-video-animate
---

# p-video-animate (Pruna)

**P-Video-Animate** animates a single image using the motion, timing, and camera movement from a given video.

**User question this answers:** *How can I animate this picture with some motion?*

Given a reference input image and video, the model generates a new video using **(1)** the style of the reference image, and **(2)** preserving the original motion, acting, timing, camera movement, and scene structure of the reference video.

Also on Replicate: [prunaai/p-video-animate](https://replicate.com/prunaai/p-video-animate). Full P-API parameters: [p-video-animate model docs](https://docs.api.pruna.ai/guides/models/p-video-animate) · operational guide (Runware host): [animating images from video](https://runware.ai/docs/models/prunaai-p-video-animate/guides/animating-images-from-video)

Shared HTTP patterns: [pruna-api.md](references/policies/pruna-api.md)

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

1. **[Generation diversity](references/policies/generation-diversity.md)** — ritual seed + axis rotation; pass as `seed` when set.
2. **[p-video-animate prompting](../../../references/video/p-video-animate-prompting.md)** — pairing gates + when to use `instruction_prompt`.
3. Confirm with the user:

- **`video`** URL — motion/audio source (upload `.mp4` to `/v1/files` first)
- **`image`** URL — subject to animate (upload jpg/jpeg/png/webp first)
- **`resolution`**: `720p` or `1080p`
- **`target_fps`**: `original`, `24`, or `48`
- Optional **`instruction_prompt`** — one specific behavior beat, or leave blank
- Optional **`save_audio`**, **`seed`**, **`disable_safety_checker`**

Run [p-video-animate-quality-checklist.md](../../../references/video/p-video-animate-quality-checklist.md) on inputs and outputs.

**Batch runs:** when several image+video pairs are independent, create **all** predictions in one parallel async batch, then batch-poll. See [parallel-execution.md](references/policies/parallel-execution.md).

## Making motion transfer work

Full pairing + `instruction_prompt` cookbook: [p-video-animate-prompting.md](../../../references/video/p-video-animate-prompting.md).

**Appearance from image, motion from video.** Match framing, pose, and limb visibility to the template’s first frame before paying for a render. Repose with **`p-image-edit`** when close but not exact. Leave **`instruction_prompt`** blank unless you need one concrete end beat.

**Wrong tool:** object removal, background replacement, or in-place identity swap → **`p-image-edit`** / **`p-video-replace`**.

Runware field map: `referenceImages[0]` → `image`, `referenceVideos[0]` → `video`, `positivePrompt` → `instruction_prompt`, `settings.preserveAudio` → `save_audio`.

Mixed-reel context: [animate-beats.md](../../../workflows/avatar-multi-scene/animate-beats.md).

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

Poll and download: [pruna-api.md](references/policies/pruna-api.md#poll).

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
- Pipeline hub: [pruna-generative-pipeline](../../../docs/WORKFLOW-RECIPES.md)
- Multi-scene motion transfer + slider demos: [avatar-multi-scene](../../../workflows/avatar-multi-scene/SKILL.md) (`animate` rows)

## Related workflow

Animate slider reels: [`generate_video_comparison.py`](../../../workflows/_shared/scripts/generate_video_comparison.py) + [avatar-multi-scene](../../../workflows/avatar-multi-scene/SKILL.md) `animate` rows.
