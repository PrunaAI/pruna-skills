#!/usr/bin/env bash
# Phase A — person plates, garment refs, p-image-try-on (async). Review stills/ before Phase B.
set -euo pipefail

: "${PRUNA_API_KEY:?Set PRUNA_API_KEY}"

API="https://api.pruna.ai/v1"
MODEL_TRYON="p-image-try-on"
MODEL_IMAGE="p-image"

upload() {
  curl -sS -X POST "${API}/files" \
    -H "apikey: ${PRUNA_API_KEY}" \
    -F "content=@${1}"
}

create_async() {
  local model="$1"
  local payload="$2"
  curl -sS -X POST "${API}/predictions" \
    -H "Content-Type: application/json" \
    -H "apikey: ${PRUNA_API_KEY}" \
    -H "Model: ${model}" \
    -d "${payload}"
}

# Example — ecommerce PDP row (scene 1)
# 1) Generate person + garment with p-image (or upload local files)
# 2) Try-on:
create_async "${MODEL_TRYON}" '{
  "input": {
    "person_image": "PERSON_URL",
    "garment_images": ["GARMENT_URL"],
    "output_format": "png",
    "preserve_input_size": true
  }
}'

# Poll: GET https://api.pruna.ai/v1/predictions/status/PREDICTION_ID
# Download generation_url with apikey header
