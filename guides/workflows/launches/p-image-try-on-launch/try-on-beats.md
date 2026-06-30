# Try-on launch beats

Companion to [SKILL.md](./SKILL.md). Each **`vertical`** chapter is one plan row using **`showcase`** or **`showcase_ladder`** motion — proof of **clothing change**, not resolution/upscale.

Run [visual-variety-bible.md](../../../references/shared/visual-variety-bible.md) before API calls. For **marketing reels**, also run [p-image-try-on-marketing-scenarios.md](../../../references/image/p-image-try-on-marketing-scenarios.md) — realistic settings, cast ledger, and non-overlapping garment slots.

## Marketing scenario diversity (launch reels)

When the user wants a **catchy retail marketing reel** (not a basic API demo):

1. Pick a [ritual seed](../../../references/shared/random-seed-ritual.md) → `project_seed`.
2. Fill the **cast + vertical + setting** matrix from [marketing scenarios](../../../references/image/p-image-try-on-marketing-scenarios.md#example-cast--vertical-matrix-7-scenes).
3. Set `defaults.try_on_mode: "single_pass"` for multi-garment rows (one API call, up to 11 refs).
4. Assign distinct `type` per garment — runner rejects overlapping body slots.
5. Use natural-light person prompts; plain packshot garment refs (no logos/text).
6. Motion: `showcase_garment_flash` / `showcase_rapid` for stacks; `showcase_flash` between beats for pacing.

**Why:** Buyers recognize real moments (office try-on, boardwalk PDP, mirror selfie UGC). Diversity across rows proves preservation + multi-garment scale without repeating one synthetic set.

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
| 6 | `avatar` | cta | **`still_from_previous`** + **`use_try_on_all`** → evening look from scene 5 · **Pruna API CTA** (see below) |

**Timing keys:** `showcase_timing` (standard), `rapid_timing` (multi-garment montage), per-scene override on ladder rows.

### CTA beat (scene 6)

End the hybrid reel on an **`avatar`** row that **invites API use** — upload person + garment refs, docs link. Do **not** repeat turbo/pricing here; those belong on hook (0) and scale (4).

**Plan flags:** `still_from_previous: true`, `use_try_on_all: true` when scene 5 was multi-garment.

**Example `voice_script`:**

```text
That's P-Image-Try-On. [short pause] Upload a person photo and your garment refs on the Pruna API — try it today at docs.api.pruna.ai.
```

**Example `video_prompt`:** slow confident push-in, open-palm invite gesture, clear lip sync on the API line.

### Avatar voice copy (feature rows)

| Row | Feature | Pricing / speed in VO |
|-----|---------|------------------------|
| 0 | speed | Fastest/cheapest hook — no per-item math |
| 2 | preservation | Character consistency — same face, same scene |
| 4 | scale | **$0.015** first garment, **$0.008** each extra; quality **&lt;2s/garment** |
| 6 | cta | API upload + docs — **no** pricing recap |

Speak **P-Image-Try-On** with dashes (not *pee-image*). For tiered cost TTS: *"one and a half cents for the first garment, eight tenths for each extra"* — not a flat per-item rate.

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

Concat + crossfade + instrumental bed → `*_with_music.mp4`. Set `background_music.reuse_bed: true` to loop an existing `audio/launch_bed.mp3` on re-assemble instead of calling Stable Audio again.

**GPT comparison bookends** — set `comparison_bookends.enabled: true` to prepend/append clips from existing comparison folders. Or set `comparison.after_each_try_on: true` to insert a 4s side-by-side after every try-on scene (recommended for marketing reels).

**Simulated Pruna speed** — when reusing `try_on_all.png`, boards show a stable random latency between `simulated_pruna_seconds_min` and `simulated_pruna_seconds_max` (default 3.5–4.5s) per scene.

## Vertical chapters

See [SKILL.md](./SKILL.md) use-case table. Every vertical uses the same **garment → person → before/after try-on** proof pattern; only cast, garment category, and setting change.

**Do not use** [p-image-upscale-comparison](../p-image-upscale-comparison/SKILL.md) for this workflow — that skill compares resolution, not outfit swaps.

## Garment reference rules

In scene plans, set `"type"` on each garment object for labeling and showcase chips — the API **auto-classifies** garments; do not send `garment_types` in predictions.

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

**Multi-garment rows:** up to 11 refs per call. Category hints in plan `type` fields are for humans/showcase only.

## Slop gate

Run [p-image-try-on-quality-checklist.md](../../../references/image/p-image-try-on-quality-checklist.md) on every try-on still before building showcase clips.
