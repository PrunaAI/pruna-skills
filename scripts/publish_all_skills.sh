#!/usr/bin/env bash
# Publish all bundled skills to PSPM. Dry-run by default.
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
exec python3 "${REPO_ROOT}/scripts/publish_all_skills.py" "$@"
