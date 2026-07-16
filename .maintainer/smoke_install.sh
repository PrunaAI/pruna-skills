#!/usr/bin/env bash
# Discover + temp-dir install smoke for npx skills / npx plugins (file layout only).
# Uses local paths (CI). Public docs use PrunaAI/pruna-skills@<name> from GitHub.
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${REPO_ROOT}"

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

echo "==> npx skills list (local repo)"
npx --yes skills add "${REPO_ROOT}" -l >"${TMP}/skills-list.txt" 2>&1 || {
  cat "${TMP}/skills-list.txt" >&2
  exit 1
}
grep -q "p-image" "${TMP}/skills-list.txt"
grep -q "music-video" "${TMP}/skills-list.txt"
echo "skills list OK"

echo "==> npx plugins discover (local repo)"
npx --yes plugins discover "${REPO_ROOT}" >"${TMP}/plugins-discover.txt" 2>&1 || true
if ! grep -qE "p-image|music-video|pruna-full|pruna-skills" "${TMP}/plugins-discover.txt"; then
  npx --yes plugins discover "${REPO_ROOT}/plugins" >"${TMP}/plugins-discover.txt" 2>&1 || true
fi
if ! grep -qE "p-image|music-video|pruna-full" "${TMP}/plugins-discover.txt"; then
  echo "WARN: plugins discover output opaque; checking marketplace.json"
  test -f .claude-plugin/marketplace.json
  python3 -c "import json; m=json.load(open('.claude-plugin/marketplace.json')); assert any(p['name']=='p-image' for p in m['plugins'])"
  echo "marketplace.json OK"
else
  echo "plugins discover OK"
fi

echo "==> temp install p-image (skills, --copy)"
mkdir -p "${TMP}/proj"
cd "${TMP}/proj"
# Local path form (GitHub @name form is for remote installs)
npx --yes skills add "${REPO_ROOT}/plugins/p-image/skills" --skill p-image -y --copy >"${TMP}/install-skill.txt" 2>&1
if ! find . -path '*p-image*' -name SKILL.md 2>/dev/null | head -1 | grep -q .; then
  echo "FAIL: p-image SKILL.md not found after install" >&2
  cat "${TMP}/install-skill.txt" >&2
  exit 1
fi
echo "skills install OK"

cd "${REPO_ROOT}"
echo "smoke_install: OK"
