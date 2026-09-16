# p-video-2 prompting

Prompt craft unique to `p-video-2` (quality-focused successor to `p-video`). Shared dramaturgy, camera, and physics: [prompt-dramaturgy.md](./prompt-dramaturgy.md), [camera-lighting-vocabulary.md](./camera-lighting-vocabulary.md), [physics-safe-motion.md](./physics-safe-motion.md). Frame payloads: [scene-anchor-pair.md](./scene-anchor-pair.md) / [scene-anchor-triple.md](./scene-anchor-triple.md). QA: [p-video-2-quality-checklist.md](./p-video-2-quality-checklist.md).

**1080p / imported-audio path.** Use `p-video-2` when the brief needs 1080p, a mixed track, or draft previews. Use `p-video-2-pro` for cinematic generation with generated audio. Use `p-video` for simpler, quicker clips.

## Strengths to write toward

- Sharper subjects, backgrounds, and motion than `p-video` — especially **close-ups and foreground objects**
- Stronger **lip-sync on native speech** — T2V with `save_audio: true` and **no imported `audio`**: the model pauses, delivers the line, then rests, and the mouth follows. **Lead dialogue / lip-sync jobs here**
- **Native audio** in the output (`save_audio` defaults true). Imported `audio` still works and keeps a **cleaner face / identity**; viseme lock vs `p-video` is mixed — do not lead lip-sync demos with a muxed wav
- Stronger **identity / input-image consistency**
- One endpoint: T2V + I2V + audio-conditioned

## Limits (do not fight them)

- Not designed for **extreme cinematic camera** (crash zooms, whip pans, chaotic handheld)
- Complex **multi-scene storytelling** in one clip is weaker — split beats
- Native **4K** is not supported
- **More than two speakers** — speaker separation degrades
- **SFX-led** clips (the ask is sound effects, not picture + optional bed) are currently limited

## Mode recipes (rewrite for the brief — do not paste)

**Text-to-video** — subject + motion + camera + lighting + audio intent in one coherent line.

```text
A sports car drifting through a neon-lit city at night, cinematic aerial shot, wet asphalt reflections, engine roar and tire screech.
```

**Image-to-video** — keep motion **subtle** and aligned with the reference frame. Prefer a **stable** camera.

```text
The camera slowly pushes in. The person turns their head and smiles naturally. Soft studio lighting, shallow depth of field.
```

**Native speech (T2V, no `audio`)** — write the spoken line into the prompt. This is the lip-sync path.

```text
A woman faces the camera and says "I'll be there in five." She pauses, delivers the line, then rests. Natural mouth motion, soft window light, camera holds steady.
```

**Audio-conditioned** — name the performer and hold. One or two faces max. Use for singing / VO length, not as the primary lip-sync demo.

```text
Close-up of a singer performing the uploaded track. Natural lip-sync, expressive face, stage lighting, camera holds steady on the performer.
```

## Duration

- Set `duration` (1–20s) when the user locked a length.
- **Leave `duration` empty** to let the model choose length from the prompt.
- When `audio` is set, omit `duration` — length follows the audio (cap **20s**; TTS ≤ ~19s).

## Iterate

Use `draft: true` for cheap previews, then `draft: false` for the paid final. Defaults: `prompt_upsampling: true`, `save_audio: true`, `resolution: 720p`, `fps: 24`, `aspect_ratio: 16:9`.
