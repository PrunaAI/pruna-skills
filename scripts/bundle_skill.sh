#!/usr/bin/env bash
# Bundle one portable skill into skills/<name>/ for npx skills add
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILL="${1:?Usage: bundle_skill.sh <skill-name> [--mine]}"
shift
"${REPO_ROOT}/scripts/install_skill.sh" "${SKILL}" --target "${REPO_ROOT}/skills" "$@"
echo "Bundled -> ${REPO_ROOT}/skills/${SKILL}"
