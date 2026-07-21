# Illustrated story reel — staged gates

Human-in-the-loop phases for **illustrated-story-reel**. Uses **p-image**, **p-image-edit**, optional **p-video** (Mode B motion), Replicate TTS/music, and local ffmpeg assembly.

## Phases

| Phase | Models / tools | Cost | User interaction |
|-------|----------------|------|------------------|
| **0 — Plan** | none | free | Present beat table, `audio_mode`, `motion_mode`, sample still lines; **approve plan** |
| **A — Stills** | `p-image`, `p-image-edit` | low | Show `stills/*.png`; run checklists; **approve stills** |
| **A2 — Audio** | Gemini TTS **or** Stable Audio / user track | low–medium | **Listen** to `audio/narration_*.mp3` or `audio/music.mp3`; **approve audio** |
| **B — Motion** | `p-video` (when `motion_mode: p-video`) | medium | **Watch + listen** to `clips/*.mp4`; **approve clips** |
| **C — Assemble** | local ffmpeg (Ken Burns + mux **or** clip concat) | free | Review `story_reel.mp4` (or `--output-name`) |

Ken Burns path skips Phase B. Music-mode reels use Ken Burns only (no p-video).

## Agent rules

1. **Only** call `p-video` when `motion_mode: p-video` and narration is approved — not for Ken Burns tremor fixes.
2. **Never** run audio, video, or assembly in the same turn as still generation without showing stills and waiting for approval.
3. **Parallelize within a phase** (batch still edits, parallel TTS, parallel p-video), not across phases.
4. **Do not pass `PRUNA_API_KEY` or `REPLICATE_API_TOKEN` to subagents** unless a subagent is running an approved still or TTS lane — parent owns gates and assembly.
5. Run [illustrated-story-reel-quality.md](./illustrated-story-reel-quality.md) on every still before audio or video.
6. **[Generation diversity](../../../guides/generation-diversity/references/generation-diversity.md)** and **[random seed ritual](../../../guides/generation-diversity/references/generation-diversity.md#random-seed-ritual-mandatory-before-every-generation)** before every `POST /v1/predictions`.

## Wording templates

After Phase 0:

> Here is the beat table, `audio_mode`, and `motion_mode`. Reply **approve plan** to generate stills, or tell me what to change.

After Phase A:

> Stills are in `stills/`. Reply **approve stills** to run TTS or music, or name beats to fix.

After Phase A2:

> Audio is in `audio/`. Listen for pace and tone. Reply **approve audio** to run p-video (if motion_mode p-video) or assemble (Ken Burns), or tell me lines to rewrite.

After Phase B (p-video):

> Motion clips are in `clips/`. Watch for style drift and listen for sync. Reply **approve clips** to assemble, or name beats to re-render.

Before assembly:

> Assembly runs ffmpeg into `{out_dir}/story_reel.mp4`. ffmpeg uses **`-y`** and overwrites the output path without confirmation — confirm `{out_dir}` is correct.

## Phases (agent)

Default stop after **stills**. Do not run TTS/music until stills are approved. Do not run p-video until audio is approved. Assembly needs approved audio (Ken Burns) or approved clips (p-video).

Follow `illustrated-story-reel` — agent runs curl + ffmpeg. No Python runner. Do not skip still/audio/clip approval gates.

## Local state files

| File | Purpose | Privacy note |
|------|---------|--------------|
| `generation_status.json` | Phase approval flags (`phase_a`, `phase_b`, `phase_c`) | Written under `--out-dir`; safe to delete to reset gates |
| `stills/`, `audio/`, `clips/`, `segments/` | Generated media | May contain prompts reflected in filenames and plan JSON |
| `plan.json` | Beat prompts and narration | Can include sensitive project details — treat as confidential |

## Anti-patterns

- **`p-video` for Ken Burns tremor** — tune `ken_burns` (prefer `pan_*`) + re-assemble per SKILL **Motion + assemble**
- **VO transcript in `video_prompt`** — Mode B motion only ([p-video-motion](./illustrated-story-reel-p-video-motion.md))
- Aggressive **zoom_in on every illustrated beat** — prefer `pan_left` / `pan_right`
- Skipping still, audio, or clip review before the next paid phase
- Passing API keys to broad subagent trees
- Running assembly before the user listens to narration or watches p-video clips
