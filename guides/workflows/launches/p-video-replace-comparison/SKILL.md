---
name: p-video-replace-comparison
description: Builds dynamic P-Video-Replace launch reels—character, clothing, object, and mixed swaps with prompt-guided mapping per reference, p-image plates, p-video-avatar or p-video I2V sources, slider compare MP4s, natural avatar VO, optional light background music (Stable Audio 2.5). Use for launch announcements, UGC/shelf/wardrobe demos; not motion transfer (use p-video-animate-comparison).
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

Obtain **explicit confirmation** before the first `POST /v1/predictions` (same gate as [pruna-generative-pipeline](../pruna-generative-pipeline/SKILL.md)).

## Human-in-the-loop (required)

Follow [staged-generation-gate.md](../../../references/shared/staged-generation-gate.md):

1. **Plan approval** — scene table + prompts; user says **go**
2. **Phase A stills** — `p-image` refs + source plates; user reviews JPEGs
3. **Phase B video** — `p-video-avatar` sources + `p-video-replace` only after approval
4. **Phase C render** — slider MP4s; user reviews before concat
5. **Optional bed** — after concat, [Stable Audio 2.5](../../../tools/audio/stable-audio-2.5/SKILL.md) light instrumental under VO (`background_music` in plan or `--background-music`)

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

Production-tested **skills library** layout (7 scenes — canonical plan [`output/launches/skills-library-announcement/announcement_plan.json`](../../../output/launches/skills-library-announcement/announcement_plan.json)):

| # | Type | `replace_target` | Beat | Source host (unique per row) |
|---|------|------------------|------|------------------------------|
| 1 | replace | character | **p-image** ladder — UGC · sketch · 2D cel | Latina fitness creator, rooftop sunrise |
| 2 | replace | character | **p-video-animate** — anime · clay · cyberpunk | East Asian filmmaker, mirror boutique |
| 3 | replace | character | **p-video-replace** — warrior · mascot · 3D royal | Black documentary host (40s), brutalist plaza |
| 4 | replace | mixed | Portable install — recast ×2 · wardrobe · **`multi_image_beat`** | Middle Eastern advocate + **closed hardcover notebook** in hand |
| 5 | replace | character | Staged gate — **full recasts** (3 different people) · **`multi_image_beat`** | Nordic stylist, mural alley |
| 6 | replace | object | Curl + renderers — in-hand tumbler → puck / cylinder / succulent | Black gym creator (40s), boardwalk |
| 7 | replace | mixed | CTA — recast · wardrobe · prop · **`multi_image_beat`** | South Asian founder, street market |

Legacy 8-scene product launch: [`output/launches/p-video-replace-announcement/announcement_plan.json`](../../../output/launches/p-video-replace-announcement/announcement_plan.json). Beat detail + anti-patterns: [replace-beats.md](./replace-beats.md).

## Skills-library narrative rows

Scenes 1–3 **`use_case` / `output_label`** name library chapters (**p-image**, **p-video-animate**, **p-video-replace**) for the VO story — they do **not** switch runner skills. Every row still uses **`p-image` reference stills** + **`p-video-avatar` source** + **`p-video-replace`** unless you explicitly branch to [p-video-animate-comparison](../p-video-animate-comparison/SKILL.md).

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
11. **Eye-catching variety** — plan **`visual_style_tag`**, optional **`render_medium_tag`**, **`setting_tag`**, **`camera_tag`**, and **`lighting_tag`** per scene **and per reference** when showcasing range; alternate gender/voice where VO allows. **Never** default UGC/install rows to neutral grey wall on source + every ref — use named environments (loft brick, rooftop dusk, cafe wood, LED studio) and varied angles (low angle, side angle, slight high angle). Scene 1 **persona ladder** spans photoreal → sketch → 2D → anime → clay → cyberpunk → epic film → anthropomorphic → CG 3D. Run [visual-variety-bible.md](../../../references/shared/visual-variety-bible.md) checklist before API calls.
12. **Full face on talking-head refs** — lead prompts with *entire face visible including eyes and mouth*; avoid torso crops that hide eyes (breaks face replace).
13. **`plate_mode: p-image` per scene** — when the source host differs from the plan hero (gender, ethnicity, age band, archetype), generate a fresh source plate with `still_edit` + `plate_seed`. **Never** `p-image-edit` a female hero into a male advocate (mushy identity).
14. **Cast ledger across scenes** — launch reels prove range: **different source host per scene row** + **different people on recast refs** (not three outfit tweaks on one face). Spread ethnicity, age (20s–40s+), and archetype (fitness creator, filmmaker, stylist, gym trainer).
15. **Dynamic still body language** — mid-gesture, leaning in, walking stride frozen, over-shoulder turn — not static passport poses. Pair with **shallow depth of field** and one **palette accent** per ref.
16. **In-hand props for object/mixed beats** — closed **hardcover notebook**, tumbler at chest, mug on side table. **No laptops, keyboards, or screens** in source or refs (swap targets fail or trigger UI text).
17. **`multi_image_beat`** — after per-ref `multi_job` steps, one slider finale with 2–4 `reference_indices` and mapped slot instructions (`clips/NN_replaced_multi.mp4`). Use on install, staged gate, and CTA rows.
18. **Phase A regen** — prompt fixes require **deleting** the target JPEG(s) or **`--fresh`**; scoped `--from-scene N --phase stills` **reuses** existing files if present.
19. **Weather wording** — describe bright open-sky environments positively. **Do not** use rain, wet pavement, puddles, or anti-rain negations (`no rain`, `dry neon`) in prompts — models latch onto trigger words.

## Dynamic eye-catching prompts

Showcase reels must **pop on a phone screen**. Stack these in every `p-image`, `still_edit`, and reference `prompt`:

| Layer | What to write |
|-------|----------------|
| **Style anchor** | photoreal UGC · premium anime · clay stop-motion · cyberpunk · blockbuster adventure film |
| **Bold subject** | statement wardrobe (hot-pink fur, cobalt hoodie, chrome armor), distinct hair, strong silhouette |
| **Distinct world** | named environment layers — loft brick + window bokeh, rooftop dusk, cafe wood panels, neon arcade corridor, mirror boutique — **not** neutral grey wall on every UGC/install ref |
| **Named lighting** | in **`p-image` stills** prefer **bright environment** (sunny window, golden afternoon) — not ring light / studio lighting / key light words; use **`lighting_tag`** on the plan row for agents |
| **Palette punch** | one dominant accent color per ref (cobalt, coral, lime, violet) — see [visual-variety-bible.md](../../../references/shared/visual-variety-bible.md) **Creative attractiveness** |
| **Texture / material** | faux fur, holographic gloss, satin, clay grain, crosshatching, chrome armor, walnut grain |
| **Camera / depth** | in **`p-image` stills** write **shot type** — slight angle from the side, slight high angle, wide shot — not “facing camera” or “three-quarter”; use **`camera_tag`** on the plan row; shallow depth of field; **single subject one frame** |
| **`swap_visual_bible`** | plan-level line for slider rows — max contrast identity readable at thumbnail size. **Skip on** `Style *` beat labels, anthropomorphic, and object refs (mixed-media collages) |

**`video_prompt`:** continuous motion with **variety** — dolly push-in, slow arc, quarter-orbit, subtle crane-down — vary grammar across scenes; never eight identical “gentle dolly push-in” lines.

**Persona ladder:** each reference = **different** subject family + **render medium** + style tag + setting + lighting; wild jumps (UGC photoreal → **pencil sketch** → **2D ink frame** → anime → clay stop-motion → cyberpunk → epic film → **anthropomorphic** → **CG 3D royal**) beat subtle tweaks.

**Subject diversity:** plan reels with **photoreal humans**, **line-art mediums** (pencil sketch, charcoal, ink wash), **2D animation frames** (hand-drawn, cel anime, flat vector), **3D animation** (stop-motion clay, CG film royals), **fictional characters**, **anthropomorphic presenters**, **wardrobe-only** beats, and **accessory-only** beats — not face-swap only. See **Persona & subject diversity** below.

**Object refs:** vivid prop color (cobalt puck, copper cylinder, emerald succulent) in hand or on side table — still **one object, one frame** (see trigger table).

## `beat_label` and `swap_visual_bible` (runner)

[`run_from_plan.py`](./scripts/run_from_plan.py) prepends plan **`swap_visual_bible`** to reference `p-image` prompts **except** when `skip_swap_visual_bible()` matches:

| `beat_label` prefix / value | Skip swap bible? |
|-----------------------------|------------------|
| `Image ·`, `Motion ·`, `Video ·`, `Replace ·`, `Phase A ·` | yes — stylized / ladder refs carry their own look |
| `Look A`, `Look B`, `Accessories`, `Recast`, `Recast A`, `Recast B`, `Wardrobe` | yes |
| `anthropomorphic`, `fictional 3d`, `object` | yes |
| Generic `Variant N` or unset | no — gets swap bible for photoreal pop |

Use **`beat_label`** consistently so persona-ladder refs are not double-styled.

## UGC & install rows (dynamic worlds)

UGC and “portable install” beats are **not** excuse for flat grey walls. Plan **art-directed locations** on the source plate **and** give each slider ref its **own environment + camera + light** when the row showcases creator range.

| Slot | Source plate | Ref A (recast) | Ref B (recast) | Ref C (wardrobe) |
|------|--------------|----------------|----------------|------------------|
| **Setting** | creative loft, brick, window bokeh | rooftop dusk, city lights | cozy cafe corner, warm wood | moody home studio, LED wash |
| **Camera** | low angle handheld | low angle chest-up | side angle chest-up | slight high angle chest-up |
| **Light** | amber window + magenta rim | golden hour rim | teal edge + window daylight | magenta-cyan wash + ring on face |

**Prompt stack:** entire face visible (eyes + mouth) · statement wardrobe · **closed hardcover notebook or in-hand tumbler** · **bright named environment** · **side angle / low angle / wide shot** — not ring light or studio lighting language in `p-image` stills (reserve **`camera_tag` / `lighting_tag`** for plan fields and `video_prompt` only).

**Anti-pattern:** `neutral grey wall`, `neutral wall`, `plain grey background` on source **and** all three refs — reads as one boring studio. **Fix:** at minimum, distinct `setting_tag` + colored gel rim per ref; ideally different location families per ref (see skills-library scene 2 plan).

Canonical example: [`output/launches/skills-library-announcement/announcement_plan.json`](../../../output/launches/skills-library-announcement/announcement_plan.json) — full cast ledger + `plate_mode` per scene.

Positive flash only — obey **Prompt trigger words** below; never negations or e-commerce packshot language.

## Persona & subject diversity

Showcase reels should prove **range**, not one photoreal talking head repeated.

| Subject type | When to use | Prompt cues |
|--------------|-------------|-------------|
| **Photoreal human** | UGC, founder, stylist, recast ladders | ethnicity, age, archetype, statement wardrobe, **entire face visible**, dynamic setting not grey wall |
| **Line art / sketch** | Persona ladder, art-forward hooks | **stylized muted-tone** presenter, soft grey tones, art-studio skylight, **mouth visible** — not charcoal/crosshatching |
| **2D animation frame** | Persona ladder, animate-adjacent | hand-drawn ink outlines, watercolor wash, cel anime, flat vector — **single frame**, not storyboard grid |
| **3D animation** | Persona ladder | stop-motion clay texture + miniature set; CG film royal with rounded forms and enchanted environment |
| **Fictional character** | Persona ladder, fantasy beats | fairy-tale royal, fantasy warrior — **adventure film** wording, not game/HUD |
| **Anthropomorphic** | Persona ladder hooks | otter/fox/red panda **presenter**, humanoid proportions, expressive face, **mouth visible**, chest-up medium close-up |
| **Stylized live-action** | Replace rows | cyberpunk, epic film costume — each its own world |
| **Wardrobe-only** | Same talent, new outfit | hot-pink bolero, holo vest — instruction maps **clothing only** |
| **Accessories-only** | Same talent, new jewelry/scarf/hat | pearl choker, silk scarf, wide-brim hat — instruction maps **accessory slot only** |
| **Object / prop** | Desk, in-hand, chair-scale | single vivid object on walnut desk — one frame |

**Rendering medium (`render_medium_tag`):** separate **how it is drawn** from **who it is**. Examples: `photoreal` · `pencil_sketch` · `charcoal` · `watercolor` · `hand_drawn_2d` · `cel_anime_2d` · `flat_vector_2d` · `stop_motion_3d` · `cg_3d_film`. One ladder step = one medium; do not blend sketch + anime in the same ref prompt.

**Sketch / 2D rules:** **wide or side-angle** framing, **mouth visible mid-speech**, **single subject one frame** — avoids storyboard panels and caption strips.

**3D rules:** stop-motion = visible clay + practical lamp; CG film = storybook warmth — distinct refs, not one generic “3D cartoon”.

**Anthropomorphic rules (talking-head / replace):** humanoid torso and face; mouth large enough for lip sync; match source shot size; avoid mascot/icon language (collage trigger).

**Accessory rules:** reference still shows the **accessory worn** on a person when source is a talking head — not flat-lay unless object-only beat.

Plan fields **`cast_descriptor`**, optional **`render_medium_tag`**, and **`palette_tag`** can note `anthropomorphic otter host`, `fictional fairy-tale royal`, `pencil_sketch`, or `warm_punch` — not only human demographics.

**Creative attractiveness:** vary **color palette**, **fabric texture**, **camera grammar**, and **age/archetype** across scenes — not only face and medium. Run the **Creative attractiveness** and **Variety checklist** sections in [visual-variety-bible.md](../../../references/shared/visual-variety-bible.md).

## Prompt wording scope

| Layer | Negations OK? | Notes |
|-------|---------------|-------|
| **`references[].prompt` / `still_edit`** | **No** — positive single-frame wording only | Trigger table below |
| **`style_bible` (plan root)** | **Yes** — agent metadata | e.g. *No laptops, computers, screens* — not sent as the full still prompt alone |
| **`video_prompt`** | **Yes** for motion | *speaks to camera*, *glance toward mug* — mouth must stay in frame |
| **Weather / rain** | **Never** in still prompts | No rain, wet pavement, or anti-rain negations (`no rain`, `dry neon`) |

## Prompt trigger words (`p-image` / `p-image-edit` stills only)

Use **positive single-frame wording** in reference and source plate prompts. Do not rely on negations like “no text” in still prompts.

### Text artifacts

| Avoid | Use instead |
|-------|-------------|
| `graphic tee`, printed shirt | plain solid-color tee |
| `neon signs`, storefront signage | neon **color bokeh**, color wash |
| `ring light`, `studio lighting`, `key light`, `rim light`, `gel light` in **`p-image` stills** | **bright environment** — sunny window, golden afternoon, cheerful daylight, warm bedroom |
| `facing camera`, `speaks to camera`, `to camera`, `medium close-up facing camera` in **`p-image` stills** | **shot framing** — slight angle from the side, slight angle portrait, head-and-shoulders view, wide shot |
| `three-quarter`, `three quarter`, `3/4`, `three-quarter angle`, `three-quarter shot` in **`p-image` stills** | **side angle chest-up**, **slight angle from the side**, **low angle from below**, **head-and-shoulders view** |
| `game`, `game trailer`, `HUD`, `visor`, `UI` | **fantasy/adventure film** portrait, blockbuster film lighting |
| readable monitors, code on screen | soft defocused monitor glow |
| branded labels, magazine, poster | unbranded matte surfaces |
| keyboard key legends, overhead key grid | **closed hardcover notebook** in hand, or rounded prop form |
| open laptop, laptop screen, `developer` at desk | **Legacy product launch only** — new plans: **hardcover notebook** or **tumbler at chest** |
| `decal`, `sticker`, `label` on props | solid **accent** on notebook spine or matte prop surface |
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
| `portrait sketch on paper`, `textured cream paper`, `charcoal`, `crosshatching`, `fine-art illustration` | **stylized muted-tone** presenter, soft grey tones, art-studio skylight |
| `animation frame`, `storyboard`, `golden-age animation` | cel **illustration**, one illustration one frame |
| `layered` jewelry, `stack`, `statement earrings` | **single** choker, one hoop earring |
| `social ad`, `hyper-saturated` ad language | creator vlog portrait, ring light halo |
| `3D render`, enchanted castle, ivy arches | one 3D **character**, soft blurred background |
| `lifestyle desk detail` | slight angle, one object on walnut desk |
| `neutral grey wall`, `neutral wall`, `plain grey background` on source + all refs | **distinct** location per ref — loft brick, rooftop dusk, cafe wood, LED studio |
| `mirror`, `fitting room`, `boutique mirrors`, `mirror bokeh` | **plain colored wall** backdrop — *exception:* single-subject **neon editorial boutique** with gel reflections and one person (skills-library scene 2) — never fitting-room grids |
| `cinematic portrait`, `greyscale cinematic`, `graphite portrait`, `graphite tones` | **stylized muted-tone** presenter, soft grey tones, sole subject one frame |
| `minimal desk`, `video call`, founder at desk on **wardrobe-only** refs | plain wall backdrop only — desk + blazer triggers conference grids |
| `Each ladder step a different visual world` in **`swap_visual_bible`** | omit — literal collage trigger; keep swap bible to wardrobe/identity pop only |
| `developer`, home office with monitors | creative loft or cafe; **closed hardcover notebook** in hand |
| `rain`, `wet pavement`, `puddle`, `no rain`, `dry neon` (anti-rain negations) | **bright open-sky**, sunny window, golden afternoon, neon arcade corridor |

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
