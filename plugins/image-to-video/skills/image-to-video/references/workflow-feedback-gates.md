# Workflow feedback gates (index)

Every workflow skill uses [staged-generation-gate.md](./staged-generation-gate.md). **Agents must pause** at each gate and **ask** when art direction is unclear.

**Before any paid generation:** [approval-red-flags.md](./approval-red-flags.md) — red flags, pause workflow, common mistakes.

| Workflow skill | Runner | Default `--phase` | Gates |
|----------------|--------|-------------------|-------|
| [interactive-explainer](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/interactive-explainer/skills/interactive-explainer/SKILL.md) | `workflows/interactive-explainer/scripts/run_from_plan.py` | `stills` | plan → stills → TTS → video → assemble+bed |
| [music-video](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/music-video/skills/music-video/SKILL.md) | `workflows/music-video/scripts/run_from_plan.py` | `song` | plan/lyrics → song → align → stills → video → assemble |
| [illustrated-story-reel](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/illustrated-story-reel/skills/illustrated-story-reel/SKILL.md) | `workflows/illustrated-story-reel/scripts/run_from_plan.py` | `stills` | plan → stills → tts **or** music → assemble (no p-video) |
| [narrated-multi-scene](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/narrated-multi-scene/skills/narrated-multi-scene/SKILL.md) | manual / phased curl | — | plan → stills → TTS → video → bed |
| [visual-transition-reel](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/visual-transition-reel/skills/visual-transition-reel/SKILL.md) | `workflows/visual-transition-reel/scripts/run_from_plan.py` | `stills` | plan → stills → video → assemble+bed |
| [avatar-single-scene](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/avatar-single-scene/skills/avatar-single-scene/SKILL.md) | manual / curl | — | plan → still → avatar |
| [avatar-multi-scene](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/avatar-multi-scene/skills/avatar-multi-scene/SKILL.md) | manual / curl | — | plan → hero+stills → avatar/animate → assembly |
| [image-to-video](../SKILL.md) | manual / curl | — | plan → stills → TTS (if triple) → video → bed |

## Universal agent rules

1. **Phase 0 — Plan:** Present scene table, cast, scripts, `style_bible`. Wait for **approve plan**.
2. **Phase A — Stills:** Generate images only. Show paths. Wait for **approve stills**.
3. **Phase A2 — Audio prep:** TTS, song, or align — user listens/reads before video.
4. **Phase B — Video:** Paid jobs only after still (+ audio prep) approval. Wait for **approve clips**.
5. **Phase C/D — Assembly + final audio:** Concat and bed/mux only after clip approval.

**Never** run plan approval and video in the same turn. **Ask** when visual mode, cast, continuity, or bed is ambiguous.

## Runner flag reference

| Flag | Sets in `generation_status.json` | Unlocks |
|------|----------------------------------|---------|
| `--approve-song` | `phase_song_approved` | music-video stills+ after song |
| `--approve-stills` | `phase_a_approved` | TTS, video, replace, animate |
| `--approve-clips` | `phase_b_approved` | assemble, bed, final mux |
| `--approve-audio` | `phase_b_approved` | illustrated-story-reel assemble (alias: `--approve-clips`) |
| `--yes-skip-stills-gate` | — | automation bypass (Phase A) |
| `--yes-skip-clips-gate` | — | automation bypass (Phase B) |
| `--yes-skip-song-gate` | — | automation bypass (song) |
| `--assemble-only` | — | concat/bed from existing clips (no API) |

Shared helpers: [`generation_gate.py`](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/_shared/scripts/generation_gate.py)

## Per-workflow commands

### Interactive explainer

```bash
python3 .../interactive-explainer/scripts/run_from_plan.py --plan PLAN --out-dir OUT --phase stills
python3 ... --approve-stills --phase tts
python3 ... --phase video
python3 ... --approve-clips --phase assemble --final-name my_final.mp4
```

### Music video

```bash
python3 .../music-video/scripts/run_from_plan.py --plan PLAN --out-dir OUT --phase song
python3 ... --approve-song --phase align
python3 ... --phase stills
python3 ... --approve-stills --phase video
python3 ... --approve-clips --phase assemble
```

### Visual transition reel

```bash
python3 .../visual-transition-reel/scripts/run_from_plan.py --plan PLAN --out-dir OUT --phase stills
python3 ... --approve-stills --phase video
python3 ... --approve-clips --phase assemble
```

### Illustrated story reel

```bash
python3 .../illustrated-story-reel/scripts/run_from_plan.py --plan PLAN --out-dir OUT --phase stills
python3 ... --approve-stills --phase tts      # narration mode (audio_mode: narration)
python3 ... --approve-stills --phase music    # music mode (audio_mode: music)
python3 ... --approve-audio --phase assemble
```

For recipe selection when unsure which workflow fits, see [WORKFLOW-RECIPES.md](https://github.com/PrunaAI/pruna-skills/tree/main/docs/WORKFLOW-RECIPES.md).
