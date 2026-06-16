# p-image-try-on quality checklist

Run after each `p-image-try-on` output.

## Applies to

See the canonical mapping in [`generation-quality-checklists.md`](../shared/generation-quality-checklists.md).

## Garment fit and identity

- Each requested garment appears on the person (correct category — see supported types in [p-image-try-on SKILL.md](../../tools/image/p-image-try-on/SKILL.md#garment-categories)).
- Unsupported garment types were not silently dropped without the user knowing (check logs / re-run with supported refs only).
- Garment color, pattern, and key details match the reference (within reasonable lighting variance).
- Person identity (face, skin tone, hair) is preserved unless the brief asked otherwise.
- Fit looks natural at shoulders, waist, sleeves, and hem — no obvious floating or clipping.

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
