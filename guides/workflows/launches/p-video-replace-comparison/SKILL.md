---
name: p-video-replace-comparison
description: Use when the user needs p-video-replace launch reels, wardrobe or SKU swap demos, or slider compares—not motion transfer from a template video.
license: MIT
metadata:
  version: "0.0.1"
---

# P-Video-Replace comparison video

Turn **original footage** + **replacement identity stills** into slider comparison MP4s and multi-scene announcement reels.

**Replace API:** [p-video-replace](../../../tools/video/p-video-replace/SKILL.md)  
**Beat pipeline:** [replace-beats.md](./replace-beats.md)  
**Slider renderer:** [`scripts/generate_video_comparison.py`](./scripts/generate_video_comparison.py) (portable) · repo wrapper: [`scripts/generate_video_animate_comparison.py`](../../../scripts/generate_video_animate_comparison.py)  
**Plan runner:** [`scripts/run_from_plan.py`](./scripts/run_from_plan.py) (default `--phase stills`)  
**Staged generation:** [staged-generation-gate.md](../../../references/shared/staged-generation-gate.md)  
**Visual variety:** [visual-variety-bible.md](../../../references/shared/visual-variety-bible.md)  
**Quality gate:** [p-video-replace-quality-checklist.md](../../../references/video/p-video-replace-quality-checklist.md)

## Quick reference

| Resource | Path |
|----------|------|
| Beat catalog, scene tables, prompt triggers | [replace-beats.md](./replace-beats.md) |
| Runner | [`run_from_plan.py`](./scripts/run_from_plan.py) · default `--phase stills` |
| Slider | [`generate_video_comparison.py`](./scripts/generate_video_comparison.py) |
| Feedback | [requesting-generation-feedback](../../router/requesting-generation-feedback/SKILL.md) |
| Canonical plan | [`output/launches/skills-library-announcement/announcement_plan.json`](../../../output/launches/skills-library-announcement/announcement_plan.json) |

## When to use

| User goal | This workflow |
|-----------|---------------|
| *Replace this person (or product) in this video* | Yes |
| *Animate this picture with motion from another clip* | No — [p-video-animate-comparison](../p-video-animate-comparison/SKILL.md) |
| Before/after still upscale demo | No — [p-image-upscale-comparison](../p-image-upscale-comparison/SKILL.md) |

## Intake: ask before generating

| Topic | Questions |
|-------|-----------|
| **Source footage** | Licensed upload, or generate with **`p-video-avatar`**? How many scenes? |
| **Replace target** | `character` · `clothing` · `object` · `mixed` per row (see [replace-beats.md](./replace-beats.md)) |
| **What to swap** | Faces, outfits only, shelf SKUs, in-hand products, bags, jackets? **How many slots** (1–4)? |
| **Prompt mapping** | `subject_in_video` + per-reference **`instruction_prompt`** (never generic "replace the person") |
| **Replacement stills** | Dynamic **`p-image`** (action poses, single-object desk/hand props, full-body outfits) or uploads? Style bible? |
| **Source motion** | Prefer **`p-video-avatar`** (speaking, single subject); upload when licensed; **`p-video` I2V** only when avatar cannot frame the beat — camera must stay **continuous** |
| **Variant showcase** | Default **`multi_job`** (one ref + mapped prompt per slider step); optional **`multi_image_beat`** for a hybrid finale; `single_call` only for simple multi-slot stills with no VO |
| **Source plate** | **`plate_mode: p-image`** when source cast ≠ plan hero (gender, ethnicity, archetype); default **`hero_edit`** only when same spokesperson arc |
| **Voice** | Avatar rows: speakable **`voice_script`**, natural **`voice_prompt`** (not announcer / spec-sheet) |
| **Delivery** | Reel length, `720p`/`1080p`, concat order, CTA + optional **light background music** ([stable-audio-2.5](../../../tools/audio/stable-audio-2.5/SKILL.md)) |
| **Visual variety** | Cast + **subject-family** diversity? **Dynamic `setting_tag` + `camera_tag` per scene and ref** — never flat grey-wall rows? Named gel lights? **Style tags** per row? [visual-variety-bible.md](../../../references/shared/visual-variety-bible.md). |

Obtain **explicit confirmation** before the first `POST /v1/predictions` ([requesting-generation-feedback](../../router/requesting-generation-feedback/SKILL.md) · [pruna-generative-pipeline](../pruna-generative-pipeline/SKILL.md)).

## Human-in-the-loop (required)

Follow [staged-generation-gate.md](../../../references/shared/staged-generation-gate.md):

1. **Plan approval** — scene table + prompts; user says **go**
2. **Phase A stills** — `p-image` refs + source plates; user reviews JPEGs
3. **Phase B video** — `p-video-avatar` sources + `p-video-replace` only after still approval (`--approve-stills`)
4. **Phase C clip review** — user reviews `clips/`; **`--approve-clips`** before render
5. **Phase D render** — slider MP4s + concat
6. **Optional bed** — after concat, only when clips approved ([Stable Audio 2.5](../../../tools/audio/stable-audio-2.5/SKILL.md))

**Generation package (pick one or combine):**

| Priority | Path |
|----------|------|
| 1 | Phased **curl** via [tool skills](../../../tools/) + [pruna-api.md](../../../references/shared/pruna-api.md) |
| 2 | [`generate_video_comparison.py`](./scripts/generate_video_comparison.py) when MP4 pairs exist |
| 3 | [`run_from_plan.py`](./scripts/run_from_plan.py) with `--phase stills` (default) → `--approve-stills --phase video` |

Install portable bundle: [`README-INSTALL.md`](./README-INSTALL.md) · `./scripts/install_skill.sh p-video-replace-comparison`

## Scene table (replace reel)

| Row type | Models | Output |
|----------|--------|--------|
| **`avatar`** (optional) | `p-image` → `p-video-avatar` | Talking-head hook or CTA |
| **`replace`** | `p-image` (×1–4 refs) → optional `p-image-edit` → `p-video-replace` → slider | Comparison MP4 per scene |
| **`source`** (metadata) | Upload or `p-video-avatar` plate | Original `.mp4` used as `input.video` |

**7-scene skills-library layout**, legacy 8-scene launch, production learnings, persona ladder, prompt triggers, and UGC row patterns: **[replace-beats.md](./replace-beats.md)**.

Scenes 1–3 **`use_case` / `output_label`** name library chapters for VO — they do **not** switch runner skills. Every row still uses **`p-image` refs** + **`p-video-avatar` source** + **`p-video-replace`** unless you branch to [p-video-animate-comparison](../p-video-animate-comparison/SKILL.md).

## Copy this plan

**Canonical:** [`output/launches/skills-library-announcement/announcement_plan.json`](../../../output/launches/skills-library-announcement/announcement_plan.json) · learnings index: [`manifest.md`](../../../output/launches/skills-library-announcement/manifest.md).

```bash
python3 guides/workflows/launches/p-video-replace-comparison/scripts/run_from_plan.py \
  --plan output/launches/skills-library-announcement/announcement_plan.json \
  --out-dir output/launches/skills-library-announcement \
  --fresh --phase stills
# review stills → --approve-stills --phase all --background-music
```

## Replace row pipeline (summary)

```text
Document subject_in_video + replace_target per row
  → p-image reference(s) matched to slot (face / outfit / packshot)
  → optional p-image-edit
  → source video (upload | p-video-avatar | p-video I2V) with continuous camera
  → p-video-replace (video + images[] + explicit instruction_prompt per ref or slot)
  → slider compare MP4
```

**Plan fields (launch / agent plans):** `replace_target`, `replace_mode` (`multi_job` | `single_call`), optional `multi_image_beat`, `source.plate_mode` (`p-image` | `hero_edit`), `source.plate_seed`, `source.subject_in_video`, per-reference `instruction_prompt`, `cast_descriptor`, `palette_tag` per ref. Runner: [`scripts/run_from_plan.py`](./scripts/run_from_plan.py).

Production learnings, dynamic prompts, persona diversity, `beat_label` rules, and **prompt trigger word** tables: **[replace-beats.md](./replace-beats.md)**.

## Slider renderer

Reuses the animate comparison script. Map fields:

| Config field | Replace workflow meaning |
|--------------|-------------------------|
| `source` | **Original** footage (pre-replace) |
| `output` | **Replaced** output (single variant) |
| `source_label` | e.g. `Original footage` |
| `output_label` | e.g. `Replaced` |

Requires `ffmpeg` and Pillow:

```bash
pip install -r scripts/requirements.txt
```

**Single scene:**

```bash
python3 scripts/generate_video_comparison.py \
  --source path/to/original-scene.mp4 \
  --output path/to/replaced-scene.mp4 \
  --render output/scene01_compare.mp4 \
  --source-label "Original footage" \
  --output-label "Replaced"
```

Portable path: `./scripts/generate_video_comparison.py` inside the installed skill.

**Batch:** [`examples/workflows/launches/p-video-replace-comparison/batch.template.json`](../../../examples/workflows/launches/p-video-replace-comparison/batch.template.json)

**Multi-variant slider** (one source, several replacement outputs): [`config.multi-sample.template.json`](../../../examples/workflows/launches/p-video-replace-comparison/config.multi-sample.template.json)

## Example prompt + plan template

- Copy/paste starter: [`examples/workflows/launches/p-video-replace-comparison/example-prompt.md`](../../../examples/workflows/launches/p-video-replace-comparison/example-prompt.md)
- Scene plan JSON: [`examples/workflows/launches/p-video-replace-comparison/scene-plan.template.json`](../../../examples/workflows/launches/p-video-replace-comparison/scene-plan.template.json)
- Launch runner: [`scripts/run_from_plan.py`](./scripts/run_from_plan.py) + plan JSON in `--out-dir` or [`templates/`](./templates/)

## Parallel execution

Within each phase after confirmation:

1. Parallel **`p-image`** for all identity plates in the reel
2. Parallel **`p-image-edit`** per still
3. Parallel **`p-video-avatar`** only for independent source plates
4. Parallel **`p-video-replace`** per scene (or one job per scene when using multi-image `images[]`)
5. Parallel slider renders
6. Sequential concat (ffmpeg) for final reel
7. Optional **background bed** — Replicate [stable-audio-2.5](../../../tools/audio/stable-audio-2.5/SKILL.md) + [`launch_background_music.py`](../../_shared/scripts/launch_background_music.py) mix at low volume

See [parallel-execution.md](../../../references/shared/parallel-execution.md).

## Background music (launch reels)

After ffmpeg concat, add an **instrumental bed** under avatar VO (does not replace dialogue).

**Plan JSON:**

```json
"background_music": {
  "enabled": true,
  "prompt": "Instrumental light electronic pop bed, soft groove and mellow synth pads, calm positive tech atmosphere, understated background music, no vocals, 94 BPM",
  "volume": 0.12,
  "output_name": "announcement_with_music.mp4"
}
```

**Runner** (requires `REPLICATE_API_TOKEN`, `ffmpeg`, `ffprobe`):

```bash
python3 guides/workflows/launches/p-video-replace-comparison/scripts/run_from_plan.py \
  --plan output/launches/skills-library-announcement/announcement_plan.json \
  --out-dir output/launches/skills-library-announcement \
  --assemble-only --background-music
```

Or standalone:

```bash
python3 guides/workflows/_shared/scripts/launch_background_music.py \
  --video output/launches/skills-library-announcement/p_video_replace_announcement.mp4 \
  --volume 0.12
```

Tool skill: [stable-audio-2.5](../../../tools/audio/stable-audio-2.5/SKILL.md) · [replicate-api.md](../../../references/shared/replicate-api.md)

## vs p-video-animate-comparison

| | **Replace comparison** (this skill) | **Animate comparison** |
|---|-------------------------------------|-------------------------|
| Question | Replace people/objects **in** footage | Animate a **still** with copied motion |
| Hero assets | Dynamic **`p-image`** identity plates | Persona stills + motion template |
| Core model | **`p-video-replace`** (`images` 1–4) | **`p-video-animate`** (`image` ×1) |
| Slider | Original vs replaced | Motion template vs animated subject |

## Related

| Topic | Location |
|-------|----------|
| Replace beat detail | [replace-beats.md](./replace-beats.md) |
| Visual variety bible | [visual-variety-bible.md](../../../references/shared/visual-variety-bible.md) |
| Replace model API | [p-video-replace/SKILL.md](../../../tools/video/p-video-replace/SKILL.md) |
| Launch background bed | [stable-audio-2.5/SKILL.md](../../../tools/audio/stable-audio-2.5/SKILL.md) |
| Motion-transfer reels | [p-video-animate-comparison](../p-video-animate-comparison/SKILL.md) |
| Scenario hub | [pruna-generative-pipeline](../pruna-generative-pipeline/SKILL.md) |

## Install

```bash
cp -R guides/workflows/launches/p-video-replace-comparison ~/.cursor/skills/
```

Restart Cursor or start a new chat.
