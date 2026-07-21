#!/usr/bin/env bash
# Sync versions + regenerate catalog / skills.sh / marketplace (skills-only).
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${REPO_ROOT}"

python3 .maintainer/sync_skill_versions.py
python3 .maintainer/write_skill_cross_refs.py
python3 .maintainer/write_skills_sh_json.py
python3 .maintainer/write_readme_skills_section.py
python3 .maintainer/write_marketplace.py
python3 .maintainer/release/publish_all_skills.py --target index --skip-verify

echo "Done. Install: npx skills add PrunaAI/pruna-skills@pruna -y"
echo "         Or:    npx skills add PrunaAI/pruna-skills@<name> -y"
