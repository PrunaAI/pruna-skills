# Pruna Skills

![Pruna Skills — images, video, music, explainers, avatars, and workflows for agent coding tools](docs/assets/readme-hero-pruna-skills.png)

Generate images, video, and audio with the [Pruna AI API](https://docs.api.pruna.ai/guides/models), plus multi-step workflows (explainers, music videos, avatars, and more). Skills follow the [Agent Skills](https://agentskills.io/specification) format and work in Cursor, Claude Code, Copilot, Codex, and [many more agents](https://skills.sh).

## How this works

| Term | Meaning |
|------|---------|
| **Skill** | A playbook (`SKILL.md`) the agent follows for one job |
| **Plugin** | An install package — one skill, or a workflow plus the tools it needs |
| **Tool** | One paid API call (image, video, audio) — install with `npx skills` |
| **Workflow** | A multi-step deliverable with approval gates — install with `npx plugins` |
| **References** | Shared markdown in [`references/`](references/README.md) (QA, API notes, policy). Not something you install; bundling copies them into each skill. Unrelated to **reference images** you upload for edit/try-on |

Pick a tool for a single generation. Pick a workflow (or **`pruna-full`**) when you want a finished production. Don’t install the same tool twice — once alone and again inside a workflow plugin.

Every skill ships with shared generation policy (diversity, QA, staged approvals for workflows) from [references/policies/](references/policies/). Recipe ideas: [docs/WORKFLOW-RECIPES.md](docs/WORKFLOW-RECIPES.md). Full list: [docs/SKILL-CATALOG.md](docs/SKILL-CATALOG.md) (12 tools + 8 workflows).

## Quickstart

```bash
export PRUNA_API_KEY="your_key"   # see [api-setup.md](docs/api-setup.md)

npx skills add PrunaAI/pruna-skills@p-image -y          # one tool
npx plugins add PrunaAI/pruna-skills                    # pick music-video, pruna-full, …
npx skills add PrunaAI/pruna-skills -l                  # list skills
npx plugins discover PrunaAI/pruna-skills               # list plugins
```

The plugins CLI has no `@name` filter (that’s skills-only). So `npx plugins add PrunaAI/pruna-skills@pruna-full` won’t work — use the picker, or in Claude Code:

```text
/plugin marketplace add PrunaAI/pruna-skills
/plugin install pruna-full@pruna-skills
```

Prefer **`pruna-full`** over `npx plugins add … -y` if you want everything once; `-y` installs every plugin package and overlaps tools.

Multi-scene workflows pause for plan → stills → clips before paid video. Skim [agent safety](references/shared/agent-safety.md) before enabling skills in untrusted repos. After install, start a **new chat**.

## Examples

### Tool — `p-image`

| | |
|--|--|
| **You say** | “Generate a 9:16 product hero — matte black headphones on concrete, soft side light” |
| **You get** | One image file or URL |

### Workflow — `music-video`

```text
plan.json → song.mp3 → stills/*.jpg → clips/*.mp4 → final.mp4
```

Install: `npx plugins add PrunaAI/pruna-skills` → pick `music-video`. Template: [music-video-plan.template.json](workflows/music-video/templates/music-video-plan.template.json).

## What’s available

### Tools (12)

| You want… | Skill |
|-----------|-------|
| Fast text-to-image | `p-image` |
| Edit / compose from refs | `p-image-edit` |
| Virtual try-on | `p-image-try-on` |
| Upscale | `p-image-upscale` |
| One video clip | `p-video` |
| Motion-transfer | `p-video-animate` |
| Person on camera speaking | `p-video-avatar` |
| Swap person or product in video | `p-video-replace` |
| Narration / voiceover | `gemini-3.1-flash-tts` |
| Song with vocals | `music-2.5` |
| Background music bed | `stable-audio-2.5` |
| Lyric timestamps | `whisperx` |

`npx skills add PrunaAI/pruna-skills@<name> -y`

### Workflows (8)

| You want… | Skill |
|-----------|-------|
| B-roll from images | `image-to-video` |
| Multi-part story with VO | `narrated-multi-scene` |
| Transition montage | `visual-transition-reel` |
| One host beat | `avatar-single-scene` |
| Multi-scene host | `avatar-multi-scene` |
| Educational explainer | `interactive-explainer` |
| Full music video | `music-video` |
| Illustrated slideshow reel | `illustrated-story-reel` |

`npx plugins add PrunaAI/pruna-skills` → pick the workflow. Each workflow plugin embeds the tools it needs.

### Full suite

**`pruna-full`** — all 20 skills in one plugin.

## Other install channels

Claude Code marketplace, ClawHub, APM — [skill-package-managers.md](references/shared/skill-package-managers.md) and [PUBLISHING.md](docs/PUBLISHING.md).

## API setup

[docs/api-setup.md](docs/api-setup.md) — `PRUNA_API_KEY`, `REPLICATE_API_TOKEN`.

## Repo layout

Author in `tools/` and `workflows/`. Bundling writes `plugins/<name>/` — don’t edit that tree by hand.

```text
tools/  workflows/     ──bundle──►  plugins/<name>/skills/<name>/
references/policies/              → injected into every skill
references/shared|image|…        → copied when listed in skill.manifest.json
```

| Path | Role |
|------|------|
| `tools/`, `workflows/` | Skill source |
| [`references/`](references/README.md) | Shared specs for authors/bundler — not a catalog tier |
| `plugins/` | Generated install bundles (21 plugins) |
| `docs/SKILL-CATALOG.md` | Generated catalog |
| `docs/WORKFLOW-RECIPES.md` | Human recipe routing |

Maintainers: `make bundle && make verify && make validate` — [CONTRIBUTING.md](CONTRIBUTING.md).

## License

See [LICENSE](./LICENSE).
