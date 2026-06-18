# p-image-try-on showcase guide

Try-on-specific guidance: garment tiers, preservation checklist, and canonical Replicate reference outputs. **Shared persona plates, avatar motion, and diversity rules:** [realistic-persona-showcase.md](../shared/realistic-persona-showcase.md).

How to produce **photoreal, art-directed try-on outputs** — not basic catalog demos. Use this when building Replicate playground examples, ecommerce packs (recipe K), or fashion avatar pipelines.

**Core strength:** the model swaps **garments only** while preserving identity, pose, hair, skin, background, lighting, and scene props. That makes it suitable for **editorial fashion**, **complex multi-panel garments**, and **accessory + logo** placements — not just flat-lay T-shirt swaps on a white background.

## Reference outputs (canonical playground bar)

Pin these five Replicate predictions as the quality bar (internal samples, June 2026). Each demonstrates a different capability beyond “simple tee on model”:

| # | Replicate prediction | What it proves |
|---|----------------------|----------------|
| 1 | [p47vaj1f…](https://replicate.com/p/p47vaj1f91rmw0cyt4er0z2zd4) | **Editorial still life** — artistic multi-panel shirt (line-art print + color-block sleeves), seated pose, textured wall + wood floor preserved |
| 2 | [tf7gqans…](https://replicate.com/p/tf7gqansnnrmt0cyt4j8mpx1c8) | **Complex suit** — collaged blazer + trousers (checkerboard, birds, vases, silhouettes), high-angle fashion framing, bare chest under open blazer |
| 3 | [hp60wyj3…](https://replicate.com/p/hp60wyj355rmy0cyt4psnc2mh0) | **Accessories + logo tee in-scene** — cap, chest logo, headphones, mirror-selfie composition, night city background unchanged |
| 4 | [bak21xr7…](https://replicate.com/p/bak21xr79srmr0cyt52tap1nw8) | **Multi-garment streetwear stack** — patchwork jacket + pants + branded tee + chain; full-body pose with prop (bat) preserved |
| 5 | [g9hd22x2…](https://replicate.com/p/g9hd22x26drmr0cytmtsx11c5g) | **Texture-heavy garment + lifestyle** — fine pleated blouse, golden-hour portrait, sunglasses + jewelry, cinematic DOF |

**Playground action (Replicate / marketing):** add predictions 1–5 to [prunaai/p-image-try-on](https://replicate.com/prunaai/p-image-try-on) Examples — coordinate with @ShinyTaskForce. This repo documents the bar; the live playground is updated separately.

## Anti-patterns (what reads as “AI sloppy”)

Avoid these in demos, docs, and agent-generated plans:

| Sloppy demo | Why it fails | Better direction |
|-------------|--------------|------------------|
| Generic white-background mannequin pose | Looks synthetic; hides preservation strength | Editorial location + named lighting (see samples 1, 5) |
| Single plain flat-lay tee only | Under-sells multi-garment + complex print support | Patchwork, color-block, or collaged refs (samples 2, 4) |
| Low-res or mushy person plate | Artifacts amplify in try-on pass | Photoreal **`p-image`** hero → slop gate → try-on |
| Same default face across all examples | No diversity signal | Rotate cast per [visual-variety-bible.md](../shared/visual-variety-bible.md) |
| Turbo-only finals | Missed garment slots on complex stacks | Normal mode for delivery; turbo for previews only |
| Replacing background or face “while dressing” | Wrong tool story | Verify preservation checklist (below) |

## Person plate quality (upstream)

Try-on quality is capped by **`person_image`**. Generate plates with **`p-image`** when you do not have licensed model photography — full prompt stack and avatar-ready rules: [realistic-persona-showcase.md](../shared/realistic-persona-showcase.md#p-image--photoreal-persona-plates).

Run [p-image-quality-checklist.md](./p-image-quality-checklist.md) before try-on.

**Multi-example batches:** rotate **`aspect_ratio`** on each person plate (`1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`) — see [generation-diversity.md](../shared/generation-diversity.md#aspect-ratio-multi-example-sets). Try-on inherits plate dimensions when `preserve_input_size: true`.

### Example person plates (by showcase tier)

**Editorial seated (→ sample 1 style):**

```text
Photoreal editorial fashion photograph, woman mid-20s Mediterranean, dark wavy hair,
seated on weathered dark wood floor against textured grey plaster wall, relaxed pose
hand near chin, bare feet visible, soft side window daylight, editorial portrait framing,
natural skin texture, not CGI, single subject one frame.
```

**High-angle suit canvas (→ sample 2 style):**

```text
Photoreal fashion lookbook, man early 30s East Asian, short styled hair, shirtless,
standing hands in pockets, seamless off-white studio floor, high angle from above,
even soft studio light, full body head to shoes visible, single subject one frame.
```

**Mirror selfie / street (→ sample 3 style):**

```text
Photoreal night street mirror selfie, woman mid-20s East Asian, long dark hair,
holding smartphone, convex traffic mirror reflection, city crosswalk and car lights
behind her, white crew tee and grey joggers, over-ear headphones around neck,
neon and streetlamp mixed lighting, vertical full-body framing, single subject one frame.
```

**Full-body streetwear (→ sample 4 style):**

```text
Photoreal street fashion portrait, woman early 20s East Asian, high ponytail,
full body on dark asphalt, holding baseball bat behind shoulders, overcast open-sky
light, vertical full-body framing, neutral base outfit, single subject one frame.
```

**Golden-hour portrait (→ sample 5 style):**

```text
Photoreal cinematic portrait, woman late 20s, dark hair loose updo, tortoiseshell
sunglasses, golden hour backlight with warm rim on hair, soft field bokeh background,
medium close-up chest-up, natural skin pores, single subject one frame.
```

## Garment reference quality

| Tier | Garment input | API notes |
|------|---------------|-----------|
| **A — Packshot** | Flat-lay on neutral | Default path; no `prompt` |
| **B — On-model ref** | Garment worn in lifestyle photo | Set **`prompt`**: `"the [color] [item] from image 1"` |
| **C — Multi-item photo** | Several pieces in one image | One URL + **`prompt`** listing each slot |
| **D — Complex print / patchwork** | Collage, color-block, fine pleats, logos | Prefer **normal mode**; verify each panel in checklist |
| **E — Accessories** | Hats, glasses, bags, jewelry | Person plate must show anchor region (head, ears, shoulder strap path) |

Name **materials and print type** in briefs — `matte canvas patchwork`, `fine vertical pleated silk`, `screen-printed logo on cotton` — agents and humans align expectations faster.

## Preservation checklist (the model’s differentiator)

After try-on, confirm **only clothing changed**:

- [ ] Face structure, skin tone, and expression match **`person_image`**
- [ ] Hair length, color, and style unchanged (unless hat/headwear requested)
- [ ] Background, props, and scene geometry preserved
- [ ] Pose and limb positions preserved (or match **`reference_pose`** when set)
- [ ] Lighting direction and shadow mood consistent with plate
- [ ] Logos / prints on garment match reference (readable where ref is readable)

Fail → retry normal mode, simplify garment stack, or regenerate person plate.

## Diversity for showcases and avatar handoff

For public examples and launch reels, plan a **cast ledger** before generation — [realistic-persona-showcase.md](../shared/realistic-persona-showcase.md#diversity-for-public-showcases) and [visual-variety-bible.md](../shared/visual-variety-bible.md):

- Rotate gender, age band, and ethnicity across the five playground slots
- Rotate **setting_tag** (studio floor · street night · open asphalt · golden-hour field · high-angle studio)
- Rotate **garment complexity tier** (A → D) so no two examples look like the same demo template

**Avatar pipeline:** approved try-on still → optional **`p-image-upscale`** → slop gate → **`p-video-avatar`** with unique **`video_prompt`** per clip — see [realistic-persona-showcase.md](../shared/realistic-persona-showcase.md#p-video-avatar--dynamic-realistic-personas). Lock **`seed`** from person-plate generation through avatar.

## API settings for delivery assets

| Setting | Showcase / final | Preview / batch |
|---------|------------------|-----------------|
| `turbo` | `false` | `true` when speed > fidelity |
| `output_quality` | `95` | `90` acceptable for internal review |
| `preserve_input_size` | `true` for PDP crops | `true` unless upscaling next |
| Garment count | ≤6 per call for finals | Same; split stacks across calls if needed |

## Related

- [p-image-try-on SKILL.md](../../tools/image/p-image-try-on/SKILL.md)
- [p-image-try-on-quality-checklist.md](./p-image-try-on-quality-checklist.md)
- [visual-variety-bible.md](../shared/visual-variety-bible.md)
- [p-image-quality-checklist.md](./p-image-quality-checklist.md)
- Recipe K: [pruna-generative-pipeline SKILL.md](../../guides/workflows/router/pruna-generative-pipeline/SKILL.md)
