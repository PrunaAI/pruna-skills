---
name: interactive-explainer
description: Use when someone wants an educational explainer with a host and characters — history or science shorts with dialogue, not voiceover-only B-roll.
license: MIT
metadata:
  version: "1.0.6"
depends:
  - p-image
  - p-image-edit
  - p-video
  - p-video-avatar
  - gemini-3.1-flash-tts
  - stable-audio-2.5
---

## Shared generation policy

<!-- shared-generation-policy -->

Before any paid `POST /v1/predictions`:

1. **[Random seed ritual](./references/random-seed-ritual.md)** — always first; derive axes via sum-mod.
2. **[Generation diversity](./references/generation-diversity.md)** — explicit prompts; rotate ≥2 scenario axes per session.
3. **[Quality checklists](./references/generation-quality-checklists.md)** — open output files and judge pass/fail before advancing.
4. **[Staged generation gate](./references/staged-generation-gate.md)** — plan → stills → audio → video → assembly; never skip phases in one turn.
5. **[Approval red flags](./references/approval-red-flags.md)** — pause when plan, stills, or clips were not reviewed.
6. **[Workflow feedback gates](./references/workflow-feedback-gates.md)** — runner flags and per-workflow commands.
7. **[Parallel execution](./references/parallel-execution.md)** — async fan-out within each approved phase only.

# Educational explainer (narrator + character interaction)

**Not** wall-to-wall narration. Alternate **host / narrator VO** (`p-video` + TTS) with **people in the story speaking** (`p-video-avatar` + `voice_script`) — historians, scientists, witnesses, animated guides, etc.

Canonical scene patterns: [interactive-explainer-scenes.md](./references/interactive-explainer-scenes.md)  
Motion (dynamic, physics-safe): [interactive-explainer-motion.md](./references/interactive-explainer-motion.md)  
Narrator triple spec: [scene-anchor-triple.md](./references/scene-anchor-triple.md)

See [p-video](../../../../tools/video/p-video/SKILL.md), [p-video-avatar](../../../../tools/video/p-video-avatar/SKILL.md), [p-image](../../../../tools/image/p-image/SKILL.md), [p-image-edit](../../../../tools/image/p-image-edit/SKILL.md), [gemini-3.1-flash-tts](../../../../tools/audio/gemini-3.1-flash-tts/SKILL.md).

For **narrator-only** explainers, use [narrated-multi-scene](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/narrated-multi-scene/skills/narrated-multi-scene/SKILL.md) instead.

**Staged generation:** [staged-generation-gate.md](https://github.com/PrunaAI/pruna-skills/tree/main/references/policies/staged-generation-gate.md) — approve plan → stills → narration TTS → video clips → assembly + bed. Default runner phase is **`stills`**.

## Quick reference

| Resource | Path |
|----------|------|
| Positive prompts / blocked phrases | [interactive-explainer-prompts.md](./references/interactive-explainer-prompts.md) |
| Scene patterns & stand-alone test | [interactive-explainer-scenes.md](./references/interactive-explainer-scenes.md) |
| Motion (OPEN/MID/CLOSE) | [interactive-explainer-motion.md](./references/interactive-explainer-motion.md) |
| Feedback discipline | [requesting-generation-feedback](https://github.com/PrunaAI/pruna-skills/tree/main/router/references/policies/approval-red-flags.md) |
| Runner | [`run_from_plan.py`](scripts/run_from_plan.py) · `--phase stills\|tts\|video\|assemble` · `--approve-stills` · `--approve-clips` |
| Plan template | [`explainer-plan.template.json`](templates/explainer-plan.template.json) |

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

Every scene needs **visible motion** — but not physics-heavy action. See [interactive-explainer-motion.md](./references/interactive-explainer-motion.md).

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

**Story depth bar (required before render):** The film must pass the [stand-alone test](./references/interactive-explainer-scenes.md#stand-alone-test). If the story is a biography, pick **one through-line** — not a life survey.

## Feedback gates (required)

| Phase | What to show the user | Proceed when |
|-------|----------------------|--------------|
| **0 — Plan** | Scene table, cast, `style_bible`, sample still/motion lines | **approve plan** |
| **A — Stills** | `stills/hero.png`, scene start/end PNGs | **approve stills** |
| **A2 — TTS** | `audio/narration_*.mp3` — listen for pace and length | Lines OK → **phase video** |
| **B — Video** | `clips/*.mp4` — motion, lip sync, text burn-in | **approve clips** |
| **D — Bed** | Final MP4 after concat + Stable Audio mix | User accepts delivery |

Ask when art direction is unclear (visual mode, cast continuity, narrator vs character mix, bed yes/no) — see [staged-generation-gate.md](https://github.com/PrunaAI/pruna-skills/tree/main/references/policies/staged-generation-gate.md).

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

| Phase | Action |
|-------|--------|
| **0** | `p-image` hero (+ optional `_cast_*` anchor stills from `anchor_still_prompt`) |
| **1** | Parallel `p-image-edit` start stills (all scenes) |
| **2** | Parallel end stills (**narrator** only) |
| **A2** | Parallel Gemini TTS (**narrator** only, ≤ ~19s per line) |
| **B** | Parallel `p-video` triples + `p-video-avatar` (avatar may exceed 20s) |
| **C/D** | Concat ± [stable-audio-2.5](../../../../tools/audio/stable-audio-2.5/SKILL.md) bed |

**Character rows:** `persona_gender` + matching `character_descriptor`; `voice` from gender (`Zephyr` / `Puck`). Use `still_from` or `_cast_*` when hero is B-roll/objects. Avatar text suppression: positive stills + default `avatar_negative_prompt` token list — [interactive-explainer-prompts.md](./references/interactive-explainer-prompts.md).

**Assembly:** optional crossfades via `assembly.hard_cut_crossfade_seconds`; `still_from_end` for bookend narrator rows. Re-run `--assemble-only` to fix concat without regen video.

## Scripting rules

Dialogue arc, stand-alone test, causal chain, visual–audio alignment, visual modes, and three-beat ending: **[interactive-explainer-scenes.md](./references/interactive-explainer-scenes.md)**.

**Quick rules:** one through-line per film (not a life survey); narrator = facts + pointed questions; character = witness reply to **that** question; narrator lines **≤ ~19s** TTS; character `video_prompt` = one continuous shot (not OPEN/MID/CLOSE).

## Common mistakes

**Anti-patterns:**
- All-narrator tables (lecture, not a conversation)
- Character lines in `narration.scene_lines` (wrong voice pipeline)
- Gemini TTS voice names on `p-video-avatar` (use Pruna voices)
- Missing **lips in frame** on character stills; **facing camera** in character still prompts (use `video_prompt` for on-camera delivery)
- Missing **`persona_gender`** on cast / voice not matching generated avatar gender
- **Negative or avoidance prompts** — `no …`, `avoid …`, `not …` in stills, `style_bible`, or `video_prompt`; use explicit positive props and surfaces instead
- Still-prompt **blocked substrings** — see [interactive-explainer-prompts.md](./references/interactive-explainer-prompts.md)
- Biographical life-survey cramming vs single through-line
- Motivational character lines instead of witness detail
- Narrator rows that combine two visual chapters in one still
- Static `video_prompt` (`OPEN: hold. CLOSE: hold.`) — always add a MID motion beat
- Physics-trap motion (throwing, pouring, walking, prop handoffs) — see [interactive-explainer-motion.md](./references/interactive-explainer-motion.md)
- `720p` / `24` fps unless user explicitly requests draft quality
- **Missing causal chain** — climax without prerequisite beats (mechanism, local standoff, deadline)
- **Visual–audio mismatch** — character interior while narration describes harbor, ships, or courts
- **Visual mode mismatch** — `photoreal` still lines under a storybook `style_bible`, or `painterly` / `illustration` lines under a photoreal `style_bible`
- **Thin ending** — single consequence sentence; no punishment → collective response → next war/reform step
- **No narrator wrap** — film ends on character witness or aftermath only; viewer never gets recap / hook payoff

## Portable runner

Default **`--phase stills`**. Phased commands: [workflow-feedback-gates.md](./references/workflow-feedback-gates.md) **Interactive explainer**.

Flags: `--phase stills|tts|video|assemble|all` · `--approve-stills` · `--approve-clips` · `--assemble-only` · `--only SCENE_ID` · `--regen-stills` · `--regen-tts` · `--regen-clips`

Requires `PRUNA_API_KEY`; optional bed needs `REPLICATE_API_TOKEN`.

## Related

- Prompt tables: [interactive-explainer-prompts.md](./references/interactive-explainer-prompts.md)
- Feedback: [requesting-generation-feedback](https://github.com/PrunaAI/pruna-skills/tree/main/router/references/policies/approval-red-flags.md)
- Narrator-only: [narrated-multi-scene](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/narrated-multi-scene/skills/narrated-multi-scene/SKILL.md)
- Visual transitions (no VO): [visual-transition-reel](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/visual-transition-reel/skills/visual-transition-reel/SKILL.md)
- Hub: [pruna-generative-pipeline](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/pruna-generative-pipeline/skills/pruna-generative-pipeline/SKILL.md) (Recipe R)
- Example prompts: [./example-prompt.md](./example-prompt.md)
- Example plans (local workspace): `output/verticals/interactive-explainer/<project-slug>/plan.json` — see [output/README.md](https://github.com/PrunaAI/pruna-skills/tree/main/output/README.md)
