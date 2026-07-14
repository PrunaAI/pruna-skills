#!/usr/bin/env bash
# Bundle all public skills into plugins/ for marketplace and npx skills add
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${REPO_ROOT}"

python3 scripts/sync_skill_versions.py

TOOLS=(
  p-image p-image-ideogram p-image-edit p-image-upscale p-image-try-on
  p-video p-video-avatar p-video-animate p-video-replace
  gemini-3.1-flash-tts music-2.5 stable-audio-2.5 whisperx
)
ROUTER=(pruna-generative-pipeline pruna-run requesting-generation-feedback)
CORE=(image-to-video narrated-multi-scene visual-transition-reel avatar-single-scene avatar-multi-scene)
VERTICALS=(interactive-explainer music-video illustrated-story-reel)
GUIDES=(generation-diversity generation-quality-checklists recipe-catalog)

STAGING=$(mktemp -d)
trap 'rm -rf "$STAGING"' EXIT
mkdir -p "${STAGING}"

for skill in "${TOOLS[@]}" "${ROUTER[@]}" "${CORE[@]}" "${VERTICALS[@]}" "${GUIDES[@]}"; do
  echo "==> ${skill}"
  ./scripts/install_skill.sh "${skill}" --target "${STAGING}"
done

python3 scripts/build_plugins.py --staging "${STAGING}"
python3 scripts/write_skills_sh_json.py
python3 scripts/write_readme_skills_section.py

python3 scripts/publish_all_skills.py --target index --skip-verify

echo "Done. Install: /plugin install <name>@pruna-skills or npx skills add PrunaAI/pruna-skills@<name> -y"
