# Publishing skills (v0.0.2+)

Bundled skills live in `plugins/<name>/skills/<name>/`. Version is repo [VERSION](VERSION), synced into every `SKILL.md` `metadata.version`, plugin manifests, and registry sidecars (`apm.yml`, `skill.deps.json`).

## What “publish” means per channel

There is **no single publish API**. Each channel has its own upload or git-based flow:

| Channel | Publish | Consumers install |
|---------|---------|-------------------|
| **GitHub + skills CLI** | Push + tag `skills-v<VERSION>` | `npx skills add …` |
| **skills.sh** | Automatic after `npx skills` installs | [skills.sh](https://skills.sh) discovery |
| **plugins CLI** | Push `plugins/` to GitHub | `npx plugins add ./plugins/<name>` |
| **Claude marketplace** | `.claude-plugin/marketplace.json` in repo | `/plugin install <name>@pruna-skills` |
| **ClawHub skills** | `clawhub skill publish` | `clawhub install @PrunaAI/<name>` |
| **ClawHub plugins** | `clawhub package publish` | `openclaw plugins install clawhub:@PrunaAI/<name>` |
| **APM** | Git paths only | `apm install PrunaAI/pruna-skills/plugins/…` |

There is **no single API** that publishes to all channels. `./scripts/publish_all_skills.py` automates both ClawHub surfaces; GitHub tag is the source-of-truth release for `npx skills`.

## One-time setup

```bash
# ClawHub — https://docs.openclaw.ai/clawhub/publishing
clawhub login
# or: export CLAWHUB_TOKEN=...
export CLAWHUB_OWNER=pruna-ai   # org/user handle on ClawHub (defaults to pruna-ai)
```

Add secrets to GitHub Actions (`CLAWHUB_TOKEN`, optional `CLAWHUB_OWNER`) for [.github/workflows/publish-skills.yml](../.github/workflows/publish-skills.yml).

## Local publish

```bash
# 1. Fresh plugins at VERSION
./scripts/bundle_all_skills.sh
./scripts/verify_skill_bundles.sh

# 2. Preview (ClawHub dry-run for skills + plugins)
./scripts/publish_all_skills.sh

# 3. Upload to ClawHub
./scripts/publish_all_skills.sh --execute

# 4. Git release marker for npx skills consumers
git tag skills-v0.0.2
git push origin skills-v0.0.2
```

Single skill or plugin:

```bash
./scripts/publish_all_skills.sh --execute --target clawhub --skill p-image
./scripts/publish_all_skills.sh --execute --target clawhub-plugins --plugin avatar-multi-scene
```

Validate a plugin locally:

```bash
claude plugin validate ./plugins/p-image
clawhub package publish ./plugins/p-image --family bundle-plugin --dry-run
```

### ClawHub skills

After publish, OpenClaw users install with:

```bash
clawhub install @PrunaAI/p-image
```

Publishes **each primary skill** at `plugins/<name>/skills/<name>/`. Workflow plugins publish only the workflow primary; embedded tool skills are not republished as separate skills.

### ClawHub plugins

Each `plugins/<name>/` folder ships Claude (`.claude-plugin/plugin.json`) and ClawHub bundle metadata (`package.json`, `openclaw.plugin.json`). Publish the whole plugin folder:

```bash
clawhub package publish ./plugins/p-image --family bundle-plugin
clawhub package publish ./plugins/pruna-full --family bundle-plugin   # full suite
```

OpenClaw install:

```bash
openclaw plugins install clawhub:@PrunaAI/p-image
openclaw plugins install clawhub:@PrunaAI/pruna-full
```

Claude Code install (GitHub marketplace, no ClawHub required):

```bash
/plugin install p-image@pruna-skills
```

### npx skills (no upload)

After pushing to GitHub and tagging `skills-v*`:

```bash
# One skill from a standalone plugin
npx skills add PrunaAI/pruna-skills/plugins/p-image/skills --skill p-image -y

# List skills discoverable via marketplace.json at repo root
npx skills add PrunaAI/pruna-skills -l

# Workflow plugin (primary + embedded deps in same folder)
npx skills add PrunaAI/pruna-skills/plugins/avatar-multi-scene/skills --skill avatar-multi-scene -y
```

Listing on [skills.sh](https://skills.sh) follows install telemetry — no separate submission step.

### npx plugins (no upload)

The [plugins CLI](https://www.npmjs.com/package/plugins) shallow-clones GitHub and scans `plugins/` for `.claude-plugin/plugin.json` bundles. No npm publish — push `plugins/` to `main`.

After clone:

```bash
npx plugins discover ./plugins
npx plugins add ./plugins/p-image -y
npx plugins add ./plugins/music-video -y
npx plugins add ./plugins/pruna-full -y
```

See the [plugins CLI on npm](https://www.npmjs.com/package/plugins) for supported agents (Claude Code, Cursor, Copilot CLI, VS Code, Codex, …).

### ClawHub CI (reusable workflow)

Skills only (flat layout):

```yaml
jobs:
  clawhub:
    uses: openclaw/clawhub/.github/workflows/skill-publish.yml@main
    with:
      owner: PrunaAI
      root: plugins
      dry_run: false
    secrets:
      clawhub_token: ${{ secrets.CLAWHUB_TOKEN }}
```

Note: the reusable workflow expects flat skill folders; use `./scripts/publish_all_skills.py` for nested `plugins/<name>/skills/<name>` layout.

This repo's workflow uses `publish_all_skills.py` for both **clawhub** (skills) and **clawhub-plugins** (bundle plugins).

### ClawHub versioning

`publish_all_skills.py` passes `--version` from repo [VERSION](../VERSION) on every ClawHub publish (skills and plugins). Without it, ClawHub defaults new skills to **1.0.0**, which breaks alignment with repo `0.0.x` versioning.

If a skill was published at 1.0.0 by mistake, publish the repo version first, then delete the errant release:

```bash
./scripts/publish_all_skills.sh --execute --target clawhub --skill p-video-replace
clawhub delete @PrunaAI/p-video-replace --version 1.0.0 --yes
```

Or fix all seven skills from the initial batch publish:

```bash
./scripts/fix_clawhub_versioning.sh
```

### ClawHub rate limit (batch over several hours)

```bash
./scripts/publish_clawhub_batches.sh
```

## Generated per workflow primary (`write_dep_manifests.py`)

| File | All skills | Workflows only |
|------|------------|----------------|
| `SKILL.md` `depends:` | | yes |
| `apm.yml` | | yes |
| `skill.deps.json` | | yes |

## CI

On push tag `skills-v*` or manual **workflow_dispatch**, GitHub Actions runs `publish_all_skills.py --execute` when secrets are configured.

See also [skill-package-managers.md](references/shared/skill-package-managers.md).
