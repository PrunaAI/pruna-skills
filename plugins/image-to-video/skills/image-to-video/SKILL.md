---
name: image-to-video
description: Use when the user needs one video clip from stills, a single narrated story beat, one B-roll shot, or one scene—not a full multi-scene film or talking-head-only piece.
license: MIT
metadata:
  version: "1.0.2"
depends:
  - p-image
  - p-image-edit
  - p-video
  - gemini-3.1-flash-tts
  - stable-audio-2.5
---

# Single-scene AI video (Pruna `p-video`)

One **`p-video`** prediction. See [p-video](../../../../tools/video/p-video/SKILL.md), [scene-anchor-triple.md](./references/scene-anchor-triple.md), and [pruna-api.md](./references/pruna-api.md).

## Skill boundary

Exactly **one scene / one `p-video` job**. No subagents, no concat across scenes, no multi-scene manifest ownership.

If the user wants a multi-scene film → hand off to [narrated-multi-scene](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/narrated-multi-scene/skills/narrated-multi-scene/SKILL.md) or [visual-transition-reel](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/visual-transition-reel/skills/visual-transition-reel/SKILL.md). Talking-head-only → [avatar-single-scene](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/avatar-single-scene/skills/avatar-single-scene/SKILL.md).

**Data handling:** [agent-safety.md](./references/agent-safety.md) before any upload or paid call.

**Staged generation:** [staged-generation-gate.md](./references/staged-generation-gate.md) · [workflow-feedback-gates.md](./references/workflow-feedback-gates.md)

## Feedback gates (required)

| Phase | What to show | Proceed when |
|-------|--------------|--------------|
| **0 — Plan** | Mode, motion prompt, frame plan | **approve plan** |
| **A — Stills** | Start + end stills | **approve stills** |
| **A2 — TTS** | Narration MP3 (triple mode) — listen | Line OK |
| **B — Video** | `p-video` clip | User accepts |
| **D — Bed** | Optional post-mux bed | User accepts |

## Intake: ask before generating

**Do not** call `POST /v1/predictions` until these are answered and logged:

| Topic | Questions |
|-------|-----------|
| **Mode** | **`triple`** (`image` + `last_frame_image` + `audio` — preferred for narrated beats) · **`pair`** (start + end still + `duration`) · T2V · I2V · I2V+last · audio-only (no frames) |
| **Creative** | Motion `prompt` only — what happens between first and last frame? One paragraph max. |
| **Frames** | Start still (upload or `p-image-edit`)? End still (`last_frame_edit_prompt`)? Stay single-scene — if the user wants a longer **`frame_chain` / multi-scene** project, stop and switch to [narrated-multi-scene](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/narrated-multi-scene/skills/narrated-multi-scene/SKILL.md) or [visual-transition-reel](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/visual-transition-reel/skills/visual-transition-reel/SKILL.md). |
| **Audio** | [Gemini TTS](../../../../tools/audio/gemini-3.1-flash-tts/SKILL.md) → upload → **`input.audio`** (preferred). Optional [Stable Audio](../../../../tools/audio/stable-audio-2.5/SKILL.md) bed **after** render. Post-mux is fallback only — [audio-post-production.md](https://github.com/PrunaAI/pruna-skills/tree/main/references/shared/audio-post-production.md). |
| **Format** | Default **`720p`**, **`24` fps**; `duration` only when **no** `audio`; override `resolution` / `fps` / `aspect_ratio` when user wants final delivery |
| **Draft** | `draft: true` for preview or `false` for final? |
| **Repro** | Fixed `seed`? |
| **Delivery** | Async (production); `Try-Sync: true` only for quick tests |

## Workflow (after intake)

### Preferred — scene anchor triple

1. **Start still** — upload or **`p-image`** / **`p-image-edit`**
2. **End still** — **`p-image-edit`** from start still + `last_frame_edit_prompt`
3. **Narration** — [Gemini TTS](../../../../tools/audio/gemini-3.1-flash-tts/SKILL.md) → probe MP3 (**≤ ~19s**) → upload to `/v1/files`
4. **`p-video`** — `image` + `last_frame_image` + **`audio`** + motion `prompt`; omit `duration`; `save_audio: true`; async poll
5. **Optional bed** — mix under embedded narration in post

Full spec: [scene-anchor-triple.md](./references/scene-anchor-triple.md).

### Other modes

- **I2V only:** `image` + `duration` + `prompt`
- **I2V + last:** add `last_frame_image`
- **T2V:** `prompt` + `duration` + `aspect_ratio`

## Related

- Multi-scene triple + frame chain: [narrated-multi-scene](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/narrated-multi-scene/skills/narrated-multi-scene/SKILL.md)
- Multi-scene visual transitions (pair, no VO): [visual-transition-reel](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/visual-transition-reel/skills/visual-transition-reel/SKILL.md)
- Talking head: [avatar-single-scene](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/avatar-single-scene/skills/avatar-single-scene/SKILL.md)
- Pipeline hub: [pruna-generative-pipeline](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/pruna-generative-pipeline/skills/pruna-generative-pipeline/SKILL.md)
