# Physics-safe motion (`p-video`)

What motion language `p-video` handles well vs what breaks. Explainer specialization still lives in [interactive-explainer-motion.md](../workflows/interactive-explainer-motion.md) — **this file is the shared SSoT** for safe/trap tables.

Related: [prompt-dramaturgy.md](./prompt-dramaturgy.md) · [scene-anchor-pair.md](./scene-anchor-pair.md) · [p-video-avatar-prompting.md](./p-video-avatar-prompting.md).

## Two tiers

### Tier A — Visual transitions (pair / character travel)

When **start and end stills** both show the subject and the end state is physically reachable, you **may** prompt locomotion and travel:

- walk / ride / fly through a continuous space  
- doors open then subject walks through  
- one continuous camera path matching the stills  

Prefer **8–10s** duration. Name the subject every beat. See [scene-anchor-pair — physical transitions](./scene-anchor-pair.md#video-phase--physical-transitions).

### Tier B — Explainers, diagrams, object-heavy beats

Prefer **camera + light + atmosphere**. Avoid object contact and force simulation. Imply action in stills; sell reaction + camera in video.

## Safe motion (use these)

| Category | Examples |
|----------|----------|
| **Camera** | slow dolly in/out, gentle pan/tilt, push-in, drift, tracking |
| **Light** | spotlight finds subject, dawn spreads, window glow brightens, cloud shadow |
| **Atmosphere** | steam rises, dust motes, curtain sways, fog rolls, rain on glass |
| **Subject (minimal)** | head turn, eyes lift, single hand to chest, subtle lean — **one** gesture max |
| **Environment** | crowd silhouettes shift, cloth ripples, leaves rustle, water surface ripples |

## Physics traps (avoid unless Tier A stills fully support)

| Avoid | Why |
|-------|-----|
| throw / catch / toss / drop | trajectory breaks |
| pour / spill / splash | fluid fails |
| walk / run across room | foot contact glitches — **except** Tier A with matching end still |
| open door / slam / handoff prop | hinge and grip artifacts |
| pick up / set down / stack | contact physics |
| jump / fall / collide / fight / chase | body dynamics break |

**Bad (Tier B):** `MID: she throws the banner and runs toward the crowd`  
**Good (Tier B):** `MID: slow push-in on her face as crowd noise swells, banner ripples behind her`  
**Good (Tier A):** `MID: same bellhop walks forward through open doors in one tracking shot onto the terrace`

## Avatar subsection

[p-video-avatar](./p-video-avatar-prompting.md): **single continuous take** — no OPEN/MID/CLOSE. Avoid physics-trap gestures while talking (`walks across room`, `holds up document`, wild handoffs). Prefer MCU + one slow push-in + speaking to camera.

## Pre-send

- [ ] Tier A or B chosen consciously  
- [ ] No trap verbs unless end still supports them  
- [ ] One dominant camera move  
- [ ] Avatar rows: continuous-take wording only
