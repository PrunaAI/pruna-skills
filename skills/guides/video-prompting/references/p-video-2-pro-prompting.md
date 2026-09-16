# p-video-2-pro prompting

Prompt craft unique to `p-video-2-pro` (cinematic generation lane next to `p-video-2`). Shared dramaturgy, camera, and physics: [prompt-dramaturgy.md](./prompt-dramaturgy.md), [camera-lighting-vocabulary.md](./camera-lighting-vocabulary.md), [physics-safe-motion.md](./physics-safe-motion.md). Visual frame payloads: [scene-anchor-pair.md](./scene-anchor-pair.md). QA: [p-video-2-pro-quality-checklist.md](./p-video-2-pro-quality-checklist.md). Uploaded audio triples stay on `p-video-2` — [scene-anchor-triple.md](./scene-anchor-triple.md).

**Cinematic generation.** Use `p-video-2-pro` for text-to-video or first/last-frame clips with **generated audio**. Use `p-video-2` for **1080p**, **imported audio**, or **draft** previews. Use `p-video` for cheaper, faster drafts.

## Strengths to write toward

- **Multi-beat cinematic blocking** in one clip (product unfold, dialogue, chase, weather) — 8s is a typical locked-in length
- **Heavier physics:** water, snow spray, fire, fabric, hair
- **Full-body anatomy** that stays coherent through fast motion
- **Two-shot dialogue** with lip-sync — write the spoken line into the prompt
- **First + last frame** as a first-class control
- **Three-level prompt upsampler** (`off` / `turbo` / `max`), independent of `mode`
- `mode: speed` vs `mode: quality` on the same prompt
- **Generated audio** already in the clip — write score, ambience, SFX, or dialogue in the prompt

## Limits (do not fight them)

- **No audio import** — muxed VO / music belongs on `p-video-2`
- Max **768p** and **15s** — not 1080p / 20s / 48 fps
- **No draft mode** — `mode: speed` is the fast recipe; `quality` is slower
- Not an editor (`p-video-edit`) or talking-head avatar (`p-video-avatar`)
- Native **4K** is not supported
- **More than two speakers** — speaker separation degrades

## Fast pass vs locked-in

**Fast pass** — subject + action + scene. Enough for first looks. Iterate in `mode: speed`.

```text
A matte stainless pour-over kettle sits on a seamless light-gray studio sweep. Thin steam rises from the spout.
```

**Locked-in** — add camera, lighting, style, and audio. Optional first-frame or last-frame still for repeatable runs.

```text
A narrative film scene, 1970s Roman trattoria at night, warm tungsten, cigarette haze, Super-8 grain. A man and a woman in period clothes sit at a small table with wine. She leans in and quietly says, "Then we leave before sunrise." The camera slowly dollies around the table. Audio: Italian radio pop from a small speaker, plates, low room tone, her line clear and close.
```

## Mode recipes (rewrite for the brief — do not paste)

**Text-to-video** — subject + action + camera + lighting + audio intent in one coherent line.

```text
A dramatic cinematic shot of an isolated lighthouse standing on a rocky cliff during an enormous Atlantic storm at dusk. The camera begins close to the lighthouse keeper standing outside near the railing as violent wind pulls at his coat. He turns toward the ocean just as a massive wave crashes against the cliff and sends water high above the lighthouse. The camera rapidly pulls back to reveal the scale of the storm. Photorealistic water physics, heavy rain, turbulent clouds, realistic human movement, and epic scale.
```

**Image-to-video (first frame)** — keep motion aligned with the reference frame.

```text
The camera slowly pushes in. The person turns their head and smiles naturally. Soft studio lighting, shallow depth of field.
```

**First + last frame** — motion consistent with both stills; end exactly on the last-frame composition.

```text
Start on the still product hero. The camera holds, then a slow push-in as light moves across the metal. End exactly on the last-frame packshot, label readable, no extra props.
```

**Native speech (T2V)** — write the spoken line into the prompt. There is no `audio` field.

```text
A woman faces the camera and says "I'll be there in five." She pauses, delivers the line, then rests. Natural mouth motion, soft window light, camera holds steady.
```

## Duration, mode, upsampler

- Set `duration` (5–15s; default **5**). Partner demos often use **8s** for locked-in cinematic beats.
- `mode: speed` (default) for iteration; `mode: quality` for the slower, higher-fidelity recipe.
- `prompt_upsampler`: `off` when copy is already locked; `turbo` (default); `max` when the source prompt is short and the scene needs more described detail. Compare `off` vs `turbo` vs `max` on the **same `seed`** before scaling.
- Defaults: `resolution: 768p`, `aspect_ratio: 16:9`, 24 fps, generated audio.

## Iterate

There is no `draft` flag. Iterate in `mode: speed`, then final with `mode: quality` when fidelity matters. Do not send `audio`, `fps`, `save_audio`, or `prompt_upsampling`.
