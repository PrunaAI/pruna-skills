#!/usr/bin/env bash
# Phase B — motion from approved try-on stills. Run only after still review.
set -euo pipefail

: "${PRUNA_API_KEY:?Set PRUNA_API_KEY}"

API="https://api.pruna.ai/v1"

# Avatar row (virtual fitting room, UGC, hook, CTA)
curl -sS -X POST "${API}/predictions" \
  -H "Content-Type: application/json" \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H "Model: p-video-avatar" \
  -d '{
    "input": {
      "image": "TRY_ON_STILL_URL",
      "voice_script": "I uploaded a selfie and the dress from the product page — seconds later I am seeing the fit before I checkout.",
      "voice": "Kore",
      "voice_language": "English (US)",
      "voice_prompt": "Casual shopper UGC, friendly, clear lip sync.",
      "video_prompt": "Handheld micro-sway like phone selfie video. She speaks to camera, mouth centered.",
      "resolution": "720p"
    }
  }'

# I2V row (PDP, lookbook)
curl -sS -X POST "${API}/predictions" \
  -H "Content-Type: application/json" \
  -H "apikey: ${PRUNA_API_KEY}" \
  -H "Model: p-video" \
  -d '{
    "input": {
      "image": "TRY_ON_STILL_URL",
      "prompt": "Slow cinematic push-in, subtle fabric sway, soft studio light, no walking.",
      "duration": 8,
      "resolution": "720p",
      "aspect_ratio": "9:16"
    }
  }'

# After all clips: concat locally, then mix bed with launch_background_music.py
