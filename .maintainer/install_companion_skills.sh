#!/usr/bin/env bash
# Companion Agent Skills for this repo (HyperFrames — launch reels, motion assembly).
# Project-local install → .agents/skills/ (gitignored; re-run after clone).
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${REPO_ROOT}"

CORE=(
  hyperframes
  hyperframes-animation
  hyperframes-cli
  hyperframes-core
  hyperframes-creative
  hyperframes-keyframes
  hyperframes-registry
  media-use
)

args=()
for s in "${CORE[@]}"; do
  args+=(--skill "$s")
done

echo "==> HyperFrames core skills → ${REPO_ROOT}/.agents/skills/"
npx --yes skills add heygen-com/hyperframes --full-depth "${args[@]}" -y --copy

echo ""
echo "Done. Router: hyperframes · workflows install on demand from there."
echo "Requires Node 22+ and ffmpeg for render."
