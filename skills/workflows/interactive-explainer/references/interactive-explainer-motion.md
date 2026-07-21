# Educational explainer motion (dynamic, physics-safe)

Motion rules for **narrator** (`p-video`) and **character** (`p-video-avatar`) beats in `interactive-explainer`.

**Shared SSoT for safe/trap tables:** [physics-safe-motion.md](../../../guides/video-prompting/references/physics-safe-motion.md). This file specializes those rules for explainers (Tier B defaults + avatar continuous-take).

Related: [scene-anchor-triple.md](../../../guides/video-prompting/references/scene-anchor-triple.md) · `visual-transition-reel` · [prompt-dramaturgy.md](../../../guides/video-prompting/references/prompt-dramaturgy.md)

## Defaults

| Field | Default |
|-------|---------|
| `defaults.resolution` | **`720p`** |
| `defaults.fps` | **`24`** (narrator `p-video` only; avatar uses `resolution`) |
| `defaults.aspect_ratio` | `16:9` |

## Goal

Every scene should **move** — camera, light, atmosphere, or subject — so the viewer stays engaged. Motion must **bridge start still → end still** without relying on **physics-heavy** actions that `p-video` handles poorly.

## Prompt shape

### Narrator (`p-video`) — OPEN / MID / CLOSE required

Write **`video_prompt`** as three beats:

```text
OPEN: [hold start composition briefly]
MID: [camera + safe motion developing — the attention hook]
CLOSE: [settle into end still]
```

Camera-led motion (dolly, pan, tilt, push-in, rack-focus feel).

### Character (`p-video-avatar`) — single continuous take

**Do not** use OPEN/MID/CLOSE on avatar rows — the model treats each beat as a transition and the clip feels cutty.

```text
Single continuous medium close-up, one very slow push-in over the full clip, speaks directly to camera, steady expression, no cuts, no glances away, minimal head motion
```

One camera move, steady light. Mouth motion comes from the avatar model.

## Safe motion (use these)

| Category | Examples |
|----------|----------|
| **Camera** | slow dolly in/out, gentle pan left/right, tilt up/down, push-in on face, drift across environment |
| **Light** | spotlight finds subject, dawn light spreads, candle flicker, window glow brightens, cloud shadow passes |
| **Atmosphere** | steam rises, dust motes, curtain sways, fog rolls, rain on glass (no splashing hands) |
| **Subject (minimal)** | head turn toward lens, eyes lift, single hand to chest, subtle lean — **one** gesture max |
| **Environment** | crowd silhouettes shift, banner cloth ripples, leaves rustle, water surface ripples (no objects entering water) |

## Avoid (physics trap)

Shared trap table: [physics-safe-motion.md](../../../guides/video-prompting/references/physics-safe-motion.md). For explainers, stay on **Tier B** — do **not** prompt object interaction, locomotion, or force:

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
- Keep moves **slow and deliberate**, not whip pans (bump to `48` fps only for final delivery if needed)

### Character (`p-video-avatar`)

- **`video_prompt`** = one continuous shot — camera + framing only, not plot action
- Safe: `single continuous medium close-up, one very slow push-in, speaks directly to camera, no cuts`
- Avoid: OPEN/MID/CLOSE beats, `candle flicker`, `expression shift`, `light shifts` (read as transitions)
- Avoid: `gestures wildly`, `walks across room while talking`, `holds up document`
- Clip length follows **`voice_script`** — no ~19s TTS cap (that limit is narrator `p-video` only)

## Examples

### Narrator (history / science)

```json
"video_prompt": "OPEN: hold wide establishing frame. MID: slow push-in toward key detail in steady light. CLOSE: settle on end composition."
```

### Narrator (diagram / mechanism)

```json
"video_prompt": "OPEN: hold wide subject. MID: gentle drift toward focal detail, subtle atmosphere. CLOSE: hold end frame — no physics action."
```

### Character (any flavor)

```json
"video_prompt": "Single continuous medium close-up, one very slow push-in, speaks directly to camera, steady light, full color, no gestures, no cuts."
```

## Plan checklist (before render)

- [ ] Every **narrator** scene has **OPEN / MID / CLOSE** in `video_prompt`
- [ ] **Character** scenes use **one continuous take** wording — no OPEN/MID/CLOSE
- [ ] Narrator MID contains **visible motion** (not `OPEN: hold. CLOSE: hold.`)
- [ ] No physics-trap verbs in `video_prompt`
- [ ] `defaults.resolution` = `720p`, `defaults.fps` = `24`
- [ ] Start/end stills differ enough that camera move has somewhere to go

Agent must reject plans missing MID beat or using physics-trap verbs — see `interactive-explainer` and this checklist.
