#!/usr/bin/env bash
# Phase B — video (p-video-avatar, p-video-replace) after stills approved
set -euo pipefail
: "${PRUNA_API_KEY:?Set PRUNA_API_KEY}"

# Run plan runner after manual curl, or use curls from tools/p-video-replace/SKILL.md
# python3 ./scripts/run_from_plan.py --approve-stills --phase video --plan ./my-plan.json --out-dir ./output/reel

echo "Approve stills first, then run Phase B curls or run_from_plan.py --approve-stills --phase video"
