# multi-scene-ai-video

Narrated multi-scene films use the [scene anchor triple](../../../../references/video/scene-anchor-triple.md): **`image`** + **`last_frame_image`** + **`audio`** per `p-video` scene.

## Install

From a clone of this repository:

```bash
mkdir -p ~/.cursor/skills
cp -R /path/to/pruna-ai-content-generation-skills/catalog/workflows/core/narrated-multi-scene ~/.cursor/skills/
```

Or install the whole repository with `npx skills add` (see repository root `README.md`). Restart Cursor or start a new chat.

## Expected path

```text
~/.cursor/skills/multi-scene-ai-video/SKILL.md
```
