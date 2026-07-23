# Logo kit

Official Pruna marks shipped with the `branding` skill. Paths are relative to the skill root (`skills/guides/branding/` in-repo, or the installed skill directory).

**Rule:** copy these files — do not regenerate, recolor, or warp the mark.

## Layout

```
assets/logo-kit/
├── svg/   ← prefer for HTML, HyperFrames, and uniform scaling
└── png/   ← prefer for ffmpeg overlay inputs
```

## Variants

| File stem | Mark | Best on |
| --- | --- | --- |
| `pruna-colored` | Full wordmark, brand colors | Light or neutral backgrounds; hero/end cards |
| `pruna-dark` | Full wordmark, dark ink | Light backgrounds |
| `pruna-light` | Full wordmark, light ink | Dark or saturated backgrounds |
| `pruna-monogram-colored` | Icon only, brand colors | Avatars, small corners, app icons |
| `pruna-monogram-dark` | Icon only, dark | Light backgrounds, tight corners |
| `pruna-monogram-light` | Icon only, light | Dark backgrounds, tight corners |

## Selection

| Background | Wordmark | Monogram (small corner) |
| --- | --- | --- |
| White / light gray / pastel | `pruna-dark` or `pruna-colored` | `pruna-monogram-dark` or `pruna-monogram-colored` |
| Dark / purple / photo (busy) | `pruna-light` | `pruna-monogram-light` |
| Mixed / unknown | `pruna-colored` wordmark | `pruna-monogram-colored` |

When in doubt on a launch reel: **`pruna-light` wordmark** on dark plates, **`pruna-colored`** on the final CTA card.

## Usage

### ffmpeg watermark (bottom-right, ~8% width)

```bash
LOGO="<SKILL_DIR>/assets/logo-kit/png/pruna-light.png"
ffmpeg -y -i input.mp4 -i "$LOGO" \
  -filter_complex "[1:v]scale=iw*0.08:-1[logo];[0:v][logo]overlay=W-w-40:H-h-40" \
  -c:a copy output.mp4
```

Swap `pruna-light.png` for the variant that contrasts with the plate.

### HyperFrames / HTML

```html
<img src="<SKILL_DIR>/assets/logo-kit/svg/pruna-colored.svg" alt="Pruna" />
```

Point `<SKILL_DIR>` at the installed skill path, or copy the SVG into the project's `assets/` folder.

### `frame.md` logo field

When authoring a project design spec, set `logo:` to the absolute or project-relative path of the chosen SVG — typically `pruna-colored.svg` or `pruna-light.svg`.

## Do not

- Prompt models to "draw the Pruna logo"
- Change hue, stretch non-uniformly, or add drop shadows that alter the mark
- Use `media-use --type logo --entity pruna` when this kit is available (these files are the canonical source)
