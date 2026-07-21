# Music and bed prompting

Prompt craft for `music-2.5` (songs with vocals) and `stable-audio-2.5` (instrumental beds). Mix/stack: [audio-post-production.md](./audio-post-production.md). In-video sync: [audio-in-video-prompting.md](../video/audio-in-video-prompting.md).

## Music 2.5 (full song)

Stack: **genre + mood + vocal + tempo + instruments + production feel** (≤ ~2000 chars).

```text
Indie pop, uplifting, warm female vocal, 92 BPM, acoustic guitar and mellow synth pads, no harsh distortion
```

| Include | Avoid |
|---------|-------|
| Genre, BPM, vocal timbre, key instruments | Vague `epic cinematic masterpiece` |
| Explicit `no harsh distortion` / energy caps when needed | Contradictions (`lo-fi quiet` + `stadium EDM drop`) |

Same lyrics + prompt still yield different arrangements — lock seeds only when the user asks.

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
- [ ] Song: genre/mood/vocal/tempo present  
- [ ] Duration matches scene or assembly plan
