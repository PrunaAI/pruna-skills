# p-video-2-pro quality checklist

After each `p-video-2-pro` output is saved, **open the clip and review it visually** (and listen — generated audio is expected) against this checklist (agent vision review — see `generation-diversity`).

Shared motion / frame-anchor items: also run [p-video-quality-checklist.md](./p-video-quality-checklist.md).

## Applies to

See the canonical mapping in `generation-diversity`. Cinematic generation path for visual-only `image-to-video` and `visual-transition-reel`. Audio-led jobs stay on `p-video-2`.

## Quality vs `p-video-2` / `p-video`

- Multi-beat blocking holds (product unfold, dialogue, weather) without collapsing into a single pose.
- Heavier physics stay readable (water, fire, fabric, hair) when the prompt asked for them.
- Full-body anatomy stays coherent through fast motion.
- Close-up / foreground objects stay readable (hands, product, face, packshot label).
- Input-image identity holds when `image` was set; last-frame composition matches when `last_frame_image` was set.

## Lip-sync and speakers

When the prompt implies speech or singing (there is **no imported `audio`**):

- Mouth follows the **written line** — pause / line / rest.
- At most **two** speaking faces stay separable; reject crowded dialogue with 3+ talkers.
- Talking-head-only jobs with no native scene audio should have used `p-video-avatar` instead.

## Generated audio

- The file is not unintentionally silent — output includes generated audio.
- Score, ambience, SFX, or dialogue match what the prompt named.
- Do not fail the job for missing an **uploaded** track — that brief belongs on `p-video-2`.
- Do not treat weak SFX as a pass if the brief was sound-effect-led — warn and offer a bed in post (`audio-prompting`) or a `p-video-2` mux.

## Camera and length

- Runtime is in the **5–15s** window and matches the requested `duration` (default 5).
- Output is **480p or 768p** as requested — not 720p / 1080p / 4K.
- Output is **24 fps**.
- When `mode: quality` was set, the clip should look tighter than a `mode: speed` preview of the same seed — if it does not, say so.

## Scene anchors

When using a first/last-frame pair, apply the pair sections in [p-video-quality-checklist.md](./p-video-quality-checklist.md), substituting `p-video-2-pro` for the prediction model. Do not expect a scene-anchor triple on this model.
