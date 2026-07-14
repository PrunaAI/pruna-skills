---
name: p-image
description: Use when the user wants the fastest text-to-image stills, quick draft photos, mood boards, or bulk panels where good quality and extremely low latency matter more than maximum photoreal fidelity.
license: MIT
metadata:
  version: "0.0.2"
  pruna_model: p-image
---

# p-image (Pruna)

**Good quality, extremely fast** text-to-image via Pruna P-API. For **high-quality fast photoreal** stills, use [p-image-ideogram](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/p-image-ideogram/skills/p-image-ideogram/SKILL.md) (Replicate deployment) instead. Full parameters: [p-image model docs](https://docs.api.pruna.ai/guides/models/p-image).

## When NOT to use

- High-fidelity photoreal hero plates or editorial portraits → [p-image-ideogram](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/p-image-ideogram/skills/p-image-ideogram/SKILL.md)
- Editing an existing image → [p-image-edit](../p-image-edit/SKILL.md)
- Virtual try-on on a person plate → [p-image-try-on](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/p-image-try-on/skills/p-image-try-on/SKILL.md)

**Dynamic persona & scenarios:** [realistic-persona-showcase.md](./references/realistic-persona-showcase.md) · examples: [example-prompt.md](./references/realistic-persona-example-prompt.md)

Shared HTTP patterns: [pruna-api.md](./references/pruna-api.md) (upload, [poll](#poll), [download](#download))

## HTTP (curl)

### Create (async — recommended)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-image' \
  -d '{
    "input": {
      "prompt": "Disco ball reflections on an otter DJ scratching vinyl at a packed 1970s roller rink, fish-eye lens, glitter confetti mid-air, funky energy",
      "aspect_ratio": "9:16"
    }
  }'
```

Poll and download: [pruna-api.md](./references/pruna-api.md#poll).

Complete the [random seed ritual](./references/random-seed-ritual.md) (SSoT) before writing prompts — **do not** pass the ritual string as API `seed`. Optional `api_seed` only when the user requests reproducibility.

### Create (sync — quick test only)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-image' \
  -H 'Try-Sync: true' \
  -d '{"input":{"prompt":"Corgi cowboy lassoing a runaway taco truck through Monument Valley dust storm, pulp western poster energy, dynamic diagonal composition","aspect_ratio":"16:9"}}'
```

## Before generating

1. **[Generation diversity](./references/generation-diversity.md)** — ritual seed (SSoT) + [explicit prompt structure](./references/generation-diversity.md#explicit-prompt-structure-required) (specific people/animals, objects, actions, setting). **`p-image` has no prompt upsampling** — follow [text hygiene](./references/generation-diversity.md#text--typography-by-model) unless routing to `p-image-ideogram` for typography. **Multi-example batches:** different **`aspect_ratio`** per still.
2. Confirm **`prompt`** and **`aspect_ratio`** with the user. Run [p-image-quality-checklist.md](./references/p-image-quality-checklist.md) on outputs before downstream steps.

## Production quality — photoreal personas

Default demos often look **AI sloppy** (generic white background, plastic skin, same face). For **`p-video-avatar`**, **`p-image-try-on`**, or public playground examples, art-direct plates explicitly:

| Goal | Prompt discipline |
|------|-------------------|
| **Photoreal** | `documentary portrait, natural skin pores, not CGI, not illustration` |
| **Stylized / anime** | Named `visual_style_tag` — cinematic cel, cyberpunk anime, clay, CG 3D; mouth visible for avatars |
| **Diverse cast** | Specific age, ethnicity, archetype — rotate across example sets |
| **Dynamic worlds** | Named setting + lighting + **camera angle** — not one template repeated |
| **Scenario matrix** | Plan medium × angle × setting × **aspect_ratio** per row before generating |
| **Avatar-ready** | Face large; **mouth clearly visible**; hands away from mouth |
| **Try-on-ready** | Full-body or region coverage for garment type (feet for shoes, etc.) |

Full scenario generation (photographic styles, anime sub-styles, camera ladder, 8-slot matrix): [realistic-persona-showcase.md](./references/realistic-persona-showcase.md). Variety planning: [visual-variety-bible.md](https://github.com/PrunaAI/pruna-skills/tree/main/references/shared/visual-variety-bible.md).

Lock **hero plate URL** at hero generation when the same identity continues to **`p-image-edit`**, **`p-image-try-on`**, or **`p-video-avatar`**.

## Required input

- `prompt` (string)

## Common optional fields

- `aspect_ratio`: `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`, `custom` (with `width` / `height` multiples of 16, 256–1440)
- `seed`, `lora_weights`, `lora_scale`, `hf_api_token`, `disable_safety_checker`

**No prompt upsampling** on this model — keep prompts concrete per [generation-diversity](./references/generation-diversity.md#text--typography-by-model). For dense readable typography, use [p-image-ideogram](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/p-image-ideogram/skills/p-image-ideogram/SKILL.md).

## Example: synchronous

(See **Create (sync)** above.)

## Example: asynchronous (batch / multi-panel)

Omit `Try-Sync`. For N panels with no shared dependency, **POST all jobs in parallel**, then poll every `get_url`. See [parallel-execution.md](https://github.com/PrunaAI/pruna-skills/tree/main/references/shared/parallel-execution.md).

## Typical next steps

- Refine or composite: [p-image-edit](../p-image-edit/SKILL.md)
- Virtual try-on on a photoreal person plate: [p-image-try-on](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/p-image-try-on/skills/p-image-try-on/SKILL.md) — see [realistic-persona-showcase.md](./references/realistic-persona-showcase.md)
- Upscale output: [p-image-upscale](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/p-image-upscale/skills/p-image-upscale/SKILL.md)
- Animate still: [p-video](../p-video/SKILL.md) — prefer [scene anchor triple](https://github.com/PrunaAI/pruna-skills/tree/main/references/shared/scene-anchor-triple.md) (`image` + `last_frame_image` + `audio`) for narrated beats; or [p-video-avatar](../p-video-avatar/SKILL.md) for talking head
- Scripted workflows (intake first): [avatar-single-scene](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/avatar-single-scene/skills/avatar-single-scene/SKILL.md), [avatar-multi-scene](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/avatar-multi-scene/skills/avatar-multi-scene/SKILL.md)
- Full pipeline: [pruna-generative-pipeline](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/pruna-generative-pipeline/skills/pruna-generative-pipeline/SKILL.md)

## Related workflow

Avatar + animate reels: [avatar-multi-scene](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/avatar-multi-scene/skills/avatar-multi-scene/SKILL.md) — bundled scripts live in workflow skills, not here.
