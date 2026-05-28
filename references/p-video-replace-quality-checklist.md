# p-video-replace quality checklist

Run on source video, each reference image, and every replacement output.

## Applies to

See the canonical mapping in [`generation-quality-checklists.md`](./generation-quality-checklists.md).

## Input gate (pre-render)

- Source **`video`** is the intended scene (motion, audio, and framing to keep).
- **`replace_target`** is explicit: character, clothing, object, or mixed.
- **`subject_in_video`** (or equivalent plan note) lists what in the source will be swapped.
- **`images`** array has **1–4** clear references (rights cleared); one still per slot.
- **`instruction_prompt`** maps each reference to a **specific** source slot — not generic "replace the person."
- **`multi_job` rows:** each reference has its **own** `instruction_prompt` when using a launch runner or plan JSON.
- **`single_call` rows:** one prompt maps index order to screen position (left/right, shelf L→R, etc.).
- **`resolution`** and **`target_fps`** match delivery spec.
- Source **`video_prompt`** uses continuous camera when footage is generated (not locked-off).
- Generated sources default to **`p-video-avatar`** (not I2V) for VO + replace rows unless user supplies upload.
- **`multi_job`** rows: each reference has its own mapped `instruction_prompt`; prefer over `single_call` for mixed/UGC/cafe/SKU ladders.
- VO rows: plate shows garments/props named in `voice_script`; `video_prompt` keeps mouth in frame; clothing/object prompts preserve lips.

## Replacement fidelity

- Output preserves source motion, timing, and scene structure.
- Swapped element reads from the reference (face, outfit, or object) — not the original.
- **Clothing-only** jobs: face and body identity stable unless intentionally recasting.
- **Object-only** jobs: hands, surfaces, and camera path unchanged except the product/prop.
- Audio (when `save_audio` is true) stays aligned with the source clip.

## Technical quality

- No severe flicker, warping, or unstable anatomy on swapped regions.
- Product labels and garment edges reasonably sharp after replace.
- Output duration matches the source video length.

## Clean delivery

- No accidental overlays, stray text, or watermark-like artifacts unless requested.
- Clip is ready for downstream edit, concat, or platform upload.
