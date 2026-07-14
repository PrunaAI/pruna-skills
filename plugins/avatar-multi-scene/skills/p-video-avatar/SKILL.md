---
name: p-video-avatar
description: Use when the user wants a talking-head video, lip-synced host or spokesperson clip, on-camera performance from a portrait plus script, or narrated avatar footage.
license: MIT
metadata:
  version: "0.0.2"
  pruna_model: p-video-avatar
---

# p-video-avatar (Pruna)

Talking-head video from one image plus **either** `voice_script` **or** `audio` (if both, audio wins). Full parameters: [P-Video-Avatar (Pruna docs)](https://docs.pruna.ai/en/stable/docs_pruna_endpoints/performance_models/p-video-avatar.html).

**Dynamic personas & scenarios:** [realistic-persona-showcase.md](./references/realistic-persona-showcase.md) · examples: [example-prompt.md](./references/realistic-persona-example-prompt.md)

Shared HTTP patterns: [pruna-api.md](./references/pruna-api.md) (upload, [poll](#poll), [download](#download))

## HTTP (curl)

### Upload portrait

```bash
curl -X POST "https://api.pruna.ai/v1/files" \
  -H "apikey: ${PRUNA_API_KEY}" \
  -F "content=@/path/to/portrait.png"
```

Use `urls.get` as `input.image`.

### Create (async — recommended)

See **Example: async** below. Poll and download: [pruna-api.md](./references/pruna-api.md#poll).

## Before generating

Follow [avatar-single-scene](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/avatar-single-scene/skills/avatar-single-scene/SKILL.md) or [avatar-multi-scene](../avatar-multi-scene/SKILL.md): **[generation diversity](./references/generation-diversity.md)** first, then **natural human `voice_script`**, **realistic conversational `voice_prompt`**, **per-scene dynamic `video_prompt`**, **locked hero plate URL**, **one fixed `voice` per recurring character**, **explicit user confirmation** before any **`POST /v1/predictions`**, then emit and run the agreed generation steps.

When calling the model directly for a small experiment: **random seed ritual (SSoT)** first, then confirm **`image`** URL (approved still from `/v1/files`), exact **`voice_script`**, **`voice`** / **`voice_language`**, **`voice_prompt`** (human delivery—not script text), **`video_prompt`** (camera/motion), and **`resolution`** with the user. Run [p-video-avatar-quality-checklist.md](./references/p-video-avatar-quality-checklist.md) on stills and outputs.

## Dynamic realistic personas (production)

A believable avatar needs **three layers** — not a static face on the default motion prompt:

1. **Slop-gated still** — from **`p-image`** / **`p-image-edit`** / optional **`p-image-try-on`**; **any medium** (photoreal, cel anime, clay, CG 3D) with mouth visible; diverse cast, angle, and setting per [realistic-persona-showcase.md](./references/realistic-persona-showcase.md)
2. **Human voice** — natural **`voice_script`** + short realistic **`voice_prompt`** (never brochure copy in either field)
3. **Unique motion per clip** — distinct **`video_prompt`** per scene (angle, gesture, glance, handheld vs dolly). **Do not** ship multi-scene reels where every row uses `medium close-up, gentle dolly push-in`

**Stylized hosts (anime, clay, 3D):** same mouth-visibility gate; match **`voice_prompt`** and **`video_prompt`** energy to the style (*anime*: slightly more expressive motion; *documentary*: restrained). Cross-style reels need **separate hero stills per `visual_style_tag`** — do not edit photoreal into anime from one anchor.

**Upstream plate quality caps avatar quality.** Regenerate mushy or synthetic stills before avatar. For fashion UGC: photoreal **`p-image`** → **`p-image-try-on`** → slop gate → avatar with same approved plate URL.

Multi-scene: pair each clip’s **`video_prompt`** with a matching **`p-image-edit`** still (background/angle delta only). See [avatar-multi-scene/prompt-templates.md](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/core/avatar-multi-scene/prompt-templates.md) scene table.

**Multi-scene:** after confirmation, create **all** avatar jobs **in parallel** (async, no `Try-Sync`); batch-poll. Prefer **one subagent per clip** — see [parallel-execution.md](./references/parallel-execution.md).

## Realistic human voice (defaults for social / founder content)

| Field | Guidance |
|-------|----------|
| **`voice_script`** | Speakable copy: contractions, short sentences, light fillers (*"Hey —"*, *"right?"*). Avoid brochure language. |
| **`voice_prompt`** | How they *sound*: *"Natural conversational tone like a founder on LinkedIn, relaxed pacing, real pauses, honest not salesy."* Never paste product names or script lines here. |
| **`video_prompt`** | **Unique per clip** — angle, push-in, gesture, setting motion, glance beats. Never copy one string across a multi-scene reel. Default `The person is talking.` is quick-test only. |
| **`seed`** | Optional API reproducibility only — pass **`api_seed`** when user locks an integer. Ritual string is **not** passed to API. |

**Motion-template use case (for `p-video-animate` beats):** When this model generates a **source motion video**, prompts must explicitly request **speaking** — `clear lip movement`, explain gestures, `speaks directly to camera`. Motion-source stills need `mouth clearly visible ready to speak`. See [animate-beats.md](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/core/avatar-multi-scene/animate-beats.md).

Templates and good/bad pairs: [avatar-multi-scene/prompt-templates.md](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/core/avatar-multi-scene/prompt-templates.md).

## Field names (JSON)

Pruna P-API uses **snake_case** in `input`: `voice_script`, `video_prompt`, `voice_prompt`, `voice_language`. Some other products use camelCase; map accordingly.

## Required input

- `image` (string URL to jpg/jpeg/png/webp)

Plus **one of**:

- `voice_script` + optional `voice`, `voice_prompt`, `voice_language`, `video_prompt`, `resolution`, or
- `audio` (URL to flac/mp3/wav)

## Common optional fields

- `voice` (default `Zephyr (Female)`); see model doc for full voice list
- `resolution`: `720p` (default) or `1080p`
- `video_prompt` (default `The person is talking.`)
- `voice_prompt` (style / tone; keep short—can leak into performance if too verbose)
- `seed`, `disable_safety_filter`, `disable_prompt_upsampling`
- `negative_prompt` + `negative_prompt_strength` — **experimental** text/overlay suppression (see below)

## Negative prompt (suppress on-screen text)

Pruna exposes **experimental** negative prompting on `p-video-avatar` to reduce burned-in subtitles, captions, and other text artifacts — especially when the start frame came from a still that tempted the model toward labels or signage.

| Field | Default | Rule |
|-------|---------|------|
| `negative_prompt` | `""` | Comma-separated elements to **suppress** — not things you want in frame |
| `negative_prompt_strength` | `0` | **Both** must be set: non-empty prompt **and** strength **> 0**, or the API ignores them |

**Starter `negative_prompt` (text triggers):**

```text
subtitles, captions, on-screen text, burned-in text, watermark, logo, typography, letters, words, readable signage, UI overlay, lower third, chyron, title card, price tag, packaging label, menu text
```

Start `negative_prompt_strength` around **0.3–0.4** and tune per asset. Higher values can drift identity, motion, or background — increase gradually.

**Still-side prevention (primary):** positive-only still lines (`plain unmarked walls`, `unprinted props`) — never `no text` or `avoid signage` in creative prompts. `negative_prompt` on the API is a **suppression token list** (nouns), not creative wording. Use it as a safety net, not a substitute for clean stills.

**Workflow plans:** interactive-explainer runner applies defaults from `plan.defaults.avatar_negative_prompt` / `avatar_negative_prompt_strength`, with optional per-scene overrides (`negative_prompt`, `negative_prompt_strength`). Helper: [`p_video_avatar_payload.py`](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/_shared/scripts/p_video_avatar_payload.py).

**Disable for a scene:** set `"negative_prompt_strength": 0` on that scene row.

```json
"defaults": {
  "avatar_negative_prompt": "subtitles, captions, on-screen text, watermark, logo, typography, letters, words",
  "avatar_negative_prompt_strength": 0.35
}
```

## Example: async (recommended — use for all production)

Omit `Try-Sync`. For multiple clips, **create all jobs in parallel**, then batch-poll every `get_url`. See [parallel-execution.md](./references/parallel-execution.md).

Complete the [random seed ritual](./references/random-seed-ritual.md) (SSoT) before writing prompts. Omit `seed` from API `input` unless the user supplied **`api_seed`**.

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

## Example: sync (single quick test only)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video-avatar' \
  -H 'Try-Sync: true' \
  -d '{
    "input": {
      "image": "https://api.pruna.ai/v1/files/FILE_ID",
      "voice_script": "Hey — so we shipped something I've wanted for a while. Sub-second images, video in seconds, and it actually feels usable in a real workflow.",
      "voice": "Puck (Male)",
      "voice_language": "English (US)",
      "voice_prompt": "Natural conversational tone — like a founder on LinkedIn, relaxed pacing, real pauses, honest not salesy.",
      "resolution": "720p",
      "video_prompt": "Medium close-up speaking directly to lens, subtle push-in, natural head motion, warm confident energy"
    }
  }'
```

## Example: uploaded narration (scene anchor triple — avatar variant)

Generate [Gemini TTS](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/gemini-3.1-flash-tts/skills/gemini-3.1-flash-tts/SKILL.md) → upload to `/v1/files`. Pass as `input.audio` with portrait `image` (and optional `last_frame_image` when the beat has a known end pose). Duration follows audio. See [scene-anchor-triple.md](./references/scene-anchor-triple.md).

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

If both `audio` and `voice_script` are set, **audio wins**.

## Typical next steps

- One-scene avatar workflow: [avatar-single-scene](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/avatar-single-scene/skills/avatar-single-scene/SKILL.md)
- Multi-scene avatar workflow: [avatar-multi-scene](../avatar-multi-scene/SKILL.md)
- Pipeline: [pruna-generative-pipeline](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/pruna-generative-pipeline/skills/pruna-generative-pipeline/SKILL.md)

## Related workflow

Avatar + animate reels: [avatar-multi-scene](../avatar-multi-scene/SKILL.md) — slider script: [`generate_video_comparison.py`](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/_shared/scripts/generate_video_comparison.py).
