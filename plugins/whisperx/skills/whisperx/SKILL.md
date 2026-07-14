---
name: whisperx
description: Use when the user needs word-level lyric timestamps, cut-safe line boundaries for music videos, or alignment after song generation before editing clips.
license: MIT
metadata:
  version: "0.0.2"
  provider: replicate
  replicate_model: victor-upmeet/whisperx
---

# WhisperX (Replicate · word-level STT)

Transcribes the **rendered song** with **word-level timestamps**. Primary use: [music-video](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/music-video/skills/music-video/SKILL.md) cut alignment after `music-2.5`.

Model: [victor-upmeet/whisperx](https://replicate.com/victor-upmeet/whisperx)

## When to use

| Goal | Use this |
|------|----------|
| Align music-video cuts to actual sung lines | Yes — run after `song.mp3` exists |
| Write lyrics from scratch | No — lyrics come from the plan first |
| Narration / VO timing | Possible, but [gemini-3.1-flash-tts](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/gemini-3.1-flash-tts/skills/gemini-3.1-flash-tts/SKILL.md) scripts are cleaner |

## Environment

```bash
export REPLICATE_API_TOKEN=r8_...
```

## Pipeline

```bash
# 1. Transcribe (word timestamps + YouTube SRT)
python3 workflows/verticals/music-video/scripts/transcribe_song.py \
  --song output/my-mv/song.mp3 \
  --out output/my-mv/whisperx_transcript.json \
  --initial-prompt "First few lyric lines help recognition"
# Also writes output/my-mv/whisperx_transcript.srt (UTF-8, upload to YouTube Studio)

# 2. Align cut manifest (requires cut_manifest.json from parse_lyric_cuts.py)
python3 workflows/verticals/music-video/scripts/align_lyric_cuts.py \
  --cuts output/my-mv/cut_manifest.json \
  --transcript output/my-mv/whisperx_transcript.json \
  --song output/my-mv/song.mp3

# Or via runner:
python3 workflows/verticals/music-video/scripts/run_from_plan.py \
  --plan output/my-mv/music_video_plan.json \
  --out-dir output/my-mv \
  --phase align
```

## Model input

| Field | Notes |
|-------|-------|
| `audio_file` | **Required.** HTTPS URL — local files uploaded via Replicate `/v1/files` |
| `language` | ISO code, e.g. `en` — speeds up and improves accuracy |
| `align_output` | **`true`** — word-level timestamps (required for cut alignment) |
| `initial_prompt` | Optional — first lyric lines improve rap/sung recognition |
| `diarization` | Optional — speaker labels; useful for multi-voice battles |

## Output

`whisperx_transcript.json`:

```json
{
  "detected_language": "en",
  "segments": [
    {
      "start": 0.071,
      "end": 2.254,
      "text": " I shipped the future while you wrote a constitution.",
      "words": [
        {"word": "I", "start": 0.071, "end": 0.111, "score": 0.5}
      ]
    }
  ]
}
```

`align_lyric_cuts.py` fuzzy-matches each planned lyric line to a contiguous word span, sets `start_sec` / `end_sec`, and gap-fills instrumental sections.

**YouTube subtitles:** `transcribe_song.py` also writes `whisperx_transcript.srt` beside the JSON — UTF-8 SRT with word-timed cues grouped for readable two-line captions. Upload in YouTube Studio → Subtitles → Upload file. Re-generate from existing JSON:

```bash
python3 workflows/_shared/scripts/whisperx_to_srt.py \
  --transcript output/my-mv/whisperx_transcript.json
```

## Related

- [music-video workflow](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/music-video/skills/music-video/SKILL.md)
- [lyrics-and-cuts.md](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/verticals/music-video/lyrics-and-cuts.md)
- [music-2.5](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/music-2.5/skills/music-2.5/SKILL.md)
