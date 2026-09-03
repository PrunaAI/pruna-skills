# Changelog

All notable changes to Pruna Skills are documented here. Skill and plugin `metadata.version` / `package.json` versions always match repo [`VERSION`](VERSION) and the GitHub release tag `skills-v<VERSION>`.

## [Unreleased]

### Added

- **`p-video-edit` tool** — instruction-based video-to-video via Pruna `p-video-edit`: source clip (≤15s) + surgical `prompt`, optional 1–4 reference images, draft/standard billing per output second.

### Changed

- **`p-video-avatar`** — dropped `last_frame_image` from the audio-driven payload.

## [1.0.10] — 2026-08-27

GitHub tag: `skills-v1.0.10`

### Added

- **`p-image-ideogram` `thinking: "very high"`** — premium path for maximum quality on complex compositions (`very high` + `image_size: "2K"`); ~2× cost of `high` ($0.033/1K, $0.066/2K).
- **`type-premium` domain profile** — flagship creative / multi-element heroes in [domain-configurations.md](skills/image/p-image-ideogram/references/domain-configurations.md).

### Changed

- **`p-image-ideogram`** — five thinking levels (`very low` … `very high`); removed stale 422 warning that blocked `"very high"`; agent defaults, generation flow, and optional fields document the premium path.

## [1.0.9] — 2026-08-04

GitHub tag: `skills-v1.0.9`

### Added

- **`p-image-ideogram` tool** — high-fidelity text-to-image via Pruna `p-image-ideogram`: thinking levels, 1K/2K output, photoreal heroes, legible typography, GTM layouts, and structured JSON prompts with hex colors and bounding boxes.

### Changed

- **`p-image`** — repositioned as the cheap/fast draft path; routes hero, typography, and structured still work to `p-image-ideogram`.
- **`image-prompting`**, **`generation-diversity`**, **`pruna-api`**, suite, and related image/video tools — default T2I routing, install tables, and still-image prompt flow updated for `p-image-ideogram`.

## [1.0.8] — 2026-07-28

GitHub tag: `skills-v1.0.8`

### Added

- **`generation-diversity` clarification intake** — library-wide SSoT for generate vs existing media, palette, narration/VO, music, captions, aspect ratio, resolution, structure, and workflow approval gates (`references/clarification-intake.md`).
- **`branding` guide** — official Pruna logo kit and usage locks for agent-generated assets.
- **`video-editing` references** — motion composition craft, narrated showcase, and social use-case reel patterns.

### Changed

- **AGENTS.md** — Clarification (library-wide) table: guides/tools, workflows, HyperFrames, and `pruna-api` behavior before paid calls.
- **Workflows and suite** — cross-link clarification intake and workflow **Intake: ask before generating** tables across avatar, narrated, music, illustrated, and transition reels.
- **`video-editing`** — expanded routing to new references; captions and HyperFrames combination notes updated.
- **`pruna-api` agent-safety** — clarification deferral before upload/generation.
- README: Hugging Face–hosted example assets; installation and maintainer docs tightened.
- README: api-setup link outside code fence; maintainer command aligned to `make bundle && make validate`.
- `visual-transition-reel/example-prompt.md`: `output/visual-transition-reel/` (removed stale `output/core/`).
- BACKLOG: trim completed description-audit section and duplicate install bootstrap.
- `.gitignore`: `.DS_Store`, `docs/assets/examples/*.tmp`, `_preview/`.

### Removed

- Orphan tracked assets: `docs/assets/readme-hero-pruna-skills.png`, `docs/assets/examples/readme-chain-monarch-*` (README quickstart embeds superseded by sneaker/drummer/whale chains).

## [1.0.7] — 2026-07-23

GitHub tag: `skills-v1.0.7`

### Added

- **`video-editing` guide** — ffmpeg assembly craft: concat, transitions, caption burn-in (whisperx → ASS → libass; stable phrase bar + word accent), overlays, comparison sliders, background music beds, export presets, and HyperFrames combination pattern.
- **HyperFrames optional companion** — `npx skills add heygen-com/hyperframes@hyperframes -y` documented in `video-editing` (same install pattern as workflow prerequisites); `make install-companion-skills` for maintainers.
- **Product sneaker edit chain** — README quickstart + `docs/EXAMPLES.md` + `gen_chain_sneaker` doc example (`p-image` → `p-image-edit` → `p-video`).
- **README hero launch reel** — full-duration GIF (≤10 MB for GitHub) linked to MP4 with VO and music.

### Changed

- **`video-editing` captions** — default launch style is stable phrase bar + text-only purple word accent (no flicker, no double box); movie timing limits and SRT centisecond parsing documented in [captions.md](skills/guides/video-editing/references/captions.md).
- **Version injection** — all skills use `@VERSION` in frontmatter; [`.maintainer/sync_skill_versions.py`](.maintainer/sync_skill_versions.py) injects repo [`VERSION`](VERSION) on `make bundle` / release (`make sync-versions`, `--check`, `--placeholders`).
- **Doc examples refresh:** README quickstart embeds use in-repo GIF/PNG paths; full-duration GIF previews (`make readme-example-embeds`, `generate_example_previews.py`). Monarch chain kept for `p-video-animate` and narrated-multi-scene; sneaker chain is the primary edit-chain demo.
- Cross-refs to `video-editing` on workflows, video/audio tools, and prompting guides; `whisperx` / `audio-prompting` point at post-render caption path.
- README: dedupe suite tables; link to [docs/SKILL-CATALOG.md](docs/SKILL-CATALOG.md) and [skills/suite/pruna/SKILL.md](skills/suite/pruna/SKILL.md) instead.
- Workflow example paths: `output/<workflow>/…` (removed stale `output/verticals/`).
- [docs/SKILL-TEST-LOG.md](docs/SKILL-TEST-LOG.md) and [docs/agents-mcp-gate.md](docs/agents-mcp-gate.md) updated for skills-only layout (`@pruna` suite, no router skills).
- Catalog: **6 guides + 12 tools + 8 workflows + `@pruna` suite** (26 installable skills).

### Removed

- Orphan `docs/assets/readme-hero-base.png`, `.maintainer/release/publish_clawhub_batches.sh`, duplicate Makefile GIF targets, `skills/workflows/README.md`.

### Note on [1.0.6]

Release notes below describe a brief plugin-era taxonomy (tools/workflows only). **Current catalog:** 5 guides + 12 tools + 8 workflows + `@pruna` suite — see [`.maintainer/skills.catalog.json`](.maintainer/skills.catalog.json).

## [1.0.6] — 2026-07-16

GitHub tag: `skills-v1.0.6`

### Changed

- **Taxonomy:** Public catalog is **12 Tools + 8 Workflows** only. Retired guide/router skills (`generation-diversity`, `generation-quality-checklists`, `recipe-catalog`, `requesting-generation-feedback`, `pruna-generative-pipeline`, `pruna-run`) — behavior preserved via bundle-injected [references/policies/](references/policies/) and [docs/WORKFLOW-RECIPES.md](docs/WORKFLOW-RECIPES.md).
- Flattened workflow source: `workflows/<name>/` (removed `core/`, `verticals/`, `router/`, and `guides/`).
- `make bundle` injects a marked **Shared generation policy** section into every skill; `make verify` checks policy markers and files.
- Plugin count: **21** (20 standalone + `pruna-full`).

### Docs

- README: Tools vs Workflows vs Plugins; clarify that [`references/`](references/README.md) is a shared authoring library (not installable; not “reference images”); full catalog in [docs/SKILL-CATALOG.md](docs/SKILL-CATALOG.md).
- Prefer `pruna-full` over `npx plugins … -y` (overlapping plugin packages).
- Contributor docs under `docs/`; maintainer automation under `.maintainer/` (Makefile-only: `make bundle`, `make validate`).
- Catalog source: [`.maintainer/skills.catalog.json`](.maintainer/skills.catalog.json); generated catalog: `docs/SKILL-CATALOG.md`. Root keeps `skills.sh.json` (skills.sh contract).
- `api-setup.md` and `PUBLISHING.md` moved to `docs/`.
- Policies live only under `references/policies/` (duplicates removed from `references/shared/`).

### Removed

- Installable skills/plugins: `generation-diversity`, `generation-quality-checklists`, `recipe-catalog`, `requesting-generation-feedback`, `pruna-generative-pipeline`, `pruna-run` (soft-delete on ClawHub at release).
- Legacy wrapper `scripts/generate_upscale_comparison.py` (canonical: `workflows/_shared/scripts/generate_upscale_comparison.py`).
- Dead `write_skill_manifests.py`, orphan `SCRIPT-TEMPLATE.md`, and top-level `scripts/` (now `.maintainer/`).

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
