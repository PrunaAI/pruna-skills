# Approval red flags (before paid generation)

Pause and show assets (or ask) when any of these are true — regardless of workflow.

| Red flag | Risk | Required action |
|----------|------|-----------------|
| Plan not presented or no **approve plan** | Wrong story, cast, or style bible | Phase 0 — scene table + sample prompts |
| Stills not shown since last prompt edit | Silent no-op regen; wasted video credits | Phase A — paths in `stills/`; wait for **approve stills** |
| TTS / song not listened when narration drives video | Bad pacing, wrong lines in lip-sync | Phase A2 — `audio/narration_*.mp3` or `song.mp3` |
| Same turn: plan approval + video | User never saw plates | Split turns; never batch |
| **approve clips** missing before concat + bed | Bad VO buried under music | Phase C/D only after clip review |
| Visual mode, cast gender/voice, or continuity unclear | Identity drift, wrong pipeline | Ask; do not guess |
| Using `--yes-skip-*-gate` without user asking for automation | Bypasses human review | Confirm explicitly |
| Regen prompts without deleting stills/clips | Old assets reused | Delete targets or `--fresh` / `--regen-*` per [staged-generation-gate.md](./staged-generation-gate.md) |
| `voice_script` revised but avatar sources not deleted | Lip sync / dialogue mismatch | Delete `sources/` + `clips/` for that scene |
| **`POST /v1/predictions` without [random seed ritual](./random-seed-ritual.md) (SSoT)** | Duplicate outputs; copied example strings | Generate and state a ritual string first; log `ritual_seed` |
| **`PRUNA_API_KEY` or `REPLICATE_API_TOKEN` missing** | Cannot run API or runners | Stop; send signup links from [api-credentials.md](https://github.com/PrunaAI/pruna-skills/tree/main/shared/api-credentials.md) |

## When NOT to stall

The user already replied **approve plan**, **approve stills**, or **approve clips** for the current phase — proceed with that phase only.

## Common mistakes

| Mistake | Fix |
|---------|-----|
| End-to-end `--phase all` on first run | Default phased flow; skip gates only when user requests automation |
| Showing manifest JSON instead of media paths | User reviews JPEG/PNG/MP3/MP4 |
| Approving "looks good" without listing paths | Name `stills/hero.png`, scene ids, or clip filenames |
| Mixing bed before clip review | Concat first; bed after **approve clips** |
| Assuming regen picked up prompt edits | Delete affected files or use `--regen-stills` / `--regen-clips` |

See [staged-generation-gate.md](./staged-generation-gate.md) for phases and wording templates · [workflow-feedback-gates.md](./workflow-feedback-gates.md) for runner flags.
