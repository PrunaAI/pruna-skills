# Character turnaround sheet (`p-image` → I2V)

Reusable identity plates before scene stills and video. Use when the brief needs the **same character** across multiple shots, not a one-off hero.

Talking-head cast ledgers and voice locks stay in [avatar-multi-scene prompt-templates](../../workflows/avatar-multi-scene/prompt-templates.md) and [realistic-persona-showcase.md](../shared/realistic-persona-showcase.md). This page is the **visual turnaround** handoff.

**Sources:** patterns adapted from [Square-Zero-Labs/video-prompting-skill](https://github.com/Square-Zero-Labs/video-prompting-skill) (Apache-2.0); rewritten for Pruna.

## Handoff order

```text
1. Character turnaround sheet  (p-image or multi-panel edit)
2. Scene stills                (p-image-edit from sheet / hero)
3. Video                       (p-video pair/triple — motion only)
```

Do not invent a new face in step 2. Lock identity from the sheet (or a single approved hero plate) and change only pose, camera, wardrobe state, or background beat.

## Sheet types

| Type | When | Prompt focus |
|------|------|--------------|
| **Turnaround** | Stylized or invented characters | Front, 3⁄4, profile, back — same outfit, neutral studio |
| **Expression row** | Performance / avatar prep | Same face + lighting; **distinct** emotions; include open-mouth for lip-sync |
| **Photoreal identity** | Real-person consistency | Same person photographed repeatedly; keep asymmetry, pores, age cues |
| **Wardrobe update** | Outfit change only | Same face/session framing; change clothes only |

## Turnaround prompt skeleton

```text
Character turnaround sheet of [named character], [age/build/species], wearing [exact outfit].
Four panels on one image: front view, three-quarter view, side profile, back view.
Identical face and costume in every panel. Neutral seamless studio backdrop #c8c8c8,
even softbox lighting, no story background, no props that change between panels.
[render style — e.g. documentary photoreal / cel-shaded anime]. Exact same character in every panel.
```

### Expression sheet add-on

```text
Expression row below: neutral, warm smile, concerned frown, surprised open mouth ready to speak.
Each expression clearly different. Mouth visible in every panel. Same lighting and camera height.
```

### Photoreal identity sheet

```text
Photoreal identity reference sheet of the same person photographed repeatedly in a studio.
Preserve freckles, asymmetric smile, skin texture, and eye color exactly.
Front and three-quarter views, soft window light, plain backdrop, no beauty retouching.
```

## Rules

1. **Neutral backdrop** — no narrative locations on the sheet (story backgrounds come in scene stills).
2. **Exact same character** language every time — models drift identity without it.
3. **Distinct expressions** — “slightly different smiles” collapses; name emotion + mouth state.
4. **One `style_bible`** — append the same medium/palette lock used in downstream edits and video.
5. **Params outside prompt** — aspect ratio and model stay in API `input`, not the text.
6. **Edit, don’t re-roll** — wardrobe or hair tweaks via `p-image-edit` from the locked sheet URL.

## Scene stills from the sheet

| Still | Source | Notes |
|-------|--------|-------|
| Hero / start | Sheet panel or locked hero URL | Match [scene-anchor](../video/scene-anchor-pair.md) OPENING composition |
| End | Start + `last_frame_edit_prompt` | Same subject in frame; physically reachable pose |
| Video | Motion-only `video_prompt` | Do not redescribe the face — see [prompt-dramaturgy.md](../video/prompt-dramaturgy.md) |

Identity lock line for edits:

```text
same [character name], identical face and costume, do not change species or age
```

## Anti-patterns

| Avoid | Why |
|-------|-----|
| Story background on the sheet | Locks the character into one location |
| Vague “consistent character” with no views | Model invents a new face per shot |
| Same expression labeled three ways | No usable performance range |
| Regenerating hero from text each scene | Identity drift |
| Mixing photoreal sheet with anime scene stills | Medium break mid-pipeline |

## Related

- Still craft: [prompt-golden-rules.md](./prompt-golden-rules.md)
- Pair / triple stills: [scene-anchor-pair.md](../video/scene-anchor-pair.md), [scene-anchor-triple.md](../video/scene-anchor-triple.md)
- Avatar multi-scene cast table: [prompt-templates.md](../../workflows/avatar-multi-scene/prompt-templates.md)
