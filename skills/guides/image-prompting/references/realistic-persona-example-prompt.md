# Dynamic persona — example prompts

Cross-model examples for **`p-image`** scenario plates → optional **`p-image-try-on`** → **`p-video-avatar`**.

**Before every curl:** [random seed ritual](../../generation-diversity/references/generation-diversity.md#random-seed-ritual-mandatory-before-every-generation) (SSoT) + [generation diversity](../../generation-diversity/references/generation-diversity.md) — state ritual string and derive axes; **omit API `seed`** unless user sets `api_seed`.

Full ladders and 8-slot matrix: [realistic-persona-showcase.md](./realistic-persona-showcase.md).

## 1. Photoreal documentary (`p-image`) — avatar-ready

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-image' \
  -d '{
    "input": {
      "prompt": "Photorealistic documentary portrait photograph of a real person, not CGI. Man early 30s Black, short fade haircut, charcoal henley, creative loft exposed brick and teal window bokeh, slight low angle chest-up, soft overcast daylight, mouth clearly visible ready to speak, natural skin pores, horizontal wide framing, single subject one frame",
      "aspect_ratio": "16:9"
    }
  }'
```

Plan fields: `render_medium_tag: photoreal`, `visual_style_tag: documentary`, `camera_tag: low_angle_mc`, `setting_tag: loft_brick`.

## 2. Premium cinematic cel anime (`p-image`) — avatar host

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-image' \
  -d '{
    "input": {
      "prompt": "Premium anime cinematic young woman hero, cel-shaded film look, violet hair, iridescent jacket, cherry-blossom rooftop at dusk with neon color bokeh, low heroic angle from the side, mouth visible mid-speech, bright clear evening atmosphere, classic portrait framing, single character one frame",
      "aspect_ratio": "4:3"    }
  }'
```

Plan fields: `render_medium_tag: cel_anime_2d`, `visual_style_tag: anime_cinematic`, `camera_tag: low_angle_hero`, `setting_tag: rooftop_dusk`.

## 3. Claymation presenter (`p-image`)

```text
Stop-motion claymation character woman presenter, visible clay texture, chunky knit scarf, round glasses,
miniature handmade cozy living room set with tiny lamp and bookshelf, medium close-up,
mouth sculpted for speech, warm practical stop-motion desk-lamp lighting, single character one frame.
```

Plan fields: `render_medium_tag: stop_motion_3d`, `visual_style_tag: clay_stop_motion`, `setting_tag: clay_living_room`.

## 4. High-angle editorial fashion (`p-image`) — try-on canvas

```text
Photoreal fashion lookbook, man early 30s East Asian, short styled hair, shirtless,
standing hands in pockets, seamless off-white studio floor, high angle from above,
even soft studio light, full body head to shoes visible, single subject one frame.
```

Use as **`person_image`** for complex suit try-on — see [p-image-try-on-quality-checklist.md](p-image-try-on-quality-checklist.md).

## 5. Scene variant (`p-image-edit`) — same identity, new angle + world

```text
Using the attached reference as identity — keep exact same person, face, skin texture, photoreal quality.
Rooftop at dusk, city lights bokeh, side angle chest-up, mouth unobstructed, cobalt hoodie,
closed hardcover notebook at chest, warm golden rim light on hair, 9:16 single subject one frame.
```

Change **only** `setting_tag`, `camera_tag`, and wardrobe delta — not identity.

## 6. Dynamic avatar — photoreal UGC

Reuse **approved hero plate URL**. Unique **`video_prompt`** per scene.

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video-avatar' \
  -d '{
    "input": {
      "image": "https://api.pruna.ai/v1/files/APPROVED_STILL_ID",
      "voice_script": "Hey — we put the patchwork set on a real street plate, not a white studio. Face and background stayed put.",
      "voice": "Puck (Male)",
      "voice_language": "English (US)",
      "voice_prompt": "Natural UGC creator tone, relaxed pacing, honest not salesy.",
      "video_prompt": "Low angle handheld sway, subtle arc left, glance to notebook then back to lens",
      "resolution": "720p"    }
  }'
```

## 7. Dynamic avatar — cinematic cel host

```bash
curl -X POST 'https://api.pruna.ai/v1/predictions' \
  -H 'Content-Type: application/json' -H "apikey: ${PRUNA_API_KEY}" \
  -H 'Model: p-video-avatar' \
  -d '{
    "input": {
      "image": "https://api.pruna.ai/v1/files/ANIME_STILL_ID",
      "voice_script": "So — same motion grammar, totally different world. That is the point of planning each scene.",
      "voice": "Zephyr (Female)",
      "voice_language": "English (US)",
      "voice_prompt": "Warm anime protagonist delivery, expressive but natural, not exaggerated dub energy.",
      "video_prompt": "Low heroic angle, subtle head tilt, confident smile building mid-line",
      "resolution": "720p"    }
  }'
```

## 8. Fashion try-on → avatar (three-step)

| Step | Action |
|------|--------|
| A | **`p-image`** full-body street plate |
| B | **`p-image-try-on`** patchwork stack, `turbo: false` |
| C | **`p-video-avatar`** — script references outfit naturally |

## 9. Eight-slot scenario matrix (playground gallery)

When publishing a public set, cover **medium × angle × setting × aspect_ratio** — not one look:

| Slot | Medium | Style | Camera | Setting | `aspect_ratio` |
|------|--------|-------|--------|---------|----------------|
| 1 | photoreal | documentary | low_angle_mc | loft_brick | `2:3` |
| 2 | photoreal | editorial_fashion | high_angle_full | plaster_floor | `16:9` |
| 3 | photoreal | street_ugc | side_angle | mirror_selfie_night | `9:16` |
| 4 | cel_anime_2d | anime_cinematic | low_angle_hero | rooftop_dusk | `4:3` |
| 5 | cel_anime_2d | cyberpunk_anime | side_angle | neon_alley | `3:4` |
| 6 | stop_motion_3d | clay_stop_motion | medium_cu | clay_living_room | `1:1` |
| 7 | cg_3d_film | fairy_tale_3d | medium_cu | enchanted_garden | `3:2` |
| 8 | photoreal | cinematic_film | extreme_cu | golden_hour_field | `2:3` |

Each slot: distinct **`cast_descriptor`** and **`aspect_ratio`**. Avatar slots: unique **`video_prompt`**.

Full rules: [realistic-persona-showcase.md](./realistic-persona-showcase.md) · [generation-diversity.md#visual-variety](../../generation-diversity/references/generation-diversity.md#visual-variety).
