#!/usr/bin/env bash
# Bundle a portable skill into a target directory (used by bundle_skill.sh; not end-user install)
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CATALOG="${REPO_ROOT}/catalog"
SKILL="${1:?Usage: install_skill.sh <skill-name> [--target DIR] [--with-examples] [--mine]}"
TARGET="${HOME}/.cursor/skills"
WITH_EXAMPLES=0
USE_MINE=0

# Legacy folder names → new paths under core/ or verticals/
case "${SKILL}" in
  single-scene-ai-video) SKILL=image-to-video ;;
  multi-scene-ai-video) SKILL=narrated-multi-scene ;;
  scene-transition-video) SKILL=visual-transition-reel ;;
  single-scene-avatar-video) SKILL=avatar-single-scene ;;
  multi-scene-avatar-video) SKILL=avatar-multi-scene ;;
  educational-explainer|documentary-explainer) SKILL=interactive-explainer ;;
  ai-music-video) SKILL=music-video ;;
esac

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
  EXAMPLE_BASES=(
    "${REPO_ROOT}/.mine/examples/workflows/launches"
  )
else
  SEARCH_BASES=(
    "${CATALOG}/workflows/router"
    "${CATALOG}/workflows/core"
    "${CATALOG}/workflows/verticals"
    "${CATALOG}/tools/image"
    "${CATALOG}/tools/video"
    "${CATALOG}/tools/audio"
  )
  EXAMPLE_BASES=(
    "${CATALOG}/examples/workflows/core"
    "${CATALOG}/examples/workflows/verticals"
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
    echo "Skill not found: ${SKILL} (searched .mine/catalog/workflows/launches/)" >&2
  else
    echo "Skill not found: ${SKILL} (searched catalog/workflows/{router,core,verticals}, catalog/tools/)" >&2
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
for f in SKILL.md README-INSTALL.md examples.md replace-beats.md animate-beats.md skill.manifest.json; do
  [[ -f "${SKILL_SRC}/${f}" ]] && cp "${SKILL_SRC}/${f}" "${DEST}/"
done

# Templates from skill templates/ or examples/workflows/
if [[ -d "${SKILL_SRC}/templates" ]]; then
  cp -R "${SKILL_SRC}/templates/." "${DEST}/templates/"
fi
EXAMPLES=""
for ex_base in "${EXAMPLE_BASES[@]}"; do
  if [[ -d "${ex_base}/${SKILL}" ]]; then
    EXAMPLES="${ex_base}/${SKILL}"
    break
  fi
done
if [[ -n "${EXAMPLES}" ]]; then
  for f in "${EXAMPLES}"/*.json "${EXAMPLES}"/*.md; do
    [[ -f "$f" ]] || continue
    case "$(basename "$f")" in
      example-prompt.md) cp "$f" "${DEST}/" ;;
      *.json) cp "$f" "${DEST}/templates/" 2>/dev/null || true ;;
    esac
  done
fi

# References from manifest (search references/{shared,image,video,audio,workflows}/)
python3 - <<PY
import json, shutil
from pathlib import Path
repo = Path("${REPO_ROOT}")
dest = Path("${DEST}")
refs_roots = [repo / "catalog" / "references"]
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
SHARED="${CATALOG}/workflows/_shared/scripts"
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
    -e 's|(\.\./\.\./\.\./catalog/references/|(\./references/|g' \
    -e 's|(\.\./\.\./catalog/references/|(\./references/|g' \
    -e 's|(\.\./catalog/references/|(\./references/|g' \
    -e 's|(\./catalog/references/|(\./references/|g' \
    -e 's|(\.\./\.\./\.\./references/|(\./references/|g' \
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
    "$f" 2>/dev/null || sed -i \
    -e 's|(\.\./\.\./\.\./catalog/references/|(\./references/|g' \
    -e 's|(\.\./\.\./catalog/references/|(\./references/|g' \
    -e 's|(\.\./catalog/references/|(\./references/|g' \
    -e 's|(\./catalog/references/|(\./references/|g' \
    -e 's|(\.\./\.\./\.\./references/|(\./references/|g' \
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
    "$f"
done

# Drop catalog cross-links — other skills are separate install bundles
python3 - <<'PY'
import re
from pathlib import Path
dest = Path("${DEST}")
pat = re.compile(r"\[([^\]]+)\]\([^)]*catalog/(?:tools|workflows)/[^)]+\)")
for md in dest.rglob("*.md"):
    text = md.read_text()
    new = pat.sub(r"\1", text)
    if new != text:
        md.write_text(new)
PY

# Declare tool skill deps (skills depends:, apm.yml, pspm.json, skill.deps.json)
python3 "${REPO_ROOT}/scripts/write_dep_manifests.py" \
  --manifest "${MANIFEST}" --dest "${DEST}" --skill "${SKILL}"

echo "Bundled ${SKILL} -> ${DEST}"
echo "  pip install -r ${DEST}/scripts/requirements.txt  # when present"
echo "  Requires: PRUNA_API_KEY, curl, ffmpeg (video workflows)"
