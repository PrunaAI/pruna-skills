#!/usr/bin/env bash
# Phase A — stills only (p-image / p-image-edit)
# Copy curls from tools/*/SKILL.md; shared upload/poll/download: references/pruna-api.md
set -euo pipefail
: "${PRUNA_API_KEY:?Set PRUNA_API_KEY}"

# Example: hero still (p-image) — replace prompt/seed from your plan
# curl -X POST 'https://api.pruna.ai/v1/predictions' \
#   -H 'Content-Type: application/json' \
#   -H "apikey: ${PRUNA_API_KEY}" \
#   -H 'Model: p-image' \
#   -d '{"input":{"prompt":"…","aspect_ratio":"16:9","seed":12345}}'
# Poll + download: see references/pruna-api.md

echo "Fill per-scene curls from tool skills, then run: python3 ./scripts/run_from_plan.py --phase stills --plan ./my-plan.json --out-dir ./output/reel"
