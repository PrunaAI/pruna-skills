# Educational explainer scenes (narrator + character)

Canonical pattern for **educational shorts** — history, science, nature, how-it-works, children's topics — that **alternate host narration with in-story character speech**. Not wall-to-wall voice-over.

Related: [scene-anchor-triple.md](../video/scene-anchor-triple.md) (narrator beats) · [multi-scene-avatar-video](../workflows/core/avatar-multi-scene/SKILL.md) (character beats) · [interactive-explainer](../workflows/verticals/interactive-explainer/SKILL.md)

## Why hybrid?

Pure narration over B-roll feels like a lecture. **Interaction** — host poses a question, an expert or witness responds, host synthesizes — reads like a prestige documentary, science show, or engaging classroom film.

| Beat type | Model | Audio | Stills |
|-----------|-------|-------|--------|
| **`narrator`** | `p-video` | Gemini TTS → `input.audio` | start + end (`p-image-edit`) |
| **`character`** | `p-video-avatar` | native `voice_script` | start only (mouth visible) |

Both use **`p-image`** hero + **`p-image-edit`** under one **`style_bible`**.

**Format defaults:** `720p`, `24` fps (narrator `p-video`); motion: [interactive-explainer-motion.md](./interactive-explainer-motion.md) — dynamic OPEN/MID/CLOSE, physics-safe.

## Subject flavors

| Flavor | Narrator role | Character role | Visual `style_bible` |
|--------|---------------|----------------|----------------------|
| History / biography | Documentary host | Historical figure, witness | Photoreal period / biopic |
| Science / cosmos | Science communicator | Researcher, astronaut | Cinematic space/nature realism |
| How-it-works | Explainer host | Engineer, inventor | Clean documentary B-roll |
| Nature | Nature narrator | Ranger, biologist | National Geographic tone |
| Children's | Friendly teacher voice | Kid, animal guide, mascot | Warm illustration or soft 3D |

Pick **one** flavor per film. Swap examples in prompts — the scene machinery is identical.

## Target mix

| Guideline | Target |
|-----------|--------|
| Character / narrator ratio | **≥ 1 character beat per 2 narrator beats** (roughly 35–50% character) |
| Scene order | Alternate when possible: narrator → character → narrator → … |
| Narrator line length | **≤ ~19s** TTS (P-API 20s **audio-led `p-video`** cap) — see [scene-anchor-triple.md](../video/scene-anchor-triple.md) |
| Character line length | Reply length as needed (often 2–4 sentences); **`p-video-avatar` may exceed 20s** — clip follows `voice_script` |

## Narrator beat (`type: "narrator"`)

Scene anchor **triple** — same as [scene-anchor-triple.md](../video/scene-anchor-triple.md):

```json
{
  "id": "02_mechanism",
  "type": "narrator",
  "edit_prompt": "OPENING: Wide view of subject in context, clear focal subject, single frame…",
  "last_frame_edit_prompt": "CLOSING: Same subject, closer on key detail, closing composition…",
  "video_prompt": "OPEN: hold wide. MID: slow push toward detail, steady daylight. CLOSE: settle on end frame."
}
```

Narration line in `narration.scene_lines.{id}`.  
**End with a question** when the next scene is a character reply.

## Character beat (`type: "character"`)

Talking-head beat — **`p-video-avatar`**:

```json
{
  "id": "03_expert_reply",
  "type": "character",
  "cast": "expert",
  "still_from": "02_prior_expert_scene",
  "follows": "02_mechanism",
  "edit_prompt": "Same cast member dominates head-and-shoulders frame, slight angle, lips in frame, topic-appropriate background",
  "video_prompt": "Single continuous medium close-up, one very slow push-in, speaks directly to camera, steady light, no gestures."
}
```

`voice_script` on the scene row or in plan `voice_scripts`:

```json
"voice_scripts": {
  "03_expert_reply": "First-person reply that answers the narrator's exact question — concrete detail, not a slogan."
}
```

**No** `last_frame_edit_prompt` on character rows — avatar uses one still.

### Cast ledger

```json
"cast": {
  "expert": {
    "name": "Dr. Example Name",
    "persona_gender": "female",
    "voice": "Zephyr (Female)",
    "voice_language": "English (US)",
    "voice_prompt": "First-person expert, clear lip sync, accessible not academic",
    "character_descriptor": "woman, role-appropriate look matching style_bible"
  }
}
```

**Gender ↔ voice:** set `persona_gender` to `female` or `male`; runner maps to `Zephyr (Female)` or `Puck (Male)`. `character_descriptor` must name the same gender so the still matches the voice.

**Still prompts:** **positive only** in `style_bible`, still lines, and `video_prompt` — never `no …`, `avoid …`, or `not …` in creative fields (spoken dialogue may use natural negation). Full blocked-phrase tables: [interactive-explainer-prompts.md](./interactive-explainer-prompts.md).

Use **Pruna avatar voices** (`Zephyr (Female)`, `Puck (Male)`, etc.) — not Gemini TTS voice names.

## Dialogue scripting (interaction)

Write the scene table as a **conversation arc**. Examples by flavor:

### Science

| # | Type | Function | Example |
|---|------|----------|---------|
| 1 | narrator | Hook | "What happens when a star runs out of fuel?" |
| 2 | character | Expert reply | "The core collapses in seconds. What looked stable for billions of years ends in a flash." |
| 3 | narrator | Context | "That collapse can outshine an entire galaxy." |
| 4 | character | Wonder beat | "The first time I saw a supernova remnant, I stopped calculating — I just stared." |

### History (single incident — preferred)

One through-line, full arc. Narrator = facts; character = witness.

| # | Type | Function |
|---|------|----------|
| 1 | narrator | Hook + stakes — date, place, named question |
| 2 | character | Witness identity — first person, specific angle |
| 3 | narrator | Escalation — what happened next, question for witness |
| 4 | character | Event witness — sensory or procedural detail |
| 5 | narrator | Consequence + question |
| 6 | character | Moral or emotional reply |
| 7+ | narrator / character | Legacy or aftermath as needed |

### History (biography — narrow the through-line)

Do **not** survey a whole life. Pick **one question** the film answers.

| # | Type | Function |
|---|------|----------|
| 1 | narrator | Hook — one wound or paradox |
| 2 | character | Witness — specific memory, not slogan |
| … | alternate | Each beat = one chapter of **that** arc only |

**Anti-pattern:** many life eras or locations in one short — each beat becomes a slogan.

## Stand-alone test

Every explainer must answer **yes** to all five before render:

| # | Question |
|---|----------|
| 1 | **Stakes** — what could be lost? |
| 2 | **Conflict** — who opposed whom? |
| 3 | **Turn** — what changed after the key event? |
| 4 | **Nuance** — at least one complication (not hagiography)? |
| 5 | **Closure** — outcome clear without outside reading? |

**Biography trap:** covering birth → fame → war → activism → death in one short. **Fix:** one through-line with the same witness/fact split as a single-incident history film.

## Narrator vs character (labor split)

| Narrator says | Character says |
|---------------|----------------|
| Dates, places, names, sequence | "I" witness, sensory detail, emotion |
| Concrete fact, then one pointed question | Reply that answers **that** question only |
| Sets up **one** question per handoff | Does not introduce a new topic or slogan |

**Bad character line:** motivational poster copy, unrelated to the question.  
**Good character line:** procedural or sensory detail tied to the prior narrator beat.

## Causal chain (event explainers)

Do not open on the climax. Map beats before render:

| Beat (minimum) | Narrator carries |
|----------------|------------------|
| **Stakes / hook** | Why anyone cared |
| **Mechanism** | Law, policy, or force that caused the crisis |
| **Local complication** | Why *this* place or group differed |
| **Deadline / trigger** | Clock or last chance before the act |
| **Act** | What people did (narrator B-roll) |
| **Response** | Authority's punishment or counter-move |
| **Aftermath** | How the story continued |

## Visual–audio alignment

| Rule | Good | Bad |
|------|------|-----|
| **Narrator B-roll** matches VO | Meeting hall while VO describes the meeting | Generic exterior for a named interior action |
| **Character still** matches witness setting | Witness at the wharf while discussing ships | Unrelated interior while VO discusses the wharf |
| **Events on narrator rows** | Destruction / trial on `type: narrator` | Event in VO but only talking head on screen |

## Visual mode (lock one look)

| Mode | `style_bible` vocabulary |
|------|--------------------------|
| **Photoreal period** | `photoreal period drama film still`, natural skin, period wardrobe |
| **Painterly / storybook** | `premium painterly historical illustration`, soft ink outlines |
| **Children's illustrated** | warm illustrated or soft 3D, friendly proportions |

Do not mix photoreal and painterly vocabulary in the same film.

## Ending closure bar

**Three-beat close** (history / biography / causal-chain):

| Order | Row | Job |
|-------|-----|-----|
| 1 | **Narrator aftermath** | Punishment, collective response, dated next step (≥ 3 facts) |
| 2 | **Character witness** | First-person line tied to aftermath — not a slogan |
| 3 | **`NN_wrap` narrator** | Recap: cause → act → consequence → legacy; answer the hook; no question to character |

Science / how-it-works may end **narrator-only** after the expert (`07_conclusion` pattern).

Example plans: `output/verticals/interactive-explainer/<project-slug>/plan.json`.

## Visual continuity

- One **`style_bible`** on every still and motion prompt.
- **Narrator beats:** wider compositions, Ken Burns motion, environment / diagram storytelling.
- **Character beats:** head-and-shoulders, **slight angle**, **lips in frame**; match lighting when `follows` is set. On-camera motion lives in `video_prompt`, not still `edit_prompt`.
- Do not mix unrelated aesthetics unless the topic demands it.

## Assembly

1. Render **all** narrator + character clips in scene order.
2. **Normalize** audio (48 kHz stereo) before concat if mixing avatar + p-video clips.
3. **Concat** with hard cuts (default) or short crossfades on `chain_from_previous`.
4. Optional **Stable Audio** bed under dialogue (~0.08–0.10).

Runner: [`run_from_plan.py`](../workflows/verticals/interactive-explainer/scripts/run_from_plan.py)

## Plan JSON skeleton

```json
{
  "title": "Topic — Educational Short",
  "hero_prompt": "…",
  "style_bible": "…",
  "narration": {
    "voice": "Charon",
    "style_prompt": "Engaging educational host…",
    "max_seconds_per_scene": 19,
    "scene_lines": { "01_hook": "…" }
  },
  "cast": {
    "expert": { "voice": "Zephyr (Female)", "voice_prompt": "…" }
  },
  "voice_scripts": {
    "02_expert_speaks": "First-person line…"
  },
  "scenes": [
    { "id": "01_hook", "type": "narrator", "edit_prompt": "…", "last_frame_edit_prompt": "…", "video_prompt": "…" },
    { "id": "02_expert_speaks", "type": "character", "cast": "expert", "edit_prompt": "… mouth visible …", "video_prompt": "…" }
  ]
}
```

## Workflows

- [interactive-explainer](../workflows/verticals/interactive-explainer/SKILL.md) — primary workflow
- [multi-scene-ai-video](../workflows/core/narrated-multi-scene/SKILL.md) — narrator-only fallback
- [multi-scene-avatar-video](../workflows/core/avatar-multi-scene/SKILL.md) — character-only pieces
