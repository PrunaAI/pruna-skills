---
name: p-image-ideogram
description: Use when the user wants high-fidelity photoreal stills, editorial portraits, hero plates, legible text rendering, or poster typography—not the fastest draft stills or mood-board throughput.
license: MIT
metadata:
  version: "0.0.2"
  provider: replicate
  replicate_deployment: prunaai/p-image-ideogram-preview
---

# p-image-ideogram (Pruna · Replicate deployment)

**High-quality, fast** text-to-image via the Pruna Ideogram preview deployment on [Replicate](https://replicate.com/prunaai/p-image-ideogram-preview). Runs on Replicate — not the Pruna P-API.

## When to use

| Goal | Use this |
|------|----------|
| Photoreal hero plates, editorial portraits, product shots | Yes |
| Legible **text rendering** — posters, signage, ads, GTM graphics | Yes — `mode: high` or `very high` + `image_size: 2K` |
| Fastest possible draft stills, mood boards, bulk panels | No — use [p-image](../p-image/SKILL.md) (Pruna P-API; good quality, **extremely** fast) |
| Editing an existing image | No — use [p-image-edit](../p-image-edit/SKILL.md) |
| Virtual try-on | No — use [p-image-try-on](../p-image-try-on/SKILL.md) |

### Mode & resolution

| `mode` | Best for |
|--------|----------|
| **`very low`** | Basic photos, fast drafts, simple scenes |
| **`medium`** (default) | Candid realistic shots, documentary portraits, everyday photoreal |
| **`high`** · **`very high`** | Text rendering, advertising shoots, dense crowds / cast diversity — pair with **`image_size: 2K`** |

Higher modes run stronger upsamplers (ideogram-sft, Gemini Flash, nano-banana-2-lite at `very high`). **Prompt upsampling is built into `mode`** — long specific prompts and named typography are OK when the brief needs readable text.

**Dynamic persona & scenarios:** [realistic-persona-showcase.md](../../../references/shared/realistic-persona-showcase.md) · examples: [example-prompt.md](./example-prompt.md)

Shared Replicate patterns: [replicate-api.md](../../../references/shared/replicate-api.md)

## Environment

```bash
export REPLICATE_API_TOKEN=r8_...
```

## Model input (Replicate deployment)

| Field | Notes |
|-------|-------|
| `prompt` | **Required.** Short text prompt for image generation. |
| `mode` | Quality/speed preset — see [Mode & resolution](#mode--resolution). `very low` · `low` · **`medium`** (default) · `high` · `very high`. |
| `aspect_ratio` | **`1:1`** (default) · standard ratios · `custom` (set `width` / `height`) |
| `image_size` | Output resolution budget: **`1K`** (default) · **`2K`** for text rendering, advertising shoots, and diversity-heavy scenes at `high` / `very high`. Ignored when `aspect_ratio=custom`. |
| `width` | When `aspect_ratio=custom` — rounded to nearest multiple of 16 (0–2560, default 1024). |
| `height` | When `aspect_ratio=custom` — rounded to nearest multiple of 16 (0–2560, default 1024). |
| `seed` | Optional integer for reproducibility. |
| `output_format` | **`jpg`** (default) · `png` |
| `output_quality` | 0–100 (default **80**); ignored for `png`. |

Complete the [random seed ritual](../../../references/shared/random-seed-ritual.md) (SSoT) before writing prompts — **do not** pass the ritual string as API `seed`. Set `seed` only when the user requests reproducibility.

## Before generating

1. **[Generation diversity](../../../references/shared/generation-diversity.md)** — ritual seed (SSoT) + [explicit prompt structure](../../../references/shared/generation-diversity.md#explicit-prompt-structure-required). Pick **`mode`** per [Mode & resolution](#mode--resolution): `very low` for basic photos, `medium` for candid realism, `high` / `very high` + **`2K`** for text rendering, ads, and diversity. Name exact strings and placements for text briefs per [text rules](../../../references/shared/generation-diversity.md#text--typography-by-model). **Multi-example batches:** different **`aspect_ratio`** per still.
2. Confirm **`prompt`**, **`mode`**, and **`aspect_ratio`** with the user. Run [p-image-quality-checklist.md](../../../references/image/p-image-quality-checklist.md) on outputs before downstream steps.

## Production quality — photoreal personas

Same discipline as [p-image](../p-image/SKILL.md): documentary portrait language, diverse cast, avatar-ready mouth visibility, try-on-ready body coverage. Full matrix: [realistic-persona-showcase.md](../../../references/shared/realistic-persona-showcase.md).

Lock **hero plate URL** at hero generation when the same identity continues to **`p-image-edit`**, **`p-image-try-on`**, or **`p-video-avatar`**.

## Python (Replicate SDK)

```python
import replicate

deployment = replicate.deployments.get("prunaai/p-image-ideogram-preview")
prediction = deployment.predictions.create(
    input={
        "prompt": "South Asian woman founder mid-30s, documentary portrait at cast-iron loft window, natural skin pores, mouth visible, hands away from mouth, golden hour side light, photoreal editorial",
        "aspect_ratio": "9:16",
        "mode": "medium",
    }
)
prediction.wait()
print(prediction.output)
```

## HTTP (curl)

```bash
curl -s -X POST \
  -H "Authorization: Bearer ${REPLICATE_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "prompt": "Hong Kong neon alley at night, fearless grandmother in floral apron juggling dumplings, awning reads HAPPY HOUR 5-7, kiosk sign PRUNA AI, fish-eye lens, crisp legible typography",
      "aspect_ratio": "9:16",
      "mode": "high",
      "image_size": "2K"
    }
  }' \
  "https://api.replicate.com/v1/deployments/prunaai/p-image-ideogram-preview/predictions"
```

Poll `urls.get` until `status` is `succeeded`; download `output` (image URL).

## Example: asynchronous (batch / multi-panel)

For N panels with no shared dependency, **POST all jobs in parallel**, then poll every `urls.get`. See [parallel-execution.md](../../../references/shared/parallel-execution.md).

## Typical next steps

- Refine or composite: [p-image-edit](../p-image-edit/SKILL.md)
- Virtual try-on: [p-image-try-on](../p-image-try-on/SKILL.md)
- Upscale output: [p-image-upscale](../p-image-upscale/SKILL.md)
- Animate still: [p-video](../../video/p-video/SKILL.md) or [p-video-avatar](../../video/p-video-avatar/SKILL.md)
- Full pipeline: [pruna-generative-pipeline](../../../workflows/router/pruna-generative-pipeline/SKILL.md)
