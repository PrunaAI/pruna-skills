#!/usr/bin/env bash
# Pre-commit: rebuild plugins/ when source skills change; block .mine in bundles.
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${REPO_ROOT}"

STAGED=$(git diff --cached --name-only --diff-filter=ACMR || true)
NEEDS_BUNDLE=0
while IFS= read -r f; do
  [[ -z "$f" ]] && continue
  case "$f" in
    tools/*|workflows/*|guides/*|references/*|skills.catalog.json|scripts/install_skill.sh|scripts/bundle*.sh|scripts/build_plugins.py|scripts/write_dep_manifests.py|scripts/write_skill_manifests.py|scripts/write_skills_sh_json.py|scripts/write_readme_skills_section.py|scripts/write_readme_install.py|scripts/skill_catalog.py|scripts/sync_skill_versions.py|VERSION)
      NEEDS_BUNDLE=1
      break
      ;;
  esac
done <<<"$STAGED"

if [[ "${NEEDS_BUNDLE}" -eq 1 ]]; then
  echo "Rebuilding plugins/ from tools/, guides/, workflows/ …"
  ./scripts/bundle_all_skills.sh
  git add plugins/ .claude-plugin/marketplace.json skills.sh.json README.skills.md README.md
fi

if [[ -d plugins ]] && rg -q '\.mine' plugins/ 2>/dev/null; then
  echo "plugins/ contains .mine references — fix source skills and rebundle" >&2
  exit 1
fi

exit 0
