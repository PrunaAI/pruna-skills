#!/usr/bin/env bash
# Release pipeline: version → bundle → verify → validate → publish (dry-run default).
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${REPO_ROOT}"

VERSION="${1:?Usage: release.sh <version> [--execute]}"
EXECUTE=0
[[ "${2:-}" == "--execute" ]] && EXECUTE=1

echo "==> Set VERSION=${VERSION}"
echo "${VERSION}" > VERSION
python3 scripts/sync_skill_versions.py
./scripts/bundle_all_skills.sh
./scripts/validate_release.sh

TAG="skills-v${VERSION}"
if [[ "${EXECUTE}" -eq 0 ]]; then
  echo ""
  echo "Dry run OK. To publish:"
  echo "  git add -A && git commit -m \"[release] skills v${VERSION}\""
  echo "  git tag ${TAG} && git push origin main && git push origin ${TAG}"
  echo "  ./scripts/publish_all_skills.sh --execute --target clawhub,clawhub-plugins,index"
  exit 0
fi

./scripts/publish_all_skills.sh --execute --target clawhub,clawhub-plugins,index
echo ""
echo "Published. Tag and push if not done by CI:"
echo "  git tag ${TAG} && git push origin ${TAG}"
