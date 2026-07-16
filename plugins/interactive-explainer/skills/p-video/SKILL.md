---
name: p-video
description: Use when someone wants one short video clip from text or images — B-roll, start/end frame animation, or a quick motion shot. Not for full multi-scene films or lip-synced hosts.
license: MIT
metadata:
  version: "1.0.5"
  pruna_model: p-video
---

# p-video (Pruna)

Premium video from text, optional **first-frame** / **last-frame** images, or optional audio. Same model on [Replicate](https://replicate.com/prunaai/p-video).

Full P-API parameters: [p-video model docs](https://docs.api.pruna.ai/guides/models/p-video).

Shared HTTP patterns: [pruna-api.md](./references/pruna-api.md) (upload, [poll](#poll), [download](#download))

## Skill boundary

This skill = **one `p-video` prediction** per invocation.

**Out of scope (do not execute from this skill):**

- Multi-scene assembly, concat, subagent orchestration, or parallel scene batches
- Motion transfer from a template video → [p-video-animate](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/p-video-animate/skills/p-video-animate/SKILL.md)
- Talking-head / lip-sync → [p-video-avatar](../p-video-avatar/SKILL.md)

If the request exceeds one clip, **stop** and recommend: [image-to-video](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/image-to-video/skills/image-to-video/SKILL.md) (one narrated beat), [visual-transition-reel](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/visual-transition-reel/skills/visual-transition-reel/SKILL.md) (multi-scene visual), or [narrated-multi-scene](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/narrated-multi-scene/skills/narrated-multi-scene/SKILL.md) (multi-scene + VO).

## HTTP (curl)

### Create (async — recommended)

See **Example: async text-to-video** below. Poll and download: [pruna-api.md](./references/pruna-api.md#poll).

### Upload for image-to-video / frame anchors

```bash
curl -X POST "https://api.pruna.ai/v1/files" \
  -H "apikey: ${PRUNA_API_KEY}" \
  -F "content=@/path/to/first-frame.png"
```

Pass `urls.get` as `input.image` (first frame) and/or `input.last_frame_image` (last frame).

## Before generating

**Data handling:** [agent-safety.md](./references/agent-safety.md) before any upload or paid call.

1. **[Generation diversity](./references/generation-diversity.md)** — ritual seed + axis rotation before each job.
2. Confirm **mode** (T2V / I2V / **visual transition pair** / scene anchor triple / audio), **`duration`** (unless audio-driven), **`resolution`**, **`fps`**, **`draft`**, **`seed`**, and **`prompt`** with the user.
3. If the request is multi-scene or needs subagents/concat — **stop** and switch skills (see **Skill boundary**).

For **narration or music** on this single clip, see [audio-post-production.md](https://github.com/PrunaAI/pruna-skills/tree/main/references/shared/audio-post-production.md) — Gemini TTS, Stable Audio beds, or upload audio for audio-conditioned mode.

Validate renders with [p-video-quality-checklist.md](./references/p-video-quality-checklist.md).

## Required input

- `prompt` (string)

## Common optional fields

| Field | Role |
|-------|------|
| `image` | **First frame** — image-to-video anchor; when set, `aspect_ratio` is ignored |
| `last_frame_image` | **Last frame** — optional end-state still the clip should move toward |
| `audio` | Audio-conditioned; duration follows audio (capped at **20s** on P-API); formats flac, mp3, wav |
| `duration` | 1–20 seconds on P-API (ignored if `audio` set). With `audio`, clip length = min(audio length, **20s**) — keep TTS ≤ ~19s |
| `resolution` | `720p` (default) or `1080p` |
| `fps` | `24` (default) or `48` |
| `aspect_ratio` | When no `image`: `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`, `1:1` |
| `draft` | `true` = ~4× faster/cheaper preview ([pricing](https://replicate.com/prunaai/p-video)); `false` = final |
| `save_audio` | Keep model-generated dialogue/SFX on output (native audio) |
| `seed` | Reproducibility |
| `prompt_upsampling` | Auto prompt enhancement (default on Replicate) |
| `disable_safety_filter` | Client policy |

## First / last frame (single clip)

Use **`image`** + **`last_frame_image`** to steer motion between two known compositions — the model interpolates from start plate to end plate.

1. Upload or generate **start still** → `input.image`
2. Upload or **`p-image-edit`** an **end still** (same subject, new pose/background beat) → `input.last_frame_image`
3. **`p-video`** with a motion-only `prompt` describing camera + action between the two plates

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video' \
  -d '{
    "input": {
      "prompt": "Dog turns head toward flying toy, grass sways, gentle push-in, warm afternoon light",
      "image": "https://api.pruna.ai/v1/files/START_ID",
      "last_frame_image": "https://api.pruna.ai/v1/files/END_ID",
      "duration": 5,
      "resolution": "720p",
      "fps": 24
    }
  }'
```

Canonical specs: [scene-anchor-pair.md](./references/scene-anchor-pair.md) · [scene-anchor-triple.md](./references/scene-anchor-triple.md) (one narrated beat).

## Visual transition mode (scene anchor pair)

Use when you have **two photos** and want **`p-video`** to **interpolate motion between them** — no narration required. Stills from [`p-image`](../p-image/SKILL.md) hero + [`p-image-edit`](../p-image-edit/SKILL.md), or user uploads.

| Field | Required | Role |
|-------|----------|------|
| `image` | yes | Start plate |
| `last_frame_image` | yes | End plate |
| `prompt` | yes | OPEN → MID → CLOSE **motion** between plates (not still descriptions) |
| `duration` | yes | Prefer 4–5s; omit when `audio` is set |

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video' \
  -d '{
    "input": {
      "prompt": "OPEN: hold wide. MID: slow dolly in, neon flickers. CLOSE: settle on end pose.",
      "image": "https://api.pruna.ai/v1/files/START_ID",
      "last_frame_image": "https://api.pruna.ai/v1/files/END_ID",
      "duration": 5,
      "resolution": "720p",
      "fps": 24
    }
  }'
```

**Stills pipeline:** `p-image` (hero) → `p-image-edit` (`edit_prompt` → start) → `p-image-edit` (`last_frame_edit_prompt` → end).

## Scene anchor triple (`image` + `last_frame_image` + `audio`)

For **one** narrated beat, pass three uploaded anchors in a single prediction:

| Anchor | Field | Role |
|--------|-------|------|
| **First frame** | `image` | Opening composition |
| **Last frame** | `last_frame_image` | Closing composition |
| **Narration / VO** | `audio` | Uploaded TTS or music — **sets clip duration** (up to **20s** P-API max) |

All three are Pruna file URLs from `POST /v1/files`. **Omit `duration`** when `audio` is set. **Probe TTS** with `ffprobe` before render — lines longer than ~19s are truncated ([`p_video_payload.py`](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/_shared/scripts/p_video_payload.py) `validate_narration_duration`).

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

Full single-beat + multi-scene extension: [scene-anchor-triple.md](./references/scene-anchor-triple.md).

## Audio modes

| Mode | Input | Duration | When |
|------|-------|----------|------|
| **Silent / native SFX** | `prompt` only (optional `save_audio`) | `duration` | Ambient clips, model-generated sound |
| **Uploaded audio (preferred)** | `audio` URL + `prompt` (+ optional `image`, `last_frame_image`) | Follows audio — **omit `duration`** | VO, TTS, song slices — upload to `/v1/files` first; set **`save_audio`: true** when keeping narration |
| **External narration** | [gemini-3.1-flash-tts](../gemini-3.1-flash-tts/SKILL.md) → upload → `audio` | Follows audio | Documentary narrator — same as uploaded audio; **never** post-mux over silent clips |
| **Post mux (fallback only)** | Silent `p-video` renders | `duration` | Only when re-render is impossible — truncates long TTS |

Shared helper: [`p_video_payload.py`](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/_shared/scripts/p_video_payload.py) — enforces omitting `duration` when `audio` is set.

Full layering guide: [audio-post-production.md](https://github.com/PrunaAI/pruna-skills/tree/main/references/shared/audio-post-production.md).

## Example: async text-to-video (recommended)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video' \
  -d '{
    "input": {
      "prompt": "Slow dolly in, rain on city street at night, cinematic",
      "duration": 5,
      "resolution": "720p",
      "aspect_ratio": "16:9"
    }
  }'
```

Poll and download: [pruna-api.md](./references/pruna-api.md#poll).

## Example: image-to-video (first frame only)

Upload image to `/v1/files`, pass its `urls.get` as `input.image`.

## Example: audio-conditioned with frame anchors (narrated story beat)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video' \
  -d '{
    "input": {
      "prompt": "Dog searches through tall grass, cinematic, motion matches narrator mood",
      "image": "https://api.pruna.ai/v1/files/START_ID",
      "last_frame_image": "https://api.pruna.ai/v1/files/END_ID",
      "audio": "https://api.pruna.ai/v1/files/NARRATION_ID",
      "resolution": "720p",
      "fps": 24,
      "save_audio": true
    }
  }'
```

Omit `duration` when `audio` is set. See **Scene anchor triple** above.

## Example: audio-conditioned (narration only, no last frame)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video' \
  -d '{
    "input": {
      "prompt": "Dog searches through tall grass, cinematic, matches narrator mood",
      "image": "https://api.pruna.ai/v1/files/START_ID",
      "audio": "https://api.pruna.ai/v1/files/NARRATION_ID",
      "resolution": "720p",
      "fps": 24
    }
  }'
```

## Related workflows (do not execute from this skill)

- One-scene narrated beat: [image-to-video](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/image-to-video/skills/image-to-video/SKILL.md)
- Visual transitions (pair, multi-scene): [visual-transition-reel](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/visual-transition-reel/skills/visual-transition-reel/SKILL.md)
- Multi-scene + frame chain + narration: [narrated-multi-scene](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/narrated-multi-scene/skills/narrated-multi-scene/SKILL.md)
- Talking portrait: [p-video-avatar](../p-video-avatar/SKILL.md)
- Motion transfer: [p-video-animate](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/p-video-animate/skills/p-video-animate/SKILL.md)
- Narration TTS: [gemini-3.1-flash-tts](../gemini-3.1-flash-tts/SKILL.md)
- Pipeline hub: [pruna-generative-pipeline](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/pruna-generative-pipeline/skills/pruna-generative-pipeline/SKILL.md)
