# p-image-upscale guidance

`p-image-upscale` is **not** a creative prompt model. There is no text prompt — quality comes from the **source still** and param choices.

QA: [p-image-upscale-quality-checklist.md](./p-image-upscale-quality-checklist.md).

## Param craft

| Field | Guidance |
|-------|----------|
| `target` | Megapixels 1–**128**. Print/billboard: 8–128. Mood boards: 4–16. Confirm cost/latency with the user. |
| `enhance_details` | Sharpens micro-detail. Use when the plate is already clean. |
| `enhance_realism` | Pushes photoreal texture. Can amplify plastic skin if the source is sloppy. |
| `output_format` | Match delivery (`png` for lossless pipeline steps, `jpg` when size matters). |

## When enhance helps vs hurts

| Source | Enhance | Outcome |
|--------|---------|---------|
| Approved photoreal hero, pores visible | `enhance_details` on | Cleaner print plate |
| Mushy CGI / AI-slop face | Either enhance flag | **Amplifies slop** — regenerate hero first |
| Stylized anime / flat cel | Prefer details off or light | Avoid forcing photoreal pores on cel art |

**Never** upscale to “fix” a rejected hero. Regenerate or edit, then upscale.

## Pipeline placement

| Workflow | Upscale? |
|----------|----------|
| Avatar / motion-transfer / replace | **No** unless user asks for print-scale stills — feed approved `p-image` / edit URLs after slop gate |
| Print, billboard, extreme crop | **Yes** — confirm `target` |
| Before/after slider demos | Optional helper scripts — not a creative step |

## Pre-send checklist

- [ ] Source still already passed slop gate
- [ ] `target` MP matches destination (not default-max “just in case”)
- [ ] Enhance flags match medium (photoreal vs stylized)
- [ ] User confirmed cost for high MP targets
