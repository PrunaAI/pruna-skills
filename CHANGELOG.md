# Changelog

All notable changes to Pruna Skills are documented here. Skill and plugin `metadata.version` / `package.json` versions always match repo [`VERSION`](VERSION) and the GitHub release tag `skills-v<VERSION>`.

## [Unreleased]

## [1.0.5] — 2026-07-16

GitHub tag: `skills-v1.0.5`

### Docs

- Natural-language README onboarding: how skills vs plugins work, channels, Quickstart, and Choosing tables for routers / core / verticals / suite.
- Document that `npx plugins add …@name` fails; copy-paste install blocks in plugin READMEs and README-INSTALL.
- Always create a GitHub Release after tagging (`./scripts/create_github_release.sh`); CI does the same on `skills-v*` pushes.

## [1.0.4] — 2026-07-16

GitHub tag: `skills-v1.0.4`

### Docs / descriptions

- README **Start here** + team default callout; same three-line default in [AGENTS.md](AGENTS.md).
- Rewrite all 26 skill `description` frontmatter lines (natural tone; images, video, edits, avatars, voice, full productions) — [docs/skill-description-style.md](docs/skill-description-style.md).
- Description trigger / non-trigger audit in [SKILL-TEST-LOG.md](SKILL-TEST-LOG.md).
- Agents/MCP decision gate (doc only): [docs/agents-mcp-gate.md](docs/agents-mcp-gate.md).
- skills.sh badge deferred (listing URL returns 500 until telemetry lands); team bootstrap noted in [BACKLOG.md](BACKLOG.md).
- Copilot dual `.github/plugin.json` still gated — CLI not installed (ENOENT), not a format failure.

## [1.0.3] — 2026-07-16

GitHub tag: `skills-v1.0.3`

### Docs / distribution UX

- Clarify README: `npx skills` / `npx plugins` as defaults; skills.sh + agent-safety links; ChatGPT note; ClawHub casing explained.
- Canonical install: `npx skills add PrunaAI/pruna-skills@<name> -y` everywhere (README-INSTALL, publish-index).
- Add [`skills.catalog.json`](skills.catalog.json), [`AGENTS.md`](AGENTS.md), [`BACKLOG.md`](BACKLOG.md).
- `make validate` → `./scripts/validate_release.sh` (verify + skills-ref + clawhub + install smoke).
- PUBLISHING: manual Cursor / Claude / Copilot smoke checklist; **How consumers get updates** (no separate Cursor/Claude app-store submit).
- **pruna-full** positioning: staged approval + parallel subagents after confirm (README + suite plugin description).
- Tighten router/tool overlap `description` frontmatter; add cheap eval prompts to [SKILL-TEST-LOG.md](SKILL-TEST-LOG.md).

## [1.0.2] — 2026-07-16

GitHub tag: `skills-v1.0.2`

### Security / ClawHub SkillSpector

- Add shared [agent-safety.md](references/shared/agent-safety.md): privacy/upload disclosure, credential handling (no key forwarding to subagents), local disk overwrite warning, locale opt-in for `voice_language`.
- Wire safety into `pruna-api`, `api-credentials`, `random-seed-ritual` (manifest-only ritual seed; not mandatory user-visible), and `parallel-execution` (multi-scene workflow scope only).
- **p-video-avatar:** confirm locale; annotate English examples as illustrative; link agent-safety before uploads.
- **p-video / image-to-video:** skill boundary = one prediction; remove bundled multi-scene/subagent orchestration (`parallel-execution` dropped from those manifests); demote multi-scene docs to outbound workflow links.
- Reframe [scene-anchor-triple.md](references/video/scene-anchor-triple.md) around a single narrated beat; multi-scene under narrated-multi-scene only.

### OpenClaw plugin validation

- All 27 plugins declare `openclaw.extensions` + `openclaw.compat.pluginApi` (via `build_plugins.py`); ClawHub `package validate` PASS with 0 warnings.
- Enforce in `verify_skill_bundles.sh`; add `./scripts/validate_clawhub_plugins.sh` and run it from `release.sh`.
- Docs: [package-openclaw-entry-missing](https://docs.openclaw.ai/clawhub/plugin-validation-fixes#package-openclaw-entry-missing), [package-plugin-api-compat-missing](https://docs.openclaw.ai/clawhub/plugin-validation-fixes#package-plugin-api-compat-missing).

## [1.0.1] — prior

Initial ClawHub / marketplace release aligned to `skills-v1.0.1`.
