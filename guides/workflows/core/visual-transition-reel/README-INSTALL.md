# scene-transition-video

Smooth multi-scene reels use the [scene anchor pair](../../../../references/video/scene-anchor-pair.md): **`image`** + **`last_frame_image`** + transition **`prompt`** + **`duration`** per `p-video` scene. Stills from **`p-image`** hero + **`p-image-edit`**.

## Install

From a clone of this repository:

```bash
mkdir -p ~/.cursor/skills
cp -R /path/to/pruna-ai-content-generation-skills/guides/workflows/core/visual-transition-reel ~/.cursor/skills/
```

Or install the whole repository with `npx skills add` (see repository root `README.md`). Restart Cursor or start a new chat.

## Expected path

```text
~/.cursor/skills/scene-transition-video/SKILL.md
```

## Run

```bash
cp guides/workflows/core/visual-transition-reel/templates/transition-plan.template.json \
  output/core/visual-transition-reel/my-reel/plan.json
python3 guides/workflows/core/visual-transition-reel/scripts/run_from_plan.py \
  --plan output/core/visual-transition-reel/my-reel/plan.json \
  --out-dir output/core/visual-transition-reel/my-reel
```
