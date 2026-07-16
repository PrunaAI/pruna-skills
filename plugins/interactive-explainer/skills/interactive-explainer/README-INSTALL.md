# visual-transition-reel

Visual montages and motion between stills — narration optional.

Spec: [interactive-explainer-scenes.md](./references/interactive-explainer-scenes.md) (scene patterns) · [staged-generation-gate.md](./references/staged-generation-gate.md)

## Install

```bash
mkdir -p ~/.cursor/skills
cp -R /path/to/pruna-skills/workflows/verticals/interactive-explainer ~/.cursor/skills/
```

## Run

```bash
cp workflows/verticals/interactive-explainer/templates/explainer-plan.template.json \
  output/verticals/interactive-explainer/my-explainer/plan.json
python3 workflows/verticals/interactive-explainer/scripts/run_from_plan.py \
  --plan output/verticals/interactive-explainer/my-explainer/plan.json \
  --out-dir output/verticals/interactive-explainer/my-explainer \
  --final-name my_explainer_final.mp4
```
