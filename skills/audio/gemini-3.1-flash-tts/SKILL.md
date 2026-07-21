---
name: gemini-3.1-flash-tts
description: Use when someone needs spoken narration or voiceover — explainer tracks, documentary lines, or voice to pair with generated video.
license: MIT
metadata:
  version: "1.0.6"
  package: pruna-skills
  provider: replicate
  replicate_model: google/gemini-3.1-flash-tts
---

## Prerequisites

Install and load these skills before generating (skip if already in context via `@pruna`):

| Skill | Description | Install |
| --- | --- | --- |
| `generation-diversity` | Use when writing any generative prompt — ritual seed, explicit structure, scenario axes, and quality gates before paid API calls. | `npx skills add PrunaAI/pruna-skills@generation-diversity -y` |
| `audio-prompting` | Use when crafting TTS, music, or bed prompts for any generative audio model — director style, song structure, and post-production layering. | `npx skills add PrunaAI/pruna-skills@audio-prompting -y` |
| `video-prompting` | Use when crafting video or motion prompts for any generative model — dramaturgy, camera, physics-safe motion, frame anchors, and clip chaining. | `npx skills add PrunaAI/pruna-skills@video-prompting -y` |
| `pruna-api` | Use before any Pruna or Replicate HTTP call — credentials, upload/poll/download, parallel batches, and agent safety. | `npx skills add PrunaAI/pruna-skills@pruna-api -y` |

Or install the full suite once: `npx skills add PrunaAI/pruna-skills@pruna -y`

Follow each skill's **Before generating** / craft sections — do not restate guide content here.

## When NOT to use

Use a different skill instead:

| Skill | Description | Install |
| --- | --- | --- |
| `p-video-avatar` | Use when someone wants a person on camera speaking a script — lip-synced host, spokesperson, or narrated avatar from a portrait photo. | `npx skills add PrunaAI/pruna-skills@p-video-avatar -y` |
| `music-2.5` | Use when someone wants an original AI song with vocals — sung lyrics, a style prompt track, or source audio for a music video. | `npx skills add PrunaAI/pruna-skills@music-2.5 -y` |
| `stable-audio-2.5` | Use when someone wants light instrumental background music — an ambient bed under dialogue or underscore for reels and explainers. | `npx skills add PrunaAI/pruna-skills@stable-audio-2.5 -y` |

## Environment

```bash
export REPLICATE_API_TOKEN=r8_...
```

Requires **`ffmpeg`** / **`ffprobe`** when trimming, concatenating scene VO, or mixing with a bed.

## HTTP (curl)

```bash
curl -s -X POST \
  -H "Authorization: Bearer ${REPLICATE_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "text": "[warmly] The plush went flying. [short pause] And then it was gone.",
      "voice": "Sulafat",
      "prompt": "Warm storybook narrator, gentle pace, empathetic, no announcer voice.",
      "language_code": "en-US"
    }
  }' \
  "https://api.replicate.com/v1/models/google/gemini-3.1-flash-tts/predictions"
```

Poll `urls.get` until `status` is `succeeded`; download `output` (audio URL). Shared client: [pruna-api / Replicate HTTP in tool skill curl/ffmpeg (no shared scripts)).

## Before generating

1. Complete Prerequisites guide reading order.
2. Confirm **`text`**, **`voice`**, **`prompt`**, and **`language_code`** with the user.
3. **Model notes:** combined `text` + `prompt` ≤ ~8,000 bytes; output capped ~655s. When TTS feeds **`p-video`** as `input.audio`, keep each line **≤ ~19s** (`ffprobe`) — P-API clips audio at **20s**. Common voices: `Kore`, `Aoede`, `Sulafat`, `Achird`, `Charon`, `Puck`, `Vindemiatrix` — full list on the [Replicate readme](https://replicate.com/google/gemini-3.1-flash-tts/readme).

## Required input

- `text` (string) — spoken copy; supports inline `[tags]`. Max ~4,000 bytes.

## Common optional fields

- `voice` (default `Kore`)
- `prompt` — style / director notes (max ~4,000 bytes)
- `language_code` — BCP-47 (default `en-US`)

Inline tags (examples): `[sigh]` `[laughing]` `[whispering]` `[short pause]` `[medium pause]` `[long pause]` `[excitedly]`.

## Typical next steps

Common follow-ons after this skill:

| Skill | Description | Install |
| --- | --- | --- |
| `p-video` | Use when someone wants one short video clip from text or images — B-roll, start/end frame animation, or a quick motion shot. Not for full multi-scene films or lip-synced hosts. | `npx skills add PrunaAI/pruna-skills@p-video -y` |
| `p-video-avatar` | Use when someone wants a person on camera speaking a script — lip-synced host, spokesperson, or narrated avatar from a portrait photo. | `npx skills add PrunaAI/pruna-skills@p-video-avatar -y` |
| `stable-audio-2.5` | Use when someone wants light instrumental background music — an ambient bed under dialogue or underscore for reels and explainers. | `npx skills add PrunaAI/pruna-skills@stable-audio-2.5 -y` |
| `narrated-multi-scene` | Use when someone wants a multi-part story with voiceover — episodic B-roll, chaptered promo, or several linked video scenes without on-camera dialogue. | `npx skills add PrunaAI/pruna-skills@narrated-multi-scene -y` |

