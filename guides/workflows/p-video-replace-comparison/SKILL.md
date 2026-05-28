---
name: p-video-replace-comparison
description: Builds dynamic P-Video-Replace showcase reels—character, clothing, object, and mixed swaps with prompt-guided mapping per reference, p-image plates, p-video-avatar or p-video I2V sources, slider compare MP4s, natural avatar VO, optional chill background music (Stable Audio 2.5). Use for launch announcements, UGC/shelf/wardrobe demos; not motion transfer (use p-video-animate-comparison).
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
**Staged generation:** [staged-generation-gate.md](../../../references/staged-generation-gate.md)  
**Visual variety:** [visual-variety-bible.md](../../../references/visual-variety-bible.md)  
**Quality gate:** [p-video-replace-quality-checklist.md](../../../references/p-video-replace-quality-checklist.md)

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
| **Variant showcase** | Default **`multi_job`** (one ref + mapped prompt per slider step); `single_call` only for simple multi-slot stills with no VO |
| **Voice** | Avatar rows: speakable **`voice_script`**, natural **`voice_prompt`** (not announcer / spec-sheet) |
| **Delivery** | Reel length, `720p`/`1080p`, concat order, CTA + optional **chill background music** ([stable-audio-2.5](../../../tools/audio/stable-audio-2.5/SKILL.md)) |
| **Visual variety** | Cast + **subject-family** diversity? **Dynamic `setting_tag` + `camera_tag` per scene and ref** — never flat grey-wall rows? Named gel lights? **Style tags** per row? [visual-variety-bible.md](../../../references/visual-variety-bible.md). |

Obtain **explicit confirmation** before the first `POST /v1/predictions` (same gate as [pruna-generative-pipeline](../pruna-generative-pipeline/SKILL.md)).

## Human-in-the-loop (required)

Follow [staged-generation-gate.md](../../../references/staged-generation-gate.md):

1. **Plan approval** — scene table + prompts; user says **go**
2. **Phase A stills** — `p-image` refs + source plates; user reviews JPEGs
3. **Phase B video** — `p-video-avatar` sources + `p-video-replace` only after approval
4. **Phase C render** — slider MP4s; user reviews before concat
5. **Optional bed** — after concat, [Stable Audio 2.5](../../../tools/audio/stable-audio-2.5/SKILL.md) chill instrumental under VO (`background_music` in plan or `--background-music`)

**Generation package (pick one or combine):**

| Priority | Path |
|----------|------|
| 1 | Phased **curl** via [tool skills](../../../tools/) + [pruna-api.md](../../../references/pruna-api.md) |
| 2 | [`generate_video_comparison.py`](./scripts/generate_video_comparison.py) when MP4 pairs exist |
| 3 | [`run_from_plan.py`](./scripts/run_from_plan.py) with `--phase stills` (default) → `--approve-stills --phase video` |

Install portable bundle: [`README-INSTALL.md`](./README-INSTALL.md) · `./scripts/install_skill.sh p-video-replace-comparison`

## Scene table (replace reel)

| Row type | Models | Output |
|----------|--------|--------|
| **`avatar`** (optional) | `p-image` → `p-video-avatar` | Talking-head hook or CTA |
| **`replace`** | `p-image` (×1–4 refs) → optional `p-image-edit` → `p-video-replace` → slider | Comparison MP4 per scene |
| **`source`** (metadata) | Upload or `p-video-avatar` plate | Original `.mp4` used as `input.video` |

Production-tested launch layout (all replace rows use **`p-video-avatar`** sources unless you have a licensed upload):

| # | Type | `replace_target` | `replace_mode` | Beat |
|---|------|------------------|----------------|------|
| 1 | replace | mixed | `multi_job` | Hook — presenter · blazer · desk product (VO source) |
| 2 | replace | mixed | `multi_job` | UGC install — creator · tee · closed laptop (**loft / rooftop / cafe** — distinct world per ref, varied camera) |
| 3 | replace | clothing | `multi_job` | Stylist talking head — 3 outfit swaps (no I2V walk) |
| 4 | replace | object | `multi_job` | In-game dialogue (`p-video-avatar`) — fantasy weapon swaps on knight |
| 5 | replace | mixed | `multi_job` | Solo cafe — face · jacket · bag on chair (calm VO, no laugh) |
| 6 | replace | object | `multi_job` | Gym — 3 in-hand SKUs + clothing (golden template — keep as-is when iterating) |
| 7 | replace | character | `multi_job` | Game character remix; VO tees **P-Video-Animate** vs Replace |
| 8 | replace | mixed | `multi_job` | CTA — presenter · blazer · desk product (VO source) |

Canonical plan: [`output/p-video-replace-announcement/announcement_plan.json`](../../../output/p-video-replace-announcement/announcement_plan.json). Beat detail + anti-patterns: [replace-beats.md](./replace-beats.md).

## Replace row pipeline (summary)

```text
Document subject_in_video + replace_target per row
  → p-image reference(s) matched to slot (face / outfit / packshot)
  → optional p-image-edit
  → source video (upload | p-video-avatar | p-video I2V) with continuous camera
  → p-video-replace (video + images[] + explicit instruction_prompt per ref or slot)
  → slider compare MP4
```

**Plan fields (launch / agent plans):** `replace_target`, `replace_mode` (`multi_job` | `single_call`), `source.subject_in_video`, per-reference `instruction_prompt`. Runner: [`scripts/run_from_plan.py`](./scripts/run_from_plan.py) uses **per-reference** instructions in `multi_job` rows.

## Production learnings (encode in every plan)

1. **References alone are not enough** — map source slot → reference in **per-reference `instruction_prompt`** (`multi_job`); never reuse one generic line for every variant.
2. **Default `multi_job` + variant slider** — one `p-video-replace` call per reference; easier mapping than `single_call` for mixed UGC, cafe, and SKU ladders.
3. **Prefer `p-video-avatar` sources** — single subject, mouth visible, product **in hand** or prop **on desk/chair**; avoid I2V full-body walks, multi-tube shelf slides, and two-shot cafe (high artifact rate).
4. **Clothing references** — same person **wearing** the target outfit in the ref still (not flat-lay only) when the source is a talking head.
5. **Object / clothing beats on VO clips** — instruction must say *do not change face, lips, jaw, or speech timing*; keep camera subtle during speech (no whip-pan while talking).
6. **Dynamic sources** — continuous camera (gentle dolly, handheld sway); static locked-off plates weaken sliders.
7. **Human avatar copy** — short `voice_script`; `voice_prompt` = conversational, explicitly *no laugh / no announcer* when tone matters.
8. **Vary swap types** — face, wardrobe-only, and object-only beats in the same reel; hook/CTA `mixed` rows should include real blazer + desk-product steps, not face-only.
9. **Do not name competitors** in launch copy; cite Pruna speed/pricing from official docs when needed.
10. **Reference inset on compare MP4s** — `reference_images[]` in compare config; **all** scene reference stills as **small bordered thumbnails** (no text) top-right for the full slider. Set **`reference_inset`: `none`** on a scene to hide.
11. **Eye-catching variety** — plan **`visual_style_tag`**, **`render_medium_tag`**, **`setting_tag`**, **`camera_tag`**, and **`lighting_tag`** per scene **and per reference** when showcasing range; alternate gender/voice where VO allows. **Never** default UGC/install rows to neutral grey wall on source + every ref — use named environments (loft brick, rooftop dusk, cafe wood, LED studio) and varied angles (low three-quarter, three-quarter, slight high angle). Scene 1 **persona ladder** spans photoreal → sketch → 2D → anime → clay → cyberpunk → epic film → anthropomorphic → CG 3D. Run [visual-variety-bible.md](../../../references/visual-variety-bible.md) checklist before API calls.
12. **Full face on talking-head refs** — lead prompts with *entire face visible including eyes and mouth*, head-and-shoulders centered; avoid torso crops that hide eyes (breaks face replace).

## Dynamic eye-catching prompts

Showcase reels must **pop on a phone screen**. Stack these in every `p-image`, `still_edit`, and reference `prompt`:

| Layer | What to write |
|-------|----------------|
| **Style anchor** | photoreal UGC · premium anime · clay stop-motion · cyberpunk · blockbuster adventure film |
| **Bold subject** | statement wardrobe (hot-pink fur, cobalt hoodie, chrome armor), distinct hair, strong silhouette |
| **Distinct world** | named environment layers — loft brick + window bokeh, rooftop dusk, cafe wood panels, rain alley, mirror boutique — **not** neutral grey wall on every UGC/install ref |
| **Named lighting** | in **`p-image` stills** prefer **bright environment** (sunny window, golden afternoon) — not ring light / studio lighting / key light words; use **`lighting_tag`** on the plan row for agents |
| **Palette punch** | one dominant accent color per ref (cobalt, coral, lime, violet) — see [visual-variety-bible.md](../../../references/visual-variety-bible.md) **Creative attractiveness** |
| **Texture / material** | faux fur, holographic gloss, satin, clay grain, crosshatching, chrome armor, walnut grain |
| **Camera / depth** | in **`p-image` stills** write **shot type** — three-quarter from the side, slight high angle, wide shot — not “facing camera”; use **`camera_tag`** on the plan row; shallow depth of field; **single subject one frame** |
| **`swap_visual_bible`** | plan-level line for slider rows — max contrast identity readable at thumbnail size. **Skip on** `Style *` beat labels, anthropomorphic, and object refs (mixed-media collages) |

**`video_prompt`:** continuous motion with **variety** — dolly push-in, slow arc, quarter-orbit, subtle crane-down — vary grammar across scenes; never eight identical “gentle dolly push-in” lines.

**Persona ladder:** each reference = **different** subject family + **render medium** + style tag + setting + lighting; wild jumps (UGC photoreal → **pencil sketch** → **2D ink frame** → anime → clay stop-motion → cyberpunk → epic film → **anthropomorphic** → **CG 3D royal**) beat subtle tweaks.

**Subject diversity:** plan reels with **photoreal humans**, **line-art mediums** (pencil sketch, charcoal, ink wash), **2D animation frames** (hand-drawn, cel anime, flat vector), **3D animation** (stop-motion clay, CG film royals), **fictional characters**, **anthropomorphic presenters**, **wardrobe-only** beats, and **accessory-only** beats — not face-swap only. See **Persona & subject diversity** below.

**Object refs:** vivid prop color (cobalt keyboard, copper cylinder, emerald succulent) on rich walnut desk — still **one object, one frame** (see trigger table).

## UGC & install rows (dynamic worlds)

UGC and “portable install” beats are **not** excuse for flat grey walls. Plan **art-directed locations** on the source plate **and** give each slider ref its **own environment + camera + light** when the row showcases creator range.

| Slot | Source plate | Ref A (recast) | Ref B (recast) | Ref C (wardrobe) |
|------|--------------|----------------|----------------|------------------|
| **Setting** | creative loft, brick, window bokeh | rooftop dusk, city lights | cozy cafe corner, warm wood | moody home studio, LED wash |
| **Camera** | low three-quarter handheld | low angle chest-up | three-quarter chest-up | slight high angle chest-up |
| **Light** | amber window + magenta rim | golden hour rim | teal edge + window daylight | magenta-cyan wash + ring on face |

**Prompt stack:** entire face visible (eyes + mouth) · statement wardrobe · closed laptop or in-hand prop · **bright named environment** · **shot from side / three-quarter / wide** — not ring light or studio lighting language in `p-image` stills (reserve **`camera_tag` / `lighting_tag`** for plan fields and `video_prompt` only).

**Anti-pattern:** `neutral grey wall`, `neutral wall`, `plain grey background` on source **and** all three refs — reads as one boring studio. **Fix:** at minimum, distinct `setting_tag` + colored gel rim per ref; ideally different location families per ref (see skills-library scene 2 plan).

Canonical example: [`output/skills-library-announcement/announcement_plan.json`](../../../output/skills-library-announcement/announcement_plan.json) scene 2.

Positive flash only — obey **Prompt trigger words** below; never negations or e-commerce packshot language.

## Persona & subject diversity

Showcase reels should prove **range**, not one photoreal talking head repeated.

| Subject type | When to use | Prompt cues |
|--------------|-------------|-------------|
| **Photoreal human** | UGC, founder, stylist, recast ladders | ethnicity, age, archetype, statement wardrobe, **entire face visible**, dynamic setting not grey wall |
| **Line art / sketch** | Persona ladder, art-forward hooks | greyscale cinematic portrait, soft graphite tones, seamless neutral background, **mouth visible** |
| **2D animation frame** | Persona ladder, animate-adjacent | hand-drawn ink outlines, watercolor wash, cel anime, flat vector — **single frame**, not storyboard grid |
| **3D animation** | Persona ladder | stop-motion clay texture + miniature set; CG film royal with rounded forms and enchanted environment |
| **Fictional character** | Persona ladder, fantasy beats | fairy-tale royal, fantasy warrior — **adventure film** wording, not game/HUD |
| **Anthropomorphic** | Persona ladder hooks | otter/fox/red panda **presenter**, humanoid proportions, expressive face, **mouth visible**, chest-up medium close-up |
| **Stylized live-action** | Replace rows | cyberpunk, epic film costume — each its own world |
| **Wardrobe-only** | Same talent, new outfit | hot-pink bolero, holo vest — instruction maps **clothing only** |
| **Accessories-only** | Same talent, new jewelry/scarf/hat | pearl choker, silk scarf, wide-brim hat — instruction maps **accessory slot only** |
| **Object / prop** | Desk, in-hand, chair-scale | single vivid object on walnut desk — one frame |

**Rendering medium (`render_medium_tag`):** separate **how it is drawn** from **who it is**. Examples: `photoreal` · `pencil_sketch` · `charcoal` · `watercolor` · `hand_drawn_2d` · `cel_anime_2d` · `flat_vector_2d` · `stop_motion_3d` · `cg_3d_film`. One ladder step = one medium; do not blend sketch + anime in the same ref prompt.

**Sketch / 2D rules:** always **medium close-up**, **mouth visible mid-speech**, **single subject one frame** — avoids storyboard panels and caption strips.

**3D rules:** stop-motion = visible clay + practical lamp; CG film = storybook warmth — distinct refs, not one generic “3D cartoon”.

**Anthropomorphic rules (talking-head / replace):** humanoid torso and face; mouth large enough for lip sync; match source shot size; avoid mascot/icon language (collage trigger).

**Accessory rules:** reference still shows the **accessory worn** on a person when source is a talking head — not flat-lay unless object-only beat.

Plan fields **`cast_descriptor`**, **`render_medium_tag`**, and **`palette_tag`** can note `anthropomorphic otter host`, `fictional fairy-tale royal`, `pencil_sketch`, or `warm_punch` — not only human demographics.

**Creative attractiveness:** vary **color palette**, **fabric texture**, **camera grammar**, and **age/archetype** across scenes — not only face and medium. Run the **Creative attractiveness** and **Variety checklist** sections in [visual-variety-bible.md](../../../references/visual-variety-bible.md).

## Prompt trigger words (never use in `p-image` / `p-image-edit` stills)

Use **positive single-frame wording** instead. Never rely on negations like “no text” in the prompt.

### Text artifacts

| Avoid | Use instead |
|-------|-------------|
| `graphic tee`, printed shirt | plain solid-color tee |
| `neon signs`, storefront signage | neon **color bokeh**, color wash |
| `ring light`, `studio lighting`, `key light`, `rim light`, `gel light` in **`p-image` stills** | **bright environment** — sunny window, golden afternoon, cheerful daylight, warm bedroom |
| `facing camera`, `speaks to camera`, `to camera`, `medium close-up facing camera` in **`p-image` stills** | **shot framing** — three-quarter from the side, slight angle portrait, head-and-shoulders view, wide shot |
| `game`, `game trailer`, `HUD`, `visor`, `UI` | **fantasy/adventure film** portrait, blockbuster film lighting |
| readable monitors, code on screen | soft defocused monitor glow |
| branded labels, magazine, poster | unbranded matte surfaces |
| keyboard key legends, overhead key grid | single wireless keyboard, lifestyle desk detail |
| open laptop, laptop screen, `developer` at desk | **closed laptop lid** toward camera, plain matte lid |
| `decal`, `sticker`, `label` on props | solid **accent patch** on closed lid |
| `USB`, `hub`, port close-up, spec sheet | generic **desk accessory**, cylindrical form |

### Collage / multi-panel artifacts

These words often produce **side-by-side**, grid, or contact-sheet layouts — fatal for reference stills.

| Avoid | Use instead |
|-------|-------------|
| `packshot`, `hero packshot`, `product still` | **single** [object] on desk, one object centered |
| `overhead flat lay`, `key tops`, catalog layout | lifestyle desk detail, shallow depth of field |
| `comparison`, `before and after`, `side by side` | (omit — slider is post-render only) |
| `collage`, `montage`, `contact sheet`, `grid` | single subject, one frame |
| `variant grid`, `tier ladder`, `lookbook spread`, `mood board` | one persona still per API call |
| `multiple angles`, `dual`, `split` | medium close-up, one camera angle |
| `same` (matching prior ref), `matching`, `identical` | describe the one frame directly; one subject one frame |
| `keyboard`, `wireless keyboard`, key legends | rounded keyboard **form**, side angle, one object |
| `geometric sculpture`, `abstract` prop | smooth ceramic **vase** or single solid object |
| `portrait sketch on paper`, `textured cream paper`, `charcoal`, `crosshatching`, `fine-art illustration` | greyscale **cinematic portrait**, soft graphite tones, seamless neutral background |
| `animation frame`, `storyboard`, `golden-age animation` | cel **illustration**, one illustration one frame |
| `layered` jewelry, `stack`, `statement earrings` | **single** choker, one hoop earring |
| `social ad`, `hyper-saturated` ad language | creator vlog portrait, ring light halo |
| `3D render`, enchanted castle, ivy arches | one 3D **character**, soft blurred background |
| `lifestyle desk detail` | three-quarter angle, one object on walnut desk |
| `lifestyle desk detail` | three-quarter angle, one object on walnut desk |
| `neutral grey wall`, `neutral wall`, `plain grey background` on source + all refs | **distinct** location per ref — loft brick, rooftop dusk, cafe wood, LED studio |
| `mirror`, `fitting room`, `boutique mirrors`, `mirror bokeh` | **plain colored wall** backdrop — mirrors cause multi-panel reflections |
| `cinematic portrait`, `greyscale cinematic`, `graphite portrait` | stylized **muted-tone** presenter, plain empty backdrop, sole subject fills frame |
| `minimal desk`, `video call`, founder at desk on **wardrobe-only** refs | plain wall backdrop only — desk + blazer triggers conference grids |
| `Each ladder step a different visual world` in **`swap_visual_bible`** | omit — literal collage trigger; keep swap bible to wardrobe/identity pop only |
| `developer`, home office with monitors | creative loft or cafe; **closed laptop lid** prop only |

13. **Object reference stills** — one prop, one frame, in-context desk scale (matches mug/hand swap). Never isolated e-commerce packshot language for replace refs.

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

**Batch:** [`examples/workflows/p-video-replace-comparison/batch.template.json`](../../../examples/workflows/p-video-replace-comparison/batch.template.json)

**Multi-variant slider** (one source, several replacement outputs): [`config.multi-sample.template.json`](../../../examples/workflows/p-video-replace-comparison/config.multi-sample.template.json)

## Example prompt + plan template

- Copy/paste starter: [`examples/workflows/p-video-replace-comparison/example-prompt.md`](../../../examples/workflows/p-video-replace-comparison/example-prompt.md)
- Scene plan JSON: [`examples/workflows/p-video-replace-comparison/scene-plan.template.json`](../../../examples/workflows/p-video-replace-comparison/scene-plan.template.json)
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

See [parallel-execution.md](../../../references/parallel-execution.md).

## Background music (launch reels)

After ffmpeg concat, add an **instrumental bed** under avatar VO (does not replace dialogue).

**Plan JSON:**

```json
"background_music": {
  "enabled": true,
  "prompt": "Instrumental chill lo-fi ambient bed, soft piano and warm pads, no vocals, 85 BPM",
  "volume": 0.12,
  "output_name": "announcement_with_music.mp4"
}
```

**Runner** (requires `REPLICATE_API_TOKEN`, `ffmpeg`, `ffprobe`):

```bash
python3 guides/workflows/p-video-replace-comparison/scripts/run_from_plan.py \
  --plan output/skills-library-announcement/announcement_plan.json \
  --out-dir output/skills-library-announcement \
  --assemble-only --background-music
```

Or standalone:

```bash
python3 guides/workflows/_shared/scripts/launch_background_music.py \
  --video output/skills-library-announcement/p_video_replace_announcement.mp4 \
  --volume 0.12
```

Tool skill: [stable-audio-2.5](../../../tools/audio/stable-audio-2.5/SKILL.md) · [replicate-api.md](../../../references/replicate-api.md)

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
| Visual variety bible | [visual-variety-bible.md](../../../references/visual-variety-bible.md) |
| Replace model API | [p-video-replace/SKILL.md](../../../tools/video/p-video-replace/SKILL.md) |
| Launch background bed | [stable-audio-2.5/SKILL.md](../../../tools/audio/stable-audio-2.5/SKILL.md) |
| Motion-transfer reels | [p-video-animate-comparison](../p-video-animate-comparison/SKILL.md) |
| Scenario hub | [pruna-generative-pipeline](../pruna-generative-pipeline/SKILL.md) |

## Install

```bash
cp -R guides/workflows/p-video-replace-comparison ~/.cursor/skills/
```

Restart Cursor or start a new chat.
