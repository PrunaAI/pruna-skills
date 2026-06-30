#!/usr/bin/env bash
# Pre-commit: rebuild skills/ when catalog sources change; block .mine in bundles.
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${REPO_ROOT}"

STAGED=$(git diff --cached --name-only --diff-filter=ACMR || true)
NEEDS_BUNDLE=0
while IFS= read -r f; do
  [[ -z "$f" ]] && continue
  case "$f" in
    catalog/*|scripts/install_skill.sh|scripts/bundle*.sh|scripts/write_dep_manifests.py|scripts/write_skill_manifests.py|scripts/sync_skill_versions.py|VERSION)
      NEEDS_BUNDLE=1
      break
      ;;
  esac
done <<<"$STAGED"

if [[ "${NEEDS_BUNDLE}" -eq 1 ]]; then
  echo "Rebuilding skills/ from catalog/ …"
  ./scripts/bundle_all_skills.sh
  git add skills/
fi

if [[ -d skills ]] && rg -q '\.mine' skills/ 2>/dev/null; then
  echo "skills/ contains .mine references — fix catalog sources and rebundle" >&2
  exit 1
fi

exit 0
