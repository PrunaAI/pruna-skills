---
name: stable-audio-2.5
description: Generates instrumental background music via Replicate stability-ai/stable-audio-2.5 for launch reels and mixes it under video with ffmpeg. Use when the user wants chill background music, ambient bed, or Stable Audio on a concat launch video.
license: MIT
metadata:
  version: "0.0.1"
  provider: replicate
  replicate_model: stability-ai/stable-audio-2.5
---

# Stable Audio 2.5 (Replicate)

Text-to-music for **instrumental background beds** on launch reels. Not a Pruna P-model — runs on [Replicate](https://replicate.com/stability-ai/stable-audio-2.5).

**Mix helper (repo):** [`launch_background_music.py`](../../../guides/workflows/_shared/scripts/launch_background_music.py) — probes video length, generates bed, mixes under VO with ffmpeg.

## When to use

| Goal | Use this |
|------|----------|
| Chill instrumental under a concat launch reel | Yes — after final assembly |
| Replace avatar VO | No — bed mixes **under** existing dialogue |
| Pruna-native audio | No — use [`p-video`](../../video/p-video/SKILL.md) audio input instead |

## Environment

```bash
export REPLICATE_API_TOKEN=r8_...
```

Requires **`ffmpeg`** and **`ffprobe`** on PATH for mix step.

## Model input (Replicate)

| Field | Notes |
|-------|-------|
| `prompt` | **Required.** Style tags work well — e.g. *Instrumental chill lo-fi ambient, soft piano, no vocals, 85 BPM* |
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
      "prompt": "Instrumental chill lo-fi ambient bed, soft piano and warm pads, no vocals, relaxed modern tech atmosphere, 85 BPM",
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
  "prompt": "Instrumental chill lo-fi ambient bed, soft piano and warm pads, no vocals, 85 BPM",
  "volume": 0.12,
  "output_name": "skills_library_announcement_with_music.mp4"
}
```

### Replace workflow runner (after concat)

```bash
python3 guides/workflows/p-video-replace-comparison/scripts/run_from_plan.py \
  --plan output/skills-library-announcement/announcement_plan.json \
  --out-dir output/skills-library-announcement \
  --phase all --background-music
```

Or standalone on any MP4:

```bash
python3 guides/workflows/_shared/scripts/launch_background_music.py \
  --video output/skills-library-announcement/p_video_replace_announcement.mp4 \
  --volume 0.12
```

## Prompt tips (launch beds)

- Lead with **Instrumental** and **no vocals**
- Name mood: chill, lo-fi, ambient, understated, warm pads
- Optional BPM (80–95 for tech launch reels)
- Avoid lyrics, song title, or artist name triggers

## Related

- [p-video-replace-comparison](../../../guides/workflows/p-video-replace-comparison/SKILL.md) — final assembly phase
- [replicate-api.md](../../../references/replicate-api.md) — shared Replicate patterns
