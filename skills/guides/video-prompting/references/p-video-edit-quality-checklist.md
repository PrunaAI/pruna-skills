# p-video-edit quality checklist

After each edit job, **open the source video, optional reference images, and output clip** and review them against this checklist (agent vision review — see `generation-diversity`).

## Applies to

See the canonical mapping in `generation-diversity`.

## Input gate (pre-render)

- Source **`video`** is the intended scene (≤ **15 seconds**; motion, audio, and framing to keep).
- **`prompt`** names one principal change and includes a keep-list (camera, motion, unmentioned subjects).
- Edit intent is explicit: attribute, remove, add, environment, relight, text, or reference-guided.
- **`images`** (if used) has **1–4** clear references (rights cleared); `prompt` maps each image to a source slot.
- Product/object refs are bare packshots — no extra hands or scene props in frame.
- Job is not a brand-new scene/plot, independently moving new in-hand object, or camera angle/zoom rewrite.
- **`draft`** and **`save_audio`** match the brief (draft for preview; `save_audio: true` to keep source audio).
- Optional API **`seed`** only when the user requested a reproducible rerun.

## Edit fidelity

- Requested change is present and obvious in every relevant frame.
- Locked regions remain stable (identity, product geometry, camera path, unmentioned props).
- "Change only X" constraints are respected; unrelated regions do not drift.
- Reference-guided jobs: added or swapped element reads from the still (shape, material, proportions) and stays attached through the camera move.
- Text jobs: named string is added, replaced, or removed; underlying pixels reconstruct cleanly.
- Audio (when `save_audio` is true) stays aligned with the source clip.

## Technical quality

- No severe flicker, warping, or unstable anatomy on edited regions.
- Output duration matches the source video length.
- Draft vs standard quality matches the chosen `draft` flag.

## Clean delivery

- No accidental overlays, stray text, or watermark-like artifacts unless requested.
- Clip is ready for downstream edit, concat, or platform upload.
