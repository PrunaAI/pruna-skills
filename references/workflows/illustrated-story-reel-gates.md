# Illustrated story reel — staged gates (still-only)

Human-in-the-loop phases for **illustrated-story-reel** only. This skill uses **p-image**, **p-image-edit**, Replicate TTS/music, and **local ffmpeg Ken Burns assembly**. It does **not** call `p-video`, `p-video-avatar`, `p-video-animate`, or `p-video-replace`.

For video workflows, use **interactive-explainer**, **narrated-multi-scene**, or **music-video** instead.

## Phases

| Phase | Models / tools | Cost | User interaction |
|-------|----------------|------|------------------|
| **0 — Plan** | none | free | Present beat table, `audio_mode`, sample still lines; **approve plan** |
| **A — Stills** | `p-image`, `p-image-edit` | low | Show `stills/*.png`; run checklists; **approve stills** |
| **A2 — Audio** | Gemini TTS **or** Stable Audio / user track | low–medium | **Listen** to `audio/narration_*.mp3` or `audio/music.mp3`; **approve audio** |
| **C — Assemble** | local ffmpeg (Ken Burns + mux) | free | Review `story_reel.mp4` (or `--output-name`) |

There is **no Phase B video**. Do not escalate to paid video APIs from this skill.

## Agent rules

1. **Never** call `p-video*` models while executing this skill.
2. **Never** run audio or assembly in the same turn as still generation without showing stills and waiting for approval.
3. **Parallelize within a phase** (batch still edits, parallel TTS), not across phases.
4. **Do not pass `PRUNA_API_KEY` or `REPLICATE_API_TOKEN` to subagents** unless a subagent is running an approved still or TTS lane — parent owns gates and assembly.
5. Run [illustrated-story-reel-quality.md](./illustrated-story-reel-quality.md) on every still before audio or assembly.
6. **[Generation diversity](../shared/generation-diversity.md)** and **[random seed ritual](../shared/random-seed-ritual.md)** before every `POST /v1/predictions`.

## Wording templates

After Phase 0:

> Here is the beat table and `audio_mode`. Reply **approve plan** to generate stills, or tell me what to change.

After Phase A:

> Stills are in `stills/`. Reply **approve stills** to run TTS or music, or name beats to fix.

After Phase A2:

> Audio is in `audio/`. Listen for pace and tone. Reply **approve audio** to assemble the slideshow, or tell me lines to rewrite.

Before assembly:

> Assembly runs ffmpeg Ken Burns + mux into `{out_dir}/story_reel.mp4`. ffmpeg uses **`-y`** and overwrites the output path without confirmation — confirm `{out_dir}` is correct.

## Runner

Default **`--phase stills`**. Audio phases require **`--approve-stills`** or `"phase_a_approved": true` in `generation_status.json`. Assembly requires **`--approve-audio`** (alias `--approve-clips`) or `"phase_b_approved": true`.

```bash
python3 .../illustrated-story-reel/scripts/run_from_plan.py --plan PLAN --out-dir OUT --phase stills
python3 ... --approve-stills --phase tts      # narration mode
python3 ... --approve-stills --phase music    # music mode
python3 ... --approve-audio --phase assemble
```

### Gate bypass flags (CI only)

`--yes-skip-stills-gate` and `--yes-skip-clips-gate` exist for **maintainer CI/automation only**. **Agents must not use them** — they bypass human review and can trigger paid API calls without approval.

## Local state files

| File | Purpose | Privacy note |
|------|---------|--------------|
| `generation_status.json` | Phase approval flags | Written under `--out-dir`; safe to delete to reset gates |
| `stills/`, `audio/`, `segments/` | Generated media | May contain prompts reflected in filenames and plan JSON |
| `plan.json` | Beat prompts and narration | Can include sensitive project details — treat as confidential |

## Anti-patterns

- Using **p-video** “for smoother motion” — stay still-only; tune Ken Burns + crossfade
- `--phase all` without still and audio review
- Passing API keys to broad subagent trees for this still-only workflow
- Running assembly before the user listens to narration or music
