#!/usr/bin/env bash
# Bundle all public skills into plugins/ for marketplace and npx skills add
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${REPO_ROOT}"

python3 scripts/sync_skill_versions.py
python3 scripts/write_readme_install.py

STAGING=$(mktemp -d)
trap 'rm -rf "$STAGING"' EXIT
mkdir -p "${STAGING}"

while IFS= read -r skill; do
  [[ -z "${skill}" ]] && continue
  echo "==> ${skill}"
  ./scripts/install_skill.sh "${skill}" --target "${STAGING}"
done < <(python3 -c "from scripts.skill_catalog import all_primary_skills; print('\n'.join(all_primary_skills()))")

python3 scripts/build_plugins.py --staging "${STAGING}"
python3 scripts/write_skills_sh_json.py
python3 scripts/write_readme_skills_section.py

python3 scripts/publish_all_skills.py --target index --skip-verify

echo "Done. Install: npx skills add PrunaAI/pruna-skills@<name> -y"
echo "         Or:    npx plugins add PrunaAI/pruna-skills   # pick from list"
echo "         Or:    npx plugins add PrunaAI/pruna-skills -y  # all plugins"

