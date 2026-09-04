# p-video-2 prompting

Prompt craft unique to `p-video-2` (quality-focused successor to `p-video`). Shared dramaturgy, camera, and physics: [prompt-dramaturgy.md](./prompt-dramaturgy.md), [camera-lighting-vocabulary.md](./camera-lighting-vocabulary.md), [physics-safe-motion.md](./physics-safe-motion.md). Frame payloads: [scene-anchor-pair.md](./scene-anchor-pair.md) / [scene-anchor-triple.md](./scene-anchor-triple.md). QA: [p-video-2-quality-checklist.md](./p-video-2-quality-checklist.md).

**Quality path.** Use `p-video-2` when the brief needs the best output. Use `p-video` for simpler, quicker clips.

## Strengths to write toward

- Sharper subjects, backgrounds, and motion than `p-video`
- Stronger **lip-sync** on dialogue and audio-conditioned singing
- **Native audio** in the output (`save_audio` defaults true) — import a track or let the model generate sound
- Strong **input-image consistency**; particularly good on **close-ups and foreground objects**
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

**Audio-conditioned** — name the performer, lip-sync, and hold. One or two faces max.

```text
Close-up of a singer performing the uploaded track. Natural lip-sync, expressive face, stage lighting, camera holds steady on the performer.
```

## Duration

- Set `duration` (1–20s) when the user locked a length.
- **Leave `duration` empty** to let the model choose length from the prompt.
- When `audio` is set, omit `duration` — length follows the audio (cap **20s**; TTS ≤ ~19s).

## Iterate

Use `draft: true` for cheap previews, then `draft: false` for the paid final. Defaults: `prompt_upsampling: true`, `save_audio: true`, `resolution: 720p`, `fps: 24`, `aspect_ratio: 16:9`.
