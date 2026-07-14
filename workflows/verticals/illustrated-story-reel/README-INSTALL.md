# illustrated-story-reel

Still-image stories — **p-image** / **p-image-edit** beats + Ken Burns ffmpeg assembly. Vertical (**9:16**), horizontal (**16:9**), or square (**1:1**) via `defaults.aspect_ratio` in the plan. Narration or music (no **p-video**).

## Install

```bash
npx skills add PrunaAI/pruna-ai-content-generation-skills/skills --skill illustrated-story-reel --agent cursor -y
```

## Run

```bash
cp catalog/workflows/verticals/illustrated-story-reel/templates/story-plan.template.json \
  output/verticals/illustrated-story-reel/my-story/plan.json
python3 catalog/workflows/verticals/illustrated-story-reel/scripts/run_from_plan.py \
  --plan output/verticals/illustrated-story-reel/my-story/plan.json \
  --out-dir output/verticals/illustrated-story-reel/my-story/ \
  --phase stills
```

Set `audio_mode` to `"narration"` or `"music"` in the plan before running audio phases.
