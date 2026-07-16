# Dynamic persona & scenario showcase

How to produce **diverse, art-directed personas and scenarios** across **`p-image`** → optional **`p-image-try-on`** / **`p-image-edit`** → **`p-video-avatar`**. Covers **photographic styles**, **anime and stylized mediums**, **camera angles**, **lighting**, **settings**, and **cast** — not generic “AI stock portrait” demos.

**Variety ladders (full tables):** [visual-variety-bible.md](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/visual-variety-bible/SKILL.md) · **Try-on garment specifics:** [p-image-try-on-quality-checklist.md](https://github.com/PrunaAI/pruna-skills/tree/main/image/p-image-try-on-quality-checklist.md) · **Copy-paste examples:** [realistic-persona-example-prompt.md](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/realistic-persona-example-prompt/SKILL.md)

## Contents

- [Why this exists](#why-this-exists)
- [Pipeline overview](#pipeline-overview)
- [Shared anti-patterns](#shared-anti-patterns)
- [Dynamic scenario generation](#dynamic-scenario-generation)
- [p-image — persona plates](#p-image--persona--scenario-plates)
- [Identity lock](#identity-lock)
- [p-video-avatar — dynamic realistic personas](#p-video-avatar--dynamic-realistic-personas)
- [Diversity for public showcases](#diversity-for-public-showcases)

## Why this exists

Current public examples often read as **AI sloppy** or **too simplistic**: same neutral wall, same face, same medium close-up, one photoreal look, brochure VO. The stack can deliver **editorial fashion**, **complex wardrobe**, **cel-anime hosts**, **documentary street portraits**, and **talking heads with distinct motion** when scenarios are planned as a matrix — not one template repeated.

## Pipeline overview

**Before any step:** [generation-diversity.md](https://github.com/PrunaAI/pruna-skills/tree/main/policies/generation-diversity.md) (ritual seed + axis rotation) · [random seed ritual](https://github.com/PrunaAI/pruna-skills/tree/main/policies/random-seed-ritual.md)

```text
p-image (hero plate)     → slop gate → identity anchor (plate URL + cast descriptor)
    ↓ optional
p-image-edit / try-on    → slop gate → dressed or reposed still
    ↓ optional
p-image-upscale          → delivery-scale still (print / PDP only when needed)
    ↓
p-video-avatar           → per-scene unique video_prompt + natural voice_script
```

| Deliverable | Minimum path |
|-------------|--------------|
| Photoreal still only | **`p-image`** (+ **`p-image-edit`** variants) |
| Dressed model still | **`p-image`** → **`p-image-try-on`** |
| Talking-head clip | **`p-image`** hero → slop gate → **`p-video-avatar`** |
| Fashion UGC ad | **`p-image`** → try-on → slop gate → **`p-video-avatar`** |
| Multi-scene host | Hero → **`p-image-edit`** per scene (parallel) → batch **`p-video-avatar`** |

## Shared anti-patterns

| Sloppy output | Fix |
|---------------|-----|
| Generic “beautiful person, soft light, white background” | Named **setting** + **lighting_tag** + **cast_descriptor** |
| Mushy skin / plastic CGI look | `photoreal documentary portrait, natural skin pores, not CGI, not illustration` |
| Same face in every public example | **Cast ledger** — rotate gender, age, ethnicity |
| Every avatar clip: medium CU + gentle dolly | Unique **`video_prompt`** per scene — angle, gesture, glance, handheld |
| Brochure **`voice_script`** | Contractions, fillers, speakable lines — see avatar templates |
| Marketing copy in **`voice_prompt`** | Performance direction only (*“relaxed founder tone, real pauses”*) |
| One **`video_prompt`** copied across scenes | Scene table with distinct camera + motion grammar |
| Skipping slop gate before avatar | Reject waxy stills — artifacts amplify in lip-sync |
| **One visual style everywhere** | Assign **`visual_style_tag`** + **`render_medium_tag`** per row — photoreal · anime · clay · sketch |
| **Same camera angle on every still** | Rotate **`camera_tag`** — low, high, profile, over-shoulder, extreme CU |
| **Anime without mouth visibility** | Lip-sync rows still need **mouth clearly visible** in stylized frames |
| **Trigger words in still prompts** | Avoid `charcoal`, `graphite`, `crosshatching` in **`p-image`** — see [wording scope](#prompt-wording-stylized-vs-photoreal) |

## Dynamic scenario generation

Plan each generation as a **scenario row** — not a loose prompt. Fill every column before **`POST /v1/predictions`**:

| Axis | Plan field | Vary across public examples |
|------|------------|----------------------------|
| **Medium / style** | `visual_style_tag`, `render_medium_tag` | photoreal · cel anime · clay · CG 3D · sketch |
| **Photographic look** | style sub-tag (see below) | documentary · editorial · street · cinematic · UGC |
| **Cast** | `cast_descriptor`, `persona_gender` | age, ethnicity, gender, archetype, species |
| **Setting** | `setting_tag` | no duplicate adjacent environments |
| **Camera** | `camera_tag` | shot size + angle — see [camera ladder](#camera-angle--shot-size-ladder) |
| **Lighting** | `lighting_tag` | golden hour · neon · overcast · practical clay |
| **Palette** | `palette_tag` | warm punch · cool contrast · neon editorial |
| **Motion** (avatar) | unique `video_prompt` | never copy one string across scenes |

**Rule:** lock consistency **within one row** (style bible for that beat). **Diverge across rows** — a showcase set should feel like a deliberate gallery, not eight variants of the same shoot.

### Photographic style families (`render_medium_tag: photoreal`)

Use when the brief is live-action or camera-native. Pick **one** sub-style per row:

| Sub-style | Prompt cues | Best for |
|-----------|-------------|----------|
| **Documentary** | available light, handheld honesty, street context, natural skin pores | explainers, founder VO |
| **Editorial fashion** | textured walls, named wardrobe piece, art-directed pose, shallow DOF | try-on, lookbook |
| **Commercial / PDP** | clean product readability, even key, unprinted props | catalog (still vary cast/angle) |
| **Street / UGC** | smartphone-adjacent, mirror selfie, night city, prop in frame | social hooks |
| **Cinematic film** | golden hour rim, anamorphic bokeh, motivated single source | hero portraits |
| **High-fashion lookbook** | high angle or extreme angle, seamless or bold set, statement silhouette | complex garment demos |
| **Night / neon editorial** | gel edge light, wet reflections, magenta-cyan ambient | variety ladder slots |

**Realism lock (photoreal only):** `photoreal photograph, natural skin texture, not CGI, not illustration, single subject one frame`.

### Anime & stylized 2D (`render_medium_tag: cel_anime_2d`, `hand_drawn_2d`)

Anime is not one look — tag the **anime sub-style** in `visual_style_tag`:

| Anime sub-style | Prompt direction | Avatar notes |
|-----------------|------------------|--------------|
| **Premium cinematic cel** | film-grade compositing, rich lighting, detailed eyes/hair | mouth visible mid-speech; avoid chibi for VO |
| **Modern action / shonen** | dynamic pose energy, bold linework, saturated accents | low heroic angle; motion `video_prompt` matches energy |
| **Slice-of-life / soft anime** | warm domestic setting, gentle palette, softer shading | cafe, rooftop, classroom `setting_tag` |
| **Cyberpunk anime** | neon alley, chrome accents, violet/cyan edge light | pair with `lighting_tag: neon_night` |
| **Retro 90s cel** | flatter shading, grain, classic TV framing | distinct from premium cinematic in same reel |
| **Hand-drawn 2D frame** | ink outlines, watercolor wash background — **single frame** | say `hand-painted cel illustration`, not `charcoal sketch` |

Example — cinematic cel host:

```text
Premium anime cinematic young woman hero, cel-shaded film look, violet hair, iridescent jacket,
cherry-blossom rooftop at dusk with neon color bokeh, low heroic angle from the side,
mouth visible mid-speech, bright clear evening atmosphere, single character one frame.
```

### 3D stylized (`render_medium_tag: stop_motion_3d`, `cg_3d_film`)

| Sub-style | Prompt direction |
|-----------|------------------|
| **Claymation / stop-motion** | visible clay texture, miniature set, practical desk-lamp lighting |
| **Disney / Pixar CG** | rounded forms, storybook warmth, enchanted garden or castle |
| **Game cinematic 3D** | armor or adventure costume, volumetric haze, epic scale |

**Avatar path:** mouth must read clearly in the sculpted/design face — reject plates where lips disappear into stylization.

### Stylized sketch & illustration (use carefully)

Sketch personas work for **replace/animate ladders** and variety slots. In **`p-image`** still prompts, **avoid** trigger words that cause contact sheets: `charcoal`, `pencil`, `crosshatching`, `graphite portrait`, `greyscale cinematic`.

**Safer wording:** `stylized muted-tone presenter`, `soft grey tones`, `hand-painted cel illustration`, `fluid ink outlines`.

See [visual-variety-bible.md](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/visual-variety-bible/SKILL.md#prompt-patterns) for blocked still trigger words.

### Camera angle & shot size ladder

Never default every plate to medium close-up facing camera. Rotate **`camera_tag`**:

| Tag | Prompt wording | Use when |
|-----|----------------|----------|
| `extreme_cu` | extreme close-up eyes and mouth | hook tension, lip-sync proof |
| `medium_cu` | medium close-up chest-up | default VO if mouth visible |
| `medium_wide` | medium wide waist-up | wardrobe, props, try-on stacks |
| `full_body` | full body head to shoes | suits, streetwear, footwear try-on |
| `low_angle_hero` | low angle from below | power, fashion, anime hero |
| `high_angle_editorial` | high angle from above | lookbook, vulnerability, fashion demo |
| `side_angle` | slight angle from the side | editorial, anime, avoid straight-on repetition |
| `over_shoulder` | over-shoulder turning toward lens | explainer, desk beats |
| `profile_turn` | profile turning in toward camera | stylized refs when motion allows |

**Still prompts:** prefer `slight angle from the side`, `low angle`, `high angle` — record exact tag in plan JSON. **Avoid** repeating `facing camera` on every row.

### Lighting & setting (quick rotate)

Pull full ladders from [visual-variety-bible.md](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/visual-variety-bible/SKILL.md#lighting-ladder). Minimum for a **5-example playground set**: 3 different `lighting_tag` + 5 different `setting_tag` values.

| Example pairing | `setting_tag` | `lighting_tag` |
|-----------------|---------------|----------------|
| Loft host | `loft_brick` | `soft_overcast` |
| Rooftop anime | `rooftop_dusk` | `golden_hour` |
| Night street | `mirror_selfie_street` | `neon_night` |
| Asphalt fashion | `open_asphalt` | `overcast_open_sky` |
| Clay set | `clay_living_room` | `practical_clay` |

### Scenario matrix — 8-slot showcase (mixed mediums)

Use when building a **public example gallery** (playground or launch page):

| Slot | `render_medium_tag` | `visual_style_tag` | `camera_tag` | `setting_tag` | `aspect_ratio` |
|------|---------------------|--------------------|--------------|---------------|----------------|
| 1 | photoreal | documentary | low_angle_mc | loft_brick | `2:3` |
| 2 | photoreal | editorial_fashion | high_angle_full | plaster_floor | `16:9` |
| 3 | photoreal | street_ugc | side_angle | mirror_selfie_night | `9:16` |
| 4 | cel_anime_2d | anime_cinematic | low_angle_hero | rooftop_dusk | `4:3` |
| 5 | cel_anime_2d | cyberpunk_anime | side_angle | neon_alley | `3:4` |
| 6 | stop_motion_3d | clay_stop_motion | medium_cu | clay_living_room | `1:1` |
| 7 | cg_3d_film | fairy_tale_3d | medium_cu | enchanted_garden | `3:2` |
| 8 | photoreal | cinematic_film | extreme_cu | golden_hour_field | `2:3` |

Each slot gets a **distinct** `cast_descriptor` and **distinct** `aspect_ratio`. For avatar examples, a **unique** `video_prompt` per slot.

### Prompt wording: stylized vs photoreal

| Intent | Do | Don't (in `p-image` still prompts) |
|--------|-----|-------------------------------------|
| Photoreal host | `documentary portrait`, `natural skin pores`, `not CGI` | `8k`, `hyperreal`, `ultra detailed` spam |
| Cel anime | `premium anime cinematic`, `cel-shaded film look` | `manga panel`, `contact sheet`, `multiple views` |
| Sketch-like | `stylized muted-tone presenter`, `soft grey tones` | `charcoal`, `pencil sketch`, `crosshatching` |
| Single frame | `single subject one frame`, `one camera angle` | `collage`, `triptych`, `character sheet layout` |

### Stylized → avatar continuity

Stylized hosts can lip-sync when:

1. **Mouth is large and visible** in the still (same gate as photoreal)
2. **`video_prompt`** matches the style energy (anime: slightly more expressive head motion; clay: smaller subtle moves)
3. **`voice_prompt`** matches archetype (*“warm anime protagonist delivery”* vs *“documentary narrator calm”*)
4. **Hero plate URL** locked per character across clips in the same style

For **cross-style multi-scene reels** (photoreal → anime → clay): treat each style as a **new row** with its own hero still — do not expect one photoreal hero to **`p-image-edit`** into anime; generate a fresh **`p-image`** per `visual_style_tag`.

## `p-image` — persona & scenario plates

### When the plate feeds avatar or try-on

Add **avatar-ready** or **try-on-ready** constraints to every hero prompt:

| Downstream | Plate requirements |
|------------|---------------------|
| **`p-video-avatar`** | Face large in frame; **mouth clearly visible**; speaking-friendly pose; hands low or away from mouth |
| **`p-image-try-on`** | Body region for garments visible (full-body for suits; feet for shoes; head for hats) |
| **Both** | Editorial photoreal + coverage for wardrobe + lip-sync |

### Dynamic prompt stack (build in order)

Applies to **every** `visual_style_tag` — not photoreal only. Full stack: [visual-variety-bible.md](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/visual-variety-bible/SKILL.md#dynamic-prompt-stack-eye-catching).

1. **Style / medium** — `visual_style_tag` + `render_medium_tag` (photoreal · cel anime · clay · CG 3D)
2. **Cast** — age, ethnicity, gender presentation, hair, archetype (or species for anthropomorphic)
3. **World** — 2–3 concrete environment cues; unique `setting_tag`
4. **Lighting** — named mood; `lighting_tag`
5. **Framing** — shot size + angle; `camera_tag` — [camera ladder](#camera-angle--shot-size-ladder)
6. **Wardrobe / texture** — statement fabric or material words when relevant
7. **Realism or stylization lock** — photoreal lock **or** medium-specific lock (cel, clay, etc.)
8. **Lip-sync hook** (avatar path) — `mouth clearly visible ready to speak`

Run [p-image-quality-checklist.md](https://github.com/PrunaAI/pruna-skills/tree/main/image/p-image-quality-checklist.md) — persona rows below.

### Hero prompt — talking head (avatar)

```text
Photorealistic documentary portrait photograph of a real person, not CGI, not 3D render.
Woman early 30s South Asian, short curly hair, olive linen blazer, warm direct expression.
Creative loft with exposed brick and teal window bokeh, slight low angle chest-up,
soft overcast daylight through windows, mouth clearly visible ready to speak,
natural skin pores, 9:16 vertical, single subject one frame, plain unmarked walls.
```

### Hero prompt — editorial full-body (try-on / fashion)

```text
Photoreal street fashion portrait, woman early 20s East Asian, high ponytail,
full body on dark asphalt, overcast open-sky light, neutral base outfit,
natural skin texture, not CGI, 9:16 vertical, single subject one frame.
```

More plate examples (including try-on garment tiers): [p-image-try-on SKILL.md](../../p-image-try-on/SKILL.md#production-quality-not-basic-demos).

### Per-scene variety without new identity

After hero approval, branch with **`p-image-edit`** from the **same anchor URL**:

- Change **only** background, camera angle, emotion, or wardrobe delta
- Never re-roll identity with a fresh unrelated **`p-image`** unless user requests recast

Templates: [prompt-templates.md](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/avatar-multi-scene/prompt-templates.md).

### Identity lock

**[Random seed ritual](https://github.com/PrunaAI/pruna-skills/tree/main/policies/random-seed-ritual.md) (SSoT)** first — log `ritual_seed` for prompt planning. Character continuity = **approved hero plate URL** + cast descriptor across hero regen and **`p-video-avatar`** clips.

## `p-video-avatar` — dynamic realistic personas

A realistic avatar is **not** a static face on a loop. Each clip needs **human delivery** + **distinct motion** + **continuity** from a slop-gated still.

### Still gate (before every clip)

Run [p-video-avatar-quality-checklist.md](https://github.com/PrunaAI/pruna-skills/tree/main/video/p-video-avatar-quality-checklist.md) input section. Reject plates with obscured mouth, extreme profile-only crop, or synthetic mush skin.

### Voice — sound human

| Field | Rule |
|-------|------|
| **`voice_script`** | Speakable dialogue — contractions, short sentences, light fillers. Read aloud before API. |
| **`voice_prompt`** | How they *sound* — pacing, warmth, archetype. **Never** paste product copy or script lines. |
| **`voice` / `voice_language`** | One preset per character across all their clips |

Good **`voice_script`:** *"Hey — so we tried this on real catalog shots, and honestly the hard part was picking which outfit looked best."*

Bad **`voice_script`:** *"Our revolutionary AI-powered virtual try-on solution delivers unparalleled garment fidelity."*

### Motion — dynamic per scene

**Default `video_prompt` (`The person is talking.`) is for quick tests only.** Production clips need unique grammar per row:

| Scene role | Example **`video_prompt`** |
|------------|---------------------------|
| Hook | `Extreme close-up speaking to lens, subtle push-in, curious eyebrow raise` |
| Proof / demo | `Medium chest-up, slight arc left, glance down to prop then back to lens` |
| UGC install | `Low angle handheld sway, natural head tilt, conversational energy` |
| CTA | `Medium close-up, slow dolly in, warm confident settle, direct eye contact` |

Pair with **`p-image-edit`** stills that match — if **`video_prompt`** mentions a notebook glance, the still must show a notebook.

**Anti-pattern:** eight scenes with identical `medium close-up, gentle dolly push-in`.

See camera/motion ladder: [visual-variety-bible.md](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/visual-variety-bible/SKILL.md#camera-angle--movement-ladder).

### Multi-scene dynamic table (plan before API)

| # | `setting_tag` | `camera_tag` | Still delta (`p-image-edit`) | `video_prompt` (unique) |
|---|---------------|--------------|------------------------------|-------------------------|
| 1 | loft_brick | low_angle_mc | hero | push-in hook |
| 2 | rooftop_dusk | side_angle | background only | handheld sway |
| 3 | cafe_corner | over_shoulder | desk + mug | glance to mug |
| 4 | led_studio | slight_high | wardrobe swap | arc right |

Workflow skills: [avatar-single-scene](../SKILL.md) · [avatar-multi-scene](../../avatar-multi-scene/SKILL.md).

### Fashion / try-on → talking head

1. Photoreal **`p-image`** plate → slop gate
2. **`p-image-try-on`** (normal mode for complex garments) → preservation checklist
3. Optional upscale if delivery resolution demands it
4. **`p-video-avatar`** — reuse approved try-on plate URL; script references the outfit naturally

Example **`voice_script`:** *"Okay — this is the patchwork jacket on me, not a mannequin. The print actually stayed sharp."*

### Negative prompt (text artifacts)

When stills risk signage or label bleed, use plan defaults — see [p-video-avatar SKILL.md](../../p-video-avatar/SKILL.md#negative-prompt-suppress-on-screen-text). Primary fix remains **clean still prompts**; API negative prompt is a safety net.

## Diversity for public showcases

Plan a **cast ledger** and **scenario matrix** before the first **`p-image`** call — see [scenario matrix](#scenario-matrix--8-slot-showcase-mixed-mediums):

| Slot | Vary |
|------|------|
| Person 1–N | Gender, age band, ethnicity, archetype, species |
| **Medium** | photoreal · cel anime · hand-drawn 2D · clay · CG 3D |
| **Photo sub-style** | documentary · editorial · street · cinematic |
| **Anime sub-style** | cinematic cel · cyberpunk · slice-of-life · retro cel |
| Settings | No duplicate adjacent `setting_tag` |
| Camera | At least 3 distinct `camera_tag` values per reel |
| Lighting | At least 3 distinct `lighting_tag` values per set |
| Motion | No duplicate `video_prompt` grammar across avatar clips |
| Garment tier (try-on) | Packshot · collage suit · streetwear stack · accessories |

Pin diverse try-on examples on [p-image-try-on](https://replicate.com/prunaai/p-image-try-on) per the playground table below.

**Playground (Replicate):** diversify **all three** model pages — not one look each:

| Model | Showcase spread |
|-------|-----------------|
| [p-image](https://replicate.com/prunaai/p-image) | Mixed mediums + angles + settings per [matrix](#scenario-matrix--8-slot-showcase-mixed-mediums) |
| [p-image-try-on](https://replicate.com/prunaai/p-image-try-on) | Five editorial/complex-garment refs + diverse cast |
| [p-video-avatar](https://replicate.com/prunaai/p-video-avatar) | Photoreal + anime + clay hosts; unique `video_prompt` each |

Coordinate with @ShinyTaskForce.

## Quick reference

| Model | Skill | Checklist |
|-------|-------|-----------|
| `p-image` | [p-image SKILL.md](../../p-image/SKILL.md) | [p-image-quality-checklist.md](https://github.com/PrunaAI/pruna-skills/tree/main/image/p-image-quality-checklist.md) |
| `p-image-try-on` | [p-image-try-on SKILL.md](../../p-image-try-on/SKILL.md) | [p-image-try-on-quality-checklist.md](https://github.com/PrunaAI/pruna-skills/tree/main/image/p-image-try-on-quality-checklist.md) |
| `p-video-avatar` | [p-video-avatar SKILL.md](../../p-video-avatar/SKILL.md) | [p-video-avatar-quality-checklist.md](https://github.com/PrunaAI/pruna-skills/tree/main/video/p-video-avatar-quality-checklist.md) |

Example prompts: [realistic-persona-example-prompt.md](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/realistic-persona-example-prompt/SKILL.md)
