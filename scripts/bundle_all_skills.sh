#!/usr/bin/env bash
# Bundle all public skills into skills/ for npx skills add ./skills
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${REPO_ROOT}"

python3 scripts/sync_skill_versions.py

TOOLS=(
  p-image p-image-edit p-image-upscale p-image-try-on
  p-video p-video-avatar p-video-animate p-video-replace
  gemini-3.1-flash-tts music-2.5 stable-audio-2.5 whisperx
)
ROUTER=(pruna-generative-pipeline pruna-run requesting-generation-feedback)
CORE=(image-to-video narrated-multi-scene visual-transition-reel avatar-single-scene avatar-multi-scene)
VERTICALS=(interactive-explainer music-video illustrated-story-reel)

rm -rf skills
mkdir -p skills

for skill in "${TOOLS[@]}" "${ROUTER[@]}" "${CORE[@]}" "${VERTICALS[@]}"; do
  echo "==> ${skill}"
  ./scripts/bundle_skill.sh "${skill}"
done

python3 scripts/publish_all_skills.py --target index --skip-verify

python3 - <<'PY'
import json
from pathlib import Path

repo = Path(".")
version = (repo / "VERSION").read_text().strip()
catalog = {"package": "pruna-ai-content-generation-skills", "version": version, "skills": []}
for skill_dir in sorted((repo / "skills").iterdir()):
    if not skill_dir.is_dir() or skill_dir.name.startswith("_"):
        continue
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        continue
    text = skill_md.read_text()
    name = skill_dir.name
    desc = ""
    if text.startswith("---"):
        fm = text.split("---", 2)[1]
        for line in fm.splitlines():
            if line.startswith("description:"):
                desc = line.split(":", 1)[1].strip()
                break
    catalog["skills"].append({"name": name, "version": version, "description": desc})
(repo / "skills" / "catalog.json").write_text(json.dumps(catalog, indent=2) + "\n")
print(f"Wrote skills/catalog.json ({len(catalog['skills'])} skills)")
PY

cat > skills/README.md <<'EOF'
# Portable skill bundles (generated)

**Do not edit files here by hand.** This tree is rebuilt from canonical sources:

| Source | Examples |
|--------|----------|
| `catalog/tools/image/`, `catalog/tools/video/`, `catalog/tools/audio/` | `p-image`, `p-video-replace`, `music-2.5` |
| `catalog/workflows/router/` | `pruna-run`, `pruna-generative-pipeline` |
| `catalog/workflows/core/` | `image-to-video`, `avatar-multi-scene` |
| `catalog/workflows/verticals/` | `interactive-explainer`, `music-video` |
| `catalog/references/` | Shared docs copied per `skill.manifest.json` |
| `catalog/examples/` | Starter prompts (bundled into `skills/` via `bundle_skill.sh`) |
| `catalog/workflows/_shared/scripts/` | Runners referenced in manifests |

Each workflow’s `tool_skills` (in `skill.manifest.json`) is bundled as:

| File | Format | Package manager |
|------|--------|-----------------|
| `SKILL.md` → `depends:` | YAML sibling names | `npx skills` |
| `apm.yml` | YAML full repo paths | APM |
| `pspm.json` | JSON `githubDependencies` | PSPM |
| `skill.deps.json` | JSON canonical + `resolvers` | any / future tools |

Author once in `catalog/**/skill.manifest.json` → `./scripts/write_dep_manifests.py` at bundle time.

## Regenerate

```bash
./scripts/bundle_all_skills.sh          # all public skills
./scripts/bundle_skill.sh <name>        # one skill
./scripts/verify_skill_bundles.sh       # fail if skills/ is stale vs sources
```

Maintainers: run `bundle_all_skills.sh` after source changes, then commit `skills/` so installs from GitHub stay current.

## Install

```bash
npx skills add ./skills --list
npx skills add ./skills --skill p-image --agent cursor -y
npx skills add ./skills --skill avatar-multi-scene --agent cursor -y
```

Other package managers (APM, PSPM, OpenClaw): see [README.md](../README.md#install-skills) and [consumer-manifests](../catalog/examples/consumer-manifests/README.md).
EOF

echo "Done. Install: npx skills add ./skills --skill <name>"
