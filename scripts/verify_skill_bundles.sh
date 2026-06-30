#!/usr/bin/env bash
# Fail if skills/ differs from a fresh bundle (sources + manifests are stale).
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${REPO_ROOT}"

if [[ ! -d skills ]]; then
  echo "skills/ missing — run ./scripts/bundle_all_skills.sh" >&2
  exit 1
fi

SNAPSHOT=$(mktemp -d)
trap 'rm -rf "$SNAPSHOT"' EXIT
cp -a skills "$SNAPSHOT/before"

./scripts/bundle_all_skills.sh >/dev/null

if diff -rq "$SNAPSHOT/before" skills >/dev/null 2>&1; then
  echo "skills/ matches sources (bundles are current)"
  exit 0
fi

echo "skills/ is stale — run ./scripts/bundle_all_skills.sh and commit:" >&2
diff -rq "$SNAPSHOT/before" skills >&2 || true
exit 1
