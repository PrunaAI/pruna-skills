# p-video quality checklist

After each `p-video` output is saved, **open the clip and review it visually** against this checklist (agent vision review — see [generation-quality-checklists.md](../../generation-diversity/references/generation-quality-checklists.md#who-applies-these-checklists)).

## Applies to

See the canonical mapping in [`generation-quality-checklists.md`](../../generation-diversity/references/generation-quality-checklists.md).

## Motion and story fidelity

- Video follows the prompt beat and intended camera grammar.
- Motion is temporally coherent (no sudden identity/scene jumps).
- Runtime and pacing fit the requested duration/use case.

## Technical quality

- Output `resolution` / `fps` meet the brief.
- No severe flicker, frame tearing, or unstable object geometry.
- If image-to-video: subject identity and core composition remain anchored to the input still.

## Scene anchor pair (visual transitions)

When using [scene-anchor-pair.md](./scene-anchor-pair.md) with **`image`** + **`last_frame_image`**:

- **Subject in both stills** — same person, animal, or product visible in start and end; reject end edits that drop the subject.
- **Identity lock** — face, uniform, fur, and palette match between plates; only pose and background change.
- **Physically plausible path** — motion in the prompt could happen in the real world (walk through a door, ride, gradual environmental morph).
- **Camera continuity** — one move (dolly, track, pan); no sudden angle or scale jumps unless start/end stills justify it.
- **Smooth timing** — OPEN hold → MID travel (most of clip) → CLOSE settle; prefer **8–10s** for character beats.
- Start still matches `input.image`; end still matches `input.last_frame_image`.
- No teleporting, empty-room morphs, or subject disappearing mid-clip.

## Scene anchor triple (narrated multi-scene)

When using [scene-anchor-triple.md](./scene-anchor-triple.md):

- Start still matches `input.image`; end still matches `input.last_frame_image`.
- Clip duration follows uploaded `audio` (no manual `duration`; ≤ **20s** API max).
- TTS per scene was probed **≤ ~19s** before render (longer lines truncate even with `input.audio`).
- Motion in the prompt bridges start → end without contradicting narration.
- Scene *N* end still aligns with scene *N+1* start when `frame_chain` is enabled.
- Narration is **not** truncated (`input.audio` passed to `p-video`, not post-muxed over silent clips).

## Audio-conditioned runs (when `audio` is used)

- Visual rhythm aligns with audio beats and speech cadence.
- Duration matches audio expectation.
- No unintentionally silent/truncated output or desync in downstream assembly.
