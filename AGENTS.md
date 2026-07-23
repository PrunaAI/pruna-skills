# Pruna Skills (agent notes)

Generative media skills for the [Pruna AI API](https://docs.api.pruna.ai/guides/models). Portable [Agent Skills](https://agentskills.io/specification) — Cursor, Claude Code, Copilot, Codex, and more.

## How this works

See [README.md](README.md) for the user-facing glossary.

| Type | Role |
|------|------|
| **Guide** | Vendor-neutral craft (`image-prompting`, `video-prompting`, `audio-prompting`, `video-editing`, `generation-diversity`) or Pruna HTTP (`pruna-api`) |
| **Tool** | One paid API call (`p-image`, `p-video`, …) |
| **Workflow** | Multi-step deliverable — agent is the runner (curl + ffmpeg) |
| **Suite** | `pruna` — install everything |

Tools list guide deps under **Prerequisites** with `npx skills add`. Workflows list **tools** only (guides come via tools). **Optional external companions** (e.g. HyperFrames for HTML → MP4 launch reels) install the same way but are not in `@pruna` — see `video-editing` and its `combination-hyperframes` reference. Do not copy craft between skills — install the other skill.

Humans picking recipes: [docs/WORKFLOW-RECIPES.md](docs/WORKFLOW-RECIPES.md). Catalog: [docs/SKILL-CATALOG.md](docs/SKILL-CATALOG.md).

## Install

```bash
export PRUNA_API_KEY="…" # see docs/api-setup.md

npx skills add PrunaAI/pruna-skills@pruna -y
```

```bash
npx skills add PrunaAI/pruna-skills@p-image -y   # one tool (+ install its Prerequisites guides)
npx skills add PrunaAI/pruna-skills -l
```

**Team default:** **`pruna`** once, then start a new chat.

**Launch reels / motion assembly:** install **`hyperframes`** when the deliverable needs HTML → MP4 composition (optional — ffmpeg-only paths skip it):

```bash
npx skills add heygen-com/hyperframes@hyperframes -y
```

Read **`hyperframes`** first — it routes to `/product-launch-video`, `/general-video`, etc. Pruna skills generate media; HyperFrames assembles HTML → MP4 (each launch uses a local `hyperframes/` subfolder in your project workspace). Maintainers: `make install-companion-skills` copies the full bundle into gitignored `.agents/skills/`.

## Layout

| Path | Role |
|------|------|
| `skills/guides/` | Craft SSoT (edit markdown under each guide’s `references/`) |
| `skills/{image,video,audio}/` | Tool skills |
| `skills/workflows/` | Workflow playbooks |
| `skills/suite/pruna/` | Umbrella |
| `docs/` | Human docs only |
| `.maintainer/skills.catalog.json` | Skill name source of truth |
| `VERSION` | Repo semver — `@VERSION` in skills is replaced on `make bundle` |

## Safety

Install `pruna-api` — agent-safety lives in that skill (`references/agent-safety.md` after install).

## Maintainers

```bash
make bundle && make validate
```

Releases: [PUBLISHING.md](docs/PUBLISHING.md) · Backlog: [BACKLOG.md](docs/BACKLOG.md)
