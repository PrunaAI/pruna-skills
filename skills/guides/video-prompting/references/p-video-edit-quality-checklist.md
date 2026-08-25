# p-video-edit quality checklist

After each edit job, **open the source video, any reference images, and the output clip** and review them against this checklist (agent vision review — see `generation-diversity`).

## Applies to

See the canonical mapping in `generation-diversity`.

## Input gate (pre-render)

- Source **`video`** is the intended scene and is **≤ 15 seconds** — output duration follows it.
- Subject stays visible; exposure is stable; no extreme camera motion or heavy occlusion over the edited region.
- **`prompt`** carries **one principal change**, not a stack of unrelated edits.
- **`prompt`** ends with a preserve-list: geometry, motion, camera movement, lighting, shadows, untouched objects.
- Cut-heavy or long clips include a persistence clause (*in every frame · after every cut*).
- **`images`** (0–4) are bare packshots in `jpg`, `jpeg`, `png`, or `webp`, rights cleared.
- Every reference passed is **named** in the prompt (*shown in the reference image*).
- Job is **not** an identity/person swap — that routes to `p-video-replace`.
- A **`draft: true`** pass ran before the full-quality run; the prompt is locked.
- **`seed`** fixed when A/B testing wording; one variable changed per run.
- **`prompt_upsampling`** left `true` unless the run is a deliberate literal test.
- **`save_audio`** matches delivery (source audio kept when true).

## Edit fidelity

- Only the named element changed — background, cast, wardrobe, and props not mentioned are untouched.
- Preserve-list held: camera path, timing, subject performance, and lighting match the source.
- Reference-guided rows read from the reference (shape, material, proportions), not the original object.
- Added objects stay attached and correctly aligned through the whole camera move.
- Removals reconstruct the surface behind them plausibly — no smear, ghost, or repeated texture.
- Environment and relight rows keep subject identity, geometry, and shadows coherent.

## Technical quality

- Edit holds across **every** frame and survives each cut — no drift back to the source look.
- No severe flicker, warping, or unstable anatomy on edited regions.
- Text removal leaves no residual glyph edges or halos.
- Product labels and material edges reasonably sharp after the edit.
- Audio (when `save_audio` is true) stays aligned with the source clip.
- Output duration matches the source video length.

## Clean delivery

- Draft artifacts are gone in the final run (`draft: false`).
- No accidental overlays, stray text, or watermark-like artifacts unless requested.
- Clip is ready for downstream edit, concat, or platform upload.
