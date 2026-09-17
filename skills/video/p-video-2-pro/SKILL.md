---
name: p-video-2-pro
description: Use when someone wants a cinematic clip from text or start/end frames — product ads, documentary shots, or dialogue with generated audio. Not for 1080p, imported audio tracks, or talking-head-only hosts.
license: MIT
metadata:
  version: "1.0.13"
  package: pruna-skills
  pruna_model: p-video-2-pro
---

## Prerequisites

Install and load these skills before generating (skip if already in context via `@pruna`):

| Skill | Description | Install |
| --- | --- | --- |
| `generation-diversity` | Use when writing any generative prompt — ritual seed, explicit structure, scenario axes, and quality gates before paid API calls. | `npx skills add PrunaAI/pruna-skills@generation-diversity -y` |
| `video-prompting` | Use when crafting video or motion prompts for any generative model — dramaturgy, camera, physics-safe motion, frame anchors, and clip chaining. | `npx skills add PrunaAI/pruna-skills@video-prompting -y` |
| `audio-prompting` | Use when crafting TTS, music, or bed prompts for any generative audio model — director style, song structure, and post-production layering. | `npx skills add PrunaAI/pruna-skills@audio-prompting -y` |
| `pruna-api` | Use before any Pruna or Replicate HTTP call — credentials, upload/poll/download, parallel batches, and agent safety. | `npx skills add PrunaAI/pruna-skills@pruna-api -y` |

Or install the full suite once: `npx skills add PrunaAI/pruna-skills@pruna -y`

Follow each skill's **Before generating** / craft sections — do not restate guide content here.

## Agent habit

**Routing:** `` `p-video-2-pro` `` is the **cinematic generation** clip (text / first frame / first+last frame) with **generated audio**. Use `` `p-video-2` `` when the brief needs **1080p**, **imported audio**, or **draft** previews. Use `` `p-video` `` for cheaper, faster drafts. Talking-head-only (no native scene audio) → `` `p-video-avatar` ``. Instruction edit of existing footage → `` `p-video-edit` ``.

In the **first reply**, name `` `p-video-2-pro` `` in backticks, confirm `PRUNA_API_KEY` (or stop with signup links from `pruna-api`), then ask for required inputs. Open intake → **`generation-diversity`** clarification intake before the first `POST`. When drafting motion prompts, follow **Prompt craft (dynamic + faithful)** and `video-prompting` (`p-video-2-pro-prompting`) — do not paste skill examples. Redirect when **When NOT to use** fits better.

## Prompt craft (dynamic + faithful)

Every `input.prompt` must be **fresh and specific**, and must **match the user's beat**. Diversity never overrides the brief. Craft deltas vs `p-video-2`: `video-prompting` (`p-video-2-pro-prompting`). Write **sound or dialogue into the prompt** — this model has no `audio` upload.

| Do | Don't |
| --- | --- |
| Run the `generation-diversity` random seed ritual; state it; rotate ≥2 free axes (camera move, lighting shift, texture, pacing) when the brief allows | Copy curl examples from this skill (`sports car`, `person turns`, …) or reuse a prior session's prompt |
| Lock user-required facts first (subject, action, scene; OPEN/MID/CLOSE when frame-anchored; spoken line / SFX when audio is part of the brief) | Swap the subject or motion for a “cooler” clip that ignores the request |
| Structure with `video-prompting` dramaturgy — subject + action + scene; add camera, lighting, style, and audio intent for locked-in finals | Vague mood-only strings (`cinematic vibe, neon energy`) or a silent prompt when the brief asked for speech or score |
| Keep speakers to **one or two**; name the line in the prompt | Crowd a clip with 3+ talking faces, or send `audio` / `draft` / `fps` (not on this API) |
| Show the drafted prompt + `mode` / `prompt_upsampler` / `duration` / `resolution` before `POST` when the user has not locked wording | Silent regen with a different subject or beat than approved |

**Fidelity check (before pay):** if you remove the user's named subject/action/setting from the prompt, the job is wrong — rewrite. Free axes only fill what the brief left open.

When showing a drafted prompt, still name `` `p-video-2-pro` `` (guides help craft; this tool owns the call).

## Skill boundary

This skill = **one `p-video-2-pro` prediction** per invocation.

**Out of scope (do not execute from this skill):**

- Multi-scene assembly, concat, subagent orchestration, or parallel scene batches
- Imported audio / mixed VO / 1080p / draft previews → `p-video-2`
- Motion transfer from a template video → `p-video-animate`
- Talking-head-only / lip-sync host without native scene audio → `p-video-avatar`
- Instruction edit of existing footage → `p-video-edit`

If the request exceeds one clip, **stop** and recommend: `image-to-video` (one beat), `visual-transition-reel` (multi-scene visual), or `narrated-multi-scene` (multi-scene + uploaded VO — that path uses `p-video-2`).

## When NOT to use

Use a different skill instead:

| Skill | Description | Install |
| --- | --- | --- |
| `p-video-2` | Use when someone wants a polished short clip from text, images, or imported audio — 1080p B-roll, start/end frame animation, or a motion shot with a mixed track. Not for cinematic generated-audio clips or talking-head-only hosts. | `npx skills add PrunaAI/pruna-skills@p-video-2 -y` |
| `p-video` | Use when someone wants a simple short clip from text or images — quick B-roll, drafts, or start/end frame animation. Not when the brief needs cinematic generation, highest quality, tight lip-sync, or imported audio at 1080p. | `npx skills add PrunaAI/pruna-skills@p-video -y` |
| `p-video-avatar` | Use when someone wants a person on camera speaking a script — lip-synced host, spokesperson, or narrated avatar from a portrait photo. | `npx skills add PrunaAI/pruna-skills@p-video-avatar -y` |
| `p-video-animate` | Use when someone wants a photo to move like another video — motion transfer, dance remixes, or performance variations from a template clip. | `npx skills add PrunaAI/pruna-skills@p-video-animate -y` |
| `p-video-replace` | Use when someone wants to swap a person, outfit, or product inside existing footage while keeping the camera move and audio. | `npx skills add PrunaAI/pruna-skills@p-video-replace -y` |
| `p-video-edit` | Use when someone wants to edit an existing video with a text instruction — recolor, restyle, remove or add objects, change environment or lighting, update on-screen text, or apply optional reference-guided product and accessory edits. Not for a new clip from scratch or ffmpeg assembly. | `npx skills add PrunaAI/pruna-skills@p-video-edit -y` |
| `video-editing` | Use when assembling or polishing already-rendered clips with ffmpeg — concat, crossfades, burned captions and subtitles, text/logo overlays, before/after sliders, background music beds, platform export — or when composing a multi-layer HTML combination video with Hyperframes. Not for AI video generation, prompt craft, or model-based video edits. | `npx skills add PrunaAI/pruna-skills@video-editing -y` |

## HTTP (curl)

### Upload for image-to-video / frame anchors

```bash
curl -X POST "https://api.pruna.ai/v1/files" \
  -H "apikey: ${PRUNA_API_KEY}" \
  -F "content=@/path/to/first-frame.png"
```

Pass `urls.get` as `input.image` (first frame) and/or `input.last_frame_image` (last frame). **Do not** upload audio for this model.

### Create (async text-to-video — recommended)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video-2-pro' \
  -d '{
    "input": {
      "prompt": "A sports car drifting through a neon-lit city at night, cinematic aerial shot",
      "duration": 5,
      "resolution": "768p",
      "aspect_ratio": "16:9"
    }
  }'
```

Poll and download: follow `pruna-api`.

Complete the random seed ritual from `generation-diversity` before writing prompts — **do not** pass the ritual string as API `seed`.

Billing is per **returned** second (not the requested `duration`). Rate limit: 250 requests per minute.

| Resolution | `mode=speed` | `mode=quality` |
|------------|--------------|----------------|
| 480p | $0.02 / s | $0.04 / s |
| 768p | $0.035 / s | $0.075 / s |

### Image-to-video (first frame)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video-2-pro' \
  -d '{
    "input": {
      "prompt": "The camera slowly pushes in, the person turns their head and smiles",
      "image": "https://api.pruna.ai/v1/files/FIRST_ID",
      "duration": 5,
      "resolution": "768p"
    }
  }'
```

### First / last frame (visual transition)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video-2-pro' \
  -d '{
    "input": {
      "prompt": "Start on the still product hero. The camera holds, then a slow push-in as light moves across the metal. End exactly on the last-frame packshot, label readable, no extra props.",
      "image": "https://api.pruna.ai/v1/files/START_ID",
      "last_frame_image": "https://api.pruna.ai/v1/files/END_ID",
      "duration": 8,
      "resolution": "768p",
      "mode": "speed",
      "prompt_upsampler": "turbo"
    }
  }'
```

There is **no scene-anchor triple** on this model (`audio` is not exposed). Uploaded VO / music → `p-video-2`.

### Create (sync — quick test only)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video-2-pro' \
  -H 'Try-Sync: true' \
  -d '{
    "input": {
      "prompt": "A sports car drifting through a neon-lit city at night, cinematic aerial shot",
      "duration": 5,
      "resolution": "480p",
      "mode": "speed"
    }
  }'
```

## Before generating

1. Complete Prerequisites guide reading order (`generation-diversity` → `video-prompting`).
2. Ritual seed → draft a **dynamic + faithful** motion prompt (section above) → confirm **mode** (T2V / I2V / frame pair), **`duration`** (5–15s, default 5), **`resolution`** (480p / 768p), **`mode`** (`speed` / `quality`), **`prompt_upsampler`**, and **`prompt`** with the user.
3. **Pruna notes:** when `image` or `last_frame_image` is set, `aspect_ratio` is ignored (canvas follows the stills). Output is **24 fps** — do not send `fps`. Output includes **generated audio**; write sound or dialogue in the prompt. **Do not send** `audio`, `draft`, `save_audio`, or `prompt_upsampling`. Iterate in **`mode: speed`**, then final with `mode: quality` when fidelity matters. If the request is multi-scene — **stop** (see Skill boundary). Native 4K is not supported. 1080p / imported audio / draft → `p-video-2`.

## Required input

- `prompt` (string)

## Common optional fields

| Field | Role |
|-------|------|
| `prompt_upsampler` | Expand the prompt before generation: `off`, `turbo` (default), or `max`. Independent of `mode` |
| `image` | First-frame reference; when set, `aspect_ratio` is ignored (`jpg`, `jpeg`, `png`, `webp`) |
| `last_frame_image` | Optional end-frame still |
| `duration` | 5–15s (default **5**) |
| `resolution` | `768p` (default) or `480p` |
| `mode` | Generation recipe: `speed` (default, faster) or `quality` (slower) |
| `aspect_ratio` | When no reference image: `16:9` (default), `9:16`, `4:3`, `3:4`, `3:2`, `2:3`, `1:1` |
| `seed` | Integer for a reproducible rerun; omit for random |

**Do not send:** `audio`, `draft`, `fps`, `save_audio`, `prompt_upsampling`.

## Related

Related skills:

| Skill | Description | Install |
| --- | --- | --- |
| `p-video-2` | Use when someone wants a polished short clip from text, images, or imported audio — 1080p B-roll, start/end frame animation, or a motion shot with a mixed track. Not for cinematic generated-audio clips or talking-head-only hosts. | `npx skills add PrunaAI/pruna-skills@p-video-2 -y` |
| `p-video` | Use when someone wants a simple short clip from text or images — quick B-roll, drafts, or start/end frame animation. Not when the brief needs cinematic generation, highest quality, tight lip-sync, or imported audio at 1080p. | `npx skills add PrunaAI/pruna-skills@p-video -y` |
| `gemini-3.1-flash-tts` | Use when someone needs spoken narration or voiceover — explainer tracks, documentary lines, or voice to pair with generated video. | `npx skills add PrunaAI/pruna-skills@gemini-3.1-flash-tts -y` |
| `image-to-video` | Use when someone wants one short film beat from images — a narrated scene, story moment, or cinematic B-roll with optional voiceover. | `npx skills add PrunaAI/pruna-skills@image-to-video -y` |
| `visual-transition-reel` | Use when someone wants a montage with transitions between shots — action-sequence reel or multi-scene piece where narration is optional. | `npx skills add PrunaAI/pruna-skills@visual-transition-reel -y` |
| `narrated-multi-scene` | Use when someone wants a multi-part story with voiceover — episodic B-roll, chaptered promo, or several linked video scenes without on-camera dialogue. | `npx skills add PrunaAI/pruna-skills@narrated-multi-scene -y` |
| `p-video-avatar` | Use when someone wants a person on camera speaking a script — lip-synced host, spokesperson, or narrated avatar from a portrait photo. | `npx skills add PrunaAI/pruna-skills@p-video-avatar -y` |
| `p-video-animate` | Use when someone wants a photo to move like another video — motion transfer, dance remixes, or performance variations from a template clip. | `npx skills add PrunaAI/pruna-skills@p-video-animate -y` |
| `video-editing` | Use when assembling or polishing already-rendered clips with ffmpeg — concat, crossfades, burned captions and subtitles, text/logo overlays, before/after sliders, background music beds, platform export — or when composing a multi-layer HTML combination video with Hyperframes. Not for AI video generation, prompt craft, or model-based video edits. | `npx skills add PrunaAI/pruna-skills@video-editing -y` |

