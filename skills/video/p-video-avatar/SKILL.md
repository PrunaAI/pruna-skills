---
name: p-video-avatar
description: Use when someone wants a person on camera speaking a script — lip-synced host, spokesperson, or narrated avatar from a portrait photo.
license: MIT
metadata:
  version: "1.0.10"
  package: pruna-skills
  pruna_model: p-video-avatar
---

## Prerequisites

Install and load these skills before generating (skip if already in context via `@pruna`):

| Skill | Description | Install |
| --- | --- | --- |
| `generation-diversity` | Use when writing any generative prompt — ritual seed, explicit structure, scenario axes, and quality gates before paid API calls. | `npx skills add PrunaAI/pruna-skills@generation-diversity -y` |
| `video-prompting` | Use when crafting video or motion prompts for any generative model — dramaturgy, camera, physics-safe motion, frame anchors, and clip chaining. | `npx skills add PrunaAI/pruna-skills@video-prompting -y` |
| `image-prompting` | Use when crafting still-image prompts for any generative model — composition, identity sheets, edits, try-on, and photoreal personas. | `npx skills add PrunaAI/pruna-skills@image-prompting -y` |
| `pruna-api` | Use before any Pruna or Replicate HTTP call — credentials, upload/poll/download, parallel batches, and agent safety. | `npx skills add PrunaAI/pruna-skills@pruna-api -y` |

Or install the full suite once: `npx skills add PrunaAI/pruna-skills@pruna -y`

Follow each skill's **Before generating** / craft sections — do not restate guide content here.

## Agent habit

In the **first reply**, name `` `p-video-avatar` `` in backticks, confirm `PRUNA_API_KEY` (or stop with signup links from `pruna-api`), then ask for required inputs. Open intake → **`generation-diversity`** clarification intake before the first `POST`. **Multiple talking-head scenes with the same person → redirect to `avatar-multi-scene`** (this skill is one clip only). Draft host motion with **Prompt craft (dynamic + faithful)** — do not paste skill examples.

## Skill boundary

This skill = **one `p-video-avatar` prediction** per invocation.

**Out of scope (stop and redirect):**

- Several host segments with continuity → `avatar-multi-scene`
- Multi-scene assembly, concat, or parallel scene batches → workflow skills (`avatar-multi-scene`, `narrated-multi-scene`, …)
- Silent B-roll / no talking head → `p-video`
- Motion transfer from a template video → `p-video-animate`

## Prompt craft (dynamic + faithful)

`video_prompt` (and optional `voice_prompt`) must be **fresh per clip** and **faithful to the user's host beat**. Diversity applies to camera nuance and delivery wording — not to changing who speaks or what they say.

| Do | Don't |
| --- | --- |
| Ritual seed from `generation-diversity` before drafting; unique `video_prompt` per clip in multi-scene work | Reuse one `video_prompt` string across a reel, or paste this skill's sample (`Medium close-up speaking directly to lens`) when the user asked for something else |
| Lock portrait identity from `image`; match head motion and pacing to **`voice_script`** or uploaded **`audio`** | Invent a new persona, wardrobe, or script line the user did not approve |
| Use `video-prompting` dramaturgy — one camera move, physics-safe head motion, mouth visible | Default `The person is talking.` for anything beyond a quick test |
| Show `video_prompt` (+ script/voice fields) before `POST` when wording is not locked | Silent regen that changes tone, framing, or delivery from the brief |

**Fidelity check (before pay):** the clip must still be the user's speaker, script/audio, and approved host beat. If mouth visibility or pacing drifts from the brief, rewrite.

## When NOT to use

Use a different skill instead:

| Skill | Description | Install |
| --- | --- | --- |
| `p-video` | Use when someone wants one short video clip from text or images — B-roll, start/end frame animation, or a quick motion shot. Not for full multi-scene films or lip-synced hosts. | `npx skills add PrunaAI/pruna-skills@p-video -y` |
| `p-video-animate` | Use when someone wants a photo to move like another video — motion transfer, dance remixes, or performance variations from a template clip. | `npx skills add PrunaAI/pruna-skills@p-video-animate -y` |
| `p-video-replace` | Use when someone wants to swap a person, outfit, or product inside existing footage while keeping the camera move and audio. | `npx skills add PrunaAI/pruna-skills@p-video-replace -y` |
| `avatar-multi-scene` | Use when someone wants the same person hosting several clips — multi-segment UGC, comparison reels, or mixed speaking and animated scenes with continuity. | `npx skills add PrunaAI/pruna-skills@avatar-multi-scene -y` |
| `avatar-single-scene` | Use when someone wants one polished host-on-camera beat — a speaking person with intake and approval gates before generation. | `npx skills add PrunaAI/pruna-skills@avatar-single-scene -y` |
| `video-editing` | Use when assembling or polishing already-rendered clips with ffmpeg — concat, crossfades, burned captions and subtitles, text/logo overlays, before/after sliders, background music beds, platform export — or when composing a multi-layer HTML combination video with Hyperframes. Not for AI video generation, prompt craft, or model-based video edits. | `npx skills add PrunaAI/pruna-skills@video-editing -y` |

## HTTP (curl)

### Upload portrait

```bash
curl -X POST "https://api.pruna.ai/v1/files" \
  -H "apikey: ${PRUNA_API_KEY}" \
  -F "content=@/path/to/portrait.png"
```

Use `urls.get` as `input.image`.

### Create (async — recommended)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video-avatar' \
  -d '{
    "input": {
      "image": "https://api.pruna.ai/v1/files/FILE_ID",
      "voice_script": "Hey — so we shipped something I've wanted for a while.",
      "voice": "Puck (Male)",
      "voice_language": "English (US)",
      "voice_prompt": "Natural conversational tone — relaxed pacing, real pauses.",
      "resolution": "720p",
      "video_prompt": "Medium close-up speaking directly to lens, subtle push-in",
      "negative_prompt": "subtitles, captions, on-screen text, watermark, logo, typography, letters, words",
      "negative_prompt_strength": 0.35
    }
  }'
```

Poll and download: follow `pruna-api`.

Complete the random seed ritual from `generation-diversity` before writing prompts — omit `seed` unless the user supplied **`api_seed`**. Confirm `voice_language` with the user.

For multiple clips: create **all** jobs in parallel (async, no `Try-Sync`), then batch-poll.

### Create (sync — quick test only)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video-avatar' \
  -H 'Try-Sync: true' \
  -d '{
    "input": {
      "image": "https://api.pruna.ai/v1/files/FILE_ID",
      "voice_script": "Hey — so we shipped something I've wanted for a while.",
      "voice": "Puck (Male)",
      "voice_language": "English (US)",
      "voice_prompt": "Natural conversational tone — relaxed pacing, real pauses.",
      "resolution": "720p",
      "video_prompt": "Medium close-up speaking directly to lens, subtle push-in"
    }
  }'
```

### Uploaded narration (audio wins over voice_script)

Generate `gemini-3.1-flash-tts` → upload to `/v1/files`. Pass as `input.audio` with portrait `image` (optional `last_frame_image`).

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video-avatar' \
  -d '{
    "input": {
      "image": "https://api.pruna.ai/v1/files/PORTRAIT_START",
      "last_frame_image": "https://api.pruna.ai/v1/files/PORTRAIT_END",
      "audio": "https://api.pruna.ai/v1/files/NARRATION_ID",
      "resolution": "720p",
      "video_prompt": "Medium close-up, natural head motion matching narration"
    }
  }'
```

## Before generating

1. Complete Prerequisites guide reading order (`generation-diversity` → `video-prompting`).
2. Ritual seed → draft a **dynamic + faithful** `video_prompt` (section above) → confirm **`image`** URL, **`voice_script`** (or **`audio`**), **`voice`** / **`voice_language`**, **`voice_prompt`**, **`video_prompt`**, and **`resolution`**. Explicit user confirmation before any paid call.
3. **Pruna notes:** P-API uses **snake_case** (`voice_script`, `video_prompt`, …). Mouth must be visible on the plate. Unique **`video_prompt`** per clip — do not reuse one string across a multi-scene reel. Default `The person is talking.` is quick-test only.

### Negative prompt (experimental — suppress on-screen text)

| Field | Default | Rule |
|-------|---------|------|
| `negative_prompt` | `""` | Comma-separated elements to **suppress** |
| `negative_prompt_strength` | `0` | Both must be set: non-empty prompt **and** strength **> 0** |

Starter: `subtitles, captions, on-screen text, burned-in text, watermark, logo, typography, letters, words`. Start strength around **0.3–0.4**. See `avatar-single-scene` for gated host workflows.

## Typical next steps

Common follow-ons after this skill:

| Skill | Description | Install |
| --- | --- | --- |
| `avatar-multi-scene` | Use when someone wants the same person hosting several clips — multi-segment UGC, comparison reels, or mixed speaking and animated scenes with continuity. | `npx skills add PrunaAI/pruna-skills@avatar-multi-scene -y` |
| `avatar-single-scene` | Use when someone wants one polished host-on-camera beat — a speaking person with intake and approval gates before generation. | `npx skills add PrunaAI/pruna-skills@avatar-single-scene -y` |
| `video-editing` | Use when assembling or polishing already-rendered clips with ffmpeg — concat, crossfades, burned captions and subtitles, text/logo overlays, before/after sliders, background music beds, platform export — or when composing a multi-layer HTML combination video with Hyperframes. Not for AI video generation, prompt craft, or model-based video edits. | `npx skills add PrunaAI/pruna-skills@video-editing -y` |

