# Interactive explainer — positive prompts & blocked phrases

Extracted reference for [interactive-explainer](../../workflows/interactive-explainer/SKILL.md). The runner enforces these via `validate_plan` and `STILL_PROMPT_TRIGGERS` in [`run_from_plan.py`](../../workflows/interactive-explainer/scripts/run_from_plan.py).

## Principle

`hero_prompt`, `style_bible`, `edit_prompt`, `last_frame_edit_prompt`, `video_prompt`, `voice_prompt`, and bed `prompt` must describe **what appears** — never what to leave out.

Saying **`no text`** often **creates** readable type. Saying **`avoid crowds`** still invokes crowds. Be explicit about the single frame you want.

**Never** use `no …`, `avoid …`, `not …`, `without …`, `don't`, or `do not` in creative fields. Spoken lines (`scene_lines`, `voice_scripts`) may use natural negation for history dialogue.

## Banned patterns → positive rewrite

| Banned pattern | Write explicitly instead |
|----------------|--------------------------|
| `no text` / `no signage` / `no labels` | `plain unmarked walls`, `unprinted wood surfaces`, `matte unprinted props` |
| `avoid markets` / `avoid text` | `plain wood table`, `single camera angle`, `one focal subject` |
| `not theatrical` / `no cuts` | `restrained matter-of-fact delivery`, `single uninterrupted take` |
| `without vocals` | `instrumental only` |
| `no cartoon` / `no modern` | `painterly historical illustration`, `period-accurate 1770s props only` |

## Rules (summary)

1. **One positive sentence per still line** — location, subject, light, period, `one camera angle`.
2. **`style_bible`** — positive comma-clauses only. Example: `unprinted wood and parchment surfaces, plain unmarked walls, warm saturated full color, 16:9`.
3. **Character `edit_prompt`:** `lips visible`, **slight angle from the side**; use `speaks directly to camera` in **`video_prompt`** only.
4. **`video_prompt` (narrator):** OPEN / MID / CLOSE — camera + light + atmosphere ([interactive-explainer-motion.md](./interactive-explainer-motion.md)).
5. **`video_prompt` (character):** `single continuous medium close-up`, `one very slow push-in`, `single uninterrupted take` — not OPEN/MID/CLOSE beats.
6. **`p-video-avatar`:** `defaults.avatar_negative_prompt` is a **Pruna suppression token list** (nouns like `subtitles`, `watermark`) — not creative wording. See [`p_video_avatar_payload.py`](../../workflows/_shared/scripts/p_video_avatar_payload.py).

## Text & signage (most common)

| Blocked phrase in stills | Why | Use instead |
|-----------------|-----|-------------|
| `farmers market`, `market stall`, `storefront`, `signage`, `neon signs` | price boards, aisle signs | produce on **plain wood table**, **matte unprinted** baskets |
| `labeled`, `packaging`, branded bags, `price tag`, `menu`, `napkin` | product copy on surfaces | **matte unprinted** jars, food in **plain glass bowl** |
| `graphic tee`, `decal`, `sticker`, `magazine`, `poster` | printed type on surfaces | solid-color fabrics, unbranded matte props |
| `plated meal`, `restaurant`, `utensil`, `fork`, `knife` | menus, rim logos | **matte ceramic plate** on **plain counter**, subject food only |
| `documentary still`, `educational still`, `educational end`, `end frame`, topic-specific doc labels | models literalize meta words | `photoreal still`, `single frame`, `closing composition` |
| `ring light`, `studio lighting`, `HUD`, `game`, readable screens | UI text, spec overlays | sunny window, golden afternoon, soft monitor glow |
| `maps`, `map`, `newspaper`, `broadside`, `poster`, `placard`, `ledger`, `open book`, `proclamation`, `headline`, `caption`, `inscription`, ship names on hulls | printed type or named banners | blank folded parchment, plain walls, unmarked wood, **merchant wharf** / **colonial assembly hall** (no proper nouns on surfaces) |
| `greyscale`, `grayscale`, `graphite`, `muted-tone`, `desaturated`, cold mist / freezer haze | flat or grey frames | **warm saturated** full color, steady window light |
| `flicker`, `strobe`, `pulse`, rapid `light shifts` / `brightens` in **narrator** `video_prompt` | pulsating exposure in `p-video` | **one** slow push-in or pan in **steady** daylight |

## Collage & layout

| Blocked phrase | Use instead |
|-------|-------------|
| `split`, `side by side`, `before and after`, `comparison`, `grid`, `collage`, `montage`, `contact sheet`, `flat lay`, `packshot`, `multiple angles`, `dual` | one subject, one camera angle, one frame |
| **`OPENING:` / `CLOSING:`** prefixes on still lines | plain scene description — labels read as **two-panel storyboard** frames |
| **`Same …`** matching prior shot | describe the one frame directly; use `still_from` / `_cast_*` for identity |
| Counted triples in stills (`three ships`, `three panels`) | “colonial ships at one wharf”, “one camera angle” |
| `storyboard`, `frame by frame`, `triptych`, `cross-section` (unless one diagram is the sole subject) | one continuous composition, one camera angle |

Runner **`sanitize_still_prompt`** strips `OPENING:`/`CLOSING:` and leading `Same` before API calls.

## Weather

| Blocked phrase | Use instead |
|-------|-------------|
| `rain`, `wet pavement`, `puddle` | bright open sky, sunny window, golden afternoon |

## `style_bible` example (positive only)

```text
Premium painterly historical illustration, one focal subject per shot, one camera angle, 16:9, unprinted wood surfaces, plain unmarked walls, warm saturated full color, period-accurate props
```

## Good vs bad still lines

| Bad still line | Good still line |
|----------------|-----------------|
| `No text, no signage, farmers market` | `Plain wood table`, matte unprinted baskets, sunny window, **one camera angle** |
| `Avoid labels on packaging` | **Matte unprinted** jars on **plain counter** |
| Meta phrase **documentary still** + **end frame** | Concrete place + objects + **closing composition**, **one camera angle** |

Broader blocked-phrase table (keyboards, mirrors, packshots): [visual-variety-bible.md](../shared/visual-variety-bible.md#prompt-patterns).

**If text appears in `p-video` but stills are clean:** simplify the narrator `video_prompt` (camera/light only) or regenerate stills with **plain surfaces** — never answer with `no text` in the prompt.

## Related

- Workflow skill: [interactive-explainer/SKILL.md](../../workflows/interactive-explainer/SKILL.md)
- Motion: [interactive-explainer-motion.md](./interactive-explainer-motion.md)
- Scenes: [interactive-explainer-scenes.md](./interactive-explainer-scenes.md)
- Gates: [staged-generation-gate.md](../policies/staged-generation-gate.md)
