# Ideogram JSON prompting (4.0 caption schema)

**Vendor SSoT:** [JSON Prompting (Ideogram 4.0)](https://docs.ideogram.ai/using-ideogram/getting-started/prompting-guide/4.-json-prompting-ideogram-4.0) · [Markdown mirror](https://docs.ideogram.ai/using-ideogram/getting-started/prompting-guide/4.-json-prompting-ideogram-4.0.md)

P-Image-Ideogram is built on Ideogram-class generation. For **exact colors**, **bounding-box layout**, **per-line text placement**, and **repeatable compositions**, put a valid Ideogram 4.0 JSON caption in **`input.prompt`** (string). Natural language still works for quick photoreal exploration.

**Pruna call:** same `POST` as other stills — `Model: p-image-ideogram`. When the prompt body is JSON, set **`prompt_upsampling: false`** (same idea as Magic Prompt OFF on Ideogram).

## When to use JSON vs natural language

| Use case | Approach |
| --- | --- |
| Quick exploration, photoreal scenes, placement not critical | Natural language |
| Posters, branded graphics, GTM UI cards | JSON (or NL + upsampling only if brief is sparse) |
| Exact text placement (signage, labels, multi-headline layouts) | JSON with `"text"` elements + optional `bbox` |
| Specific palette (brand hex) | JSON `color_palette` on `style_description` and/or elements |
| Repeatable layout across seeds | JSON |

## Top-level caption fields

| Field | Required | Role |
| --- | --- | --- |
| `high_level_description` | Strongly recommended | One–two sentence image summary |
| `style_description` | Optional | Style, lighting, medium, palette |
| `compositional_deconstruction` | **Required** | `background` + `elements` list |

## `style_description`

Include **exactly one** of `photo` (camera/lens string) **or** `art_style` (non-photo). When present, also set `aesthetics`, `lighting`, and `medium`. Optional `color_palette`: up to **16** uppercase `#RRGGBB` hex strings.

**Key order (trained):**

| Caption type | Order |
| --- | --- |
| Photo | `aesthetics`, `lighting`, `photo`, `medium`, `color_palette` |
| Non-photo | `aesthetics`, `lighting`, `medium`, `art_style`, `color_palette` |

## `compositional_deconstruction`

`background` (string) **first**, then `elements` (array). Each element is `"obj"` or `"text"`.

| Type | Key order |
| --- | --- |
| `"obj"` | `type`, `bbox` (optional), `desc`, `color_palette` (optional) |
| `"text"` | `type`, `bbox` (optional), `text`, `desc`, `color_palette` (optional) |

- **`text`:** literal string to render in the image.
- **`desc`:** styling/placement prose for that element.
- **`color_palette`:** up to **5** uppercase `#RRGGBB` per element.

## Bounding boxes

Optional per element. Normalized **0–1000**, origin top-left:

```text
[y_min, x_min, y_max, x_max]
```

Example: `[250, 250, 750, 750]` centers an element; omit `bbox` to let the model place freely.

## Color rules

- Uppercase hex only: `#RRGGBB`
- Include background tones in `style_description.color_palette` when you need global mood
- Contrast pairs (highlight + shadow) help lighting control

## Minimal JSON example (no bboxes)

Pass as **`input.prompt`** (escape for JSON in curl):

```json
{
  "high_level_description": "A lone sailboat on calm water at golden hour.",
  "style_description": {
    "aesthetics": "serene, warm, golden hour",
    "lighting": "golden hour backlighting, warm atmospheric haze",
    "photo": "wide angle, f/8, long exposure",
    "medium": "photograph",
    "color_palette": ["#FF6B35", "#F7C59F", "#004E89", "#1A659E", "#2B2D42"]
  },
  "compositional_deconstruction": {
    "background": "Calm ocean to a low horizon, sky in orange and pink.",
    "elements": [
      {
        "type": "obj",
        "desc": "Single sailboat, white triangular sail, silhouetted against the sun."
      }
    ]
  }
}
```

Pair with **`thinking: "high"`**, **`image_size: "2K"`** when typography or layout density matters.

Full poster example with multiple `"text"` + `bbox` entries: vendor doc above.

## Agent checklist (JSON jobs)

- [ ] Valid JSON object (not truncated); key order matches schema tables
- [ ] Every visible string has a `"text"` element (or is described in `background` / `obj` only when appropriate)
- [ ] Brand hex in uppercase; count within palette limits
- [ ] `prompt_upsampling: false` unless user wants NL-style expansion
- [ ] Show parsed structure + API knobs before first paid `POST`
- [ ] Batch ≥4 seeds when layout is dense; pick visually — JSON improves repeatability, not perfection on seed 1
