# p-video quality checklist

Run after each `p-video` output.

## Applies to

See the canonical mapping in [`generation-quality-checklists.md`](./generation-quality-checklists.md).

## Motion and story fidelity

- Video follows the prompt beat and intended camera grammar.
- Motion is temporally coherent (no sudden identity/scene jumps).
- Runtime and pacing fit the requested duration/use case.

## Technical quality

- Output `resolution` / `fps` meet the brief.
- No severe flicker, frame tearing, or unstable object geometry.
- If image-to-video: subject identity and core composition remain anchored to the input still.

## Scene anchor triple (narrated multi-scene)

When using [scene-anchor-triple.md](./scene-anchor-triple.md):

- Start still matches `input.image`; end still matches `input.last_frame_image`.
- Clip duration follows uploaded `audio` (no manual `duration`).
- Motion in the prompt bridges start → end without contradicting narration.
- Scene *N* end still aligns with scene *N+1* start when `frame_chain` is enabled.
- Narration is **not** truncated (audio passed to `p-video`, not post-muxed).

## Audio-conditioned runs (when `audio` is used)

- Visual rhythm aligns with audio beats and speech cadence.
- Duration matches audio expectation.
- No unintentionally silent/truncated output or desync in downstream assembly.
