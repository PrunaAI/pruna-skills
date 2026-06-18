---
name: p-image-try-on-launch
description: Use when the user needs a p-image-try-on launch reel, virtual fitting room demo, fashion vertical showcase, or try-on announcement with narration and background music.
license: MIT
metadata:
  version: "0.0.1"
---

# P-Image-Try-On launch reel

Turn **generated people + garment references** into a multi-vertical announcement reel: **`p-image-try-on`** stills, **`showcase`** clips (garment → person → before/after compare → wipe → try-on hold), **Gemini narration**, and a final **instrumental bed**.

**Showcase renderer:** [`scripts/generate_tryon_showcase.py`](./scripts/generate_tryon_showcase.py) — clothing-change proof only; **not** [p-image-upscale-comparison](../p-image-upscale-comparison/SKILL.md).

**Try-on API:** [p-image-try-on](../../../tools/image/p-image-try-on/SKILL.md)  
**Beat catalog + vertical chapters:** [try-on-beats.md](./try-on-beats.md)  
**Plan runner:** [`scripts/run_from_plan.py`](./scripts/run_from_plan.py) (default `--phase stills`)  
**Staged generation:** [staged-generation-gate.md](../../../references/shared/staged-generation-gate.md)  
**Visual variety:** [visual-variety-bible.md](../../../references/shared/visual-variety-bible.md)  
**Quality gate:** [p-image-try-on-quality-checklist.md](../../../references/image/p-image-try-on-quality-checklist.md)

Install: `./scripts/install_skill.sh p-image-try-on-launch`

## Quick reference

| Resource | Path |
|----------|------|
| Vertical chapters, scene tables, prompt triggers | [try-on-beats.md](./try-on-beats.md) |
| Runner | [`run_from_plan.py`](./scripts/run_from_plan.py) · default `--phase stills` |
| Plan template | [`templates/scene-plan.template.json`](./templates/scene-plan.template.json) |
| Example prompt | [`examples/workflows/launches/p-image-try-on-launch/example-prompt.md`](../../../examples/workflows/launches/p-image-try-on-launch/example-prompt.md) |
| Feedback discipline | [requesting-generation-feedback](../../router/requesting-generation-feedback/SKILL.md) |

## Use cases by vertical

Each reel chapter maps to one **`vertical`** field in the plan. Run [visual-variety-bible.md](../../../references/shared/visual-variety-bible.md) so cast, setting, and garment palette differ across rows.

| Vertical | `vertical` key | What to show | Typical motion |
|----------|--------------|--------------|----------------|
| **E-commerce product visualization** | `ecommerce_pdp` | Garment ref → person → try-on compare | `showcase` |
| **Virtual fitting room** | `virtual_fitting_room` | Selfie base outfit → dressed result | `showcase` |
| **Wholesale & B2B catalog** | `wholesale_catalog` | Same SKU, before/after outfit swap | `showcase` |
| **Lookbook & campaign** | `lookbook_campaign` | Editorial person → campaign garment | `showcase` |
| **UGC ad variations** | `ugc_ads` | Creator + streetwear try-on proof | `showcase` |
| **Personalized outfit recommendations** | `personalized_outfits` | One person · multiple outfits | `showcase_ladder` |

## When to use

| User goal | This workflow |
|-----------|---------------|
| Launch **`p-image-try-on`** with fashion / retail verticals | Yes |
| In-video wardrobe swap inside existing footage | No — [p-video-replace-comparison](../p-video-replace-comparison/SKILL.md) |
| Still-only illustrated story (no try-on API) | No — [illustrated-story-reel](../../verticals/illustrated-story-reel/SKILL.md) |
| Resolution / upscale demo | No — [p-image-upscale-comparison](../p-image-upscale-comparison/SKILL.md) |

## Intake: ask before generating

| Topic | Questions |
|-------|-----------|
| **Verticals** | Which chapters from the table above? All six or a subset? |
| **Cast** | How many distinct people? Gender / ethnicity / age diversity per [visual-variety-bible](../../../references/shared/visual-variety-bible.md)? |
| **Garments** | Flat-lay packshots, on-hanger, or ghost-mannequin? 1–10 refs per try-on row? Set **`type`** per ref (see [garment types](../../../tools/image/p-image-try-on/SKILL.md#garment-types)) — e.g. `tops`, `bottoms`, `outerwear`. |
| **Motion mode** | Default **`showcase`** — garment ref, person photo, side-by-side before/after, wipe, try-on hold. Use **`showcase_ladder`** for multi-outfit rows. |
| **Delivery** | Reel length (~60–90s), `9:16` vs `16:9`, `720p`/`1080p` |
| **Music** | Light **instrumental bed** after concat? Style prompt + volume (~0.12)? |

Obtain **explicit confirmation** before the first `POST /v1/predictions` ([requesting-generation-feedback](../../router/requesting-generation-feedback/SKILL.md)).

## Human-in-the-loop (required)

Follow [staged-generation-gate.md](../../../references/shared/staged-generation-gate.md):

1. **Plan approval** — vertical chapter table + prompts; user says **go**
2. **Phase A stills** — person plates, garment refs, try-on outputs; user reviews JPEGs/PNGs
3. **Phase B video** — `p-video-avatar` / `p-video` / slider MP4s only after still approval (`--approve-stills`)
4. **Phase C audio** — Gemini TTS per scene when plan uses narration overlay (`--approve-stills --phase tts`)
5. **Phase D assemble** — ffmpeg concat
6. **Phase E bed** — **background music** under VO after user accepts concat (`--background-music`)

**Generation package (pick one or combine):**

| Priority | Path |
|----------|------|
| 1 | Phased **curl** via [tool skills](../../../tools/) + [pruna-api.md](../../../references/shared/pruna-api.md) |
| 2 | [`run_from_plan.py`](./scripts/run_from_plan.py) with `--phase stills` → `--approve-stills --phase video --force-video` |
| 3 | [`generate_tryon_showcase.py`](./scripts/generate_tryon_showcase.py) on approved still triplets |

## Scene table (launch reel)

| Row type | Models | Output |
|----------|--------|--------|
| **`try_on` + `showcase`** | `p-image` person + garment → **`p-image-try-on`** → local showcase clip | Garment → person → **before/after** → wipe → try-on |
| **`try_on` + `showcase_ladder`** | same, multiple garments | Repeated outfit swaps on one person |
| **Final mux** | concat → Gemini TTS → **Stable Audio 2.5** bed | `*_with_music.mp4` |

Full persona ladders, garment prompt patterns, and narration lines: **[try-on-beats.md](./try-on-beats.md)**.

## Try-on row pipeline (summary)

```text
p-image person plate (full-body or upper-body, neutral base outfit)
  → p-image garment ref(s) (flat-lay or on-model product shot)
  → p-image-try-on (person_image + garment_images[])
  → slop gate (p-image-try-on-quality-checklist)
  → motion branch:
       avatar  → p-video-avatar (voice_script + video_prompt)
       i2v     → p-video (image = try-on still, optional Gemini TTS mux)
       slider  → before/after still compare MP4
  → concat → optional instrumental bed
```

**Plan fields:** `vertical`, `motion` (`avatar` | `i2v` | `still_slider`), `person.prompt`, `garments[]` (each with `prompt`, optional `type`, optional `gender`), `voice_script`, `narration`, `video_prompt`, `slider_title`. See [`templates/scene-plan.template.json`](./templates/scene-plan.template.json).

## Motion mode guide

| Mode | When | Output |
|------|------|--------|
| **`showcase`** | Single garment proof — garment → person → before/after → wipe → hold | 9:16 MP4 + optional Gemini TTS |
| **`showcase_rapid`** | **Multiple garments** — fast montage, wipe per outfit | Catchy multi-look beat |
| **`showcase_flash`** | **Between beats** — 0.5–1s try-on cuts on same person (`still_from`) | Styles: **`beat_cut`** (white flash + zoom pulse), **`zoom_pulse`**, **`pingpong`**, **`staccato`**, **`shuffle_wipe`** |

**Avatar lip sync:** default **`avatar_use_uploaded_audio`: true** — Gemini TTS (`Sulafat` / `Achird`) → upload → **`p-video-avatar`** with **`audio`** (not `voice_script`). Portrait crop via **`avatar_crop_top_ratio`**. All avatar rows (`motion: avatar`) use **`p-video-avatar`**.
| **`showcase_ladder`** | One person · 2–4 outfit ladder with compare frames | Personalized feed demo |
| **`avatar`** | Feature explainers — presenter **in try-on look** speaks to camera | `p-video-avatar` lip-sync VO |

**Hybrid reel pattern:** alternate **`avatar`** feature beats with **`showcase`** / **`showcase_rapid`** proof beats — explain then show, or show then explain.

**Avatar try-on source:** set **`still_from_previous`: true** on avatar rows so the clip uses the **final try-on still from the prior showcase scene** (last garment in a ladder/rapid). Lock **`persona_gender`** on each cast row and let the runner pick **`Zephyr (Female)`** / **`Puck (Male)`** from `voice_map` — scene `voice` overrides only when gender matches.

**Gender-matched garments:** set **`persona_gender`** on every person row; garment still prompts auto-prefix **Women's** / **Men's** when not already tagged (override per garment with `"gender": "male"` if needed).

**Aspect ratio lock:** set `defaults.output_width` / `output_height` (e.g. **1080×1920** for 9:16). All stills normalized; avatar + showcase clips normalized before concat.

## Narration

Two layers are common on launch reels:

1. **In-clip VO** — `voice_script` on `p-video-avatar` rows (primary for UGC / fitting room).
2. **Scene narration** — Gemini [gemini-3.1-flash-tts](../../../tools/audio/gemini-3.1-flash-tts/SKILL.md) per row when `motion` is `i2v` or `still_slider`:

```json
"narration": {
  "voice": "Kore",
  "style_prompt": "Warm retail storyteller, confident product demo pace, one chapter per vertical",
  "language_code": "en-US"
}
```

Runner: `--phase tts` after still approval. Listen before assemble ([workflow-feedback-gates.md](../../../references/workflows/workflow-feedback-gates.md)).

If narration runs longer than the showcase clip, the runner **holds the last frame** until VO finishes (small tail pad) — narration is never cut with `-shortest`.

## Background music (required for launch delivery)

After ffmpeg concat, add a **low-volume instrumental bed** under dialogue — does not replace VO.

**Plan JSON:**

```json
"background_music": {
  "enabled": true,
  "prompt": "Instrumental fashion-tech pop bed, soft four-on-the-floor groove, warm synth pads, modern retail energy, understated background music, no vocals, 100 BPM",
  "volume": 0.12,
  "output_name": "try_on_launch_with_music.mp4"
}
```

**Runner** (requires `REPLICATE_API_TOKEN`, `ffmpeg`, `ffprobe`):

```bash
python3 guides/workflows/launches/p-image-try-on-launch/scripts/run_from_plan.py \
  --plan output/launches/p-image-try-on-launch/plan.json \
  --out-dir output/launches/p-image-try-on-launch \
  --assemble-only --background-music
```

Or standalone:

```bash
python3 guides/workflows/_shared/scripts/launch_background_music.py \
  --video output/launches/p-image-try-on-launch/try_on_launch.mp4 \
  --volume 0.12 \
  --prompt "Instrumental fashion-tech pop bed, soft groove, no vocals, 100 BPM"
```

Tool: [stable-audio-2.5](../../../tools/audio/stable-audio-2.5/SKILL.md)

## Copy this plan

```bash
python3 guides/workflows/launches/p-image-try-on-launch/scripts/run_from_plan.py \
  --plan guides/workflows/launches/p-image-try-on-launch/templates/scene-plan.template.json \
  --out-dir output/launches/p-image-try-on-launch \
  --fresh --phase stills
# review stills → --approve-stills --phase video
# review clips → --approve-clips --phase tts   (if narration overlay)
# assemble → --approve-audio --phase assemble --background-music
```

## Parallel execution

Within each phase after confirmation:

1. Parallel **`p-image`** for all person plates and garment refs
2. Parallel **`p-image-try-on`** per scene (independent rows)
3. Parallel **`p-video-avatar`** / **`p-video`** per approved try-on still
4. Parallel slider renders (`still_slider` rows)
5. Parallel Gemini TTS
6. Sequential concat → **background bed**

See [parallel-execution.md](../../../references/shared/parallel-execution.md).

## Related

| Topic | Location |
|-------|----------|
| Vertical beat detail | [try-on-beats.md](./try-on-beats.md) |
| Try-on model API | [p-image-try-on/SKILL.md](../../../tools/image/p-image-try-on/SKILL.md) |
| Still before/after renderer | [generate_tryon_showcase.py](./scripts/generate_tryon_showcase.py) |
| Avatar discipline | [avatar-single-scene](../../core/avatar-single-scene/SKILL.md) |
| Scenario hub | [pruna-generative-pipeline](../../router/pruna-generative-pipeline/SKILL.md) |

## Install

```bash
./scripts/install_skill.sh p-image-try-on-launch
```

Restart Cursor or start a new chat.
