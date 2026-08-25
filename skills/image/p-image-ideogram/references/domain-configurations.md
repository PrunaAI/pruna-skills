# Domain configurations (verticals & job type)

Use with **`p-image-ideogram`** when a **`vertical-*`** workflow (or any brief) implies a job type. **SSoT for knobs:** `thinking`, `image_size`, prompt form (natural language vs Ideogram JSON), and batch discipline. **Agent default:** **`thinking: high`**, **`prompt_upsampling: true`**. Set **`prompt_upsampling: false`** for JSON prompts, locked on-image copy, or verbatim wording.

**Before POST:** list exact on-image strings in the plan; pick the profile below; show prompt + knobs unless the user locked wording.

## Profiles

| Profile | `thinking` | `image_size` | Prompt form | When |
| --- | --- | --- | --- | --- |
| **photoreal-standard** | `medium` | `1K` | NL | Product/scene heroes, portraits, staging fills — **no** critical readable copy |
| **photoreal-hero** | `medium` | `2K` | NL | Large crop, print-bound, or single hero that must stay sharp at 100% |
| **type-heavy** | `high` | `2K` | NL | Headlines, titles, CTAs, shade names — **every string literal in the prompt** |
| **type-structured** | `high` | `2K` | [JSON caption](./ideogram-json-prompting.md) | Multi-zone layouts, brand hex, repeated panels, exact placement |
| **type-micro** | `high` | `2K` | JSON preferred | Many small labels (dimensions, SKUs, shade grid, spec callouts) |
| **type-premium** | `very high` | `2K` | NL or JSON | Maximum quality — complex hero compositions with multiple text elements, intricate layouts, or flagship creative where cost is secondary to output quality; ~2× cost of `high` |
| **draft-explore** | `low` | `1K` | NL | Internal exploration only — user asked cheap/fast → prefer **`p-image`** instead |

**Batch:** for **type-heavy**, **type-structured**, and **type-micro**, run **≥4 parallel seeds** (async), pick one winner visually. **photoreal-standard** may use 1–4 seeds when the hero gates downstream edits.

**Upsampling:** default **`true`** for NL prompts. Stay **`false`** for JSON prompts and for any brief with locked copy.

## Complexity ladder (quick pick)

1. **No readable text** → **photoreal-standard** (raise to **photoreal-hero** for print/large delivery).
2. **One headline or title** → **type-heavy**.
3. **Several strings or one brand hex** → **type-heavy** or **type-structured** (JSON if layout must repeat).
4. **Spec sheet / ad board / dimension overlay** → **type-micro** or **type-structured** (JSON).
5. **Flagship creative / complex multi-element composition** → **type-premium** (when absolute best quality justifies ~2× cost).

## By vertical skill

Rows apply to **`p-image-ideogram`** photo-generation steps in that vertical. Use-case `#` matches that vertical skill's `references/use-cases.md` table.

### `vertical-marketing-ugc`

| Use case # | Job | Profile | `aspect_ratio` notes |
| --- | --- | --- | --- |
| 1 | Ad concept from brief | **type-structured** (multi-placement) or **type-heavy** (single headline) | Match destination: `1:1`, `9:16`, `16:9`; one job per placement if copy differs |

### `vertical-education`

| Use case # | Job | Profile | Notes |
| --- | --- | --- | --- |
| 1 | Instructor from portrait | **photoreal-standard** | Face/hands visible; avoid dense type on face |
| 4 | Course illustrations & covers | **type-heavy** | Title + chapter pill; JSON if title strings are locked |

### `vertical-gaming`

| Use case # | Job | Profile | Notes |
| --- | --- | --- | --- |
| 1 | Key art from brief | **type-heavy** | Game title in frame → JSON if title + tagline are locked |

### `vertical-furniture-home`

| Use case # | Job | Profile | Notes |
| --- | --- | --- | --- |
| 4 | Dimensioned sketch / spec still | **type-micro** | Dimension lines + SKU; JSON for label elements |
| 8 | Missing packshot (generate photo) | **photoreal-standard** | No spec overlay |

### `vertical-beauty-cosmetics`

| Use case # | Job | Profile | Notes |
| --- | --- | --- | --- |
| 1 | On-model / product hero | **photoreal-standard** if no shade copy; **type-heavy** if shade names on swatches | JSON when >3 shade strings |

### `vertical-fashion-apparel`

| Use case # | Job | Profile | Notes |
| --- | --- | --- | --- |
| 2 | Catalog hero | **photoreal-standard** | Try-on path uses **`p-image-try-on`**, not ideogram config |

### `vertical-automotive`

| Use case # | Job | Profile | Notes |
| --- | --- | --- | --- |
| 1 | Configurator hero from brief | **photoreal-standard** | Trim/badge copy → **type-heavy** |

### `vertical-food-beverage`

| Use case # | Job | Profile | Notes |
| --- | --- | --- | --- |
| 1 | Dish hero from description | **photoreal-standard** | Menu name on plate → **type-heavy** |

### `vertical-real-estate`

| Use case # | Job | Profile | Notes |
| --- | --- | --- | --- |
| 5 | Missing angle / twilight fill | **photoreal-standard** | Rarely type; do not add listing copy in generated photos |

### `vertical-hi-tech-electronics`

| Use case # | Job | Profile | Notes |
| --- | --- | --- | --- |
| (gap — generate photo) | Packshot / lifestyle fill when edit cannot source | **photoreal-standard** | Port labels or UI chrome → **type-heavy**; prefer **`p-image-edit`** for screen cleanup |

## Example `input` shapes (conceptual)

**photoreal-standard:**

```json
{
  "prompt": "… concrete scene …",
  "thinking": "medium",
  "image_size": "1K",
  "prompt_upsampling": false,
  "aspect_ratio": "16:9"
}
```

**type-heavy:**

```json
{
  "prompt": "… scene … headline text exactly SHOP NOW … subline exactly Aurora Buds Pro … legible sans serif …",
  "thinking": "high",
  "image_size": "2K",
  "prompt_upsampling": false,
  "aspect_ratio": "16:9"
}
```

**type-structured:** same knobs; `prompt` body is Ideogram 4.0 JSON per [ideogram-json-prompting.md](./ideogram-json-prompting.md).

## Vertical playbooks

Each **`vertical-*`** skill's `references/workflow-playbook.md` points here for phase **2 — Hero / gaps**. Do not duplicate the full matrix in vertical skills — cite the row for that industry.
