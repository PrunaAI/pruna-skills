# p-video-animate-comparison

## Install (portable bundle)

```bash
./scripts/install_skill.sh p-video-animate-comparison
```

Restart Cursor or start a new chat.

## Dependencies

```bash
pip install -r scripts/requirements.txt
export PRUNA_API_KEY=your_key
# ffmpeg on PATH for slider renders
```

## Run

```bash
python3 ./scripts/run_from_plan.py --plan ./templates/config.template.json --out-dir ./output/my-animate-reel --phase stills
python3 ./scripts/run_from_plan.py --approve-stills --phase video --plan ... --out-dir ...
```

See [multi-scene-avatar-video](../multi-scene-avatar-video/SKILL.md) for the canonical mixed workflow.
