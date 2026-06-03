# p-video-animate quality checklist

Run on source video, reference image, and every animated output.

## Applies to

See the canonical mapping in [`generation-quality-checklists.md`](./generation-quality-checklists.md).

## Input gate (pre-render)

- Source **`video`** is the intended motion template (camera path, acting, timing, scene structure).
- Reference **`image`** clearly shows the subject to animate (face/body unobstructed, rights cleared).
- **Pose and framing alignment:** shot size, facing direction, and visible limbs match the motion template (or repose with **`p-image-edit`** first).
- **Proportion fit:** human full-body motion on meme/mascot/chibi subjects often breaks legs, arms, and contact points—flag before generate.
- **`instruction_prompt`** (if used) steers subject behavior without contradicting source motion.
- **`resolution`** and **`target_fps`** match delivery spec.

## Motion transfer fidelity

- Output preserves source motion, timing, and camera movement (not a generic re-enactment).
- Acting beats and scene structure track the reference video.
- Subject identity and style come from the reference image, not the source video's actor.

## Technical quality

- No severe flicker, warping, or unstable anatomy during motion.
- Audio (when `save_audio` is true) stays aligned with visual motion.
- Output duration matches the source video length.

## Clean delivery

- No accidental overlays, stray text, or watermark-like artifacts unless requested.
- Clip is ready for downstream edit, concat, or platform upload.
