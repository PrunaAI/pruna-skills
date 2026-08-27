---
name: narrated-multi-scene
description: Use when someone wants a multi-part story with voiceover — episodic B-roll, chaptered promo, or several linked video scenes without on-camera dialogue.
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

In **every reply**, name `` `narrated-multi-scene` `` in backticks. State phase gates using exact phrases **approve plan**, **approve stills**, **approve clips** (user types these to proceed). Do **not** same-turn plan + paid video. Skip-review / burn-credits → follow `generation-diversity` **Red flags**.

## Feedback gates (required)

| Phase | What to show | Proceed when |
|-------|--------------|--------------|
| **0 — Plan** | Scene table, narration lines, `style_bible` | **approve plan** |
| **A — Stills** | Hero + start/end stills per scene | **approve stills** |
| **A2 — TTS** | `audio/narration_*.mp3` per scene — listen | Lines OK (`ffprobe` ≤ ~19s) |
| **B — Video** | `p-video` clips with embedded VO | **approve clips** |
| **D — Bed** | Optional Stable Audio under concat | User accepts |

Execute phases with parallel curl batches — **never** batch `p-video` before still and TTS review.

## Intake: ask before generating

Open intake → **`generation-diversity`** clarification intake.

**Do not** start scene 1 until the **whole** scene plan exists in writing (manifest or table):

| Topic | Questions |
|-------|-----------|
| **Story** | Order of scenes (1…N)? What changes between scenes (location, time, emotion)? |
| **Media source** | Per scene: **generate** stills/TTS with Pruna tools vs **upload** user frames or VO? |
| **Format** | Global `aspect_ratio`; default video **`720p` / `1080p`** and `fps` for triple scenes? |
| **Per scene *i*** | Primary `prompt`? **First frame** (`image`), **last frame** (`last_frame_image`), **narration** (`audio` URL)? Scene-level `resolution` / `fps` / `draft` overrides? |
| **Continuity** | Per scene: **`chain_from_previous`** only when motion continues (same moment/location). Otherwise composed OPENING still + hard cut. End stills via `p-image-edit`; extract last frame when chaining. |
| **Audio** | **Scene anchor triple (preferred):** TTS → upload → **`p-video`** with `image` + `last_frame_image` + **`audio`** (omit `duration`; `save_audio: true`). **Each scene line ≤ ~19s** — P-API caps audio-led clips at **20s**. Optional **Stable Audio** bed in post only. |
| **Visual style** | Locked `style_bible`? **One specific subject/location per still**? Avoid unrelated branding unless the brief asks for it |
| **Global** | Default `aspect_ratio` for text-only scenes? Global `seed` policy? |
| **Runtime** | Target total duration after assembly? |
| **Assembly** | Concat order; narration mux; bed mix volume (~0.08–0.15 under VO)? |

Ask follow-ups until every scene row has enough to build `input` without guessing.

### Scene table (template — fill during intake)

| `#` | Prompt | First frame (`image`) | Last frame (`last_frame_image`) | Narration (`audio`) | Mode |
|-----|--------|----------------------|----------------------------------|---------------------|------|
| 1 | motion prompt | start still | end still → scene 2 | TTS line → upload | triple |
| 2 | | = scene 1 end | end still → scene 3 | TTS line → upload | triple |

**Mode:** `T2V` · `I2V` · `I2V+last` · **`triple`** (`image` + `last_frame_image` + `audio` — omit `duration`)

## How the agent runs this

1. Write the scene table (or plan JSON) → **approve plan**.
2. Hero → parallel `p-image-edit` start/end stills (`pruna-api` parallel batches) → **approve stills**.
3. Parallel Gemini TTS → **duration gate** on every MP3 → upload → listen → proceed.
4. Parallel `p-video` triples once all anchors ready → **approve clips**.
5. ffmpeg concat (± crossfade) → optional bed.

## Workflow (after intake)

### Phase 0 — Stills (parallel when independent)

1. **Hero anchor** — one approved `p-image` or upload.
2. **`p-image-edit`** per scene — **start still** (`edit_prompt`) from hero; **end still** (`last_frame_edit_prompt`) from start still. Parallel after hero exists.
3. **Frame chain (selective):** set `chain_from_previous: true` only when scene *i* continues directly from *i−1*. Use composed start still + hard cut for new beats.

### Phase 1 — Audio (parallel)

`gemini-3.1-flash-tts` per scene → upload each to `/v1/files`.

**Duration gate (required):**

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 audio/narration_01.mp3
```

If any scene exceeds **~19s**, fix before `p-video` — output truncates at the **20s** API max even when `input.audio` is set.

**If a line is too long (pick one or combine):**

| Remedy | When | Action |
|--------|------|--------|
| **Shorten copy** | One beat has too many facts | Cut clauses; keep dates/names; target **≤ ~45 words** (~17–18s) per scene |
| **Faster pace** | Line is right length but slow delivery | Tighten Gemini `style_prompt` (e.g. *~2.3 words/sec, brisk, no filler*); regenerate TTS only |
| **Split scene** | Two story beats in one row | Add scene row + `edit_prompt` / `last_frame_edit_prompt` / narration; one MP3 per row |

### Phase 2 — Video (parallel when all anchors ready)

**Scene anchor triple** — one `p-video` job per row:

```json
{
  "prompt": "...",
  "image": "START_URL",
  "last_frame_image": "END_URL",
  "audio": "NARRATION_URL",
  "resolution": "720p",
  "fps": 24,
  "save_audio": true
}
```

Omit `duration`. **Always** include uploaded `audio` in `input`. Poll all `get_url` until done; retry failed scenes only. Parallel pattern: `pruna-api`.

### Phase 3 — Review

Adjust prompt, stills, or narration; re-run **that scene only**.

### Phase 4 — Assembly

Hard-cut concat (narration already embedded):

```bash
# clips.txt: file 'clips/01.mp4'\nfile 'clips/02.mp4' …
ffmpeg -y -f concat -safe 0 -i clips.txt -c copy film.mp4
```

Optional short crossfade between chained scenes (~0.15s) — use `xfade` / `acrossfade` when joins need softness; hard-cut elsewhere.

**Optional bed** — `stable-audio-2.5` under VO:

```bash
ffmpeg -y -i film.mp4 -i bed.mp3 \
  -filter_complex "[1:a]volume=0.12[bed];[0:a][bed]amix=inputs=2:duration=first[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac film_with_bed.mp4
```

### Phase 5 — Manifest

Scene table + all six URLs per scene (start, end, audio in/out) + prediction ids.

## Frame-chain + narration example (dog story)

```text
Scene 1: composed start,  last=play_end,   audio=vo_1   chain→2
Scene 2: extract(clip_1), last=loss_end,   audio=vo_2   hard cut→3
Scene 3: composed start,  last=search_end, audio=vo_3   chain→4
Scene 4: extract(clip_3), last=tree_end,   audio=vo_4   chain→5
Scene 5: extract(clip_4), last=reunion,   audio=vo_5
```

See `video-prompting` for when to chain vs hard cut, and OPEN/MID/CLOSE prompt structure.

## Related

Related skills:

| Skill | Description | Install |
| --- | --- | --- |
| `image-to-video` | Use when someone wants one short film beat from images — a narrated scene, story moment, or cinematic B-roll with optional voiceover. | `npx skills add PrunaAI/pruna-skills@image-to-video -y` |
| `avatar-multi-scene` | Use when someone wants the same person hosting several clips — multi-segment UGC, comparison reels, or mixed speaking and animated scenes with continuity. | `npx skills add PrunaAI/pruna-skills@avatar-multi-scene -y` |
| `audio-prompting` | Use when crafting TTS, music, or bed prompts for any generative audio model — director style, song structure, and post-production layering. | `npx skills add PrunaAI/pruna-skills@audio-prompting -y` |
| `pruna-api` | Use before any Pruna or Replicate HTTP call — credentials, upload/poll/download, parallel batches, and agent safety. | `npx skills add PrunaAI/pruna-skills@pruna-api -y` |
| `video-editing` | Use when assembling or polishing already-rendered clips with ffmpeg — concat, crossfades, burned captions and subtitles, text/logo overlays, before/after sliders, background music beds, platform export — or when composing a multi-layer HTML combination video with Hyperframes. Not for AI video generation, prompt craft, or model-based video edits. | `npx skills add PrunaAI/pruna-skills@video-editing -y` |

