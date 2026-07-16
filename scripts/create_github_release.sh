#!/usr/bin/env bash
# Create (or update notes for) a GitHub Release from CHANGELOG.md for tag skills-v<VERSION>.
# Usage: ./scripts/create_github_release.sh <version> [--draft]
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${REPO_ROOT}"

VERSION="${1:?Usage: create_github_release.sh <version> [--draft]}"
DRAFT=0
[[ "${2:-}" == "--draft" ]] && DRAFT=1

TAG="skills-v${VERSION}"
CHANGELOG="${REPO_ROOT}/CHANGELOG.md"
[[ -f "${CHANGELOG}" ]] || { echo "missing CHANGELOG.md" >&2; exit 1; }

NOTES="$(python3 - "${VERSION}" "${CHANGELOG}" <<'PY'
import re, sys
version, path = sys.argv[1], sys.argv[2]
text = open(path, encoding="utf-8").read()
m = re.search(rf"## \[{re.escape(version)}\][^\n]*\n(.*?)(?=\n## \[|\Z)", text, re.S)
if not m:
    sys.stderr.write(f"No CHANGELOG section for [{version}]\n")
    sys.exit(1)
print(m.group(0).strip())
PY
)"

TMP="$(mktemp)"
trap 'rm -f "${TMP}"' EXIT
printf '%s\n' "${NOTES}" > "${TMP}"

ARGS=(release create "${TAG}" --title "skills v${VERSION}" --notes-file "${TMP}")
[[ "${DRAFT}" -eq 1 ]] && ARGS+=(--draft)

if gh release view "${TAG}" >/dev/null 2>&1; then
  echo "==> Release ${TAG} exists — updating notes"
  gh release edit "${TAG}" --title "skills v${VERSION}" --notes-file "${TMP}"
else
  echo "==> Creating GitHub release ${TAG}"
  gh "${ARGS[@]}"
fi

gh release view "${TAG}" --json url -q .url
