#!/usr/bin/env bash
# Rebuild all plugins and verify the requested skill exists.
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILL="${1:?Usage: bundle_skill.sh <skill-name> [--mine]}"
shift
"${REPO_ROOT}/scripts/bundle_all_skills.sh"
PLUGIN="${REPO_ROOT}/plugins/${SKILL}"
if [[ ! -f "${PLUGIN}/skills/${SKILL}/SKILL.md" ]]; then
  echo "Plugin not found after rebuild: ${PLUGIN}" >&2
  exit 1
fi
echo "Bundled -> ${PLUGIN}"
