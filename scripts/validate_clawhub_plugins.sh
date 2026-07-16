#!/usr/bin/env bash
# Run clawhub package validate on every plugins/<name>/ (OpenClaw Plugin Inspector).
# Catches package-plugin-api-compat-missing / package-openclaw-entry-missing before publish.
# Docs: https://docs.openclaw.ai/clawhub/plugin-validation-fixes
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${REPO_ROOT}"

if ! command -v clawhub >/dev/null 2>&1; then
  echo "clawhub CLI not found — skipping package validate (install or use npx clawhub@latest)" >&2
  exit 0
fi

fail=0
ok=0
shopt -s nullglob
for d in plugins/*/; do
  name="$(basename "$d")"
  [[ "$name" == _* ]] && continue
  [[ -f "${d}package.json" ]] || continue
  out="$(clawhub package validate "$d" 2>&1)" || true
  # Drop inspector report dirs so they do not dirty the tree / stale-check
  rm -rf "${d}reports"
  if echo "$out" | grep -q 'Plugin Inspector: PASS'; then
    if echo "$out" | grep -qE 'Warnings: [1-9]|Breakages: [1-9]'; then
      echo "WARN $name (PASS with findings)" >&2
      echo "$out" | head -30 >&2
      fail=$((fail + 1))
    else
      echo "PASS $name"
      ok=$((ok + 1))
    fi
  else
    echo "FAIL $name" >&2
    echo "$out" | head -40 >&2
    fail=$((fail + 1))
  fi
done

echo "clawhub package validate: ok=$ok fail=$fail"
[[ "$fail" -eq 0 ]]
