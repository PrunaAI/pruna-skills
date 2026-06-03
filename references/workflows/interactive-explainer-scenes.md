# Educational explainer scenes (narrator + character)

Canonical pattern for **educational shorts** — history, science, nature, how-it-works, children's topics — that **alternate host narration with in-story character speech**. Not wall-to-wall voice-over.

Related: [scene-anchor-triple.md](../video/scene-anchor-triple.md) (narrator beats) · [multi-scene-avatar-video](../guides/workflows/core/avatar-multi-scene/SKILL.md) (character beats) · [interactive-explainer](../guides/workflows/verticals/interactive-explainer/SKILL.md)

## Why hybrid?

Pure narration over B-roll feels like a lecture. **Interaction** — host poses a question, an expert or witness responds, host synthesizes — reads like a prestige documentary, science show, or engaging classroom film.

| Beat type | Model | Audio | Stills |
|-----------|-------|-------|--------|
| **`narrator`** | `p-video` | Gemini TTS → `input.audio` | start + end (`p-image-edit`) |
| **`character`** | `p-video-avatar` | native `voice_script` | start only (mouth visible) |

Both use **`p-image`** hero + **`p-image-edit`** under one **`style_bible`**.

**Format defaults:** `1080p`, `48` fps (narrator `p-video`); motion: [educational-explainer-motion.md](./interactive-explainer-motion.md) — dynamic OPEN/MID/CLOSE, physics-safe.

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
| Narrator line length | **≤ ~19s** TTS (P-API 20s audio-led cap) — see [scene-anchor-triple.md](../video/scene-anchor-triple.md) |
| Character line length | Short reply (1–3 sentences); avatar clip follows script length |

## Narrator beat (`type: "narrator"`)

Scene anchor **triple** — same as [scene-anchor-triple.md](../video/scene-anchor-triple.md):

```json
{
  "id": "02_how_it_works",
  "type": "narrator",
  "edit_prompt": "OPENING: Wide cross-section diagram of a volcano, educational documentary still, clear focal subject…",
  "last_frame_edit_prompt": "CLOSING: Same volcano, closer on magma chamber glow, educational end frame…",
  "video_prompt": "OPEN: hold wide diagram. MID: slow push toward chamber glow, heat shimmer. CLOSE: settle on glowing core."
}
```

Narration line in `narration.scene_lines.{id}`.  
**End with a question** when the next scene is a character reply.

## Character beat (`type: "character"`)

Talking-head beat — **`p-video-avatar`**:

```json
{
  "id": "03_geologist_speaks",
  "type": "character",
  "cast": "field_geologist",
  "follows": "02_how_it_works",
  "edit_prompt": "Same educational style, head-and-shoulders, slight angle from the side, lips in frame, volcanic landscape background",
  "video_prompt": "Medium close-up, speaks directly to camera, subtle push-in, enthusiastic expert tone"
}
```

`voice_script` on the scene row or in plan `voice_scripts`:

```json
"voice_scripts": {
  "03_geologist_speaks": "I've stood on active vents where the ground was warm under my boots. Pressure builds for decades — then the earth reminds you who's in charge."
}
```

**No** `last_frame_edit_prompt` on character rows — avatar uses one still.

### Cast ledger

```json
"cast": {
  "field_geologist": {
    "name": "Dr. Elena Reyes",
    "persona_gender": "female",
    "voice": "Zephyr (Female)",
    "voice_language": "English (US)",
    "voice_prompt": "Enthusiastic field scientist, clear lip sync, first-person expert, accessible not academic",
    "character_descriptor": "woman, Latina geologist, 40s, field gear, documentary realism"
  }
}
```

**Gender ↔ voice:** set `persona_gender` to `female` or `male`; runner maps to `Zephyr (Female)` or `Puck (Male)`. `character_descriptor` must name the same gender so the still matches the voice.

**Still prompts:** positive single-frame wording in `hero_prompt` / `edit_prompt` / `last_frame_edit_prompt` — no `split`, `labeled`, `side by side`, or `no text` in still lines (use `style_bible` for negations). Character stills: **slight angle**, lips in frame — not `facing camera` (save on-camera delivery for `video_prompt`). See [p-video-replace-comparison/SKILL.md](../guides/workflows/launches/p-video-replace-comparison/SKILL.md) trigger table.

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

### History (Ancaster pattern — preferred)

Single incident, full arc. Narrator = facts; character = witness.

| # | Type | Function | Example |
|---|------|----------|---------|
| 1 | narrator | Hook + stakes | "On June third, eighteen twenty-six, that somewhere was Ancaster. Who was George Rolph?" |
| 2 | character | Witness identity | "I was clerk of the peace — close to the Tories, but I refused their galas." |
| 3 | narrator | Escalation | "That night, men gathered at Dr. Hamilton's house. What happened when they reached his bed?" |
| 4 | character | Event witness | "They dragged me from my bed into a field. I knew every man in that mob." |
| 5 | narrator | Consequence + question | "The jury awarded twenty pounds. Was that justice?" |
| 6 | character | Emotional / moral reply | "Witnesses looked at the floor and said nothing." |
| 7 | narrator | Legacy turn | "In eighteen twenty-eight, Reformers broke the Tory majority." |
| 8 | character | Closing witness | "No one went to prison. But the farmers remembered." |

Reference plan: `output/verticals/interactive-explainer/ancaster-explainer/plan.json`

### History (biography — narrow the through-line)

Do **not** survey a whole life. Pick one question, e.g. *Why did France put her in the Panthéon before America ever fully claimed her?*

| # | Type | Function |
|---|------|----------|
| 1 | narrator | Hook — one country, one wound |
| 2 | character | Witness — specific memory, not slogan |
| … | alternate | Each beat = one chapter of **that** arc only |

**Anti-pattern:** St. Louis → Harlem → Paris → Folies → spy → march → Rainbow Tribe → Panthéon in nine scenes.

## Stand-alone test

Every explainer must answer **yes** to all five before render:

| # | Question | Ancaster example |
|---|----------|------------------|
| 1 | **Stakes** — what could be lost? | Rolph's body, reputation, safety; rule of law |
| 2 | **Conflict** — who opposed whom? | Family Compact vs reform-minded clerk |
| 3 | **Turn** — what changed? | Mob violence → failed suit → 1828 reform victory |
| 4 | **Nuance** — complication, not hagiography? | Rolph was Tory-adjacent; witnesses stayed silent; £20 verdict |
| 5 | **Closure** — outcome clear without Wikipedia? | No prison, but farmers remembered and broke the majority |

**Biography trap:** covering birth → fame → war → activism → death in one short. Each beat becomes a slogan; nothing lands. **Fix:** one through-line (e.g. *Why did France honor a woman America refused?*) with the same witness/fact split as Ancaster.

## Narrator vs character (labor split)

| Narrator says | Character says |
|---------------|----------------|
| Dates, places, names, sequence | "I" witness, sensory detail, emotion |
| "The jury awarded twenty pounds. Was that justice?" | "Witnesses looked at the floor. Twenty pounds — a slap on the wrist." |
| Sets up **one** question per handoff | Answers **that** question — not a new topic |

**Bad character line:** "I learned to dance toward my dreams."  
**Good character line:** "They dragged me from my bed. Tar first — feathers from my own pillow."

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

Runner: [`run_from_plan.py`](../guides/workflows/verticals/interactive-explainer/scripts/run_from_plan.py)

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

- [interactive-explainer](../guides/workflows/verticals/interactive-explainer/SKILL.md) — primary workflow
- [multi-scene-ai-video](../guides/workflows/core/narrated-multi-scene/SKILL.md) — narrator-only fallback
- [multi-scene-avatar-video](../guides/workflows/core/avatar-multi-scene/SKILL.md) — character-only pieces
