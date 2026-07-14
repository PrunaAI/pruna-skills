# visual-transition-reel

Smooth multi-scene reels use the [scene anchor pair](../../../../references/video/scene-anchor-pair.md): **`image`** + **`last_frame_image`** + transition **`prompt`** + **`duration`** per `p-video` scene. Stills from **`p-image`** hero + **`p-image-edit`**.

Legacy install name: `scene-transition-video` (same bundle).

## Install

```bash
npx skills add PrunaAI/pruna-ai-content-generation-skills/skills --skill visual-transition-reel --agent cursor -y
```

Or copy manually:

```bash
mkdir -p ~/.cursor/skills
cp -R /path/to/pruna-ai-content-generation-skills/catalog/workflows/core/visual-transition-reel ~/.cursor/skills/
```

## Expected path

```text
~/.cursor/skills/visual-transition-reel/SKILL.md
```

## Run

```bash
cp catalog/workflows/core/visual-transition-reel/templates/transition-plan.template.json \
  output/core/visual-transition-reel/my-reel/plan.json
python3 catalog/workflows/core/visual-transition-reel/scripts/run_from_plan.py \
  --plan output/core/visual-transition-reel/my-reel/plan.json \
  --out-dir output/core/visual-transition-reel/my-reel
```
