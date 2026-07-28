# Motion composition craft (HTML / HyperFrames)

Vendor-neutral patterns for **designed reels**: timed HTML compositions (HyperFrames, Remotion exports, or similar) where layout, type, and stills/clips carry the message. Adapt colors, fonts, and scene count to the brand and brief.

For concat, captions, and beds on a finished render, stay in the other references in this guide. For HyperFrames install and render commands, see [combination-hyperframes.md](./combination-hyperframes.md).

---

## What this covers

| In scope | Out of scope |
|----------|----------------|
| Act structure, on-screen copy, framed media, VO timing, motion habits | Generating images/video (use image/video tools first) |
| Borrowing *approach* from a reference reel | Copy-pasting another reel’s scene order verbatim |
| Instructional / promo / example reels | Long-form film dramaturgy (`video-prompting`) |

---

## Visual system — proposals, not requirements

These are **starting suggestions** for a small token set you might reuse in CSS across scenes. They are not a default theme. Replace every value with brand guidelines or the brief when you have them.

| Token | Typical role | Example direction |
|-------|----------------|-------------------|
| Canvas | Full-bleed background | Often near-black; optional radial glow behind hero content |
| Accent | Tags, active borders, highlights | One hue is enough |
| Body font | Headlines and paragraphs | Sans, readable at 1080p |
| Mono font | Steps, URLs, commands, labels | Optional; can signal “technical” without a terminal UI |

**Framed media — proposal:** When the deliverable is “here is output” — still series, product shots, demo tiles — showing assets **inside** cards or bordered frames, not only full-bleed wallpaper, often reads clearer. A blurred **cover** layer behind **contain** foreground is one way to avoid flat letterbox gray; skip it if the brief prefers full-bleed.

**Logo — proposal:** A light-on-dark wordmark for the full timeline, top-right above a footer bar, repeated smaller on the CTA beat, is a common social pattern. See [social-usecase-reel.md](./social-usecase-reel.md) for one HyperFrames layout.

**Copy + picture — proposal:** Split layouts with text column + visual column help when the viewer must read steps while seeing an example. Full-bleed hero + lower title bar works when the image is the hook. Choose per brief; neither is mandatory.

---

## Story shape (open interpretation)

There is no single correct act count. Common **patterns** — mix, omit, or repeat:

| Pattern | When it helps |
|---------|----------------|
| **Hook** | Name the idea or outcome in the first few seconds |
| **Explain** | Numbered steps, demo flow, or “how it works” — use when the viewer must follow a process |
| **Evidence** | Grid, carousel, or spotlight on 1–N examples |
| **Close** | One action: link, hashtag, signup, or “try it” — avoid stacking three CTAs |

Write a short **spec** — acts, target duration, VO script, on-screen beats — before authoring HTML. Lock root `data-duration` to **measured narration + tail hold**, not the first guess.

For **named flow presets** — hook → context → reel → close, showcase-first, and so on — **rotating hero vs grid**, and **showcase length tied to VO end**, see [narrated-showcase.md](./narrated-showcase.md).

**VO vs on-screen text:** Align on *meaning*, same story. They need not match word-for-word. For process videos, VO can stay conversational while the second beat shows **numbered steps** with fuller detail: URLs, limits, platform names.

**Narration tone:** For briefs about *concept and process*, VO can describe the task without repeating every constraint that appears on screen — e.g. “lock style across frames” on screen, “pick a concept that feels camera-real” in VO.

---

## Borrow approach, don’t clone templates

| Do | Don’t |
|----|--------|
| Reuse **tokens**, calm VO, bed under speech, `check` before `render` | Reuse another project’s **exact scene order** if the brief differs |
| Take inspiration from split hooks, mono pills, framed grids | Drop in a terminal typing scene unless the brief is literally about install/CLI |
| Lead with what makes **this** deliverable unique | Swap only the title on someone else’s launch and ship |

**Sanity check:** If retitling the piece makes it look like a different product’s announcement, change structure—not just copy.

---

## Motion and scene structure

| Habit | Why |
|-------|-----|
| **Opacity crossfade** between stacked layers (same frame) | Avoid swapping one `<img src>` — causes visible pops on seek/render |
| **Fewer hard scene cuts** when one layout can carry multiple beats | GSAP timeline on a stable DOM; scenes as clips only when layout changes radically |
| **Subtle Ken Burns** on stills inside frames | Motion without distracting from content |
| **Stagger** reveals (copy, then tiles) | Matches Skills-style polish; optional |
| Register motion on `window.__timelines["main"]` (paused) | HyperFrames seek-safe render |

Creative freedom: terminal panels, chat mocks, kinetic type, 6-up grids, or minimal single-layout carousels are all valid when the spec calls for them.

---

## Instructional second beats

When the middle of the reel teaches a **process** (onboarding, rules, recipe, workflow):

1. **Number steps** (1–4 is readable at 1080p; shorten copy per step).
2. Put **access details** (URLs, free tiers, API docs) in secondary mono lines or a side panel—not only in VO.
3. Give the explain beat **enough duration** (often 35–55% of VO) so viewers can read; don’t flash a wall of text for two seconds.
4. Follow with an **example** beat (grid or spotlight) if you have generated or captured samples.

Side panels styled like app windows are optional chrome—not required for every instructional reel.

---

## Audio

| Element | Guidance |
|---------|----------|
| **Narration** | Generate or record first; measure duration; place narration clip at **t=0** in the composition for caption alignment |
| **Bed** | Instrumental under VO, typically ~10–15% of narration level for explainers/promos ([background-music.md](./background-music.md)) |
| **Tone** | Conversational for how-to; avoid trailer bark unless the brief is hype |

Embed bed in HTML or mux after caption burn—see [combination-hyperframes.md](./combination-hyperframes.md) §5.

---

## Delivery loop

```text
spec → VO (+ measure) → author index.html → npm run check → render → optional captions/bed (ffmpeg)
```

| Step | Note |
|------|------|
| Render to a **temp file**, then replace deliverable | Avoids partial overwrites and helps tools notice new bytes |
| Run **check** before every render | Catches contrast, missing assets, timeline issues |
| If preview looks stale after re-render | Player may cache identical files; remux or re-open file |

---

## Anti-patterns

| Mistake | Fix |
|---------|-----|
| `data-duration` shorter than VO | Measure audio; add tail on last scene |
| One `<img>` + JS src swap for a slideshow | Layer images; crossfade opacity |
| All text in VO, nothing on screen for a how-to | Add numbered or titled beats |
| Clone another reel’s acts for a different brief | Re-spec acts for this message |
| Burn captions in HTML **and** post-render ASS | Pick one path ([combination-hyperframes.md](./combination-hyperframes.md)) |

---

## Related

- [combination-hyperframes.md](./combination-hyperframes.md) — HyperFrames project layout, tracks, post-render captions
- [social-usecase-reel.md](./social-usecase-reel.md) — one portrait workflow-demo layout: structure plus optional visual examples
- [captions.md](./captions.md) — phrase-bar burn after render
- [background-music.md](./background-music.md) — bed mux

Project-specific examples outside this guide may live in your repo’s launch or campaign folders; extract **patterns** from them using this doc, not copy-paste HTML.
