# Workflow feedback gates

Agent-only approval phases for multi-step workflows. Universal QA: [generation-quality-checklists.md](./generation-quality-checklists.md#approval-gates-workflows).

**Agents must pause** at each gate and **ask** when art direction is unclear. Never approve the plan and run paid video in the same turn. There are **no Python runners** — follow each workflow skill’s phase tables (curl + ffmpeg).

## Phase table (all workflows)

| Phase | What to show | Proceed when |
|-------|--------------|--------------|
| **0 — Plan** | Scene table, cast, scripts, `style_bible` | **approve plan** |
| **A — Stills** | Generated images only | **approve stills** |
| **A2 — Audio** (when used) | TTS / song / align preview | User listens / accepts |
| **B — Video** | Paid clip outputs | **approve clips** |
| **C — Assembly** | Concat / bed / final mux | User accepts deliverable |

## Per-workflow gate order

| Workflow | Install | Gates |
|----------|---------|-------|
| `image-to-video` | `@image-to-video` | plan → stills → TTS (if triple) → video → bed |
| `narrated-multi-scene` | `@narrated-multi-scene` | plan → stills → TTS → video → bed |
| `visual-transition-reel` | `@visual-transition-reel` | plan → stills → video → assemble ± bed |
| `avatar-single-scene` | `@avatar-single-scene` | plan → still → avatar |
| `avatar-multi-scene` | `@avatar-multi-scene` | plan → hero+stills → avatar/animate → assembly |
| `interactive-explainer` | `@interactive-explainer` | plan → stills → TTS → video → assemble ± bed |
| `music-video` | `@music-video` | plan/lyrics → song → align → stills → video → assemble |
| `illustrated-story-reel` | `@illustrated-story-reel` | plan → stills → tts or music → [video if p-video] → assemble |

## Agent rules

1. Complete `generation-diversity` ritual before any prompt work.
2. Install workflow tools via that skill’s **Prerequisites** (or `@pruna` once).
3. Parallelize independent curl jobs within a phase; never skip stills approval before paid video.
4. Recipe picker for humans: [WORKFLOW-RECIPES.md](../../../../docs/WORKFLOW-RECIPES.md).
