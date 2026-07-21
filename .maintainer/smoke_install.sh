#!/usr/bin/env bash
# Discover + temp-dir install smoke for npx skills (file layout only).
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
grep -q "image-prompting" "${TMP}/skills-list.txt"
grep -q "pruna" "${TMP}/skills-list.txt"
echo "skills list OK"

echo "==> temp install p-image (skills, --copy)"
mkdir -p "${TMP}/proj"
cd "${TMP}/proj"
npx --yes skills add "${REPO_ROOT}/skills/image" --skill p-image -y --copy >"${TMP}/install-skill.txt" 2>&1
if ! find . -path '*p-image*' -name SKILL.md 2>/dev/null | head -1 | grep -q .; then
  echo "FAIL: p-image SKILL.md not found after install" >&2
  cat "${TMP}/install-skill.txt" >&2
  exit 1
fi
echo "skills install OK"

cd "${REPO_ROOT}"
echo "smoke_install: OK"
