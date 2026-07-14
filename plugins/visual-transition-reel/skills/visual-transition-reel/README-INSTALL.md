# visual-transition-reel

Smooth multi-scene reels use the [scene anchor pair](./references/scene-anchor-pair.md): **`image`** + **`last_frame_image`** + transition **`prompt`** + **`duration`** per `p-video` scene. Stills from **`p-image`** hero + **`p-image-edit`**.

## Install

```bash
npx skills add PrunaAI/pruna-skills/plugins/visual-transition-reel/skills --skill visual-transition-reel --agent cursor -y
```

Or copy manually:

```bash
mkdir -p ~/.cursor/skills
cp -R /path/to/pruna-skills/workflows/core/visual-transition-reel ~/.cursor/skills/
```

## Expected path

```text
~/.cursor/skills/visual-transition-reel/SKILL.md
```

## Run

```bash
cp workflows/core/visual-transition-reel/templates/transition-plan.template.json \
  output/core/visual-transition-reel/my-reel/plan.json
python3 workflows/core/visual-transition-reel/scripts/run_from_plan.py \
  --plan output/core/visual-transition-reel/my-reel/plan.json \
  --out-dir output/core/visual-transition-reel/my-reel
```
