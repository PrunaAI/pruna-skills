# illustrated-story-reel

Still-image stories — **p-image** / **p-image-edit** beats + Ken Burns ffmpeg assembly. Vertical (**9:16**), horizontal (**16:9**), or square (**1:1**) via `defaults.aspect_ratio` in the plan. Narration or music (no **p-video**).

## Requirements

| Requirement | Purpose |
|-------------|---------|
| `PRUNA_API_KEY` | Hero + beat stills (`p-image`, `p-image-edit`) |
| `REPLICATE_API_TOKEN` | Gemini TTS and/or Stable Audio bed |
| `ffmpeg`, `ffprobe` | Ken Burns segments and final mux |
| `python3` + `pip install -r scripts/requirements.txt` | Runner scripts |

**Scope:** This skill does not call `p-video*`. Install only if you accept paid image/audio APIs, local ffmpeg execution, and media written under your output directory. See `skill.manifest.json` `permissions` and SKILL.md **Security & scope**.

## Install

```bash
npx skills add PrunaAI/pruna-skills/plugins/illustrated-story-reel/skills --skill illustrated-story-reel --agent cursor -y
```

## Run

```bash
cp workflows/verticals/illustrated-story-reel/templates/story-plan.template.json \
  output/verticals/illustrated-story-reel/my-story/plan.json
python3 workflows/verticals/illustrated-story-reel/scripts/run_from_plan.py \
  --plan output/verticals/illustrated-story-reel/my-story/plan.json \
  --out-dir output/verticals/illustrated-story-reel/my-story/ \
  --phase stills
```

Set `audio_mode` to `"narration"` or `"music"` in the plan before running audio phases.
