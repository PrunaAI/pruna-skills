# Parallel async execution (agents)

**Scope:** multi-scene **workflow** skills only (`narrated-multi-scene`, `visual-transition-reel`, `avatar-multi-scene`, `interactive-explainer`, `music-video`, and similar). Single-clip tools (`p-video`, `image-to-video`, one-shot `p-video-avatar`) must **not** import this doc as permission to expand into multi-scene orchestration.

Default for those multi-step workflows: **async predictions + parallel fan-out** wherever steps do not depend on each other's outputs. In Cursor and similar agent hosts, **dispatch subagents** for independent lanes and merge results into one manifest.

Shared HTTP basics: [pruna-api.md](./pruna-api.md). Credentials and privacy: [agent-safety.md](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/core/agent-safety/SKILL.md).

**Human-in-the-loop:** Do not start paid video phases until stills pass review. See [staged-generation-gate.md](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/core/staged-generation-gate/SKILL.md).

## Defaults

| Rule | Guidance |
|------|----------|
| **Async first** | Omit `Try-Sync` on **all** production predictions. Poll `get_url` until `succeeded` or `failed`. |
| **Parallel when independent** | If job B does not need job A's `generation_url`, **start both** before polling either. |
| **Phased when dependent** | Finish phase N (all jobs in the phase) before starting phase N+1. |
| **Subagents for lanes** | One subagent per independent scene/lane when 2+ scenes; parent owns manifest, confirmation gate, and assembly. |
| **Sync only for probes** | `Try-Sync: true` is OK for a **single** quick image test—not for video, avatar, or batch runs. |

## Phase model (typical multi-scene avatar)

```text
Phase 0 — intake + confirmation (sequential; no API)
Phase 1 — hero: p-image → slop gate → anchor URL              (sequential)
Phase 2 — per-scene stills: p-image-edit × N                  (parallel across scenes)
Phase 3 — slop gate on scene stills                           (parallel review; regen failed lanes only)
Phase 4 — p-video-avatar × N                                  (parallel; all approved still URLs + scripts ready)
Phase 5 — download + assembly                                 (sequential ordering only)
```

**Multi-scene `p-video` (B-roll):** after shared uploads, **all scene predictions in one parallel batch** when every scene’s `image` / `last_frame_image` URL is known upfront.

**Multi-scene `p-video` (frame chain):** when scene *i+1* **`image`** must equal scene *i* **`last_frame_image`** and end stills are **not** pre-planned, run **phased** — finish scene *i*, extract or approve end still, upload, then start scene *i+1*. When **`p-image-edit`** produces both start and end stills for all scenes before any video job, revert to **parallel** video batch. See [p-video](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/p-video/skills/p-video/SKILL.md) and [narrated-multi-scene](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/narrated-multi-scene/skills/narrated-multi-scene/SKILL.md).

**Multi-scene narration:** [Gemini TTS](../../gemini-3.1-flash-tts/SKILL.md) per scene can run **in parallel** after scripts are approved. Upload all audio URLs, then **`p-video`** with **`image` + `last_frame_image` + `audio`** per scene ([scene-anchor-triple.md](./scene-anchor-triple.md)). Post-mux is fallback only. Optional [Stable Audio](../../stable-audio-2.5/SKILL.md) bed after concat — [audio-post-production.md](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/core/audio-post-production/SKILL.md).

**Multi-scene `p-video-animate` (motion transfer):** see [avatar-multi-scene](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/avatar-multi-scene/skills/avatar-multi-scene/SKILL.md) **`animate`** rows. After confirmation: parallel uploads → optional parallel `p-image-edit` per lane → **`p-video-animate` × N in one batch** → parallel slider renders → sequential concat.

**Mood board (Recipe A):** all **`p-image`** panels with no shared anchor → **parallel async** from the start.

## Parallel API pattern (shell / script)

1. **Create** — `POST /v1/predictions` for every job in the current phase **without waiting** between creates. Store each `{ id, get_url, scene_label }` in the manifest.
2. **Poll** — Loop all open jobs (sleep 5–15s). Mark `succeeded` / `failed`; retry failed lanes individually.
3. **Advance** — When every job in the phase succeeds, upload outputs if needed and start the next phase.

Example shape (conceptual):

```bash
# Phase 5: create all avatar jobs (no Try-Sync)
for scene in 1 2 3 4 5; do
  curl -s -X POST 'https://api.pruna.ai/v1/predictions' \
    -H 'Content-Type: application/json' \
    -H "apikey: ${PRUNA_API_KEY}" \
    -H 'Model: p-video-avatar' \
    -d @"scene${scene}_avatar_payload.json" \
    > "scene${scene}_avatar_create.json" &
done
wait
# Then poll all get_url values until none are pending
```

Generation packages in this repo should **emit parallel creates + batch poll**, not one scene at a time, unless the user explicitly wants serial execution for cost control.

## Subagent delegation (Cursor / agent hosts)

Use subagents when **2+ independent lanes** exist after the confirmation gate.

| Parent agent | Subagent (one per lane) |
|--------------|-------------------------|
| Intake, cast ledger, scene table, read-through, **confirmation** | — |
| Writes manifest skeleton + phase plan | — |
| Merges URLs, prediction ids, pass/fail into manifest | Returns lane result JSON |
| Assembly script + final delivery | — |

**Good splits**

- **Per-scene still lane:** upload (if needed) → `p-image-edit` → slop gate → approved file URL.
- **Per-scene avatar lane:** `p-video-avatar` async create + poll + download (after still URL is in manifest).
- **Per-scene B-roll lane:** `p-video` async create + poll + download.
- **Per-scene motion-transfer lane:** optional repose (`p-image-edit`) → `p-video-animate` async create + poll + download → slider comparison render.

**Launch in parallel** — e.g. five scenes → five subagents in one message; do not walk scenes serially if lanes are independent.

**Parent must**

- Pass each subagent: scene row, hero/anchor URL, `ritual_seed`, cast ledger slice, output paths — **never** API keys in task text ([agent-safety.md](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/core/agent-safety/SKILL.md)). Prefer parent-owned API calls when the host cannot inject secrets safely.
- Refuse to start subagents until the user has **explicitly confirmed** the script/plan.
- Reconcile partial failures: rerun **only** failed lanes.

**Avoid**

- Subagents before confirmation (wastes cost; violates workflow skills).
- Splitting a **single** dependency chain across subagents (hero must finish before scene edits).
- Duplicate manifest writes without merge (use one parent-owned `manifest.md` / JSON).
- Forwarding `PRUNA_API_KEY` / `REPLICATE_API_TOKEN` into prompts, manifests, or subagent briefs.

## When to stay sequential

- **Hero / identity anchor** must exist before any `p-image-edit` from that character.
- **User asked for serial** execution to limit concurrent spend or rate limits.
- **Regeneration** after slop failure — rerun that lane only, not the whole project.

## Checklist for agents

- [ ] Confirmation received before first `POST /v1/predictions`
- [ ] Async used for every video / avatar / batch image job
- [ ] Independent jobs in the same phase started together
- [ ] Subagents used for 2+ scene lanes when the host supports them
- [ ] Manifest records all parallel job ids and per-lane status
- [ ] Assembly order matches approved scene table (parallel gen ≠ parallel stitch)
