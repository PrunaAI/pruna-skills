# p-video-2 quality checklist

After each `p-video-2` output is saved, **open the clip and review it visually** (and listen when audio is expected) against this checklist (agent vision review — see `generation-diversity`).

Shared motion / frame-anchor items: also run [p-video-quality-checklist.md](./p-video-quality-checklist.md).

## Applies to

See the canonical mapping in `generation-diversity`. Audio-led / 1080p / draft path for `image-to-video`, `narrated-multi-scene`, `interactive-explainer`, and B-roll rows with imported audio. Visual-only cinematic pairs → `p-video-2-pro`. Use `p-video` for simpler / quicker clips.

## Quality vs `p-video`

- Subjects, backgrounds, and motion look sharper than a typical `p-video` draft of the same brief.
- Close-up / foreground objects stay readable (hands, product, face).
- Input-image identity holds when `image` was set.

## Lip-sync and speakers

When the prompt or `audio` implies speech or singing:

- **Native speech (no imported `audio`):** mouth follows pause / line / rest — this is the quality bar vs `p-video`.
- **Imported `audio`:** face/identity stays clean; do not fail the job solely because visemes are not tighter than `p-video`.
- At most **two** speaking faces stay separable; reject crowded dialogue with 3+ talkers.
- Talking-head-only jobs with no native scene audio should have used `p-video-avatar` instead.

## Native audio

- When `save_audio` is true (default), the file is not unintentionally silent.
- Uploaded `audio` is embedded and not truncated (TTS was ≤ ~19s; API cap 20s).
- Do not treat weak SFX as a pass if the brief was sound-effect-led — warn and offer a bed in post (`audio-prompting`).

## Camera and length

- Camera move is stable (slow push / hold / one dolly) — not an extreme cinematic stunt.
- If `duration` was omitted (no audio), runtime matches the prompt’s implied beat.
- If `duration` was set, runtime is in the 1–20s window and matches the request.
- Output is 720p or 1080p as requested — not 4K.

## Scene anchors

When using pair or triple payloads, apply the pair/triple sections in [p-video-quality-checklist.md](./p-video-quality-checklist.md), substituting `p-video-2` for the prediction model.
