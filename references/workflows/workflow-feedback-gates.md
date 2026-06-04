# Workflow feedback gates (index)

Every workflow skill uses [staged-generation-gate.md](../shared/staged-generation-gate.md). **Agents must pause** at each gate and **ask** when art direction is unclear.

| Workflow skill | Runner | Default `--phase` | Gates |
|----------------|--------|-------------------|-------|
| [interactive-explainer](../../guides/workflows/verticals/interactive-explainer/SKILL.md) | `verticals/interactive-explainer/scripts/run_from_plan.py` | `stills` | plan → stills → TTS → video → assemble+bed |
| [music-video](../../guides/workflows/verticals/music-video/SKILL.md) | `verticals/music-video/scripts/run_from_plan.py` | `song` | plan/lyrics → song → align → stills → video → assemble |
| [narrated-multi-scene](../../guides/workflows/core/narrated-multi-scene/SKILL.md) | manual / phased curl | — | plan → stills → TTS → video → bed |
| [visual-transition-reel](../../guides/workflows/core/visual-transition-reel/SKILL.md) | `core/visual-transition-reel/scripts/run_from_plan.py` | `stills` | plan → stills → video → assemble+bed |
| [avatar-single-scene](../../guides/workflows/core/avatar-single-scene/SKILL.md) | manual / curl | — | plan → still → avatar |
| [avatar-multi-scene](../../guides/workflows/core/avatar-multi-scene/SKILL.md) | manual / curl | — | plan → hero+stills → avatar/animate → assembly |
| [image-to-video](../../guides/workflows/core/image-to-video/SKILL.md) | manual / curl | — | plan → stills → TTS (if triple) → video → bed |
| [p-video-replace-comparison](../../guides/workflows/launches/p-video-replace-comparison/SKILL.md) | `launches/p-video-replace-comparison/scripts/run_from_plan.py` | `stills` | plan → stills → video → render+bed |
| [p-video-animate-comparison](../../guides/workflows/launches/p-video-animate-comparison/SKILL.md) | `launches/p-video-animate-comparison/scripts/run_from_plan.py` | `stills` | plan → stills → animate → render |
| [p-image-upscale-comparison](../../guides/workflows/launches/p-image-upscale-comparison/SKILL.md) | local ffmpeg | — | plan → upscale QA → comparison render |
| [pruna-generative-pipeline](../../guides/workflows/router/pruna-generative-pipeline/SKILL.md) | recipe-specific | — | routes to rows above |

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
| `--yes-skip-stills-gate` | — | automation bypass (Phase A) |
| `--yes-skip-clips-gate` | — | automation bypass (Phase B) |
| `--yes-skip-song-gate` | — | automation bypass (song) |
| `--assemble-only` | — | concat/bed from existing clips (no API) |

Shared helpers: [`generation_gate.py`](../../guides/workflows/_shared/scripts/generation_gate.py)

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

### Replace comparison

```bash
python3 .../p-video-replace-comparison/scripts/run_from_plan.py --plan PLAN --out-dir OUT --phase stills
python3 ... --approve-stills --phase video
python3 ... --approve-clips --phase render --background-music
```

### Narrated multi-scene / avatar (no runner)

Execute manually in order: hero → scene stills (parallel) → slop gate → TTS (parallel) → user listens → `p-video` batch → user reviews clips → concat → optional bed.
