---
name: educational-explainer
description: Builds educational short films — history, science, nature, how-it-works, children's topics — that alternate narrator p-video beats (scene anchor triple + Gemini TTS) with in-story character dialogue via p-video-avatar. p-image hero, p-image-edit stills, assembly with optional bed. Use for any explainer where the host interacts with experts, witnesses, or characters instead of pure voice-over.
metadata:
  version: "0.0.8"
---

# Educational explainer (narrator + character interaction)

**Not** wall-to-wall narration. Alternate **host / narrator VO** (`p-video` + TTS) with **people in the story speaking** (`p-video-avatar` + `voice_script`) — historians, scientists, witnesses, animated guides, etc.

Canonical scene patterns: [educational-explainer-scenes.md](../../../../../references/workflows/interactive-explainer-scenes.md)  
Motion (dynamic, physics-safe): [educational-explainer-motion.md](../../../../../references/workflows/interactive-explainer-motion.md)  
Narrator triple spec: [scene-anchor-triple.md](../../../../../references/video/scene-anchor-triple.md)

See [p-video](../../../../tools/video/p-video/SKILL.md), [p-video-avatar](../../../../tools/video/p-video-avatar/SKILL.md), [p-image](../../../../tools/image/p-image/SKILL.md), [p-image-edit](../../../../tools/image/p-image-edit/SKILL.md), [gemini-3.1-flash-tts](../../../../tools/audio/gemini-3.1-flash-tts/SKILL.md).

For **narrator-only** explainers, use [multi-scene-ai-video](../../core/narrated-multi-scene/SKILL.md) instead.

**Staged generation:** [staged-generation-gate.md](../../../../../references/shared/staged-generation-gate.md) — approve plan → stills → narration TTS → video clips → assembly + bed. Default runner phase is **`stills`**.

## Subject flavors (pick one `style_bible`)

| Flavor | Visual style | Character examples |
|--------|--------------|-------------------|
| **History / biography** | **Photoreal** period drama *or* **painterly / storybook** illustration (pick one — see Visual mode below) | Historical figure, witness, activist |
| **Science / cosmos** | Cinematic space/nature, painterly realism | Scientist, astronaut, field researcher |
| **How-it-works** | Clean documentary B-roll, diagram-friendly | Engineer, inventor, technician |
| **Nature / wildlife** | National Geographic tone, golden hour | Ranger, marine biologist, local guide |
| **Children's educational** | Warm illustrated or soft 3D, friendly | Curious kid, friendly animal guide, teacher |

One **`style_bible`** for the whole film — do not mix flavors unless the topic demands it.

## Defaults (720p / 24 fps)

Every plan should set:

```json
"defaults": {
  "resolution": "720p",
  "fps": 24,
  "aspect_ratio": "16:9"
}
```

- **`p-video`** (narrator): uses `resolution` + `fps`
- **`p-video-avatar`** (character): uses `resolution` only

Template: [`explainer-plan.template.json`](templates/explainer-plan.template.json)

## Motion (dynamic, physics-safe)

Every scene needs **visible motion** — but not physics-heavy action. See [educational-explainer-motion.md](../../../../../references/workflows/interactive-explainer-motion.md).

| Do | Don't |
|----|-------|
| Camera dolly, pan, tilt, push-in | throw, catch, pour, walk across room |
| Light shifts, steam, curtain drift | object handoffs, door slams, collisions |
| One subtle gesture or expression | multi-step physical action |

Write **`video_prompt`** as `OPEN:` → `MID:` (attention hook) → `CLOSE:` (settle on end still). Keep camera moves **slow and deliberate** (use `1080p` / `48` fps only when the user asks for final delivery).

## Intake: ask before generating

| Topic | Questions |
|-------|-----------|
| **Topic** | What should the viewer learn? Key facts or story beats? |
| **Audience** | Kids, general public, enthusiast? Sets tone and vocabulary |
| **Flavor** | History? Science? Nature? How-it-works? Illustrated? |
| **Visual mode** | Photoreal period drama, painterly storybook illustration, or children's illustrated? (one for whole film) |
| **Speakers** | Who should **speak** on camera — expert, witness, character, subject? |
| **Interaction mix** | Target **≥ 35% character beats** — who speaks, in what order? |
| **Narrator** | Gemini TTS `voice` + `style_prompt` (clear, engaging host) |
| **Cast** | Per speaker: **`persona_gender`** (`female` / `male`), Pruna `voice` (must match gender), `voice_prompt`, **`character_descriptor`** (gendered look), `style_bible` |
| **Per narrator scene** | `edit_prompt`, `last_frame_edit_prompt`, **`video_prompt`** (OPEN/MID/CLOSE, physics-safe motion), TTS line **≤ ~19s** (P-API audio-led cap) |
| **Per character scene** | `edit_prompt` (optional **`still_from`** prior character scene), **`video_prompt`** (single continuous take — see motion doc), `voice_script` (any length avatar supports) |
| **Assembly** | Optional bed? Crossfades? |

Draft the **full scene table** as a dialogue arc before any API calls. Confirm with user (**Phase 0 — plan**). Do not call generative APIs until the user replies **approve plan** / **go**.

**Story depth bar (required before render):** The film must pass the [stand-alone test](../../../../../references/workflows/interactive-explainer-scenes.md#stand-alone-test). If the story is a biography, pick **one through-line** — not a life survey.

## Feedback gates (required)

| Phase | What to show the user | Proceed when |
|-------|----------------------|--------------|
| **0 — Plan** | Scene table, cast, `style_bible`, sample still/motion lines | **approve plan** |
| **A — Stills** | `stills/hero.png`, scene start/end PNGs | **approve stills** |
| **A2 — TTS** | `audio/narration_*.mp3` — listen for pace and length | Lines OK → **phase video** |
| **B — Video** | `clips/*.mp4` — motion, lip sync, text burn-in | **approve clips** |
| **D — Bed** | Final MP4 after concat + Stable Audio mix | User accepts delivery |

Ask when art direction is unclear (visual mode, cast continuity, narrator vs character mix, bed yes/no) — see [staged-generation-gate.md](../../../../../references/shared/staged-generation-gate.md).

### Scene table (template)

| `#` | `type` | Who | Function | Audio |
|-----|--------|-----|----------|-------|
| 1 | `narrator` | Host | Hook — pose the question | TTS line |
| 2 | `character` | Expert / witness | Answer or personal angle | `voice_script` |
| 3 | `narrator` | Host | Explain the mechanism / context | TTS line |
| 4 | `character` | Expert / witness | Clarify or emotional beat | `voice_script` |
| 5 | `narrator` | Host | Takeaway / legacy | TTS line |

## Scene types

| `type` | Model | Stills | Audio |
|--------|-------|--------|-------|
| **`narrator`** | `p-video` | start + end via `p-image-edit` | TTS → upload → `input.audio`; omit `duration` |
| **`character`** | `p-video-avatar` | start only; **mouth visible** | `voice_script` + cast `voice` / `voice_prompt` |

Default if omitted: **`narrator`** (backward compatible with older all-VO plans).

## Workflow

### Phase 0 — Hero (`p-image`)

One anchor still from `hero_prompt` + `style_bible` + optional `project_seed`.

### Phase 1 — Start stills (`p-image-edit`, parallel)

All scenes (narrator + character) get a start still from hero + `edit_prompt`.

### Phase 2 — End stills (`p-image-edit`, parallel)

**Narrator scenes only** — `last_frame_edit_prompt` from start still.

### Phase 3 — Narrator TTS (parallel)

Gemini TTS for **`narrator`** rows only. Probe duration; keep **≤ ~19s** per narrator scene ([`validate_narration_duration`](../../_shared/scripts/p_video_payload.py)). The **20s cap applies to audio-led `p-video` only** — **`p-video-avatar` clips follow `voice_script` length** and may run longer than twenty seconds.

### Phase 4 — Video (parallel)

- **`narrator`:** `build_p_video_payload` with `image` + `last_frame_image` + `audio`, `save_audio: true`
- **`character`:** `p-video-avatar` with still URL + `voice_script` + cast voice fields + `video_prompt`. Runner **prepends `character_descriptor`** to character `edit_prompt` and sets **`voice` from `persona_gender`** (`female` → `Zephyr (Female)`, `male` → `Puck (Male)`). Runner also sets **`negative_prompt` + `negative_prompt_strength`** (experimental) to suppress burned-in text on avatar output — see [p-video-avatar](../../../../tools/video/p-video-avatar/SKILL.md) **Negative prompt**.

Pass `project_seed` to avatar clips when locking motion.

### Character beats: text suppression (stills + avatar API field)

| Layer | What to do |
|-------|------------|
| **P-Image stills** | **Positive prompts only** — plain surfaces, unprinted props, one camera angle (runner errors on blocked substrings). |
| **`p-video-avatar`** | `defaults.avatar_negative_prompt` is a **Pruna suppression token list** (nouns like `subtitles`, `watermark`) — **not** creative wording. Do **not** write sentences there; keep the default list in [`p_video_avatar_payload.py`](../../_shared/scripts/p_video_avatar_payload.py). Strength **0.35** unless disabled per scene. |
| **`voice_prompt`** | **Positive delivery only** — e.g. `restrained matter-of-fact delivery`, `clear lip sync`, `working-class dignity`. Script lines stay in `voice_script` only. |

**Never** use `no …`, `avoid …`, `not …`, `without …`, `don't`, or `do not` in `hero_prompt`, `style_bible`, still lines, `video_prompt`, `voice_prompt`, `narration.style_prompt`, or bed `prompt`. Spoken lines (`scene_lines`, `voice_scripts`) may use natural negation for history dialogue.

### What the runner sends (plan.json ≠ output manifest)

| File / field | Fed into generative APIs? |
|--------------|---------------------------|
| **`output/.../manifest.json`** | **No** — write-only record (`title`, `final`, `scene_types`) after assembly |
| **`skill.manifest.json`** | **No** — install bundle (script paths, tool skills) |
| **`plan.json` → `hero_prompt` / `edit_prompt` / `last_frame_edit_prompt`** | **Yes** — sanitized (`OPENING:`/`CLOSING:`/`Same` stripped), then **`positive_style_bible`** appended |
| **`plan.json` → `style_bible`** | **Yes** — must be **positive comma-clauses only**; runner **`validate_plan`** rejects `no …` / `avoid …` / `not …` |
| **`plan.json` → `narration.style_prompt`** | **TTS only** (Gemini) — not appended to `p-image` / `p-video` |
| **`plan.json` → `voice_scripts` / `voice_prompt`** | **Avatar only** (`voice_script` + `voice_prompt` fields) |
| **`plan.json` → `video_prompt`** | **`p-video` / `p-video-avatar` only** — positive motion wording + `positive_style_bible` append |
| **`cast.character_descriptor`** | **First** character still from hero only; rows with **`still_from": "_cast_*"`** use **`edit_prompt` + positive bible** (descriptor not duplicated) |

Do not paste the whole plan, scene list, or manifest into a single image prompt — one scene line + positive style per API call.

### Positive prompts only (required)

`hero_prompt`, `style_bible`, `edit_prompt`, `last_frame_edit_prompt`, `video_prompt`, `voice_prompt`, and bed `prompt` must describe **what appears** — never what to leave out.

**Banned in creative fields** (runner **`assert_positive_wording`**):

| Banned pattern | Write explicitly instead |
|----------------|--------------------------|
| `no text` / `no signage` / `no labels` | `plain unmarked walls`, `unprinted wood surfaces`, `matte unprinted props` |
| `avoid markets` / `avoid text` | `plain wood table`, `single camera angle`, `one focal subject` |
| `not theatrical` / `no cuts` | `restrained matter-of-fact delivery`, `single uninterrupted take` |
| `without vocals` | `instrumental only` |
| `no cartoon` / `no modern` | `painterly historical illustration`, `period-accurate 1770s props only` |

Saying **`no text`** often **creates** readable type. Saying **`avoid crowds`** still invokes crowds. Be explicit about the single frame you want.

**Rules:**

1. **One positive sentence per still line** — location, subject, light, period, `one camera angle`.
2. **`style_bible`** — positive comma-clauses only (same vocabulary as stills). Example: `unprinted wood and parchment surfaces, plain unmarked walls, warm saturated full color, 16:9`.
3. **Character `edit_prompt`:** `lips visible`, **slight angle from the side**; use `speaks directly to camera` in **`video_prompt`** only.
4. **`video_prompt` (narrator):** OPEN / MID / CLOSE — camera + light + atmosphere (see [interactive-explainer-motion.md](../../../../../references/workflows/interactive-explainer-motion.md)).
5. **`video_prompt` (character):** `single continuous medium close-up`, `one very slow push-in`, `single uninterrupted take` — not OPEN/MID/CLOSE beats.
6. Runner **`validate_plan`** errors on banned substrings in [`run_from_plan.py`](scripts/run_from_plan.py) `STILL_PROMPT_TRIGGERS` **and** on `no` / `avoid` / `not` / `without` / `don't` / `do not` in creative fields.

#### Text & signage (most common in explainers)

| Blocked phrase in stills | Why | Use instead |
|-----------------|-----|-------------|
| `farmers market`, `market stall`, `storefront`, `signage`, `neon signs` | price boards, aisle signs, branded stalls | produce on **plain wood table**, **matte unprinted** baskets |
| `labeled`, `packaging`, branded bags, `price tag`, `menu`, `napkin` | product copy on surfaces | **matte unprinted** jars, food in **plain glass bowl** |
| `graphic tee`, `decal`, `sticker`, `magazine`, `poster` | printed type on surfaces | solid-color fabrics, unbranded matte props |
| `plated meal`, `restaurant`, `utensil`, `fork`, `knife` | menus, rim logos, cutlery embossing | **matte ceramic plate** on **plain counter**, subject food only |
| `documentary still`, `educational still`, `educational end`, `end frame`, topic-specific doc labels | models literalize meta words as on-screen type | `photoreal still`, `single frame`, `closing composition` |
| `ring light`, `studio lighting`, `HUD`, `game`, readable screens | UI text, spec overlays | sunny window, golden afternoon, soft monitor glow |
| `maps`, `map`, `newspaper`, `broadside`, `poster`, `placard`, `ledger`, `open book`, `proclamation`, `headline`, `caption`, `inscription`, `congress`, `liberty`, `parliament`, `meeting house`, `constitution`, `declaration`, ship names on hulls | printed type on walls/tables or named banners | blank folded parchment, plain walls, unmarked wood, **merchant wharf** / **colonial assembly hall** (no proper nouns on surfaces) |
| `greyscale`, `grayscale`, `graphite`, `muted-tone`, `desaturated`, cold mist / freezer haze | flat or grey frames | **warm saturated** full color, steady window light |
| `flicker`, `strobe`, `pulse`, rapid `light shifts` / `brightens` in **narrator** `video_prompt` | pulsating exposure in `p-video` | **one** slow push-in or pan in **steady** daylight |

#### Collage & layout

| Blocked phrase | Use instead |
|-------|-------------|
| `split`, `side by side`, `before and after`, `comparison`, `grid`, `collage`, `montage`, `contact sheet`, `flat lay`, `packshot`, `multiple angles`, `dual` | one subject, one camera angle, one frame |
| **`OPENING:` / `CLOSING:`** prefixes on still lines | plain scene description — those labels read as **two-panel storyboard** frames to `p-image` |
| **`Same …`** matching prior shot (`Same harbor`, `Same painterly man`) | describe the one frame directly; use `still_from` / `_cast_*` for identity — **never** “match opening” language |
| Counted triples in stills (`three ships`, `three panels`) | “colonial ships at one wharf”, “one camera angle” — counts invite triptychs |
| `storyboard`, `frame by frame`, `triptych`, `cross-section` (unless one diagram is the sole subject) | one continuous composition, one camera angle |

Runner **`sanitize_still_prompt`** strips `OPENING:`/`CLOSING:` and leading `Same` before API calls; **`validate_plan`** errors on the substrings in [`run_from_plan.py`](scripts/run_from_plan.py) `STILL_PROMPT_TRIGGERS`.

#### Weather

| Blocked phrase | Use instead |
|-------|-------------|
| `rain`, `wet pavement`, `puddle` | bright open sky, sunny window, golden afternoon |

#### `style_bible` example (positive only)

```text
Premium painterly historical illustration, one focal subject per shot, one camera angle, 16:9, unprinted wood surfaces, plain unmarked walls, warm saturated full color, period-accurate props
```

#### Good vs bad (still lines — any topic)

| Bad still line | Good still line |
|----------------|-----------------|
| `No text, no signage, farmers market` | `Plain wood table`, matte unprinted baskets, sunny window, **one camera angle** |
| `Avoid labels on packaging` | **Matte unprinted** jars on **plain counter** |
| Meta phrase **documentary still** + **end frame** | Concrete place + objects + **closing composition**, **one camera angle** |

Broader blocked-phrase table (keyboards, mirrors, packshots): [p-video-replace-comparison/SKILL.md](../../launches/p-video-replace-comparison/SKILL.md) **Prompt trigger words**.

**If text appears in `p-video` but stills are clean:** simplify the narrator `video_prompt` (camera/light only) or regenerate stills with **plain surfaces** — never answer with `no text` in the prompt.

### Avatar gender ↔ voice lock

Every `cast` entry used on character rows **must** include:

```json
"persona_gender": "female",
"voice": "Zephyr (Female)",
"character_descriptor": "woman, …"
```

Optional per-scene override: `"persona_gender": "male"` on a character row. Descriptor must name the same gender (woman/female or man/male) so the generated face matches the voice.

**Character still after object/B-roll hero:** when the hero is **objects, landscapes, or diagrams**, the next **character** edit from hero alone often **drops the speaker**. Set `"still_from": "<id_of_last_good_character_scene>"` so `p-image-edit` branches from that talking-head still. In `edit_prompt`, state that the **cast member dominates the frame** (head-and-shoulders, lips in frame); props stay small and out of focus.

### Cast face lock (`anchor_still_prompt` + `still_from`)

When the hero is **objects or landscapes**, character edits from hero alone **drift face and costume**. Per cast entry, set **`anchor_still_prompt`** (portrait on a neutral set). The runner generates `stills/_cast_<key>.png` in **Phase 0**, then every character row uses `"still_from": "_cast_<key>"` with a short scene-specific `edit_prompt` that starts with **Same painterly …**.

Generate anchors **before** scene stills; do not rely on parallel `still_from` of a later scene id (race → hero fallback → new face).

### Phase 5 — Assembly

Normalize clip audio → concat → optional [stable-audio-2.5](../../../../tools/audio/stable-audio-2.5/SKILL.md) bed.

**Too many hard cuts:** raise `assembly.hard_cut_crossfade_seconds` (e.g. **0.2–0.35**) for narrator↔character and vignette changes; use `chain_crossfade_seconds` only when `chain_from_previous: true`. [`concat_clips.py`](../../_shared/scripts/concat_clips.py) applies **`acrossfade`** on audio whenever video uses **`xfade`** — do not hard-cut audio under a visual crossfade. Optional `still_from` + `still_from_end: true` on the next narrator row branches from the prior scene’s **end still** (runner Phase 1b after end stills) for smoother bookends.

**Audio sounds wrong / lines cut off:** re-run assembly only (no API) after fixing concat; bed mix uses `amix` with `duration=first` and `normalize=0` so narration level stays stable under the bed.

## Scripting rules

### Narrator carries facts; character carries witness

Split labor like a prestige documentary — **not** two voices saying the same summary.

| Voice | Job | Good | Bad |
|-------|-----|------|-----|
| **Narrator** | Context, dates, names, stakes, the question | Concrete fact, then a pointed question tied to the next beat | Vague praise or life-summary slogans |
| **Character** | First-person reply to the **specific** prior question | Sensory or procedural detail that answers that question | Motivational poster copy unrelated to the question |

### One through-line per film

Pick **one question** the whole short answers (e.g. *Can power act without consequence?* or *Why did one place honor them when another did not?*).

**Anti-pattern:** biographical **life survey** — many eras or locations in one short, each beat a slogan instead of a scene.

**Fix:** narrow scope, or add scenes — never cram two chapters into one narrator row or one visual.

### Causal chain (event explainers — required)

Viewers cannot follow *what happened* if the film opens on the climax. For protests, wars, discoveries, or policy fights, map **prerequisites → trigger → act → response → legacy** before rendering.

| Beat (minimum) | Narrator carries |
|----------------|------------------|
| **Stakes / hook** | Why anyone cared |
| **Mechanism** | Law, policy, or force that caused the crisis |
| **Local complication** | Why *this* place or group differed |
| **Deadline / trigger** | Clock or last chance before the act |
| **Act** | What people did (on a narrator row with matching B-roll) |
| **Response** | Authority's punishment or counter-move |
| **Aftermath** | How the story continued (congress, boycott, war, reform, discovery) |

**Anti-pattern:** open on the **climax** then jump to **reaction** with no mechanism, local standoff, or deadline — the ending feels hollow because the middle never taught the cause.

### Visual–audio alignment (required)

Each row's **`edit_prompt` / `last_frame_edit_prompt` must depict what that row's audio says** — same location, props, and era. Models cannot infer context from narration alone.

| Rule | Good | Bad |
|------|------|-----|
| **Narrator B-roll** shows the fact being spoken | Meeting hall interior while VO describes the meeting | Generic exterior while VO names a specific interior action |
| **Character still** matches witness setting | Witness at the wharf while they speak about the ships | Witness in unrelated interior while VO discusses the wharf |
| **Action on narrator rows** | Destruction / closure / trial on `type: narrator` | Event described in VO but only a talking head on screen |
| **One chapter per frame** | One location or action per still | Multiple story chapters collapsed into one still |

**Character beats** are talking heads by design (`p-video-avatar`). Put **events** on narrator triples; place the witness **in the environment** the line references (wharf, doorway, dock), not a neutral interior.

### Visual mode (lock one look)

Pick **one** rendering mode for the whole film. Put the mode in **`style_bible`** and repeat the **same vocabulary** in `hero_prompt`, every `edit_prompt`, and `character_descriptor` — not a mix.

| Mode | When to use | `style_bible` + still vocabulary |
|------|-------------|----------------------------------|
| **Photoreal period** | Prestige documentary, adult general audience | `photoreal period drama film still`, natural skin texture, period-accurate wardrobe, shallow depth of field |
| **Painterly / storybook** | Editorial history shorts, classroom tone, graphic-novel feel | `premium painterly historical illustration`, soft ink outlines, editorial storybook realism, rich period color |
| **Children's illustrated** | Young audience | warm illustrated or soft 3D, friendly proportions, simpler shapes |

**Anti-pattern — style mismatch:** `style_bible` says storybook but still lines say `photoreal` (or the reverse). Models drift toward generic or uncanny frames. **Fix:** align every still line to the chosen mode; only change mode on user request, then **regen all stills**.

**Blocked substrings** still apply in both modes — see **Positive prompts only** above.

### Ending closure bar (required)

The film must **close**, not stop. Viewers need **facts after the act**, a **human witness**, and a **narrator recap** that answers the opening hook.

#### Three-beat close (history, biography, causal-chain topics)

| Order | Row | Job |
|-------|-----|-----|
| 1 | **Narrator aftermath** | Punishment, collective response, dated next step (≥ 3 concrete facts) |
| 2 | **Character witness** | First-person line tied to that aftermath — not a poster slogan |
| 3 | **`11_wrap` narrator recap** (or `07_conclusion` / `NN_wrap`) | Third-person **summary**: restate cause → act → consequence → legacy in one line each; **answer the hook**; warm tone; **no question** to a character |

Add **`narration.scene_lines["NN_wrap"]`** and a final **`type: narrator`** scene with harbor/hero **bookend** stills when the opening was a place (reuse `still_from` + `still_from_end` from hook when it fits).

**Science / how-it-works** may end on **narrator only** after the expert (see fruit-veg `07_conclusion`) — same recap job, no extra character row.

Before render, the **aftermath + wrap** narration must state explicitly:

1. **Punishment or reaction** — what the other side did (laws, port closure, trial, embargo).
2. **Colonial / public response** — boycott, congress, solidarity, refusal to pay damages.
3. **Next escalation** — the concrete step toward war, reform, or discovery (e.g. First Continental Congress → Lexington; lawsuit → election).
4. **Recap line** — one sentence that ties the through-line and answers *why this mattered* without “in conclusion” meta language.

**Anti-pattern:** ending on character platitude only; no narrator wrap; recap repeats the hook verbatim without new synthesis.

**Anti-pattern:** one rushed consequence line plus a legacy platitude with no punishment detail, collective response, or dated next step.

**Fix:** add **`09_aftermath`** (or split consequence across two narrator scenes), then **witness**, then **`NN_wrap` narrator**. Target **≥ 3 concrete facts** in the aftermath narrator; wrap ≤ ~19s TTS.

### Stand-alone test

Before API calls, confirm:

1. **Stakes** — what could be lost? (liberty, dignity, life, truth)
2. **Conflict** — who or what opposed the subject?
3. **Turn** — what changed after the key event?
4. **Nuance** — at least one contradiction or complication (not hagiography)
5. **Closure** — viewer understands outcome without reading Wikipedia

If any answer is missing, rewrite the scene table — do not render.

**Narrator (`narration.scene_lines`):**
- Clear, engaging host — third person; **concrete facts** (dates, names, places)
- One story beat per scene; **≤ ~19s** when read aloud
- End with a **specific question** when the next row is `character` — not "what did she remember?"
- Match audience level (simple for kids, precise for science)

**Character (`voice_scripts` or scene `voice_script`):**
- **Witness testimony** — reply to the narrator's exact question; use "I", specific detail
- Grave, natural speech — not inspirational poster copy or brochure slogans
- **No ~19s cap** — longer replies are fine; one avatar take beats cramming or splitting
- **`video_prompt`:** one continuous shot (slow push-in), **not** OPEN/MID/CLOSE beats — multi-beat prompts cause jarring transitions inside the clip
- Use `follows` in plan; see [multi-scene-avatar-video/prompt-templates.md](../../core/avatar-multi-scene/prompt-templates.md)

**Anti-patterns:**
- All-narrator tables (lecture, not a conversation)
- Character lines in `narration.scene_lines` (wrong voice pipeline)
- Gemini TTS voice names on `p-video-avatar` (use Pruna voices)
- Missing **lips in frame** on character stills; **facing camera** in character still prompts (use `video_prompt` for on-camera delivery)
- Missing **`persona_gender`** on cast / voice not matching generated avatar gender
- **Negative or avoidance prompts** — `no …`, `avoid …`, `not …` in stills, `style_bible`, or `video_prompt`; use explicit positive props and surfaces instead
- Still-prompt **blocked substrings** — markets/signage, `labeled`/`packaging`, meta words (`educational`, `documentary still`, `end frame`), collage language; see **Positive prompts only** above
- Biographical life-survey cramming vs single through-line
- Motivational character lines instead of witness detail
- Narrator rows that combine two visual chapters in one still
- Static `video_prompt` (`OPEN: hold. CLOSE: hold.`) — always add a MID motion beat
- Physics-trap motion (throwing, pouring, walking, prop handoffs) — see [educational-explainer-motion.md](../../../../../references/workflows/interactive-explainer-motion.md)
- `720p` / `24` fps unless user explicitly requests draft quality
- **Missing causal chain** — climax without prerequisite beats (mechanism, local standoff, deadline)
- **Visual–audio mismatch** — character interior while narration describes harbor, ships, or courts
- **Visual mode mismatch** — `photoreal` still lines under a storybook `style_bible`, or `painterly` / `illustration` lines under a photoreal `style_bible`
- **Thin ending** — single consequence sentence; no punishment → collective response → next war/reform step
- **No narrator wrap** — film ends on character witness or aftermath only; viewer never gets recap / hook payoff

## Portable runner

Default **`--phase stills`**. Full human-in-the-loop flow:

```bash
mkdir -p output/verticals/interactive-explainer/my-explainer/{stills,clips,audio}
cp guides/workflows/verticals/interactive-explainer/templates/explainer-plan.template.json \
   output/verticals/interactive-explainer/my-explainer/plan.json

# Phase A — stills (default)
python3 guides/workflows/verticals/interactive-explainer/scripts/run_from_plan.py \
  --plan output/verticals/interactive-explainer/my-explainer/plan.json \
  --out-dir output/verticals/interactive-explainer/my-explainer

# Phase A2 — narration TTS (after user approves stills)
python3 guides/workflows/verticals/interactive-explainer/scripts/run_from_plan.py \
  --plan output/verticals/interactive-explainer/my-explainer/plan.json \
  --out-dir output/verticals/interactive-explainer/my-explainer \
  --approve-stills --phase tts

# Phase B — video (paid)
python3 guides/workflows/verticals/interactive-explainer/scripts/run_from_plan.py \
  --plan output/verticals/interactive-explainer/my-explainer/plan.json \
  --out-dir output/verticals/interactive-explainer/my-explainer \
  --phase video

# Phase C + D — concat + optional bed (after user approves clips)
python3 guides/workflows/verticals/interactive-explainer/scripts/run_from_plan.py \
  --plan output/verticals/interactive-explainer/my-explainer/plan.json \
  --out-dir output/verticals/interactive-explainer/my-explainer \
  --approve-clips --phase assemble --final-name my_explainer_final.mp4
```

One-shot (automation only): `--phase all --yes-skip-stills-gate --yes-skip-clips-gate`.

Flags: `--phase stills|tts|video|assemble|all` · `--approve-stills` · `--approve-clips` · `--assemble-only` · `--only SCENE_ID` · `--regen-stills` · `--regen-tts` · `--regen-clips` · `--skip-assembly` · `--skip-narration-check`

Requires `PRUNA_API_KEY`; optional bed needs `REPLICATE_API_TOKEN`.

## Related

- Narrator-only: [multi-scene-ai-video](../../core/narrated-multi-scene/SKILL.md)
- Visual transitions (no VO): [scene-transition-video](../../core/visual-transition-reel/SKILL.md)
- Hub: [pruna-generative-pipeline](../pruna-generative-pipeline/SKILL.md) (Recipe R)
- Example prompts: [examples/workflows/verticals/interactive-explainer/example-prompt.md](../../../../examples/workflows/verticals/interactive-explainer/example-prompt.md)
- Example plans (local workspace): `output/verticals/interactive-explainer/<project-slug>/plan.json` — see [output/README.md](../../../../output/README.md)
