#!/usr/bin/env bash
# Batch ClawHub skill publish (one skill at a time) from publish-index.json.
# Usage: publish_clawhub_batches.sh [--execute]
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "${REPO_ROOT}"

EXECUTE=0
[[ "${1:-}" == "--execute" ]] && EXECUTE=1

IDX=".maintainer/publish-index.json"
if [[ ! -f "${IDX}" ]]; then
  echo "No ${IDX} — run make bundle first" >&2
  exit 1
fi

mapfile -t SKILLS < <(python3 -c "import json; print('\n'.join(s['name'] for s in json.load(open('${IDX}'))['skills']))")
echo "Publishing ${#SKILLS[@]} skills to ClawHub$([[ ${EXECUTE} -eq 1 ]] && echo '' || echo ' (dry-run)')…"

ARGS=(--target clawhub)
[[ ${EXECUTE} -eq 1 ]] && ARGS+=(--execute)

failures=0
for name in "${SKILLS[@]}"; do
  echo "==> ${name}"
  if ! python3 .maintainer/release/publish_all_skills.py "${ARGS[@]}" --skill "${name}" --skip-verify; then
    failures=$((failures + 1))
  fi
done

[[ ${failures} -eq 0 ]] || exit 1
echo "publish_clawhub_batches: OK"
