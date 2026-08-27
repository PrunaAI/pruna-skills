---
name: visual-transition-reel
description: Use when someone wants a montage with transitions between shots — action-sequence reel or multi-scene piece where narration is optional.
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
| `stable-audio-2.5` | Use when someone wants light instrumental background music — an ambient bed under dialogue or underscore for reels and explainers. | `npx skills add PrunaAI/pruna-skills@stable-audio-2.5 -y` |

Or install the full suite once: `npx skills add PrunaAI/pruna-skills@pruna -y`

Follow each skill's **Before generating** / craft sections — do not restate guide content here.

## Workflow habit

In **every reply**, name `` `visual-transition-reel` `` in backticks. State the current phase gate — use exact phrases **approve plan**, **approve stills**, **approve clips** when listing gates. Do **not** same-turn plan + paid video. Skip-review / burn-credits → follow `generation-diversity` **Red flags**.

## Skill boundary

Montage with **transitions between composed video clips** — not a picture-book slideshow.

**Redirect before intake:**

- Picture-book / illustrated slideshow / Ken Burns story with narration → `` `illustrated-story-reel` ``
- Cinematic multi-scene B-roll chapters (full `p-video` scenes) → `` `narrated-multi-scene` ``

## When NOT to use

Use a different skill instead:

| Skill | Description | Install |
| --- | --- | --- |
| `illustrated-story-reel` | Use when someone wants a slideshow story with narration or music — picture-book illustrated frames with Ken Burns or gentle p-video motion. | `npx skills add PrunaAI/pruna-skills@illustrated-story-reel -y` |
| `narrated-multi-scene` | Use when someone wants a multi-part story with voiceover — episodic B-roll, chaptered promo, or several linked video scenes without on-camera dialogue. | `npx skills add PrunaAI/pruna-skills@narrated-multi-scene -y` |
| `interactive-explainer` | Use when someone wants an educational explainer with a host and characters — history or science shorts with dialogue, not voiceover-only B-roll. | `npx skills add PrunaAI/pruna-skills@interactive-explainer -y` |

## Feedback gates (required)

| Phase | What to show | Proceed when |
|-------|--------------|--------------|
| **0 — Plan** | Scene table, transition prompts, `style_bible` | **approve plan** |
| **A — Stills** | Hero + start/end PNGs | **approve stills** |
| **B — Video** | `clips/*.mp4` | **approve clips** |
| **D — Bed** | Final after concat + optional bed | User accepts |

## Intake: ask before generating

Open intake → **`generation-diversity`** clarification intake.

**Do not** start scene 1 until the **whole** scene plan exists in writing (manifest or table):

| Topic | Questions |
|-------|-----------|
| **Story** | Scene order (1…N)? What changes between beats (location, time, emotion)? |
| **Per scene *i*** | **Start still** (`edit_prompt` or upload)? **End still** (`last_frame_edit_prompt`)? **Transition `video_prompt`** (OPEN/MID/CLOSE motion)? `duration_seconds`? |
| **Continuity** | Per scene: **`chain_from_previous`** only when motion continues. Otherwise composed OPENING still + hard cut. |
| **Stills source** | Generate via **`p-image`** hero + **`p-image-edit`**, or user-supplied photo pairs? |
| **Format** | `aspect_ratio`; transition clips **`720p` / `1080p`**? |
| **Global** | `style_bible`? `ritual_seed`? `frame_chain_mode` (`extract_last_frame` vs `parallel_vignettes`)? |
| **Audio** | Native SFX only (default), optional `stable-audio-2.5` bed in post, or upgrade to triple + TTS? |
| **Assembly** | Concat order; chain crossfade (~0.12–0.15s) vs hard cut (0)? Target total duration? |

Ask follow-ups until every scene row has enough to build `input` without guessing.

### Anchor pairs + `video-prompting`

Start/end stills and transition motion use **`video-prompting`** scene-anchor pairs — physically **reachable** end states; **same subject** in both plates (identity preserved). Craft OPEN/MID/CLOSE in transition prompts; still OPENING/CLOSING prefixes on `p-image-edit` plates per `image-prompting`.

### Scene table (template)

| `#` | Start (`image`) | End (`last_frame_image`) | Transition prompt | Duration | Chain? |
|-----|-----------------|--------------------------|-------------------|----------|--------|
| 1 | `edit_prompt` → still | `last_frame_edit_prompt` → still | OPEN/MID/CLOSE motion | 5s | no |
| 2 | = scene 1 end *or* extract(clip 1) | end still | motion prompt | 4s | yes / no |

## How the agent runs this

1. Copy [templates/transition-plan.template.json](./templates/transition-plan.template.json) → fill from intake → **approve plan**.
2. Hero → parallel start stills → parallel end stills → **approve stills**.
3. Parallel (or sequential for extract-chain) `p-video` pair jobs → **approve clips**.
4. ffmpeg concat ± per-join crossfade → optional bed.

## Generation phases

| Phase | Action |
|-------|--------|
| **stills** | Hero + start/end PNGs (default first stop) |
| **video** | After stills approval — `p-video` pairs |
| **assemble** | After clips approval — concat ± bed |

## Workflow (after intake)

### Phase 0 — Hero (`p-image`)

One approved anchor photo when generating a new image:

1. **`p-image`** with `hero_prompt` + `style_bible` + ritual seed from `generation-diversity`
2. Slop gate — approve before branching edits

Skip when every scene uses **uploaded** start/end images.

### Phase 1 — Start stills (`p-image-edit`, parallel)

For each scene without an uploaded start image:

1. Upload hero URL to `/v1/files`
2. **`p-image-edit`** with `edit_prompt` + hero in `images[]`
3. Download → `{scene_id}.png`

Run all start stills **in parallel** after hero exists (`pruna-api`).

### Phase 2 — End stills (`p-image-edit`, parallel)

For each scene with `last_frame_edit_prompt`:

1. Upload start still URL
2. **`p-image-edit`** with `last_frame_edit_prompt` + start still in `images[]`
3. Download → `{scene_id}_last.png`

Run all end stills **in parallel** once start stills exist.

### Phase 3 — Video (`p-video`)

**Scene anchor pair** — one job per row (`duration` set, **no** `audio`):

```json
{
  "prompt": "OPEN: hold. MID: dolly in, subject turns. CLOSE: settle on end pose.",
  "image": "START_URL",
  "last_frame_image": "END_URL",
  "duration": 5,
  "resolution": "720p",
  "fps": 24
}
```

| `frame_chain_mode` | Start frame when `chain_from_previous: true` | Render order |
|--------------------|----------------------------------------------|--------------|
| **`extract_last_frame`** | ffmpeg last frame from prior clip | Sequential for chained scenes |
| **`parallel_vignettes`** | always composed start still | Parallel (montage / hard cuts) |
| **`planned_stills`** | prior scene end still URL | Parallel once all stills exist |

Extract last frame when chaining:

```bash
ffmpeg -y -sseof -0.05 -i clips/01.mp4 -frames:v 1 stills/02_from_prev.png
```

Poll all `get_url` until done; retry failed scenes only.

### Phase 4 — Review

Adjust transition prompt, stills, or duration; re-run **that scene only**.

### Phase 5 — Assembly

1. **Normalize** clip audio (48 kHz stereo) if concat fails on mixed formats
2. **Concat** — hard cuts:

```bash
ffmpeg -y -f concat -safe 0 -i clips.txt -c copy reel.mp4
```

Per-join **crossfade** (~0.12–0.15s) on chain joins — use `xfade` (video) + `acrossfade` (audio); hard-cut joins stay at 0.

3. **Optional bed** — `stable-audio-2.5` under native SFX (`amix`, bed ~0.10–0.15)

### Phase 6 — Manifest

Scene table + start/end URLs + prediction ids + `chain_from_previous` flags.

## Transition prompt shape

Write **`video_prompt`** as motion between the two plates — not a repeat of the still descriptions:

```text
OPEN: [what holds at start frame]
MID: [camera + subject motion developing]
CLOSE: [how motion settles into end frame]
```

**Limits:** prefer 4–5s beats; avoid extreme camera whips; start/end plates should differ clearly but share identity and lighting.

## When to chain vs hard cut

| Use **`chain_from_previous: true`** | Use **`chain_from_previous: false`** |
|-------------------------------------|--------------------------------------|
| Same location, motion continues | New location or story beat |
| Subject mid-action into next beat | Emotional pause or time jump |
| You will **`extract_last_frame`** from prior clip | Montage vignettes (`parallel_vignettes`) |

## Related

Related skills:

| Skill | Description | Install |
| --- | --- | --- |
| `image-to-video` | Use when someone wants one short film beat from images — a narrated scene, story moment, or cinematic B-roll with optional voiceover. | `npx skills add PrunaAI/pruna-skills@image-to-video -y` |
| `narrated-multi-scene` | Use when someone wants a multi-part story with voiceover — episodic B-roll, chaptered promo, or several linked video scenes without on-camera dialogue. | `npx skills add PrunaAI/pruna-skills@narrated-multi-scene -y` |
| `video-editing` | Use when assembling or polishing already-rendered clips with ffmpeg — concat, crossfades, burned captions and subtitles, text/logo overlays, before/after sliders, background music beds, platform export — or when composing a multi-layer HTML combination video with Hyperframes. Not for AI video generation, prompt craft, or model-based video edits. | `npx skills add PrunaAI/pruna-skills@video-editing -y` |

