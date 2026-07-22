# Video prompt dramaturgy (`p-video`)

Creative-director layer for `p-video` motion prompts. Timing structure: [scene-anchor-pair.md](./scene-anchor-pair.md) / [scene-anchor-triple.md](./scene-anchor-triple.md). Vocabulary: [camera-lighting-vocabulary.md](./camera-lighting-vocabulary.md). Physics: [physics-safe-motion.md](./physics-safe-motion.md).

**Do not** apply OPEN/MID/CLOSE to [p-video-avatar](./p-video-avatar-prompting.md) — use a single continuous take.

**Sources:** patterns adapted from [smixs/visual-skills](https://github.com/smixs/visual-skills) (MIT); rewritten for Pruna.

## Details Law (non-negotiable)

Every OPEN / MID / CLOSE segment needs **at least three** concrete facts:

1. **Environmental pressure** — cold fridge light, wet asphalt, steam, flickering fluorescent, curtain in AC  
2. **Physical micro-action** — jaw locks, knuckles whiten, tail flicks, coat ripples, head turns toward lens  
3. **Sound or visual motif** — rain on the same pane, neon flicker before settle, phone glow, crowd murmur (even if audio is uploaded separately, name diegetic cues the picture should sell). When Mode A + `save_audio`, the motif may include **quoted dialogue** — see [audio-in-video-prompting.md](./audio-in-video-prompting.md)

Lazy words that fail the audit: `cinematic`, `masterpiece`, `stunning`, `epic`, `beautiful lighting`, bare emotions (`he is sad`) with no body.

## Scene formula (short piece)

Before writing beats, name:

| Element | Question |
|---------|----------|
| Desire | What does the subject want in this clip? |
| Obstacle | What resists (space, weather, timing)? |
| Space | Geometry the camera can read |
| Gaze | Where do eyes / lens look? |
| Rhythm | Hold → travel → settle |

**Three jobs** — each clip should do at least one: change emotion, advance action, increase pressure.

## Weight-at-start

Lead with **subject + action**. Camera and light in the middle. Style / palette last. Params (`duration`, `resolution`, model name) stay in API `input`, never in the prompt string.

## One primary camera move

Pick one dominant move for MID (dolly, track, crane, pan, push-in). Do not stack three moves in a 5–10s clip. See vocabulary sheet for lens language.

## Final-image rule

Name the ending frame explicitly — pairs with `last_frame_image` and CLOSE:

```text
CLOSE: settle on same bellhop facing camera as city lights glow — match end pose
```

## OPEN / MID / CLOSE + Details Law

```text
OPEN: hold on bellhop in elevator, eye-level, brass reflections, jaw set.
MID: brass doors open; same bellhop walks forward in one shoulder-height track onto the terrace; coat catches wind; neon signs flicker once.
CLOSE: he stops facing camera, city lights soft behind him — match end pose.
```

## Worked example — product B-roll (espresso hero still)

Brief lock: matte-black espresso machine, white marble bar, steam from portafilter. One primary move: slow push-in.

```text
OPEN: hold on matte-black espresso machine on white marble bar, soft window daylight, steam wisps from portafilter, shallow depth of field, product hero framing.
MID: same machine, slow dolly push-in along the bar; steam curls upward; chrome portafilter catches a soft highlight; marble grain readable.
CLOSE: settle on same machine centered in frame, steam still rising, bokeh cafe window behind — match end product angle.
```

Details Law audit: each beat names environment (marble bar, window light), micro-action (steam curls, push-in), motif (chrome highlight). No `cinematic masterpiece` filler.

## Pre-send audit

- [ ] Each beat has environment + micro-action + motif  
- [ ] Subject named in every beat when continuity matters  
- [ ] One primary camera path  
- [ ] CLOSE matches end still  
- [ ] No banned filler  
- [ ] Physics tier appropriate ([physics-safe-motion.md](./physics-safe-motion.md))  
- [ ] Audio mode chosen ([audio-in-video-prompting.md](./audio-in-video-prompting.md))
