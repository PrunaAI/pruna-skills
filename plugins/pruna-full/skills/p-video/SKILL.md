---
name: p-video
description: Use when the user wants one video clip from text or stills, start/end frame animation, or B-roll and cinematic shots—not multi-scene films, talking-head avatar clips, or motion transfer from a template video.
license: MIT
metadata:
  version: "0.0.2"
  pruna_model: p-video
---

# p-video (Pruna)

Premium video from text, optional **first-frame** / **last-frame** images, or optional audio. Same model on [Replicate](https://replicate.com/prunaai/p-video) — see **First / last frame chaining** for multi-scene handoffs.

Full P-API parameters: [p-video model docs](https://docs.api.pruna.ai/guides/models/p-video).

Shared HTTP patterns: [pruna-api.md](./references/pruna-api.md) (upload, [poll](#poll), [download](#download))

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

1. **[Generation diversity](./references/generation-diversity.md)** — ritual seed + axis rotation before each job.
2. Confirm **mode** (T2V / I2V / **visual transition pair** / scene anchor triple / audio), **`duration`** (unless audio-driven), **`resolution`**, **`fps`**, **`draft`**, **`seed`**, and **`prompt`** with the user—or run intake from [image-to-video](../image-to-video/SKILL.md), [visual-transition-reel](../visual-transition-reel/SKILL.md), or [narrated-multi-scene](../narrated-multi-scene/SKILL.md).

For **narration or music**, see [audio-post-production.md](https://github.com/PrunaAI/pruna-skills/tree/main/references/shared/audio-post-production.md) — Gemini TTS, Stable Audio beds, or upload audio for audio-conditioned mode.

Validate renders with [p-video-quality-checklist.md](./references/p-video-quality-checklist.md).

## Required input

- `prompt` (string)

## Common optional fields

| Field | Role |
|-------|------|
| `image` | **First frame** — image-to-video anchor; when set, `aspect_ratio` is ignored |
| `last_frame_image` | **Last frame** — optional end-state still the clip should move toward |
| `audio` | Audio-conditioned; duration follows audio (capped at **20s** on P-API); formats flac, mp3, wav |
| `duration` | 1–20 seconds on P-API (ignored if `audio` set). With `audio`, clip length = min(audio length, **20s**) — keep TTS ≤ ~19s per scene |
| `resolution` | `720p` (default) or `1080p` |
| `fps` | `24` (default) or `48` |
| `aspect_ratio` | When no `image`: `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`, `1:1` |
| `draft` | `true` = ~4× faster/cheaper preview ([pricing](https://replicate.com/prunaai/p-video)); `false` = final |
| `save_audio` | Keep model-generated dialogue/SFX on output (native audio) |
| `seed` | Reproducibility |
| `prompt_upsampling` | Auto prompt enhancement (default on Replicate) |
| `disable_safety_filter` | Client policy |

## First / last frame chaining

Use **`image`** + **`last_frame_image`** to steer motion between two known compositions — the model interpolates from start plate to end plate. This is the primary tool for **smoother multi-scene stories** when hard cuts between unrelated T2V clips feel disjointed.

### Single scene (controlled arc)

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

### Multi-scene handoff (scene *i* → *i+1*)

| Strategy | How | Parallel? |
|----------|-----|-----------|
| **Planned anchor chain** (recommended) | `p-image-edit` produces `start_i` and `end_i` per scene. Scene *i* uses `image=start_i`, `last_frame_image=end_i`. Scene *i+1* uses `image=end_i` (same URL). | Stills: parallel. Video: **phased** if each scene's `end_i` must be approved before the next scene's render — or parallel once all stills exist. |
| **Extract last frame** | After scene *i* renders, ffmpeg-grab last frame → upload → `image` for scene *i+1* | **Sequential** — scene *i+1* cannot start until scene *i* finishes |

**Continuity tips**

- Keep **`resolution`**, **`fps`**, and lighting language consistent across chained scenes.
- End still of scene *N* should match the **intended first composition** of scene *N+1* (same framing when possible).
- Use **`draft: true`** on the full chain for cheap motion approval, then rerun finals with locked `seed`/prompts.
- [P-Video limitations](https://replicate.com/prunaai/p-video): not built for extreme camera motion or very complex arcs — prefer short beats (4–5s) and clear start/end plates.

See [visual-transition-reel](../visual-transition-reel/SKILL.md) for multi-scene visual montages and [narrated-multi-scene](../narrated-multi-scene/SKILL.md) for scene-table columns and [parallel-execution.md](./references/parallel-execution.md) for phased vs parallel batches.

Canonical visual transition spec: [scene-anchor-pair.md](./references/scene-anchor-pair.md).  
Canonical narrated spec: [scene-anchor-triple.md](./references/scene-anchor-triple.md).

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

**Multi-scene:** [visual-transition-reel](../visual-transition-reel/SKILL.md) — selective `chain_from_previous`, `extract_last_frame`, concat crossfades.

**Upgrade to narrated:** add TTS → upload → `audio`; omit `duration` → [scene-anchor-triple.md](./references/scene-anchor-triple.md).

## Scene anchor triple (`image` + `last_frame_image` + `audio`)

For narrated multi-scene films, treat each scene as **three uploaded anchors** — the same way first/last frames bracket visual motion, **`audio`** brackets timing and performance:

| Anchor | Field | Role |
|--------|-------|------|
| **First frame** | `image` | Opening composition (hero or `p-image-edit` start still) |
| **Last frame** | `last_frame_image` | Closing composition (end still; becomes next scene's `image` when chaining) |
| **Narration / VO** | `audio` | Uploaded TTS or music — **sets clip duration** (up to **20s** P-API max); model syncs motion to speech |

All three are Pruna file URLs from `POST /v1/files`. Pass them together in one `p-video` prediction; **omit `duration`** when `audio` is set. **Probe each TTS file** with `ffprobe` before render — lines longer than ~19s are truncated at the API ceiling even when `audio` is passed ([`p_video_payload.py`](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/_shared/scripts/p_video_payload.py) `validate_narration_duration`).

### Per-scene payload (recommended story mode)

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

### Multi-scene chain (visual + audio)

```text
Scene 1: image=start_1,  last_frame_image=end_1,  audio=vo_1
Scene 2: image=end_1,    last_frame_image=end_2,  audio=vo_2   ← same URL as scene 1 end
Scene 3: image=end_2,    last_frame_image=end_3,  audio=vo_3
```

**Stills phase:** `p-image-edit` start still from hero; end still from start still (parallel per scene after starts exist).  
**Audio phase:** [Gemini TTS](../gemini-3.1-flash-tts/SKILL.md) per scene (parallel) → upload each.  
**Video phase:** parallel `p-video` when all six URLs per scene row are ready.

Same triple pattern on **`p-video-avatar`**: portrait `image` + optional `last_frame_image` + uploaded `audio` for lip-sync narration.

## Audio modes

| Mode | Input | Duration | When |
|------|-------|----------|------|
| **Silent / native SFX** | `prompt` only (optional `save_audio`) | `duration` | Ambient clips, model-generated sound |
| **Uploaded audio (preferred)** | `audio` URL + `prompt` (+ optional `image`, `last_frame_image`) | Follows audio — **omit `duration`** | VO, TTS, song slices — upload to `/v1/files` first; set **`save_audio`: true** for narrated concat |
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

**Multi-scene:** after shared uploads, fire predictions in **parallel** when scenes do not share frame dependencies; use **phased** batches when `last_frame_image` of scene *N* is the `image` of scene *N+1* and stills are not pre-planned. See [parallel-execution.md](./references/parallel-execution.md).

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

## Typical next steps

- One-scene workflow: [image-to-video](../image-to-video/SKILL.md)
- Visual transitions (pair, no VO): [visual-transition-reel](../visual-transition-reel/SKILL.md)
- Multi-scene + frame chain + narration: [narrated-multi-scene](../narrated-multi-scene/SKILL.md)
- Talking portrait: [p-video-avatar](../p-video-avatar/SKILL.md)
- Narration TTS: [gemini-3.1-flash-tts](../gemini-3.1-flash-tts/SKILL.md)
- Pipeline hub: [pruna-generative-pipeline](../pruna-generative-pipeline/SKILL.md)

## Related workflow

Multi-scene AI video: [narrated-multi-scene](../narrated-multi-scene/SKILL.md) — scene table, frame columns, audio phases.
