# Publishing skills

Bundled skills live in `plugins/<name>/skills/<name>/`. Version is repo [VERSION](VERSION), synced into every `SKILL.md` `metadata.version`, plugin manifests, and registry sidecars (`apm.yml`, `skill.deps.json`).

**Version alignment:** ClawHub skill versions, ClawHub plugin package versions, and the GitHub release tag **`skills-v<VERSION>`** must all match [VERSION](VERSION). Record release notes in [CHANGELOG.md](CHANGELOG.md) before tagging.

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
# 1. Update CHANGELOG.md, then set VERSION and rebuild
./scripts/release.sh 1.0.2

# 2. Commit, tag (must match VERSION), push
git add -A && git commit -m "[release] skills v1.0.2"
git tag skills-v1.0.2
git push origin main && git push origin skills-v1.0.2

# 3. Always create the GitHub Release (notes from CHANGELOG)
./scripts/create_github_release.sh 1.0.2

# 4. Upload to ClawHub (or rely on CI on tag push)
./scripts/publish_all_skills.sh --execute --target clawhub,clawhub-plugins,index
```

A tag alone is not enough for the release page — **always** run `./scripts/create_github_release.sh <VERSION>` (or let CI create it on `skills-v*` push). Consumers and maintainers use the [Releases](https://github.com/PrunaAI/pruna-skills/releases) page for notes.

Legacy one-liner steps:

```bash
# 1. Fresh plugins at VERSION
./scripts/bundle_all_skills.sh
./scripts/verify_skill_bundles.sh

# 2. Preview (ClawHub dry-run for skills + plugins)
./scripts/publish_all_skills.sh

# 3. Upload to ClawHub
./scripts/publish_all_skills.sh --execute

# 4. Git tag + GitHub Release for npx skills consumers
git tag skills-v1.0.2
git push origin skills-v1.0.2
./scripts/create_github_release.sh 1.0.2
```

Single skill or plugin:

```bash
./scripts/publish_all_skills.sh --execute --target clawhub --skill p-image
./scripts/publish_all_skills.sh --execute --target clawhub-plugins --plugin avatar-multi-scene
```

Validate before release:

```bash
./scripts/validate_release.sh          # verify + skills-ref + clawhub + install smoke
# or: make validate
```

Single plugin:

```bash
claude plugin validate ./plugins/p-image
clawhub package validate ./plugins/p-image
```

Every `plugins/*/package.json` must declare OpenClaw entry + API compat (enforced by `verify_skill_bundles.sh`):

```json
"openclaw": {
  "extensions": ["./openclaw-entry.mjs"],
  "compat": { "pluginApi": ">=2026.3.24-beta.2" }
}
```

See [package-openclaw-entry-missing](https://docs.openclaw.ai/clawhub/plugin-validation-fixes#package-openclaw-entry-missing) and [package-plugin-api-compat-missing](https://docs.openclaw.ai/clawhub/plugin-validation-fixes#package-plugin-api-compat-missing).

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
npx skills add PrunaAI/pruna-skills@p-image -y
npx skills add PrunaAI/pruna-skills@music-video -y
npx skills add PrunaAI/pruna-skills -l
```

Listing on [skills.sh](https://skills.sh) follows install telemetry — no separate submission step.

### npx plugins (no upload)

The [plugins CLI](https://www.npmjs.com/package/plugins) shallow-clones GitHub and scans `plugins/` for `.claude-plugin/plugin.json` bundles. No npm publish — push `plugins/` to `main`.

```bash
npx plugins discover PrunaAI/pruna-skills

# Interactive — pick one (e.g. music-video, pruna-full)
npx plugins add PrunaAI/pruna-skills

# Install ALL 27 plugins
npx plugins add PrunaAI/pruna-skills -y

npx plugins add PrunaAI/pruna-skills --target cursor
```

Do **not** use `npx plugins add PrunaAI/pruna-skills@pruna-full` — plugins CLI has no `@name` filter (skills CLI only); that command prints “No plugins found”.

See the [plugins CLI on npm](https://www.npmjs.com/package/plugins) for supported agents.

## Manual IDE smoke (after release)

CI covers file layout only. Before announcing a release, spend ~5–10 minutes:

1. **Cursor** — `npx skills add PrunaAI/pruna-skills@p-image -y` → new chat → “Generate a product hero image” → skill loads.
2. **Claude Code** — `npx plugins add PrunaAI/pruna-skills` → pick `music-video`, or `/plugin install music-video@pruna-skills` → new session → trigger a workflow prompt.
3. **Copilot CLI** — `copilot plugin install p-image@pruna-skills` (or `npx plugins add PrunaAI/pruna-skills --target github-copilot`) → confirm skill/plugin is listed.

If Copilot native install fails without a `.github/plugin.json`, see [BACKLOG.md](BACKLOG.md).

**ClawHub naming:** docs use `@PrunaAI/…`; `package.json` scope is `@pruna-ai/…` (same org, different casing).

## How consumers get updates (Claude / Cursor / Copilot)

There is **no separate “submit to Cursor” or “Claude App Store” upload**. One GitHub push (plus optional ClawHub publish) updates every IDE channel.

| Channel | Separate publish? | What you do | What users run |
|---------|-------------------|-------------|----------------|
| **Cursor** | No | Push `plugins/` to GitHub | `npx skills add PrunaAI/pruna-skills@p-image -y` or `npx plugins add PrunaAI/pruna-skills` (pick) |
| **Claude Code** | No (marketplace is in-repo) | Keep `.claude-plugin/marketplace.json` current via bundle; push | `/plugin marketplace add PrunaAI/pruna-skills` then `/plugin install <name>@pruna-skills` |
| **Copilot CLI / VS Code** | No | Same GitHub push | `npx plugins add PrunaAI/pruna-skills` or `copilot plugin marketplace add` + `copilot plugin install …` |
| **skills.sh** | No | Nothing — listing follows install telemetry | Discover after installs; drive traffic from README |
| **ClawHub / OpenClaw** | Yes | `./scripts/publish_all_skills.sh --execute` (or CI on tag) | `clawhub install @PrunaAI/p-image` |
| **ChatGPT** | Manual / admin | Upload `SKILL.md` in product UI | No `npx` path |

**Claude:** users add the GitHub repo once as a marketplace; they refresh after you push tags/commits.  
**Cursor:** skills land via `npx skills` (`.agents/skills/` or `~/.cursor/skills/`); plugins via `npx plugins`. Default is latest `main`; pin with `skills-v*` when the CLI supports `@ref`.

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
