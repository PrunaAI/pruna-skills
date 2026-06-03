# Educational explainer motion (dynamic, physics-safe)

Motion rules for **narrator** (`p-video`) and **character** (`p-video-avatar`) beats in [educational-explainer](../guides/workflows/verticals/interactive-explainer/SKILL.md).

Related: [scene-anchor-triple.md](./scene-anchor-triple.md) · [scene-transition-video](../guides/workflows/core/visual-transition-reel/SKILL.md)

## Defaults

| Field | Default |
|-------|---------|
| `defaults.resolution` | **`1080p`** |
| `defaults.fps` | **`48`** (narrator `p-video` only; avatar uses `resolution`) |
| `defaults.aspect_ratio` | `16:9` |

## Goal

Every scene should **move** — camera, light, atmosphere, or subject — so the viewer stays engaged. Motion must **bridge start still → end still** without relying on **physics-heavy** actions that `p-video` handles poorly.

## Prompt shape (required)

Write **`video_prompt`** as three beats:

```text
OPEN: [hold start composition briefly]
MID: [camera + safe motion developing — the attention hook]
CLOSE: [settle into end still]
```

**Narrator scenes:** camera-led motion (dolly, pan, tilt, push-in, rack-focus feel).  
**Character scenes:** speaking + subtle push-in, expression shift, light flicker — mouth already moving via avatar.

## Safe motion (use these)

| Category | Examples |
|----------|----------|
| **Camera** | slow dolly in/out, gentle pan left/right, tilt up/down, push-in on face, drift across environment |
| **Light** | spotlight finds subject, dawn light spreads, candle flicker, window glow brightens, cloud shadow passes |
| **Atmosphere** | steam rises, dust motes, curtain sways, fog rolls, rain on glass (no splashing hands) |
| **Subject (minimal)** | head turn toward lens, eyes lift, single hand to chest, subtle lean — **one** gesture max |
| **Environment** | crowd silhouettes shift, banner cloth ripples, leaves rustle, water surface ripples (no objects entering water) |

## Avoid (physics trap)

Do **not** prompt object interaction, locomotion, or force:

| Avoid | Why |
|-------|-----|
| throw / catch / toss / drop | object trajectory breaks |
| pour / spill / splash | fluid simulation fails |
| walk / run / stride across room | foot contact glitches |
| open door / slam / handoff prop | hinge and grip artifacts |
| pick up / set down / stack items | contact physics |
| jump / fall / collide | body dynamics break |
| fight / chase / sports action | multi-body chaos |

If the story needs action, **imply it** in the stills and use **camera move + reaction** in video — not the action itself.

**Bad:** `MID: she throws the banner and runs toward the crowd`  
**Good:** `MID: slow push-in on her face as crowd noise swells, banner ripples behind her`

## By scene type

### Narrator (`p-video` + triple)

- Start/end stills define composition; **`video_prompt` sells the transition**
- Prefer **one dominant camera move** in MID — not three unrelated motions
- Match narration energy: tense scenes → tighter push-in; legacy → slow tilt up
- At **48 fps**, motion reads smoother — keep moves **slow and deliberate**, not whip pans

### Character (`p-video-avatar`)

- **`video_prompt`** = camera + performance framing, not plot action
- Safe: `medium close-up, subtle push-in, speaks directly to camera, soft expression shift`
- Avoid: `gestures wildly`, `walks across room while talking`, `holds up document`

## Examples

### History (Ancaster-style)

```json
"video_prompt": "OPEN: hold desk and map. MID: slow push-in as candle flickers, shadow crosses ledger. CLOSE: finger rests on Ancaster — hold end frame."
```

### Science

```json
"video_prompt": "OPEN: hold cross-section wide. MID: gentle drift toward glowing magma chamber, heat shimmer in air. CLOSE: settle on bright core — no eruption, no splashing."
```

### Character witness

```json
"video_prompt": "Medium close-up, speaks directly to camera, subtle push-in, moonlight shifts on face, grave witness tone — no hand gestures."
```

## Plan checklist (before render)

- [ ] Every scene has **OPEN / MID / CLOSE** in `video_prompt`
- [ ] MID contains **visible motion** (not `OPEN: hold. CLOSE: hold.`)
- [ ] No physics-trap verbs in `video_prompt`
- [ ] `defaults.resolution` = `1080p`, `defaults.fps` = `48`
- [ ] Start/end stills differ enough that camera move has somewhere to go

Runner warns on missing MID beat or physics keywords — see [`run_from_plan.py`](../guides/workflows/verticals/interactive-explainer/scripts/run_from_plan.py) `validate_plan`.
