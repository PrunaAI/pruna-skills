# Generation quality checklist hub

Use this as the shared quality gate across models and workflows.
Run the **Core checklist** for every generation job, then run the model-specific checklist.

Maintenance rule: keep tool/guide mapping only in this file to avoid link drift.

## Match map (tool -> checklist -> guides)

| Tool/model | Checklist | Common guides |
|------------|-----------|---------------|
| `p-image` | [`p-image-quality-checklist.md`](./p-image-quality-checklist.md) | [`single-scene-ai-video`](../guides/workflows/single-scene-ai-video/SKILL.md), [`multi-scene-ai-video`](../guides/workflows/multi-scene-ai-video/SKILL.md), [`pruna-generative-pipeline`](../guides/workflows/pruna-generative-pipeline/SKILL.md) |
| `p-image-edit` | [`p-image-edit-quality-checklist.md`](./p-image-edit-quality-checklist.md) | [`single-scene-avatar-video`](../guides/workflows/single-scene-avatar-video/SKILL.md), [`multi-scene-avatar-video`](../guides/workflows/multi-scene-avatar-video/SKILL.md), [`pruna-generative-pipeline`](../guides/workflows/pruna-generative-pipeline/SKILL.md) |
| `p-image-upscale` | [`p-image-upscale-quality-checklist.md`](./p-image-upscale-quality-checklist.md) | [`single-scene-ai-video`](../guides/workflows/single-scene-ai-video/SKILL.md), [`multi-scene-ai-video`](../guides/workflows/multi-scene-ai-video/SKILL.md), [`pruna-generative-pipeline`](../guides/workflows/pruna-generative-pipeline/SKILL.md) |
| `p-video` | [`p-video-quality-checklist.md`](./p-video-quality-checklist.md) | [`single-scene-ai-video`](../guides/workflows/single-scene-ai-video/SKILL.md), [`multi-scene-ai-video`](../guides/workflows/multi-scene-ai-video/SKILL.md), [`pruna-generative-pipeline`](../guides/workflows/pruna-generative-pipeline/SKILL.md) |
| `p-video-avatar` | [`p-video-avatar-quality-checklist.md`](./p-video-avatar-quality-checklist.md) | [`single-scene-avatar-video`](../guides/workflows/single-scene-avatar-video/SKILL.md), [`multi-scene-avatar-video`](../guides/workflows/multi-scene-avatar-video/SKILL.md), [`pruna-generative-pipeline`](../guides/workflows/pruna-generative-pipeline/SKILL.md) |

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

## Workflow note

For multi-scene projects, run these checks per scene and add a final continuity pass
(style, character identity, voice, and pacing consistency across scenes).
