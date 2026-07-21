# Camera and lighting vocabulary

Shared lexicon for `camera_tag` / `lighting_tag` (stills) and motion lines in `p-video` / `p-video-avatar` prompts. Diversity axes: [generation-diversity.md#visual-variety](../../generation-diversity/references/generation-diversity.md#visual-variety). Dramaturgy: [prompt-dramaturgy.md](./prompt-dramaturgy.md).

**Sources:** patterns adapted from [smixs/visual-skills](https://github.com/smixs/visual-skills) and [inference-sh/skills](https://github.com/inference-sh/skills) (MIT); rewritten for Pruna.

## Framing ladder

| Term | Use when |
|------|----------|
| ECU (extreme close-up) | Eyes, hands, product detail |
| CU (close-up) | Face, emotion |
| MCU (medium close-up) | Talking head default |
| MS (medium shot) | Waist-up action |
| MLS / FS | Full body travel |
| WS / EWS | Environment as character |

Log as `camera_tag`, e.g. `medium close-up, slight low angle`.

## Lens roles (optional but sharp)

| Lens | Feel |
|------|------|
| 24mm | Wide, immersive, exaggerated space |
| 35mm | Documentary natural |
| 50mm | Intimate human perspective |
| 85mm | Portrait, compressed background |
| Macro | Texture, product detail |

Example: `shot on 50mm, eye-level`.

## Camera moves (pick one for MID)

| Move | Prompt cue |
|------|------------|
| Dolly / push-in | `slow dolly in`, `gentle push-in` |
| Dolly out | `slow pull back revealing the room` |
| Pan | `gentle pan left across the alley` |
| Tilt | `tilt up from hands to face` |
| Track / truck | `shoulder-height tracking shot beside the subject` |
| Crane | `slow crane down past neon signs` |
| Static + atmosphere | `locked camera, steam rises, light shifts` |
| Handheld | `subtle handheld drift` (use sparingly) |

Avoid whip pans and stacked contradictory moves in one short clip.

## Motivated lighting

Prefer **named sources** over “beautiful lighting”:

| Source | Example cue |
|--------|-------------|
| Window / dawn | `dawn light spreads across the desk` |
| Practical | `warm lamp spill, cool window fill` |
| Neon / gel | `magenta-cyan neon rim, wet reflections` |
| Overhead institutional | `cold fluorescent flicker` |
| Fire / candle | `candle flicker on faces` (avatar: often too transition-y — prefer steady) |
| Overcast soft | `soft overcast skylight, low contrast` |

Log as `lighting_tag`. Hex in stills when brand colors matter (`#0d3d2d rim`).

## Palette cues (one look)

Pick one coherent palette phrase: `teal-magenta night`, `warm tungsten interior`, `bleached noon desert`, `desaturated documentary`.

Do not stack competing genre looks in one prompt.

## Avatar-friendly defaults

Talking heads: **MCU**, one slow push-in or static, **steady light**, mouth visible. Variety across scenes = change angle/background still, not five camera moves mid-line. See [p-video-avatar-prompting.md](./p-video-avatar-prompting.md).
