# p-image quality checklist

After each `p-image` output is saved, **open the file and review it visually** against this checklist (agent vision review — see [generation-quality-checklists.md](https://github.com/PrunaAI/pruna-skills/tree/main/shared/generation-quality-checklists.md#who-applies-these-checklists)).

## Applies to

See the canonical mapping in [`generation-quality-checklists.md`](./generation-quality-checklists.md).

## Composition and prompt fidelity

- Main subject and action match the prompt intent.
- Framing and `aspect_ratio` fit destination (`9:16`, `16:9`, etc.).
- Style bible is present and respected (no unrequested style drift).

## Persona plates (avatar / try-on / showcase)

When the output feeds **`p-video-avatar`**, **`p-image-try-on`**, or a public example set:

- **Style tagged** — matches planned `visual_style_tag` / `render_medium_tag` (photoreal, cel anime, clay, etc.).
- **Photoreal intent** (when photoreal) — natural skin texture; not waxy CGI unless stylized brief.
- **Cast specificity** — matches planned age, ethnicity, archetype — not generic “model”.
- **Dynamic world** — unique `setting_tag`; named lighting; **distinct `camera_tag`**; **distinct `aspect_ratio`** in multi-example batches — not default MC facing camera every row.
- **Avatar-ready** (when lip-sync next) — face large; mouth clearly visible; hands not covering mouth.
- **Try-on-ready** (when dressing next) — body regions for garment types visible (full-body, feet, head as needed).
- **`seed`** recorded when identity continues downstream.

Scenario matrix and style ladders: [realistic-persona-showcase.md](https://github.com/PrunaAI/pruna-skills/tree/main/shared/realistic-persona-showcase.md).

## Visual integrity

- No major anatomy defects (extra fingers, warped limbs, broken symmetry where it matters).
- No obvious rendering artifacts (mush textures, duplicated objects, clipped elements).
- Background supports the scene and does not distract from the subject.

## Cleanliness and delivery

- No accidental logos, watermarks, UI elements, or stray text unless requested.
- Image is acceptable as-is or marked for `p-image-edit` / `p-image-upscale` next.
