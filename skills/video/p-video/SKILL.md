---
name: p-video
description: Use when someone wants one short video clip from text or images — B-roll, start/end frame animation, or a quick motion shot. Not for full multi-scene films or lip-synced hosts.
license: MIT
metadata:
  version: "1.0.10"
  package: pruna-skills
  pruna_model: p-video
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

In the **first reply**, name `` `p-video` `` in backticks, confirm `PRUNA_API_KEY` (or stop with signup links from `pruna-api`), then ask for required inputs. Open intake → **`generation-diversity`** clarification intake before the first `POST`. When drafting motion prompts, follow **Prompt craft (dynamic + faithful)** — do not paste skill examples. Redirect when **When NOT to use** fits better.

## Prompt craft (dynamic + faithful)

Every `input.prompt` must be **fresh and specific**, and must **match the user's beat**. Diversity never overrides the brief.

| Do | Don't |
| --- | --- |
| Run the `generation-diversity` random seed ritual; state it; rotate ≥2 free axes (camera move, lighting shift, texture, pacing) when the brief allows | Copy curl examples from this skill (`rain-slick street`, `dog tosses plush`, …) or reuse a prior session's prompt |
| Lock user-required facts first (subject, action beat, OPEN/MID/CLOSE when frame-anchored, narration sync when `audio` is set) | Swap the subject or motion for a “cooler” clip that ignores the request |
| Structure with `video-prompting` dramaturgy — one frozen action per beat, physics-safe motion, camera grammar | Vague mood-only strings (`cinematic vibe, neon energy`) |
| When `audio` is set, motion and pacing must **match the narration beat** | Drift to unrelated action while VO plays |
| Show the drafted prompt + mode fields before `POST` when the user has not locked wording | Silent regen with a different subject or beat than approved |

**Fidelity check (before pay):** if you remove the user's named subject/action/setting from the prompt, the job is wrong — rewrite. Free axes only fill what the brief left open.

When showing a drafted prompt, still name `` `p-video` `` (guides help craft; this tool owns the call).

## Skill boundary

This skill = **one `p-video` prediction** per invocation.

**Out of scope (do not execute from this skill):**

- Multi-scene assembly, concat, subagent orchestration, or parallel scene batches
- Motion transfer from a template video → `p-video-animate`
- Talking-head / lip-sync → `p-video-avatar`

If the request exceeds one clip, **stop** and recommend: `image-to-video` (one narrated beat), `visual-transition-reel` (multi-scene visual), or `narrated-multi-scene` (multi-scene + VO).

## When NOT to use

Use a different skill instead:

| Skill | Description | Install |
| --- | --- | --- |
| `p-video-avatar` | Use when someone wants a person on camera speaking a script — lip-synced host, spokesperson, or narrated avatar from a portrait photo. | `npx skills add PrunaAI/pruna-skills@p-video-avatar -y` |
| `p-video-animate` | Use when someone wants a photo to move like another video — motion transfer, dance remixes, or performance variations from a template clip. | `npx skills add PrunaAI/pruna-skills@p-video-animate -y` |
| `p-video-replace` | Use when someone wants to swap a person, outfit, or product inside existing footage while keeping the camera move and audio. | `npx skills add PrunaAI/pruna-skills@p-video-replace -y` |
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
  -H 'Model: p-video' \
  -d '{
    "input": {
      "prompt": "Slow dolly in on rain-slick street at night, neon reflections, distant traffic hiss",
      "duration": 5,
      "resolution": "720p",
      "aspect_ratio": "16:9"
    }
  }'
```

Poll and download: follow `pruna-api`.

Complete the random seed ritual from `generation-diversity` before writing prompts — **do not** pass the ritual string as API `seed`.

### First / last frame (visual transition)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video' \
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
  -H 'Model: p-video' \
  -d '{
    "input": {
      "prompt": "Dog tosses plush upward, tail wagging, motion matches narrator, warm light",
      "image": "https://api.pruna.ai/v1/files/SCENE_START",
      "last_frame_image": "https://api.pruna.ai/v1/files/SCENE_END",
      "audio": "https://api.pruna.ai/v1/files/SCENE_NARRATION",
      "resolution": "720p",
      "fps": 24,
      "save_audio": true
    }
  }'
```

**Omit `duration`** when `audio` is set. Clip length = min(audio length, **20s**) — keep TTS ≤ ~19s (`ffprobe` before render).

## Before generating

1. Complete Prerequisites guide reading order (`generation-diversity` → `video-prompting`).
2. Ritual seed → draft a **dynamic + faithful** motion prompt (section above) → confirm **mode** (T2V / I2V / frame pair / audio), **`duration`** (unless audio-driven), **`resolution`**, **`fps`**, **`draft`**, and **`prompt`** with the user.
3. **Pruna notes:** when `image` is set, `aspect_ratio` is ignored. With `audio`, omit `duration` and set **`save_audio: true`** to keep narration. Prefer uploaded VO over post-mux. If the request is multi-scene — **stop** (see Skill boundary).

## Required input

- `prompt` (string)

## Common optional fields

| Field | Role |
|-------|------|
| `image` | First frame — I2V anchor; when set, `aspect_ratio` is ignored |
| `last_frame_image` | Optional end-state still |
| `audio` | Audio-conditioned; duration follows audio (capped at **20s**); flac/mp3/wav |
| `duration` | 1–20s (ignored if `audio` set) |
| `resolution` | `720p` (default) or `1080p` |
| `fps` | `24` (default) or `48` |
| `aspect_ratio` | When no `image`: `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`, `1:1` |
| `draft` | `true` ≈ 4× faster/cheaper preview; `false` = final |
| `save_audio` | Keep model-generated or uploaded audio on output |
| `seed`, `prompt_upsampling`, `disable_safety_filter` | Reproducibility / client policy |

## Related

Related skills:

| Skill | Description | Install |
| --- | --- | --- |
| `gemini-3.1-flash-tts` | Use when someone needs spoken narration or voiceover — explainer tracks, documentary lines, or voice to pair with generated video. | `npx skills add PrunaAI/pruna-skills@gemini-3.1-flash-tts -y` |
| `image-to-video` | Use when someone wants one short film beat from images — a narrated scene, story moment, or cinematic B-roll with optional voiceover. | `npx skills add PrunaAI/pruna-skills@image-to-video -y` |
| `visual-transition-reel` | Use when someone wants a montage with transitions between shots — action-sequence reel or multi-scene piece where narration is optional. | `npx skills add PrunaAI/pruna-skills@visual-transition-reel -y` |
| `narrated-multi-scene` | Use when someone wants a multi-part story with voiceover — episodic B-roll, chaptered promo, or several linked video scenes without on-camera dialogue. | `npx skills add PrunaAI/pruna-skills@narrated-multi-scene -y` |
| `p-video-avatar` | Use when someone wants a person on camera speaking a script — lip-synced host, spokesperson, or narrated avatar from a portrait photo. | `npx skills add PrunaAI/pruna-skills@p-video-avatar -y` |
| `p-video-animate` | Use when someone wants a photo to move like another video — motion transfer, dance remixes, or performance variations from a template clip. | `npx skills add PrunaAI/pruna-skills@p-video-animate -y` |
| `video-editing` | Use when assembling or polishing already-rendered clips with ffmpeg — concat, crossfades, burned captions and subtitles, text/logo overlays, before/after sliders, background music beds, platform export — or when composing a multi-layer HTML combination video with Hyperframes. Not for AI video generation, prompt craft, or model-based video edits. | `npx skills add PrunaAI/pruna-skills@video-editing -y` |

