# Pruna models (index)

Pricing and limits change; confirm on the official page: [Available models](https://docs.api.pruna.ai/guides/models).

**Execution:** Multi-scene and batch runs should use **async parallel fan-out** and **subagents per independent lane** — see [parallel-execution.md](./parallel-execution.md).

## First-party Pruna models covered by this repo

| Model ID | Type | Skill folder | QA checklist |
|----------|------|----------------|--------------|
| `p-image` | Text-to-image | `tools/image/p-image` | `references/p-image-quality-checklist.md` |
| `p-image-edit` | Image edit / compose (1–5 images) | `tools/image/p-image-edit` | `references/p-image-edit-quality-checklist.md` |
| `p-image-upscale` | Upscale (target MP 1–128, optional enhance) | `tools/image/p-image-upscale` | `references/p-image-upscale-quality-checklist.md` |
| `p-video` | Text / image / audio video | `tools/video/p-video` | `references/p-video-quality-checklist.md` |
| `p-video-avatar` | Talking avatar from portrait + script or audio | `tools/video/p-video-avatar` | `references/p-video-avatar-quality-checklist.md` |
| `p-video-animate` | Animate a still using source video motion (motion transfer) | `tools/video/p-video-animate` | `references/p-video-animate-quality-checklist.md` |
| `p-video-replace` | Replace people in source video using 1–4 identity images | `tools/video/p-video-replace` | `references/p-video-replace-quality-checklist.md` |

## External tools (Replicate)

| Tool | Type | Skill folder | Notes |
|------|------|--------------|-------|
| `stable-audio-2.5` | Text-to-music bed | `tools/audio/stable-audio-2.5` | Requires `REPLICATE_API_TOKEN`; mix via `launch_background_music.py` |
| `music-2.5` | Full song with vocals (lyrics + style) | `tools/audio/music-2.5` | Requires `REPLICATE_API_TOKEN`; [ai-music-video](../guides/workflows/ai-music-video/SKILL.md) workflow |

## Related models (not duplicated as skills here)

Documented on the same models page: `p-image-lora`, trainers, `flux-*`, `wan-*`, `qwen-*`, `vace`, etc. Add a new `tools/.../<name>/SKILL.md` when you need agent guidance for another model.

## Composed workflows in this repo

| Workflow | Path |
|----------|------|
| Prompt-first fast entrypoint (auto route + direct chains) | `guides/workflows/pruna-run` |
| Pruna generative **scenario hub** (mood boards, packs, I2V, audio-led `p-video`, upscale chains; points to scene workflows) | `guides/workflows/pruna-generative-pipeline` |
| Single-scene avatar (`p-video-avatar`, intake first) | `guides/workflows/single-scene-avatar-video` |
| Multi-scene avatar (stills + `p-video-avatar` per scene, intake first) | `guides/workflows/multi-scene-avatar-video` |
| Single-scene cinematic (`p-video`, intake first) | `guides/workflows/single-scene-ai-video` |
| Multi-scene cinematic (`p-video` per scene, intake first) | `guides/workflows/multi-scene-ai-video` |
| Motion-transfer showcase (`p-video-animate` + slider comparisons) | `guides/workflows/multi-scene-avatar-video` (animate rows) |
| In-video replacement showcase (`p-video-replace` + slider comparisons) | `guides/workflows/p-video-replace-comparison` |
| AI music video (lyrics → Music 2.5 → avatar + B-roll) | `guides/workflows/ai-music-video` |
| Route I: UGC ad factory | `guides/workflows/ugc-ad-factory` |
| Route J: Product-to-story reel builder | `guides/workflows/product-to-story-reel-builder` |
| Route K: Ecommerce creative pack generator | `guides/workflows/ecommerce-creative-pack-generator` |
| Route L: Character IP content engine | `guides/workflows/character-ip-content-engine` |
