# Random seed ritual (SSoT — mandatory before every generation)

The random seed ritual is a lean [String Seed of Thought](https://pub.sakana.ai/ssot/) (DAG) protocol. **Every** Pruna generation — every prompt, every `POST /v1/predictions`, every scene row — starts here.

This prevents copy-pasting example strings (`k7Qm2xP9`, `482901`, …) and reduces accidental duplicate outputs across sessions.

## The ritual (do this first)

Before writing prompts, curl, or runner JSON:

1. **Generate a random string** in-agent (8–16 chars, mixed case + digits).
2. **State it in the turn** — e.g. *"Ritual seed: k7Qm2xP9."*
3. **Derive prompt choices** from the string — sum char codes, mod N — pick axes from [generation-diversity.md](./generation-diversity.md) (`aspect_ratio`, `camera_tag`, `render_category_tag`, …).
4. **Write the prompt** using [explicit prompt structure](./generation-diversity.md#explicit-prompt-structure-required) and derived axes.
5. **Log** `ritual_seed`, axes chosen, and prediction id in the manifest.

**Do not pass the ritual string to API `seed`.** API runs without `seed` unless the user explicitly requests reproducibility (`api_seed`).

**Never** proceed to `POST /v1/predictions` without completing steps 1–2 in the same turn (unless the user supplied an explicit `api_seed` — see below).

## Reuse rules

| Situation | Action |
|-----------|--------|
| **New hero / independent still / mood-board panel** | Fresh ritual string |
| **Same-brief slop retry** | Reuse same `ritual_seed`; note `retry_ritual_seed` in manifest |
| **Same character arc** | Lock **hero plate URL** + cast descriptor; reuse `ritual_seed` only on same-brief regen |
| **User says "lock seed" / provides integer** | Pass **their** number as `api_seed` → `input.seed`; skip new ritual for that chain |

Character continuity = approved plate URL + cast descriptor — **not** the ritual string on the API.

## Anti-patterns

| Wrong | Right |
|-------|--------|
| Copy example strings from SKILL.md | Fresh ritual string each independent generation |
| Pass ritual string as API `seed` | Ritual is planning-only; `api_seed` only when user asks |
| One ritual string for entire mood board | New ritual per independent **`p-image`** |
| Skip ritual because API `seed` is optional | Ritual always; API omits `seed` by default |

## Example (agent turn)

> **Ritual seed: k7Qm2xP9.**  
> Derived: aspect_ratio 16:9, camera_tag fish-eye, render_category_tag cartoon_anime_fantasy.  
> Prompt: Disco ball reflections on an otter DJ scratching vinyl at a packed 1970s roller rink, fish-eye lens, glitter confetti mid-air, funky energy.  
> Identity locks on approved plate URL for avatar clips.  
> …then curl / runner **without** `"seed"` in `input`.

## Manifest snippet

```json
{
  "ritual_seed_policy": "ssot_dag_before_every_generation",
  "ritual_seed": "k7Qm2xP9",
  "seed_log": [
    { "phase": "hero_p_image", "ritual_seed": "k7Qm2xP9", "creature_tag": "otter_dj", "setting_tag": "1970s_roller_rink", "prompt_hash": "…" },
    { "phase": "scene_2_avatar", "ritual_seed": "k7Qm2xP9", "scene_id": 2 }
  ]
}
```

## Where this applies

All Pruna generation skills and workflow runners — **every invocation**:

- **`p-image`**, **`p-image-edit`**, **`p-image-try-on`**, **`p-image-upscale`**
- **`p-video`**, **`p-video-avatar`**, **`p-video-animate`**, **`p-video-replace`**

## Related

- [generation-diversity.md](./generation-diversity.md) — ritual + axis rotation + sum-mod derivation
- [realistic-persona-showcase.md](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/core/realistic-persona-showcase/SKILL.md) — persona planning
- [staged-generation-gate.md](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/core/staged-generation-gate/SKILL.md) — approval phases
- [requesting-generation-feedback/SKILL.md](../../requesting-generation-feedback/SKILL.md) — red flags
