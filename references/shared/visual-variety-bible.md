# Visual variety bible

Shared guidance for **eye-catching** Pruna launch reels — comparison sliders, announcement plans, and multi-scene pieces.

Use this whenever you plan **`p-image`**, **`p-image-edit`**, **`p-video-avatar`**, **`p-video-animate`**, or **`p-video-replace`** rows. Run the **Variety checklist** at the bottom before the first API call.

## Goal

Launch and demo reels should feel **art-directed**, not like the same talking head in the same office repeated eight times. Deliberately vary:

- **Cast** — gender, age band, ethnicity, persona archetype
- **Setting** — background / environment (never repeat the same location + framing twice in a row)
- **Camera** — angle, shot size, movement grammar
- **Lighting** — time of day, key/fill mood, practical vs cinematic
- **Visual style** — photoreal, pencil sketch, hand-drawn 2D, cel anime, flat vector, stop-motion clay, CG 3D film, cyberpunk, blockbuster film, editorial, etc.
- **Render medium** — how the frame is made: `photoreal` · `pencil_sketch` · `hand_drawn_2d` · `cel_anime_2d` · `stop_motion_3d` · `cg_3d_film` (orthogonal to subject family)

**Rule:** Within one **scene row**, lock a local **style bible** so references in that row match (e.g. all three anime refs share the same cel-shaded look). **Across scene rows**, push variety — alternate worlds, angles, and lighting.

## Dynamic prompt stack (eye-catching)

Every still prompt should feel **art-directed and thumb-stopping**, not generic stock. Build in order:

1. **Style + subject** — who they are + one statement wardrobe piece  
2. **World** — 2–3 concrete environment cues (city bokeh, mirror panels, miniature teal lamp, twin moons)  
3. **Lighting name** — in **`p-image` / reference stills**: bright environment (sunny window, cheerful daylight, golden afternoon). **Avoid** ring light, studio lighting, key/rim/gel light **wording** in still prompts — those belong in plan `lighting_tag` + `video_prompt`, not `p-image`.  
4. **Shot framing** — in still prompts: slight angle from the side, wide shot, slight high angle — **not** “facing camera”, “three-quarter”, or “3/4”. Record angle in plan `camera_tag`.  
5. **`swap_visual_bible`** (plan) — amplify contrast on persona-ladder refs  

**Anti-pattern:** flat “neutral wall, soft natural light” on **every row in a scene** — especially UGC/install beats with three grey-wall refs. **Fix:** distinct location family per ref (loft · rooftop · cafe · LED studio) + named gel rim + varied **`camera_tag`** (low angle, side angle, slight high angle).

See **Prompt patterns** below — flash without text/collage artifacts.

## Creative attractiveness (beyond cast & medium)

Subject diversity is necessary but not sufficient. Thumb-stopping frames also need **color**, **composition**, **texture**, and **motion** variety.

### Color palette ladder

Assign a **`palette_tag`** per scene or ref so sliders do not all read as teal-and-amber:

| Palette | Wardrobe + light pairing |
|---------|--------------------------|
| **Warm punch** | coral wall + magenta-cyan LED + gold chain |
| **Cool contrast** | cobalt hoodie + teal edge light |
| **Split gel** | rose-gold key + cyan-magenta rim (editorial) |
| **Monochrome pop** | charcoal + single vivid accent (lime crew, orange sculpture) |
| **Earth luxe** | walnut desk + copper prop + tungsten accent |
| **Neon editorial** | violet hair + cherry-blossom bokeh + magenta-teal ambient |

**Rule:** one **dominant accent color** per ref at thumbnail scale — avoid muddy mid-tones everywhere.

### Texture & material

Name fabrics and surfaces in prompts — models respond strongly to material words:

- faux fur · holographic puffer · satin wrap · matte clay · crosshatching · glossy chrome armor · walnut grain · matte ceramic

Scene 3 already stacks texture beats (fur, holo, pearl/gold); reuse that pattern on wardrobe rows elsewhere.

### Composition & depth

- **Shallow DOF** + gel reflections (single-subject neon boutique) or city window bokeh (studio) — separates subject from background  
- **Foreground anchor** — mug, **closed hardcover notebook**, tumbler at chest gives replace sliders a readable swap target  
- **Single subject one frame** — always; negative space on one side reads cleaner in inset thumbnails  

### Age & profession spread

Not every scene needs “tech founder early 30s.” Rotate:

- Gen-Z UGC creator · mid-30s creative director · late-20s advocate · **40s+ expert/trainer** for one VO row  
- Archetypes beyond tech: stylist, chef, fitness creator, museum docent — when the narrative allows  

### Camera & motion (reel-level)

Current plan anti-pattern to avoid: every scene `medium_cu_dolly_in`. Spread:

| Scene role | Suggested `camera_tag` | `video_prompt` grammar |
|------------|------------------------|-------------------------|
| Hook ladder | medium_cu_dolly_in + quarter-orbit | dolly + orbit |
| UGC install | low_angle_handheld | handheld sway + arc left + push |
| UGC ref ladder | low angle · side angle · slight high angle | vary per ref within one scene row |
| Editorial gate | medium_cu_handheld | slow arc right |
| Desk props | medium_cu_slow_arc | arc + push |
| CTA | medium_cu_crane_settle | dolly + crane-down |

Vary **gaze beats** in `video_prompt` (glance to prop, bookshelf, mirror) — not only straight-to-lens.

### Slider pacing

Long persona ladders (7–9 refs) need tighter **`slider_seconds`** (1.25–1.5) or trim refs — otherwise hook scene dominates reel runtime.

### Quality gates before Phase B

- Ref still readable at **256px wide** (identity + accent color)  
- Adjacent refs differ in **medium + palette + setting**, not just hair color  
- `instruction_prompt` colors/materials **match** reference prompt (lime crew ≠ forest green; copper ≠ silver)  
- Source `video_prompt` props **match** `still_edit` (no mug glance if no mug in plate)

## Cast diversity

Plan a **cast ledger** before generation. For **skills-library / launch reels** (not single-spokesperson arcs):

| Rule | Guidance |
|------|----------|
| **Source host** | **Different person per scene row** — `plate_mode: p-image` + unique `cast_descriptor`. Do not hero-edit one female presenter into every male/advocacy row. |
| **Reference beats** | Prefer **full recasts** (different ethnicity, age, archetype per ref) over three wardrobe tweaks on one face when proving library range. |
| **Gender** | Alternate **`persona_gender`** and matching Pruna **`voice`** (`Zephyr (Female)` / `Puck (Male)`) across scenes when lip-sync VO matters. Face-swap refs must stay **same gender** as the source subject on talking-head beats. |
| **Ethnicity / region** | Name specific, respectful descriptors in prompts (South Asian, East Asian, Black, Latina, Middle Eastern, Nordic, Mediterranean, etc.) — spread representation across the reel, not one token face. |
| **Age** | Mix early 20s creator energy, mid-30s founder, 40s+ expert — match wardrobe and setting to age. |
| **Persona archetype** | UGC creator, corporate trainer, fantasy warrior, anime hero, clay character, cyberpunk netrunner, fairy-tale royal, **anthropomorphic otter/fox presenter**, documentary host, gym creator, stylist, etc. |
| **Subject family** | Photoreal human · fictional character · anthropomorphic (humanoid) · stylized 3D · wardrobe-only · accessories-only · object prop |

**Eye-catching persona ladder (replace hook / animate slider):** one source performance → 5–7 **wildly different** reference stills — e.g. photoreal UGC → premium anime → claymation → cyberpunk → epic film warrior → **anthropomorphic library host** → **fairy-tale 3D royal**. Each ref gets its **own environment, lighting, wardrobe, and subject type**.

**Wardrobe & accessories:** dedicate whole slider steps to **outfit-only** (bolero, vest) and **accessory-only** (scarf, choker, hat, statement earrings) with per-reference `instruction_prompt` naming the slot — same talent, new look, lips unchanged.

## Background & setting ladder

No two consecutive scene rows should share the **same location type + shot size**. Rotate through distinct worlds:

| Setting family | Example backgrounds |
|----------------|---------------------|
| **Domestic / UGC** | bedroom ring light, **creative loft brick**, rooftop dusk, cozy cafe corner, moody LED studio — use **one per ref**, not grey wall ×3 |
| **Commercial** | boutique, gym floor, outdoor cafe, rooftop at dusk |
| **Institutional** | classroom whiteboard, news desk, museum gallery |
| **Fantasy / sci-fi** | stone temple courtyard, alien canyon twin moons, neon arcade corridor, enchanted garden |
| **Stylized miniature** | clay living room set, diorama street, stop-motion bookshelf nook |
| **Urban / editorial** | cherry-blossom night street, brutalist plaza, subway platform bokeh |

Record **`setting_tag`** per scene in the plan (e.g. `"neon_anime_alley"`, `"clay_living_room"`, `"temple_courtyard"`) and verify no duplicate tags in adjacent rows.

## Camera angle & movement ladder

Vary **shot size**, **angle**, and **movement** per scene. Never default every row to medium close-up + gentle dolly.

| Angle / size | When to use |
|--------------|-------------|
| Extreme close-up (eyes / mouth) | Hook tension, lip-sync proof |
| Medium close-up (chest-up) | Default VO rows — mouth visible |
| Medium wide (waist-up) | Wardrobe beats, props in frame |
| Low angle (heroic) | Game knight, blockbuster reveal |
| High angle (vulnerable / editorial) | Documentary, stylized anime |
| Over-shoulder turning in | Explainer, product demo |
| Profile side angle | Stylized refs when motion allows |

**Movement grammar** (prefix `video_prompt` with continuous camera):

- gentle dolly push-in · slow arc left · subtle handheld sway · orbit quarter-left · crane-down settle · tracking follow (silent B-roll only)

**Anti-pattern:** eight scenes, all `medium close-up, gentle dolly push-in`.

## Lighting ladder

Name lighting in every **`p-image` prompt**, **`still_edit`**, and reference still:

| Mood | Prompt cues |
|------|-------------|
| Soft overcast documentary | even skin, neutral shadows |
| Golden hour warm | rim light, amber fill, long shadows |
| Neon / cyberpunk | magenta-cyan edge light, wet reflections |
| Anime film dramatic | strong key, colored bounce, neon bokeh |
| Stop-motion practical | warm desk lamp, miniature set glow |
| Blockbuster / game cinematic | motivated sun shafts, volumetric haze |
| Clean educational | bright even key, soft classroom fill |
| Low-key cinematic | single motivated source, deep background falloff |

Alternate lighting families across scenes — not only "soft natural light" on every row.

## Visual style ladder

For **showcase / launch** reels, plan at least **4 distinct visual styles** across the full piece. Pick from (mix and match):

| Style tag | Prompt direction |
|-----------|------------------|
| **Photoreal UGC** | smartphone-adjacent, natural skin, real locations |
| **Photoreal commercial** | crisp product labels, controlled studio or location |
| **Pencil / charcoal sketch** | crosshatching on cream paper, art-studio daylight, mouth visible |
| **Hand-drawn 2D animation** | ink outlines, watercolor wash, golden-age animation palette — **single frame** |
| **Premium anime (2D cel)** | cel-shaded, film-grade compositing, stylized hair/eyes |
| **Flat vector 2D** | bold shapes, limited palette, motion-graphics friendly |
| **Disney / Pixar 3D (CG film)** | rounded forms, storybook warmth, enchanted environments |
| **Claymation / stop-motion 3D** | visible clay texture, miniature sets, practical lighting |
| **Cyberpunk** | chrome, neon arcade corridor, HUD-free (no readable UI text) |
| **Blockbuster movie** | anamorphic cues, epic scale, costume drama |
| **Editorial fashion** | bold wardrobe, shallow DOF, magazine angles |
| **Documentary** | handheld honesty, available light |
| **Meme / reaction** | dorm, gaming chair, exaggerated expression (launch scene 7 pattern) |
| **Anthropomorphic** | humanoid otter/fox/red panda presenter, expressive face, mouth visible, cozy set |

**Rendering medium ladder (persona hooks):** aim for **5+ mediums** in one slider when showcasing range — e.g. photoreal → pencil sketch → 2D ink frame → cel anime → stop-motion clay → CG 3D royal. Tag optional `render_medium_tag` per ref in plans.

**Animate rows:** generate **one persona still per style** on the same motion template — each still carries its own background, lighting, and rendering style while matching pose/framing to the template.

**Replace rows:** stylized refs (anime, clay, cyberpunk, **anthropomorphic**, **fictional 3D**) work best on **persona-ladder** hooks or **character** beats; use dedicated rows for **wardrobe-only** and **accessory-only** swaps; keep object beats as single props in frame.

## Plan fields (agents & JSON plans)

Add to scene plans and manifests:

| Field | Purpose |
|-------|---------|
| `visual_style_tag` | e.g. `anime_cinematic`, `clay_stop_motion`, `pencil_sketch`, `hand_drawn_2d` |
| `render_medium_tag` | optional: `photoreal` · `pencil_sketch` · `hand_drawn_2d` · `cel_anime_2d` · `stop_motion_3d` · `cg_3d_film` |
| `palette_tag` | optional dominant accent pairing: `warm_punch` · `cool_contrast` · `split_gel` · `monochrome_pop` · `neon_editorial` |
| `setting_tag` | unique environment label per row |
| `camera_tag` | e.g. `low_angle_mc`, `extreme_cu`, `over_shoulder` |
| `lighting_tag` | e.g. `golden_hour`, `neon_night`, `practical_clay` |
| `persona_gender` | `female` / `male` — lock voice + face-swap gender |
| `cast_descriptor` | one-line identity (ethnicity, age, archetype, **anthropomorphic otter host**, **fictional royal**) |
| `subject_family` | optional: `photoreal_human` · `fictional_character` · `anthropomorphic` · `wardrobe` · `accessories` · `object` |

**Style bible (project level):** one sentence for **technical** consistency (aspect ratio, photoreal skin when photoreal). **Do not** use the style bible to force every scene into the same look — use **`visual_style_tag`** per row for deliberate variety.

**Never use prompt trigger words** that cause stray text or multi-panel collages — see blocked phrases in **Prompt patterns** below. Prefer positive single-frame wording only.

## Prompt patterns

### Photoreal recast (replace / avatar)

```text
Documentary street portrait, woman mid-30s, South Asian, curly auburn hair, emerald coat,
low angle from below, city bokeh background, bright open-sky daylight,
entire face visible including eyes and mouth, walking stride frozen mid-step, one person one frame.
```

### UGC install row (source + per-ref worlds)

**Source plate:** creative loft, exposed brick, teal window bokeh, low angle handheld, amber key + magenta rim.

**Ref A — rooftop recast:** low angle chest-up, cobalt hoodie, city lights bokeh, golden hour rim, **closed hardcover notebook** at chest.

**Ref B — cafe recast:** side angle chest-up, orange hoodie, warm wood panels, teal edge light, **closed hardcover notebook** at chest.

**Ref C — wardrobe:** slight high angle, lime crewneck, magenta-cyan LED studio wash, ring light on face, **closed hardcover notebook** at chest.

Never reuse `neutral grey wall` on source and all three refs.

### Pencil sketch persona

```text
Stylized muted-tone woman presenter, soft grey tones, north-facing art studio with soft skylight,
wide shot slight high angle, mouth open mid-word turning from profile, sole subject one frame.
```

Avoid in **`p-image` still prompts:** charcoal, pencil, paper, crosshatching, drawing, illustration, **cinematic portrait**, **greyscale cinematic**, **graphite portrait** — they trigger contact-sheet and split-screen collages. **`style_bible`** negations (e.g. no laptops) are fine at plan root — not in per-still positive prompts.

### Hand-drawn 2D animation frame

```text
Hand-painted cel illustration of woman presenter, fluid ink outlines and soft peach watercolor wash background,
slight angle from the side, mouth visible mid-speech, warm golden afternoon atmosphere, single subject one frame.
```

### Anime persona (animate / replace ladder)

```text
Premium anime cinematic young woman hero, cel-shaded film look, violet hair, iridescent jacket,
cherry-blossom rooftop at dusk with neon color bokeh, low heroic angle from the side,
mouth visible mid-speech, bright clear evening atmosphere, single character one frame.
```

### Claymation persona

```text
Stop-motion claymation character woman, visible clay texture, chunky knit scarf, round glasses,
miniature handmade cozy living room set with tiny lamp and bookshelf, medium close-up,
mouth sculpted for speech, warm practical stop-motion desk-lamp lighting.
```

### Disney / fairy-tale 3D

```text
Classic fairy-tale royal princess cinematic 3D render, elegant ball gown, delicate tiara,
enchanted castle garden at golden hour with ivy arches and lantern bokeh, medium close-up,
mouth visible, storybook blockbuster film lighting.
```

### Cyberpunk

```text
Cyberpunk netrunner woman, chrome undercut, iridescent jacket, neon arcade corridor with magenta-cyan edge light,
low angle from below, mouth visible mid-speech, bright electric atmosphere, single subject one frame.
```

## Ecommerce try-on & photoreal personas

Public examples across **`p-image`**, **`p-image-try-on`**, and **`p-video-avatar`** should not share one “white studio + plain tee + medium dolly” template.

| Rule | Guidance |
|------|----------|
| **Unified bar** | [generation-diversity.md](./generation-diversity.md) · [realistic-persona-showcase.md](./realistic-persona-showcase.md)
| **Person plate** | Photoreal **`p-image`** editorial prompts → slop gate |
| **Try-on** | Garment tiers + preservation — [p-image-try-on-quality-checklist.md](../image/p-image-try-on-quality-checklist.md) |
| **Avatar motion** | Unique **`video_prompt`** per clip; natural **`voice_script`** |
| **Cast** | Diversity ledger — gender, age, ethnicity spread |
| **Playground** | Pin try-on refs on [p-image-try-on](https://replicate.com/prunaai/p-image-try-on); match with diverse [p-video-avatar](https://replicate.com/prunaai/p-video-avatar) examples — @ShinyTaskForce |

**Try-on → avatar handoff:** approved try-on still → optional upscale → **`p-video-avatar`**; lock **`seed`** from person-plate generation.

## Workflow-specific notes

| Workflow | Variety emphasis |
|----------|-------------------|
| [p-image-try-on](../../tools/image/p-image-try-on/SKILL.md) | Editorial plates + complex garment refs; preservation checklist; diversity across playground set |
| [p-video-replace](../../tools/video/p-video-replace/SKILL.md) | Scene 1 **persona ladder** + per-scene distinct `still_edit` backgrounds; optional **light bed** after concat |
| [p-video-animate](../../tools/video/p-video-animate/SKILL.md) | 3–4 **style tags** per animate slider row |
| [avatar-multi-scene](../workflows/core/avatar-multi-scene/SKILL.md) | Every avatar row: new `setting_tag` + `camera_tag` via `p-image-edit` |
| [pruna-generative-pipeline](../workflows/router/pruna-generative-pipeline/SKILL.md) | Intake must capture variety plan before recipe execution |

## Variety checklist (before first API call)

- [ ] **Cast:** gender, age, and ethnicity spread across scenes — not one default face
- [ ] **Settings:** no adjacent duplicate `setting_tag`; at least 5 distinct environments in an 8-scene reel
- [ ] **Palettes:** no three adjacent scenes share the same dominant accent; name gel/light pairs in prompts
- [ ] **Textures:** wardrobe rows name fabric/material (fur, holo, satin, clay)
- [ ] **Camera:** at least 3 different `camera_tag` values; no duplicate motion grammar on every `video_prompt`
- [ ] **Motion props:** `video_prompt` glance targets match objects in `still_edit`
- [ ] **UGC/install rows:** source + refs use **different** locations and cameras — not neutral grey wall on all stills
- [ ] **Lighting:** at least 3 different `lighting_tag` values; stylized scenes name their light mood
- [ ] **Styles:** at least 4 `visual_style_tag` values in a launch reel (mix **photoreal**, **sketch/2D**, **stop-motion 3D**, **CG 3D**)
- [ ] **Render mediums:** persona ladder includes 5+ distinct mediums when showcasing replace range
- [ ] **Persona ladder:** hook or animate row includes 6+ visually distinct refs if showcasing range
- [ ] **Local consistency:** refs within one scene row share one style; across rows, styles diverge
- [ ] **Lip sync:** VO rows still use speaking sources + preserve-lips `instruction_prompt` language
- [ ] **Delivery:** if the reel ships with avatar VO, confirm whether to add an **light instrumental bed** under dialogue ([stable-audio-2.5](../tools/audio/stable-audio-2.5/SKILL.md), ~0.12 volume, no vocals)

## Related

- [generation-quality-checklists.md](./generation-quality-checklists.md)
- [p-video-replace-quality-checklist.md](./p-video-replace-quality-checklist.md)
- [p-video-animate-quality-checklist.md](./p-video-animate-quality-checklist.md)
