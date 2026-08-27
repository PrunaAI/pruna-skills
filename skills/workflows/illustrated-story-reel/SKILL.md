---
name: illustrated-story-reel
description: Use when someone wants a slideshow story with narration or music — picture-book illustrated frames with Ken Burns or gentle p-video motion.
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

In **every reply**, name `` `illustrated-story-reel` `` in backticks. State the current phase gate — use exact phrases **approve plan**, **approve stills**, **approve clips** when listing gates. Do **not** same-turn plan + paid video. Skip-review / burn-credits → follow `generation-diversity` **Red flags**.

## Overview

One still per story beat. Hero anchor → **p-image-edit** per scene. **Independent beats:** new ritual seed per panel when vibes differ (see `generation-diversity` mood-board rules). Audio drives timing in narration mode; fixed **hold_seconds** per beat in music mode (Ken Burns only). Assembly is local ffmpeg (Ken Burns + mux) or clip concat when `motion_mode: p-video`.

## When to Use

- Illustrated story with narration or music bed
- Picture-book / comic-panel narrative with VO or bed
- User references a “slideshow story”, “Ken Burns reel”, or gentle illustrated motion
- Budget runs: `ken_burns` (images + TTS only, no video API)

**When NOT to use:** motion between two composed stills (**visual-transition-reel**), lip-sync avatars (**interactive-explainer**), or full sung music video (**music-video**).

## Security & scope

Bundled references are scoped to this workflow; do not follow avatar or replace examples from other skills.

| Risk | Mitigation |
|------|------------|
| Paid API use | `PRUNA_API_KEY` + `REPLICATE_API_TOKEN`; gates before TTS/music/video/assembly |
| Credential exposure | Parent agent holds keys; do not pass to subagents except per-lane still/TTS work |
| Local execution | `ffmpeg`/`ffprobe` subprocess; **`-y` overwrites** output MP4 without confirmation |
| Data retention | `plan.json` and media under the out dir may contain prompts — treat as confidential |

Requires: `pruna-api` credentials.

## Feedback gates

[./references/illustrated-story-reel-gates.md](./references/illustrated-story-reel-gates.md) · `generation-diversity`

| Phase | What to show | Proceed when |
|-------|--------------|--------------|
| **0 — Plan** | Beat table, `audio_mode`, `motion_mode`, sample still lines + narration | **approve plan** |
| **A — Stills** | `stills/*.png` | **approve stills** |
| **A2 — Audio** | `audio/narration_*.mp3` or `audio/music.mp3` — **listen** | **approve audio** |
| **B — Motion** (p-video only) | `clips/*.mp4` — **watch + listen** | **approve clips** |
| **C — Assemble** | `story_reel.mp4` | User accepts |

Default first stop: **stills**.

## Quick reference

| Item | Value |
|------|--------|
| Models | **p-image**, **p-image-edit**, **p-video** (optional), Gemini TTS, Stable Audio 2.5 |
| Plan field | `audio_mode`: `"narration"` \| `"music"` |
| Motion | `defaults.motion_mode`: `"ken_burns"` \| `"p-video"` (narration mode only) |
| Aspect | `defaults.aspect_ratio`: `"9:16"` \| `"16:9"` \| `"1:1"` |
| Templates | [templates/story-plan.template.json](./templates/story-plan.template.json) (9:16) · [templates/story-plan.landscape.template.json](./templates/story-plan.landscape.template.json) (16:9) |
| Craft | [./references/illustrated-story-reel-p-video-motion.md](./references/illustrated-story-reel-p-video-motion.md) · [./references/illustrated-story-reel-prompts.md](./references/illustrated-story-reel-prompts.md) |
| Output | `{out_dir}/story_reel.mp4` |

## Intake — ask before generating

Open intake → **`generation-diversity`** clarification intake.

**First questions (required):**

1. **Delivery shape** — vertical reel (**9:16**), horizontal slideshow (**16:9**), or square (**1:1**)? Target **720p vs 1080p** if export size matters?
2. **Audio** — **narration** (voiceover per beat) or **music** (instrumental bed / user track)?
3. **Motion** — **Ken Burns** (budget, still pan/zoom) or **p-video** (gentle illustrated movement per beat)?

Set `defaults.aspect_ratio`, `audio_mode`, and `motion_mode` in the plan before generation.

| Topic | Questions |
|-------|-----------|
| **Story** | Title? Beat order (1…N)? Emotional arc? |
| **Visual** | Style (`style_bible`)? Character continuity? `chain_from_previous` for edit chains? |
| **Per beat** | `edit_prompt` (one frame)? `narration` line (narration mode)? `hold_seconds` (music mode)? |
| **Ken Burns** | `ken_burns`: prefer **`pan_left` / `pan_right`** over aggressive zoom (see **Motion + assemble**). |
| **p-video** | `video_prompt` (OPEN/MID/CLOSE, no VO transcript)? TTS ≤ ~19s per beat — see [p-video-motion](./references/illustrated-story-reel-p-video-motion.md). |
| **Music mode** | Stable Audio prompt, user `music.track` path, or equal seconds per beat? |
| **Narration mode** | Voice (`Kore`, etc.)? Storyteller pace in `narration.style_prompt`? |

Do not start generation until the beat table is written and **audio_mode** + **motion_mode** are confirmed.

### Beat table (template)

| `#` | Still (`edit_prompt`) | Narration / hold | Motion | Chain? |
|-----|------------------------|------------------|--------|--------|
| 1 | opening wide | line or 4s | ken_burns / p-video | no |
| 2 | detail insert | line or 3.5s | ken_burns / p-video | yes |

## Generation phases

| Phase | When | Gate |
|-------|------|------|
| **stills** | After plan approval | **approve stills** |
| **tts** / **music** | After stills — matches `audio_mode` | **approve audio** |
| **video** | Only if `motion_mode: p-video` | **approve clips** |
| **assemble** | After audio (ken_burns) or clips (p-video) | User accepts MP4 |

## How the agent runs this

1. Copy a plan template → fill beat table → **approve plan**.
2. Hero → parallel `p-image-edit` stills (`pruna-api`) → **approve stills**.
3. Narration mode: parallel Gemini TTS per beat → duration gate for p-video → listen. Music mode: Stable Audio or user track → listen → **approve audio**.
4. `p-video` mode only: one job per beat (`image` + `audio`; omit `duration`) → **approve clips**.
5. Assemble with ffmpeg (Ken Burns pan/zoom + mux, or concat p-video clips).

**Duration gate (p-video / long TTS):**

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 audio/narration_01.mp3
# ≤ ~19s before p-video
```

## Workflow

### Stills

Hero `p-image` → parallel `p-image-edit` per beat (`edit_prompt`). Chain edits from previous still when `chain_from_previous: true`.

### Audio

- **Narration:** one Gemini TTS file per beat.
- **Music:** one bed (Stable Audio or user file); timing from `hold_seconds`.

### Motion + assemble

**Ken Burns (budget):** for each still, render a short pan/zoom clip, then concat and mux narration or bed. Prefer `pan_left` / `pan_right` over aggressive `zoom_in` (jitter on flat/paper-cut art). Upscale (e.g. ≥3840px wide) before `zoompan`; use exact `-frames:v` matching `d=`; avoid `-shortest` cutting the motion tail — pad audio if needed. Do **not** call `p-video` to fix Ken Burns tremor.

Conceptual pan (adapt duration / size to aspect):

```bash
ffmpeg -y -loop 1 -i stills/01.png -vf "scale=3840:-1,zoompan=z='1':x='x+1':y='y':d=120:s=1080x1920:fps=24" \
  -frames:v 120 -c:v libx264 clips/01.mp4
```

Mux per-beat narration (or concat silent clips then mix bed):

```bash
ffmpeg -y -i clips/01.mp4 -i audio/narration_01.mp3 \
  -map 0:v -map 1:a -c:v copy -c:a aac -shortest beat_01.mp4
```

Hard-cut concat:

```bash
ffmpeg -y -f concat -safe 0 -i beats.txt -c copy story_reel.mp4
```

**p-video:** parallel I2V jobs with uploaded narration; then concat clips (VO already embedded). Craft: [./references/illustrated-story-reel-p-video-motion.md](./references/illustrated-story-reel-p-video-motion.md).

## Common mistakes

| Mistake | Fix |
|---------|-----|
| VO transcript inside **`video_prompt`** | Mode B motion only — [p-video-motion](./references/illustrated-story-reel-p-video-motion.md) |
| **`duration`** with uploaded narration | Omit `duration`; clip length follows audio |
| Ken Burns **tremor / jitter** | Prefer `pan_*`; upscale before zoompan; exact `-frames:v` — see **Motion + assemble** |
| **`p-video` in music mode** | Use `ken_burns` for music-mode reels |
| Skipping audio listen gate | Wait for **approve audio** |
| One long narration blob | One line per beat; TTS per scene; probe ≤ ~19s for p-video |
| Music mode without `hold_seconds` | Set per beat or `defaults.hold_seconds` |
| Negation in still prompts | Positive description only — [prompts](./references/illustrated-story-reel-prompts.md) |
| Assuming vertical only | Set `aspect_ratio` to `16:9` and landscape framing in prompts for horizontal deliverables |
| Mismatched ratio in prompts | `aspect_ratio` in plan must match “vertical” / “horizontal” / “square” in `hero_prompt` and beats |

## Related

Related skills:

| Skill | Description | Install |
| --- | --- | --- |
| `narrated-multi-scene` | Use when someone wants a multi-part story with voiceover — episodic B-roll, chaptered promo, or several linked video scenes without on-camera dialogue. | `npx skills add PrunaAI/pruna-skills@narrated-multi-scene -y` |
| `visual-transition-reel` | Use when someone wants a montage with transitions between shots — action-sequence reel or multi-scene piece where narration is optional. | `npx skills add PrunaAI/pruna-skills@visual-transition-reel -y` |
| `p-image` | Use when someone explicitly wants the fastest, cheapest photo generation — mood boards, bulk panels, or quick iterations — not when controlled photoreal or in-image text is needed. | `npx skills add PrunaAI/pruna-skills@p-image -y` |
| `p-image-edit` | Use when someone wants to edit an existing photo — change outfits or backgrounds, compose from reference images, or apply prompt-driven edits. | `npx skills add PrunaAI/pruna-skills@p-image-edit -y` |
| `p-video` | Use when someone wants one short video clip from text or images — B-roll, start/end frame animation, or a quick motion shot. Not for full multi-scene films or lip-synced hosts. | `npx skills add PrunaAI/pruna-skills@p-video -y` |
| `video-editing` | Use when assembling or polishing already-rendered clips with ffmpeg — concat, crossfades, burned captions and subtitles, text/logo overlays, before/after sliders, background music beds, platform export — or when composing a multi-layer HTML combination video with Hyperframes. Not for AI video generation, prompt craft, or model-based video edits. | `npx skills add PrunaAI/pruna-skills@video-editing -y` |

