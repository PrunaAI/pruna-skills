---
name: p-video-edit
description: Use when someone wants to change what is inside an existing video — colors, materials, objects, on-screen text, lighting, or the setting — while keeping the camera move, timing, and performance.
license: MIT
metadata:
  version: "1.0.10"
  package: pruna-skills
  pruna_model: p-video-edit
---

## Prerequisites

Install and load these skills before generating (skip if already in context via `@pruna`):

| Skill | Description | Install |
| --- | --- | --- |
| `generation-diversity` | Use when writing any generative prompt — ritual seed, explicit structure, scenario axes, and quality gates before paid API calls. | `npx skills add PrunaAI/pruna-skills@generation-diversity -y` |
| `video-prompting` | Use when crafting video or motion prompts for any generative model — dramaturgy, camera, physics-safe motion, frame anchors, and clip chaining. | `npx skills add PrunaAI/pruna-skills@video-prompting -y` |
| `pruna-api` | Use before any Pruna or Replicate HTTP call — credentials, upload/poll/download, parallel batches, and agent safety. | `npx skills add PrunaAI/pruna-skills@pruna-api -y` |

Or install the full suite once: `npx skills add PrunaAI/pruna-skills@pruna -y`

Follow each skill's **Before generating** / craft sections — do not restate guide content here.

## Agent habit

In the **first reply**, name `` `p-video-edit` `` in backticks, confirm `PRUNA_API_KEY` (or stop with signup links from `pruna-api`), then ask for required inputs. Open intake → **`generation-diversity`** clarification intake before the first `POST`. Draft the edit with **Prompt craft (dynamic + faithful)** — do not paste skill examples. Iterate in **`draft`** before a full-quality run. Redirect when **When NOT to use** fits better.

## Prompt craft (dynamic + faithful)

**`prompt`** carries **one principal change** plus a **preserve-list**. Describe the desired final state, then name everything that must stay identical — geometry, motion, camera, lighting, audio.

| Do | Don't |
| --- | --- |
| Formula: `Change only [X] to [Y]` → preserve-list (`camera movement`, `subject performance`, `lighting`, `shadows`) | Vague `make the video better` or mood-only rewrites |
| One principal change per run; stack further edits as a second job on the output | Stack unrelated edits (colorway + text removal + relight) in one prompt |
| Ritual seed before drafting; fresh wording for preserve clauses when the brief allows | Copy this skill's sample (`jacket blue to red`) when the user described a different target |
| Name references in the prompt — `the cargo box shown in the reference image` | Pass `images` and never mention them in `prompt` |
| Show **`prompt`** before `POST` when wording is not locked | Silent run that changes background, cast, or unrequested regions |

**Fidelity check (before pay):** the stated change and every stated keep must appear in **`prompt`**. Do not "spice" extras when they asked for one edit.

## Skill boundary

| | **p-video-edit** (this skill) | **p-video-replace** |
|---|-------------------------------|---------------------|
| **User question** | *Change what is in this shot?* | *Replace this person in this video?* |
| **Job** | Rewrite content: color, material, object, text, environment, lighting | Swap **identity** into existing footage |
| **Reference images** | **`images`** — **0 to 4**, optional, for SKU / accessory / look match | **`images`** — **1 to 4**, required identity refs |
| **Source cap** | **15 s** | Source length |

**Default for any instruction edit on existing footage.** **Use `p-video-replace`** only when the job is a person/identity swap driven by 1–4 identity stills.

## When NOT to use

Use a different skill instead:

| Skill | Description | Install |
| --- | --- | --- |
| `p-video-replace` | Use when someone wants to swap a person, outfit, or product inside existing footage while keeping the camera move and audio. | `npx skills add PrunaAI/pruna-skills@p-video-replace -y` |
| `p-video-animate` | Use when someone wants a photo to move like another video — motion transfer, dance remixes, or performance variations from a template clip. | `npx skills add PrunaAI/pruna-skills@p-video-animate -y` |
| `p-video` | Use when someone wants one short video clip from text or images — B-roll, start/end frame animation, or a quick motion shot. Not for full multi-scene films or lip-synced hosts. | `npx skills add PrunaAI/pruna-skills@p-video -y` |
| `video-editing` | Use when assembling or polishing already-rendered clips with ffmpeg — concat, crossfades, burned captions and subtitles, text/logo overlays, before/after sliders, background music beds, platform export — or when composing a multi-layer HTML combination video with Hyperframes. Not for AI video generation, prompt craft, or model-based video edits. | `npx skills add PrunaAI/pruna-skills@video-editing -y` |

## HTTP (curl)

### Upload source assets

```bash
curl -X POST "https://api.pruna.ai/v1/files" \
  -H "apikey: ${PRUNA_API_KEY}" \
  -F "content=@/path/to/source-video.mp4"

curl -X POST "https://api.pruna.ai/v1/files" \
  -H "apikey: ${PRUNA_API_KEY}" \
  -F "content=@/path/to/reference-product.png"
```

Use each response `urls.get` in `input.video` and `input.images`.

### Create (async — recommended)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video-edit' \
  -d '{
    "input": {
      "video": "https://api.pruna.ai/v1/files/source-video-abc123",
      "prompt": "Change only the SUV body paint to deep metallic red. Preserve the vehicle geometry, glass, trim, headlights, tires, reflections and shadows. Keep the environment, lighting and camera movement unchanged."
    }
  }'
```

Reference-guided edit — add up to 4 stills and name them in the prompt:

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video-edit' \
  -d '{
    "input": {
      "video": "https://api.pruna.ai/v1/files/source-video-abc123",
      "prompt": "Add the roof cargo box shown in the reference image to the SUV. Keep it rigidly attached and aligned to the roof throughout the camera movement. Preserve the vehicle body, wheels, environment and lighting.",
      "images": [
        "https://api.pruna.ai/v1/files/reference-product-def456"
      ]
    }
  }'
```

Poll and download: follow `pruna-api`. Output duration follows the source video.

Complete the random seed ritual from `generation-diversity` before writing prompts.

### Create (sync — draft preview only)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video-edit' \
  -H 'Try-Sync: true' \
  -d '{
    "input": {
      "video": "https://api.pruna.ai/v1/files/source-video-abc123",
      "prompt": "Change only the plain trench coat into a yellow trench coat.",
      "draft": true
    }
  }'
```

## Before generating

1. Complete Prerequisites guide reading order (`generation-diversity` → `video-prompting`).
2. Ritual seed → draft a **dynamic + faithful** **`prompt`** (section above) → confirm **`video`** (≤ 15 s), the single principal change, the preserve-list, and whether **`images`** are needed.
3. **Pruna notes:** source video is capped at **15 s** and output duration follows it. Billing is per second of returned video — **$0.045/s** standard, **$0.025/s** with **`draft: true`**, so iterate in draft and rerun the locked prompt at full quality. **`prompt_upsampling`** stays `true` in production; set `false` only for literal A/B tests. **`images`** are for SKU / accessory / look match only — identity swaps belong to `p-video-replace`. Fast action, heavy occlusion, and extreme camera motion reduce consistency. Rate limit **50 requests per minute**.

## Required input

- `video` (string URL): source clip, **max 15 seconds**
- `prompt` (string): one principal change + preserve-list

## Common optional fields

- `images` (array of up to 4 string URLs): reference stills — `jpg`, `jpeg`, `png`, `webp`
- `prompt_upsampling` (boolean, default `true`)
- `draft` (boolean, default `false`): faster, cheaper, lower-quality preview
- `save_audio` (boolean, default `true`)
- `seed` (integer `0`–`2147483647`, default random)

## Typical next steps

Common follow-ons after this skill:

| Skill | Description | Install |
| --- | --- | --- |
| `p-image` | Use when someone explicitly wants the fastest, cheapest photo generation — mood boards, bulk panels, or quick iterations — not when controlled photoreal or in-image text is needed. | `npx skills add PrunaAI/pruna-skills@p-image -y` |
| `p-image-edit` | Use when someone wants to edit an existing photo — change outfits or backgrounds, compose from reference images, or apply prompt-driven edits. | `npx skills add PrunaAI/pruna-skills@p-image-edit -y` |
| `p-video-replace` | Use when someone wants to swap a person, outfit, or product inside existing footage while keeping the camera move and audio. | `npx skills add PrunaAI/pruna-skills@p-video-replace -y` |
| `video-editing` | Use when assembling or polishing already-rendered clips with ffmpeg — concat, crossfades, burned captions and subtitles, text/logo overlays, before/after sliders, background music beds, platform export — or when composing a multi-layer HTML combination video with Hyperframes. Not for AI video generation, prompt craft, or model-based video edits. | `npx skills add PrunaAI/pruna-skills@video-editing -y` |

