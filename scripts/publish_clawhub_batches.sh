#!/usr/bin/env bash
# Publish ClawHub skills in batches (registry rate limit ~5/hour).
# Usage: ./scripts/publish_clawhub_batches.sh [logfile]
set -uo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${REPO_ROOT}"

LOG="${1:-${REPO_ROOT}/output/clawhub-publish-batch.log}"
mkdir -p "$(dirname "$LOG")"
BATCH_SIZE="${CLAWHUB_BATCH_SIZE:-5}"
BATCH_DELAY="${CLAWHUB_BATCH_DELAY_S:-3600}"

log() { echo "$@" | tee -a "$LOG"; }

mapfile -t ALL_SKILLS < <(
  python3 - <<'PY'
import json
from pathlib import Path
idx = Path("plugins/publish-index.json")
data = json.loads(idx.read_text())
for s in data.get("skills", []):
    print(s["name"])
PY
)

if [[ "${#ALL_SKILLS[@]}" -eq 0 ]]; then
  echo "No skills in plugins/publish-index.json — run bundle first" >&2
  exit 1
fi

BATCHES=()
batch=()
for skill in "${ALL_SKILLS[@]}"; do
  batch+=("${skill}")
  if [[ "${#batch[@]}" -ge "${BATCH_SIZE}" ]]; then
    BATCHES+=("${batch[*]}")
    batch=()
  fi
done
[[ "${#batch[@]}" -gt 0 ]] && BATCHES+=("${batch[*]}")

log "=== ClawHub batch publish started $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
log "Skills: ${#ALL_SKILLS[@]} in ${#BATCHES[@]} batches (size ${BATCH_SIZE}, delay ${BATCH_DELAY}s)"
if [[ -n "${CLAWHUB_INITIAL_DELAY_S:-}" ]] && [[ "${CLAWHUB_INITIAL_DELAY_S}" -gt 0 ]]; then
  log "Initial delay ${CLAWHUB_INITIAL_DELAY_S}s..."
  sleep "${CLAWHUB_INITIAL_DELAY_S}"
fi
clawhub whoami 2>&1 | tee -a "$LOG" || log "(clawhub whoami failed — run clawhub login)"

n=${#BATCHES[@]}
start="${CLAWHUB_START_BATCH:-1}"
i=0
for batch in "${BATCHES[@]}"; do
  i=$((i + 1))
  if [[ "$i" -lt "$start" ]]; then
    log "Skipping batch ${i}/${n} (CLAWHUB_START_BATCH=${start})"
    continue
  fi
  log ""
  log "=== Batch ${i}/${n} $(date -u +%Y-%m-%dT%H:%M:%SZ): ${batch} ==="
  args=(--execute --target clawhub --skip-verify)
  for skill in ${batch}; do
    args+=(--skill "${skill}")
  done
  if ./scripts/publish_all_skills.sh "${args[@]}" >>"$LOG" 2>&1; then
    log "Batch ${i} OK"
  else
    log "WARN: batch ${i} had failures (see log)"
  fi
  if [[ "$i" -lt "$n" ]]; then
    if date -v+"${BATCH_DELAY}S" >/dev/null 2>&1; then
      next_at=$(date -u -v+"${BATCH_DELAY}S" +%Y-%m-%dT%H:%M:%SZ)
    else
      next_at=$(date -u -d "+${BATCH_DELAY} seconds" +%Y-%m-%dT%H:%M:%SZ)
    fi
    log "Sleeping ${BATCH_DELAY}s — next batch ~${next_at}"
    sleep "${BATCH_DELAY}"
  fi
done

log ""
log "=== ClawHub batch publish finished $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
