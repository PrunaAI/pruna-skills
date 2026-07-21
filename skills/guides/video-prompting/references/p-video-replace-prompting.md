# p-video-replace prompting

`instruction_prompt` craft for `p-video-replace`. QA: [p-video-replace-quality-checklist.md](./p-video-replace-quality-checklist.md).

Identity comes from **`images`**. Slot mapping comes from **`instruction_prompt`**.

## Decide swap intent first

| Intent | Reference shows | Prompt must |
|--------|-----------------|-------------|
| **Character** | New person | Name who in the **source** is replaced; keep motion/scene |
| **Clothing** | Outfit | Replace **only garments**; keep face, motion, background |
| **Object** | Packshot/prop | Replace **only the object**; keep hands/camera |
| **Mixed** | 1–4 refs | Map **each** image index to a source slot |

## Slot-mapping formula

```text
1. Name the specific source element (left person / olive coat / bottle in right hand)
2. Map to reference ("first reference", "reference image 2")
3. Preserve-list (camera, audio, background, other people, props you keep)
4. Closer: "Only the [X] should change; everything else stays as the source."
```

**Anti-pattern:** `Replace the person in the video` with no source slot or preserve-list.

## Multi-ref vs multi_job

| Approach | When |
|----------|------|
| One call, up to 4 `images` | Mixed slots in a single shot |
| **`multi_job`** (one image per call) | Variant rows / safer isolation — prefer for replace reels |

Held objects: name the **person** as swap target and list the prop as **preserved**, or the ref may land on the object.

## Good examples

**Character**

```text
Replace the man in the centre of the group, the one adjusting his sunglasses, with the man from the reference.
Preserve motion, audio, camera, lighting, and the other four men exactly as in the source.
```

**Clothing only**

```text
Replace the olive-green t-shirt the woman is wearing with the white oxford button-down from the reference.
Preserve her face, hair, the earbuds case in her right hand, gestures, speech, studio, lighting, camera, and audio.
Only the top she is wearing should change; everything else stays as the source.
```

**Object**

```text
Replace the matte-black earbuds case in the woman's right hand with the terracotta succulent from the reference.
Preserve her face, hair, olive t-shirt, gestures, speech, studio, lighting, camera, and audio.
Only the object in her hand should change; everything else stays as the source.
```

**Mixed**

```text
Replace the olive-green t-shirt with the white oxford from reference image 1, AND replace the earbuds case with the coffee tumbler from reference image 2.
Preserve her face, hair, gestures, speech, studio, lighting, camera, and audio.
Both the top and the hand object should change; everything else stays as the source.
```

## Reference stills

Bare product/garment packshots when swapping objects/clothes — no extra hands/props in frame. Match framing/scale to the source slot.

## Pre-send

- [ ] Swap intent chosen  
- [ ] Source element named + ref indexed  
- [ ] Preserve-list present  
- [ ] Clothing/object jobs end with “only X changes”  
- [ ] `save_audio` decided (source voice stays when true)
