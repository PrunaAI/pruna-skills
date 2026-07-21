# p-image-try-on prompting

When and how to use the experimental **`prompt`** on `p-image-try-on`. Upstream person plates: [realistic-persona-showcase.md](./realistic-persona-showcase.md). QA: [p-image-try-on-quality-checklist.md](./p-image-try-on-quality-checklist.md).

## Default: leave `prompt` empty

| Garment input | `prompt` |
|---------------|----------|
| Flat-lay / packshot (one clear item) | **Omit** — best default |
| Single clear garment on white | **Omit** |
| On-model / lifestyle / multi-item frame | **Set** — disambiguate which garment |
| Multiple garments in one image | **Set** — name items + image index |

Try-on is **image-led**. The prompt does not invent fashion — it only points at which garment from which ref.

## Disambiguation patterns

```text
the green t-shirt from image 1 and the trousers from image 2
```

```text
the black leather jacket worn by the model in image 1 — ignore the jeans
```

```text
only the red sneakers from image 2
```

Rules:

- Index refs the same way the API lists `garment_images` (image 1 = first URL).
- Name **color + garment type**; avoid marketing adjectives (`iconic`, `premium`).
- Do not write full scene/fashion-editorial prompts here — that belongs on the person plate (`p-image`).

## Upstream plate caps quality

Bad person plates → bad try-on. Fix with photoreal `p-image` (golden rules + persona showcase), then try-on, then optional upscale/avatar.

Anti-slop: no white-background-only demos, no mushy CGI faces, rotate cast/settings per [generation-diversity.md#visual-variety](../../generation-diversity/references/generation-diversity.md#visual-variety).

## `reference_pose`

Optional second person URL — output pose follows that reference. Keep `prompt` focused on **garment choice**, not pose description.

## Pre-send checklist

- [ ] Flat-lay? Prompt empty
- [ ] Multi-item or on-model? Prompt names color + item + image index
- [ ] Person plate approved (mouth/body region visible for garment type)
- [ ] Garment count within multi-garment limits (≤6 finals)
- [ ] No creative scene prose in `prompt`
