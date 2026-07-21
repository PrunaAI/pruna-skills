#!/usr/bin/env bash
# Release pipeline: version → bundle → verify → validate → publish (dry-run default).
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "${REPO_ROOT}"

VERSION="${1:?Usage: release.sh <version> [--execute]}"
EXECUTE=0
[[ "${2:-}" == "--execute" ]] && EXECUTE=1

echo "==> Set VERSION=${VERSION}"
echo "${VERSION}" > VERSION
python3 .maintainer/sync_skill_versions.py
./.maintainer/bundle_all_skills.sh
./.maintainer/validate_release.sh

TAG="skills-v${VERSION}"
if [[ "${EXECUTE}" -eq 0 ]]; then
  echo ""
  echo "Dry run OK. To publish:"
  echo "  git add -A && git commit -m \"[release] skills v${VERSION}\""
  echo "  git tag ${TAG} && git push origin main && git push origin ${TAG}"
  echo "  ./.maintainer/release/create_github_release.sh ${VERSION}"
  echo "  ./.maintainer/release/publish_all_skills.sh --execute --target clawhub,index"
  exit 0
fi

./.maintainer/release/publish_all_skills.sh --execute --target clawhub,index
echo ""
echo "Published. Tag, push, and GitHub Release if not done by CI:"
echo "  git tag ${TAG} && git push origin ${TAG}"
echo "  ./.maintainer/release/create_github_release.sh ${VERSION}"
