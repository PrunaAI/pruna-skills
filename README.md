# Pruna Skills

![Pruna Skills — images, video, music, explainers, avatars, and workflows for agent coding tools](docs/assets/readme-hero-pruna-skills.png)

Generate images, video, and audio with the [Pruna AI API](https://docs.api.pruna.ai/guides/models), plus multi-step workflows like explainers, music videos, and avatars. Skills follow the [Agent Skills](https://agentskills.io/specification) format and work in Cursor, Claude Code, Copilot, Codex, and [many more agents](https://skills.sh).

## How this works

A **skill** is a playbook (`SKILL.md`) your agent loads for one job.

A **plugin** is an **install bundle** — manifest plus one or more skill folders. Workflow plugins embed the workflow skill plus its tool dependencies.

**References** are shared markdown specs in the repo ([`references/`](references/README.md)). They are best practices that are shared across various **skils**.

| Type | What it is | Typical install |
|------|------------|-----------------|
| **Tool** | One paid API call — image, video, or audio | `npx skills` |
| **Workflow** | Multi-step deliverable with approval gates | Prefer `npx plugins` |

**Rule of thumb:** one operation → `npx skills add …@tool-name`. Finished production → `npx plugins add` and pick a workflow (or **`pruna-full`** for everything once). Do not install the same tool twice — standalone and again inside a workflow plugin.

Every bundled skill includes shared generation policy (diversity, QA, staged approvals for workflows) — injected at bundle time from [references/policies/](references/policies/).

Unsure which workflow fits? See [docs/WORKFLOW-RECIPES.md](docs/WORKFLOW-RECIPES.md).

## Quickstart

```bash
export PRUNA_API_KEY="your_key"   # see [api-setup.md](docs/api-setup.md)
```

| Goal | Command |
|------|---------|
| **One tool** | `npx skills add PrunaAI/pruna-skills@p-image -y` |
| **One production** | `npx plugins add PrunaAI/pruna-skills` → pick e.g. `music-video` |
| **Full suite (non-overlapping)** | same picker → **`pruna-full`** |

```bash
npx skills add PrunaAI/pruna-skills -l
npx plugins discover PrunaAI/pruna-skills
```

Full inventory: [docs/SKILL-CATALOG.md](docs/SKILL-CATALOG.md) (20 skills: 12 tools + 8 workflows).

**Plugins CLI gotcha:** no `@name` filter — `npx plugins add PrunaAI/pruna-skills@pruna-full` fails. Use the picker, or Claude Code:

```text
/plugin marketplace add PrunaAI/pruna-skills
/plugin install pruna-full@pruna-skills
```

On multi-scene work, agents pause for plan → stills → clips before paid video. Skim [agent safety](references/shared/agent-safety.md) before enabling skills in untrusted repos.

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

## Choosing what to install

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

Install any tool: `npx skills add PrunaAI/pruna-skills@<name> -y`

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

Install: `npx plugins add PrunaAI/pruna-skills` → pick workflow name.

### Full suite

**`pruna-full`** — all 20 skills in one plugin. Prefer this over `npx plugins add … -y` (which installs 21 overlapping plugin packages).

## Install skills (`npx skills`)

```bash
npx skills add PrunaAI/pruna-skills@p-image -y
```

After install, start a **new chat**.

## Install plugins (`npx plugins`)

```bash
npx plugins add PrunaAI/pruna-skills
npx plugins add PrunaAI/pruna-skills --target cursor
```

Workflow plugins embed their tools — e.g. `music-video` includes `p-image`, `p-video`, TTS, and friends.

## Other install channels

Claude Code marketplace, ClawHub, APM — see [skill-package-managers.md](references/shared/skill-package-managers.md) and [PUBLISHING.md](docs/PUBLISHING.md).

## API setup

[docs/api-setup.md](docs/api-setup.md) — `PRUNA_API_KEY`, `REPLICATE_API_TOKEN`.

## Repo layout

Author in `tools/` and `workflows/`. Bundling copies into `plugins/<name>/` — do not edit `plugins/` by hand.

[`references/`](references/README.md) is the shared authoring library for QA checklists, API notes, and generation policy. You do **not** install it with `npx skills` / `npx plugins`. After install, those files appear inside each skill as `references/*.md`.

- **`references/policies/`** — diversity, QA, approval gates — **auto-injected** into every skill
- **`references/{shared,image,video,audio,workflows}/`** — skill-specific docs listed by basename in each `skill.manifest.json`

```text
tools/  workflows/     ──bundle──►  plugins/<name>/skills/<name>/
references/policies/              → …/references/ + “Shared generation policy” in SKILL.md
references/shared|image|…        → …/references/ when listed in the manifest
```

| Path | Role |
|------|------|
| `tools/`, `workflows/` | Skill source (what you install) |
| [`references/`](references/README.md) | Shared specs for authors/bundler — not a catalog tier |
| `plugins/` | Generated install bundles (21 plugins) |
| `docs/SKILL-CATALOG.md` | Generated catalog |
| `docs/WORKFLOW-RECIPES.md` | Human recipe routing |

Maintainers: `make bundle && make verify && make validate` — [CONTRIBUTING.md](CONTRIBUTING.md).

## License

See [LICENSE](./LICENSE).
