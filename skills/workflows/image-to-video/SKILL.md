---
name: image-to-video
description: Use when someone wants one short film beat from images — a narrated scene, story moment, or cinematic B-roll with optional voiceover.
license: MIT
metadata:
  version: "1.0.10"
  package: pruna-skills
---

## Prerequisites

Install and load these skills before generating (skip if already in context via `@pruna`):

| Skill | Description | Install |
| --- | --- | --- |
| `p-image` | Use when someone explicitly wants the fastest, cheapest photo generation — mood boards, bulk panels, or quick iterations — not when controlled photoreal or in-image text is needed. | `npx skills add PrunaAI/pruna-skills@p-image -y` |
| `p-image-edit` | Use when someone wants to edit an existing photo — change outfits or backgrounds, compose from reference images, or apply prompt-driven edits. | `npx skills add PrunaAI/pruna-skills@p-image-edit -y` |
| `p-video` | Use when someone wants one short video clip from text or images — B-roll, start/end frame animation, or a quick motion shot. Not for full multi-scene films or lip-synced hosts. | `npx skills add PrunaAI/pruna-skills@p-video -y` |
| `gemini-3.1-flash-tts` | Use when someone needs spoken narration or voiceover — explainer tracks, documentary lines, or voice to pair with generated video. | `npx skills add PrunaAI/pruna-skills@gemini-3.1-flash-tts -y` |
| `stable-audio-2.5` | Use when someone wants light instrumental background music — an ambient bed under dialogue or underscore for reels and explainers. | `npx skills add PrunaAI/pruna-skills@stable-audio-2.5 -y` |

Or install the full suite once: `npx skills add PrunaAI/pruna-skills@pruna -y`

Follow each skill's **Before generating** / craft sections — do not restate guide content here.

## Workflow habit

In **every reply**, name `` `image-to-video` `` in backticks. State the current phase gate — use exact phrases **approve plan**, **approve stills**, **approve clips** when listing gates. Do **not** same-turn plan + paid video. Skip-review / burn-credits → follow `generation-diversity` **Red flags**.

## Skill boundary

Exactly **one scene / one `p-video` job**. No subagents, no concat across scenes, no multi-scene manifest ownership.

If the user wants a multi-scene film → hand off to `narrated-multi-scene` or `visual-transition-reel`. Talking-head-only → `avatar-single-scene`.

**Data handling:** `pruna-api` (agent safety) before any upload or paid call.

**Staged generation:** `generation-diversity` · `generation-diversity`

## Feedback gates (required)

| Phase | What to show | Proceed when |
|-------|--------------|--------------|
| **0 — Plan** | Mode, motion prompt, frame plan | **approve plan** |
| **A — Stills** | Start + end stills | **approve stills** |
| **A2 — TTS** | Narration MP3 (triple mode) — listen | Line OK (`ffprobe` ≤ ~19s) |
| **B — Video** | `p-video` clip | **approve clips** |
| **D — Bed** | Optional post-mux bed | User accepts |

## Intake: ask before generating

Open intake → **`generation-diversity`** clarification intake.

**Do not** call `POST /v1/predictions` until these are answered and logged:

| Topic | Questions |
|-------|-----------|
| **Mode** | **`triple`** (`image` + `last_frame_image` + `audio` — preferred for narrated beats) · **`pair`** (start + end still + `duration`) · T2V · I2V · I2V+last · audio-only (no frames) |
| **Media source** | **Generate** start/end stills (`p-image` / `p-image-edit`) vs **upload** user photos for frames? |
| **Creative** | Motion `prompt` only — what happens between first and last frame? One paragraph max. |
| **Frames** | Start still (upload or `p-image-edit`)? End still (`last_frame_edit_prompt`)? Stay single-scene — if the user wants a longer **`frame_chain` / multi-scene** project, stop and switch to `narrated-multi-scene` or `visual-transition-reel`. |
| **Audio** | `gemini-3.1-flash-tts` → upload → **`input.audio`** (preferred). Optional `stable-audio-2.5` bed **after** render. Post-mux is fallback only — `audio-prompting`. |
| **Format** | Default **`720p`**, **`24` fps**; `duration` only when **no** `audio`; override `resolution` / `fps` / `aspect_ratio` when user wants final delivery |
| **Draft** | `draft: true` for preview or `false` for final? |
| **Repro** | Fixed `seed`? |
| **Delivery** | Async (production); `Try-Sync: true` only for quick tests |

## How the agent runs this

**Order (narrated triple — user supplies stills + script):** **approve plan** → build/review stills → **approve stills** → Gemini TTS + `ffprobe` (≤ ~19s) → upload audio → one `p-video` embed → **approve clips**. Do **not** batch `p-video` before still and TTS review.

1. Confirm intake → present plan → wait for **approve plan**.
2. Build start/end stills with curl (`pruna-api` upload/poll/download). Show stills → **approve stills**.
3. **Triple mode:** Gemini TTS → probe duration → upload MP3:

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 narration.mp3
# must be ≤ ~19 (P-API audio-led max is 20s)
```

4. One async `p-video` job (`image` + `last_frame_image` + `audio`; omit `duration`; `save_audio: true`). Poll → download.
5. Optional bed: mix `stable-audio-2.5` under embedded VO with ffmpeg (`amix`, bed ~0.08–0.15).

## Workflow (after intake)

### Preferred — scene anchor triple

1. **Start still** — upload or **`p-image`** / **`p-image-edit`**
2. **End still** — **`p-image-edit`** from start still + `last_frame_edit_prompt`
3. **Narration** — Gemini TTS → `ffprobe` (**≤ ~19s**) → upload to `/v1/files`
4. **`p-video`** — `image` + `last_frame_image` + **`audio`** + motion `prompt`; omit `duration`; `save_audio: true`; async poll
5. **Optional bed** — mix under embedded narration in post

Craft: `video-prompting` (scene-anchor triple).

### Other modes

- **I2V only:** `image` + `duration` + `prompt`
- **I2V + last:** add `last_frame_image`
- **T2V:** `prompt` + `duration` + `aspect_ratio`

## Related

Related skills:

| Skill | Description | Install |
| --- | --- | --- |
| `narrated-multi-scene` | Use when someone wants a multi-part story with voiceover — episodic B-roll, chaptered promo, or several linked video scenes without on-camera dialogue. | `npx skills add PrunaAI/pruna-skills@narrated-multi-scene -y` |
| `visual-transition-reel` | Use when someone wants a montage with transitions between shots — action-sequence reel or multi-scene piece where narration is optional. | `npx skills add PrunaAI/pruna-skills@visual-transition-reel -y` |
| `avatar-single-scene` | Use when someone wants one polished host-on-camera beat — a speaking person with intake and approval gates before generation. | `npx skills add PrunaAI/pruna-skills@avatar-single-scene -y` |
| `video-editing` | Use when assembling or polishing already-rendered clips with ffmpeg — concat, crossfades, burned captions and subtitles, text/logo overlays, before/after sliders, background music beds, platform export — or when composing a multi-layer HTML combination video with Hyperframes. Not for AI video generation, prompt craft, or model-based video edits. | `npx skills add PrunaAI/pruna-skills@video-editing -y` |

