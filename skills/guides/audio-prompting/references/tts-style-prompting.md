# TTS style prompting (Gemini 3.1 Flash TTS)

Director-style `prompt` craft for `gemini-3.1-flash-tts`. Upload results to Pruna for Mode B in-video audio (install `video-prompting`). Layering: [audio-post-production.md](./audio-post-production.md).

## Align three channels

| Channel | Role |
|---------|------|
| `text` | Spoken words (+ optional inline `[tags]`) |
| `prompt` | Tone, pace, accent, character — max ~4k bytes |
| `[tags]` in text | Momentary direction matching `prompt` |

All three must point the **same** emotional direction.

**Bracket clarity:** `[tags]` live only in this TTS `text` field. Still typography uses double-quoted `"[STRING]"` — see `image-prompting`. Native clip dialogue (`[subject] says "[LINE]"`) is Mode A in `video-prompting` — not this skill.

## Human narrator defaults

```text
Warm storybook narrator, gentle pace, empathetic, no announcer voice.
```

```text
Natural documentary host, measured pacing, clear consonants, calm authority.
```

Avoid: radio-ad hype, “cinematic trailer voice”, reading the product brief into `prompt`.

## Duration gate for `p-video`

Audio-led clips cap at **20s** (keep TTS ≤ **~19s**). If `ffprobe` is long:

1. Shorten `text`  
2. Add pace to `prompt`: `brisk pace, ~2.3 words per second, no filler`  
3. Split into two scene rows  

Never rely on post-mux over silent video.

## Avatar vs TTS

| Path | Fields |
|------|--------|
| Narrator B-roll | Gemini TTS → `p-video` `input.audio` |
| On-camera speaker | `p-video-avatar` `voice_script` + `voice_prompt` — **not** this TTS `prompt` |

Do not paste VO into avatar `voice_prompt`.

## Pre-send

- [ ] `prompt` / `text` / tags aligned  
- [ ] Length probed for `p-video`  
- [ ] Voice + language recorded in manifest for regen consistency

## Worked example — explainer narration (aligned channels)

User lock: documentary explainer, **measured** pace, ~45s script, will feed `p-video` Mode B.

**`prompt`** (director style):

```text
Natural documentary host, measured pacing, clear consonants, calm authority, empathetic, no radio-ad hype
```

**`text`** (spoken words + inline tags):

```text
[warm] Most teams treat diversity as a checkbox.
[pause] But the ritual seed is what breaks repetition before you ever hit generate.
[emphasis] Lock the brief first — then rotate free axes.
[measured] Same subject, fresh camera and light, every panel.
```

**Alignment check:** tags match the calm documentary `prompt` — no `[shout]` hype against a gentle director line.

**Duration gate:** 45s exceeds single **~19s** `p-video` audio-led cap → split into **three** scene rows (~15s each) or shorten copy; probe with `ffprobe` after TTS. Never plan one 45s embed clip.

**Avatar redirect:** on-camera host speaking to lens → `p-video-avatar` `voice_script` + `voice_prompt` — do **not** paste this TTS `prompt` into avatar fields.
