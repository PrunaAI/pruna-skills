#!/usr/bin/env bash
# Single validate entrypoint: bundle freshness → skills-ref → clawhub → install smoke.
# Usage: ./scripts/validate_release.sh [--skip-verify] [--skip-clawhub] [--skip-smoke]
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${REPO_ROOT}"

SKIP_VERIFY=0
SKIP_CLAWHUB=0
SKIP_SMOKE=0
for arg in "$@"; do
  case "$arg" in
    --skip-verify) SKIP_VERIFY=1 ;;
    --skip-clawhub) SKIP_CLAWHUB=1 ;;
    --skip-smoke) SKIP_SMOKE=1 ;;
    -h|--help)
      echo "Usage: $0 [--skip-verify] [--skip-clawhub] [--skip-smoke]"
      exit 0
      ;;
  esac
done

if [[ "${SKIP_VERIFY}" -eq 0 ]]; then
  echo "==> verify_skill_bundles"
  ./scripts/verify_skill_bundles.sh
else
  echo "==> skip verify"
fi

echo "==> skills.sh.json --check"
python3 scripts/write_skills_sh_json.py --check

echo "==> validate_all_skills (skills-ref)"
python3 scripts/validate_all_skills.py

if [[ "${SKIP_CLAWHUB}" -eq 0 ]]; then
  echo "==> validate_clawhub_plugins"
  ./scripts/validate_clawhub_plugins.sh
else
  echo "==> skip clawhub"
fi

if [[ "${SKIP_SMOKE}" -eq 0 ]]; then
  echo "==> smoke_install"
  ./scripts/smoke_install.sh
else
  echo "==> skip smoke"
fi

echo "validate_release: OK"
