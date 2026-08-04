# Generation diversity (all models)

One policy for **every** generative output — images, video, try-on, avatars, replace, animate (Pruna or otherwise). Covers the **random seed ritual**, explicit prompt structure, scenario axis rotation, and **visual variety** ladders.

Use the **full** checklist here for every generation.

## Contents

- [Random seed ritual](#random-seed-ritual-mandatory-before-every-generation)
- [Three steps (every job)](#three-steps-every-job)
- [Still-image prompt flow](./still-image-prompt-flow.md) — `p-image` / `p-image-edit` agent pipeline (brief lock → ritual → POST)
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
- [Visual variety](#visual-variety)
- [Variety checklist](#variety-checklist-before-first-api-call)
- [Prompt patterns (variety)](#prompt-patterns-variety)
- [Anti-patterns](#anti-patterns)

## Three steps (every job)

1. **[Random seed ritual](#random-seed-ritual-mandatory-before-every-generation) (SSoT)** — **always first**, before the prompt. Generate a fresh random string, **state it in the turn**, derive axes via [sum-mod](#ssot-axis-derivation-sum-mod). **Do not** pass the ritual string to API `seed`. **One new ritual string per independent generation**; reuse only on same-brief slop retry.
2. **Write an [explicit prompt](#explicit-prompt-structure-required)** — name specific people, animals, objects, actions, setting, and camera/light. Add text/typography only when the brief needs it — see [text rules by model](#text--typography-by-model).
3. **Diversify the scenario row** — change at least **two axes** from the previous output in the same session (cast, setting, camera, **`render_category_tag`**, **aspect_ratio**, creatures, props, … — unless user asked for continuity).
4. **Log** — `ritual_seed`, axes chosen, prediction id (manifest or turn text).



## Random seed ritual (mandatory before every generation)

The random seed ritual is a lean [String Seed of Thought](https://pub.sakana.ai/ssot/) (DAG) protocol. **Every** Pruna generation — every prompt, every `POST /v1/predictions`, every scene row — starts here.

This prevents copy-pasting example strings (`k7Qm2xP9`, `482901`, …) and reduces accidental duplicate outputs across sessions.

### The ritual (do this first)

Before writing prompts, curl, or runner JSON:

1. **Generate a random string** in-agent (8–16 chars, mixed case + digits).
2. **Log it** as `ritual_seed` in the manifest / internal plan. Do **not** require a user-visible *"Ritual seed: …"* line unless the user asks for transparency.
3. **Derive prompt choices** from the string — sum char codes, mod N — pick axes from this doc (`aspect_ratio`, `camera_tag`, `render_category_tag`, …).
4. **Write the prompt** using [explicit prompt structure](#explicit-prompt-structure-required) and derived axes.
5. **Record** axes chosen and prediction id in the manifest alongside `ritual_seed`.

**Do not pass the ritual string to API `seed`.** API runs without `seed` unless the user explicitly requests reproducibility (`api_seed`).

**Never** proceed to `POST /v1/predictions` without completing steps 1–2 (unless the user supplied an explicit `api_seed` — see below).

### Reuse rules

| Situation | Action |
|-----------|--------|
| **New hero / independent still / mood-board panel** | Fresh ritual string |
| **Same-brief slop retry** | Reuse same `ritual_seed`; note `retry_ritual_seed` in manifest |
| **Same character arc** | Lock **hero plate URL** + cast descriptor; reuse `ritual_seed` only on same-brief regen |
| **User says "lock seed" / provides integer** | Pass **their** number as `api_seed` → `input.seed`; skip new ritual for that chain |

Character continuity = approved plate URL + cast descriptor — **not** the ritual string on the API.

### Ritual anti-patterns

| Wrong | Right |
|-------|--------|
| Copy example strings from SKILL.md | Fresh ritual string each independent generation |
| Pass ritual string as API `seed` | Ritual is planning-only; `api_seed` only when user asks |
| One ritual string for entire mood board | New ritual per independent **`p-image`** |
| Skip ritual because API `seed` is optional | Ritual always; API omits `seed` by default |

### Example (internal plan / optional user-visible)

Manifest: `"ritual_seed": "k7Qm2xP9"`. Derived: aspect_ratio 16:9, camera_tag fish-eye, render_category_tag cartoon_anime_fantasy.  
Prompt: Disco ball reflections on an otter DJ scratching vinyl at a packed 1970s roller rink, fish-eye lens, glitter confetti mid-air, funky energy.  
…then curl / runner **without** `"seed"` in `input`.

### Manifest snippet

```json
{
  "ritual_seed_policy": "ssot_dag_before_every_generation",
  "ritual_seed": "k7Qm2xP9",
  "seed_log": [
    { "phase": "hero_p_image", "ritual_seed": "k7Qm2xP9", "creature_tag": "otter_dj", "setting_tag": "1970s_roller_rink", "prompt_hash": "…" },
    { "phase": "scene_2_avatar", "ritual_seed": "k7Qm2xP9", "scene_id": 2 }
  ]
}
```

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
| **`p-image-ideogram`** | Optional (`prompt_upsampling`; **prefer `false`** unless brief is sparse) | **Default T2I** for readable type, hex colors, JSON-style control blocks, and panel layouts. List exact strings + surfaces; use `thinking: high` + `image_size: 2K` when legibility is critical. |
| **`p-image`** | **No** effective prompt upsampling | **Avoid** dense readable-type requests unless user explicitly wants `text_rendering`. Short prompts; skip `readable`, `legible`, `headline`, multi-sign lists — they drift to gibberish. Use when user asked **cheap / fast** or bulk draft throughput. Collage triggers still apply: `interactive-explainer` (`flat lay`, `grid`, `collage`, …). |

**`p-image` text hygiene:** prefer scenes without copy. If a screen appears: `monitor soft colorful blur glow only` — not legible UI unless the user explicitly asked for readable text (route to **`p-image-ideogram`** or simplify the brief).

**Channel split (quotes vs tags):**

- **`text_spec` (stills):** `"[exact string]"` + `[surface]` + `[placement]` → `image-prompting` §5
- **Native clip dialogue:** `p-video` Mode A only (`[subject] says "[LINE]"` + mouth + gesture) → `video-prompting` — not `p-image`
- **`[tags]`:** Gemini TTS `text` performance only — not still typography, not `p-video` motion prompt → `audio-prompting`

**Collage triggers (all T2I models):** still avoid `flat lay`, `packshot`, `grid`, `collage`, `montage`, `contact sheet`, `split`, `before and after` — use `single frame`, `one camera angle` instead. Full table: `interactive-explainer`.

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

Full style/camera/lighting ladders: [Visual variety](#visual-variety) below. Persona + try-on bar: `image-prompting`.

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

Same-gender / identity rules for talking-head beats still apply — see [Cast diversity](#cast-diversity) below.

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

**How to pick:** after the [random seed ritual](#random-seed-ritual-mandatory-before-every-generation), use [sum-mod](#ssot-axis-derivation-sum-mod) on `ritual_seed` — state it in the turn (*"Aspect ratio: 16:9"*). Do **not** default every example to `9:16` or `1:1`.

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
| Copy doc example ritual strings | [Random seed ritual](#random-seed-ritual-mandatory-before-every-generation) — fresh string each time |
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
| Dense typography on **`p-image`** | Drop copy or simplify the brief — `p-image` has no prompt upsampling |

## Visual variety

Use this whenever you plan **`p-image`**, **`p-image-edit`**, **`p-video-avatar`**, **`p-video-animate`**, or **`p-video-replace`** rows. Run the **Variety checklist** at the bottom before the first API call.

### Goal

Showcase and multi-scene work should feel **art-directed**, not like the same talking head in the same office repeated eight times. Deliberately vary:

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

Plan a **cast ledger** before generation. For **skills-library / showcase batches** (not single-spokesperson arcs):

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

For **showcase and multi-scene** work, plan at least **4 distinct visual styles** across the full piece. Pick from (mix and match):

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
| **Meme / reaction** | dorm, gaming chair, exaggerated expression (reaction / meme beat pattern) |
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

## Prompt patterns (variety)

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
| **Unified bar** | this document · `image-prompting`
| **Person plate** | Photoreal **`p-image`** editorial prompts → slop gate |
| **Try-on** | Garment tiers + preservation — `image-prompting` |
| **Avatar motion** | Unique **`video_prompt`** per clip; natural **`voice_script`** |
| **Cast** | Diversity ledger — gender, age, ethnicity spread |
| **Playground** | Pin try-on refs on [p-image-try-on](https://replicate.com/prunaai/p-image-try-on); match with diverse [p-video-avatar](https://replicate.com/prunaai/p-video-avatar) examples — @ShinyTaskForce |

**Try-on → avatar handoff:** approved try-on still → optional upscale → **`p-video-avatar`**; lock **`seed`** from person-plate generation.

## Workflow-specific notes

| Workflow | Variety emphasis |
|----------|-------------------|
| `p-image-try-on` | Editorial plates + complex garment refs; preservation checklist; diversity across playground set |
| `p-video-replace` | Scene 1 **persona ladder** + per-scene distinct `still_edit` backgrounds; optional **light bed** after concat |
| `p-video-animate` | 3–4 **style tags** per animate slider row |
| `avatar-multi-scene` | Every avatar row: new `setting_tag` + `camera_tag` via `p-image-edit` |
| WORKFLOW-RECIPES | Intake must capture variety plan before recipe execution |

## Variety checklist (before first API call)

- [ ] **Cast:** gender, age, and ethnicity spread across scenes — not one default face
- [ ] **Settings:** no adjacent duplicate `setting_tag`; at least 5 distinct environments in an 8-scene project
- [ ] **Palettes:** no three adjacent scenes share the same dominant accent; name gel/light pairs in prompts
- [ ] **Textures:** wardrobe rows name fabric/material (fur, holo, satin, clay)
- [ ] **Camera:** at least 3 different `camera_tag` values; no duplicate motion grammar on every `video_prompt`
- [ ] **Motion props:** `video_prompt` glance targets match objects in `still_edit`
- [ ] **UGC/install rows:** source + refs use **different** locations and cameras — not neutral grey wall on all stills
- [ ] **Lighting:** at least 3 different `lighting_tag` values; stylized scenes name their light mood
- [ ] **Styles:** at least 4 `visual_style_tag` values in a multi-scene piece (mix **photoreal**, **sketch/2D**, **stop-motion 3D**, **CG 3D**)
- [ ] **Render mediums:** persona ladder includes 5+ distinct mediums when showcasing replace range
- [ ] **Persona ladder:** hook or animate row includes 6+ visually distinct refs if showcasing range
- [ ] **Local consistency:** refs within one scene row share one style; across rows, styles diverge
- [ ] **Lip sync:** VO rows still use speaking sources + preserve-lips `instruction_prompt` language
- [ ] **Delivery:** if the reel ships with avatar VO, confirm whether to add an **light instrumental bed** under dialogue (`stable-audio-2.5`, ~0.12 volume, no vocals)

## Related

- [generation-quality-checklists.md](./generation-quality-checklists.md) — core + model checklists · [approval gates](./generation-quality-checklists.md#approval-gates-workflows)
- `image-prompting` — persona planning
