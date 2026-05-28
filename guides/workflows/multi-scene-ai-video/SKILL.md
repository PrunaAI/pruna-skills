---
name: multi-scene-ai-video
description: Produces multiple Pruna p-video clips from a scene list defined by intake Q&A—per-scene prompts and durations (or I2V/audio per scene), async parallel jobs with optional subagents per scene, then assembly outside Pruna. Use when the user wants episodic B-roll, chaptered promos, or story beats without talking-avatar (no p-video-avatar).
metadata:
  version: "0.0.1"
---

# Multi-scene AI video (Pruna `p-video` only)

Each scene = one **`p-video`** job (same model, separate predictions). Assembly is **outside** Pruna (your editor or pipeline). No **`p-video-avatar`** in this workflow.

See [p-video](../../../tools/video/p-video/SKILL.md) and [references/pruna-api.md](../../../references/pruna-api.md).

## Intake: ask before generating

**Do not** start scene 1 until the **whole** scene plan exists in writing (manifest or table):

| Topic | Questions |
|-------|-----------|
| **Story** | Order of scenes (1…N)? What changes between scenes (location, time, product, emotion)? |
| **Per scene *i*** | Primary `prompt` (or I2V: which reference image)? Target `duration`? `resolution` / `fps` / `draft`? |
| **Continuity** | Should lighting or subject match previous scene (note in prompt text)? |
| **Audio** | Any scene use uploaded `audio` (clip length = audio length)? |
| **Global** | Default `aspect_ratio` for text-only scenes? Global `seed` policy (per scene vs none)? |
| **Runtime** | Target total duration after assembly (rough cap guides per-scene lengths)? |
| **Assembly** | Who concatenates and mixes (tool agnostic)? |

Ask follow-ups until every scene row has enough to build `input` without guessing.

### Scene table (template — fill during intake)

| `#` | Prompt summary | Mode (T2V / I2V / audio) | Duration | Notes |
|-----|------------------|--------------------------|----------|--------|
| 1 | | | | |
| 2 | | | | |

## Workflow (after intake)

1. **Shared uploads** — Upload any reuse images or audio to `/v1/files`; note URLs per scene.
2. **Generate in parallel** — After uploads, **`POST /v1/predictions`** for **every scene row at once** (`Model: p-video`, each row’s `input`). Use **async** (no `Try-Sync`); poll **all** `get_url` until every job is `succeeded` or `failed`; retry failed scenes only. Download each `generation_url`. Prefer **one subagent per scene** for create + poll + download when 2+ scenes ([parallel-execution.md](../../../references/parallel-execution.md)).
3. **Review** — If a scene fails intent, adjust prompt and re-run **that** scene only.
4. **Assembly** — Join clips in scene order; handle audio crossfades in your toolchain.
5. **Manifest** — Intake table + every prediction id, prompts, outputs, retries.

## Related

- Single clip: [single-scene-ai-video](../single-scene-ai-video/SKILL.md)
- Talking avatars: [multi-scene-avatar-video](../multi-scene-avatar-video/SKILL.md)
- Generic chain: [pruna-generative-pipeline](../pruna-generative-pipeline/SKILL.md)
