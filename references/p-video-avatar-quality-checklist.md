# p-video-avatar quality checklist

Run on every still before generation and on every avatar output.

## Applies to

See the canonical mapping in [`generation-quality-checklists.md`](./generation-quality-checklists.md).

## Input still gate (pre-render)

- Face and mouth/beak are large and clear enough for lip-sync.
- Mouth/beak and eyes are unobstructed (no hair/props/foreground clutter crossing them).
- Head pose is speaking-friendly (avoid extreme angles, tiny head crop, or chin cutoff).
- Identity/style match cast bible and scene continuity.

## Speech and performance

- Spoken output matches intended script/audio content.
- Voice choice is consistent for recurring characters.
- Delivery tone matches brief; `voice_prompt` is short and does not leak unintended text.

## Lip-sync and visual stability

- Mouth movement is plausible and synchronized.
- No facial warping, jitter, or unstable eye/teeth regions.
- Hands/props near face do not cause ambiguous anatomy artifacts.

## Clean delivery

- `video_prompt` results in clean framing/motion without prompt side effects.
- No accidental overlays, stray text, or watermark-like artifacts unless requested.
- Clip is ready for assembly with consistent style/voice across adjacent scenes.
