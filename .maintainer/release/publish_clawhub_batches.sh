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

ARGS=(--target clawhub --skip-verify)
[[ ${EXECUTE} -eq 1 ]] && ARGS+=(--execute)

failures=0
count=0
while IFS= read -r name; do
  [[ -z "${name}" ]] && continue
  count=$((count + 1))
  echo "==> ${name}"
  if ! python3 .maintainer/release/publish_all_skills.py "${ARGS[@]}" --skill "${name}"; then
    failures=$((failures + 1))
  fi
done < <(python3 -c "import json; print('\n'.join(s['name'] for s in json.load(open('${IDX}'))['skills']))")

echo "publish_clawhub_batches: ${count} skills, ${failures} failures$([[ ${EXECUTE} -eq 1 ]] || echo ' (dry-run)')"
[[ ${failures} -eq 0 ]] || exit 1
