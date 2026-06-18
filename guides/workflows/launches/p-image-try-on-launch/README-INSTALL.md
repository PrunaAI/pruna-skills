# p-image-try-on-launch

## Install (portable bundle)

From a clone of this repository:

```bash
./scripts/install_skill.sh p-image-try-on-launch
# or: ./scripts/install_skill.sh p-image-try-on-launch --target ~/.cursor/skills
```

Restart Cursor or start a new chat.

## Dependencies

```bash
pip install -r scripts/requirements.txt   # inside installed skill, or repo skill path
# ffmpeg + ffprobe must be on PATH
export PRUNA_API_KEY=your_key
# narration overlay + background bed:
export REPLICATE_API_TOKEN=r8_...
```

## Run (portable)

Default is **Phase A stills only** — review person, garment, and try-on images before video jobs.

```bash
python3 ./scripts/run_from_plan.py \
  --plan ./templates/scene-plan.template.json \
  --out-dir ./output/my-try-on-launch \
  --phase stills

python3 ./scripts/run_from_plan.py \
  --plan ./output/my-try-on-launch/plan.json \
  --out-dir ./output/my-try-on-launch \
  --approve-stills \
  --phase video

# Optional narration for i2v / slider rows:
python3 ./scripts/run_from_plan.py \
  --plan ./output/my-try-on-launch/plan.json \
  --out-dir ./output/my-try-on-launch \
  --approve-stills --phase tts

# Concat + instrumental bed:
python3 ./scripts/run_from_plan.py \
  --plan ./output/my-try-on-launch/plan.json \
  --out-dir ./output/my-try-on-launch \
  --approve-audio --phase assemble --background-music
```

Set `"background_music": { "enabled": true, ... }` in the plan. Tool: [stable-audio-2.5](../../../tools/audio/stable-audio-2.5/SKILL.md).

Curl-first alternative: `templates/curl-phase-a.template.sh` and `templates/curl-phase-b.template.sh`.

## Expected path after install

```text
~/.cursor/skills/p-image-try-on-launch/
├── SKILL.md
├── try-on-beats.md
├── scripts/run_from_plan.py
├── references/
└── templates/
```
