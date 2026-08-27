---
name: interactive-explainer
description: Use when someone wants an educational explainer with a host and characters — history or science shorts with dialogue, not voiceover-only B-roll.
license: MIT
metadata:
  version: "1.0.10"
  package: pruna-skills
---

## Prerequisites

Install and load these skills before generating (skip if already in context via `@pruna`):

| Skill | Description | Install |
| --- | --- | --- |
| `p-image` | Use when someone explicitly wants the fastest, cheapest photo generation — mood boards, bulk panels, or quick iterations — not when controlled photoreal or in-image text is needed. | `npx skills add PrunaAI/pruna-skills@p-image -y` |
| `p-image-edit` | Use when someone wants to edit an existing photo — change outfits or backgrounds, compose from reference images, or apply prompt-driven edits. | `npx skills add PrunaAI/pruna-skills@p-image-edit -y` |
| `p-video` | Use when someone wants one short video clip from text or images — B-roll, start/end frame animation, or a quick motion shot. Not for full multi-scene films or lip-synced hosts. | `npx skills add PrunaAI/pruna-skills@p-video -y` |
| `p-video-avatar` | Use when someone wants a person on camera speaking a script — lip-synced host, spokesperson, or narrated avatar from a portrait photo. | `npx skills add PrunaAI/pruna-skills@p-video-avatar -y` |
| `gemini-3.1-flash-tts` | Use when someone needs spoken narration or voiceover — explainer tracks, documentary lines, or voice to pair with generated video. | `npx skills add PrunaAI/pruna-skills@gemini-3.1-flash-tts -y` |
| `stable-audio-2.5` | Use when someone wants light instrumental background music — an ambient bed under dialogue or underscore for reels and explainers. | `npx skills add PrunaAI/pruna-skills@stable-audio-2.5 -y` |

Or install the full suite once: `npx skills add PrunaAI/pruna-skills@pruna -y`

Follow each skill's **Before generating** / craft sections — do not restate guide content here.

## Workflow habit

In **every reply**, name `` `interactive-explainer` `` in backticks. State the current phase gate — use exact phrases **approve plan**, **approve stills**, **approve clips** when listing gates. Do **not** same-turn plan + paid video. Skip-review / burn-credits → follow `generation-diversity` **Red flags**.

## Quick reference

| Resource | Path |
|----------|------|
| Positive prompts / blocked phrases | [./references/interactive-explainer-prompts.md](./references/interactive-explainer-prompts.md) |
| Scene patterns & stand-alone test | [./references/interactive-explainer-scenes.md](./references/interactive-explainer-scenes.md) |
| Motion (OPEN/MID/CLOSE) | [./references/interactive-explainer-motion.md](./references/interactive-explainer-motion.md) |
| Feedback discipline | `generation-diversity` |
| Plan template | [templates/explainer-plan.template.json](./templates/explainer-plan.template.json) |

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

## Motion (dynamic, physics-safe)

Every scene needs **visible motion** — but not physics-heavy action. See [./references/interactive-explainer-motion.md](./references/interactive-explainer-motion.md).

| Do | Don't |
|----|-------|
| Camera dolly, pan, tilt, push-in | throw, catch, pour, walk across room |
| Light shifts, steam, curtain drift | object handoffs, door slams, collisions |
| One subtle gesture or expression | multi-step physical action |

Write **`video_prompt`** as `OPEN:` → `MID:` (attention hook) → `CLOSE:` (settle on end still). Keep camera moves **slow and deliberate**.

## Intake: ask before generating

Open intake → **`generation-diversity`** clarification intake.

| Topic | Questions |
|-------|-----------|
| **Topic** | What should the viewer learn? Key facts or story beats? |
| **Media source** | **Generate** all stills/avatars with Pruna vs **upload** cast photos, locations, or reference plates? |
| **Format** | Delivery **`9:16` / `16:9`**; avatar and `p-video` output **`720p` / `1080p`**? |
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
| **A2 — TTS** | `audio/narration_*.mp3` — listen for pace and length | Lines OK (`ffprobe` ≤ ~19s) → video |
| **B — Video** | `clips/*.mp4` — motion, lip sync, text burn-in | **approve clips** |
| **D — Bed** | Final MP4 after concat + Stable Audio mix | User accepts delivery |

## Generation phases

| Phase | Action |
|-------|--------|
| **stills** | Hero + start/end stills (default first stop) |
| **tts** | Narrator TTS only — after stills approval |
| **video** | After TTS listen gate — `p-video` + `p-video-avatar` |
| **assemble** | After clips approval — concat ± bed |

## Scene table (template)

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

Default if omitted: **`narrator`**.

## How the agent runs this

1. Copy [templates/explainer-plan.template.json](./templates/explainer-plan.template.json) → fill cast + scene table → **approve plan**.
2. Parallel stills curl (`pruna-api`) → **approve stills**.
3. Parallel Gemini TTS (narrator rows) → duration gate → listen.
4. Parallel `p-video` triples + `p-video-avatar` → **approve clips**.
5. ffmpeg concat ± crossfade → optional bed.

## Workflow

| Phase | Action |
|-------|--------|
| **0** | `p-image` hero (+ optional `_cast_*` anchor stills from `anchor_still_prompt`) |
| **1** | Parallel `p-image-edit` start stills (all scenes) |
| **2** | Parallel end stills (**narrator** only) |
| **A2** | Parallel Gemini TTS (**narrator** only) |

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 audio/narration_01.mp3
# ≤ ~19s before p-video
```

| Phase | Action |
|-------|--------|
| **B** | Parallel `p-video` triples + `p-video-avatar` (avatar may exceed 20s) |
| **C/D** | Concat ± `stable-audio-2.5` bed |

**Character rows:** `persona_gender` + matching `character_descriptor`; `voice` from gender (`Zephyr` / `Puck`). Use `still_from` or `_cast_*` when hero is B-roll/objects. Avatar text suppression: [./references/interactive-explainer-prompts.md](./references/interactive-explainer-prompts.md).

**Assembly:**

```bash
ffmpeg -y -f concat -safe 0 -i clips.txt -c copy explainer.mp4
```

Optional crossfades via plan `assembly.hard_cut_crossfade_seconds` (~0.12–0.15 on soft joins). Re-assemble from existing clips without regenerating video.

## Scripting rules

Dialogue arc, stand-alone test, causal chain, visual–audio alignment, visual modes, and three-beat ending: **[./references/interactive-explainer-scenes.md](./references/interactive-explainer-scenes.md)**.

**Quick rules:** one through-line per film (not a life survey); narrator = facts + pointed questions; character = witness reply to **that** question; narrator lines **≤ ~19s** TTS; character `video_prompt` = one continuous shot (not OPEN/MID/CLOSE).

## Common mistakes

- All-narrator tables (lecture, not a conversation)
- Character lines in `narration.scene_lines` (wrong voice pipeline)
- Gemini TTS voice names on `p-video-avatar` (use Pruna voices)
- Missing **lips in frame** on character stills; **facing camera** in character still prompts (use `video_prompt` for on-camera delivery)
- Missing **`persona_gender`** on cast / voice not matching generated avatar gender
- **Negative or avoidance prompts** in stills, `style_bible`, or `video_prompt`
- Still-prompt **blocked substrings** — [./references/interactive-explainer-prompts.md](./references/interactive-explainer-prompts.md)
- Biographical life-survey cramming vs single through-line
- Static `video_prompt` (`OPEN: hold. CLOSE: hold.`) — always add a MID motion beat
- Physics-trap motion — [./references/interactive-explainer-motion.md](./references/interactive-explainer-motion.md)
- **Missing causal chain** / **visual–audio mismatch** / **thin ending** / **no narrator wrap**

## Related

Related skills:

| Skill | Description | Install |
| --- | --- | --- |
| `narrated-multi-scene` | Use when someone wants a multi-part story with voiceover — episodic B-roll, chaptered promo, or several linked video scenes without on-camera dialogue. | `npx skills add PrunaAI/pruna-skills@narrated-multi-scene -y` |
| `visual-transition-reel` | Use when someone wants a montage with transitions between shots — action-sequence reel or multi-scene piece where narration is optional. | `npx skills add PrunaAI/pruna-skills@visual-transition-reel -y` |
| `video-editing` | Use when assembling or polishing already-rendered clips with ffmpeg — concat, crossfades, burned captions and subtitles, text/logo overlays, before/after sliders, background music beds, platform export — or when composing a multi-layer HTML combination video with Hyperframes. Not for AI video generation, prompt craft, or model-based video edits. | `npx skills add PrunaAI/pruna-skills@video-editing -y` |

