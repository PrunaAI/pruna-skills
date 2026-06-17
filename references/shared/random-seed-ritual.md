# Random seed ritual (mandatory before every generation)

**Every time** an agent uses a Pruna generation skill — every prompt, every `POST /v1/predictions`, every scene row — **stop and pick a random integer first**, then build the API payload.

This prevents copy-pasting example seeds (`482901`, `771204`, …) and reduces accidental duplicate outputs across sessions.

## The ritual (do this first)

Before writing curl, runner JSON, or calling the API:

1. **Think of a random integer** — e.g. six digits, range **100000–999999** (or use `shuf -i 100000-999999 -n 1` / language RNG when executing locally).
2. **Say it in the turn** when planning or confirming — e.g. *"Ritual seed for this hero: 384729."*
3. **Assign it** per the rules below → `seed` in `input`, or `project_seed` in manifest.
4. **Log it** in the manifest / generation log with the prompt and prediction id.

**Never** proceed to `POST /v1/predictions` without completing steps 1–2 in the same turn (unless the user supplied an explicit seed — see exceptions).

## How to assign the number

| Situation | Use the ritual number as |
|-----------|--------------------------|
| **New hero / new identity / new playground example** | `seed` on that **`p-image`** call → becomes **`project_seed`** |
| **Same character — hero regen** (same prompt, fix slop) | Reuse existing **`project_seed`** — do **not** pick a new number |
| **Same character — all `p-video-avatar` clips** | Same **`project_seed`** on every clip unless A/B testing motion |
| **Same character — `p-image-try-on` after approved hero** | Same **`project_seed`** as hero when the API accepts it; identity comes from the plate URL |
| **Independent parallel stills** (mood board, no shared identity) | **New ritual number per panel** |
| **Slop-gate retry** (same scene, new attempt) | **New ritual number**; note `retry_seed` in manifest |
| **User says "lock seed" / provides integer** | Use **their** number; skip new ritual for that chain |
| **Model has no `seed` param** | Still pick and log as **`run_id`** / `ritual_seed` in manifest |

## Anti-patterns

| Wrong | Right |
|-------|--------|
| Copy `482901` from SKILL.md examples | Fresh ritual number each new generation |
| Reuse yesterday's manifest seed for a new project | New ritual at project start |
| Skip ritual because "seed is optional" | Ritual always; omit API `seed` only when model docs say so and user wants random backend |
| One seed for entire mood board exploration | New ritual per independent **`p-image`** |
| New random seed mid-chain for same avatar character | Lock **`project_seed`** through avatar clips |

## Example (agent turn)

> **Ritual seed: 518263.**  
> Plan: photoreal loft hero, 9:16, `project_seed` 518263 for hero + three avatar clips.  
> …then curl / runner with `"seed": 518263`.

## Manifest snippet

```json
{
  "ritual_seed_policy": "pick_before_every_generation",
  "project_seed": 518263,
  "seed_log": [
    { "phase": "hero_p_image", "seed": 518263, "prompt_hash": "…" },
    { "phase": "scene_2_avatar", "seed": 518263, "scene_id": 2 }
  ]
}
```

## Where this applies

All models that accept **`seed`** or benefit from run traceability:

- **`p-image`**, **`p-image-edit`** (when supported), **`p-image-try-on`**, **`p-image-upscale`**
- **`p-video`**, **`p-video-avatar`**, **`p-video-animate`**, **`p-video-replace`**

Workflow skills, tool skills, and plan runners — **every invocation**.

## Related

- [generation-diversity.md](./generation-diversity.md) — all models: ritual + axis rotation
- Persona planning: [realistic-persona-showcase.md](./realistic-persona-showcase.md)
- Phases and approval: [staged-generation-gate.md](./staged-generation-gate.md)
- Red flags: [requesting-generation-feedback/SKILL.md](../../guides/workflows/router/requesting-generation-feedback/SKILL.md)
