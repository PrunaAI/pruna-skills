---
name: music-2.5
description: Use when the user wants AI song generation with vocals, sung lyrics, original tracks from a style prompt, or source audio for a music video.
license: MIT
metadata:
  version: "1.0.2"
  provider: replicate
  replicate_model: minimax/music-2.5
---

# Music 2.5 (MiniMax · Replicate)

Full-length **songs with natural vocals** from lyrics + style description. Not a Pruna P-model — runs on [Replicate](https://replicate.com/minimax/music-2.5).

**Primary workflow:** [music-video](../music-video/SKILL.md) — lyrics → song → lyric-safe cuts → `p-video-avatar` / `p-video` clips → assembly.

## When to use

| Goal | Use this |
|------|----------|
| Sung track for a music video | Yes — write lyrics with section tags first |
| Drive **`p-video`** clip length | Yes — export MP3 → upload to Pruna → `audio` input |
| Documentary narration | No — use [gemini-3.1-flash-tts](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/gemini-3.1-flash-tts/skills/gemini-3.1-flash-tts/SKILL.md) |
| Instrumental bed under VO | No — use [stable-audio-2.5](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/stable-audio-2.5/skills/stable-audio-2.5/SKILL.md) |

## Environment

```bash
export REPLICATE_API_TOKEN=r8_...
```

Requires **`ffmpeg`** / **`ffprobe`** for slicing and assembly in the music-video workflow.

## Model input (Replicate)

| Field | Notes |
|-------|-------|
| `lyrics` | **Required.** 1–3,500 characters. Use [structure tags](#structure-tags) and `\n` line breaks. |
| `prompt` | Optional style string — genre, mood, tempo, vocal timbre, key instruments (up to ~2,000 chars). |
| `sample_rate` | `16000` · `24000` · `32000` · **`44100`** (default) |
| `bitrate` | `32000` · `64000` · `128000` · **`256000`** (default) |
| `audio_format` | **`mp3`** (default) · `wav` · `pcm` |

Output: audio file URL (typically **MP3**, ~2:30–4:30 for full songs).

## Structure tags

Control arrangement with tags on their own lines (see [Music 2.5 readme](https://replicate.com/minimax/music-2.5)):

`[Intro]` · `[Verse]` · `[Pre Chorus]` · `[Chorus]` · `[Hook]` · `[Bridge]` · `[Solo]` · `[Inst]` · `[Build Up]` · `[Drop]` · `[Interlude]` · `[Break]` · `[Transition]` · `[Outro]`

- One tag per section; follow with 2–4 lyric lines per section for clean melodies.
- `\n` = line break (also a **safe video cut boundary** in the music-video workflow).
- `\n\n` = pause between sections.
- Parentheticals work for ad-libs and directions: `(Ooh, yeah)` · `(Guitar solo — slow, bluesy)`.

## Prompt tips

Follow the model’s [prompt guide](https://replicate.com/minimax/music-2.5): genre + mood + vocal description + tempo + instruments + production feel.

**Example prompt:**

```text
Indie pop, uplifting, warm female vocal, 92 BPM, acoustic guitar and soft synth pads,
wide soundstage, crisp modern production, anthemic chorus
```

**Instrumental sections:** use `[Inst]` or `[Solo]` tags with parenthetical instrument directions instead of sung lines.

## HTTP (curl)

```bash
curl -s -X POST \
  -H "Authorization: Bearer ${REPLICATE_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "lyrics": "[Verse]\nWe built it line by line\nEvery skill a stepping stone\n\n[Chorus]\nRun the pipeline, watch it grow\nPruna models, let them flow",
      "prompt": "Indie pop, uplifting, warm female vocal, 92 BPM, acoustic guitar and mellow synth pads, no harsh distortion",
      "sample_rate": 44100,
      "bitrate": 256000,
      "audio_format": "mp3"
    }
  }' \
  "https://api.replicate.com/v1/models/minimax/music-2.5/predictions"
```

Poll `urls.get` until `status` is `succeeded`; download `output`.

## Repo helper

```bash
python3 workflows/verticals/music-video/scripts/generate_song.py \
  --plan output/my-music-video/music_video_plan.json \
  --out-dir output/my-music-video
```

## Good to know

- **English and Mandarin** have strongest pronunciation; other languages vary.
- Each generation is unique — same lyrics + prompt produce different arrangements.
- Max ~5 minutes per generation.
- Data is sent to MiniMax via Replicate — see their [privacy policy](https://www.minimax.io/platform/protocol/privacy-policy).

## Related

- [audio-post-production.md](https://github.com/PrunaAI/pruna-skills/tree/main/references/shared/audio-post-production.md) — when to use songs vs narration vs beds
- [music-video workflow](../music-video/SKILL.md)
- [gemini-3.1-flash-tts](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/gemini-3.1-flash-tts/skills/gemini-3.1-flash-tts/SKILL.md) — spoken narration (not song)
- [stable-audio-2.5](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/stable-audio-2.5/skills/stable-audio-2.5/SKILL.md) — instrumental beds only
- [replicate-api.md](./references/replicate-api.md)
