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
