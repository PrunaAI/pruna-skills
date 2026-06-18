# Try-on launch beats

Companion to [SKILL.md](./SKILL.md). Each **`vertical`** chapter is one plan row using **`showcase`** or **`showcase_ladder`** motion — proof of **clothing change**, not resolution/upscale.

Run [visual-variety-bible.md](../../../references/shared/visual-variety-bible.md) before API calls.

## Showcase clip structure (every beat)

Local renderer [`generate_tryon_showcase.py`](./scripts/generate_tryon_showcase.py):

1. **Input · garment ref** — full-frame product shot  
2. **Input · person photo** — same person, base outfit  
3. **Side-by-side** — Before · base outfit | After · try-on  
4. **Wipe reveal** — same comparison, animated  
5. **Try-on hold** — dressed result full frame  
6. **Flash compare** — quick before/after blink (optional)

**`showcase_rapid`** — same assets, tighter timing (`rapid_timing`): garment flash → wipe → hold per outfit, no side-by-side hold. Use for multi-garment beats.

All frames at one canvas (default **1080×1920**).

## Hybrid reel (~60s) — avatar + multi-garment

Alternate **feature explainers** (`avatar` + `voice_script`) with **try-on proof** (`showcase`, `showcase_rapid`, `showcase_ladder`).

| # | Motion | Feature | What it shows |
|---|--------|---------|---------------|
| 0 | `avatar` | speed | Presenter in try-on look — hook + value |
| 1 | `showcase_rapid` | multi_garment | 3 garments · fast montage on one person |
| 1f | `showcase_flash` | flash | **0.5–1s random try-on cuts** · same person from scene 1 |
| 2 | `avatar` | preservation | Same person/scene — **`still_from_previous`** → final look from scene 1 |
| 3 | `showcase` | fitting_room | Selfie + product → dressed result |
| 4 | `avatar` | scale | **`still_from_previous`** → final try-on from scene 3 · **`persona_gender`** voice match |
| 5 | `showcase_ladder` | personalized | Work / weekend / evening on one person |
| 5f | `showcase_flash` | flash | **Double-cycle quick swaps** before CTA avatar |
| 6 | `avatar` | cta | **`still_from_previous`** → evening look from scene 5 |

**Timing keys:** `showcase_timing` (standard), `rapid_timing` (multi-garment montage), per-scene override on ladder rows.

## Default 8-beat reel (~90s, showcase-only)

| # | Type | Vertical | Motion |
|---|------|----------|--------|
| 0 | hook | — | `showcase` |
| 1 | try_on | `ecommerce_pdp` | `showcase` |
| 2 | try_on | `virtual_fitting_room` | `showcase` |
| 3 | try_on | `wholesale_catalog` | `showcase` |
| 4 | try_on | `lookbook_campaign` | `showcase` |
| 5 | try_on | `ugc_ads` | `showcase` |
| 6 | try_on | `personalized_outfits` | `showcase_ladder` |
| 7 | cta | — | `showcase` |

Concat + crossfade + instrumental bed → `*_with_music.mp4`.

## Vertical chapters

See [SKILL.md](./SKILL.md) use-case table. Every vertical uses the same **garment → person → before/after try-on** proof pattern; only cast, garment category, and setting change.

**Do not use** [p-image-upscale-comparison](../p-image-upscale-comparison/SKILL.md) for this workflow — that skill compares resolution, not outfit swaps.

## Garment reference rules

API **`garment_types`** (one per ref, same order as `garment_images[]`): `underwear`, `bottoms`, `dresses`, `feet`, `tops`, `top-layers`, `outerwear`, `headwear`, `neckwear`, `bags`, `wristwear-single`. Full table: [p-image-try-on/SKILL.md](../../../tools/image/p-image-try-on/SKILL.md#garment-types).

In scene plans, set `"type"` on each garment object — the runner maps it to `garment_types[]`.

| Type | Best reference | Avoid |
|------|----------------|-------|
| `tops` / `top-layers` / `outerwear` | Flat-lay front or hanger, labels and structure visible | Crumpled pile |
| `bottoms` | Flat-lay front, waistband and hem readable | Folded stack |
| `dresses` | Ghost mannequin or hanger | Extreme perspective |
| `underwear` | Packshot on white sweep | Busy lifestyle context |
| `feet` | Side profile or pair flat-lay | Blurry sole detail |
| `headwear` | Product shot on white, brim/shape clear | Face-heavy mannequin shot |
| `neckwear` | Flat-lay or drape | Tangled knot |
| `bags` | Front-facing product, strap laid out | Cluttered lifestyle scene |
| `wristwear-single` | Single item flat-lay, clasp visible | Multiple stacked pieces |

**Multi-garment rows:** up to 10 refs per call; always pass matching `type` / `garment_types` for 2+ items.

## Slop gate

Run [p-image-try-on-quality-checklist.md](../../../references/image/p-image-try-on-quality-checklist.md) on every try-on still before building showcase clips.
