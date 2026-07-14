# p-image-ideogram — example prompts

**Before every job:** [random seed ritual](../../../references/shared/random-seed-ritual.md) · [explicit prompt structure](../../../references/shared/generation-diversity.md#explicit-prompt-structure-required) · [text rules by model](../../../references/shared/generation-diversity.md#text--typography-by-model).

`mode` includes prompt upsamplers — long specific prompts and named typography are OK. Default **`mode: medium`** for finals; raise for dense `text_rendering` rows.

Photoreal persona bar: [realistic-persona-showcase.md](../../../references/shared/realistic-persona-showcase.md).

## Dynamic / playground (no readable copy)

**Brief:** packed roller-rink energy, single frame, no collage triggers.

```text
Disco ball reflections on an otter DJ scratching vinyl at a packed 1970s roller rink,
fish-eye lens, glitter confetti mid-air, funky energy
```

```bash
export REPLICATE_API_TOKEN="r8_..."

curl -s -X POST \
  -H "Authorization: Bearer ${REPLICATE_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "prompt": "Bioluminescent jellyfish nightclub at abyss depth, VIP anglerfish in sunglasses at velvet rope, teal-magenta cinematic lighting",
      "aspect_ratio": "16:9",
      "mode": "medium"
    }
  }' \
  "https://api.replicate.com/v1/deployments/prunaai/p-image-ideogram-preview/predictions"
```

## Text rendering (`text_rendering`)

**Brief:** multiple strings + surfaces; list every string in the prompt. Use `mode: high` or `very high` when legibility matters.

```text
Hong Kong neon alley at night, fearless grandmother in floral apron juggling dumplings,
awning reads HAPPY HOUR 5-7, kiosk sign PRUNA AI, fish-eye lens, crisp legible typography
```

```bash
curl -s -X POST \
  -H "Authorization: Bearer ${REPLICATE_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "prompt": "Circus poster on brick wall: headline THE GREATEST OTTER, subtitle ONE NIGHT ONLY, ringmaster otter in top hat mid-bow, baroque oil painting, crisp legible typography",
      "aspect_ratio": "3:4",
      "mode": "high"
    }
  }' \
  "https://api.replicate.com/v1/deployments/prunaai/p-image-ideogram-preview/predictions"
```

**Avoid:** `no text`, `without signs` — negation often invokes copy. Prefer `plain unmarked walls` when you want blank surfaces.

## Photoreal founder plate (avatar downstream)

**Brief:** 9:16 talking-head plate — mouth visible, documentary lock. Route here instead of `p-image` when fidelity matters.

```text
South Asian woman founder mid-30s, documentary portrait at cast-iron loft window,
natural skin pores, mouth visible, hands away from mouth, golden hour side light, photoreal editorial
```

Set `aspect_ratio: "9:16"`, `mode: medium`. Lock hero plate URL before `p-image-edit`, `p-image-try-on`, or `p-video-avatar`.

## When to use `p-image` instead

Fastest drafts, mood boards, bulk panels with no dense typography → [p-image](../../../tools/image/p-image/SKILL.md) (Pruna P-API; no prompt upsampling).
