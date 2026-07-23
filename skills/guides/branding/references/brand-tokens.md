# Brand tokens

Hex values extracted from the official logo kit SVGs. Use for caption accents, lower-thirds, CTA bars, and `frame.md` frontmatter.

## Core palette

| Token | Hex | Use |
| --- | --- | --- |
| `plum` | `#3A1451` | Primary brand purple — headlines, icon fill, dark UI |
| `plum-deep` | `#36124C` | Strokes, dark accents |
| `violet` | `#7A2293` | Secondary purple highlights |
| `green` | `#69A45C` | Leaf / accent green in the mark |
| `pink` | `#FF94FB` | Smile / playful accent |
| `ink-on-dark` | `#F5F5F5` | Wordmark on dark backgrounds |

## Example `frame.md` snippet

```yaml
---
name: pruna-launch
plum: "#3A1451"
accent: "#7A2293"
highlight: "#FF94FB"
ink: "#F5F5F5"
canvas: "#0F0614"
logo: assets/pruna-light.svg
---
```

Copy the chosen logo SVG into the project `assets/` folder and reference it from `logo:`.

## Caption / bar pairing

Launch-style burned captions often use:

- Phrase bar: white `#FFFFFF`
- Spoken-word accent: `#7A2293` or `#3A1451`
- Bottom promo bar: `#121214` background, `#FF94FB` or green accent rule

See `video-editing` → `captions.md` for burn-in mechanics; use these hex values for brand alignment.
