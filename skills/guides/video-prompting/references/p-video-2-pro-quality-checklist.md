# p-video-2-pro quality checklist

After each `p-video-2-pro` or `p-video-2-pro-reference` output is saved, **open the clip and review it visually** and listen to the audio (agent vision review — see `generation-diversity`). Both pro models return generated sound. On `p-video-2-pro-reference`, uploaded audio is guidance only unless `keep_audio: true` was sent with exactly one audio file — then that file is the soundtrack.

Shared checklist scope: also run the motion, story-fidelity, and general technical-quality checks in [p-video-quality-checklist.md](./p-video-quality-checklist.md). For standard `p-video-2-pro`, also apply its normal scene-anchor pair checks, including exact start/end matching. For `p-video-2-pro-reference`, do **not** inherit those exact endpoint assertions; replace them with the soft directional opening/closing fidelity checks below.

## Applies to

See the canonical mapping in `generation-diversity`. Cinematic generation path for `image-to-video` and `visual-transition-reel`; use `p-video-2-pro-reference` when imported image or video references should condition identity, style, motion, timing, or performance, with optional audio guidance or one kept soundtrack (`keep_audio`). 1080p / draft / scene-anchor triple jobs stay on `p-video-2`.

## Quality vs `p-video-2` / `p-video`

- Multi-beat blocking holds (product unfold, dialogue, weather) without collapsing into a single pose.
- Heavier physics stay readable (water, fire, fabric, hair) when the prompt asked for them.
- Full-body anatomy stays coherent through fast motion.
- Close-up / foreground objects stay readable (hands, product, face, packshot label).
- Standard `p-video-2-pro`: input-image identity holds when `image` was set; last-frame composition matches when `last_frame_image` was set.

## Standard generated speech (`p-video-2-pro` only)

When the standard prompt implies speech or singing:

- Mouth follows the **written line** — pause / line / rest.
- At most **two** speaking faces stay separable; reject crowded dialogue with 3+ talkers.
- Talking-head-only jobs with no native scene audio should have used `p-video-avatar` instead.

## Standard generated audio (`p-video-2-pro` only)

- The file is not unintentionally silent — output includes generated audio.
- Score, ambience, SFX, or dialogue match what the prompt named.
- Do not expect an uploaded track; standard `p-video-2-pro` has no audio import.
- Do not treat weak SFX as a pass if the brief was sound-effect-led — warn and offer a bed in post (`audio-prompting`) or a `p-video-2` mux.

## Reference fidelity (`p-video-2-pro-reference`)

- Each image reference’s assigned identity, material, composition, or style role is recognizable without forcing unrelated roles onto it.
- Each video reference’s assigned motion, camera rhythm, or performance role is reflected without claiming exact choreography.
- Each audio reference’s assigned timing, cadence, energy, or performance role is reflected. Without `keep_audio`, do **not** require the uploaded audio to survive as an exact soundtrack.
- No two references compete for the same role without an explicit priority; if the output visibly averages or oscillates between them, simplify the set and rerun.
- First/last frame references guide a **soft** opening/closing state. Review directional fidelity, not exact-pixel endpoint matching.
- Without `keep_audio`, the output carries **generated sound** — it matches the ambience, SFX, or line the prompt named and is not unintentionally silent.

## Kept soundtrack (`p-video-2-pro-reference` with `keep_audio`)

- The uploaded track is present as the clip's audio, not replaced or remixed.
- Motion, cuts, and any lip movement follow the track's beats, cadence, or words.
- Track shorter than `duration`: it plays first and the generated remainder does not jar. Track longer than `duration`: it is cut at `duration`. Track within 1 s of `duration`: clip length follows the track.

## Camera and length

- Runtime is in the **5–15s** window and matches the requested `duration` (default 5).
- Output is **480p or 768p** as requested — not 720p / 1080p / 4K.
- Output is **24 fps**.
- On `p-video-2-pro`, when `mode: cost` was set, treat visual quality as equivalent to `mode: speed` of the same seed — do not fail for looking like speed.
- On `p-video-2-pro`, when `mode: quality` was set, the clip should look tighter than a `mode: speed` or `mode: cost` preview of the same seed — if it does not, say so.
- For `p-video-2-pro-reference`, output is **480p or 768p** and `mode` is **cost or speed only**. Reject payloads or manifests that claim 1080p, draft, or quality mode.

## Scene anchors

When using a first/last-frame pair on `p-video-2-pro`, apply the pair section in [p-video-quality-checklist.md](./p-video-quality-checklist.md), substituting `p-video-2-pro` for the prediction model, including its exact start/end matching assertions. For `p-video-2-pro-reference`, apply only the pair section’s identity, plausible-path, camera-continuity, smooth-timing, and anti-teleportation checks; replace both exact start/end matching assertions with soft directional opening/closing fidelity. Do not expect a scene-anchor triple on either pro model. On `p-video-2-pro-reference`, a `keep_audio` track is kept, but 1080p or draft audio-led jobs stay on `p-video-2`.
