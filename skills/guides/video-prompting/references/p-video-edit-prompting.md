# p-video-edit prompting

`prompt` craft for `p-video-edit`. QA: [p-video-edit-quality-checklist.md](./p-video-edit-quality-checklist.md).

Motion, camera, timing, and performance come from **`video`**. The edit comes from **`prompt`**. Optional **`images`** (up to 4) match a specific product, accessory, or look.

## Pick the edit family first

| Family | Typical ask | Needs `images`? |
|--------|-------------|-----------------|
| **Attribute / material** | Colorway, fabric, liquid, packaging variant | No |
| **Object add** | Attach an accessory or SKU to the subject | Usually yes |
| **Object remove** | Clean clutter, packaging, cables, props | No |
| **Text remove / edit** | Strip or localize on-screen ad copy | No |
| **Environment** | Move the shot to another setting or season | No |
| **Relight / mood** | Restyle lighting and grade, keep the subject | No |
| **Reference-guided replace** | Swap a product for an exact SKU | Yes |

Identity/person swaps are **not** this model — use `p-video-replace`.

## Change + preserve formula

```text
1. One principal change, as a final state ("Change only the sofa fabric to deep teal upholstery")
2. Reference hook when images are passed ("shown in the reference image")
3. Preserve-list (geometry, motion, camera movement, lighting, shadows, other objects, audio)
4. Persistence clause for long or cut-heavy clips ("in every frame, after every cut")
```

**Anti-patterns:** stacking unrelated edits in one run · mood-only strings (`make it pop`) · passing `images` without naming them in the prompt.

## Draft-then-final loop

| Step | Setting | Why |
|------|---------|-----|
| Explore wording | `draft: true` | $0.025/s — cheap enough to A/B three phrasings |
| Lock the prompt | keep `seed` fixed, change one variable | Isolates what the wording did |
| Deliver | `draft: false` | $0.045/s, full quality, same prompt |

Leave `prompt_upsampling: true` for production; turn it off only when testing a literal prompt.

## Good examples

**Attribute (fast pass)**

```text
Change only the plain trench coat into a yellow trench coat.
```

**Attribute (locked-in)**

```text
Change only the SUV body paint to deep metallic red.
Preserve the vehicle geometry, glass, trim, headlights, tires, reflections and shadows.
Keep the environment, lighting and camera movement unchanged.
```

**Object add from reference**

```text
Add the roof cargo box shown in the reference image to the SUV. Match its shape, matte-black material and proportions.
Keep it rigidly attached and correctly aligned to the vehicle roof throughout the camera movement.
Preserve the vehicle body, windows, trim, wheels, environment and lighting.
```

**Object remove**

```text
Remove only the potted plant from the countertop. Reconstruct the countertop and wall naturally.
Keep the person, bottle, camera and lighting unchanged.
```

**Text remove**

```text
Remove all advertising text overlays from the video.
Reconstruct the underlying image naturally where the text was located.
```

**Environment**

```text
Change only the room wall from beige plaster to deep sage-green plaster. Preserve the room geometry and shadows.
Keep the furniture and camera motion unchanged.
```

**Cut-heavy restyle (persistence clause)**

```text
Change the entire game environment into a colorful candy world, persistently from the first frame to the last.
Apply this environment after every cut and camera transition.
Preserve the runner, rivals, gameplay mechanics, course layout, camera, actions, speed and timing. Change nothing else.
```

## Reference stills

Bare packshots of the product or accessory — no extra hands, props, or busy scene. Match framing and scale to the slot in the source clip. `jpg`, `jpeg`, `png`, `webp`; up to four.

## Pre-send

- [ ] Edit family chosen
- [ ] One principal change only
- [ ] Preserve-list present (geometry, motion, camera, lighting)
- [ ] References named in the prompt when `images` is set
- [ ] Source clip ≤ 15 s
- [ ] Draft pass done before the full-quality run
- [ ] `save_audio` decided (source audio stays when true)
