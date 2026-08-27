---
name: p-image-ideogram
description: Use when photo generation needs more control — photoreal results, text in the image, or structured JSON with hex colors and bounding boxes. Simpler photo generation, edits, and video use other skills in the suite.
license: MIT
metadata:
  version: "1.0.10"
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

**Route by complexity:** Use `` `p-image-ideogram` `` when **photo generation** needs more control — readable text in the image, structured JSON, hex/`bbox` placement, or high-detail photoreal shots. Use `` `p-image` `` for **simple, quick** photo generation. Use `` `p-image-edit` `` to change an existing photo; use `` `p-video` `` (or `` `p-video-animate` `` from a still) for motion.

In the **first reply**, name `` `p-image-ideogram` `` in backticks, confirm `PRUNA_API_KEY` is set (or stop with signup links from `pruna-api`), then ask for prompt / aspect ratio / any copy-on-surface (open intake → **`generation-diversity`** clarification intake). When drafting the prompt, follow **Prompt craft** below — do not paste skill examples.

**Agent defaults (override API defaults):** send **`thinking: "high"`**, **`prompt_upsampling: true`**, and **`image_size: "1K"`** unless a profile in [domain-configurations.md](./references/domain-configurations.md) says otherwise. Use **`image_size: "2K"`** for dense in-image text, multi-panel layouts, and large output. Set **`prompt_upsampling: false`** when text is locked (JSON prompts, exact strings) or the user wants verbatim prompts only.

**Premium path:** when the user requests maximum quality or the composition is highly complex (many text elements, intricate multi-panel layouts, detailed structured scenes), send **`thinking: "very high"`** + **`image_size: "2K"`**. Costs ~2× `high` ($0.033/1K, $0.066/2K) — confirm with the user before using unless they explicitly asked for top quality.

**Speed path (same model):** when the scene is simpler but you still want ideogram (or need a faster pass on this model), send **`thinking: "low"`**, **`prompt_upsampling: false`**, and a **nuanced, explicit prompt** you fully draft — upsampling stays off because the prompt already carries the detail. Faster than the default **`high`** + upsampling path. For the simplest quick photo drafts, route to **`p-image`** instead.

When the job comes from a **`vertical-*`** workflow (or another multi-step production with spec copy or covers), pick **`thinking`**, **`image_size`**, and NL vs JSON from [domain-configurations.md](./references/domain-configurations.md) for that vertical and use-case `#` — do not use one global knob set for every industry.

## vs `p-image`

| | `` `p-image-ideogram` `` | `` `p-image` `` |
| --- | --- | --- |
| **When** | **More control** — text in the image, JSON layout, hex/`bbox`, detailed photoreal photos | **Simple, quick** photo generation from a short prompt |
| **Quality** | Strong photorealism and typography; five **`thinking`** levels (`very low` to `very high`); **1K / 2K** | Good quality, extremely fast; no prompt upsampling |
| **Prompt upsampling** | **`true` by default** (`high` path); **`false`** on speed path or locked copy / JSON | None — concrete language is the whole craft |
| **Knob default** | **`thinking: high`** + **`prompt_upsampling: true`** | Single fast pass — no thinking/upsampling knobs |
| **Structured layout** | Ideogram 4.0 **JSON caption** in `prompt` (hex, `bbox`, `"text"` elements) — see [ideogram-json-prompting.md](./references/ideogram-json-prompting.md) | Avoid dense readable type |

Official parameters: [P-Image-Ideogram](https://docs.api.pruna.ai/guides/models/p-image-ideogram)

## Prompt craft (dynamic + faithful)

Every `input.prompt` must be **fresh and specific**, and must **keep the user's request**. Diversity never overrides what the user asked for.

| Do | Don't |
| --- | --- |
| Run the `generation-diversity` random seed ritual; state it; rotate ≥2 free axes (camera, lighting, setting texture, render category) | Copy curl examples from this skill or reuse a prior session's prompt verbatim |
| Lock user-required facts first (subject, product, brand cues, must-keep props, **exact strings** for text in the image) | Swap the subject for a “cooler” scene that ignores the request |
| For **structured layouts**, use the [Ideogram JSON caption schema](./references/ideogram-json-prompting.md) in `input.prompt` when placement, palette, or repeatability matter; otherwise name panels, literal copy, and hex in natural language | Chain **`p-image-edit`** to fix multi-panel copy — regenerate the photo instead |
| Expand with concrete nouns, frozen action, materials, placement (`image-prompting` golden rules) | Vague mood-only strings (`cool product vibe, neon`) |
| Show drafted prompt + `thinking` + `image_size` + `aspect_ratio` + `prompt_upsampling` before `POST` when the user has not locked wording | Silent regen with a different subject than approved |

**Fidelity check (before pay):** if you remove the user’s named subject/product/setting from the prompt, the job is wrong — rewrite. Free axes only fill what the user did not specify.

**Typography:** list every string and surface; use **`image_size: "2K"`** and **`prompt_upsampling: false`** when legibility is critical (default **`thinking: "high"`**). Domain-specific profiles and vertical rows: [domain-configurations.md](./references/domain-configurations.md). **JSON captions** (exact placement, brand hex, repeatable layout): [ideogram-json-prompting.md](./references/ideogram-json-prompting.md).

## Thinking & resolution

| `thinking` | Best for |
| --- | --- |
| **`very low`** | Basic photos, fastest ideogram pass |
| **`low`** | **Speed path** — pair with **`prompt_upsampling: false`** and a nuanced explicit prompt; faster than the default when the scene is simpler but ideogram is still the right model |
| **`medium`** | Middle ground when **`high`** is heavier than needed but the prompt is not fully self-contained |
| **`high`** | **Default agent choice** — text in the image, multi-panel layouts, editorial portraits; pair with **`image_size: "2K"`** when legibility or large output matters |
| **`very high`** | **Maximum quality** — complex compositions with multiple text elements, intricate layouts, or when the absolute best output justifies the ~2× cost over `high`; pair with **`image_size: "2K"`** for best results |

## When NOT to use

Use a different skill instead:

| Skill | Description | Install |
| --- | --- | --- |
| `p-image` | Use when someone explicitly wants the fastest, cheapest photo generation — mood boards, bulk panels, or quick iterations — not when controlled photoreal or in-image text is needed. | `npx skills add PrunaAI/pruna-skills@p-image -y` |
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
      "thinking": "high",
      "image_size": "1K",
      "prompt_upsampling": true,
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
  -d '{"input":{"prompt":"Hong Kong neon alley at night, fearless grandmother in floral apron juggling dumplings, awning reads HAPPY HOUR 5-7, kiosk sign PRUNA AI, fish-eye lens, crisp legible typography","thinking":"high","image_size":"2K","prompt_upsampling":true,"aspect_ratio":"9:16"}}'
```

## Generation flow

Follow `generation-diversity` **still-image prompt flow** every time:

1. **Lock the request** — subject, product, format, any text on the image.
2. **Ritual seed** — fresh string; derive free axes (camera, lighting, `render_category_tag`, **`aspect_ratio`** when unset).
3. **Pick knobs** — [domain-configurations.md](./references/domain-configurations.md) profile for the vertical/use case, else default **`thinking: high`**, **`image_size: 1K`**, **`prompt_upsampling: true`**; or **speed path** — **`thinking: low`**, **`prompt_upsampling: false`**, nuanced explicit prompt; or **premium path** — **`thinking: "very high"`**, **`image_size: "2K"`** for maximum quality on complex compositions; raise **`image_size`** to **`2K`** for dense in-image text or multi-panel layouts; set **`prompt_upsampling: false`** for locked text or JSON.
4. **Draft explicit prompt** — **Prompt craft** + `image-prompting` golden rules; **fidelity check** before pay.
5. **Confirm** — show `prompt` + knobs unless wording is locked.
6. **POST** — async curl below; poll via `pruna-api`; run `p-image` quality checklist in `image-prompting` before upscale/video.

**Aspect ratio:** pass `aspect_ratio` in `input`; if output dimensions do not match (e.g. asked `16:9`, got portrait), retry once with explicit `horizontal wide` / `vertical` wording in the prompt.

**Mood board / batch:** new ritual per independent photo; different **`aspect_ratio`** per panel when format not locked.

**Photo approved → edit:** hand off to `p-image-edit` on the output URL for **photo** edits — do not run photo generation again for the same subject; do not use edit to fix dense multi-panel in-image text (regenerate instead).

**Photo approved → video:** use `p-video` (image-to-video) or `p-video-animate` when motion is next; upscale first with `p-image-upscale` if resolution is tight.

## Required input

- `prompt` (string)

## Common optional fields

- `thinking`: `very low`, `low`, `medium`, `high`, `very high` — **default `high`**; **`low`** + **`prompt_upsampling: false`** + explicit prompt for the speed path; **`very high`** for maximum quality on complex compositions
- `image_size`: `1K`, `2K` (ignored when `aspect_ratio` is `custom`)
- `prompt_upsampling`: boolean — **default `true`** with **`thinking: high`**; **`false`** on speed path, locked copy, JSON prompts, or verbatim wording
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

