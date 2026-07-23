#!/usr/bin/env bash
# Pre-commit: regenerate catalog when source skills change.
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${REPO_ROOT}"

STAGED=$(git diff --cached --name-only --diff-filter=ACMR || true)
NEEDS_BUNDLE=0
while IFS= read -r f; do
  [[ -z "$f" ]] && continue
  case "$f" in
    skills/*|.maintainer/skills.catalog.json|.maintainer/bundle*.sh|.maintainer/write_skills_sh_json.py|.maintainer/write_readme_skills_section.py|.maintainer/write_skill_cross_refs.py|.maintainer/skill_catalog.py|.maintainer/sync_skill_versions.py|.maintainer/write_marketplace.py|VERSION)
      NEEDS_BUNDLE=1
      break
      ;;
  esac
done <<<"$STAGED"

if [[ "${NEEDS_BUNDLE}" -eq 1 ]]; then
  echo "Regenerating catalog …"
  ./.maintainer/bundle_all_skills.sh
  git add skills/ skills.sh.json docs/SKILL-CATALOG.md .maintainer/publish-index.json .claude-plugin/marketplace.json README.md AGENTS.md 2>/dev/null || true
fi

exit 0
