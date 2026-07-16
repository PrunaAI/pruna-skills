# Illustrated story reel — positive still prompts

Still-line guidance for **illustrated-story-reel** (`hero_prompt`, `style_bible`, `edit_prompt` per beat). **No `video_prompt`** — motion is Ken Burns in ffmpeg only.

## Principle

Describe **what appears** in each frame — never what to leave out. Saying `no text` often **creates** readable type. Be explicit about the single frame you want.

**Never** use `no …`, `avoid …`, `not …`, `without …`, `don't`, or `do not` in creative fields. Spoken narration lines may use natural negation.

## Banned patterns → positive rewrite

| Banned pattern | Write explicitly instead |
|----------------|--------------------------|
| `no text` / `no signage` / `no labels` | `plain unmarked walls`, `unprinted wood surfaces`, `matte unprinted props` |
| `avoid markets` / `avoid text` | `plain wood table`, `single camera angle`, `one focal subject` |
| `without vocals` (music bed prompt) | `instrumental only` |
| `no cartoon` / `no modern` | `painterly historical illustration`, `period-accurate props only` |

## Rules

1. **One positive sentence per beat** — location, subject, light, `one camera angle`.
2. **`style_bible`** — positive comma-clauses only. Match `defaults.aspect_ratio` (e.g. `16:9 horizontal frame` for landscape).
3. **`edit_prompt`** — one composed still per beat; use `chain_from_previous` for visual continuity.
4. **`ken_burns`** — `zoom_in`, `zoom_out`, `pan_left`, `pan_right`, or `none` (set per beat or in defaults).

## Text & signage (most common)

| Blocked phrase in stills | Use instead |
|--------------------------|-------------|
| `farmers market`, `signage`, `neon signs` | produce on **plain wood table**, **matte unprinted** baskets |
| `labeled`, `packaging`, `price tag`, `menu` | **matte unprinted** jars, food in **plain glass bowl** |
| `graphic tee`, `poster`, `magazine` | solid-color fabrics, unbranded matte props |
| `maps`, `newspaper`, `headline`, `caption` | blank folded parchment, plain walls, unmarked wood |

## Collage & layout

| Blocked phrase | Use instead |
|----------------|-------------|
| `split`, `side by side`, `grid`, `collage`, `montage`, `multiple angles` | one subject, one camera angle, one frame |
| `OPENING:` / `CLOSING:` prefixes | plain scene description |
| `storyboard`, `triptych` | one continuous composition |

## Good vs bad still lines

| Bad | Good |
|-----|------|
| `No text, farmers market` | `Plain wood table`, matte baskets, sunny window, **one camera angle** |
| `Avoid labels on packaging` | **Matte unprinted** jars on **plain counter** |
