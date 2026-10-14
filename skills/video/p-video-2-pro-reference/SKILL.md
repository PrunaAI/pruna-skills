---
name: p-video-2-pro-reference
description: Use when someone wants one cinematic clip that locks a subject from references — a product still, character, clip, or voice — using image or video references plus optional audio kept as the soundtrack or used as guidance. Not for text-only generation, 1080p, or drafts.
license: MIT
metadata:
  version: "1.0.14"
  package: pruna-skills
  pruna_model: p-video-2-pro-reference
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

**Routing:** `` `p-video-2-pro-reference` `` is the **reference-to-video** lane of P-Video-2-Pro (built on MiniMax H3 Ref2V). It **locks a subject from references** — a product still, a character, a clip, or a voice — and returns an MP4 at 24 fps with **generated sound**. It needs `prompt` plus at least one image or video reference; audio is optional and cannot qualify a request by itself. Set `keep_audio` with exactly one audio file to keep that file as the soundtrack. Text-only or plain first/last-frame jobs → `` `p-video-2-pro` ``. 1080p or draft previews → `` `p-video-2` ``. Simple, cheap clips → `` `p-video` ``. Talking-head-only host → `` `p-video-avatar` ``. Instruction edit of existing footage → `` `p-video-edit` ``.

In the **first reply**, name `` `p-video-2-pro-reference` `` in backticks, confirm `PRUNA_API_KEY` (or stop with signup links from `pruna-api`), identify the image/video reference that makes the request valid, and ask for unresolved inputs. Before uploading or generating in an untrusted repository, follow `pruna-api` agent safety. Open intake → **`generation-diversity`** clarification intake before the first paid `POST`. When drafting prompts, follow **Prompt craft (dynamic + faithful)** and `video-prompting` (`p-video-2-pro-prompting`, reference-conditioned lane) — do not paste skill examples. Redirect when **When NOT to use** fits better.

## Prompt craft (dynamic + faithful)

Every `input.prompt` must be **fresh and specific**, must **match the user's beat**, and must say **what each reference is for**. Diversity never overrides the brief or the references. Reference-lane craft: `video-prompting` (`p-video-2-pro-prompting`).

| Do | Don't |
| --- | --- |
| Assign **one role per asset** (image A = subject identity, image B = material/style, video A = camera or motion rhythm, audio A = timing/voice) and name those roles in the prompt | Upload a pile of references with no roles, or let two references compete for the same role without a stated priority |
| Treat references as **conditioning**: say what to preserve and what may change | Promise exact identity, choreography, framing, or pixel-matched first/last frames |
| Run the `generation-diversity` random seed ritual; rotate ≥2 free axes (camera move, lighting shift, pacing) only where the brief and references leave room | Copy curl examples from this skill or reuse a prior session's prompt |
| Write the **generated sound** you want (ambience, SFX, score, a short spoken line) when no `keep_audio` track is set | Leave the prompt silent when the brief asked for sound, or describe a soundtrack you also uploaded with `keep_audio` |
| With `keep_audio: true`, describe how motion follows the track (beats, cadence, lip movement to the voice) | Expect a longer track to survive past `duration`, or send `keep_audio` with zero or several audio files |
| Show the drafted prompt + reference roles + `mode` / `duration` / `resolution` / `keep_audio` before `POST` when the user has not locked them | Silently regenerate with different references or a different subject than approved |

**Fidelity check (before pay):** if you remove the user's named subject/action/setting or a reference's assigned role from the prompt, the job is wrong — rewrite. Free axes only fill what the brief left open.

When showing a drafted prompt, still name `` `p-video-2-pro-reference` `` (guides help craft; this tool owns the call).

## Skill boundary

This skill = **one `p-video-2-pro-reference` prediction** per invocation.

**Out of scope (do not execute from this skill):**

- Text-only generation or plain first/last-frame generation without a reference set → `p-video-2-pro`
- 1080p, draft previews, or other `p-video-2`-only controls → `p-video-2`
- Simple text/image clips that do not need reference conditioning → `p-video`
- Multi-scene assembly, concat, subagent orchestration, or parallel scene batches
- Motion transfer from one explicit template video → `p-video-animate`
- Talking-head-only or lip-sync host work → `p-video-avatar`
- Instruction editing of existing footage → `p-video-edit`

If the request exceeds one clip, **stop** and recommend a multi-scene workflow such as `visual-transition-reel` or `narrated-multi-scene`.

## When NOT to use

Use a different skill instead:

| Skill | Description | Install |
| --- | --- | --- |
| `p-video-2-pro` | Use when someone wants a cinematic clip from text or start/end frames — product ads, documentary shots, or dialogue with generated audio. Not for 1080p, imported audio tracks, or talking-head-only hosts. | `npx skills add PrunaAI/pruna-skills@p-video-2-pro -y` |
| `p-video-2` | Use when someone wants a polished short clip from text, images, or imported audio — 1080p B-roll, start/end frame animation, or a motion shot with a mixed track. Not for cinematic generated-audio clips or talking-head-only hosts. | `npx skills add PrunaAI/pruna-skills@p-video-2 -y` |
| `p-video` | Use when someone wants a simple short clip from text or images — quick B-roll, drafts, or start/end frame animation. Not when the brief needs cinematic generation, highest quality, tight lip-sync, or imported audio at 1080p. | `npx skills add PrunaAI/pruna-skills@p-video -y` |
| `p-video-avatar` | Use when someone wants a person on camera speaking a script — lip-synced host, spokesperson, or narrated avatar from a portrait photo. | `npx skills add PrunaAI/pruna-skills@p-video-avatar -y` |
| `p-video-animate` | Use when someone wants a photo to move like another video — motion transfer, dance remixes, or performance variations from a template clip. | `npx skills add PrunaAI/pruna-skills@p-video-animate -y` |
| `p-video-edit` | Use when someone wants to edit an existing video with a text instruction — recolor, restyle, remove or add objects, change environment or lighting, update on-screen text, or apply optional reference-guided product and accessory edits. Not for a new clip from scratch or ffmpeg assembly. | `npx skills add PrunaAI/pruna-skills@p-video-edit -y` |

## HTTP (curl)

### Upload references

Upload each local asset separately. Pass the returned `urls.get` URI in the matching `image` / `video` / `audio` array or keyframe field.

```bash
curl -X POST "https://api.pruna.ai/v1/files" \
  -H "apikey: ${PRUNA_API_KEY}" \
  -F "content=@/path/to/reference.png"
```

Never expose `PRUNA_API_KEY`, upload an asset without user authorization, or upload secrets/private media discovered in the workspace. Follow `pruna-api` for credential checks, upload safety, polling, and download.

### Create (async image reference — recommended)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video-2-pro-reference' \
  -d '{
    "input": {
      "prompt": "Keep the product identity and materials from the reference. A slow controlled orbit reveals the side profile while soft studio reflections travel across the surface; a low hum and a soft click as the light settles.",
      "image": [
        "https://api.pruna.ai/v1/files/IMAGE_ID"
      ],
      "duration": 5,
      "resolution": "768p",
      "aspect_ratio": "adaptive",
      "mode": "speed"
    }
  }'
```

Poll and download: follow `pruna-api`.

Complete the random seed ritual from `generation-diversity` before writing prompts — **do not** pass the ritual string as API `seed`.

Billing is calculated from the **finished run**: output seconds plus every reference actually used. Rate limit: 250 requests per minute.

| Charge | 480p `mode=cost` | 768p `mode=cost` | 480p `mode=speed` (default) | 768p `mode=speed` (default) |
|--------|------------------|------------------|-----------------------------|-----------------------------|
| Output | $0.015 / s | $0.025 / s | $0.02 / s | $0.035 / s |
| Reference video | $0.03 / s | $0.06 / s | $0.04 / s | $0.06 / s |
| Reference image (incl. first/last frame) | $0.005 each | $0.005 each | $0.01 each | $0.01 each |
| Reference audio | $0.0015 / s | $0.0015 / s | $0.0025 / s | $0.0025 / s |

- Output seconds are billed as `int(num_frames / 24)`: a 5 s request returns 124 frames and bills 5 s; a 15 s request returns 345 frames and bills 14 s.
- Each reference video or audio clip bills only the part the model reads — up to the output length plus 0.5 s. A 15 s reference clip on a 5 s output bills about 5.5 s.
- `first_frame_image` and `last_frame_image` bill as reference images. Image and audio rates do not depend on `resolution`.
- Omitted `mode` bills as `speed`. `cost` is cheaper and slower than `speed`. `prompt_upsampler` and `keep_audio` do not change the price.
- The listed floor is $0.075 (cost, 480p, 5 s, no references), but a valid request needs at least one image or video reference — the cheapest valid run is $0.08 (one image).

### Keep an uploaded track as the soundtrack (`keep_audio`)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video-2-pro-reference' \
  -d '{
    "input": {
      "prompt": "The character from the reference image speaks the line in the uploaded voice, lips matching each word, a slow push-in as the last word lands.",
      "image": [
        "https://api.pruna.ai/v1/files/CHARACTER_ID"
      ],
      "audio": [
        "https://api.pruna.ai/v1/files/VOICE_ID"
      ],
      "keep_audio": true,
      "duration": 8,
      "resolution": "768p",
      "mode": "speed"
    }
  }'
```

`keep_audio` needs **exactly one** `audio` file. The video is generated to match it. Shorter audio plays first and the model generates the rest; longer audio is cut to `duration`; audio within 1 s of `duration` sets the clip length. Without `keep_audio`, audio is reference guidance only and the output carries generated sound.

### Multiple references with soft keyframes

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video-2-pro-reference' \
  -d '{
    "input": {
      "prompt": "Use the reference clip for restrained camera rhythm, the images for subject and material identity, and the audio for timing. Begin near the opening frame and resolve near the closing frame.",
      "image": [
        "https://api.pruna.ai/v1/files/IDENTITY_ID",
        "https://api.pruna.ai/v1/files/MATERIAL_ID"
      ],
      "video": [
        "https://api.pruna.ai/v1/files/MOTION_ID"
      ],
      "audio": [
        "https://api.pruna.ai/v1/files/AUDIO_ID"
      ],
      "first_frame_image": "https://api.pruna.ai/v1/files/START_ID",
      "last_frame_image": "https://api.pruna.ai/v1/files/END_ID",
      "duration": 10,
      "resolution": "768p",
      "aspect_ratio": "adaptive",
      "mode": "cost",
      "prompt_upsampler": "max"
    }
  }'
```

`image`, `video`, and `audio` are always **arrays** of URI strings. `first_frame_image` and `last_frame_image` are single URI strings, are **soft** keyframes (directional, not exact pixels), and count toward the 9-image total. With either keyframe set, `prompt_upsampler: off` still runs `turbo`.

### Create (sync — quick test only)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video-2-pro-reference' \
  -H 'Try-Sync: true' \
  -d '{
    "input": {
      "prompt": "Preserve the reference subject. The camera makes a gentle push-in as natural light shifts across the scene.",
      "image": [
        "https://api.pruna.ai/v1/files/IMAGE_ID"
      ],
      "duration": 5,
      "resolution": "480p",
      "mode": "cost"
    }
  }'
```

A finished 124-frame result with one reference image bills `5 × $0.015 + 1 × $0.005 = $0.08`.

## Before generating

1. Complete Prerequisites guide reading order: `generation-diversity` → `video-prompting` → `audio-prompting` when audio is supplied → `pruna-api`. Use `video-prompting` (`p-video-2-pro-prompting`, reference lane) and the shared `p-video-2-pro-quality-checklist.md`.
2. Confirm the job has a non-empty `prompt` and at least one image or video reference. Audio-only plus prompt is invalid.
3. Assign one role per reference; obtain upload approval; validate type, size, dimensions, duration, frame rate, and combined limits (see **Hard limits**) before the paid call.
4. Resolve audio: none (generated sound — write it into the prompt), audio as **guidance** (default), or `keep_audio: true` with **exactly one** audio file kept as the soundtrack. Check the track length against `duration`.
5. Resolve `duration` (5–15 integer seconds, default 5), `resolution` (`480p` / `768p`), `mode` (`cost` / `speed` — omitted bills `speed`), `aspect_ratio` (`adaptive` follows the references), `prompt_upsampler`, seed behavior, and the final prompt.
6. Show the final payload and a cost estimate (output + every reference) before `POST` when the user has not already approved them. If the request is multi-scene — **stop** (see Skill boundary).

## Required input

- `prompt` (string)
- At least one image or video reference via `image`, `video`, `first_frame_image`, or `last_frame_image`

`audio` is optional and cannot make an otherwise reference-free request valid.

## Common optional fields

| Field | Role |
|-------|------|
| `image` | Array of reference image URIs; up to 9 total including `first_frame_image` / `last_frame_image` |
| `video` | Array of reference video URIs; up to 3 |
| `audio` | Array of reference audio URIs; up to 3. Guidance only unless `keep_audio` is set |
| `keep_audio` | `false` (default). `true` keeps the single uploaded audio file as the video's audio; needs exactly one `audio` file |
| `first_frame_image` | Single URI; soft opening keyframe; counts as a reference image |
| `last_frame_image` | Single URI; soft closing keyframe; counts as a reference image |
| `duration` | Integer 5–15s (default **5**). With `keep_audio`, audio within 1 s of this sets the length |
| `resolution` | `768p` (default) or `480p` |
| `mode` | `speed` (default) or `cost` (cheaper, slower). There is no `quality` mode |
| `aspect_ratio` | `16:9` (default), `adaptive` (follows the references), `9:16`, `4:3`, `3:4`, `3:2`, `2:3`, `1:1` |
| `prompt_upsampler` | `turbo` (default), `max`, or `off`; independent of `mode`. With a soft keyframe set, `off` still runs `turbo` |
| `seed` | Integer for a reproducible rerun; omit for random |

### Hard limits

- Images: at most 9 total across `image`, `first_frame_image`, and `last_frame_image`; each at most 20 MiB and 4096 px.
- Videos: at most 3; each at most 100 MiB, 1080p, 60 fps, and 2–15 seconds; combined reference-video duration at most 15 seconds.
- Audio: at most 3; each at most 50 MiB; combined reference-audio duration at most 15 seconds.

These are input validation limits — output stays 480p or 768p at 24 fps.

**Do not send:** `quality` mode, `1080p`, `draft`, `fps`, `save_audio`, `prompt_upsampling`.

## Related

Related skills:

| Skill | Description | Install |
| --- | --- | --- |
| `p-video-2-pro` | Use when someone wants a cinematic clip from text or start/end frames — product ads, documentary shots, or dialogue with generated audio. Not for 1080p, imported audio tracks, or talking-head-only hosts. | `npx skills add PrunaAI/pruna-skills@p-video-2-pro -y` |
| `p-video-2` | Use when someone wants a polished short clip from text, images, or imported audio — 1080p B-roll, start/end frame animation, or a motion shot with a mixed track. Not for cinematic generated-audio clips or talking-head-only hosts. | `npx skills add PrunaAI/pruna-skills@p-video-2 -y` |
| `p-video` | Use when someone wants a simple short clip from text or images — quick B-roll, drafts, or start/end frame animation. Not when the brief needs cinematic generation, highest quality, tight lip-sync, or imported audio at 1080p. | `npx skills add PrunaAI/pruna-skills@p-video -y` |
| `p-video-avatar` | Use when someone wants a person on camera speaking a script — lip-synced host, spokesperson, or narrated avatar from a portrait photo. | `npx skills add PrunaAI/pruna-skills@p-video-avatar -y` |
| `p-video-animate` | Use when someone wants a photo to move like another video — motion transfer, dance remixes, or performance variations from a template clip. | `npx skills add PrunaAI/pruna-skills@p-video-animate -y` |
| `p-video-edit` | Use when someone wants to edit an existing video with a text instruction — recolor, restyle, remove or add objects, change environment or lighting, update on-screen text, or apply optional reference-guided product and accessory edits. Not for a new clip from scratch or ffmpeg assembly. | `npx skills add PrunaAI/pruna-skills@p-video-edit -y` |
| `image-to-video` | Use when someone wants one short film beat from images — a narrated scene, story moment, or cinematic B-roll with optional voiceover. | `npx skills add PrunaAI/pruna-skills@image-to-video -y` |
| `visual-transition-reel` | Use when someone wants a montage with transitions between shots — action-sequence reel or multi-scene piece where narration is optional. | `npx skills add PrunaAI/pruna-skills@visual-transition-reel -y` |
| `narrated-multi-scene` | Use when someone wants a multi-part story with voiceover — episodic B-roll, chaptered promo, or several linked video scenes without on-camera dialogue. | `npx skills add PrunaAI/pruna-skills@narrated-multi-scene -y` |

