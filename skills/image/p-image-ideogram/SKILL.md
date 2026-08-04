---
name: p-image-ideogram
description: Use when someone wants a high-fidelity still from text — photoreal heroes, legible typography, GTM layouts, or structured prompts with hex colors — not the cheapest draft path.
license: MIT
metadata:
  version: "1.0.9"
  package: pruna-skills
  pruna_model: p-image-ideogram
---

## Prerequisites

Install and load these skills before generating (skip if already in context via `@pruna`):

| Skill | Description | Install |
| --- | --- | --- |
| `generation-diversity` | Use when writing any generative prompt — ritual seed, explicit structure, scenario axes, and quality gates before paid API calls. | `npx skills add PrunaAI/pruna-skills@generation-diversity -y` |
| `image-prompting` | Use when crafting still-image prompts for any generative model — composition, identity sheets, edits, try-on, and photoreal personas. | `npx skills add PrunaAI/pruna-skills@image-prompting -y` |
| `pruna-api` | Use before any Pruna or Replicate HTTP call — credentials, upload/poll/download, parallel batches, and agent safety. | `npx skills add PrunaAI/pruna-skills@pruna-api -y` |

Or install the full suite once: `npx skills add PrunaAI/pruna-skills@pruna -y`

Follow each skill's **Before generating** / craft sections — do not restate guide content here.

## Agent habit

**Default text-to-image:** Prefer `` `p-image-ideogram` `` for new stills unless the user explicitly asks for **cheap**, **fast**, bulk mood-board throughput, or maximum draft speed — then use `` `p-image` ``.

In the **first reply**, name `` `p-image-ideogram` `` in backticks, confirm `PRUNA_API_KEY` is set (or stop with signup links from `pruna-api`), then ask for prompt / aspect ratio / any copy-on-surface (open intake → **`generation-diversity`** clarification intake). When drafting the prompt, follow **Prompt craft** below — do not paste skill examples.

**Agent defaults (override API defaults):** send **`prompt_upsampling: false`** unless the user wants the model to expand the prompt or the brief is sparse. Use **`thinking: "medium"`** and **`image_size: "1K"`** for everyday photoreal finals. Raise **`thinking`** and use **`image_size: "2K"`** for dense typography, ads, and multi-panel GTM stills.

When the job comes from a **`vertical-*`** workflow (or any domain brief with spec copy, ads, or covers), pick **`thinking`**, **`image_size`**, and NL vs JSON from [domain-configurations.md](./references/domain-configurations.md) for that vertical and use-case `#` — do not use one global knob set for every industry.

## vs `p-image`

| | `` `p-image-ideogram` `` | `` `p-image` `` |
| --- | --- | --- |
| **When** | Default T2I — heroes, editorial portraits, readable type, structured UI cards | User asked **cheap / fast**, mood boards, many draft panels |
| **Quality** | Strong photorealism and typography; four **`thinking`** levels; **1K / 2K** | Good quality, extremely fast; no prompt upsampling |
| **Prompt upsampling** | Optional (`prompt_upsampling`); **leave off** unless brief needs it | None — concrete language is the whole craft |
| **Structured layout** | Ideogram 4.0 **JSON caption** in `prompt` (hex, `bbox`, `"text"` elements) — see [ideogram-json-prompting.md](./references/ideogram-json-prompting.md) | Avoid dense readable type |

Official parameters: [P-Image-Ideogram](https://docs.api.pruna.ai/guides/models/p-image-ideogram)

## Prompt craft (dynamic + faithful)

Every `input.prompt` must be **fresh and specific**, and must **keep the user's request**. Diversity never overrides the brief.

| Do | Don't |
| --- | --- |
| Run the `generation-diversity` random seed ritual; state it; rotate ≥2 free axes (camera, lighting, setting texture, render category) | Copy curl examples from this skill or reuse a prior session's prompt verbatim |
| Lock user-required facts first (subject, product, brand cues, must-keep props, **exact strings** for typography briefs) | Swap the subject for a “cooler” scene that ignores the request |
| For **structured layouts**, use the [Ideogram JSON caption schema](./references/ideogram-json-prompting.md) in `input.prompt` when placement, palette, or repeatability matter; otherwise name panels, literal copy, and hex in natural language | Chain **`p-image-edit`** to fix multi-panel copy — regen T2I instead |
| Expand with concrete nouns, frozen action, materials, placement (`image-prompting` golden rules) | Vague mood-only strings (`cool product vibe, neon`) |
| Show drafted prompt + `thinking` + `image_size` + `aspect_ratio` + `prompt_upsampling` before `POST` when the user has not locked wording | Silent regen with a different subject than approved |

**Fidelity check (before pay):** if you remove the user’s named subject/product/setting from the prompt, the job is wrong — rewrite. Free axes only fill what the brief left open.

**Typography:** list every string and surface; use **`thinking: "high"`** + **`image_size: "2K"`** when legibility is critical. Domain-specific profiles and vertical rows: [domain-configurations.md](./references/domain-configurations.md). **JSON captions** (exact placement, brand hex, repeatable layout): [ideogram-json-prompting.md](./references/ideogram-json-prompting.md).

## Thinking & resolution

| `thinking` | Best for |
| --- | --- |
| **`very low`** | Basic photos, fastest ideogram pass |
| **`low`** | Simple scenes, lighter reasoning |
| **`medium`** | **Default agent choice** — candid photoreal, editorial portraits, product heroes at 1K |
| **`high`** | Text rendering, advertising shoots, multi-panel UI, cast diversity — pair with **`image_size: "2K"`** |

Do not send invalid values (e.g. `"very high"` has returned **422** on some deployments). Stick to **`very low`**, **`low`**, **`medium`**, **`high`**.

## When NOT to use

Use a different skill instead:

| Skill | Description | Install |
| --- | --- | --- |
| `p-image` | Use when someone explicitly wants the fastest, cheapest text-to-image drafts — mood boards, bulk panels, or quick iterations — not the default hero or typography path. | `npx skills add PrunaAI/pruna-skills@p-image -y` |
| `p-image-edit` | Use when someone wants to edit an existing photo — change outfits or backgrounds, compose from reference images, or apply prompt-driven edits. | `npx skills add PrunaAI/pruna-skills@p-image-edit -y` |
| `p-image-try-on` | Use when someone wants virtual try-on — dress a person in clothes from reference photos for fashion or ecommerce. | `npx skills add PrunaAI/pruna-skills@p-image-try-on -y` |

## HTTP (curl)

### Create (async — recommended)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-image-ideogram' \
  -d '{
    "input": {
      "prompt": "South Asian woman founder mid-30s, documentary portrait at cast-iron loft window, natural skin pores, mouth visible, hands away from mouth, golden hour side light, photoreal editorial",
      "thinking": "medium",
      "image_size": "1K",
      "prompt_upsampling": false,
      "aspect_ratio": "9:16"
    }
  }'
```

Poll and download: follow `pruna-api`.

Complete the random seed ritual from `generation-diversity` before writing prompts — **do not** pass the ritual string as API `seed`. Optional `seed` only when the user requests reproducibility.

### Create (sync — quick test only)

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-image-ideogram' \
  -H 'Try-Sync: true' \
  -d '{"input":{"prompt":"Hong Kong neon alley at night, fearless grandmother in floral apron juggling dumplings, awning reads HAPPY HOUR 5-7, kiosk sign PRUNA AI, fish-eye lens, crisp legible typography","thinking":"high","image_size":"2K","prompt_upsampling":false,"aspect_ratio":"9:16"}}'
```

## Generation flow

Follow `generation-diversity` **still-image prompt flow** every time:

1. **Lock brief** — user subject, product, format, any copy-on-surface.
2. **Ritual seed** — fresh string; derive free axes (camera, lighting, `render_category_tag`, **`aspect_ratio`** when unset).
3. **Pick knobs** — [domain-configurations.md](./references/domain-configurations.md) profile for the vertical/use case, else default **`thinking: medium`**, **`image_size: 1K`**, **`prompt_upsampling: false`**; raise for typography / GTM cards.
4. **Draft explicit prompt** — **Prompt craft** + `image-prompting` golden rules; **fidelity check** before pay.
5. **Confirm** — show `prompt` + knobs unless wording is locked.
6. **POST** — async curl below; poll via `pruna-api`; run `p-image` quality checklist in `image-prompting` before upscale/video.

**Aspect ratio:** pass `aspect_ratio` in `input`; if output dimensions do not match (e.g. asked `16:9`, got portrait), retry once with explicit `horizontal wide` / `vertical` wording in the prompt.

**Mood board / batch:** new ritual per independent still; different **`aspect_ratio`** per panel when format not locked.

**Hero approved → tweak:** hand off to `p-image-edit` on the hero URL for **photo** edits — do not text-to-image re-roll the same subject; do not use edit to fix dense multi-panel UI copy.

## Required input

- `prompt` (string)

## Common optional fields

- `thinking`: `very low`, `low`, `medium`, `high`
- `image_size`: `1K`, `2K` (ignored when `aspect_ratio` is `custom`)
- `prompt_upsampling`: boolean — **prefer `false`** unless the user wants expansion
- `aspect_ratio`: `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`, `custom` (with `width` / `height` up to 2560, multiples of 16)
- `seed`, `output_format` (`jpg`, `png`, `webp`), `output_quality` (0–100; ignored for `png`)

## Typical next steps

Common follow-ons after this skill:

| Skill | Description | Install |
| --- | --- | --- |
| `p-image-edit` | Use when someone wants to edit an existing photo — change outfits or backgrounds, compose from reference images, or apply prompt-driven edits. | `npx skills add PrunaAI/pruna-skills@p-image-edit -y` |
| `p-image-try-on` | Use when someone wants virtual try-on — dress a person in clothes from reference photos for fashion or ecommerce. | `npx skills add PrunaAI/pruna-skills@p-image-try-on -y` |
| `p-image-upscale` | Use when someone wants to upscale or sharpen an existing image for print, large crops, or higher-quality delivery. | `npx skills add PrunaAI/pruna-skills@p-image-upscale -y` |
| `p-video` | Use when someone wants one short video clip from text or images — B-roll, start/end frame animation, or a quick motion shot. Not for full multi-scene films or lip-synced hosts. | `npx skills add PrunaAI/pruna-skills@p-video -y` |
| `p-video-avatar` | Use when someone wants a person on camera speaking a script — lip-synced host, spokesperson, or narrated avatar from a portrait photo. | `npx skills add PrunaAI/pruna-skills@p-video-avatar -y` |

