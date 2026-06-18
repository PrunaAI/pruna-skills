# Example prompt: P-Image-Try-On launch reel

Use **[p-image-try-on-launch](../../../guides/workflows/launches/p-image-try-on-launch/SKILL.md)** with **`try_on`** rows across six retail verticals. Pipeline: [try-on-beats.md](../../../guides/workflows/launches/p-image-try-on-launch/try-on-beats.md).

## Prompt

> Build a **p-image-try-on launch reel** (~75–90s, 9:16) that showcases **six fashion verticals**: ecommerce PDP, virtual fitting room, wholesale catalog, lookbook campaign, UGC ads, and personalized outfit recommendations.
>
> **Generation flow:** dynamic **`p-image`** person plates + **`p-image`** garment refs → **`p-image-try-on`** → slop gate → motion branch per scene:
> - **`avatar`** for fitting room + UGC + hook/CTA (`p-video-avatar`, speakable scripts)
> - **`i2v`** for PDP + lookbook (`p-video` subtle motion)
> - **`still_slider`** for wholesale + personalized outfits (before = person, after = try-on)
>
> **Variety:** distinct cast, settings, and garment categories per vertical — run [visual-variety-bible.md](../../../references/shared/visual-variety-bible.md) before API calls.
>
> **Narration:** Gemini TTS chapters on `i2v` and `still_slider` rows; lip-sync VO on `avatar` rows.
>
> **Delivery:** concat with crossfade → light **instrumental background music** under all dialogue (Stable Audio 2.5, ~0.12 volume, no vocals).

## Example scene table

| # | Vertical | Motion | Beat |
|---|----------|--------|------|
| 0 | intro | `avatar` | Hook — presenter in signature try-on look |
| 1 | ecommerce_pdp | `i2v` | Flat-lay dress → on-model + TTS |
| 2 | virtual_fitting_room | `avatar` | Selfie shopper speaks about fit |
| 3 | wholesale_catalog | `still_slider` | One sweater · diverse model |
| 4 | lookbook_campaign | `i2v` | Editorial coat + TTS |
| 5 | ugc_ads | `avatar` | Creator streetwear ad read |
| 6 | personalized_outfits | `still_slider` | 3-outfit ladder + TTS |
| 7 | outro | `avatar` | CTA |

## Run (after confirmation)

```bash
export PRUNA_API_KEY="your_key"
export REPLICATE_API_TOKEN="your_token"
pip install -r guides/workflows/launches/p-image-try-on-launch/scripts/requirements.txt

python3 guides/workflows/launches/p-image-try-on-launch/scripts/run_from_plan.py \
  --plan guides/workflows/launches/p-image-try-on-launch/templates/scene-plan.template.json \
  --out-dir output/launches/p-image-try-on-launch \
  --phase stills
```

After reviewing stills:

```bash
python3 guides/workflows/launches/p-image-try-on-launch/scripts/run_from_plan.py \
  --plan output/launches/p-image-try-on-launch/plan.json \
  --out-dir output/launches/p-image-try-on-launch \
  --approve-stills --phase video

python3 guides/workflows/launches/p-image-try-on-launch/scripts/run_from_plan.py \
  --plan output/launches/p-image-try-on-launch/plan.json \
  --out-dir output/launches/p-image-try-on-launch \
  --approve-stills --phase tts

python3 guides/workflows/launches/p-image-try-on-launch/scripts/run_from_plan.py \
  --plan output/launches/p-image-try-on-launch/plan.json \
  --out-dir output/launches/p-image-try-on-launch \
  --approve-audio --phase assemble --background-music
```

Plan template: [`templates/scene-plan.template.json`](../../../guides/workflows/launches/p-image-try-on-launch/templates/scene-plan.template.json)
