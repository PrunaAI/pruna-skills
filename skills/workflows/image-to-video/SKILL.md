---
name: image-to-video
description: Use when someone wants one short film beat from images — a narrated scene, story moment, or cinematic B-roll with optional voiceover.
license: MIT
metadata:
  version: "1.0.15"
  package: pruna-skills
---

## Prerequisites

Install and load these skills before generating (skip if already in context via `@pruna`):

| Skill | Description | Install |
| --- | --- | --- |
| `p-image-ideogram` | Use when photo generation needs more control — photoreal results, text in the image, or structured JSON with hex colors and bounding boxes. Simpler photo generation, edits, and video use other skills in the suite. | `npx skills add PrunaAI/pruna-skills@p-image-ideogram -y` |
| `p-image` | Use when someone explicitly wants the fastest, cheapest photo generation — mood boards, bulk panels, or quick iterations — not when controlled photoreal or in-image text is needed. | `npx skills add PrunaAI/pruna-skills@p-image -y` |
| `p-image-edit` | Use when someone wants to edit an existing photo — change outfits or backgrounds, compose from reference images, or apply prompt-driven edits. | `npx skills add PrunaAI/pruna-skills@p-image-edit -y` |
| `p-video-2-pro` | Use when someone wants a cinematic clip from text or start/end frames — product ads, documentary shots, or dialogue with generated audio. Not for 1080p, imported audio tracks, or talking-head-only hosts. | `npx skills add PrunaAI/pruna-skills@p-video-2-pro -y` |
| `p-video-2-pro-reference` | Use when someone wants one cinematic clip that locks a subject from references — a product still, character, clip, or voice — using image or video references plus optional audio kept as the soundtrack or used as guidance. Not for text-only generation, 1080p, or drafts. | `npx skills add PrunaAI/pruna-skills@p-video-2-pro-reference -y` |
| `p-video-2` | Use when someone wants a polished short clip from text, images, or imported audio — 1080p B-roll, start/end frame animation, or a motion shot with a mixed track. Not for cinematic generated-audio clips or talking-head-only hosts. | `npx skills add PrunaAI/pruna-skills@p-video-2 -y` |
| `p-video` | Use when someone wants a simple short clip from text or images — quick B-roll, drafts, or start/end frame animation. Not when the brief needs cinematic generation, highest quality, tight lip-sync, or imported audio at 1080p. | `npx skills add PrunaAI/pruna-skills@p-video -y` |
| `gemini-3.1-flash-tts` | Use when someone needs spoken narration or voiceover — explainer tracks, documentary lines, or voice to pair with generated video. | `npx skills add PrunaAI/pruna-skills@gemini-3.1-flash-tts -y` |
| `stable-audio-2.5` | Use when someone wants light instrumental background music — an ambient bed under dialogue or underscore for reels and explainers. | `npx skills add PrunaAI/pruna-skills@stable-audio-2.5 -y` |

Or install the full suite once: `npx skills add PrunaAI/pruna-skills@pruna -y`

Follow each skill's **Before generating** / craft sections — do not restate guide content here.

## Workflow habit

In **every reply**, name `` `image-to-video` `` in backticks. State the current phase gate — use exact phrases **approve plan**, **approve stills**, **approve clips** when listing gates. Do **not** same-turn plan + paid video. Skip-review / burn-credits → follow `generation-diversity` **Red flags**.

## Skill boundary

Exactly **one scene / one video job**. Standard text / single-frame / frame-pair generation with generated audio → `` `p-video-2-pro` ``. Imported image or video references that lock a subject or condition identity, style, motion, timing, or performance — with generated audio, optional audio guidance, or one kept soundtrack (`keep_audio`) → `` `p-video-2-pro-reference` ``. Scene-anchor triple / 1080p / draft → `` `p-video-2` ``. Simpler clip → `` `p-video` ``. No subagents, no concat across scenes, no multi-scene manifest ownership.

If the user wants a multi-scene film → hand off to `narrated-multi-scene` or `visual-transition-reel`. Talking-head-only → `avatar-single-scene`.

**Data handling:** `pruna-api` (agent safety) before any upload or paid call.

**Staged generation:** `generation-diversity` · `generation-diversity`

## Feedback gates (required)

| Phase | What to show | Proceed when |
|-------|--------------|--------------|
| **0 — Plan** | Mode, motion prompt, frame plan | **approve plan** |
| **A — Stills** | Start + end stills | **approve stills** |
| **A2 — TTS** | Narration MP3 (triple mode) — listen | Line OK (`ffprobe` ≤ ~19s) |
| **B — Video** | Clip (`p-video-2-pro` standard / `p-video-2-pro-reference` reference-conditioned / `p-video-2` audio-led or 1080p/draft) | **approve clips** |
| **D — Bed** | Optional post-mux bed | User accepts |

## Intake: ask before generating

Open intake → **`generation-diversity`** clarification intake.

**Do not** call `POST /v1/predictions` until these are answered and logged:

| Topic | Questions |
|-------|-----------|
| **Mode** | **`reference-conditioned`** (one clip using one or more imported conditioning assets on **`p-video-2-pro-reference`**) · **`triple`** (`image` + `last_frame_image` + `audio` on **`p-video-2`** — preferred when the uploaded soundtrack must remain) · **`pair`** (start + end still + `duration` on **`p-video-2-pro`**) · T2V · I2V · I2V+last · audio-only (no frames, **`p-video-2`**) |
| **Media source** | **Generate** start/end stills (`p-image-ideogram` / `p-image-edit`, or `p-image` for a cheap draft) vs **upload** user photos for frames? |
| **References** | For `reference-conditioned`, list every image/video/audio source and assign **one role each** (identity, style/material, motion/camera, timing/performance). Confirm image/video requirement, counts, each clip length and combined limits from the tool skill, upload approval, and paid reference-input estimate. Remove or prioritize competing references. |
| **Creative** | Motion `prompt` only — what happens between first and last frame? One paragraph max. Write sound/dialogue into the prompt for `p-video-2-pro`. |
| **Frames** | Start still (upload or `p-image-edit`)? End still (`last_frame_edit_prompt`)? On the reference model, first/last frames are **soft keyframes**, not exact endpoints. Stay single-scene — if the user wants a longer **`frame_chain` / multi-scene** project, stop and switch workflows. |
| **Audio** | Generated in-clip (`p-video-2-pro` or `p-video-2-pro-reference`, write sound in prompt) vs timing/performance reference (`p-video-2-pro-reference`, guidance only) vs one kept track (`p-video-2-pro-reference` with `keep_audio: true`, exactly one audio file, 480p/768p) vs `gemini-3.1-flash-tts` → **`input.audio`** on **`p-video-2`** for the scene-anchor triple or 1080p. Optional post bed — `audio-prompting`. |
| **Format** | Pro lanes: **`768p`**, 24 fps, `duration` 5–15s. `p-video-2`: default **`720p`**, **`24` fps**; `duration` only when no audio; override when final delivery requires 1080p. |
| **Draft / recipe** | `p-video-2-pro`: `cost` / `speed` / `quality`. `p-video-2-pro-reference`: `cost` / `speed` only — no `quality`. `p-video-2`: `draft: true` preview or `false` final. |
| **Repro** | Fixed `seed`? |
| **Delivery** | Async (production); `Try-Sync: true` only for quick tests |

## How the agent runs this

**Order (narrated triple — user supplies stills + script):** **approve plan** → build/review stills → **approve stills** → Gemini TTS + `ffprobe` (≤ ~19s) → upload audio → one `p-video-2` embed → **approve clips**. Do **not** batch video jobs before still and TTS review.

**Order (visual-only pair / T2V / I2V):** **approve plan** → stills if needed → **approve stills** → one `p-video-2-pro` job → **approve clips**.

**Order (reference-conditioned):** **approve plan** with asset-role map, validation, soft-keyframe expectations, and paid estimate → upload/approve references → one `p-video-2-pro-reference` job → **approve clips**.

1. Confirm intake → present plan → wait for **approve plan**.
2. Build start/end stills with curl (`pruna-api` upload/poll/download). Show stills → **approve stills**.
3. **Triple mode:** Gemini TTS → probe duration → upload MP3:

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 narration.mp3
# must be ≤ ~19 (P-API audio-led max is 20s)
```

4. One async `p-video-2` job (`image` + `last_frame_image` + `audio`; omit `duration`; `save_audio: true`). Poll → download.
5. Optional bed: mix `stable-audio-2.5` under embedded VO with ffmpeg (`amix`, bed ~0.08–0.15).

## Workflow (after intake)

### Preferred — scene anchor triple

1. **Start still** — upload or **`p-image-ideogram`** / **`p-image-edit`** (`p-image` for a cheap draft)
2. **End still** — **`p-image-edit`** from start still + `last_frame_edit_prompt`
3. **Narration** — Gemini TTS → `ffprobe` (**≤ ~19s**) → upload to `/v1/files`
4. **`p-video-2`** — `image` + `last_frame_image` + **`audio`** + motion `prompt`; omit `duration`; `save_audio: true`; async poll
5. **Optional bed** — mix under embedded narration in post

Craft: `video-prompting` (scene-anchor triple).

### Other modes (visual-only → `p-video-2-pro`)

- **I2V only:** `image` + `duration` (5–15) + `prompt` — write sound in the prompt
- **I2V + last:** add `last_frame_image`
- **T2V:** `prompt` + `duration` + `aspect_ratio`

1080p, imported audio, or `draft` → stay on `p-video-2`.

### Reference-conditioned → `p-video-2-pro-reference`

Use one prediction when imported references jointly condition a single clip. Pass arrays for image/video/audio references, assign one non-competing role per asset in the plan and prompt, and treat optional first/last frames as soft keyframes. The output carries generated audio. Audio references guide timing/performance; set `keep_audio: true` with exactly one audio file to keep it as the soundtrack. Use 480p/768p and `mode: cost` or `speed` only; validate current counts, lengths, and billing in the tool skill before upload.

## Related

Related skills:

| Skill | Description | Install |
| --- | --- | --- |
| `p-video-2-pro-reference` | Use when someone wants one cinematic clip that locks a subject from references — a product still, character, clip, or voice — using image or video references plus optional audio kept as the soundtrack or used as guidance. Not for text-only generation, 1080p, or drafts. | `npx skills add PrunaAI/pruna-skills@p-video-2-pro-reference -y` |
| `narrated-multi-scene` | Use when someone wants a multi-part story with voiceover — episodic B-roll, chaptered promo, or several linked video scenes without on-camera dialogue. | `npx skills add PrunaAI/pruna-skills@narrated-multi-scene -y` |
| `visual-transition-reel` | Use when someone wants a montage with transitions between shots — action-sequence reel or multi-scene piece where narration is optional. | `npx skills add PrunaAI/pruna-skills@visual-transition-reel -y` |
| `avatar-single-scene` | Use when someone wants one polished host-on-camera beat — a speaking person with intake and approval gates before generation. | `npx skills add PrunaAI/pruna-skills@avatar-single-scene -y` |
| `video-editing` | Use when assembling or polishing already-rendered clips with ffmpeg — concat, crossfades, burned captions and subtitles, text/logo overlays, before/after sliders, background music beds, platform export — or when composing a multi-layer HTML combination video with Hyperframes. Not for AI video generation, prompt craft, or model-based video edits. | `npx skills add PrunaAI/pruna-skills@video-editing -y` |

