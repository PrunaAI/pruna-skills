# illustrated-story-reel

Still-image story reels — **p-image** / **p-image-edit** beats + Ken Burns ffmpeg assembly. Narration or music (no **p-video**).

## Install

```bash
./scripts/install_skill.sh illustrated-story-reel
```

## Run

```bash
cp guides/workflows/verticals/illustrated-story-reel/templates/story-plan.template.json \
  output/verticals/illustrated-story-reel/my-story/plan.json
python3 guides/workflows/verticals/illustrated-story-reel/scripts/run_from_plan.py \
  --plan output/verticals/illustrated-story-reel/my-story/plan.json \
  --out-dir output/verticals/illustrated-story-reel/my-story/ \
  --phase stills
```

Set `audio_mode` to `"narration"` or `"music"` in the plan before running audio phases.
