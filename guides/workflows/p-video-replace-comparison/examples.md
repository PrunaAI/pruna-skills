# P-Video-Replace comparison examples

## Mixed hook / CTA (`replace_target: mixed`, `multi_job`)

1. Source: hero spokesperson at desk + mug (`p-video-avatar`, VO).
2. **`p-image`** × 3 — new presenter, green blazer **on woman**, desk-scale packshot.
3. Three **`p-video-replace`** jobs; each **`instruction_prompt`** names one slot (face / blazer only / mug only) and preserves lips on VO beats.

## UGC install — face, wardrobe, closed laptop (`replace_target: mixed`, `multi_job`)

1. Source: advocate in **creative loft** (brick, window bokeh), low three-quarter handheld, closed laptop at chest (`p-video-avatar`) — not grey wall, not open laptop.
2. References — **each ref its own world + camera:**
   - Recast A: rooftop dusk, low angle, cobalt hoodie
   - Recast B: cafe corner, three-quarter, orange hoodie
   - Wardrobe: LED studio, slight high angle, lime crewneck
3. Per-ref instructions preserve closed laptop + lips. Plan: [`skills-library-announcement/announcement_plan.json`](../../../output/skills-library-announcement/announcement_plan.json) scene 2.

## UGC — face, tee, in-hand SKU (legacy tube pattern)

1. Source: creator in **named location** (loft, bedroom ring light, cafe — not flat grey on every ref), white tube at chest (`p-video-avatar`) — not kitchen + pointing.
2. References: recast creator in **different setting per ref**, sage tee **on same face**, rose gold in-hand prop.
3. Per-ref instructions: *clothing only* / *tube in hand only* + preserve lips.

## Wardrobe talking head (`replace_target: clothing`, `multi_job`)

1. Source: stylist bust in sweater + open denim jacket (`p-video-avatar`, short VO).
2. References: three looks — each ref shows **same face wearing** target outfit.
3. Three replace jobs → variant slider (avoid I2V full-body walk for launch reels).

## In-game dialogue weapon swaps (`replace_target: object`, `multi_job`)

1. Source: **in-game dialogue camera** via `p-video-avatar` — knight speaks to camera, plain white sword at hip (not streamer desk).
2. Three matching **fantasy sword** asset refs (hero gold / frost / runic greatsword); each instruction: *replace only weapon in hand*, preserve lips.
3. Distinct from scene 7 (live-action reaction → full game character). Multi-sample slider.

## Solo cafe mixed (`replace_target: mixed`, `multi_job`)

1. Source: **one** woman at cafe, yellow bag on **empty chair**, calm product explainer VO (`p-video-avatar`).
2. References: new face, olive bomber **on woman**, burgundy bag packshot at chair scale.
3. Three `multi_job` swaps — not two-shot `single_call` I2V.

## In-hand SKU + clothing (`replace_target: object` + clothing, `multi_job`) — golden template

1. Source: gym creator speaks to camera, white tub at chest, subtle handheld (`p-video-avatar`) — see scene 6 in launch plan.
2. Three SKU refs + one shirt ref; instructions preserve **lips and audio** on product beats.
3. Reuse this row structure when other scenes fail.

## Full launch reel

[`example-prompt.md`](../../../examples/workflows/p-video-replace-comparison/example-prompt.md) · [`announcement_plan.json`](../../../output/p-video-replace-announcement/announcement_plan.json) · [`run_from_plan.py`](./scripts/run_from_plan.py)

**Delivery:** after concat, optional **chill background music** via plan `background_music` or `--background-music` — [stable-audio-2.5](../../../tools/audio/stable-audio-2.5/SKILL.md) instrumental bed mixed under VO at ~0.12 volume.

## Persona ladder hook (scene 1 pattern)

One VO source → **multi_job** refs spanning distinct **`visual_style_tag`** values — each ref prompt includes its own background + lighting + **subject family**:

| Ref | Style | Medium | Subject | Setting + light |
|-----|-------|--------|---------|-----------------|
| UGC creator | photoreal_ugc | photoreal | human | bedroom ring light |
| Pencil portrait | pencil_sketch | pencil_sketch | human | art-studio north light |
| Hand-drawn frame | hand_drawn_2d | hand_drawn_2d | stylized | watercolor wash, golden hour |
| Anime hero | anime_cinematic | cel_anime_2d | stylized | neon rain alley |
| Clay character | clay_stop_motion | stop_motion_3d | stylized | miniature living room, warm lamp |
| Cyberpunk netrunner | cyberpunk_cinematic | photoreal_stylized | stylized | rain alley, magenta-cyan rim |
| Epic film warrior | epic_film | photoreal_stylized | fictional | canyon rim light |
| Library otter host | storybook_film | cg_3d_film | **anthropomorphic** | cozy desk lamp, medium CU |
| Fairy-tale royal | disney_3d | cg_3d_film | **fictional 3D** | enchanted garden, golden hour |

**Other scenes:** use **wardrobe-only** (bolero, blazer) and **accessory-only** (scarf, choker, earrings) rows — same talent, mapped slot swap, lips unchanged.

See [visual-variety-bible.md](../../../references/visual-variety-bible.md) and [SKILL.md](./SKILL.md) **Persona & subject diversity**.
