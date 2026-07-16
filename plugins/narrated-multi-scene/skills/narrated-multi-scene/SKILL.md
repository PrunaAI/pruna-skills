---
name: narrated-multi-scene
description: Use when someone wants a multi-part story with voiceover — episodic B-roll, chaptered promo, or several linked video scenes without on-camera dialogue.
license: MIT
metadata:
  version: "1.0.4"
depends:
  - p-image
  - p-image-edit
  - p-video
  - gemini-3.1-flash-tts
  - stable-audio-2.5
---

# Multi-scene AI video (Pruna `p-video` only)

Each scene = one **`p-video`** job (same model, separate predictions). Assembly is **outside** Pruna (ffmpeg or your editor). No **`p-video-avatar`** in this workflow.

See [p-video](../../../../tools/video/p-video/SKILL.md) (first/last frame chaining), [scene-anchor-triple.md](./references/scene-anchor-triple.md), [scene-anchor-pair.md](https://github.com/PrunaAI/pruna-skills/tree/main/references/shared/scene-anchor-pair.md) (visual-only alternative), [audio-post-production.md](https://github.com/PrunaAI/pruna-skills/tree/main/references/shared/audio-post-production.md), and [pruna-api.md](./references/pruna-api.md).

For **visual transitions without narration**, use [visual-transition-reel](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/visual-transition-reel/skills/visual-transition-reel/SKILL.md) instead.

For **educational explainers** (history, science, nature, how-it-works) with narrator + in-story character dialogue, use [interactive-explainer](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/interactive-explainer/skills/interactive-explainer/SKILL.md) instead of narrator-only tables.

**Staged generation:** [staged-generation-gate.md](./references/staged-generation-gate.md) · [workflow-feedback-gates.md](./references/workflow-feedback-gates.md)

## Feedback gates (required)

| Phase | What to show | Proceed when |
|-------|--------------|--------------|
| **0 — Plan** | Scene table, narration lines, `style_bible` | **approve plan** |
| **A — Stills** | Hero + start/end stills per scene | **approve stills** |
| **A2 — TTS** | `audio/narration_*.mp3` per scene — listen | Lines OK |
| **B — Video** | `p-video` clips with embedded VO | **approve clips** |
| **D — Bed** | Optional Stable Audio under concat | User accepts |

Execute phases manually or with phased curl — no bundled runner. **Never** batch `p-video` before still and TTS review.

## Intake: ask before generating

**Do not** start scene 1 until the **whole** scene plan exists in writing (manifest or table):

| Topic | Questions |
|-------|-----------|
| **Story** | Order of scenes (1…N)? What changes between scenes (location, time, emotion)? |
| **Per scene *i*** | Primary `prompt`? **First frame** (`image`), **last frame** (`last_frame_image`), **narration** (`audio` URL)? `resolution` / `fps` / `draft`? |
| **Continuity** | Per scene: **`chain_from_previous`** only when motion continues (same moment/location). Otherwise composed OPENING still + hard cut. End stills via `p-image-edit`; extract last frame when chaining. |
| **Audio** | **Scene anchor triple (preferred):** TTS → upload → **`p-video`** with `image` + `last_frame_image` + **`audio`** (omit `duration`; `save_audio: true`). **Each scene line ≤ ~19s** — P-API caps audio-led clips at **20s**. Optional **Stable Audio** bed in post only. |
| **Visual style** | Locked `style_bible`? **One specific subject/location per still** (painterly illustration, period film still, etc.)? Avoid unrelated branding (e.g. science-show nebula) unless the brief asks for it |
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

## Workflow (after intake)

### Phase 0 — Stills (parallel when independent)

1. **Hero anchor** — one approved `p-image` or upload.
2. **`p-image-edit`** per scene — **start still** (`edit_prompt`) from hero; **end still** (`last_frame_edit_prompt`) from start still. Parallel after hero exists.
3. **Frame chain (selective):** set `chain_from_previous: true` only when scene *i* continues directly from *i−1*. Use composed start still + hard cut for new beats.

### Phase 1 — Audio (parallel)

[Gemini TTS](../../../../tools/audio/gemini-3.1-flash-tts/SKILL.md) per scene → upload each to `/v1/files`.

**Duration gate (required):** after TTS, `ffprobe` each MP3. If any scene exceeds **~19s**, fix before `p-video` — output truncates at the **20s** API max even when `input.audio` is set. Use [`validate_narration_duration`](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/_shared/scripts/p_video_payload.py) in runners.

**If a line is too long (pick one or combine):**

| Remedy | When | Action |
|--------|------|--------|
| **Shorten copy** | One beat has too many facts | Cut clauses; keep dates/names; target **≤ ~45 words** (~17–18s) per scene |
| **Faster pace** | Line is right length but slow delivery | Tighten Gemini `style_prompt` (e.g. *~2.3 words/sec, brisk, no filler*); regenerate TTS only |
| **Split scene** | Two story beats in one row | Add scene row + `edit_prompt` / `last_frame_edit_prompt` / `scene_lines` entry; one narration file per row |

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

Omit `duration`. **Always** include uploaded `audio` in `input` — silent `duration`-only renders truncate narration on concat. Poll all `get_url` until done; retry failed scenes only.

### Phase 3 — Review

Adjust prompt, stills, or narration; re-run **that scene only**.

### Phase 4 — Assembly

1. **Concat** clips in scene order (narration already embedded).
2. **Optional bed** — [stable-audio-2.5](../../../../tools/audio/stable-audio-2.5/SKILL.md) under VO ([`launch_background_music.py`](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/_shared/scripts/launch_background_music.py)).

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

See [scene-anchor-triple.md](./references/scene-anchor-triple.md) for when to chain vs hard cut, and OPEN/MID/CLOSE prompt structure.

## Related

- Single clip: [image-to-video](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/image-to-video/skills/image-to-video/SKILL.md)
- Talking avatars: [avatar-multi-scene](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/avatar-multi-scene/skills/avatar-multi-scene/SKILL.md)
- Audio layering: [audio-post-production.md](https://github.com/PrunaAI/pruna-skills/tree/main/references/shared/audio-post-production.md)
- Parallel vs phased: [parallel-execution.md](./references/parallel-execution.md)
- Generic chain: [pruna-generative-pipeline](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/pruna-generative-pipeline/skills/pruna-generative-pipeline/SKILL.md)
