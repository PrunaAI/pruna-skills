# p-image-try-on quality checklist

Run after each `p-image-try-on` output.

## Applies to

See the canonical mapping in [`generation-quality-checklists.md`](../shared/generation-quality-checklists.md).

## Scene preservation (garment-only edit)

The model should change **clothing only**. Fail if the plate’s world drifted:

- Face structure, skin tone, and expression match **`person_image`**.
- Hair length, color, and style unchanged (unless headwear was requested).
- Background, props, and scene geometry preserved (mirror lines, floor texture, street context).
- Lighting direction and shadow mood consistent with the plate.
- Pose and limb positions preserved (or match **`reference_pose`** when set).

See [p-image-try-on-showcase.md](./p-image-try-on-showcase.md#preservation-checklist-the-models-differentiator).

## Garment fit and identity

- Each requested garment appears on the person (correct category — see supported types in [p-image-try-on SKILL.md](../../tools/image/p-image-try-on/SKILL.md#garment-categories)).
- Unsupported garment types were not silently dropped without the user knowing (check logs / re-run with supported refs only).
- Garment color, pattern, logos, and key details match the reference (within reasonable lighting variance).
- **Complex garments:** patchwork panels, collaged prints, pleats, and color-blocks align at seams — no smeared or melted panels.
- Fit looks natural at shoulders, waist, sleeves, and hem — no obvious floating or clipping.

## Upstream person plate (before try-on)

If **`person_image`** was generated with **`p-image`**, confirm [p-image-quality-checklist.md](./p-image-quality-checklist.md) passed first — mushy or synthetic plates produce mushy try-ons.

- Photoreal editorial intent (not generic “fashion model white background” unless requested).
- Cast and setting match the showcase brief when building public examples — [visual-variety-bible.md](../shared/visual-variety-bible.md).

## Pose and composition

- When `reference_pose` was set, the output pose matches the reference closely enough for the use case.
- When `reference_pose` was omitted, the person remains in a plausible stance for the garment type.
- Framing and `preserve_input_size` behavior match the destination (PDP crop, full-body, etc.).

## Turbo vs normal mode

- If **`turbo: true`**, re-check every garment slot — turbo can miss items; retry in normal mode for final assets.
- With **more than 6 garments**, verify none were dropped or merged incorrectly.

## Non-flatlay / prompt (EXPERIMENTAL)

- When `prompt` was used, only the named garments from the named images were applied.
- No stray garments from multi-item reference photos leaked into the result.

## Technical and handoff checks

- Output dimensions and format match target use (`output_format`, `output_quality`).
- No major artifacts (smears, duplicated limbs, warped fabric textures).
- Result is ready for downstream `p-image-upscale`, `p-video`, or ecommerce handoff — or flagged for another pass.
