---
name: requesting-generation-feedback
description: Use when running any Pruna workflow and about to call POST /v1/predictions, mix final audio, or skip user review.
license: MIT
metadata:
  version: "0.0.1"
---

# Requesting generation feedback

## Overview

Pruna video and replace jobs are expensive. This discipline skill governs **when to pause**, **what to show**, and **what wording to use** before any paid generation or final audio mux — regardless of which workflow skill is active.

Canonical phase rules: [staged-generation-gate.md](../../../../references/shared/staged-generation-gate.md)  
Per-workflow runners and flags: [workflow-feedback-gates.md](../../../../references/workflows/workflow-feedback-gates.md)

## When to Use

- Before the **first** `POST /v1/predictions` in a session
- Before **Phase B** video (`p-video`, `p-video-avatar`, `p-video-replace`, `p-video-animate`)
- Before **Phase D** assembly with background bed or full-song mux
- When the user says "just run it" but stills or clips have **not** been reviewed
- When art direction is ambiguous (visual mode, cast, continuity, bed yes/no)

**When NOT to use as an excuse to stall:** the user already replied **approve plan**, **approve stills**, or **approve clips** for the current phase — proceed with that phase only.

## Red flags

Stop and ask (or show assets) if any of these are true:

| Red flag | Risk | Required action |
|----------|------|-----------------|
| Plan not presented or no **approve plan** | Wrong story, cast, or style bible | Phase 0 — scene table + sample prompts |
| Stills not shown since last prompt edit | Silent no-op regen; wasted video credits | Phase A — paths in `stills/`; wait for **approve stills** |
| TTS / song not listened when narration drives video | Bad pacing, wrong lines in lip-sync | Phase A2 — `audio/narration_*.mp3` or `song.mp3` |
| Same turn: plan approval + video | User never saw plates | Split turns; never batch |
| **approve clips** missing before concat + bed | Bad VO buried under music | Phase C/D only after clip review |
| Visual mode, cast gender/voice, or continuity unclear | Identity drift, wrong pipeline | Ask; do not guess |
| Using `--yes-skip-*-gate` without user asking for automation | Bypasses human review | Confirm explicitly |
| Regen prompts without deleting stills/clips | Old assets reused | Delete targets or `--fresh` / `--regen-*` per [staged-generation-gate.md](../../../../references/shared/staged-generation-gate.md) partial regen table |
| `voice_script` revised but avatar sources not deleted | Lip sync / dialogue mismatch | Delete `sources/` + `clips/` for that scene |
| **`POST /v1/predictions` without [random seed ritual](../../../../references/shared/random-seed-ritual.md)** | Duplicate outputs; copied example seeds | Pick and state a random integer first; log `project_seed` |

## Workflow

1. **Classify the next phase** — plan (0), stills (A), audio prep (A2), video (B), assembly (C), final audio (D). See [staged-generation-gate.md](../../../../references/shared/staged-generation-gate.md).
2. **Present the right artifact** — table for Phase 0; file paths or thumbnails for stills; playable audio for A2; `clips/` for B.
3. **Use the wording templates** from staged-generation-gate (approve plan / stills / audio / clips).
4. **Cost warning before Phase B** — state that `p-video` / avatar / replace / animate are paid.
5. **Run only the approved phase** — default runners use `--phase stills` or `--phase song`; unlock video with `--approve-stills` (or `generation_status.json`).
6. **Partial regen** — fix one asset, not the whole pipeline; follow the decision tree in staged-generation-gate.

Runner flag cheat sheet: [workflow-feedback-gates.md](../../../../references/workflows/workflow-feedback-gates.md) (Runner flag reference + per-workflow commands).

## Common mistakes

| Mistake | Fix |
|---------|-----|
| End-to-end `--phase all` on first run | Default phased flow; skip gates only when user requests automation |
| Showing manifest JSON instead of media paths | User reviews JPEG/PNG/MP3/MP4 |
| Approving "looks good" without listing paths | Name `stills/hero.png`, scene ids, or clip filenames |
| Mixing bed before clip review | Concat first; bed after **approve clips** |
| Assuming regen picked up prompt edits | Delete affected files or use `--regen-stills` / `--regen-clips` |

## Related

- [staged-generation-gate.md](../../../../references/shared/staged-generation-gate.md) — phases, templates, partial regen
- [workflow-feedback-gates.md](../../../../references/workflows/workflow-feedback-gates.md) — workflow index + CLI flags
- [generation_gate.py](../../_shared/scripts/generation_gate.py) — `generation_status.json` helpers
- Scenario hub: [pruna-generative-pipeline](../pruna-generative-pipeline/SKILL.md)
