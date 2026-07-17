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
npx plugins add PrunaAI/pruna-skills                    # pick a workflow or pruna-full
npx skills add PrunaAI/pruna-skills -l                  # list tools
npx plugins discover PrunaAI/pruna-skills               # list plugins
```

**Install everything once** — pick **`pruna-full`** in the plugin picker (all 20 skills, no overlap). The plugins CLI has no `@name` filter; in Claude Code:

```text
/plugin marketplace add PrunaAI/pruna-skills
/plugin install pruna-full@pruna-skills
```

Don’t run `npx plugins add … -y` for the whole repo — that installs 21 overlapping packages.

After install, start a **new chat**. Multi-scene workflows pause for you to review the plan and images before generating video. Skim [agent safety](references/shared/agent-safety.md) before enabling skills in untrusted repos.

### Example — one image, then a three-step chain

**Step 1 — `p-image`** (one tool):

> Create an image of a red panda as barista.

![red panda barista](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/quickstart-panda-01-open.png)

```bash
npx skills add PrunaAI/pruna-skills@p-image -y
```

> Edit the image and make sure the panda becomes and astronaut then chain the images together with a video.

| Kyoto café | Same panda on Mars | 10s clip |
|------------|-------------------|---------|
| ![café](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/quickstart-panda-01-open.png) | ![Mars](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/quickstart-panda-02-end.png) | <video src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/quickstart-panda-clip.mp4" controls width="200"></video> |

```bash
npx skills add PrunaAI/pruna-skills@p-image-edit -y
npx skills add PrunaAI/pruna-skills@p-video -y
```

Or install a workflow plugin that bundles the tools — e.g. `npx plugins add PrunaAI/pruna-skills` → pick `visual-transition-reel` or **`pruna-full`**.

More examples — each a different scenario: [docs/EXAMPLES.md](docs/EXAMPLES.md).

## What’s available

### Tools (12)

| You want… | Skill |
|-----------|-------|
| Fast text-to-image | `p-image` |
| Edit or combine from reference photos | `p-image-edit` |
| Virtual try-on | `p-image-try-on` |
| Upscale | `p-image-upscale` |
| One video clip | `p-video` |
| Copy motion from one video to another | `p-video-animate` |
| Person on camera speaking | `p-video-avatar` |
| Swap person or product in video | `p-video-replace` |
| Narration (text to speech) | `gemini-3.1-flash-tts` |
| Song with vocals | `music-2.5` |
| Background music (no vocals) | `stable-audio-2.5` |
| Lyric timestamps | `whisperx` |

```bash
npx skills add PrunaAI/pruna-skills@<name> -y    # e.g. @p-image, @p-video, @music-2.5
```

### Workflows (8)

| You want… | Skill |
|-----------|-------|
| Turn images into video clips | `image-to-video` |
| Multi-part story with narration | `narrated-multi-scene` |
| Scene-to-scene transition montage | `visual-transition-reel` |
| One short presenter clip | `avatar-single-scene` |
| Presenter across several scenes | `avatar-multi-scene` |
| Educational explainer | `interactive-explainer` |
| Full music video | `music-video` |
| Illustrated slideshow reel | `illustrated-story-reel` |

```bash
npx plugins add PrunaAI/pruna-skills   # pick a workflow from the list
```

Each workflow plugin includes the tools it needs — you don’t install those separately.

### Full suite — `pruna-full`

All 20 skills (12 tools + 8 workflows) in one plugin. Best if you want the whole library without picking individual packages.

```bash
npx plugins add PrunaAI/pruna-skills   # pick pruna-full
```

Claude Code:

```text
/plugin marketplace add PrunaAI/pruna-skills
/plugin install pruna-full@pruna-skills
```

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
| `docs/EXAMPLES.md` | Prompt → image/video gallery (HF dataset + local sidecars) |
| `docs/WORKFLOW-RECIPES.md` | Human recipe routing |

Maintainers: `make bundle && make verify && make validate` — [CONTRIBUTING.md](CONTRIBUTING.md).

## License

See [LICENSE](./LICENSE).
