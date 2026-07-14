#!/usr/bin/env bash
# Bundle a portable skill into a target directory (used by bundle_skill.sh; not end-user install)
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILL="${1:?Usage: install_skill.sh <skill-name> [--target DIR] [--with-examples] [--mine]}"
TARGET="${HOME}/.cursor/skills"
WITH_EXAMPLES=0
USE_MINE=0

shift
while [[ $# -gt 0 ]]; do
  case "$1" in
    --target) TARGET="$2"; shift 2 ;;
    --with-examples) WITH_EXAMPLES=1; shift ;;
    --mine) USE_MINE=1; shift ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

SKILL_SRC=""
if [[ "${USE_MINE}" -eq 1 ]]; then
  SEARCH_BASES=(
    "${REPO_ROOT}/.mine/guides/workflows/launches"
  )
else
  SEARCH_BASES=(
    "${REPO_ROOT}/workflows/router"
    "${REPO_ROOT}/workflows/core"
    "${REPO_ROOT}/workflows/verticals"
    "${REPO_ROOT}/tools/image"
    "${REPO_ROOT}/tools/video"
    "${REPO_ROOT}/tools/audio"
    "${REPO_ROOT}/guides/prompting"
    "${REPO_ROOT}/guides/quality"
    "${REPO_ROOT}/guides/routing"
  )
fi
for base in "${SEARCH_BASES[@]}"; do
  if [[ -f "${base}/${SKILL}/SKILL.md" ]]; then
    SKILL_SRC="${base}/${SKILL}"
    break
  fi
done
MANIFEST="${SKILL_SRC}/skill.manifest.json"
if [[ -z "${SKILL_SRC}" || ! -f "${SKILL_SRC}/SKILL.md" ]]; then
  if [[ "${USE_MINE}" -eq 1 ]]; then
    echo "Skill not found: ${SKILL} (searched .mine/guides/workflows/launches/)" >&2
  else
    echo "Skill not found: ${SKILL} (searched workflows/, tools/, guides/)" >&2
    echo "Pruna-internal launch skills: install_skill.sh ${SKILL} --mine" >&2
  fi
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
for f in SKILL.md README-INSTALL.md example-prompt.md examples.md replace-beats.md animate-beats.md prompt-templates.md lyrics-and-cuts.md skill.manifest.json; do
  [[ -f "${SKILL_SRC}/${f}" ]] && cp "${SKILL_SRC}/${f}" "${DEST}/"
done

# Templates from skill templates/
if [[ -d "${SKILL_SRC}/templates" ]]; then
  cp -R "${SKILL_SRC}/templates/." "${DEST}/templates/"
fi
if [[ "${USE_MINE}" -eq 1 ]]; then
  for ex_base in "${REPO_ROOT}/.mine/examples/workflows/launches"; do
    [[ -d "${ex_base}/${SKILL}" ]] || continue
    for f in "${ex_base}/${SKILL}"/*.json "${ex_base}/${SKILL}"/*.md; do
      [[ -f "$f" ]] || continue
      case "$(basename "$f")" in
        example-prompt.md) cp "$f" "${DEST}/" ;;
        *.json) cp "$f" "${DEST}/templates/" 2>/dev/null || true ;;
      esac
    done
  done
fi

# References from manifest (search references/{shared,image,video,audio,workflows}/)
python3 - <<PY
import json, shutil
from pathlib import Path
repo = Path("${REPO_ROOT}")
dest = Path("${DEST}")
refs_roots = [repo / "references"]
if ${USE_MINE}:
    refs_roots.append(repo / ".mine" / "references")
manifest = json.loads(Path("${MANIFEST}").read_text())
for name in manifest.get("references", []):
    src = None
    for refs_root in refs_roots:
        candidate = refs_root / name
        if candidate.exists():
            src = candidate
            break
    if src is None:
        matches = []
        for refs_root in refs_roots:
            matches.extend(p for p in refs_root.rglob(Path(name).name) if p.is_file())
        src = matches[0] if matches else None
    if src and src.is_file():
        out = dest / "references" / src.name
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, out)
    else:
        print(f"warn: missing reference {name}")
PY

# Scripts: skill scripts/ + shared from manifest
SHARED="${REPO_ROOT}/workflows/_shared/scripts"
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
    -e 's|(\.\./\.\./_shared/scripts/|(\./scripts/|g' \
    -e 's|(\.\./_shared/scripts/|(\./scripts/|g' \
    -e 's|catalog/workflows/_shared/scripts/|scripts/|g' \
    -e 's|(\.\./\.\./\.\./catalog/references/|(\./references/|g' \
    -e 's|(\.\./\.\./catalog/references/|(\./references/|g' \
    -e 's|(\.\./catalog/references/|(\./references/|g' \
    -e 's|(\./catalog/references/|(\./references/|g' \
    -e 's|(\(\.\./\)\{1,\}references/|(./references/|g' \
    -e 's|(\./references/image/|(./references/|g' \
    -e 's|(\(\.\./\)\{1,\}examples/shared/realistic-persona/example-prompt.md|(./example-prompt.md|g' \
    -e 's|(\(\.\./\)\{1,\}examples/tools/p-image-try-on/example-prompt.md|(./example-prompt.md|g' \
    -e 's|(\(\.\./\)\{1,\}examples/tools/p-image-ideogram/example-prompt.md|(./example-prompt.md|g' \
    -e 's|(\.\./\.\./references/|(\./references/|g' \
    -e 's|(\.\./references/|(\./references/|g' \
    -e 's|(\./references/video/|(\./references/|g' \
    -e 's|(\./references/workflows/|(\./references/|g' \
    -e 's|(\./references/audio/|(\./references/|g' \
    -e 's|(\./references/shared/|(\./references/|g' \
    -e 's|(\./catalog/references/video/|(\./references/|g' \
    -e 's|(\./catalog/references/workflows/|(\./references/|g' \
    -e 's|(\./catalog/references/audio/|(\./references/|g' \
    -e 's|(\./catalog/references/shared/|(\./references/|g' \
    -e 's|(\.\./\.\./\.\./scripts/|(\./scripts/|g' \
    -e 's|(\.\./\.\./scripts/|(\./scripts/|g' \
    -e 's|(\../../../catalog/tools/|(\./|g' \
    -e 's|(\../../../tools/|(\./|g' \
    -e 's|]((./|](./|g' \
    "$f" 2>/dev/null || sed -i \
    -e 's|(\.\./\.\./_shared/scripts/|(\./scripts/|g' \
    -e 's|(\.\./_shared/scripts/|(\./scripts/|g' \
    -e 's|catalog/workflows/_shared/scripts/|scripts/|g' \
    -e 's|(\.\./\.\./\.\./catalog/references/|(\./references/|g' \
    -e 's|(\.\./\.\./catalog/references/|(\./references/|g' \
    -e 's|(\.\./catalog/references/|(\./references/|g' \
    -e 's|(\./catalog/references/|(\./references/|g' \
    -e 's|(\(\.\./\)\{1,\}references/|(./references/|g' \
    -e 's|(\./references/image/|(./references/|g' \
    -e 's|(\(\.\./\)\{1,\}examples/shared/realistic-persona/example-prompt.md|(./example-prompt.md|g' \
    -e 's|(\(\.\./\)\{1,\}examples/tools/p-image-try-on/example-prompt.md|(./example-prompt.md|g' \
    -e 's|(\(\.\./\)\{1,\}examples/tools/p-image-ideogram/example-prompt.md|(./example-prompt.md|g' \
    -e 's|(\.\./\.\./references/|(\./references/|g' \
    -e 's|(\.\./references/|(\./references/|g' \
    -e 's|(\./references/video/|(\./references/|g' \
    -e 's|(\./references/workflows/|(\./references/|g' \
    -e 's|(\./references/audio/|(\./references/|g' \
    -e 's|(\./references/shared/|(\./references/|g' \
    -e 's|(\./catalog/references/video/|(\./references/|g' \
    -e 's|(\./catalog/references/workflows/|(\./references/|g' \
    -e 's|(\./catalog/references/audio/|(\./references/|g' \
    -e 's|(\./catalog/references/shared/|(\./references/|g' \
    -e 's|(\.\./\.\./\.\./scripts/|(\./scripts/|g' \
    -e 's|(\.\./\.\./scripts/|(\./scripts/|g' \
    -e 's|(\../../../catalog/tools/|(\./|g' \
    -e 's|(\../../../tools/|(\./|g' \
    -e 's|]((./|](./|g' \
    "$f"
done

echo "Bundled ${SKILL} -> ${DEST}"
echo "  pip install -r ${DEST}/scripts/requirements.txt  # when present"
echo "  Requires: PRUNA_API_KEY, curl, ffmpeg (video workflows)"
