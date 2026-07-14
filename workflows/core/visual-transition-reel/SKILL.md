---
name: visual-transition-reel
description: Use when the user needs a visual montage, transitions between stills, action-sequence reel, or multi-scene piece where narration is optional or absent.
license: MIT
metadata:
  version: "0.0.2"
---

# Scene transition video (Pruna `p-video` + `p-image` / `p-image-edit`)

Each scene = one **`p-video`** job steered by **two stills** and a **transition prompt**. Assembly is **outside** Pruna (ffmpeg concat). Narration is **optional** — default mode is visual-only (scene anchor **pair**).

Canonical spec: [scene-anchor-pair.md](../../../../../references/video/scene-anchor-pair.md)

See [p-video](../../../../tools/video/p-video/SKILL.md), [p-image](../../../../tools/image/p-image/SKILL.md), [p-image-edit](../../../../tools/image/p-image-edit/SKILL.md), [parallel-execution.md](../../../../../references/shared/parallel-execution.md), and [pruna-api.md](../../../../../references/shared/pruna-api.md).

For narrated films (pair + TTS audio), use [narrated-multi-scene](../narrated-multi-scene/SKILL.md) instead.

**Staged generation:** [staged-generation-gate.md](../../../../../references/shared/staged-generation-gate.md) · [workflow-feedback-gates.md](../../../../../references/workflows/workflow-feedback-gates.md). Default runner **`--phase stills`**.

## Feedback gates (required)

| Phase | What to show | Proceed when |
|-------|--------------|--------------|
| **0 — Plan** | Scene table, transition prompts, `style_bible` | **approve plan** |
| **A — Stills** | Hero + start/end PNGs | **approve stills** |
| **B — Video** | `clips/*.mp4` | **approve clips** |
| **D — Bed** | Final after concat + optional bed | User accepts |

## Intake: ask before generating

**Do not** start scene 1 until the **whole** scene plan exists in writing (manifest or table):

| Topic | Questions |
|-------|-----------|
| **Story** | Scene order (1…N)? What changes between beats (location, time, emotion)? |
| **Per scene *i*** | **Start still** (`edit_prompt` or upload)? **End still** (`last_frame_edit_prompt`)? **Transition `video_prompt`** (OPEN/MID/CLOSE motion)? `duration_seconds`? |
| **Continuity** | Per scene: **`chain_from_previous`** only when motion continues. Otherwise composed OPENING still + hard cut. |
| **Stills source** | Generate via **`p-image`** hero + **`p-image-edit`**, or user-supplied photo pairs? |
| **Global** | `style_bible`? `aspect_ratio`? `ritual_seed`? `frame_chain_mode` (`extract_last_frame` vs `parallel_vignettes`)? |
| **Audio** | Native SFX only (default), optional [stable-audio-2.5](../../../../tools/audio/stable-audio-2.5/SKILL.md) bed in post, or upgrade to triple + TTS? |
| **Assembly** | Concat order; chain crossfade (~0.12–0.15s) vs hard cut (0)? Target total duration? |

Ask follow-ups until every scene row has enough to build `input` without guessing.

### Scene table (template)

| `#` | Start (`image`) | End (`last_frame_image`) | Transition prompt | Duration | Chain? |
|-----|-----------------|--------------------------|-------------------|----------|--------|
| 1 | `edit_prompt` → still | `last_frame_edit_prompt` → still | OPEN/MID/CLOSE motion | 5s | no |
| 2 | = scene 1 end *or* extract(clip 1) | end still | motion prompt | 4s | yes / no |

## Workflow (after intake)

### Phase 0 — Hero (`p-image`)

One approved anchor still when generating from text:

1. **`p-image`** with `hero_prompt` + `style_bible` + [random seed ritual](../../../references/shared/random-seed-ritual.md) (SSoT)
2. Slop gate — approve before branching edits

Skip when every scene uses **uploaded** start/end images.

### Phase 1 — Start stills (`p-image-edit`, parallel)

For each scene without an uploaded start image:

1. Upload hero URL to `/v1/files`
2. **`p-image-edit`** with `edit_prompt` + hero in `images[]`
3. Download → `{scene_id}.png`

Run all start stills **in parallel** after hero exists.

### Phase 2 — End stills (`p-image-edit`, parallel)

For each scene with `last_frame_edit_prompt`:

1. Upload start still URL
2. **`p-image-edit`** with `last_frame_edit_prompt` + start still in `images[]`
3. Download → `{scene_id}_last.png`

Run all end stills **in parallel** once start stills exist.

### Phase 3 — Video (`p-video`)

**Scene anchor pair** — one job per row:

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

Use [`p_video_payload.py`](../_shared/scripts/p_video_payload.py) — **`duration` set, no `audio`**.

Poll all `get_url` until done; retry failed scenes only.

### Phase 4 — Review

Adjust transition prompt, stills, or duration; re-run **that scene only** (`--only SCENE_ID`).

### Phase 5 — Assembly

1. **Normalize** clip audio (48 kHz stereo) if concat fails on mixed formats
2. **Concat** via [`concat_clips.py`](../_shared/scripts/concat_clips.py) with per-join crossfades
3. **Optional bed** — [stable-audio-2.5](../../../../tools/audio/stable-audio-2.5/SKILL.md) under native SFX

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

## Portable runner

Default **`--phase stills`**. Phased flow:

```bash
mkdir -p output/core/visual-transition-reel/my-transitions/{stills,clips}
cp workflows/core/visual-transition-reel/templates/transition-plan.template.json \
   output/core/visual-transition-reel/my-transitions/plan.json

python3 workflows/core/visual-transition-reel/scripts/run_from_plan.py \
  --plan output/core/visual-transition-reel/my-transitions/plan.json \
  --out-dir output/core/visual-transition-reel/my-transitions

python3 .../run_from_plan.py --plan ... --out-dir ... --approve-stills --phase video
python3 .../run_from_plan.py --plan ... --out-dir ... --approve-clips --phase assemble
```

Flags: `--phase hero|stills|video|assemble|all` · `--approve-stills` · `--approve-clips` · `--assemble-only` · `--only SCENE_ID …` · `--regen-stills` · `--regen-clips` · `--skip-assembly`

Requires `PRUNA_API_KEY`. Optional bed needs `REPLICATE_API_TOKEN`.

## When to chain vs hard cut

| Use **`chain_from_previous: true`** | Use **`chain_from_previous: false`** |
|-------------------------------------|--------------------------------------|
| Same location, motion continues | New location or story beat |
| Subject mid-action into next beat | Emotional pause or time jump |
| You will **`extract_last_frame`** from prior clip | Montage vignettes (`parallel_vignettes`) |

## Related

- One beat: [image-to-video](../image-to-video/SKILL.md)
- Narrated triple: [narrated-multi-scene](../narrated-multi-scene/SKILL.md)
- Scenario hub: [pruna-generative-pipeline](../pruna-generative-pipeline/SKILL.md) (Recipe Q)
- Example prompt: [./example-prompt.md](./example-prompt.md)
