# p-image quality checklist

Run after each `p-image` output.

## Applies to

See the canonical mapping in [`generation-quality-checklists.md`](./generation-quality-checklists.md).

## Composition and prompt fidelity

- Main subject and action match the prompt intent.
- Framing and `aspect_ratio` fit destination (`9:16`, `16:9`, etc.).
- Style bible is present and respected (no unrequested style drift).

## Visual integrity

- No major anatomy defects (extra fingers, warped limbs, broken symmetry where it matters).
- No obvious rendering artifacts (mush textures, duplicated objects, clipped elements).
- Background supports the scene and does not distract from the subject.

## Cleanliness and delivery

- No accidental logos, watermarks, UI elements, or stray text unless requested.
- Image is acceptable as-is or marked for `p-image-edit` / `p-image-upscale` next.
