---
name: illustrated-story-reel
description: Use when the user wants a still-image story reel, picture-book slideshow, or illustrated narrative with voiceover or music—and explicitly not generative video (p-video).
license: MIT
metadata:
  version: "0.0.1"
---

# Illustrated story reel

Sequential **p-image** / **p-image-edit** stills assembled in ffmpeg with subtle Ken Burns motion, synced to **narration** (Gemini TTS) or **instrumental music** (Stable Audio or user track). **No p-video.**

Ideal for social story posts, fairy-tale explainers, mood reels, and “moving illustration” formats like illustrated TikTok/X threads.

## Overview

One still per story beat. Hero anchor → **p-image-edit** per scene. Audio drives timing in narration mode; fixed **hold_seconds** per beat in music mode. Assembly is local ffmpeg only.

## When to Use

- Illustrated story without AI video generation
- Picture-book / comic-panel narrative with VO or bed
- User references a “slideshow story”, “Ken Burns reel”, or still-only social post
- Budget-sensitive runs (images only, no video API credits)

**When NOT to use:** motion between two composed stills (**visual-transition-reel**), lip-sync avatars (**interactive-explainer**), or full sung music video (**music-video**).

## Feedback gates

[staged-generation-gate.md](../../../../../references/shared/staged-generation-gate.md) · [workflow-feedback-gates.md](../../../../../references/workflows/workflow-feedback-gates.md)

| Phase | What to show | Proceed when |
|-------|--------------|--------------|
| **0 — Plan** | Beat table, `audio_mode`, sample still lines + narration | **approve plan** |
| **A — Stills** | `stills/*.png` | **approve stills** |
| **A2 — Audio** | `audio/narration_*.mp3` or `audio/music.mp3` — **listen** | **approve audio** |
| **C — Assemble** | `story_reel.mp4` | User accepts |

Default runner **`--phase stills`**.

## Quick reference

| Item | Value |
|------|--------|
| Models | **p-image**, **p-image-edit**, Gemini TTS, Stable Audio 2.5 |
| Plan field | `audio_mode`: `"narration"` \| `"music"` |
| Runner | `verticals/illustrated-story-reel/scripts/run_from_plan.py` |
| Template | `templates/story-plan.template.json` |
| Output | `{out_dir}/story_reel.mp4` |

## Intake — ask before generating

**First question (required):** “Should this story use **narration** (voiceover per beat) or **music** (instrumental bed / your track)?”

Set `audio_mode` in the plan accordingly.

| Topic | Questions |
|-------|-----------|
| **Story** | Title? Beat order (1…N)? Emotional arc? |
| **Visual** | Style (`style_bible`)? Portrait **9:16** vs landscape **16:9**? Character continuity? |
| **Per beat** | `edit_prompt` (one frame)? `narration` line (narration mode)? `hold_seconds` (music mode)? |
| **Motion** | `ken_burns`: `zoom_in`, `zoom_out`, `pan_left`, `pan_right`, `none`? Crossfade vs hard cut? |
| **Music mode** | Stable Audio prompt, user `music.track` path, or equal seconds per beat? |
| **Narration mode** | Voice (`Kore`, etc.)? Storyteller pace in `narration.style_prompt`? |

Do not start generation until the beat table is written and **audio_mode** is confirmed.

### Beat table (template)

| `#` | Still (`edit_prompt`) | Narration / hold | Ken Burns | Chain? |
|-----|------------------------|------------------|-----------|--------|
| 1 | opening wide | line or 4s | zoom_in | no |
| 2 | detail insert | line or 3.5s | pan_right | yes |

## Workflow

```bash
# Phase A — stills only
python3 guides/workflows/verticals/illustrated-story-reel/scripts/run_from_plan.py \
  --plan output/.../plan.json --out-dir output/.../ --phase stills

# Phase A2 — narration OR music (matches audio_mode in plan)
python3 ... --approve-stills --phase tts    # narration mode
python3 ... --approve-stills --phase music   # music mode

# Phase C — Ken Burns + mux
python3 ... --approve-audio --phase assemble
```

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Using **p-video** “for smoother motion” | Stay still-only; tune Ken Burns + crossfade |
| Skipping audio listen gate | Run `--phase tts` or `music`; wait for **approve audio** |
| One long narration blob | One line per beat; TTS per scene for sync |
| Music mode without `hold_seconds` | Set per beat or `defaults.hold_seconds` |
| Negation in still prompts | Positive description only — see [interactive-explainer-prompts.md](../../../../../references/workflows/interactive-explainer-prompts.md) |

## Related

- Stills batch: [stills_pipeline.py](../../_shared/scripts/stills_pipeline.py)
- Narrated **video** film: [narrated-multi-scene](../../core/narrated-multi-scene/SKILL.md)
- Motion between stills: [visual-transition-reel](../../core/visual-transition-reel/SKILL.md)
- Tools: [p-image](../../../../tools/image/p-image/SKILL.md), [p-image-edit](../../../../tools/image/p-image-edit/SKILL.md)
