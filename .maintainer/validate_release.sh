#!/usr/bin/env bash
# Single validate entrypoint: layout → skills-ref → install smoke.
# Usage: make validate   or   ./.maintainer/validate_release.sh [--skip-verify] [--skip-smoke]
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${REPO_ROOT}"

SKIP_VERIFY=0
SKIP_SMOKE=0
for arg in "$@"; do
  case "$arg" in
    --skip-verify) SKIP_VERIFY=1 ;;
    --skip-smoke) SKIP_SMOKE=1 ;;
    -h|--help)
      echo "Usage: $0 [--skip-verify] [--skip-smoke]"
      exit 0
      ;;
  esac
done

if [[ "${SKIP_VERIFY}" -eq 0 ]]; then
  echo "==> verify_skill_bundles"
  ./.maintainer/verify_skill_bundles.sh
else
  echo "==> skip verify"
fi

echo "==> skills.sh.json --check"
python3 .maintainer/write_skills_sh_json.py --check

echo "==> validate_all_skills (skills-ref)"
python3 .maintainer/validate_all_skills.py

if [[ "${SKIP_SMOKE}" -eq 0 ]]; then
  echo "==> smoke_install"
  ./.maintainer/smoke_install.sh
else
  echo "==> skip smoke"
fi

echo "validate_release: OK"
