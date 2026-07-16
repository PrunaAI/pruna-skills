#!/usr/bin/env bash
# Drop errant ClawHub 1.0.0 releases and republish at repo VERSION (see ../VERSION).
# ClawHub defaults new skills to 1.0.0 when --version is omitted; semver then keeps
# that as latest even after publishing 0.0.x.
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${REPO_ROOT}"

VER="$(tr -d '[:space:]' < VERSION)"
SKILLS=(
  p-video-replace
  pruna-generative-pipeline
  pruna-run
  requesting-generation-feedback
  stable-audio-2.5
  visual-transition-reel
  whisperx
)

slug() { printf '%s' "$1" | tr '.' '-'; }

for skill in "${SKILLS[@]}"; do
  spec="@pruna-ai/$(slug "$skill")"
  echo "=== ${skill} (${spec}) ==="
  ./scripts/publish_all_skills.sh --execute --target clawhub --skill "${skill}"
  if clawhub inspect "${spec}" 2>/dev/null | grep -q 'Latest   1.0.0'; then
    echo "  deleting errant 1.0.0 (replacement ${VER} is live)..."
    clawhub delete "${spec}" --version 1.0.0 --yes
  fi
done

echo "Done. ClawHub skills should show latest ${VER}."
