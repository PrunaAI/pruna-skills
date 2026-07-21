# Generation quality checklist hub

Use this as the shared quality gate across models and workflows.
Run the **Core checklist** for every generation job, then run the model-specific checklist.

## Who applies these checklists?

**The coding agent** — by **opening the real output files** (images, video, or audio) and reviewing them with vision. These checklists are **not** automated test scripts. There is no separate scoring service: the agent reads each item and judges pass or fail from what it sees and hears.

Typical flow:

1. **Generate or download** the asset to a local path (`stills/`, `clips/`, etc.).
2. **Inspect the file** — view the image, watch the video clip, or listen to narration when the checklist covers audio.
3. Run the **Core checklist** (below), then the **model-specific checklist** for that job.
4. **If something fails** — note which items failed, adjust prompt / settings / seed, and regenerate **only that asset** (do not advance to expensive video steps on a bad still).
5. **If it passes** — show the user the file paths (and previews when helpful). In workflows, still follow [approval gates](#approval-gates-workflows): agent checklist review happens **before** you ask the user to approve stills or clips.

The user's **approve plan / approve stills / approve clips** gates are separate. Agent checklists catch obvious problems early so the user is not asked to sign off on broken outputs.

Maintenance rule: keep tool/workflow mapping only in this file to avoid link drift.

## Match map (tool -> checklist -> workflows)

| Tool/model | Checklist | Common workflows |
|------------|-----------|---------------|
| `p-image` | [`p-image-quality-checklist.md`](../image/p-image-quality-checklist.md) · persona bar: [`realistic-persona-showcase.md`](../shared/realistic-persona-showcase.md) | `image-to-video`, `narrated-multi-scene`, [`WORKFLOW-RECIPES`](../../docs/WORKFLOW-RECIPES.md) |
| `p-image-edit` | [`p-image-edit-quality-checklist.md`](../image/p-image-edit-quality-checklist.md) | `avatar-single-scene`, `avatar-multi-scene`, [`WORKFLOW-RECIPES`](../../docs/WORKFLOW-RECIPES.md) |
| `p-image-upscale` | [`p-image-upscale-quality-checklist.md`](../image/p-image-upscale-quality-checklist.md) | `image-to-video`, `narrated-multi-scene`, [`WORKFLOW-RECIPES`](../../docs/WORKFLOW-RECIPES.md), [`generate_upscale_comparison.pyagent curl/ffmpeg (no shared scripts)) |
| `p-image-try-on` | [`p-image-try-on-quality-checklist.md`](../image/p-image-try-on-quality-checklist.md) | [`WORKFLOW-RECIPES`](../../docs/WORKFLOW-RECIPES.md), `p-image-try-on`, [`realistic-persona-showcase.md`](../shared/realistic-persona-showcase.md) |
| `p-video` | [`p-video-quality-checklist.md`](../video/p-video-quality-checklist.md) | `image-to-video`, `narrated-multi-scene`, `interactive-explainer`, `visual-transition-reel`, [`WORKFLOW-RECIPES`](../../docs/WORKFLOW-RECIPES.md) |
| `p-video-avatar` | [`p-video-avatar-quality-checklist.md`](../video/p-video-avatar-quality-checklist.md) · persona bar: [`realistic-persona-showcase.md`](../shared/realistic-persona-showcase.md) | `avatar-single-scene`, `avatar-multi-scene`, `interactive-explainer`, [`WORKFLOW-RECIPES`](../../docs/WORKFLOW-RECIPES.md) |
| `p-video-animate` | [`p-video-animate-quality-checklist.md`](../video/p-video-animate-quality-checklist.md) | `avatar-multi-scene`, [`WORKFLOW-RECIPES`](../../docs/WORKFLOW-RECIPES.md) |
| `p-video-replace` | [`p-video-replace-quality-checklist.md`](../video/p-video-replace-quality-checklist.md) | `p-video-replace`, [ffmpeg hstack slider (see workflow SKILL) curl/ffmpeg (no shared scripts)) |
| `music-2.5` + music video assembly | [`music-video-quality-checklist.md`](../workflows/music-video-quality-checklist.md) | `music-video`, `music-2.5` |

## Core checklist (all models)

- **[Generation diversity](./generation-diversity.md)** — ritual seed, explicit prompts, visual variety; rotate scenario axes on **every** model (image, video, try-on, avatar, …).
- Goal and acceptance criteria are explicit (what "good" looks like is written down).
- Input assets are valid and licensed (URL/file reachable, rights cleared).
- Prompt and settings match the intended output format (`aspect_ratio`, duration, resolution, style lock). **Video default:** `720p`, `24` fps unless the brief asks for final `1080p` / `48`.
- Output contains no accidental watermarks, UI overlays, or stray text unless requested.
- Brand, legal, and safety constraints are satisfied before handoff.
- Manifest/log captures model, input fields, prediction id, output URL, and **`ritual_seed`** for traceability.

## Model-specific checklists

- [`p-image-quality-checklist.md`](../image/p-image-quality-checklist.md)
- [`p-image-edit-quality-checklist.md`](../image/p-image-edit-quality-checklist.md)
- [`p-image-upscale-quality-checklist.md`](../image/p-image-upscale-quality-checklist.md)
- [`p-image-try-on-quality-checklist.md`](../image/p-image-try-on-quality-checklist.md)
- [`p-video-quality-checklist.md`](../video/p-video-quality-checklist.md)
- [`p-video-avatar-quality-checklist.md`](../video/p-video-avatar-quality-checklist.md)
- [`p-video-animate-quality-checklist.md`](../video/p-video-animate-quality-checklist.md)
- [`p-video-replace-quality-checklist.md`](../video/p-video-replace-quality-checklist.md)
- [`music-video-quality-checklist.md`](../workflows/music-video-quality-checklist.md)

## Visual variety

Before **any** generation, run [generation-diversity.md](./generation-diversity.md) including the [Variety checklist](./generation-diversity.md#variety-checklist-before-first-api-call). Persona/playground bar: [realistic-persona-showcase.md](../shared/realistic-persona-showcase.md).

## Approval gates (workflows)

Human-in-the-loop phases for multi-step workflows. **Video and replace jobs are expensive** — gate on approved stills before any `p-video-*` call. Final audio (bed mix, full-song mux) runs only after clip review.

| Phase | Models | Cost | User interaction |
|-------|--------|------|------------------|
| **0 — Plan** | none | free | Present scene table, cast, scripts, `style_bible`; explicit **approve plan / go** |
| **A — Stills** | `p-image`, `p-image-edit` | low | Show hero + start/end plates; run checklists; **approve stills** |
| **A2 — Audio prep** | Gemini TTS, Music 2.5, WhisperX align | low–medium | **Listen / read** narration or song; fix copy before video |
| **B — Video** | `p-video`, `p-video-avatar`, `p-video-animate`, `p-video-replace` | **high** | Only after Phase A approval; **approve clips** before assembly |
| **C — Assembly** | local ffmpeg concat / slider scripts | free | Review concat (embedded VO); compare MP4s before final mux |
| **D — Final audio** | Stable Audio bed, bed mix, full-song mux | low | Only after Phase B clip approval |

**Never** run Phase B in the same turn as Phase A without showing stills and waiting for approval. Parallelize within a phase, not across phases.

### Red flags (pause before paid generation)

| Red flag | Required action |
|----------|-----------------|
| Plan not presented or no **approve plan** | Phase 0 — scene table + sample prompts |
| Stills not shown since last prompt edit | Phase A — paths in `stills/`; wait for **approve stills** |
| Same turn: plan approval + video | Split turns; never batch |
| **approve clips** missing before concat + bed | Phase C/D only after clip review |
| Using `--yes-skip-*-gate` without user asking for automation | Confirm explicitly |
| Regen prompts without deleting stills/clips | Delete targets or `--fresh` / `--regen-*` |
| Missing `PRUNA_API_KEY` / `REPLICATE_API_TOKEN` | Stop; [api-credentials.md](../shared/api-credentials.md) |

**When not to stall:** the user already replied **approve plan**, **approve stills**, or **approve clips** for the current phase — proceed with that phase only.

Runner `--approve-*` flags and per-workflow commands: [workflow-feedback-gates.md](../workflows/workflow-feedback-gates.md).

## Workflow note

For multi-scene projects, run these checks per scene and add a final continuity pass
(style, character identity, voice, and pacing consistency across scenes).

**Narrated cinematic B-roll:** validate [scene anchor triple](../video/scene-anchor-triple.md) inputs before `p-video` — start still, end still, uploaded narration URL per row.
