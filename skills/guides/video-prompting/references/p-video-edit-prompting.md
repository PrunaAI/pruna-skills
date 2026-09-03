# p-video-edit prompting

Surgical edit prompts for `p-video-edit`. QA: [p-video-edit-quality-checklist.md](./p-video-edit-quality-checklist.md). Identity/slot swap on footage → [p-video-replace-prompting.md](./p-video-replace-prompting.md).

**`prompt`** is the edit instruction. Optional **`images`** (0–4) guide product, accessory, or style when the brief names a reference.

## Core formula

One principal change per run. Describe the desired final state, then name what must stay unchanged.

```text
Change only [specific thing]. Preserve [geometry / motion / camera / lighting / unmentioned subjects].
```

| Do | Don't |
|----|-------|
| `Change only the jacket from blue to red. Preserve its cut, folds and motion.` | `Make it cinematic` |
| Name the source element (`SUV body paint`, `text overlay "Miam"`, `plants in the corner`) | Vague `edit the video` |
| Point at refs: `Add the cargo box from the first reference to the roof.` | `Use the reference` with no slot |
| Keep-list for camera, motion, and subjects you are not changing | Hope the model leaves them alone |

## Decide edit intent first

| Intent | Prompt must |
|--------|-------------|
| **Attribute** | Name the property (color, material, shade) and keep cut/geometry/motion |
| **Remove** | Name only the object to delete; reconstruct the occluded surface |
| **Add** | Name what to add and where it attaches; keep the rest |
| **Environment** | Change setting or walls; preserve subject, furniture, camera path |
| **Relight** | Change atmosphere/palette only; keep faces, products, blocking |
| **Text** | Quote the exact string to add, replace, or remove |
| **Reference-guided** | Map each image to a source slot (`first reference` → roof box / sunglasses) |

## Weak jobs (warn before pay)

- A brand-new scene, plot, or video rather than an edit of this clip
- Adding an object with its own independent motion — especially a new in-hand shape
- Changing camera angle, camera motion, or zoom

Split those into a new `p-video` generation, or keep the camera locked and edit only appearance.

## Patterns (rewrite for the brief — do not paste as the user's prompt)

**Attribute**

```text
Change only the SUV body paint to deep metallic red. Preserve the vehicle geometry, glass, trim, headlights, tires, reflections and shadows. Keep the environment, lighting and camera movement unchanged.
```

**Remove**

```text
Remove only the potted plant from the countertop. Reconstruct the countertop and wall naturally. Keep the person, bottle, camera and lighting unchanged.
```

**Add (optional reference)**

```text
Add the roof cargo box shown in the first reference to the SUV. Match its shape, matte-black material and proportions. Keep it rigidly attached and correctly aligned to the vehicle roof throughout the camera movement. Preserve the vehicle body, windows, trim, wheels, environment and lighting.
```

**Environment**

```text
Change only the room wall from beige plaster to deep sage-green plaster. Preserve the room geometry and shadows. Keep the furniture and camera motion unchanged.
```

**Text**

```text
Remove only the text "Miam". Reconstruct the underlying image naturally where the text was located.
```

## Reference stills

Use when the user supplied a product, accessory, or SKU to match. Bare packshots — no extra hands or scene props. Index refs in `prompt` (`first reference`, `image 2`). Max 4 images (`jpg`, `jpeg`, `png`, `webp`).

## Pre-send

- [ ] Edit intent chosen (one principal change)
- [ ] Source element named + keep-list present
- [ ] Source `video` ≤ 15 seconds
- [ ] Refs (if any) indexed and ≤ 4
- [ ] Not a new scene, independent in-hand motion, or camera rewrite
- [ ] `draft` / `save_audio` decided
