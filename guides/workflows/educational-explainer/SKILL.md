---
name: educational-explainer
description: Builds educational short films — history, science, nature, how-it-works, children's topics — that alternate narrator p-video beats (scene anchor triple + Gemini TTS) with in-story character dialogue via p-video-avatar. p-image hero, p-image-edit stills, assembly with optional bed. Use for any explainer where the host interacts with experts, witnesses, or characters instead of pure voice-over.
metadata:
  version: "0.0.3"
---

# Educational explainer (narrator + character interaction)

**Not** wall-to-wall narration. Alternate **host / narrator VO** (`p-video` + TTS) with **people in the story speaking** (`p-video-avatar` + `voice_script`) — historians, scientists, witnesses, animated guides, etc.

Canonical scene patterns: [educational-explainer-scenes.md](../../../references/educational-explainer-scenes.md)  
Motion (dynamic, physics-safe): [educational-explainer-motion.md](../../../references/educational-explainer-motion.md)  
Narrator triple spec: [scene-anchor-triple.md](../../../references/scene-anchor-triple.md)

See [p-video](../../../tools/video/p-video/SKILL.md), [p-video-avatar](../../../tools/video/p-video-avatar/SKILL.md), [p-image](../../../tools/image/p-image/SKILL.md), [p-image-edit](../../../tools/image/p-image-edit/SKILL.md), [gemini-3.1-flash-tts](../../../tools/audio/gemini-3.1-flash-tts/SKILL.md).

For **narrator-only** explainers, use [multi-scene-ai-video](../core/narrated-multi-scene/SKILL.md) instead.

> **Canonical workflow:** [interactive-explainer](../verticals/interactive-explainer/SKILL.md) — same pipeline with staged gates (`--phase stills` default). Use that skill for new projects.

## Subject flavors (pick one `style_bible`)

| Flavor | Visual style | Character examples |
|--------|--------------|-------------------|
| **History / biography** | Photoreal biopic, period film stills | Historical figure, witness, activist |
| **Science / cosmos** | Cinematic space/nature, painterly realism | Scientist, astronaut, field researcher |
| **How-it-works** | Clean documentary B-roll, diagram-friendly | Engineer, inventor, technician |
| **Nature / wildlife** | National Geographic tone, golden hour | Ranger, marine biologist, local guide |
| **Children's educational** | Warm illustrated or soft 3D, friendly | Curious kid, friendly animal guide, teacher |

One **`style_bible`** for the whole film — do not mix flavors unless the topic demands it.

## Defaults (1080p / 48 fps)

Every plan should set:

```json
"defaults": {
  "resolution": "1080p",
  "fps": 48,
  "aspect_ratio": "16:9"
}
```

- **`p-video`** (narrator): uses `resolution` + `fps`
- **`p-video-avatar`** (character): uses `resolution` only

Template: [`explainer-plan.template.json`](templates/explainer-plan.template.json)

## Motion (dynamic, physics-safe)

Every scene needs **visible motion** — but not physics-heavy action. See [educational-explainer-motion.md](../../../references/educational-explainer-motion.md).

| Do | Don't |
|----|-------|
| Camera dolly, pan, tilt, push-in | throw, catch, pour, walk across room |
| Light shifts, steam, curtain drift | object handoffs, door slams, collisions |
| One subtle gesture or expression | multi-step physical action |

Write **`video_prompt`** as `OPEN:` → `MID:` (attention hook) → `CLOSE:` (settle on end still). At 48 fps, keep camera moves **slow and deliberate**.

## Intake: ask before generating

| Topic | Questions |
|-------|-----------|
| **Topic** | What should the viewer learn? Key facts or story beats? |
| **Audience** | Kids, general public, enthusiast? Sets tone and vocabulary |
| **Flavor** | History? Science? Nature? How-it-works? Illustrated? |
| **Speakers** | Who should **speak** on camera — expert, witness, character, subject? |
| **Interaction mix** | Target **≥ 35% character beats** — who speaks, in what order? |
| **Narrator** | Gemini TTS `voice` + `style_prompt` (clear, engaging host) |
| **Cast** | Per speaker: **`persona_gender`** (`female` / `male`), Pruna `voice` (must match gender), `voice_prompt`, **`character_descriptor`** (gendered look), `style_bible` |
| **Per narrator scene** | `edit_prompt`, `last_frame_edit_prompt`, **`video_prompt`** (OPEN/MID/CLOSE, physics-safe motion), line **≤ ~19s** |
| **Per character scene** | `edit_prompt` (lips in frame, slight angle), **`video_prompt`** (push-in / light shift — no plot action), `voice_script` |
| **Assembly** | Optional bed? Crossfades? |

Draft the **full scene table** as a dialogue arc before any API calls. Confirm with user.

**Story depth bar (required before render):** The film must pass the [stand-alone test](./educational-explainer-scenes.md#stand-alone-test). If the story is a biography, pick **one through-line** — not a life survey. Reference quality: `output/ancaster-explainer/plan.json`.

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

Gemini TTS for **`narrator`** rows only. Probe duration; keep **≤ ~19s** per scene ([`validate_narration_duration`](../../_shared/scripts/p_video_payload.py)).

### Phase 4 — Video (parallel)

- **`narrator`:** `build_p_video_payload` with `image` + `last_frame_image` + `audio`, `save_audio: true`
- **`character`:** `p-video-avatar` with still URL + `voice_script` + cast voice fields + `video_prompt`. Runner **prepends `character_descriptor`** to character `edit_prompt` and sets **`voice` from `persona_gender`** (`female` → `Zephyr (Female)`, `male` → `Puck (Male)`).

Pass `project_seed` to avatar clips when locking motion.

### Still prompts: avoid trigger words

`hero_prompt`, `edit_prompt`, and `last_frame_edit_prompt` are **`p-image` / `p-image-edit` stills** — use **positive single-frame wording only**. Put negations (`no text`, `no laptops`) in **`style_bible`** at plan root, not in still lines.

| Risk | Avoid in stills | Use instead |
|------|-----------------|-------------|
| Text overlays | `labeled`, `graphic tee`, signage | unbranded jars, solid fabrics |
| Multi-panel | `split`, `side by side`, `comparison`, `grid`, `collage` | one subject, one frame |
| Lip-sync still bugs | `facing camera`, `to camera`, `ready to speak` in **character** stills | slight angle from the side, lips in frame |
| Weather glitches | `rain`, `wet pavement`, `no rain` | sunny window, golden afternoon |

Full table: [p-video-replace-comparison/SKILL.md](../p-video-replace-comparison/SKILL.md) **Prompt trigger words**. The runner **errors** on common triggers before any API call.

### Avatar gender ↔ voice lock

Every `cast` entry used on character rows **must** include:

```json
"persona_gender": "female",
"voice": "Zephyr (Female)",
"character_descriptor": "woman, …"
```

Optional per-scene override: `"persona_gender": "male"` on a character row. Descriptor must name the same gender (woman/female or man/male) so the generated face matches the voice.

### Phase 5 — Assembly

Normalize clip audio → concat → optional [stable-audio-2.5](../../../tools/audio/stable-audio-2.5/SKILL.md) bed.

## Scripting rules

### Narrator carries facts; character carries witness

Split labor like a prestige documentary — **not** two voices saying the same summary.

| Voice | Job | Good | Bad |
|-------|-----|------|-----|
| **Narrator** | Context, dates, names, stakes, the question | "Ten months later, Rolph sued. The jury awarded twenty pounds. Was that justice?" | "She was amazing and did many things." |
| **Character** | First-person reply to the **specific** prior question | "Witnesses looked at the floor and said nothing. Twenty pounds — a slap on the wrist." | "I always believed in myself and danced toward my dreams." |

### One through-line per film

Pick **one question** the whole short answers. Ancaster: *Can power punish without consequence?* Josephine (good): *Why did France honor a woman America refused?*

**Anti-pattern:** biographical survey — St. Louis, then Harlem, then Paris, then war, then civil rights, then legacy in nine rushed beats. Each beat gets a slogan instead of a scene.

**Fix:** narrow scope, or add scenes — never cram two chapters into one narrator row or one visual.

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
- Use `follows` in plan; see [multi-scene-avatar-video/prompt-templates.md](../multi-scene-avatar-video/prompt-templates.md)

**Anti-patterns:**
- All-narrator tables (lecture, not a conversation)
- Character lines in `narration.scene_lines` (wrong voice pipeline)
- Gemini TTS voice names on `p-video-avatar` (use Pruna voices)
- Missing **lips in frame** on character stills; **facing camera** in character still prompts (use `video_prompt` for on-camera delivery)
- Missing **`persona_gender`** on cast / voice not matching generated avatar gender
- Still-prompt **trigger words** (`split`, `labeled`, `side by side`, negations like `no text` in still lines)
- Biographical survey cramming (Josephine-style) vs single through-line (Ancaster-style)
- Motivational character lines ("dance toward your dreams") instead of witness detail
- Narrator rows that combine two visual chapters (e.g. Folies Bergère + WWII in one scene)
- Static `video_prompt` (`OPEN: hold. CLOSE: hold.`) — always add a MID motion beat
- Physics-trap motion (throwing, pouring, walking, prop handoffs) — see [educational-explainer-motion.md](../../../references/educational-explainer-motion.md)
- `720p` / `24` fps unless user explicitly requests draft quality

## Portable runner

```bash
mkdir -p output/my-explainer/{stills,clips,audio}
cp guides/workflows/educational-explainer/templates/explainer-plan.template.json \
   output/my-explainer/plan.json

python3 guides/workflows/educational-explainer/scripts/run_from_plan.py \
  --plan output/my-explainer/plan.json \
  --out-dir output/my-explainer \
  --final-name my_explainer_final.mp4
```

Flags: `--only SCENE_ID` · `--regen-stills` · `--regen-tts` · `--regen-clips` · `--skip-assembly` · `--skip-narration-check`

Requires `PRUNA_API_KEY`; optional bed needs `REPLICATE_API_TOKEN`.

## Related

- Narrator-only: [multi-scene-ai-video](../multi-scene-ai-video/SKILL.md)
- Visual transitions (no VO): [scene-transition-video](../scene-transition-video/SKILL.md)
- Hub: [pruna-generative-pipeline](../pruna-generative-pipeline/SKILL.md) (Recipe R)
- Example: [examples/workflows/educational-explainer/example-prompt.md](../../../examples/workflows/educational-explainer/example-prompt.md)
- Gold-standard plan (history, witness dialogue): `output/ancaster-explainer/plan.json`
