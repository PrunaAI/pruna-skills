# P-Video-Replace comparison examples

Canonical skills-library reel: [`output/launches/skills-library-announcement/announcement_plan.json`](../../../output/launches/skills-library-announcement/announcement_plan.json) · [`manifest.md`](../../../output/launches/skills-library-announcement/manifest.md).

## Portable install — notebook in hand (`replace_target: mixed`, scene 4)

1. Source: advocate on **subway platform** (or loft), **`plate_mode: p-image`**, closed **hardcover notebook** at chest (`p-video-avatar`).
2. References — **each ref its own world + camera:**
   - Recast A: rooftop dusk, low angle, cobalt hoodie
   - Recast B: cafe corner, side angle, orange hoodie (different age/ethnicity OK)
   - Wardrobe: LED studio, slight high angle, lime crewneck
3. Optional **`multi_image_beat`**: rooftop recast + LED wardrobe in one `p-video-replace` call.
4. Per-ref instructions preserve notebook + lips.

## Staged gate — full recasts (`replace_target: character`, scene 5)

1. Source: Nordic stylist in **mural alley**, `plate_mode: p-image`.
2. Three refs = **three different people** (East Asian rooftop · Black gallery · Latina mural) — not wardrobe-only on one face.
3. **`multi_image_beat`** optional finale combining two refs.
4. VO: human-in-the-loop / Phase A approval — avoid API jargon in spoken lines.

## In-hand prop swap (`replace_target: object`, scene 6)

1. Source: gym creator on **boardwalk**, white **tumbler** at chest, `plate_mode: p-image`.
2. Object refs: cobalt puck · copper cylinder · succulent — hand + prop visible, vivid accent color.
3. Instructions swap prop + background; preserve face and lips.

## CTA mixed row (`replace_target: mixed`, scene 7)

1. Source: founder at **street market**, mug on side table, `plate_mode: p-image`.
2. Refs: recast · scarf/terrace · wardrobe/rooftop · vase prop.
3. **`multi_image_beat`**: face + wardrobe + vase in one call.

## Persona ladder hooks (scenes 1–3)

One VO source per scene → **multi_job** refs spanning distinct **`visual_style_tag`** + optional **`render_medium_tag`**:

| Scene | Narrative label | Ref families |
|-------|-----------------|--------------|
| 1 | p-image | UGC photoreal · muted-tone sketch · 2D cel |
| 2 | p-video-animate | anime · clay elder · cyberpunk |
| 3 | p-video-replace | epic warrior · fox mascot · 3D royal |

**Note:** Scenes 1–3 use the **same workflow** (`p-image` refs + `p-video-replace`); labels name library chapters, not separate runner skills.

See [visual-variety-bible.md](../../../references/shared/visual-variety-bible.md) and [SKILL.md](./SKILL.md) **Persona & subject diversity**.

## Full skills-library reel

[`example-prompt.md`](../../../examples/workflows/launches/p-video-replace-comparison/example-prompt.md) · [`run_from_plan.py`](./scripts/run_from_plan.py)

**Delivery:** after concat, optional **light background music** via plan `background_music` or `--background-music` — [stable-audio-2.5](../../../tools/audio/stable-audio-2.5/SKILL.md) at ~0.12 volume.

---

## Legacy: product launch reel (8 scenes)

Use only when explicitly building the **P-Video-Replace product** announcement — not the skills library reel.

| Pattern | Notes |
|---------|-------|
| Hook / CTA desk + mug | `hero_edit` from plan hero; mixed blazer + desk SKU |
| UGC install + **closed laptop** | **Legacy prop** — prefer **hardcover notebook** for new plans ([SKILL.md](./SKILL.md) §16) |
| Wardrobe-only stylist | Same face, three outfits |
| In-game knight weapons | `p-video-avatar` dialogue cam |
| Game character reaction dorm | Scene 7 legacy |

Plan: [`output/launches/p-video-replace-announcement/announcement_plan.json`](../../../output/launches/p-video-replace-announcement/announcement_plan.json)
