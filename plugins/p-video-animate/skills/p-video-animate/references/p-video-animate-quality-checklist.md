# p-video-animate quality checklist

After each animate job, **open the source video, reference image, and output clip** and review them against this list (agent vision review — see [generation-quality-checklists.md](https://github.com/PrunaAI/pruna-skills/tree/main/policies/generation-quality-checklists.md#who-applies-these-checklists)).

## Applies to

See the canonical mapping in [`generation-quality-checklists.md`](https://github.com/PrunaAI/pruna-skills/tree/main/policies/generation-quality-checklists.md).

## Input gate (pre-render)

- Source **`video`** is the intended motion template (camera path, acting, timing, scene structure); motion is **clear and readable** (not blurry, fast-cut, or low-contrast).
- Reference **`image`** clearly shows the subject to animate (face/body unobstructed, rights cleared).
- **First-frame alignment:** framing, pose, and visible limbs match the **first frame** of the source video (or repose with **`p-image-edit`** first).
- **Mismatch risk:** head-and-shoulders still + full-body template → expect lost choreography, not full-body motion.
- **Proportion fit:** human full-body motion on meme/mascot/chibi subjects often breaks legs, arms, and contact points—flag before generate.
- **`instruction_prompt`** (if used) describes **behavior overrides only** — not a repeat of the image description.
- **`resolution`** and **`target_fps`** match delivery spec.
- Source longer than budget: plan to **split** the template and animate segments (~5 s compute per 1 s video).

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
