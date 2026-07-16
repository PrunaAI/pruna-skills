---
name: illustrated-story-reel
description: Use when the user wants a still-image story reel or slideshow, picture-book narrative with voiceover or music—and explicitly not full motion-video generation.
license: MIT
metadata:
  version: "1.0.2"
---

# Illustrated story reel

Sequential **p-image** / **p-image-edit** stills assembled in ffmpeg with subtle Ken Burns motion, synced to **narration** (Gemini TTS) or **instrumental music** (Stable Audio or user track). **No p-video.**

Delivery is **not** limited to vertical reels. Set `defaults.aspect_ratio` to **`9:16`** (Stories/Reels/TikTok), **`16:9`** (YouTube, presentations, landing-page hero), or **`1:1`** (feed squares). The runner renders at 1080p for the chosen ratio; default output filename is `story_reel.mp4` — override with `--output-name` (e.g. `story_slideshow.mp4`) when the deliverable is landscape.

Ideal for social story posts, fairy-tale explainers, mood reels, horizontal photo essays, product ramps, and “moving illustration” formats.

## Overview

One still per story beat. Hero anchor → **p-image-edit** per scene. Audio drives timing in narration mode; fixed **hold_seconds** per beat in music mode. Assembly is local ffmpeg only.

## When to Use

- Illustrated story without AI video generation
- Picture-book / comic-panel narrative with VO or bed
- User references a “slideshow story”, “Ken Burns reel”, or still-only social post
- Budget-sensitive runs (images only, no video API credits)

**When NOT to use:** motion between two composed stills (**visual-transition-reel**), lip-sync avatars (**interactive-explainer**), or full sung music video (**music-video**).

## Security & scope

**Still-image slideshow only — no `p-video*`.** Bundled references are scoped to this workflow; do not follow video/avatar examples from other skills.

| Risk | Mitigation |
|------|------------|
| Paid API use | `PRUNA_API_KEY` + `REPLICATE_API_TOKEN`; gates before TTS/music/assembly |
| Credential exposure | Parent agent holds keys; do not pass to subagents except per-lane still/TTS work |
| Local execution | `ffmpeg`/`ffprobe` subprocess; **`-y` overwrites** output MP4 without confirmation |
| Data retention | `plan.json`, `generation_status.json`, and media under `--out-dir` may contain prompts — treat as confidential |

Requires: [api-credentials.md](./references/api-credentials.md) · Permissions: `skill.manifest.json`

## Feedback gates

[illustrated-story-reel-gates.md](./references/illustrated-story-reel-gates.md)

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
| Aspect | `defaults.aspect_ratio`: `"9:16"` \| `"16:9"` \| `"1:1"` (match in `hero_prompt` / still lines) |
| Runner | `verticals/illustrated-story-reel/scripts/run_from_plan.py` |
| Template | `templates/story-plan.template.json` (9:16) · `templates/story-plan.landscape.template.json` (16:9) |
| Output | `{out_dir}/story_reel.mp4` (default; use `--output-name` for landscape naming) |

## Intake — ask before generating

**First questions (required):**

1. **Delivery shape** — vertical reel (**9:16**), horizontal slideshow (**16:9**), or square (**1:1**)?
2. **Audio** — **narration** (voiceover per beat) or **music** (instrumental bed / user track)?

Set `defaults.aspect_ratio` and `audio_mode` in the plan before generation. Align `hero_prompt` wording with the ratio (e.g. “16:9 horizontal frame” for landscape).

| Topic | Questions |
|-------|-----------|
| **Story** | Title? Beat order (1…N)? Emotional arc? |
| **Visual** | Style (`style_bible`)? Character continuity? `chain_from_previous` for edit chains? |
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
python3 workflows/verticals/illustrated-story-reel/scripts/run_from_plan.py \
  --plan output/.../plan.json --out-dir output/.../ --phase stills

# Phase A2 — narration OR music (matches audio_mode in plan)
python3 ... --approve-stills --phase tts    # narration mode
python3 ... --approve-stills --phase music   # music mode

# Phase C — Ken Burns + mux
python3 ... --approve-audio --phase assemble

# Landscape example (16:9 in plan.json defaults)
python3 ... --approve-audio --phase assemble --output-name story_slideshow.mp4
```

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Using **p-video** “for smoother motion” | Stay still-only; tune Ken Burns + crossfade |
| Skipping audio listen gate | Run `--phase tts` or `music`; wait for **approve audio** |
| One long narration blob | One line per beat; TTS per scene for sync |
| Music mode without `hold_seconds` | Set per beat or `defaults.hold_seconds` |
| Negation in still prompts | Positive description only — see [illustrated-story-reel-prompts.md](./references/illustrated-story-reel-prompts.md) |
| Assuming vertical only | Set `aspect_ratio` to `16:9` and landscape framing in prompts for horizontal deliverables |
| Mismatched ratio in prompts | `aspect_ratio` in plan must match “vertical” / “horizontal” / “square” in `hero_prompt` and beats |

## Related

- Stills batch: [stills_pipeline.py](./scripts/stills_pipeline.py)
- Narrated **video** film: [narrated-multi-scene](../narrated-multi-scene/SKILL.md)
- Motion between stills: [visual-transition-reel](../visual-transition-reel/SKILL.md)
- Tools: [p-image](../../../../tools/image/p-image/SKILL.md), [p-image-edit](../../../../tools/image/p-image-edit/SKILL.md)
