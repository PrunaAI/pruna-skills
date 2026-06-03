# interactive-explainer

Educational shorts (history, science, nature, how-it-works, children's) with **narrator + character interaction** — not pure voice-over.

Spec: [educational-explainer-scenes.md](../../../../references/workflows/interactive-explainer-scenes.md)

## Install

```bash
mkdir -p ~/.cursor/skills
cp -R /path/to/pruna-ai-content-generation-skills/guides/workflows/verticals/interactive-explainer ~/.cursor/skills/
```

## Run

```bash
cp guides/workflows/verticals/interactive-explainer/templates/explainer-plan.template.json \
  output/verticals/interactive-explainer/my-explainer/plan.json
python3 guides/workflows/verticals/interactive-explainer/scripts/run_from_plan.py \
  --plan output/verticals/interactive-explainer/my-explainer/plan.json \
  --out-dir output/verticals/interactive-explainer/my-explainer \
  --final-name my_explainer_final.mp4
```
