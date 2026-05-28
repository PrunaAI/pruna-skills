# Staged generation gate

Human-in-the-loop phases for workflow skills and plan runners. **Video and replace jobs are expensive** — gate on approved stills before any `p-video-*` call.

See also: [parallel-execution.md](./parallel-execution.md) Phase 0, [generation-quality-checklists.md](./generation-quality-checklists.md).

## Phases

| Phase | Models | Cost | User interaction |
|-------|--------|------|------------------|
| **0 — Plan** | none | free | Present scene table, cast, prompts; explicit **approve / go** |
| **A — Stills** | `p-image`, `p-image-edit` | low | Show reference + source plates; run checklists |
| **B — Video** | `p-video-avatar`, `p-video-animate`, `p-video-replace`, `p-video` | **high** | Only after Phase A approval |
| **C — Render** | local ffmpeg / slider scripts | free | Compare MP4s; review before concat |

## Agent rules

1. **Never** run Phase B in the same turn as Phase A without showing stills and waiting for approval.
2. **Parallelize within a phase**, not across phases.
3. **Per-scene approval** for persona ladders and face recasts — show JPEG paths or thumbnails.
4. **Regeneration loop** — reject → rerun only the still (`p-image` / edit), not video.
5. Run model checklists on every still before Phase B.

## Wording templates

After Phase A:

> Here are the reference stills for scene N (`references/sceneNN_*.jpeg`, `stills/sceneNN_source_plate.jpeg`). Reply **approve stills** to run video jobs, or tell me what to fix.

Before Phase B (cost warning):

> Phase B will call `p-video-avatar` / `p-video-replace` (paid). Confirm you have reviewed the stills.

## Plan runners

Default **`--phase stills`**. Phase B requires **`--approve-stills`** or `"phase_a_approved": true` in `generation_status.json`.

```bash
python3 ./scripts/run_from_plan.py --plan ./my-plan.json --out-dir ./output/reel --phase stills
python3 ./scripts/run_from_plan.py --plan ./my-plan.json --out-dir ./output/reel --phase video --approve-stills
python3 ./scripts/run_from_plan.py --plan ./my-plan.json --out-dir ./output/reel --phase render
python3 ./scripts/run_from_plan.py --plan ./my-plan.json --out-dir ./output/reel --phase all --yes-skip-stills-gate
```

## Anti-patterns

- Full `--fresh` end-to-end without still review
- Batch `p-video-replace` before reference QA
- Same-turn plan approval + video generation
