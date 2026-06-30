# Publishing skills (v0.0.1+)

Bundled skills live in `skills/`. Version is repo [`VERSION`](../VERSION) (currently **0.0.1**), synced into every `SKILL.md` `metadata.version` and registry manifests (`pspm.json`, `apm.yml`, `skill.deps.json`).

## What “publish” means per package manager

| Channel | Upload API? | How Pruna publishes |
|---------|-------------|---------------------|
| **GitHub + `npx skills`** | No | Push `skills/` to `main`; tag `skills-v0.0.1` |
| **skills.sh** | No | Install telemetry after `npx skills add` |
| **APM** | Registry optional | Consumers `apm install PrunaAI/…/skills/<name>` from GitHub |
| **PSPM** | `pspm publish` | `PSPM_API_KEY` → registry `@pruna/<skill>` |

There is **no single API** that publishes to all channels. `./scripts/publish_all_skills.py` automates PSPM upload; GitHub tag is the source-of-truth release.

## One-time setup

```bash
# PSPM — https://pspm.dev
export PSPM_API_KEY=sk_...
```

Add the same secret to GitHub Actions (`PSPM_API_KEY`) for [`.github/workflows/publish-skills.yml`](../.github/workflows/publish-skills.yml).

## Local publish

```bash
# 1. Fresh bundles at VERSION
./scripts/bundle_all_skills.sh
./scripts/verify_skill_bundles.sh

# 2. Preview
./scripts/publish_all_skills.sh

# 3. Upload to PSPM
./scripts/publish_all_skills.sh --execute

# 4. Git release marker (manual or CI)
git tag skills-v0.0.1
git push origin skills-v0.0.1
```

Single skill:

```bash
./scripts/publish_all_skills.sh --execute --skill p-image --target pspm
```

## Generated per skill (`write_dep_manifests.py`)

| File | All skills | Workflows only |
|------|------------|----------------|
| `pspm.json` | yes (`@pruna/<name>` @ VERSION) | + `githubDependencies` |
| `SKILL.md` `depends:` | | yes |
| `apm.yml` | | yes |
| `skill.deps.json` | | yes |

## CI

On push tag `skills-v*` or manual **workflow_dispatch**, GitHub Actions runs `publish_all_skills.py --execute` when secrets are configured.

## Not automated

- **APM registry zip upload** (`apm publish`) — requires `.apm/` package layout; we ship git-installable `SKILL.md` bundles instead.
- **ClawHub / Agensi** — separate publisher accounts and review flows.
- **skills.sh “Official”** — curated by Vercel; install counts drive discovery.

See also [skill-package-managers.md](references/shared/skill-package-managers.md).
