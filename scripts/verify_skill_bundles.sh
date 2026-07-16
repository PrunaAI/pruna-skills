#!/usr/bin/env bash
# Fail if plugins/ differs from a fresh bundle (sources + manifests are stale).
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${REPO_ROOT}"

if [[ ! -d plugins ]]; then
  echo "plugins/ missing — run ./scripts/bundle_all_skills.sh" >&2
  exit 1
fi

SNAPSHOT=$(mktemp -d)
trap 'rm -rf "$SNAPSHOT"' EXIT
cp -a plugins "$SNAPSHOT/before"
if [[ -f .claude-plugin/marketplace.json ]]; then
  cp .claude-plugin/marketplace.json "$SNAPSHOT/marketplace.before"
fi

./scripts/bundle_all_skills.sh >/dev/null

if diff -rq "$SNAPSHOT/before" plugins >/dev/null 2>&1; then
  echo "plugin bundles match sources (plugins/ is current)"
else
  echo "plugins/ is stale — run ./scripts/bundle_all_skills.sh and commit:" >&2
  diff -rq "$SNAPSHOT/before" plugins >&2 || true
  exit 1
fi

if [[ -f "$SNAPSHOT/marketplace.before" ]]; then
  if ! diff -q "$SNAPSHOT/marketplace.before" .claude-plugin/marketplace.json >/dev/null 2>&1; then
    echo ".claude-plugin/marketplace.json is stale — run ./scripts/bundle_all_skills.sh and commit" >&2
    diff -u "$SNAPSHOT/marketplace.before" .claude-plugin/marketplace.json >&2 || true
    exit 1
  fi
fi

python3 - <<'PY'
import json
import re
import sys
from pathlib import Path

repo = Path(".")
plugins_root = repo / "plugins"
marketplace_path = repo / ".claude-plugin" / "marketplace.json"
SUITE_PLUGIN = "pruna-full"
double_paren_re = re.compile(r"\]\(\(")
bad: list[str] = []

if not marketplace_path.is_file():
    bad.append(f"missing {marketplace_path}")

plugin_dirs = sorted(
    p for p in plugins_root.iterdir()
    if p.is_dir() and not p.name.startswith("_") and p.name != "publish-index.json"
)

for plugin_dir in plugin_dirs:
    name = plugin_dir.name
    manifest_dir = plugin_dir / ".claude-plugin"
    manifest = manifest_dir / "plugin.json"
    primary = plugin_dir / "skills" / name / "SKILL.md"

    if not manifest.is_file():
        bad.append(f"{plugin_dir}: missing .claude-plugin/plugin.json")
    else:
        extra = [p.name for p in manifest_dir.iterdir() if p.name != "plugin.json"]
        if extra:
            bad.append(f"{manifest_dir}: unexpected files {extra!r} (only plugin.json allowed)")

    for clawhub_file in ("openclaw.plugin.json", "package.json"):
        if not (plugin_dir / clawhub_file).is_file():
            bad.append(f"{plugin_dir}: missing {clawhub_file} (ClawHub bundle-plugin publish)")

    if not primary.is_file():
        if name == SUITE_PLUGIN:
            skills_dir = plugin_dir / "skills"
            if not skills_dir.is_dir() or not any(skills_dir.iterdir()):
                bad.append(f"{plugin_dir}: suite plugin has empty skills/")
        else:
            bad.append(f"{plugin_dir}: missing skills/{name}/SKILL.md")

    if name != SUITE_PLUGIN:
        manifest_json = plugin_dir / "skills" / name / "skill.manifest.json"
        if manifest_json.is_file():
            deps = json.loads(manifest_json.read_text()).get("tool_skills") or []
            for dep in deps:
                dep_skill = plugin_dir / "skills" / dep / "SKILL.md"
                if not dep_skill.is_file():
                    bad.append(f"{plugin_dir}: tool_skills missing embedded skill {dep}")

        primary_dir = plugin_dir / "skills" / name
        if primary_dir.is_dir():
            for md in sorted(primary_dir.rglob("*.md")):
                if double_paren_re.search(md.read_text()):
                    bad.append(f"{md}: malformed link (](()")
            skill_md = primary_dir / "SKILL.md"
            if skill_md.exists():
                for target in re.findall(r"\]\((\./[^)#]+)\)", skill_md.read_text()):
                    if not (skill_md.parent / target).resolve().exists():
                        bad.append(f"{skill_md}: missing -> {target}")

if marketplace_path.is_file():
    marketplace = json.loads(marketplace_path.read_text())
    entries = marketplace.get("plugins") or []
    seen = {p["name"]: p for p in entries}
    for plugin_dir in plugin_dirs:
        name = plugin_dir.name
        if name not in seen:
            bad.append(f"marketplace.json missing plugin entry for {name}")
            continue
        source = seen[name].get("source", "")
        expected = f"./{name}"
        if source not in (expected, name):
            bad.append(f"marketplace.json: {name} source={source!r}, expected {expected!r}")
    plugin_root = (marketplace.get("metadata") or {}).get("pluginRoot", ".")
    root_dir = (repo / plugin_root.lstrip("./")) if plugin_root not in (".", "./") else repo
    for entry in entries:
        src = entry.get("source", "").lstrip("./")
        if not (root_dir / src).is_dir():
            bad.append(f"marketplace.json: source {entry.get('source')!r} does not exist")

if bad:
    print("Plugin bundle checks failed:", file=sys.stderr)
    print("\n".join(bad), file=sys.stderr)
    sys.exit(1)

print(f"Plugin layout OK ({len(plugin_dirs)} plugins)")
PY
