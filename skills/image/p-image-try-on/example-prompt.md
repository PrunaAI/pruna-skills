# p-image-try-on — example prompts

**Before every job:** random seed ritual (`generation-diversity`).

Try-on scenario briefs and Replicate reference links. **Cross-model persona + avatar examples:** `image-prompting`.

Starter plates aligned with `image-prompting` and `image-prompting`.

## Canonical reference outputs

Quality bar (Replicate playground candidates):

1. [Editorial seated + artistic shirt](https://replicate.com/p/p47vaj1f91rmw0cyt4er0z2zd4)
2. [Complex collaged suit, high angle](https://replicate.com/p/tf7gqansnnrmt0cyt4j8mpx1c8)
3. [Mirror selfie + cap + logo tee](https://replicate.com/p/hp60wyj355rmy0cyt4psnc2mh0)
4. [Multi-garment streetwear stack](https://replicate.com/p/bak21xr79srmr0cyt52tap1nw8)
5. [Pleated blouse, golden-hour portrait](https://replicate.com/p/g9hd22x26drmr0cytmtsx11c5g)

## Person plate → try-on (minimal curl flow)

```bash
export PRUNA_API_KEY="your_key"

# 1) Generate photoreal plate (or upload your own)
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-image' \
  -d '{"input":{"prompt":"Photoreal editorial fashion photograph, woman mid-20s South Asian, seated on weathered wood floor against textured plaster wall, soft window daylight, 3:4, natural skin, single subject one frame","aspect_ratio":"3:4"}}'

# Complete random seed ritual (SSoT) before writing prompts — do not pass ritual string as API seed

# 2) Upload person + garment refs → /v1/files, then try-on (normal mode for finals)
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-image-try-on' \
  -d '{
    "input": {
      "person_image": "https://api.pruna.ai/v1/files/PERSON_ID",
      "garment_images": ["https://api.pruna.ai/v1/files/GARMENT_ID"],
      "output_quality": 95,
      "preserve_input_size": true
    }
  }'
```

Run the slop gate on the person plate before step 2. Run `image-prompting` on the output.

## Scenario briefs

### Complex collaged suit (tier D)

**Person plate:** high-angle full-body studio, shirtless male model, hands in pockets — see showcase doc.

**Garments:** two refs (blazer + trousers) or one on-model lifestyle ref with:

```json
"prompt": "the artistic collaged blazer from image 1 and the matching patchwork trousers from image 2"
```

**Settings:** `turbo: false`, up to 2–4 garment URLs.

### Streetwear stack (tier D, multi-garment)

**Person plate:** full-body asphalt, prop in frame (bat, bag) — preserve props in output.

**Garments:** jacket, tee, pants as separate packshots **or** one stack photo + prompt:

```json
"prompt": "the patchwork jacket from image 1, the yellow logo tee from image 2, and the patchwork pants from image 3"
```

### Accessories in-scene (tier E)

**Person plate:** mirror selfie or street portrait with visible head/shoulders.

**Garments:** cap ref + tee ref (≤6 total). Verify hat brim and logo placement in checklist.

### Golden-hour texture (tier D + lifestyle)

**Person plate:** cinematic portrait, shallow DOF — pleated or crinkled fabric refs show best here.

**Optional next step:** `p-image-upscale` → `p-video-avatar` for ecommerce VO.

## Diversity rotation (five public examples)

When publishing a set, avoid five identical “white studio + plain tee” rows:

| Slot | Cast shift | Setting shift | Garment shift |
|------|------------|---------------|---------------|
| 1 | Woman, Mediterranean | Editorial floor | Artistic print shirt |
| 2 | Man, East Asian | High-angle studio | Collaged suit |
| 3 | Woman, East Asian | Night street mirror | Cap + logo tee |
| 4 | Woman, East Asian | Open asphalt | Patchwork stack |
| 5 | Woman, ambiguous | Golden-hour field | Pleated blouse |

See generation-diversity.md#visual-variety (`generation-diversity`) for cast ledger fields.
