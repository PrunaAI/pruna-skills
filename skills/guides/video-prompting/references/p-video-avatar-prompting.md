# p-video-avatar prompting

Talking-head prompt craft for `p-video-avatar`. Templates: [avatar-multi-scene/prompt-templates.md](../../workflows/avatar-multi-scene/prompt-templates.md). Camera: [camera-lighting-vocabulary.md](./camera-lighting-vocabulary.md). Physics: [physics-safe-motion.md](./physics-safe-motion.md).

**Do not** use OPEN/MID/CLOSE — the model treats beats as cuts and the clip feels cutty.

## Three-layer stack

| Layer | Field | Job |
|-------|-------|-----|
| 1. Plate | `image` | Locked approved still — mouth visible; quality caps the avatar |
| 2. Voice | `voice_script` + `voice_prompt` | What they say + how they sound |
| 3. Motion | `video_prompt` | Unique camera/gesture per clip |

Never ship multi-scene reels where every row reuses `medium close-up, gentle dolly push-in`.

## Field hygiene

| Field | Write | Never |
|-------|-------|-------|
| **`voice_script`** | Natural spoken lines | Brochure / slogan paste as the only line without human rhythm |
| **`voice_prompt`** | Short delivery: pacing, warmth, archetype | Product names, script lines, long scene descriptions |
| **`video_prompt`** | MCU, one slow push-in or static, speaks to camera | OPEN/MID/CLOSE; walk across room; hold up documents; wild gestures |

Stylized hosts: match energy to medium (anime slightly more expressive; documentary restrained). Separate hero stills per `visual_style_tag`.

## Micro-actions (talking-head Details Law)

Prefer face/eye micro-moves over locomotion:

- eyes lift to lens, slight nod, natural blink rhythm, subtle lean  
- one small hand-to-chest max  

Avoid physics traps while speaking ([physics-safe-motion.md](./physics-safe-motion.md) avatar subsection).

## Negative prompt (experimental)

API `negative_prompt` = **noun suppression list** (subtitles, captions, watermark…), not creative wording. Strength ~0.3–0.4. Primary fix: positive-only stills (`plain unmarked walls`). See SKILL for defaults.

## Good / bad triples

**Good**

```text
voice_script: "So we tried something weird last quarter — and it actually worked."
voice_prompt: Natural conversational tone, relaxed pacing, real pauses, honest not salesy.
video_prompt: Medium close-up speaking directly to lens, one very slow push-in, steady light, natural head motion, no cuts.
```

**Bad**

```text
voice_prompt: Mention Pruna and our 10x faster inference in an exciting cinematic way.
video_prompt: OPEN: hold. MID: she walks across the room waving a laptop. CLOSE: product hero shot.
```

## Pre-send

- [ ] Plate approved; mouth visible  
- [ ] `voice` locked per character across scenes  
- [ ] Unique `video_prompt` per clip  
- [ ] No OPEN/MID/CLOSE  
- [ ] `voice_prompt` has no script/product paste  

QA: [p-video-avatar-quality-checklist.md](./p-video-avatar-quality-checklist.md).
