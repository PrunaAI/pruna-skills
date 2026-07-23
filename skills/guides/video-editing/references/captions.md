# Captions and subtitles

Burn readable captions onto finished video, or mux soft subtitles. **Alignment** is a paid step — use `whisperx`; **styling and burn-in** live here.

## Pipeline overview

```text
1. Extract mono 16 kHz audio from video (or use isolated narration track — better coverage)
2. Run whisperx on audio → word-level JSON
3. Build ASS (preferred) or SRT from word timestamps
4. Burn with ffmpeg + libass (re-encode required)
```

Install `whisperx` + `pruna-api` before step 2. Follow that skill's HTTP phase table — do not restate payloads here.

## Default style — phrase bar + word accent (launch reels)

A **stable phrase line** on layer 0; the **spoken word** tints **purple** (`#F6369B`) on layer 1. One black bar per cue — no second box on the accent.

| Layer | Style | Visual |
|-------|-------|--------|
| **0 — phrase** | `PhraseBase` | Full phrase, white text, semi-transparent **black bar** (`BackColour` `&H47000000`, `BorderStyle=3`, `Outline=12`) — **one dialogue for the whole cue** |
| **1 — accent** | `WordAccent` | Same phrase string; inactive tokens `{\alpha&HFF&}`; active token `{\alpha&H00&\1c&H00F6369B&}` — **text only, no box** |

Mechanism: layer 0 never swaps per word (no flicker). Layer 1 swaps only the purple tint.

### Style rules (critical)

| Rule | Layer 0 `PhraseBase` | Layer 1 `WordAccent` |
|------|----------------------|----------------------|
| Background bar | `BorderStyle=3`, `Outline=12` | **`BorderStyle=0`** — no outline, no box |
| `BackColour` | `&H47000000` (semi-transparent bar) | `&HFF000000` (fully transparent) |
| Font / size / pos | `Helvetica Neue` 34, `{\an2\pos(960,1024)}` | **Match layer 0 exactly** |
| Fade | `{\fad(80,0)}` on cue start only | **No `\fad`** on word handoffs |
| Duration | Full cue window | One dialogue per word; window runs word start → next word start (or cue end) |

Do **not**:

- Replace layer 0 per word — redraws the bar every token (**flicker**)
- Put `BorderStyle=3` on the accent layer — draws a **second box** over the phrase bar
- Tint the whole line with per-word layer-0 dialogues or `\t` colour swaps
- Use per-word `\pos` — libass layout must match via identical metrics + alpha-hide

Shared tokens:

- **Launch size** — `Fontsize` **34**, `Bold=1`, bottom-center (`Alignment=2`), `MarginV` **56**
- **Min whisper token** — **0.18s**
- **Single line** — max **42 characters** per cue for launch reels (no `\N` breaks)

### Movie / broadcast timing (apply when grouping cues)

Use when building phrase windows from whisperx + SRT:

| Limit | Value |
|-------|--------|
| Max characters per line | **42** |
| Max lines on screen (launch default) | **1** (line-block fallback: **2**) |
| Min cue duration | **0.83s** |
| Max cue duration | **6s** |
| Max reading speed | **17 CPS** |
| Min gap between cues | **80ms** |

Extend cue end to cover the last spoken word; never truncate words because SRT windows were parsed too narrow (see below).

### SRT timestamp pitfall

SRT uses **centiseconds** after the comma: `00:00:05,31` → **5.31s**.

```python
# wrong — treats ,31 as milliseconds → 5.031s, drops trailing words
int(ms) / 1000

# correct
int(cs) / 100.0
```

When phrase text “cuts off” or vanishes early, check SRT parsing first.

Use **isolated narration audio** when the final mux has a loud bed — whisperx on the mixed master often misses quiet opening lines.

### ASS template (1920×1080)

```ass
[Script Info]
Title: Phrase bar + word accent
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: PhraseBase,Helvetica Neue,34,&H00FFFFFF,&H00FFFFFF,&H00000000,&H47000000,1,0,0,0,100,100,0,0,3,12,0,2,48,48,56,1
Style: WordAccent,Helvetica Neue,34,&H00FFFFFF,&H00FFFFFF,&H00000000,&HFF000000,1,0,0,0,100,100,0,0,0,0,0,2,48,48,56,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.35,0:00:02.71,PhraseBase,,0,0,0,,{\an2\pos(960,1024)\fad(80,0)}Your coding agent can generate images,
Dialogue: 1,0:00:00.69,0:00:01.03,WordAccent,,0,0,0,,{\an2\pos(960,1024)}{\alpha&HFF&}Your {\alpha&H00&\1c&H00F6369B&}coding{\alpha&HFF&} agent can generate images,
Dialogue: 1,0:00:01.03,0:00:01.37,WordAccent,,0,0,0,,{\an2\pos(960,1024)}{\alpha&HFF&}Your {\alpha&HFF&}coding{\alpha&HFF&} {\alpha&H00&\1c&H00F6369B&}agent{\alpha&HFF&} can generate images,
```

Colour notes (ASS uses `&HAABBGGRR`):

| Token | ASS | Role |
|-------|-----|------|
| White text | `&H00FFFFFF` | Phrase bar (layer 0) |
| Accent tint | `\alpha&H00&\1c&H00F6369B&` | Active word on layer 1 |
| Hidden overlay | `\alpha&HFF&` | Inactive tokens on layer 1 (layout only) |
| Outer box | `&H47000000` | Phrase bar (**layer 0 only**) |

### Build rules (from whisperx JSON)

1. Collect `segments[].words[]`; skip empty tokens; enforce **min duration 0.18s** per word.
2. **Group words into phrases** — prefer timed `captions.srt` cues; split long lines at **42 characters**; **one line** for launch reels.
3. Layer 0: one `PhraseBase` dialogue per phrase (full duration, `{\fad(80,0)}` only).
4. Layer 1: one `WordAccent` dialogue per word — **same phrase string**, alpha-hide inactive tokens; highlight window from word start through **next word start** (or cue end).
5. Layer 1: **no `\fad`**; optional **50ms** end overlap between adjacent accent dialogues is fine — do not redraw layer 0.
6. Pin `{\an2\pos(x,y)}` on all events; identical font metrics on both styles.

9:16 exports: set `PlayResX/PlayResY` to `1080×1920`, reduce `Fontsize` to **28**, `MarginV` to **72**.

**Duplicate subs:** if HyperFrames HTML still includes `.subtitle` clips, the render will bake phrase captions into the MP4 *and* post-burn adds overlays — remove HTML subtitle layers before render when using this path.

### Burn-in (libass)

Burn-in uses **`ass=`** (required for `\t` colour transforms). Default Homebrew **`ffmpeg`** often omits libass — install **`ffmpeg-full`**:

```bash
/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg -filters 2>/dev/null | grep -E ' ass | subtitles '
```

```bash
cd captions_dir
/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg -y -i ../input.mp4 \
  -vf "ass=captions_burn.ass" \
  -c:v libx264 -crf 20 -preset veryfast -c:a copy \
  -pix_fmt yuv420p -movflags +faststart ../output_captioned.mp4
```

## Alternate style — word-only pop (one word at a time)

When the phrase bar feels too busy, show **one word per cue** with only the outer black box. One `Dialogue` line per word with `{\fad(80,80)}`.

## Alternate style — line-block (fallback)

When word-accent layering is too much (long narrated docs, no karaoke):

- **Max ~42 characters** per line, **max 2 lines** per cue (`\N`)
- **Min display ~0.83s**, **max ~6s** per cue, **max 17 CPS**
- Break at sentence boundaries; **gap ≥ 80ms** between cues

Use SRT + `subtitles=` or a simpler ASS style without per-word transforms.

## Extract audio for whisperx

Prefer **narration-only** file when available:

```bash
ffmpeg -y -i narration.mp3 -acodec pcm_s16le -ar 16000 -ac 1 audio_16k.wav
```

From mixed master (may miss quiet VO under bed):

```bash
ffmpeg -y -i input.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 audio_16k.wav
```

Upload via `pruna-api` helpers; run whisperx with `align_output: true` and an `initial_prompt` of the first script lines.

## Soft subtitles (timing check only)

Mux without re-encoding — no box styling:

```bash
ffmpeg -y -i input.mp4 -i captions.srt -c copy -c:s mov_text -metadata:s:s:0 language=eng soft_subbed.mp4
```

Burn-in is required for social platforms that ignore subtitle tracks.

## When NOT to use whisperx here

- User already has timed SRT/ASS → skip to burn-in
- Full song generation → `music-2.5`
- TTS generation → `gemini-3.1-flash-tts`

Lyric-synced **cuts** (not on-screen text) → whisperx output feeds edit decisions in `music-video`.

### HyperFrames compositions (post-render only)

HyperFrames renders motion + audio **without** burned captions. Caption burn-in is always a **separate ffmpeg pass** on the finished MP4.

```text
1. HyperFrames: npm run check && npm run render → render.mp4
2. whisperx on isolated narration (NOT the bed-heavy master) → word-level JSON
3. Build phrase-bar + word-accent ASS (this doc) → burn with ffmpeg-full
4. Optional: amix bed under captioned render (-c:v copy) → background-music.md
```

Do **not** inject subtitle `<div>` clips into `index.html` for social deliverables — that duplicates timing work and is harder to iterate than a post-burn script. Full pipeline: [combination-hyperframes.md](./combination-hyperframes.md).

**Timing rule:** narration must start at **t=0** in the final mux (same as the whisperx source file). If VO is offset in the composition, shift ASS timestamps or align on the mixed track only as a last resort.

**SRT rule:** when grouping phrases from whisperx, regenerate cue windows from the transcript JSON — hand-edited SRT with wrong comma decimals (ms vs cs) drops or merges cues silently.

## Next steps

- Bed under captioned VO → [background-music.md](./background-music.md)
- Export → [export-presets.md](./export-presets.md)
