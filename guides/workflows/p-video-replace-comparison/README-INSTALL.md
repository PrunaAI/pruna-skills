# p-video-replace-comparison

## Install (portable bundle)

From a clone of this repository:

```bash
./scripts/install_skill.sh p-video-replace-comparison
# or: ./scripts/install_skill.sh p-video-replace-comparison --target ~/.cursor/skills
```

Restart Cursor or start a new chat.

## Dependencies

```bash
pip install -r scripts/requirements.txt   # inside installed skill, or repo skill path
# ffmpeg must be on PATH
export PRUNA_API_KEY=your_key
# optional — chill background bed after concat:
export REPLICATE_API_TOKEN=r8_...
```

## Run (portable)

Default is **Phase A stills only** — review images before video jobs.

```bash
python3 ./scripts/run_from_plan.py \
  --plan ./templates/scene-plan.template.json \
  --out-dir ./output/my-replace-reel \
  --phase stills

python3 ./scripts/run_from_plan.py \
  --plan ./output/my-replace-reel/plan.json \
  --out-dir ./output/my-replace-reel \
  --approve-stills \
  --phase video

# After slider MP4s exist — concat + optional chill bed (plan background_music.enabled or flag):
python3 ./scripts/run_from_plan.py \
  --plan ./output/my-replace-reel/plan.json \
  --out-dir ./output/my-replace-reel \
  --assemble-only --background-music
```

Set `"background_music": { "enabled": true, ... }` in the plan to skip the flag. Tool: [stable-audio-2.5](../../../tools/audio/stable-audio-2.5/SKILL.md).

Curl-first alternative: see `templates/curl-phase-a.template.sh` and tool skills under `tools/`.

## Expected path after install

```text
~/.cursor/skills/p-video-replace-comparison/
├── SKILL.md
├── scripts/run_from_plan.py
├── references/
└── templates/
```

## Repo clone (backward compatible)

```bash
python3 scripts/run_p_video_replace_announcement.py --phase stills
```
