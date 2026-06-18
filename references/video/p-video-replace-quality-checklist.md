# p-video-replace quality checklist

Run on source video, each reference image, and every replacement output.

## Applies to

See the canonical mapping in [`generation-quality-checklists.md`](./generation-quality-checklists.md).

## Input gate (pre-render)

- Source **`video`** is the intended scene (motion, audio, and framing to keep).
- **`replace_target`** is explicit: character, clothing, object, or mixed.
- **`subject_in_video`** (or equivalent plan note) lists what in the source will be swapped.
- **`images`** array has **1–4** clear references (rights cleared); one still per slot.
- **Product/object refs** are bare packshots — no person, hands, or scene props in frame.
- **`instruction_prompt`** maps each reference to a **specific** source slot — not generic "replace the person."
- **Localized swaps:** prompt ends with *only [X] changes; everything else stays as the source* for clothing/object rows.
- **Held-object scenes:** prompt names the **person** as swap target and lists the prop as preserved.
- **`multi_job` rows:** each reference has its **own** `instruction_prompt` when using a launch runner or plan JSON.
- **`single_call` rows:** one prompt maps index order to screen position (left/right, shelf L→R, etc.).
- **`resolution`** and **`target_fps`** match delivery spec.
- **Variant batches:** review at **720p**; finals at **1080p** only for approved rows.
- Source **`video_prompt`** uses continuous camera when footage is generated (not locked-off).
- Generated sources default to **`p-video-avatar`** (not I2V) for VO + replace rows unless user supplies upload.
- **`multi_job`** rows: each reference has its own mapped `instruction_prompt`; prefer over `single_call` for mixed/UGC/cafe/SKU ladders.
- VO rows: plate shows garments/props named in `voice_script`; `video_prompt` keeps mouth in frame; clothing/object prompts preserve lips.

## Launches reel gates (skills-library)

Run [visual-variety-bible.md](./visual-variety-bible.md) checklist **before** Phase B. Additional gates for 7-scene launch reels:

- [ ] **Cast ledger:** when `plate_mode: p-image`, source host ≠ hero and ≠ slider ref faces — unique people per scene row
- [ ] **Thumbnail read:** each reference still readable at **256px** width — bold silhouette, accent color, shallow DOF
- [ ] **Adjacent variety:** neighboring refs differ in **medium + palette + setting**, not just hair or wardrobe tint
- [ ] **Instruction color match:** `instruction_prompt` garment colors match ref prompt (lime crew ≠ forest green)
- [ ] **No screens:** no laptops, keyboards, monitors, or readable UI in plate or refs — notebook / tumbler / mug only
- [ ] **`multi_image_beat`:** hybrid slider indices (2–4) mapped in dedicated `instruction_prompt`; per-ref jobs still have individual prompts
- [ ] **Spoken copy:** no API jargon (*replace jobs*, *multi_job*) in `voice_script` — human documentary tone

## Replacement fidelity

- Output preserves source motion, timing, and scene structure.
- Swapped element reads from the reference (face, outfit, or object) — not the original.
- **Clothing-only** jobs: face and body identity stable unless intentionally recasting.
- **Object-only** jobs: hands, surfaces, and camera path unchanged except the product/prop.
- **Character recast:** voice/timbre from **source** audio, not the reference portrait.
- Audio (when `save_audio` is true) stays aligned with the source clip.

## Technical quality

- No severe flicker, warping, or unstable anatomy on swapped regions.
- Product labels and garment edges reasonably sharp after replace.
- Output duration matches the source video length.

## Clean delivery

- No accidental overlays, stray text, or watermark-like artifacts unless requested.
- Clip is ready for downstream edit, concat, or platform upload.
