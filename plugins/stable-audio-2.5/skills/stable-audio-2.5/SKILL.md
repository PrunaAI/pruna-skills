---
name: stable-audio-2.5
description: Use when someone wants light instrumental background music — an ambient bed under dialogue or underscore for reels and explainers.
license: MIT
metadata:
  version: "1.0.5"
  provider: replicate
  replicate_model: stability-ai/stable-audio-2.5
---

# Stable Audio 2.5 (Replicate)

Text-to-music for **instrumental background beds** on launch reels. Not a Pruna P-model — runs on [Replicate](https://replicate.com/stability-ai/stable-audio-2.5).

**Mix helper (repo):** [`launch_background_music.py`](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/_shared/scripts/launch_background_music.py) — probes video length, generates bed, mixes under VO with ffmpeg.

## When to use

| Goal | Use this |
|------|----------|
| Light instrumental under a concat launch reel | Yes — after final assembly |
| Under **embedded narration** from scene anchor triple | Yes — mix quiet bed after concat — [audio-post-production.md](./references/audio-post-production.md) |
| Replace avatar VO | No — bed mixes **under** existing dialogue |
| Pruna-native audio | No — use [`p-video`](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/p-video/skills/p-video/SKILL.md) audio input instead |

## Environment

```bash
export REPLICATE_API_TOKEN=r8_...
```

Requires **`ffmpeg`** and **`ffprobe`** on PATH for mix step.

## Model input (Replicate)

| Field | Notes |
|-------|-------|
| `prompt` | **Required.** Style tags work well — e.g. *Instrumental light electronic pop, soft groove, mellow synth pads, no vocals, 94 BPM* |
| `duration` | Seconds, 1–190 (match or slightly exceed reel length) |
| `steps` | 4–8 (default 8) |
| `cfg_scale` | 1–25 (default 1) |
| `seed` | Optional integer for reproducibility |

Output: single **MP3** URL.

## HTTP (curl)

### Create prediction

```bash
curl -s -X POST \
  -H "Authorization: Bearer ${REPLICATE_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "prompt": "Instrumental light electronic pop bed, soft groove and mellow synth pads, calm positive tech atmosphere, understated background music, no vocals, 94 BPM",
      "duration": 90,
      "steps": 8,
      "cfg_scale": 1
    }
  }' \
  "https://api.replicate.com/v1/models/stability-ai/stable-audio-2.5/predictions"
```

Poll `urls.get` until `status` is `succeeded`; download `output` MP3.

## Launch reel integration

### Plan JSON (`background_music`)

```json
"background_music": {
  "enabled": true,
  "prompt": "Instrumental light electronic pop bed, soft groove and mellow synth pads, calm positive tech atmosphere, understated background music, no vocals, 94 BPM",
  "volume": 0.12,
  "output_name": "skills_library_announcement_with_music.mp4"
}
```

### Post-concat bed on any MP4

```bash
python3 workflows/_shared/scripts/launch_background_music.py \
  --video output/my_reel/final.mp4 \
  --volume 0.12
```

## Prompt tips (launch beds)

- Lead with **Instrumental** and **no vocals**
- Name mood: light, calm, positive, soft groove, mellow — keep *understated* and *background music* so beds sit under VO
- Optional BPM (**88–98** for tech launch reels; default script uses **94**)
- Avoid *energetic*, *driving*, or very high BPM — beds should support dialogue, not compete with it
- Avoid lyrics, song title, or artist name triggers
- Scene-specific beds (restaurant, jungle, boutique): name the setting but keep groove soft and BPM in the high 80s–mid 90s

## Related

- [audio-post-production.md](./references/audio-post-production.md) — narration + bed layering
- [gemini-3.1-flash-tts](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/gemini-3.1-flash-tts/skills/gemini-3.1-flash-tts/SKILL.md) — narration voiceover
- [visual-transition-reel](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/visual-transition-reel/skills/visual-transition-reel/SKILL.md) — concat + optional bed assembly
- [replicate-api.md](./references/replicate-api.md) — shared Replicate patterns
