# Audio-in-video prompting (`p-video`)

How to **write prompts** when sound matters on `p-video`. Tool picker and mix levels: [audio-post-production.md](../audio/audio-post-production.md). TTS craft: [tts-style-prompting.md](../audio/tts-style-prompting.md). Talking heads: [p-video-avatar-prompting.md](./p-video-avatar-prompting.md).

## Three modes

| Mode | API | Prompt job |
|------|-----|------------|
| **A — Native SFX / dialogue** | `prompt` + optional `save_audio`; use `duration` | Name **diegetic** sounds the picture should emit |
| **B — Uploaded audio (preferred for VO/music)** | `audio` URL; **omit `duration`**; `save_audio: true` | Motion matches **mood/beats** of the track — do not paste VO text into `prompt` |
| **C — Post bed** | Stable Audio mixed under VO in ffmpeg | Bed prompt is separate ([music-and-bed-prompting.md](../audio/music-and-bed-prompting.md)); video prompt ignores the bed |

Never generate silent `p-video` and post-mux narration unless re-render is impossible (truncation risk). Probe TTS ≤ ~19s before Mode B.

## Mode A — native SFX / dialogue

**When:** `save_audio: true`, no uploaded `audio`, user wants diegetic SFX and/or spoken lines in the clip.

### Diegetic SFX

Be concrete; skip `cinematic soundscape`:

| Bad | Good |
|-----|------|
| `epic soundtrack vibe` | `rain ticks on the awning, distant train horn once` |
| `dramatic music` | `crowd murmur swells, single glass clink` |

Keep cues short — the model invents audio from visual+prompt context when `save_audio` is on.

### Native dialogue

Put **exact spoken words in double quotes** inside the motion `prompt` (Mode A only). Placeholders in square brackets below are docs notation, not literal syntax — do not confuse with Gemini TTS `[tags]`.

**Template** (inside OPEN/MID/CLOSE):

```text
MID: [same subject] says "[LINE]" — mouth open, [one gesture toward target]; [optional diegetic SFX cue]
```

Rules:

- Exact spoken words in **double quotes** — never paraphrase the line
- Name **who** speaks — repeat the subject label for continuity (`same [role]`)
- Pair every line with **mouth state** + **one gesture** (point, turn to camera, hand on prop)
- Keep lines **short** (1–2 per beat)
- Diegetic SFX can sit beside dialogue — stay concrete (table above)
- **Mode B:** when `input.audio` is set, do **not** put the VO transcript in `prompt` — motion matches mood only

## Mode B — motion matches uploaded audio

```text
OPEN: hold wide on dog in tall grass, warm afternoon light.
MID: gentle push-in as he searches; tail motion matches narrator energy; grass sways.
CLOSE: settle on end pose — curious head tilt.
```

Rules:

- Describe **picture motion**, not the spoken words.  
- Match energy: tense VO → tighter push-in; calm story → slow drift.  
- Optional: `motion matches narrator mood` once — not a transcript.  
- Triple anchors: [scene-anchor-triple.md](./scene-anchor-triple.md).

## Avatar path (not Mode B fields)

`p-video-avatar` uses `voice_script` + `voice_prompt` + `video_prompt` — not `p-video` `input.audio` for the spoken line. See avatar prompting ref. Do not paste script lines into `voice_prompt`.

## Pre-send

- [ ] Mode A / B / C chosen  
- [ ] Mode B: `duration` omitted; TTS length probed  
- [ ] No VO transcript inside motion `prompt` (Mode B)  
- [ ] Diegetic cues concrete (Mode A) or mood-aligned (Mode B)
- [ ] Mode A dialogue (if any): quoted line + named speaker + mouth + one gesture
