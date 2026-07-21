# p-video-animate prompting

Motion-transfer craft for `p-video-animate`. QA: [p-video-animate-quality-checklist.md](./p-video-animate-quality-checklist.md). Mixed reels: [animate-beats.md](../../workflows/avatar-multi-scene/animate-beats.md).

**Appearance from `image`, motion from `video`.** Wrong tool for identity swap on real footage → [p-video-replace-prompting.md](./p-video-replace-prompting.md).

## Pairing gates (before every job)

Ask:

1. **Framing** — same body region (head-and-shoulders / medium / full body)?  
2. **Pose** — facing and limb position roughly aligned with the template’s first frame?  
3. **Visibility** — same body parts visible; no crop the video lacks?

| Factor | Guidance |
|--------|----------|
| Shot size | Match close-up / medium / full |
| Facing | Front still + profile motion → artifacts |
| Limbs | If template waves arms, still must show arms |
| Proportions | Human full-body dance on chibi often breaks gait |
| Speaking templates | Mouth clear and large when source has dialogue |

**Pairing failure:** head-and-shoulders still + full-body dance → model does **not** invent limbs; choreography is lost. Repose with `p-image-edit` or pick a closer template.

## `instruction_prompt`

Optional. Overrides **behavior**, not identity. **Leave blank** when source motion is already right.

**Useful** — one specific end beat:

```text
At the very end of the clip, just after her last gesture, she gives a clear thumbs-up toward the camera. Keep the source motion otherwise.
```

**Less useful** — redescribes the still:

```text
A confident woman in a charcoal blazer speaks to the camera in a modern office.
```

## Style variety

Photoreal, cartoon, 3D, and mascot stills can share one template when framing aligns — the still’s render style carries through.

## Speaking motion sources

When this template feeds lip-sync showcases, the source clip (often from `p-video-avatar`) must show clear speaking / lip movement. See [p-video-avatar-prompting.md](./p-video-avatar-prompting.md) and animate-beats.

## Pre-send

- [ ] Framing / pose / limbs match  
- [ ] `instruction_prompt` blank or one concrete beat  
- [ ] Not using animate for in-place replace  
- [ ] Long templates split (~5s compute per 1s video)
