# Generation quality checklist hub

Use this as the shared quality gate across models and workflows.
Run the **Core checklist** for every generation job, then run the model-specific checklist.

Maintenance rule: keep tool/guide mapping only in this file to avoid link drift.

## Match map (tool -> checklist -> guides)

| Tool/model | Checklist | Common guides |
|------------|-----------|---------------|
| `p-image` | [`p-image-quality-checklist.md`](./p-image-quality-checklist.md) | [`single-scene-ai-video`](../guides/workflows/single-scene-ai-video/SKILL.md), [`multi-scene-ai-video`](../guides/workflows/multi-scene-ai-video/SKILL.md), [`pruna-generative-pipeline`](../guides/workflows/pruna-generative-pipeline/SKILL.md) |
| `p-image-edit` | [`p-image-edit-quality-checklist.md`](./p-image-edit-quality-checklist.md) | [`single-scene-avatar-video`](../guides/workflows/single-scene-avatar-video/SKILL.md), [`multi-scene-avatar-video`](../guides/workflows/multi-scene-avatar-video/SKILL.md), [`pruna-generative-pipeline`](../guides/workflows/pruna-generative-pipeline/SKILL.md) |
| `p-image-upscale` | [`p-image-upscale-quality-checklist.md`](./p-image-upscale-quality-checklist.md) | [`single-scene-ai-video`](../guides/workflows/single-scene-ai-video/SKILL.md), [`multi-scene-ai-video`](../guides/workflows/multi-scene-ai-video/SKILL.md), [`pruna-generative-pipeline`](../guides/workflows/pruna-generative-pipeline/SKILL.md), [`p-image-upscale-comparison`](../guides/workflows/p-image-upscale-comparison/SKILL.md) |
| `p-video` | [`p-video-quality-checklist.md`](./p-video-quality-checklist.md) | [`single-scene-ai-video`](../guides/workflows/single-scene-ai-video/SKILL.md), [`multi-scene-ai-video`](../guides/workflows/multi-scene-ai-video/SKILL.md), [`pruna-generative-pipeline`](../guides/workflows/pruna-generative-pipeline/SKILL.md) |
| `p-video-avatar` | [`p-video-avatar-quality-checklist.md`](./p-video-avatar-quality-checklist.md) | [`single-scene-avatar-video`](../guides/workflows/single-scene-avatar-video/SKILL.md), [`multi-scene-avatar-video`](../guides/workflows/multi-scene-avatar-video/SKILL.md), [`pruna-generative-pipeline`](../guides/workflows/pruna-generative-pipeline/SKILL.md) |
| `p-video-animate` | [`p-video-animate-quality-checklist.md`](./p-video-animate-quality-checklist.md) | [`multi-scene-avatar-video`](../guides/workflows/multi-scene-avatar-video/SKILL.md), [`pruna-generative-pipeline`](../guides/workflows/pruna-generative-pipeline/SKILL.md) |
| `p-video-replace` | [`p-video-replace-quality-checklist.md`](./p-video-replace-quality-checklist.md) | [`p-video-replace`](../tools/video/p-video-replace/SKILL.md), [`p-video-replace-comparison`](../guides/workflows/p-video-replace-comparison/SKILL.md) |
| `music-2.5` + music video assembly | [`music-video-quality-checklist.md`](./music-video-quality-checklist.md) | [`ai-music-video`](../guides/workflows/ai-music-video/SKILL.md), [`music-2.5`](../tools/audio/music-2.5/SKILL.md) |

## Core checklist (all models)

- Goal and acceptance criteria are explicit (what "good" looks like is written down).
- Input assets are valid and licensed (URL/file reachable, rights cleared).
- Prompt and settings match the intended output format (`aspect_ratio`, duration, resolution, style lock).
- Output contains no accidental watermarks, UI overlays, or stray text unless requested.
- Brand, legal, and safety constraints are satisfied before handoff.
- Manifest/log captures model, input fields, prediction id, and output URL for reproducibility.

## Model-specific checklists

- [`p-image-quality-checklist.md`](./p-image-quality-checklist.md)
- [`p-image-edit-quality-checklist.md`](./p-image-edit-quality-checklist.md)
- [`p-image-upscale-quality-checklist.md`](./p-image-upscale-quality-checklist.md)
- [`p-video-quality-checklist.md`](./p-video-quality-checklist.md)
- [`p-video-avatar-quality-checklist.md`](./p-video-avatar-quality-checklist.md)
- [`p-video-animate-quality-checklist.md`](./p-video-animate-quality-checklist.md)
- [`p-video-replace-quality-checklist.md`](./p-video-replace-quality-checklist.md)
- [`music-video-quality-checklist.md`](./music-video-quality-checklist.md)

## Visual variety (showcase reels)

Before generation on comparison or launch reels, run [visual-variety-bible.md](./visual-variety-bible.md) **Variety checklist** — cast diversity, distinct backgrounds, camera angles, lighting, and style tags.

For phased human review before expensive video jobs, see [staged-generation-gate.md](./staged-generation-gate.md).

## Workflow note

For multi-scene projects, run these checks per scene and add a final continuity pass
(style, character identity, voice, and pacing consistency across scenes).

**Narrated cinematic B-roll:** validate [scene anchor triple](./scene-anchor-triple.md) inputs before `p-video` — start still, end still, uploaded narration URL per row.
