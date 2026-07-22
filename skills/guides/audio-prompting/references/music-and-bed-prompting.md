# Music and bed prompting

Prompt craft for `music-2.5` (songs with vocals) and `stable-audio-2.5` (instrumental beds). Mix/stack: [audio-post-production.md](./audio-post-production.md). In-video sync: install `video-prompting`.

## Music 2.5 (full song)

Stack: **genre + mood + vocal + tempo + instruments + production feel** (≤ ~2000 chars). Pair with a **lyrics** field — verse / chorus / bridge structure for vocal tracks.

```text
Indie pop, uplifting, warm female vocal, 92 BPM, acoustic guitar and mellow synth pads, no harsh distortion
```

**Lyrics:** write singable lines per section (verse, chorus, optional bridge). Lock structure before the paid call; same lyrics + prompt still yield different arrangements — lock seeds only when the user asks.

| Include | Avoid |
|---------|-------|
| Genre, BPM, vocal timbre, key instruments | Vague `epic cinematic masterpiece` |
| Explicit `no harsh distortion` / energy caps when needed | Contradictions (`lo-fi quiet` + `stadium EDM drop`) |

## Stable Audio 2.5 (beds under VO)

Instrumental, understated, mix-friendly:

```text
Instrumental light electronic pop bed, soft groove and mellow synth pads, calm positive tech atmosphere, understated background music, no vocals, 94 BPM
```

Rules:

- Always **`no vocals`** when under narration  
- Keep energy **below** dialogue — assembly mixes ~0.08–0.15 under VO  
- Tag style works well; keep prompts short  

## Which tool?

| Need | Tool |
|------|------|
| Sung song / music video source | Music 2.5 |
| Quiet bed under TTS or avatar | Stable Audio 2.5 |
| Diegetic SFX inside `p-video` | Native `save_audio` / prompt cues — not these models |

## Pre-send

- [ ] Song vs bed chosen deliberately  
- [ ] Bed: no vocals + BPM + understated  
- [ ] Song: genre/mood/vocal/tempo + **lyrics** structure present  
- [ ] Duration matches scene or assembly plan

## Worked examples

### Full song (Music 2.5) — indie pop, remote-work theme

User lock: warm female vocal, ~92 BPM, acoustic + mellow synth, **not** EDM drop.

**Style prompt** (`prompt` field):

```text
Indie pop, warm and hopeful, female vocal, 92 BPM, acoustic guitar and mellow synth pads, intimate bedroom-production feel, no harsh distortion, no stadium drop
```

**Lyrics** (`lyrics` field — verse / chorus / bridge):

```text
[Verse 1]
Coffee rings on the desk again
Window light on a second screen
Slack pings like a metronome
Building something from my home

[Chorus]
We're still here, we're still on
Pixels bridge what miles have drawn
Heart in the work, voice in the song
Remote but never alone

[Verse 2]
Cat walks across the keyboard line
Deadline hums but the team's aligned
Same sky, different time zones
Same goal in our headphones

[Bridge]
When the Wi‑Fi stutters, we don't fold
Call reconnects — the story holds

[Chorus]
We're still here, we're still on
...
```

Confirm lyrics + style before `POST`. For music-video cut points later → `whisperx` after the track exists.

### Instrumental bed (Stable Audio 2.5) — explainer under VO

User lock: **90s**, calm tech explainer, dialogue must stay clear.

```text
Instrumental light electronic pop bed, soft groove and mellow synth pads, calm positive tech atmosphere, understated background music, no vocals, 94 BPM
```

Duration: `90` seconds. Mix target ~0.08–0.15 under narration in assembly — see [audio-post-production.md](./audio-post-production.md).

### Wrong tool check

| User ask | Tool |
|----------|------|
| "Sing an original chorus about launch day" | Music 2.5 + **lyrics** |
| "Quiet underscore while the host talks" | Stable Audio + **no vocals** |
| "Replace the sung hook with spoken VO" | Gemini TTS — not Stable Audio |
