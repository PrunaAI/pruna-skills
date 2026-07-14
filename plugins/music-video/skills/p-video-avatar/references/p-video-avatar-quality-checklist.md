# p-video-avatar quality checklist

Before calling the model and after each avatar clip, **open the still or video and review it visually** against this checklist (agent vision review — see [generation-quality-checklists.md](https://github.com/PrunaAI/pruna-skills/tree/main/shared/generation-quality-checklists.md#who-applies-these-checklists)).

## Applies to

See the canonical mapping in [`generation-quality-checklists.md`](./generation-quality-checklists.md).

## Input still gate (pre-render)

- Face and mouth/beak are large and clear enough for lip-sync.
- Mouth/beak and eyes are unobstructed (no hair/props/foreground clutter crossing them).
- Head pose is speaking-friendly (avoid extreme angles, tiny head crop, or chin cutoff).
- Identity/style match cast bible and scene continuity.
- **Photoreal path:** skin reads natural (not mushy/waxy); plate matches [realistic-persona-showcase.md](https://github.com/PrunaAI/pruna-skills/tree/main/shared/realistic-persona-showcase.md) intent.
- **Try-on → avatar path:** try-on preservation passed; outfit details visible if script references them.

## Speech and performance

- Spoken output matches intended script/audio content.
- Voice choice is consistent for recurring characters.
- Delivery tone matches brief; `voice_prompt` is short and does not leak unintended text.
- **`voice_script`** reads as speakable human dialogue — not brochure/marketing copy.

## Motion and scene dynamism

- **`video_prompt`** is **unique to this clip** — not duplicated from other scenes in the same project.
- Motion grammar matches the still (props, setting, angle) — e.g. glance targets exist in plate.
- Multi-scene reels vary camera angle and movement — not every clip `medium close-up, gentle dolly push-in`.
- **Stylized clips:** motion energy matches `visual_style_tag` (anime vs documentary vs clay).
- **Motion templates:** when the clip is a source for `p-video-animate`, verify audible speech and visible lip sync — reject smile/wave-only outputs with no dialogue motion.

## Lip-sync and visual stability

- Mouth movement is plausible and synchronized.
- No facial warping, jitter, or unstable eye/teeth regions.
- Hands/props near face do not cause ambiguous anatomy artifacts.

## Clean delivery

- `video_prompt` results in clean framing/motion without prompt side effects.
- No accidental overlays, stray text, or watermark-like artifacts unless requested.
- For explainers / any text-prone still: `negative_prompt` + `negative_prompt_strength` > 0 on `p-video-avatar` (runner default or plan `defaults.avatar_negative_*`). Tune strength up only if artifacts persist — high values can harm identity/motion.
- Still lines stayed free of signage/label triggers; `style_bible` holds negations, not `edit_prompt`.
- Clip is ready for assembly with consistent style/voice across adjacent scenes.
