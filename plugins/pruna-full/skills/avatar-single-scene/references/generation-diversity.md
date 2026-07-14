# Generation diversity (all models)

One checklist so **every** Pruna output — **`p-image`**, **`p-video`**, try-on, avatar, replace, animate — is as **diverse** as the brief allows. Details live in linked docs; this page is the agent shortcut.

Use the **full** checklist here for every generation.

## Contents

- [Three steps (every job)](#three-steps-every-job)
- [Explicit prompt structure](#explicit-prompt-structure-required)
- [Text & typography by model](#text--typography-by-model)
- [SSoT axis derivation](#ssot-axis-derivation-sum-mod)
- [Scenario axes](#scenario-axes-rotate-across-outputs)
- [Render categories](#render-categories)
- [Crowded scenes](#crowded-scenes-p-image)
- [Body type spread](#body-type-spread)
- [Location-matched crowds](#location-matched-crowds)
- [Group classes](#group-classes--courses)
- [Framing & camera](#framing--camera)
- [Scene spice](#scene-spice-when-it-fits)
- [Photoreal anti-slop](#photoreal-anti-slop-neon--stylized-briefs)
- [Aspect ratio](#aspect-ratio-multi-example-sets)
- [By model](#by-model-minimum-diversity)
- [When not to maximize diversity](#when-not-to-maximize-diversity)
- [Anti-patterns](#anti-patterns)

## Three steps (every job)

1. **[Random seed ritual](./random-seed-ritual.md) (SSoT)** — **always first**, before the prompt. Generate a fresh random string, **state it in the turn**, derive axes via [sum-mod](#ssot-axis-derivation-sum-mod). **Do not** pass the ritual string to API `seed`. **One new ritual string per independent generation**; reuse only on same-brief slop retry.
2. **Write an [explicit prompt](#explicit-prompt-structure-required)** — name specific people, animals, objects, actions, setting, and camera/light. Add text/typography only when the brief needs it — see [text rules by model](#text--typography-by-model).
3. **Diversify the scenario row** — change at least **two axes** from the previous output in the same session (cast, setting, camera, **`render_category_tag`**, **aspect_ratio**, creatures, props, … — unless user asked for continuity).
4. **Log** — `ritual_seed`, axes chosen, prediction id (manifest or turn text).

## Explicit prompt structure (required)

**Vague prompts produce generic AI slop.** After the ritual and axis picks, every still prompt must be **specific and dynamic** — concrete nouns, frozen actions, named places. Prefer playground/creative briefs over marketing abstractions.

**Name at least four of these per prompt (log tags in manifest):**

| Clause | Log as | Agent must specify |
|--------|--------|-------------------|
| **People** | `cast_descriptor` | Named role + age band + expression (`fearless grandmother in floral apron`, not `woman`) |
| **Animals / creatures** | `creature_tag` | Species + attitude (`otter DJ`, `luna moth knight`, `VIP anglerfish`) |
| **Objects** | `prop_tag` | Concrete props (`vinyl record`, `chrome rocket sled`, `velvet rope`, `tiny boombox`) |
| **Action** | `action_tag` | Frozen mid-motion verb (`scratching vinyl`, `lassoing runaway taco truck`, `cape mid-swing`) |
| **Duration** | `duration_tag` | When timing matters (`1970s`, `8PM`, `45-minute spin class`, `Saturday-morning cartoon`) |
| **Setting** | `setting_tag` | Named place + era + materials (`packed 1970s roller rink`, `abyss-depth jellyfish nightclub`, `Monument Valley dust storm`) |
| **Text / typography** | `text_spec` | Only when brief needs readable type — exact strings + surface (see [by model](#text--typography-by-model)) |
| **Camera + light** | `camera_tag`, `lighting_tag` | `fish-eye lens`, `tilt-shift macro`, `teal-magenta cinematic`, `golden hour sparkle` |
| **Style** | `render_category_tag` | Medium (`cel-shaded anime`, `baroque oil painting`, `ink-wash storybook`, `photoreal documentary`) |

**Template:**

```text
{people and/or creatures} {action} with/at {specific objects} in {named setting},
{style or era cues}, {camera_tag}, {lighting_tag}
```

**Good examples (dynamic / specific):**

```text
Disco ball reflections on an otter DJ scratching vinyl at a packed 1970s roller rink,
fish-eye lens, glitter confetti mid-air, funky energy
```

```text
Bioluminescent jellyfish nightclub at abyss depth, VIP anglerfish in sunglasses at velvet rope,
teal-magenta cinematic lighting
```

```text
Corgi cowboy lassoing a runaway taco truck through Monument Valley dust storm,
pulp western poster energy, dynamic diagonal composition
```

**Anti-pattern:** `cool cyberpunk portrait, neon vibes` — no subject, no action, no place. **Right:** name who, what they're doing, where, with which props.

## Text & typography by model

**Never use negation to suppress text** — `no text`, `without signs`, `no typography` often **invoke** the thing you are trying to avoid. Describe surfaces positively when you want blank walls (`plain unmarked walls`, `matte unprinted props`).

| Model | Prompt upsampling | Typography in prompt |
|-------|-------------------|----------------------|
| **`p-image`** | **No** effective prompt upsampling | **Avoid** dense readable-type requests unless user explicitly wants `text_rendering`. Short prompts; skip `readable`, `legible`, `headline`, multi-sign lists — they drift to gibberish. Collage triggers still apply: [interactive-explainer-prompts.md](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/interactive-explainer-prompts.md) (`flat lay`, `grid`, `collage`, …). |
| **`p-image-ideogram`** | **Yes** — `mode` runs upsamplers (ideogram-sft, Gemini Flash, etc.) | **OK** to name exact strings and placements when the brief needs type (`rooftop neon PRUNA`, `chalkboard HAPPY HOUR 5-7`). List every string + surface for `text_rendering` rows. |

**`p-image` text hygiene:** prefer scenes without copy. If a screen appears: `monitor soft colorful blur glow only` — not legible UI unless the user asked for readable text and you route to **`p-image-ideogram`**.

**`p-image-ideogram` text briefs:** stack multiple strings across the frame (billboard, awning, kiosk, phone notification) with positions; end with `crisp legible typography` when quality matters. Benchmark: repo `output/p-image-ideogram-mode-comparison/` text_rendering rows.

**Collage triggers (all T2I models):** still avoid `flat lay`, `packshot`, `grid`, `collage`, `montage`, `contact sheet`, `split`, `before and after` — use `single frame`, `one camera angle` instead. Full table: [interactive-explainer-prompts.md](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/interactive-explainer-prompts.md).

## SSoT axis derivation (sum-mod)

After stating `ritual_seed` (random string), derive prompt choices — sum Unicode/ASCII char codes, mod list length:

```text
RATIOS = ["1:1", "16:9", "9:16", "4:3", "3:4", "3:2", "2:3"]
aspect_ratio  ← RATIOS[ sum(codes(ritual_seed)) % 7 ]
camera_tag    ← camera_tags[ sum(codes(ritual_seed[0:4])) % len(camera_tags) ]
render_tag    ← render_tags[ sum(codes(ritual_seed[4:8])) % len(render_tags) ]
```

`camera_tags` and `render_tags` — see [framing & camera](#framing--camera) and [render categories](#render-categories). State derived picks in the turn (*"Aspect ratio: 16:9, camera: over-shoulder"*).

**User `api_seed`:** when the user supplies an integer for reproducibility, pass it as `input.seed` — separate from the ritual string.

## Scenario axes (rotate across outputs)

| Axis | Vary with | Applies to |
|------|-----------|------------|
| **Cast** | age, ethnicity, gender, archetype, **hairstyle**, **body type** (rotate — see [below](#body-type-spread)), disability aids (wheelchair, cane), visible age band twice in prompt | all person/content gens |
| **Medium** | `render_category_tag` — rotate across [render categories](#render-categories) | `p-image`, avatar stills |
| **Setting** | unique `setting_tag` — specific room/street/venue/era, not repeat adjacent rows | stills + video plates |
| **Camera** | `camera_tag` — rotate across [framing ladder](#framing--camera); never default MC facing lens | stills, `video_prompt` |
| **Lighting** | `lighting_tag` — golden hour · neon · overcast · practical | stills, video mood |
| **Motion** | unique `video_prompt` per clip | `p-video`, `p-video-avatar`, animate |
| **Voice** | natural `voice_script`; one `voice` preset per character | avatar, TTS-led video |
| **Seed** | new ritual string per **independent** job; reuse only on same-brief slop retry | all generation skills |
| **Aspect ratio** | different `aspect_ratio` per independent still in a batch — see [below](#aspect-ratio-multi-example-sets) | `p-image`, `p-image-edit` |
| **Crowd density** | layered background population + activity cues — see [below](#crowded-scenes-p-image) | `p-image` plates with busy worlds |

Full style/camera/lighting ladders: [visual-variety-bible.md](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/core/visual-variety-bible/SKILL.md). Persona + try-on bar: [realistic-persona-showcase.md](./realistic-persona-showcase.md).

## Render categories

Rotate **`render_category_tag`** (and log it) so diversity batches cover more than photoreal portraits or anime. Category families below mirror arena leaderboards — pick a **different tag per independent output**.

**Random seed ritual still applies** to every generation in [step 1](#three-steps-every-job); categories describe *what* to vary, not *when* to pick `seed`.

### Text-to-image — `p-image`

Sources: [Arena text-to-image](https://arena.ai/leaderboard/text-to-image) · [AA text-to-image](https://artificialanalysis.ai/image/leaderboard/text-to-image)

**Unified `render_category_tag`** (Arena bucket = tag — pick one per still):

`product_branding_commercial` · `3d_imaging_modeling` · `cartoon_anime_fantasy` · `photoreal_cinematic` · `art` · `portraits` · `nature_environment` · `animals_creature` · `text_rendering`

| Tag | Typical prompt lane |
|-----|---------------------|
| `product_branding_commercial` | single product on seamless studio, person + product in named setting, showroom (not `flat lay` / `packshot` words) |
| `3d_imaging_modeling` | CG film still, clay/stop-motion, rounded 3D forms |
| `cartoon_anime_fantasy` | cel anime, fantasy character, crowded stylized world |
| `photoreal_cinematic` | documentary crowd scenes, film-scale wide, urban march |
| `art` | oil, watercolor, gouache, charcoal, flat vector |
| `portraits` | single-subject editorial or documentary portrait (crowd optional behind) |
| `nature_environment` | landscape-wide; subject small in frame |
| `animals_creature` | named species + handler; crowded market/park when it fits |
| `text_rendering` | **user-requested only** — otherwise no readable text |

Log `render_category_tag` in manifest. Combine with [crowded scenes](#crowded-scenes-p-image), [body type](#body-type-spread), and [scene spice](#scene-spice-when-it-fits) when the brief allows.

### Image edit — `p-image-edit`

Sources: [Arena image edit](https://arena.ai/leaderboard/image-edit) · [AA image editing](https://artificialanalysis.ai/image/leaderboard/editing)

Arena modalities: `single_image_edit` · `multi_image_edit`

Edit diversity tags: `background_swap` · `relight` · `wardrobe_on_plate` · `pose_or_angle_delta` · `multi_ref_composite` · `region_inpaint`

Vary **instruction** and **what changes** while identity URL stays fixed on character arcs.

### Text-to-video — `p-video`

Sources: [Arena text-to-video](https://arena.ai/leaderboard/text-to-video) · [AA text-to-video](https://artificialanalysis.ai/video/leaderboard/text-to-video)

Motion/scene tags: `character_performance` · `landscape_broll` · `urban_street` · `product_demo` · `abstract_mood` · `crowd_scene` · `dialogue_beat`

Rotate `video_prompt` grammar, start plate world, and `camera_tag` per clip.

### Image-to-video — `p-video` (+ plate upload)

Sources: [Arena image-to-video](https://arena.ai/leaderboard/image-to-video) · [AA image-to-video](https://artificialanalysis.ai/video/leaderboard/image-to-video)

Plate-driven tags: `animate_hero_still` · `camera_move_on_plate` · `environmental_parallax` · `avatar_lip_sync` · `hands_or_prop_motion`

Match motion to what the **still** already shows — do not contradict the plate.

### Video edit — `p-video-replace` (and edit-style video)

Source: [Arena video edit](https://arena.ai/leaderboard/video-edit)

Edit tags: `face_recast` · `wardrobe_swap` · `accessory_swap` · `background_replace` · `object_in_hand_swap` · `style_transfer_on_subject`

Same-gender / identity rules for talking-head beats still apply — see [visual-variety-bible.md](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/core/visual-variety-bible/SKILL.md).

## Crowded scenes (`p-image`)

When the brief asks for **busy**, **crowded**, or **lively** worlds — not a lone subject on a blank wall — stack density in the prompt:

1. **Three depth layers** — sharp foreground subject · readable midground faces/hands/props · landmark bokeh (stage, temple, billboards, ferris wheel).
2. **Named population count** — `hundreds of pedestrians`, `dozens of faces in midground`, `20+ tiny clay figures` (stylized sets need explicit counts; models under-deliver on vague "busy").
3. **Activity verbs** — raised hands, umbrellas open, food steam, confetti, market haggling, commuters pressed shoulder-to-shoulder.
4. **Shallow DOF + single subject** — `single subject one frame` keeps one identity readable while the crowd stays behind them.
5. **Age & angle lock** — repeat age band twice (`woman in her late 50s, visibly fifty`) and use [framing & camera](#framing--camera) — models drift younger, center-frame, and front-facing without it.

| Crowd family | Density cues |
|--------------|--------------|
| **Urban rush** | crosswalk stripes, wet reflections, umbrellas, billboard bokeh |
| **Festival / parade** | confetti, raised hands, costume layers, smoke haze |
| **Market / bazaar** | overflowing stalls, hanging goods, steam, price tags as color blobs |
| **Transit crush** | strap hangers, door windows, blurred faces pressed together |
| **Stylized miniature** | counted clay/figurine shoppers (`20+`), cramped aisle, stacked crates |
| **Institutional / ER** | framed oil portraits on beige walls, triage number board, wall sanitizer, vending machine, scuffed linoleum, TV blur, mixed-age seated patients |
| **Urban march / protest** | named city, local landmarks, multiracial crowd cues separate from hero — see [location-matched crowds](#location-matched-crowds) |
| **Group fitness class** | class name + duration, mixed-gender riders, realistic warm studio light — see [group classes](#group-classes--courses) |

**Anti-pattern:** one blurred smear behind a portrait — name **what** the crowd is doing and **where** layers sit. **Institutional** scenes (ER, airport, classroom) need `benches full`, `standing room only`, or `shoulder-to-shoulder` — otherwise models default to a quiet hallway. Name **set dressing** too: framed portraits on walls, triage number board, vending machine glow, scuffed linoleum — generic mint corridors read AI-empty.

## Body type spread

Models default to one “average fitness” body. In diversity batches, **name build on the hero and vary background bodies**:

| Build tag | Prompt cue |
|-----------|------------|
| **Plus-size / curvy** | `plus-size`, `curvy build`, `full-figured` |
| **Athletic / muscular** | `broad shoulders`, `muscular arms`, `athletic build` |
| **Petite / slim** | `petite frame`, `slim build`, `narrow shoulders` |
| **Tall / lanky** | `tall and lanky`, `6-foot frame`, `long limbs` |
| **Stocky / heavyset** | `stocky build`, `heavyset`, `barrel chest` |
| **Lean wiry** | `lean wiry frame`, `weathered thin face` |

**Rule:** rotate build across independent panels in a session — not every hero “athletic build”. Background crowd should mix ages **and** silhouettes (`elderly thin woman`, `heavyset man`, `pregnant woman seated`, `toddler on lap`).

## Location-matched crowds

When the prompt names a **real city or country**, background faces must match that place’s **demographic mix** — not clone the hero’s ethnicity.

| Wrong | Right |
|-------|--------|
| South Asian hero + only South Asian protesters in “New York” | Hero is one identity; crowd explicitly `multiracial NYC march — Black, Latino, white, East Asian protesters` |
| “Dense city march” with no geography | Name city + 3–4 crowd ethnicity cues + local landmarks (yellow cabs, art deco towers, steam vent) |
| Festival in Lagos with only Nordic faces | Match crowd to `setting_tag` region |

**Prompt pattern:** lock hero cast in sentence 1; sentence 2 lists **four+ distinct background silhouettes** unrelated to hero ethnicity; sentence 3 names **local landmarks** so the plate cannot read as generic stock.

**Applies to:** protests, airports, transit, street markets, sports crowds — any scene where “crowded” implies a real place.

## Group classes & courses

When the scene is a **class, workshop, or team activity**, name the **course type** and **who else is in the room** — models default to monochrome crowds (all men, all one age).

| Specify | Example cues |
|---------|----------------|
| **Class type** | `45-minute evening spin class`, `beginner yoga flow`, `HIIT bootcamp circuit` |
| **Room realism** | warm overhead track lights, mirror wall, rubber floor, water bottles, towels — **not** magenta-cyan neon strips unless brief is explicitly nightclub |
| **Gender mix** | hero is one person; crowd `mixed-gender class — women with ponytails, men with beards, nonbinary cyclist` |
| **Body + age mix** | plus-size rider, petite woman, athletic man, woman in her 50s — same as [body type spread](#body-type-spread) |

**Lighting rule for fitness:** real boutique studios are **dim warm overhead** or **single spotlight on instructor** — avoid `split gel`, `neon LED strips`, `magenta-cyan` on photoreal gym plates; those read AI-fake.

**Prompt pattern:** `Documentary fitness portrait` + class name + instructor on bike at front + `20+ mixed-gender cyclists` with 3–4 named background silhouettes + realistic room props.

## Framing & camera

Models default to **centered subject, eyes at camera**. In diversity batches, **rotate `camera_tag` and frame placement** every row — log both in manifest.

**Gaze rule:** `glance off-lens`, `profile`, `back to camera`, `looking down at [prop]`, or `watching the crowd` — **not** `facing camera` or `looking at viewer` unless the user asked for a direct-address avatar plate.

**Placement rule:** name where the subject sits in frame — `left third`, `right third`, `lower right corner`, `edge of frame`, `small in environmental wide` — **not** centered mugshot every time.

| `camera_tag` | Prompt cue |
|--------------|------------|
| **Overhead / bird's eye** | `overhead aerial view`, `top-down`, `drone shot looking straight down` |
| **High corner** | `high angle from corner`, `surveillance-style downward angle` |
| **Worm's eye** | `ground-level worm's eye`, `camera on pavement` |
| **Crane-down** | `slight high angle crane-down` |
| **Over-shoulder** | `over-shoulder from behind`, `seen past someone's shoulder` |
| **Profile / side** | `profile side angle`, `walking across frame` |
| **From behind** | `back to camera`, `three-quarter from behind` |
| **Dutch tilt** | `dutch tilt` — tension scenes only |
| **Through crowd** | `subject visible through gap in crowd`, `foreground heads out of focus` |

**Batch rule:** no two adjacent stills share the same `camera_tag` **and** placement corner (e.g. don't do `left third` twice in a row).

Avatar / lip-sync exception: face must stay readable and mouth visible — use `slight angle from the side` or `three-quarter`, still **off-center** and **off-lens gaze** when not delivering VO to camera.

## Scene spice (when it fits)

Default plates are person + crowd + place. Add **one or two specific attributes** when the setting naturally supports them — not random clutter on every row.

| Spice type | When to add | Example |
|------------|-------------|---------|
| **Animals** | setting implies them | dog park → `golden retriever on leash`; harbor → `seagulls overhead`; rooftop → `pigeons on water tower`; parade → `police horse midground` |
| **Held / worn props** | role or weather | `red umbrella tucked under arm`, `wire beekeeper smoker`, `chipped ceramic mug`, `sample strawberry basket` |
| **Micro-detail** | one thumb-stopping oddity | `muddy paw prints on pavement`, `honey jar on crate`, `green parade beads on fence` |

Camera and placement live in [framing & camera](#framing--camera) — not optional spice.

**Rule:** pick **at most two** spice items per prompt. They must answer “what would a photographer notice here?” — not a checklist dump.

**Skip spice when:** product hero, avatar MC talking head, try-on full-body (garment is the focus), or minimal studio brief.

## Photoreal anti-slop (neon / stylized briefs)

Stylized settings still need **documentary skin discipline** or outputs go waxy:

- Lead with `documentary portrait, natural skin pores, not CGI, not illustration` even for neon/cyberpunk worlds.
- Prefer **worn real materials** — matte leather, faded denim, scratched CRT bezels, sticky carpet — over `holographic puffer`, `chrome armor`, `HUD`.
- Name **gritty location cues** — basement arcade, wet alley, scuffed linoleum — not abstract `neon corridor`.
- Background crowd faces need **imperfect texture**; blur is fine, plastic skin in midground is not.

## Aspect ratio (multi-example sets)

When generating **two or more** stills in one session (playground grid, demo batch, mood board), give each independent output a **different** `aspect_ratio` unless the user locked a format.

**Allowed `p-image` values:** `1:1` · `16:9` · `9:16` · `4:3` · `3:4` · `3:2` · `2:3`

**How to pick:** after the [random seed ritual](./random-seed-ritual.md), use [sum-mod](#ssot-axis-derivation-sum-mod) on `ritual_seed` — state it in the turn (*"Aspect ratio: 16:9"*). Do **not** default every example to `9:16` or `1:1`.

| Ratio | Typical use |
|-------|-------------|
| `9:16` | vertical UGC, full-body fashion, avatar talking head |
| `16:9` | environmental wide, cinematic landscape plate |
| `3:4` | editorial portrait, try-on full-body |
| `4:3` | classic portrait, product + person |
| `1:1` | packshot grid, social tile |
| `3:2` · `2:3` | magazine / poster crops |

Match prompt framing to ratio (e.g. `16:9 horizontal wide shot`, `9:16 vertical full body`). **`p-image-try-on`** inherits plate size when `preserve_input_size: true` — diversify person plates first.

**Same character arc:** one ratio for the whole chain unless the user asks for reframes.

## By model (minimum diversity)

| Model | Besides ritual seed, always vary |
|-------|-----------------------------------|
| **`p-image`** | cast/creature + objects + action + setting + camera + **`render_category_tag`** + **aspect_ratio**; [explicit structure](#explicit-prompt-structure-required); [text hygiene](#text--typography-by-model) (no upsampling) |
| **`p-image-ideogram`** | same axes; explicit typography OK when brief needs it; use `mode: medium`+; [text rules](#text--typography-by-model) |
| **`p-image-edit`** | edit tag + setting/angle delta; same identity URL |
| **`p-image-try-on`** | person plate world + garment complexity; preserve scene |
| **`p-image-upscale`** | N/A on prompt — diversify **source** stills |
| **`p-video`** | motion/scene tag + `video_prompt`; differ start plates per scene |
| **`p-video-avatar`** | `video_prompt` + still world per scene; lock voice per character |
| **`p-video-animate`** | persona still style/setting per slider ref |
| **`p-video-replace`** | video-edit tag + full cast spread on showcase reels |

## When **not** to maximize diversity

- **Same character arc** — lock hero plate URL, one `voice`, cast descriptor; vary only setting/angle/motion per scene.
- **User asked for continuity** — match their cast and approved plates.
- **Draft → final** — same prompt; change only `draft: false`. Use `api_seed` only if user locked API reproducibility.

## Anti-patterns

| Wrong | Right |
|-------|--------|
| Copy doc example ritual strings | [Random seed ritual](./random-seed-ritual.md) — fresh string each time |
| Pass ritual string as API `seed` | Ritual is SSoT planning only; `api_seed` when user requests |
| White wall + MC CU on every demo | Rotate setting + camera + cast |
| One `video_prompt` for whole reel | Unique motion per scene row |
| New ritual string mid avatar chain on same brief | Reuse `ritual_seed` until recast or new independent output |
| Same aspect ratio on every playground example | Rotate `1:1` · `16:9` · `9:16` · `4:3` · `3:4` · `3:2` · `2:3` per [aspect ratio rules](#aspect-ratio-multi-example-sets) |
| Every hero same athletic body | Rotate [body type spread](#body-type-spread) |
| Generic hospital hallway | Named ER set dressing + mixed body types in crowd |
| `holographic` / `chrome` on photoreal cyber scenes | Worn leather, scratched cabinets, documentary skin cues |
| Monoculture crowd in a named global city | [Location-matched crowds](#location-matched-crowds) — hero ≠ background ethnicity |
| Magenta-cyan neon on photoreal gym | Warm overhead studio light, mirror wall, real spin bikes |
| All-male or all-female group class | [Group classes](#group-classes--courses) — mixed-gender background cues |
| Centered subject every frame | [Framing & camera](#framing--camera) — rotate `camera_tag` + placement |
| Subject facing camera / at viewer | Off-lens gaze, profile, from behind, or watching crowd |
| Random animals with no setting reason | Animals only when place implies them |
| Every stylized panel is anime | Rotate [render categories](#render-categories) — use `cartoon_anime_fantasy` at most once per batch |
| Vague `cool portrait, neon vibes` | [Explicit structure](#explicit-prompt-structure-required) — named subject, action, objects, setting |
| `no text` / `without signage` in prompt | Negation invokes text — use [text rules by model](#text--typography-by-model) |
| Dense typography on **`p-image`** | Route to **`p-image-ideogram`** or drop copy — `p-image` has no prompt upsampling |

## Related

- [generation-quality-checklists.md](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/core/generation-quality-checklists/SKILL.md) — core + model checklists
- [staged-generation-gate.md](./staged-generation-gate.md) — approval phases
