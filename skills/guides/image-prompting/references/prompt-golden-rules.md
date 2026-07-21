# Image prompt golden rules (`p-image` / `p-image-edit`)

Production-grade still prompts for Pruna. **`p-image` has no prompt upsampling** — concrete language is the whole craft.

Tag structure, ritual seed, and diversity axes stay in [generation-diversity.md](../../generation-diversity/references/generation-diversity.md). This page is the creative-director layer on top.

**Sources:** patterns adapted from [smixs/visual-skills](https://github.com/smixs/visual-skills) (MIT) and [higgsfield-ai/skills](https://github.com/higgsfield-ai/skills) (MIT); rewritten for Pruna.

## Before writing any prompt

1. Complete the [random seed ritual](../../generation-diversity/references/generation-diversity.md#random-seed-ritual-mandatory-before-every-generation) (SSoT).
2. Name at least four clauses from [explicit prompt structure](../../generation-diversity/references/generation-diversity.md#explicit-prompt-structure-required).
3. Apply the rules below — then confirm `prompt` + `aspect_ratio` with the user.

## Golden rules

### 1. Lead with concrete subject + action

Name who/what and a frozen verb. Avoid mood-only openers.

| Bad | Good |
|-----|------|
| `cool cyberpunk vibe, neon` | `Courier in rain-slick jacket vaults a puddle under kanji neon, wet asphalt reflections` |

### 2. Positive framing only

Describe presence, not absence. Negation often invokes the thing you forbid.

| Want | Write | Avoid |
|------|-------|-------|
| Empty street | `empty street, wide wet asphalt` | `street with no cars` |
| Clean wall | `plain unmarked wall, matte paint` | `no text, no signs` |
| Solo subject | `solo portrait, one person` | `no other people` |

Full text hygiene: [generation-diversity — text & typography](../../generation-diversity/references/generation-diversity.md#text--typography-by-model).

### 3. Natural sentences over tag soup

| Bad | Good |
|-----|------|
| `car, neon, city, night, 8k, masterpiece` | `Wide shot of a sports coupe speeding through a rainy Tokyo side street at night; neon reflecting on wet pavement and metal` |

### 4. Be specific (hex, materials, placement)

| Element | Vague | Specific |
|---------|-------|----------|
| Subject | `a woman` | `elderly jazz singer in a sequined shawl, mid-laugh` |
| Material | `shiny` | `brushed steel with matte black grips` |
| Color | `dark green` | `#0d3d2d deep emerald` |
| Placement | `on the right` | `right third of frame, subject bleeding off edge` |

### 5. Typography on surfaces

Readable copy is **static text on a surface** — not spoken dialogue (that is `p-video` Mode A → [audio-in-video-prompting.md](../video/audio-in-video-prompting.md)).

**Template** (placeholders in square brackets are docs notation, not prompt syntax):

```text
Typography:
[surface]: "[EXACT STRING]" in [weight], [color or hex], [placement in frame]
```

Rules:

- Put exact copy in **double quotes** — never paraphrase
- Always name **surface** + **placement** (upper third, lower right of display, centered on label)
- Add weight/color when it matters (bold condensed sans, cream #hex)
- One primary text element per still unless the user wants a layout brief
- Default: no readable copy — [generation-diversity text hygiene](../../generation-diversity/references/generation-diversity.md#text--typography-by-model)
- Prefer scenes without dense typography — `p-image` is weak at multi-line UI copy
- **Not** spoken dialogue (`[subject] says "…"`) — use `p-video` Mode A
- **Not** square-bracket `[tags]` — those are Gemini TTS performance tags only; stills use quoted strings

### 6. Params stay outside the prompt

Never put model name, `aspect_ratio`, resolution, duration, or API field names in the prompt string. Those belong in `input` JSON.

### 7. Edit, don't re-roll

If a still is ~80% right, use `p-image-edit` with a surgical change (`Change background to soft #e8e4dc gradient, keep subject identical`) instead of regenerating from scratch.

### 8. One world / genre anchor max

Use **one** high-level anchor, then concrete details:

| Type | Example |
|------|---------|
| Era + place | `Havana, 1957` + linen suit, harsh noon sun under awning |
| Cultural / style | `Studio Ghibli mood` + moss stones, morning mist, monk sweeping |
| Genre look | `documentary portrait, natural skin pores` |

Do **not** stack genre anchors (`Wes Anderson + Lindbergh + Ghibli` → mush).

## Banned filler (strip before send)

These add heat without rendering: `masterpiece`, `best quality`, `8k`, `4k`, `ultra detailed`, `stunning`, `epic`, `beautiful lighting`, bare `cinematic` with no camera/light nouns.

Replace with concrete camera + light from [camera-lighting-vocabulary.md](../video/camera-lighting-vocabulary.md) or diversity `camera_tag` / `lighting_tag`.

Photoreal anti-slop lock when needed: [generation-diversity — photoreal anti-slop](../../generation-diversity/references/generation-diversity.md#photoreal-anti-slop-neon--stylized-briefs).

## Continuity handoffs

| Goal | Path |
|------|------|
| Same face across many stills | [character-turnaround-sheet.md](./character-turnaround-sheet.md) → scene stills → I2V |
| Talking-head / avatar cast | [realistic-persona-showcase.md](../shared/realistic-persona-showcase.md) + avatar prompt templates |
| Start/end plates for video | [scene-anchor-pair.md](../video/scene-anchor-pair.md) / [scene-anchor-triple.md](../video/scene-anchor-triple.md) |

## Pre-send checklist

- [ ] Ritual seed stated; axes logged
- [ ] Subject + action + setting named (no mood-only prompt)
- [ ] Positive framing; no `no text` / `without X`
- [ ] Hex or named materials where color matters
- [ ] On-image copy: quoted string + surface + placement (if any)
- [ ] No API params inside the prompt string
- [ ] At most one genre/era anchor + concrete details
- [ ] No banned filler words
