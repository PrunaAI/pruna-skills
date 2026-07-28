# Social use-case reels — HyperFrames portrait

Patterns for **short workflow demo promos**: one capability proof, persistent metadata bar, intro slide, and CTA.

**Structure vs. look:** Act order, full-length demo timing, and HyperFrames lint fixes below are **pattern guidance** that prevents broken renders and muddy storytelling. Colors, type sizes, footer layout, pills, and logo placement in the examples are **proposals only** — swap them for brand guidelines or the brief.

For HyperFrames install, tracks, and post-render captions, start at [combination-hyperframes.md](./combination-hyperframes.md). For act vocabulary and motion habits, [motion-composition-craft.md](./motion-composition-craft.md).

---

## When this layout fits

| Fits | Use something else |
|------|---------------------|
| Single workflow proof: input → output video, slider, or clip | Multi-act narrated explainers → [narrated-showcase.md](./narrated-showcase.md) |
| Portrait social, ~1080 wide + fixed footer | Landscape launch reels at 1920×1080 → HyperFrames `/general-video` |
| Metadata bar: category · use case · model · speed/price or similar | Full-screen kinetic hook with no footer |

---

## Suggested act order

Durations are **typical**, not targets. Avoid duplicating the footer in a long title hook when an intro slide already carries the title.

| Act | Typical duration | Content |
|-----|-------------------|---------|
| **Intro** | ~2–2.5s | Category badge, use case title, **model or product name**, optional metric pills with the same facts as the bar, not repeated in a long hook |
| **Demo** | **Full source video length** | Framed clips; for image → MP4 workflows, a still beat then crossfade to output is one common approach; Input / Output labels optional |
| **CTA** | ~2.5–3s | Primary action: try or demo URL; secondary: API or account sign-up URL; model name as reminder if useful |
| **Bar** | Whole timeline | Category · use case, model, optional Speed / Price or equivalent chips |

Lock root `data-duration` to intro + demo beats + CTA + small tail hold.

---

## Video timing — do not truncate

| Rule | Why |
|------|-----|
| Set `<video>` **`data-duration`** to **probed file length** | HyperFrames stops playback at `data-duration`; shorter values cut the demo |
| Use **`id`** on every timed `<video>` | Missing `id` can freeze video in render per HyperFrames lint |
| **`data-has-audio="true"`** when the clip keeps source sound; keep `muted` otherwise | Lint requires explicit audio intent |
| Cap length only for **reference motion** tiles at ~3.5s, not primary outputs | Reference is B-roll, not the deliverable |

Still → video: after an **intro** slide if you use one, one beat can show an input still with Ken Burns then crossfade to the **full-length** output MP4. Splitting the first step into a separate opener-only still *before* the intro usually duplicates the input.

---

## Example visual direction — suggestions only

Not a brand spec or default theme. The table is **one dark portrait proposal**; treat every row as optional inspiration.

| Token | Example proposal |
|-------|------------------|
| Canvas | Near-black base, subtle radial glow behind hero |
| Accent | One hue for bar stripe and pill borders |
| Footer | Two columns: context + model on the left, metric chips on the right |
| Media | Blurred **cover** backdrop + **contain** foreground; optional accent inset on “cinema” frames |
| Logo | Light wordmark on dark — top-right watermark + optional CTA repeat |

**Type scale, proposal only:** on a ~1080×1372 canvas, context ~30–32px, model ~24px mono, metric values ~22px often pass contrast and lint checks. Truncate long bar titles with ellipsis if `text_box_overflow` fires.

---

## HyperFrames checklist before render

```bash
npm run check   # fix errors; contrast + text_box_overflow on bar copy
npm run render
```

| Lint / motion | Fix |
|---------------|-----|
| `media_missing_id` on `<video>` | Add unique `id` |
| `video_missing_muted` / `data-has-audio` | Match audio policy |
| Duplicate same `src` on two `<img>` clips | One hero image per scene: backdrop via CSS or a single layer |
| `text_box_overflow` on bar | Shorter copy or slightly smaller context font |
| Overlapping GSAP on same target | One ken-burn tween or use `overwrite: "auto"` |

Post-render, same as other HF promos: bed via [background-music.md](./background-music.md), avatar captions via [captions.md](./captions.md) when needed, GIF export optional.

---

## Logo watermark — optional pattern

Copy an approved PNG into `hyperframes/assets/`, for example `brand-logo.png`. Full-timeline clip:

```html
<img id="brand-logo" class="clip logo-watermark" data-start="0" data-duration="45"
  data-track-index="95" src="assets/brand-logo.png" alt="" />
```

Place top-right above the footer; repeat smaller on the CTA scene if the brief asks for brand reinforcement. For ffmpeg-only paths, see [overlays.md](./overlays.md).

---

## Anti-patterns

| Mistake | Fix |
|---------|-----|
| 5.5s cap on all MP4s | Full probed duration on output demos |
| Hook repeats bar title + model | Dedicated **intro** slide for title + model; bar stays context-only during demo |
| No CTA | End on URLs the brief names; try + sign-up is a common pair |
| Flat gray letterboxing | One fix: blurred cover backdrop behind a contain layer; other looks are valid too |
| ffmpeg concat for framed UI + pills | HyperFrames scenes |

---

## Related

- [combination-hyperframes.md](./combination-hyperframes.md) — two-phase render + polish
- [overlays.md](./overlays.md) — logo on plain MP4
- [motion-composition-craft.md](./motion-composition-craft.md) — more optional token and layout proposals
