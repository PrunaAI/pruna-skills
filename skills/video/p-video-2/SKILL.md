---
name: p-video-2
description: Use when someone wants the best-quality short clip from text, images, or audio — polished B-roll, start/end frame animation, or a motion shot with stronger lip-sync. Not for full multi-scene films or talking-head-only hosts.
license: MIT
metadata:
  version: "1.0.12"
  package: pruna-skills
  pruna_model: p-video-2
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

**Routing:** `` `p-video-2` `` is the **quality** clip generator (text / image / audio). Use `` `p-video` `` for simpler, quicker clips. Talking-head-only (no native scene audio) → `` `p-video-avatar` ``. Instruction edit of existing footage → `` `p-video-edit` ``.

In the **first reply**, name `` `p-video-2` `` in backticks, confirm `PRUNA_API_KEY` (or stop with signup links from `pruna-api`), then ask for required inputs. Open intake → **`generation-diversity`** clarification intake before the first `POST`. When drafting motion prompts, follow **Prompt craft (dynamic + faithful)** and `video-prompting` (`p-video-2-prompting`) — do not paste skill examples. Redirect when **When NOT to use** fits better.

## Prompt craft (dynamic + faithful)

Every `input.prompt` must be **fresh and specific**, and must **match the user's beat**. Diversity never overrides the brief. Craft deltas vs `p-video`: `video-prompting` (`p-video-2-prompting`).

| Do | Don't |
| --- | --- |
| Run the `generation-diversity` random seed ritual; state it; rotate ≥2 free axes (camera move, lighting shift, texture, pacing) when the brief allows | Copy curl examples from this skill (`sports car`, `person turns`, …) or reuse a prior session's prompt |
| Lock user-required facts first (subject, action beat, OPEN/MID/CLOSE when frame-anchored, narration sync when `audio` is set) | Swap the subject or motion for a “cooler” clip that ignores the request |
| Structure with `video-prompting` dramaturgy — one frozen action per beat, **stable** camera for I2V, physics-safe motion | Vague mood-only strings (`cinematic vibe, neon energy`) or extreme cinematic camera moves |
| When `audio` is set, motion and pacing must **match the narration / performance beat**; keep speakers to **one or two** | Drift to unrelated action while VO plays, or crowd a clip with 3+ talking faces |
| Show the drafted prompt + mode fields before `POST` when the user has not locked wording | Silent regen with a different subject or beat than approved |

**Fidelity check (before pay):** if you remove the user's named subject/action/setting from the prompt, the job is wrong — rewrite. Free axes only fill what the brief left open.

When showing a drafted prompt, still name `` `p-video-2` `` (guides help craft; this tool owns the call).

## Skill boundary

This skill = **one `p-video-2` prediction** per invocation.

**Out of scope (do not execute from this skill):**

- Multi-scene assembly, concat, subagent orchestration, or parallel scene batches
- Motion transfer from a template video → `p-video-animate`
- Talking-head-only / lip-sync host without native scene audio → `p-video-avatar`
- Instruction edit of existing footage → `p-video-edit`

If the request exceeds one clip, **stop** and recommend: `image-to-video` (one narrated beat), `visual-transition-reel` (multi-scene visual), or `narrated-multi-scene` (multi-scene + VO).

## When NOT to use

Use a different skill instead:

| Skill | Description | Install |
| --- | --- | --- |
| `p-video` | Use when someone wants a simple short clip from text or images — quick B-roll, drafts, or start/end frame animation. Not when the brief needs the highest quality or tight lip-sync. | `npx skills add PrunaAI/pruna-skills@p-video -y` |
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

Pass `urls.get` as `input.image` (first frame) and/or `input.last_frame_image` (last frame). Upload TTS/music the same way for `input.audio`.

### Create (async text-to-video — recommended)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video-2' \
  -d '{
    "input": {
      "prompt": "A sports car drifting through a neon-lit city at night, cinematic aerial shot",
      "duration": 5,
      "resolution": "720p",
      "aspect_ratio": "16:9"
    }
  }'
```

Poll and download: follow `pruna-api`.

Complete the random seed ritual from `generation-diversity` before writing prompts — **do not** pass the ritual string as API `seed`.

Billing is per **returned** second (not the requested `duration`). Rate limit: 250 requests per minute.

| Resolution | `draft=false` | `draft=true` |
|------------|---------------|--------------|
| 720p | $0.025 / s | $0.015 / s |
| 1080p | $0.05 / s | $0.03 / s |

### First / last frame (visual transition)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video-2' \
  -d '{
    "input": {
      "prompt": "OPEN: hold wide on wet alley, neon flicker. MID: slow dolly in, rain ticks on pavement. CLOSE: settle on end pose.",
      "image": "https://api.pruna.ai/v1/files/START_ID",
      "last_frame_image": "https://api.pruna.ai/v1/files/END_ID",
      "duration": 5,
      "resolution": "720p",
      "fps": 24
    }
  }'
```

### Scene anchor triple (`image` + `last_frame_image` + `audio`)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video-2' \
  -d '{
    "input": {
      "prompt": "Close-up of a singer performing the uploaded track. Natural lip-sync, expressive face, stage lighting, camera holds steady on the performer.",
      "image": "https://api.pruna.ai/v1/files/SCENE_START",
      "last_frame_image": "https://api.pruna.ai/v1/files/SCENE_END",
      "audio": "https://api.pruna.ai/v1/files/SCENE_NARRATION",
      "resolution": "720p",
      "fps": 24,
      "save_audio": true
    }
  }'
```

**Omit `duration`** when `audio` is set. Clip length = min(audio length, **20s**) — keep TTS ≤ ~19s (`ffprobe` before render). Audio-conditioned jobs bill the **audio length**.

### Create (sync — quick test only)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video-2' \
  -H 'Try-Sync: true' \
  -d '{
    "input": {
      "prompt": "A sports car drifting through a neon-lit city at night, cinematic aerial shot",
      "duration": 5,
      "resolution": "720p",
      "draft": true
    }
  }'
```

## Before generating

1. Complete Prerequisites guide reading order (`generation-diversity` → `video-prompting`).
2. Ritual seed → draft a **dynamic + faithful** motion prompt (section above) → confirm **mode** (T2V / I2V / frame pair / audio), **`duration`** (omit to let the model choose from the prompt, or when audio-driven), **`resolution`**, **`fps`**, **`draft`**, and **`prompt`** with the user.
3. **Pruna notes:** when `image` is set, `aspect_ratio` is ignored. With `audio`, omit `duration` and keep **`save_audio: true`** (default) to keep narration. For **on-camera speech**, lead with **T2V native speech** (`save_audio: true`, no imported `audio`) — pause / line / rest lip-sync is the quality jump vs `p-video`. Imported `audio` keeps a cleaner face; viseme lock is mixed — do not treat a muxed wav as the lip-sync demo. Iterate in **`draft: true`**, then final with `draft: false`. If the request is multi-scene — **stop** (see Skill boundary). Native 4K is not supported.

## Required input

- `prompt` (string)

## Common optional fields

| Field | Role |
|-------|------|
| `image` | First frame — I2V anchor; when set, `aspect_ratio` is ignored (`jpg`, `jpeg`, `png`, `webp`) |
| `last_frame_image` | Optional end-state still |
| `audio` | Audio-conditioned; duration follows audio (capped at **20s**); flac/mp3/wav |
| `duration` | 1–20s; **leave empty** to let the model choose length from the prompt; ignored if `audio` set |
| `resolution` | `720p` (default) or `1080p` |
| `fps` | `24` (default) or `48` |
| `aspect_ratio` | When no `image`: `16:9` (default), `9:16`, `4:3`, `3:4`, `3:2`, `2:3`, `1:1` |
| `draft` | `true` = cheaper, faster preview ($0.015/s 720p, $0.03/s 1080p); `false` (default) = final |
| `save_audio` | Keep model-generated or uploaded audio on output (default `true`) |
| `prompt_upsampling` | Enhance the prompt (default `true`) |
| `seed`, `disable_safety_filter` | Reproducibility / client policy |

## Related

Related skills:

| Skill | Description | Install |
| --- | --- | --- |
| `p-video` | Use when someone wants a simple short clip from text or images — quick B-roll, drafts, or start/end frame animation. Not when the brief needs the highest quality or tight lip-sync. | `npx skills add PrunaAI/pruna-skills@p-video -y` |
| `gemini-3.1-flash-tts` | Use when someone needs spoken narration or voiceover — explainer tracks, documentary lines, or voice to pair with generated video. | `npx skills add PrunaAI/pruna-skills@gemini-3.1-flash-tts -y` |
| `image-to-video` | Use when someone wants one short film beat from images — a narrated scene, story moment, or cinematic B-roll with optional voiceover. | `npx skills add PrunaAI/pruna-skills@image-to-video -y` |
| `visual-transition-reel` | Use when someone wants a montage with transitions between shots — action-sequence reel or multi-scene piece where narration is optional. | `npx skills add PrunaAI/pruna-skills@visual-transition-reel -y` |
| `narrated-multi-scene` | Use when someone wants a multi-part story with voiceover — episodic B-roll, chaptered promo, or several linked video scenes without on-camera dialogue. | `npx skills add PrunaAI/pruna-skills@narrated-multi-scene -y` |
| `p-video-avatar` | Use when someone wants a person on camera speaking a script — lip-synced host, spokesperson, or narrated avatar from a portrait photo. | `npx skills add PrunaAI/pruna-skills@p-video-avatar -y` |
| `p-video-animate` | Use when someone wants a photo to move like another video — motion transfer, dance remixes, or performance variations from a template clip. | `npx skills add PrunaAI/pruna-skills@p-video-animate -y` |
| `video-editing` | Use when assembling or polishing already-rendered clips with ffmpeg — concat, crossfades, burned captions and subtitles, text/logo overlays, before/after sliders, background music beds, platform export — or when composing a multi-layer HTML combination video with Hyperframes. Not for AI video generation, prompt craft, or model-based video edits. | `npx skills add PrunaAI/pruna-skills@video-editing -y` |

