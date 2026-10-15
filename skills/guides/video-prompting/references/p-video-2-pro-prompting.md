# p-video-2-pro prompting

Shared MiniMax H3 prompt craft for `p-video-2-pro` and `p-video-2-pro-reference` (cinematic lanes next to `p-video-2`). Shared dramaturgy, camera, and physics: [prompt-dramaturgy.md](./prompt-dramaturgy.md), [camera-lighting-vocabulary.md](./camera-lighting-vocabulary.md), [physics-safe-motion.md](./physics-safe-motion.md). Visual frame payloads: [scene-anchor-pair.md](./scene-anchor-pair.md). QA: [p-video-2-pro-quality-checklist.md](./p-video-2-pro-quality-checklist.md). Exact uploaded-soundtrack triples stay on `p-video-2` — [scene-anchor-triple.md](./scene-anchor-triple.md).

**Routing by intent.** Use `p-video-2-pro` for standard text-to-video or first/last-frame generation with **generated audio**. Use `p-video-2-pro-reference` when imported image or video references should lock a subject or condition identity, style, motion, timing, or performance; it also returns **generated audio**, and one uploaded audio file can be kept as the soundtrack with `keep_audio`. Audio cannot qualify a reference request by itself. Use `p-video-2` for **1080p**, **draft** previews, or the scene-anchor triple with an uploaded soundtrack. Use `p-video` for cheaper, faster drafts.

## Common H3 strengths to write toward

- **Multi-beat cinematic blocking** in one clip (product unfold, chase, weather)
- **Heavier physics:** water, snow spray, fire, fabric, hair
- **Full-body anatomy** that stays coherent through fast motion
- Coherent camera paths and physically reachable OPEN/MID/CLOSE motion
- Strong foreground readability for faces, hands, products, and materials

## Standard lane (`p-video-2-pro`)

- Standard text, first-frame, and first+last-frame generation; first/last frames are direct anchors, not the reference model’s soft keyframes.
- Output includes **generated audio**. Write score, ambience, SFX, dialogue, or a spoken line into the prompt.
- **No audio import**: do not send `audio`; an uploaded soundtrack belongs on `p-video-2-pro-reference` (`keep_audio`) or `p-video-2`.
- Two-shot dialogue and written-line lip-sync are standard-lane strengths; keep speaking faces to one or two.
- `mode` is `cost`, `speed`, or `quality`. Only this standard lane has `quality`.
- `prompt_upsampler` is `off`, `turbo`, or `max`, independent of `mode`.

## Reference-conditioned lane (`p-video-2-pro-reference`)

Use the common MiniMax H3 craft above, then make the reference contract explicit:

- Assign **one role per asset** before prompting: e.g. image A = subject identity, image B = materials/style, video A = camera or motion rhythm, audio A = timing/performance. If two references compete for the same role, remove one or state a clear priority.
- Treat references as **conditioning, not exact-copy guarantees**. Describe what to preserve and what may change; do not promise exact identity, choreography, framing, or soundtrack reproduction.
- `first_frame_image` and `last_frame_image` are **soft opening/closing keyframes**, not exact first/last pixels. Prompt the intended approach and resolution rather than “match exactly.”
- Output includes **generated audio**. With no kept track, write ambience, SFX, score, or a short line into the prompt, as on the standard lane.
- Imported audio guides **timing or performance** by default. Name the desired beat, cadence, energy, or performance response; do not claim the output will contain the uploaded track.
- With `keep_audio: true` and **exactly one** audio file, that file becomes the soundtrack and the video is generated to match it. Describe how motion follows it (beats, cuts, lip movement to the voice) and do not describe a different soundtrack. Shorter audio plays first and the model generates the rest; longer audio is cut to `duration`.
- Keep the prompt + OPEN/MID/CLOSE motion coherent with every assigned role. More references are not automatically better; prefer the smallest non-competing set.
- This lane supports `mode: cost` and `mode: speed` only. **Never send or recommend `quality`**. Output is 480p or 768p; 1080p/draft remains `p-video-2`.

The request must include a prompt and at least one image or video reference; audio alone is not sufficient. Field shapes, counts, durations, validation limits, and billing belong to the `p-video-2-pro-reference` tool skill.

## Limits by lane

- Both H3 lanes max out at **768p**, **15s**, and 24 fps; neither has draft mode or native 4K.
- Standard `p-video-2-pro`: no audio import; `mode` supports cost/speed/quality; generated audio is expected.
- `p-video-2-pro-reference`: generated audio by default; imported audio is guidance, or the kept soundtrack with `keep_audio`; `mode` supports cost/speed only; first/last images are soft keyframes.
- Not an editor (`p-video-edit`) or talking-head avatar (`p-video-avatar`)
- On standard generated-dialogue jobs, more than two speakers degrades separation.

## Standard-lane examples (`p-video-2-pro`)

The examples and recipes below are standard-only: direct first/last anchors and `quality` mode do not transfer to the reference lane. Generated-audio wording does transfer when no `keep_audio` track is set.

### Fast pass vs locked-in

**Fast pass** — subject + action + scene. Enough for first looks. Iterate in `mode: cost` (price) or `mode: speed` (wall-clock).

```text
A matte stainless pour-over kettle sits on a seamless light-gray studio sweep. Thin steam rises from the spout.
```

**Locked-in** — add camera, lighting, style, and audio. Optional first-frame or last-frame still for repeatable runs.

```text
A narrative film scene, 1970s Roman trattoria at night, warm tungsten, cigarette haze, Super-8 grain. A man and a woman in period clothes sit at a small table with wine. She leans in and quietly says, "Then we leave before sunrise." The camera slowly dollies around the table. Audio: Italian radio pop from a small speaker, plates, low room tone, her line clear and close.
```

### Mode recipes (rewrite for the brief — do not paste)

**Text-to-video** — subject + action + camera + lighting + audio intent in one coherent line.

```text
A dramatic cinematic shot of an isolated lighthouse standing on a rocky cliff during an enormous Atlantic storm at dusk. The camera begins close to the lighthouse keeper standing outside near the railing as violent wind pulls at his coat. He turns toward the ocean just as a massive wave crashes against the cliff and sends water high above the lighthouse. The camera rapidly pulls back to reveal the scale of the storm. Photorealistic water physics, heavy rain, turbulent clouds, realistic human movement, and epic scale.
```

**Image-to-video (first frame)** — keep motion aligned with the reference frame.

```text
The camera slowly pushes in. The person turns their head and smiles naturally. Soft studio lighting, shallow depth of field.
```

**First + last frame** — standard-lane motion consistent with both direct anchors; end on the last-frame composition.

```text
Start on the still product hero. The camera holds, then a slow push-in as light moves across the metal. End exactly on the last-frame packshot, label readable, no extra props.
```

**Native speech (T2V)** — write the spoken line into the prompt. There is no `audio` field.

```text
A woman faces the camera and says "I'll be there in five." She pauses, delivers the line, then rests. Natural mouth motion, soft window light, camera holds steady.
```

## Duration, mode, upsampler (`p-video-2-pro`)

- Set `duration` (5–15s; default **5**). Partner demos often use **8s** for locked-in cinematic beats.
- `mode: cost` when price is the priority (same quality as `speed`, but cheaper and slower); `mode: speed` (default) when generation time matters; `mode: quality` for the slower, higher-fidelity recipe.
- `prompt_upsampler`: `off` when copy is already locked; `turbo` (default); `max` when the source prompt is short and the scene needs more described detail. Compare `off` vs `turbo` vs `max` on the **same `seed`** before scaling.
- Defaults: `resolution: 768p`, `aspect_ratio: 16:9`, 24 fps, generated audio.

## Iterate (`p-video-2-pro`)

There is no `draft` flag. Iterate in `mode: cost` (same quality as `speed`, but cheaper and slower) or `mode: speed` (faster); then final with `mode: quality` when fidelity matters. Do not send `audio`, `fps`, `save_audio`, or `prompt_upsampling`.

For `p-video-2-pro-reference`, iterate and finish with `cost` or `speed`; there is no `quality` mode. Output carries generated audio unless `keep_audio` keeps the single uploaded track.
