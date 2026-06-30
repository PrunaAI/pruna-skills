# P-Image-Try-On — marketing scenario diversity

How to plan **catchy but believable** try-on marketing reels — not generic catalog demos, and not fantasy neon sets that read as synthetic.

Use this when building launch reels, comparison packs, or multi-scene `plan.json` files for retail marketing.

**Related:** [visual-variety-bible.md](../shared/visual-variety-bible.md) · [generation-diversity.md](../shared/generation-diversity.md) · [p-image-try-on-showcase.md](./p-image-try-on-showcase.md) · [try-on-beats.md](../../guides/workflows/launches/p-image-try-on-launch/try-on-beats.md)

## Goal

Each scene should feel like a **real shopper or buyer moment** someone recognizes — while the **reel as a whole** still rotates cast, setting, garment complexity, and retail vertical so the model range is obvious at thumbnail scale.

**Catchy** comes from composition, wardrobe contrast, and location specificity — not from neon gel lighting, oversaturated grades, or fantasy environments.

## The diversity iteration (run before every marketing batch)

Complete this table **before** the first `p-image` call. Pick a fresh [ritual seed](../shared/random-seed-ritual.md) as `project_seed`.

| Step | Action | Why |
|------|--------|-----|
| 1 | **Cast ledger** — unique gender, age band, ethnicity, archetype per scene row | Proves try-on on diverse real bodies; avoids one default face |
| 2 | **Vertical spread** — rotate `ecommerce_pdp`, `virtual_fitting_room`, `wholesale_catalog`, `lookbook_campaign`, `ugc_ads`, `personalized_outfits` | Maps to buyer use cases in one reel |
| 3 | **Setting ladder** — no two adjacent rows share location type | Keeps the reel from feeling like one repeated shoot |
| 4 | **Natural light only** — window daylight, overcast open sky, golden hour, soft studio | Photoreal retail; neon/LED reads as AI demo not production workflow |
| 5 | **Garment tier ladder** — rotate packshot (A) → multi-panel (D) → multi-garment stack | Shows capability beyond a plain tee |
| 6 | **Body-slot map** — one item per region; layer only `tops` + `outerwear` + `neckwear` | Prevents overlapping try-on refs in single-pass calls |
| 7 | **Single-pass multi-garment** — `defaults.try_on_mode: "single_pass"` when showing stacks | One API call, up to 11 refs; matches how integrators batch |
| 8 | **Plain garment refs** — no logos, embroidery, or readable text on packshots | Avoids text artifacts and failed partial try-ons |

Log `project_seed`, per-scene `setting_tag`, `palette_tag`, garment `type` slots, and prediction ids in the manifest.

## Realistic setting ladder (marketing)

Rotate through **believable** locations — same diversity axis as the variety bible, without stylized lighting:

| Setting tag | Real-world moment | Typical vertical |
|-------------|-------------------|------------------|
| `golden_hour_field` | Outdoor editorial / lookbook | `lookbook_campaign` |
| `night_street_portrait` | Night street full-body portrait (no mirror) | `ugc_ads` |
| `high_angle_studio` | Catalog buyer preview | `wholesale_catalog` |
| `fitting_room_alcove` | In-store try-on, facing camera | `virtual_fitting_room` |
| `boardwalk_morning` | Lifestyle PDP / athleisure | `ecommerce_pdp` |
| `cobblestone_autumn` | Weekend outfit stack | `personalized_outfits` |
| `sidewalk_cafe_blue_hour` | Occasion / date-night stack | `ecommerce_pdp` |
| `open_asphalt_overcast` | Streetwear full-body | `ugc_ads` |

**Avoid for marketing finals:** `neon_*`, `led_*`, `cyberpunk`, `magenta-teal gel`, `saturated color grade`, pure white seamless on every row.

## Garment body slots (no overlap)

When `try_on_mode: "single_pass"`, assign **one ref per slot** in the plan `type` field. The runner validates duplicates.

| Slot | Plan `type` values | Layering rule |
|------|-------------------|---------------|
| Head | `headwear` | One only |
| Neck | `neckwear` | One only; stacks over tops |
| Torso inner | `tops` | One only |
| Torso outer | `outerwear` | One only; stacks over tops |
| Legs | `bottoms` | One only |
| Feet | `feet` | One only (not socks + shoes in one call) |
| Full body | `dresses` | Exclusive — no separate tops/bottoms |
| Carry | `bags` | One only; person plate must show strap path |

**Full-body scenes** (fitting room, street full-length, boardwalk): include a `feet` garment in the single-pass stack **and** call out head-to-toe framing in the person prompt — bare feet or missing shoes in finals usually means no `feet` ref was passed.

**No mirrors in person plates** — convex traffic mirrors, fitting-room mirrors, and glass reflections leave a second copy of the subject on the base outfit; try-on only swaps clothing on the foreground figure. Use direct-to-camera portraits instead of mirror selfies for marketing finals.

**Reliable counts:** ≤6 for finals; 7–8 usually lands; up to 11 supported with diminishing guarantee on last pieces.

## Plan fields (marketing)

```json
{
  "project_seed": 517283,
  "defaults": {
    "try_on_mode": "single_pass",
    "aspect_ratio": "9:16"
  },
  "style_bible": "Photoreal everyday retail, natural available light, believable locations, natural skin texture, single subject one frame. No screens or UI. No readable text or signage.",
  "garment_bible": "Flat-lay on white sweep, color-accurate, plain fabric only — no graphics, embroidery, or labels facing camera."
}
```

Per multi-garment scene: list garments with distinct `type` values and `output_label` for showcase chips.

## Anti-patterns (what failed in early demos)

| Sloppy pattern | Why it fails | Fix |
|----------------|--------------|-----|
| Neon boutique / LED fitting room | Reads synthetic; not a shopper moment | Window light, overcast street, golden hour |
| Same grey studio every row | Hides preservation in real scenes | Setting ladder above |
| Logo tee / embroidered cap | Text artifacts in try-on pass | Plain packshots only |
| Incremental try-on per garment in marketing | Under-sells one-call multi-garment API | `try_on_mode: "single_pass"` |
| Two tops or two bottoms in one call | Slot overlap; unpredictable winner | One `type` per body region |
| Full-body mirror / street with no `feet` garment | Bare feet or wrong footwear in try-on | Add `feet` ref + head-to-toe person prompt |
| Mirrors / convex traffic mirrors in person plate | Reflection shows base outfit; foreground shows try-on — broken scene | Direct-to-camera portrait; ban mirrors in `style_bible` |
| Blazer-only stack with shirtless base | Open chest, missing shoes in output | Add `tops` + `feet` garments; base outfit with tee and shoes |
| White-background mannequin only | Under-sells scene preservation | Named real location in person prompt |

## Scene proof pattern (video)

| Garment count | Suggested `motion` |
|---------------|-------------------|
| 1 | `showcase` + `showcase_timing` |
| 2–6 single-pass | `showcase_rapid` or `showcase_garment_flash` + `showcase_timing` |
| Flash beat after stack | `showcase_flash` + `still_from_previous` + `use_try_on_all` · prefer `style: crossfade`, `zoom_peak: 1.0` |

**Clean delivery:** set `defaults.show_labels: false` to drop on-frame chips and before/after captions — let the try-on stills speak.

**Pacing:** prefer `showcase_timing` over `rapid_timing` for marketing finals; reserve `beat_cut` / `zoom_pulse` flash styles for hype cuts only.

## Example cast + vertical matrix (7 scenes)

| # | Vertical | Setting | Cast shift | Garment proof |
|---|----------|---------|------------|---------------|
| 1 | `lookbook_campaign` | Golden-hour field | F, Mediterranean, late 20s | Fine pleat blouse |
| 2 | `ugc_ads` | Night street mirror | F, East Asian, early 20s | 4-piece street stack · one call |
| 3 | `wholesale_catalog` | High-angle studio | M, Black, early 30s | Color-block blazer + trousers |
| 4 | `virtual_fitting_room` | Boutique office | F, Black, early 30s | Blazer + trousers |
| 5 | `ecommerce_pdp` | Boardwalk morning | F, Latina, mid 20s | Tee + joggers + jacket + sneakers |
| 6 | `personalized_outfits` | Cobblestone autumn | F, Nordic, late 20s | Coat + scarf + jeans + boots |
| 7 | `ecommerce_pdp` | Hotel lobby evening | M, Middle Eastern, mid 30s | Blazer + shirt + trousers + oxfords |

Adjacent rows differ on **at least two axes** (cast + setting + garment tier).

## Related

- Runner slot validation: `run_from_plan.py` → `validate_garment_slots()`
- Multi-garment renderer: `generate_tryon_showcase.py` → `render_multi_garment_showcase()`
- API limits: [p-image-try-on SKILL.md](../../tools/image/p-image-try-on/SKILL.md#multi-garment-limits)
