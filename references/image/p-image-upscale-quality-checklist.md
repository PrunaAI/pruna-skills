# p-image-upscale quality checklist

Run after each `p-image-upscale` output.

## Applies to

See the canonical mapping in [`generation-quality-checklists.md`](./generation-quality-checklists.md).

## Resolution and detail

- Effective detail increased versus source (not just larger dimensions).
- Important features remain sharp (eyes, logos, product edges, text if intentionally present).
- Chosen `target` MP is appropriate for destination (avatar plate ~4 MP; print up to 128 MP).

## Fidelity to source

- Geometry and identity are preserved (no face/product drift).
- Colors and contrast stay within acceptable variance.
- `enhance_realism` did not introduce unwanted style or texture changes.

## Artifact scan

- No haloing, ringing, oversharpening, or waxy/plastic skin textures.
- No checkerboard/noise amplification in flat regions.
- Output format and quality settings (`png`/`jpg`/`webp`) match delivery needs.
