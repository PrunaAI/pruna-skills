#!/usr/bin/env bash
# Install a portable workflow skill bundle to ~/.cursor/skills/ (or --target DIR)
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILL="${1:?Usage: install_skill.sh <skill-name> [--target DIR] [--with-examples]}"
TARGET="${HOME}/.cursor/skills"
WITH_EXAMPLES=0

shift
while [[ $# -gt 0 ]]; do
  case "$1" in
    --target) TARGET="$2"; shift 2 ;;
    --with-examples) WITH_EXAMPLES=1; shift ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

SKILL_SRC="${REPO_ROOT}/guides/workflows/${SKILL}"
MANIFEST="${SKILL_SRC}/skill.manifest.json"
if [[ ! -f "${SKILL_SRC}/SKILL.md" ]]; then
  echo "Skill not found: ${SKILL_SRC}/SKILL.md" >&2
  exit 1
fi
if [[ ! -f "${MANIFEST}" ]]; then
  echo "Missing manifest: ${MANIFEST}" >&2
  exit 1
fi

DEST="${TARGET}/${SKILL}"
rm -rf "${DEST}"
mkdir -p "${DEST}/scripts" "${DEST}/references" "${DEST}/templates"

# Skill markdown + beat docs
for f in SKILL.md README-INSTALL.md examples.md replace-beats.md animate-beats.md skill.manifest.json; do
  [[ -f "${SKILL_SRC}/${f}" ]] && cp "${SKILL_SRC}/${f}" "${DEST}/"
done

# Templates from skill templates/ or examples/workflows/
if [[ -d "${SKILL_SRC}/templates" ]]; then
  cp -R "${SKILL_SRC}/templates/." "${DEST}/templates/"
fi
EXAMPLES="${REPO_ROOT}/examples/workflows/${SKILL}"
if [[ -d "${EXAMPLES}" ]]; then
  for f in "${EXAMPLES}"/*.json "${EXAMPLES}"/*.md; do
    [[ -f "$f" ]] || continue
    case "$(basename "$f")" in
      example-prompt.md) cp "$f" "${DEST}/" ;;
      *.json) cp "$f" "${DEST}/templates/" 2>/dev/null || true ;;
    esac
  done
fi

# References from manifest
python3 - <<PY
import json, shutil
from pathlib import Path
repo = Path("${REPO_ROOT}")
dest = Path("${DEST}")
manifest = json.loads(Path("${MANIFEST}").read_text())
for name in manifest.get("references", []):
    src = repo / "references" / name
    if src.exists():
        shutil.copy2(src, dest / "references" / name)
    else:
        print(f"warn: missing reference {src}")
PY

# Scripts: skill scripts/ + shared from manifest
SHARED="${REPO_ROOT}/guides/workflows/_shared/scripts"
python3 - <<PY
import json, shutil
from pathlib import Path
repo = Path("${REPO_ROOT}")
skill_src = Path("${SKILL_SRC}")
dest = Path("${DEST}")
shared = Path("${SHARED}")
manifest = json.loads(Path("${MANIFEST}").read_text())
scripts = manifest.get("scripts", {})
for name in scripts.get("core", []) + scripts.get("shared", []):
    for base in (skill_src / "scripts", shared):
        src = base / name
        if src.exists():
            shutil.copy2(src, dest / "scripts" / name)
            break
    else:
        print(f"warn: missing script {name}")
if ${WITH_EXAMPLES}:
    for name in scripts.get("optional", []):
        src = skill_src / "scripts" / name
        if src.exists():
            shutil.copy2(src, dest / "scripts" / name)
PY

# Rewrite reference links in markdown for portable bundle
find "${DEST}" -name '*.md' -print0 | while IFS= read -r -d '' f; do
  sed -i '' \
    -e 's|(\../../../references/|(\./references/|g' \
    -e 's|(\../../references/|(\./references/|g' \
    -e 's|(\../../../scripts/|(\./scripts/|g' \
    -e 's|(\../../../tools/|(\../../../tools/|g' \
    "$f" 2>/dev/null || sed -i \
    -e 's|(\../../../references/|(\./references/|g' \
    -e 's|(\../../references/|(\./references/|g' \
    -e 's|(\../../../scripts/|(\./scripts/|g' \
    "$f"
done

echo "Installed ${SKILL} -> ${DEST}"
echo "  pip install -r ${DEST}/scripts/requirements.txt  # when present"
echo "  Requires: PRUNA_API_KEY, curl, ffmpeg (video workflows)"
