---
name: p-video-edit
description: Use when someone wants to edit an existing video with a text instruction — recolor, restyle, remove or add objects, change environment or lighting, update on-screen text, or apply optional reference-guided product and accessory edits. Not for a new clip from scratch or ffmpeg assembly.
license: MIT
metadata:
  version: "1.0.11"
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

In the **first reply**, name `` `p-video-edit` `` in backticks, confirm `PRUNA_API_KEY` (or stop with signup links from `pruna-api`), then ask for the source video (max **15s**) and edit brief. Open intake → `generation-diversity` clarification intake before the first `POST`. Draft edits with **Prompt craft (dynamic + faithful)** — do not paste skill examples. Redirect when **When NOT to use** fits better.

## Prompt craft (dynamic + faithful)

`prompt` is **surgical** and **request-locked**. One principal change per run. Describe the desired final state, then name what must stay unchanged. Change only what the user asked; keep camera, motion, audio, and unmentioned elements identical.

| Do                                                                                                   | Don't                                                                            |
| ---------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Formula: `Change only [X]. Preserve [geometry / motion / camera / lighting / unmentioned subjects].` | Vague `make it better` / mood-only rewrites that invent a new scene              |
| Name every **must-keep** from the user (subject, camera path, lighting, props)                       | Drop keep-clauses and hope the model preserves them                              |
| Ritual seed before drafting; fresh wording for keep clauses when the brief allows                    | Copy this skill's sample (`sunset sky`) when the user described a different edit |
| Point at refs when used: `add the accessory from the first reference`                                | Vague `use the reference` with no source slot                                    |
| Show `prompt` before `POST` when wording is not locked                                               | Silent edit that changes camera, cast, or unrequested regions                    |

**Fidelity check (before pay):** the prompt must still satisfy the user’s change **and** every stated keep. Do not “spice” extras when they asked for one attribute or environment edit.

**Weak jobs (avoid or warn):** a brand-new scene/plot; adding an object with its own independent motion (especially a new in-hand shape); changing camera angle, camera motion, or zoom.

## Skill boundary

|                      | **p-video-edit**                                                          | **p-video-replace**                     |
| -------------------- | ------------------------------------------------------------------------- | --------------------------------------- |
| **User question**    | *Change the color / environment / object / text / lighting in this clip?* | *Replace this person in this video?*    |
| **Goal**             | Instruction edit of the **source clip**                                   | Swap identity **into** existing footage |
| **Reference images** | Optional `images` — **0 to 4**                                            | Required `images` — **1 to 4**          |
| **Prompt field**     | `prompt`                                                                  | `instruction_prompt`                    |

**Use** `p-video-replace` when the job is a character swap from required reference stills. **Use this skill** for prompt-driven attribute, environment, object, text, or lighting edits.

## When NOT to use

Use a different skill instead:

| Skill | Description | Install |
| --- | --- | --- |
| `p-video` | Use when someone wants one short video clip from text or images — B-roll, start/end frame animation, or a quick motion shot. Not for full multi-scene films or lip-synced hosts. | `npx skills add PrunaAI/pruna-skills@p-video -y` |
| `p-video-replace` | Use when someone wants to swap a person, outfit, or product inside existing footage while keeping the camera move and audio. | `npx skills add PrunaAI/pruna-skills@p-video-replace -y` |
| `p-video-animate` | Use when someone wants a photo to move like another video — motion transfer, dance remixes, or performance variations from a template clip. | `npx skills add PrunaAI/pruna-skills@p-video-animate -y` |
| `video-editing` | Use when assembling or polishing already-rendered clips with ffmpeg — concat, crossfades, burned captions and subtitles, text/logo overlays, before/after sliders, background music beds, platform export — or when composing a multi-layer HTML combination video with Hyperframes. Not for AI video generation, prompt craft, or model-based video edits. | `npx skills add PrunaAI/pruna-skills@video-editing -y` |

## HTTP (curl)

### Upload source video

```bash
curl -X POST "https://api.pruna.ai/v1/files" \
  -H "apikey: ${PRUNA_API_KEY}" \
  -F "content=@/path/to/source-video.mp4"
```

Use the response `urls.get` in `input.video`. Source video maximum length: **15 seconds**.

### Optional reference images

```bash
curl -X POST "https://api.pruna.ai/v1/files" \
  -H "apikey: ${PRUNA_API_KEY}" \
  -F "content=@/path/to/reference-image.png"
```

Use each response `urls.get` in `input.images` (up to 4; `jpg`, `jpeg`, `png`, `webp`).

### Create (async — recommended)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video-edit' \
  -d '{
    "input": {
      "video": "https://api.pruna.ai/v1/files/source-video-abc123",
      "prompt": "Change only the sky to a sunset. Preserve the subject, camera path, and lighting on the foreground."
    }
  }'
```

Poll and download: follow `pruna-api`. Output duration follows the source video. Billing is per **returned** second (`$0.045` standard, `$0.025` draft). Rate limit: 50 requests per minute.

Complete the random seed ritual from `generation-diversity` before writing prompts — **do not** pass the ritual string as API `seed`. Optional `seed` only when the user requests reproducibility.

### Create (sync — quick test only)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video-edit' \
  -H 'Try-Sync: true' \
  -d '{
    "input": {
      "video": "https://api.pruna.ai/v1/files/source-video-abc123",
      "prompt": "Change only the sky to a sunset. Preserve the subject, camera path, and lighting on the foreground.",
      "draft": true
    }
  }'
```

## Before generating

1. Complete Prerequisites guide reading order (`generation-diversity` → `video-prompting`).
2. Ritual seed → draft a **dynamic + faithful** `prompt` (section above) → confirm `video` (≤15s), `prompt`, optional `images` (0–4), `draft`, `save_audio`, and edit intent (attribute / remove / add / environment / relight / text / reference-guided).
3. **Pruna notes:** one principal change per run. Identity or product match comes from optional `images`; the edit instruction lives in `prompt`. Vague targets and brand-new scenes drop quality. Do not send a `task` field — it is not in the public API.

## Required input

- `video` (string URL): source video to edit. Maximum length: 15 seconds
- `prompt` (string): text instruction describing the edit

## Common optional fields

- `images` (array of up to 4 string URLs): reference image(s) for reference-guided editing (`jpg`, `jpeg`, `png`, `webp`)
- `prompt_upsampling` (boolean, default `true`)
- `draft` (boolean, default `false`): faster, lower-quality preview; billed at `$0.025` per output second
- `save_audio` (boolean, default `true`)
- `seed` (integer): set only for reproducible reruns

## Typical next steps

Common follow-ons after this skill:

| Skill | Description | Install |
| --- | --- | --- |
| `p-video-replace` | Use when someone wants to swap a person, outfit, or product inside existing footage while keeping the camera move and audio. | `npx skills add PrunaAI/pruna-skills@p-video-replace -y` |
| `p-image-edit` | Use when someone wants to edit an existing photo — change outfits or backgrounds, compose from reference images, or apply prompt-driven edits. | `npx skills add PrunaAI/pruna-skills@p-image-edit -y` |
| `video-editing` | Use when assembling or polishing already-rendered clips with ffmpeg — concat, crossfades, burned captions and subtitles, text/logo overlays, before/after sliders, background music beds, platform export — or when composing a multi-layer HTML combination video with Hyperframes. Not for AI video generation, prompt craft, or model-based video edits. | `npx skills add PrunaAI/pruna-skills@video-editing -y` |

