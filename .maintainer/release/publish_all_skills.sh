#!/usr/bin/env bash
# Publish all bundled skills to ClawHub. Dry-run by default.
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
exec python3 "${REPO_ROOT}/.maintainer/release/publish_all_skills.py" "$@"
