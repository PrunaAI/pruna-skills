# Narrated showcase (multi-act)

Short **explain-and-show** pieces: spoken VO over designed frames, with existing clips or stills as proof. Works for product intros, portfolio reels, recap montages, or any “here is what this is + here is what it looks like” deliverable.

**Design language** (tokens, copy vs VO, instructional beats, motion habits): [motion-composition-craft.md](./motion-composition-craft.md). This doc focuses on **structure choice**, **reel timing**, and **showcase layout** options.

When the brief is open-ended, propose **two or three structure options** (see flows below) and ask which direction to keep before authoring HTML or ffmpeg graphs.

## When this pattern fits

| Fit | Often skip |
|-----|------------|
| VO carries the story; visuals support | Pure B-roll with no on-screen context |
| 3–8 source clips or stills already exist | Every pixel must be generative |
| 30–90s landscape or 9:16 social | Sub-10s motion stings → motion-graphics path in HyperFrames |
| You need labels, stats, or setup copy on screen | Single full-bleed clip only |

HyperFrames is the usual compose tool for **designed acts**; ffmpeg alone is fine for **concat + burn + bed** when there is no UI chrome. See [combination-hyperframes.md](./combination-hyperframes.md).

## Act building blocks (mix and reorder)

| Block | Typical job | Visual character |
|-------|-------------|------------------|
| **Hook** | Name the topic, promise, audience | Headline, optional badge, stat pills or short bullets |
| **Context** | How it works, constraints, steps | Text-forward panel, checklist, numbered layers — **can differ visually from the reel** |
| **Showcase** | Proof from real media | Grid, **single hero with crossfades**, sequential full-bleed beats, or PiP |
| **Close** | One action or link | Title + URL, command line, or hashtag — keep readable at a glance |

Nothing requires all four blocks. A **showcase-first** open (teaser grid, then context) is valid when the visuals are the hook.

## Suggested flows (starting points only)

| Flow | Order | Good when |
|------|-------|-----------|
| **A** | Hook → context → showcase → close | Specs or steps matter before clips |
| **B** | Hook → showcase → close | Visual-first; minimal copy |
| **C** | Showcase teaser → context → full showcase → close | “See it, then explain it” |
| **D** | Hook → panel / chat mock → close | Workflow or tool demo |
| **E** | Hook → sequential beats → close | 3–5 distinct messages, one visual each |
| **F** | Context → showcase | Internal or embed; light branding |

Rename, merge, or drop acts. Record the chosen flow in project notes (`structure_flow: …`) so later passes stay consistent.

## Showcase timing and motion

**Extend the showcase act until narration finishes** (VO often starts at **t=0** in the composition). Measure narration duration; set root `data-duration` and the showcase scene length from that, not from a first guess.

**Rotating hero (one large frame):** cycle clips with short crossfades for the whole showcase window; update on-screen labels per clip. Strong when clip count is low and you want **larger** frames.

**Grid:** show several tiles at once; good for breadth. Can still **highlight** one tile at a time with opacity or border while others stay visible.

**Sequential full-bleed:** one clip per beat; clearest when each clip needs full attention.

Match **clip `data-start` / `data-duration`** to segment boundaries when using HyperFrames. Prefer **stage-level** `<video>` elements (direct children of the composition root) when the linter reports nested timed media; align position with empty frame chrome in the scene if needed.

## Context vs showcase (visual separation)

If the **context** act is text-heavy (workflow steps, I/O, requirements), treat it as its own look: centered copy, staggered reveals, no duplicate of the showcase layout. That keeps the **showcase** act clearly “the reel” and avoids two identical preview columns.

Terminal chrome, cards, or minimal motion are all valid — the viewer should read context and showcase as **two different beats**.

## Audio and post

| Step | Notes |
|------|--------|
| VO | Generate or record first; embed at **t=0** — [motion-composition-craft.md](./motion-composition-craft.md) |
| Bed | Optional; often **post-mux** after captions — [background-music.md](./background-music.md) |
| Captions | Always **post-render** burn on the finished MP4 — [captions.md](./captions.md). Use **isolated narration** for whisperx when the mux has a loud bed |

Caption style is a creative choice: **word-accent karaoke**, **simple phrase lines** (bottom safe area), or **line-block**. Pick for readability and brand.

## ffmpeg-only shortcut

When there is no HTML layout:

1. Concat or crossfade clips to cover **narration length**
2. Mux VO (+ optional bed)
3. whisperx → ASS → burn

Use HyperFrames when you need **on-screen information design** (pills, layers, titles) beyond burned captions.

## Checklist

- [ ] Narration duration drives **showcase** (and total) length
- [ ] Context and showcase **look distinct** if both exist
- [ ] Captions burned **after** render; no duplicate subtitle layers in HTML
- [ ] Structure chosen or confirmed with the user when the brief was vague
- [ ] `npm run check` before HyperFrames render (layout, contrast, nested media)

## See also

- [motion-composition-craft.md](./motion-composition-craft.md) — example visual tokens, instructional beats, motion habits
- [combination-hyperframes.md](./combination-hyperframes.md) — project layout, render loop, anti-patterns
- [captions.md](./captions.md) — whisperx, ASS styles, ffmpeg-full
- Optional HTML composition skills — **showcase-style routes** and **structure catalogs** with feedback prompts for act order when the brief is open-ended
