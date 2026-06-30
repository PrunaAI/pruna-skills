# pruna-ai-content-generation-skills

Agent skills for generating images, video, and audio with the [Pruna AI API](https://docs.api.pruna.ai/guides/models) — plus multi-step workflows for explainers, music videos, and similar projects.

Skills follow the [Agent Skills](https://agentskills.io/specification) format. Install with [`npx skills`](https://www.npmjs.com/package/skills), [APM](https://microsoft.github.io/apm/), [PSPM](https://docs.anyt.io/pspm/introduction), or other agents — see [Install skills](#install-skills).

## Repository layout

```text
catalog/                           # authoring sources — edit here (see catalog/README.md)
  references/     API specs, quality checklists, workflow docs
  tools/          one skill per model (p-image, p-video, …)
  workflows/      multi-step workflows (router, core, verticals, _shared/scripts)
  examples/       starter prompts and templates

skills/                            # generated install bundles — do not edit; rebuilt on pre-commit
scripts/                           # repo build tooling (bundle, install, pre-commit)

output/                            # local generated files (not committed)
.mine/                             # Pruna-internal campaign work (not for public install)
```

**Tool** skills document a single API. **Workflow** skills describe full projects: scene plans, approval steps, and helper scripts.

## Workflow organization

| Layer | Where | Choose this when |
|-------|--------|------------------|
| **Models** | `catalog/tools/` | You need one API call (a single image, video clip, or audio file) |
| **Router** | `catalog/workflows/router/` | You are not sure which workflow fits yet |
| **Core** | `catalog/workflows/core/` | You know the scene structure (one clip, multi-scene story, transitions, talking head) |
| **Vertical** | `catalog/workflows/verticals/` | You know the end product (explainer, music video, illustrated story) |

Pruna-internal marketing reels live in [`.mine/`](.mine/README.md) and are not part of the public install set.

**Good starting points:** [pruna-generative-pipeline](catalog/workflows/router/pruna-generative-pipeline/SKILL.md) (recipe menu) or [pruna-run](catalog/workflows/router/pruna-run/SKILL.md) (quick single-shot generation).

### Core workflows (building blocks)

| Skill | Also known as | What it does |
|-------|---------------|--------------|
| [image-to-video](catalog/workflows/core/image-to-video/SKILL.md) | `single-scene-ai-video` | One video clip from a start image, optional end image, and optional narration audio |
| [narrated-multi-scene](catalog/workflows/core/narrated-multi-scene/SKILL.md) | `multi-scene-ai-video` | Multi-scene film: each scene has start and end images plus narration, then clips are combined |
| [visual-transition-reel](catalog/workflows/core/visual-transition-reel/SKILL.md) | `scene-transition-video` | Montage that moves between still images — visual only, no spoken narration required |
| [avatar-single-scene](catalog/workflows/core/avatar-single-scene/SKILL.md) | `single-scene-avatar-video` | One talking-head clip: portrait image plus script, with a quality check before you pay for video |
| [avatar-multi-scene](catalog/workflows/core/avatar-multi-scene/SKILL.md) | `multi-scene-avatar-video` | Several talking-head or motion-transfer scenes with the same character, then assembled into one video |

### Vertical workflows (finished formats)

| Skill | Also known as | What it does |
|-------|---------------|--------------|
| [interactive-explainer](catalog/workflows/verticals/interactive-explainer/SKILL.md) | `educational-explainer` | Educational video: narrator scenes plus character dialogue (history, science, biography, and similar) |
| [music-video](catalog/workflows/verticals/music-video/SKILL.md) | `ai-music-video` | Full music video: generated song, timed cuts, performance clips and background footage |
| [illustrated-story-reel](catalog/workflows/verticals/illustrated-story-reel/SKILL.md) | — | Story told with still images (Ken Burns motion), plus narration or music — no video model required |

More detail: [interactive-explainer-scenes.md](catalog/references/workflows/interactive-explainer-scenes.md) · [pruna-models.md](catalog/references/shared/pruna-models.md) · [examples](catalog/examples/README.md)

## All skills

### Model skills (Pruna API)

| Skill | What it does |
|-------|----------------|
| `p-image` | Generate an image from a text prompt; choose aspect ratio and optional seed |
| `p-image-edit` | Edit or compose images from a text prompt plus one to five reference images |
| `p-image-upscale` | Upscale an image (1–128 megapixels) with optional detail or realism enhancement |
| `p-image-try-on` | Put clothing from reference photos onto a person photo (virtual try-on) |
| `p-video` | Generate video from text, from a still image, or between a start and end frame; can sync to uploaded audio |
| `p-video-avatar` | Talking-head video from a portrait plus a spoken script or audio file |
| `p-video-animate` | Apply motion from a reference video onto a still image |
| `p-video-replace` | Swap a person, outfit, or product into existing footage using reference images |

### Model skills (Replicate)

| Skill | What it does |
|-------|----------------|
| `music-2.5` | Generate a full song with vocals from lyrics and a style prompt ([MiniMax Music 2.5](https://replicate.com/minimax/music-2.5)) |
| `gemini-3.1-flash-tts` | Generate spoken narration with controllable voice and delivery ([Gemini Flash TTS](https://replicate.com/google/gemini-3.1-flash-tts)) |
| `stable-audio-2.5` | Generate instrumental background music to mix under a video |
| `whisperx` | Transcribe audio (used in music-video lyric timing workflows) |

### Router skills

| Skill | What it does |
|-------|----------------|
| `pruna-generative-pipeline` | Help pick a workflow from a recipe menu (mood boards, hero variants, multi-scene films, and more) |
| `pruna-run` | Run a single prompt quickly — routes to image, image-to-video, or avatar generation |
| `requesting-generation-feedback` | Pause for user approval before paid API calls and final assembly |

### Core workflows

| Skill | What it does |
|-------|----------------|
| `image-to-video` | Plan and generate one cinematic clip |
| `narrated-multi-scene` | Plan and generate a multi-scene narrated film |
| `visual-transition-reel` | Plan and generate a visual montage between stills |
| `avatar-single-scene` | Plan and generate one talking-head clip with approval gates |
| `avatar-multi-scene` | Plan and generate several avatar or motion-transfer scenes |

### Vertical workflows

| Skill | What it does |
|-------|----------------|
| `interactive-explainer` | End-to-end educational explainer with narrator and character scenes |
| `music-video` | End-to-end music video from lyrics through song, clips, and final edit |
| `illustrated-story-reel` | End-to-end illustrated story with stills and narration or music |

## Install skills

Use the committed [`skills/`](skills/README.md) bundles (not the repo root). `metadata.version` matches [`VERSION`](VERSION) (**0.0.1**). Workflow folders include generated **`depends:`**, **`apm.yml`**, **`pspm.json`**, and **`skill.deps.json`** from the same `tool_skills` list.

Copy-paste project manifests: [catalog/examples/consumer-manifests/](catalog/examples/consumer-manifests/README.md). Full comparison: [skill-package-managers.md](catalog/references/shared/skill-package-managers.md).

### `npx skills` (Cursor, Codex, Claude Code, …)

**From GitHub (no clone)**

```bash
# List
npx skills add PrunaAI/pruna-ai-content-generation-skills/skills --list

# Tool skill
npx skills add PrunaAI/pruna-ai-content-generation-skills/skills \
  --skill p-image --agent cursor -y

# Shorthand
npx skills add PrunaAI/pruna-ai-content-generation-skills/skills@p-image -y

# Workflow — tool skills from depends: in SKILL.md frontmatter
npx skills add PrunaAI/pruna-ai-content-generation-skills/skills \
  --skill avatar-multi-scene --agent cursor -y

# Router + vertical
npx skills add PrunaAI/pruna-ai-content-generation-skills/skills \
  --skill pruna-generative-pipeline --skill music-video -y
```

| Format | Example |
|--------|---------|
| GitHub shorthand | `npx skills add PrunaAI/pruna-ai-content-generation-skills/skills --skill p-image -y` |
| `@skill` shorthand | `npx skills add PrunaAI/pruna-ai-content-generation-skills/skills@p-image -y` |
| Full tree URL | `npx skills add https://github.com/PrunaAI/pruna-ai-content-generation-skills/tree/main/skills -y` |
| Single skill URL | `npx skills add https://github.com/PrunaAI/pruna-ai-content-generation-skills/tree/main/skills/p-image -y` |
| Global (`-g`) | `npx skills add PrunaAI/pruna-ai-content-generation-skills/skills --skill p-image -g -y` |

Always use the **`/skills`** path — not the repo root (root also discovers `.mine/` launch skills).

**From a local clone**

```bash
npx skills add ./skills --list
npx skills add ./skills --skill p-image --agent cursor -y
npx skills add ./skills --skill avatar-multi-scene --agent cursor -y
```

Restart Cursor or start a new chat. Installed paths look like `~/.cursor/skills/<name>/SKILL.md` or `.cursor/skills/<name>/SKILL.md`. Do not use `~/.cursor/skills-cursor/` (Cursor built-ins).

### APM

Install a skill path from GitHub (workflow bundles include **`apm.yml`** listing transitive tool skills):

```bash
apm install PrunaAI/pruna-ai-content-generation-skills/skills/p-image
apm install PrunaAI/pruna-ai-content-generation-skills/skills/avatar-multi-scene
```

Or declare deps in a project **`apm.yml`** and run `apm install`:

```yaml
dependencies:
  apm:
    - PrunaAI/pruna-ai-content-generation-skills/skills/avatar-multi-scene
```

### PSPM

Add from GitHub, then install into the project (each bundle ships **`pspm.json`** as `@pruna/<skill>`):

```bash
pspm add github:PrunaAI/pruna-ai-content-generation-skills/skills/p-image
pspm add github:PrunaAI/pruna-ai-content-generation-skills/skills/avatar-multi-scene
pspm install
```

Or pin in **`pspm.json`**:

```json
"githubDependencies": {
  "github:PrunaAI/pruna-ai-content-generation-skills/skills/avatar-multi-scene": "main"
}
```

### OpenClaw / ClawHub

Install from the repo git ref, then add each skill subpath (no single meta-install yet):

```bash
openclaw skills install git:PrunaAI/pruna-ai-content-generation-skills@main
# install skills/<name> from the cloned tree per skill
```

### Workflow dependencies

Workflow skills declare sibling tool skills in **`depends:`** frontmatter:

```yaml
depends:
  - p-image
  - p-image-edit
  - p-video-avatar
  - p-video-animate
```

Inspect machine-readable deps: `cat skills/avatar-multi-scene/skill.deps.json | jq '.depends, .resolvers'`

**Maintainers:** `./scripts/bundle_all_skills.sh` then commit `skills/`. Registry publish: [`catalog/PUBLISHING.md`](catalog/PUBLISHING.md) (`./scripts/publish_all_skills.sh --execute` with `PSPM_API_KEY`).

See each skill's `README-INSTALL.md` for details. Workflow runners that support phased generation default to **`--phase stills`** so you can review images before paying for video.

## Optional: validate skills locally

```bash
npx skills-ref validate ./skills/p-image
```

See [skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref) and [skill creation best practices](https://agentskills.io/skill-creation/best-practices).

## Fast path: agent workflows

Use workflow skills with phased curl (see each `catalog/tools/*/SKILL.md`) or portable runners:

```bash
export PRUNA_API_KEY="your_key"

# Upscale before/after slider from any still pair
python3 catalog/workflows/_shared/scripts/generate_upscale_comparison.py \
  --before assets/before.jpg --after assets/after.jpg \
  --output output/upscale-demo.mp4 --preset portrait

# Learning explainer (vertical) — edit plan.json first
python3 catalog/workflows/verticals/interactive-explainer/scripts/run_from_plan.py \
  --plan output/verticals/interactive-explainer/my-explainer/plan.json \
  --out-dir output/verticals/interactive-explainer/my-explainer \
  --final-name my_explainer_final.mp4

# Music video (vertical)
python3 catalog/workflows/verticals/music-video/scripts/run_from_plan.py \
  --plan output/verticals/music-video/my-music-video/plan.json \
  --out-dir output/verticals/music-video/my-music-video
```

For scenario routing, use [pruna-run](catalog/workflows/router/pruna-run/SKILL.md) or [pruna-generative-pipeline](catalog/workflows/router/pruna-generative-pipeline/SKILL.md). Example prompts live under [catalog/examples/workflows/](catalog/examples/README.md).

## Skill format (required for installability)

- **Directory name** must match the `name` field in `SKILL.md` YAML frontmatter (lowercase, hyphens, max 64 characters, no leading/trailing hyphen, no `--`). See the [Agent Skills specification](https://agentskills.io/specification).
- **`SKILL.md`** must include at least `name` and `description` (what the skill does and when to use it, including trigger phrases).

Optional: `scripts/`, `references/`, `assets/`, `license`, `compatibility`, `metadata`, and workflow-only **`depends:`** (sibling skill names) in frontmatter.

## Optional: Claude Code plugin

This repo includes [`.claude-plugin/plugin.json`](./.claude-plugin/plugin.json) listing every `SKILL.md` for Claude Code–style plugin installs. Adjust `name` / metadata when you publish. This is **not** required for Cursor manual install or for `npx skills add` targeting Cursor.

## API setup

| Service | Env var | Get a key |
|---------|---------|-----------|
| **Pruna** (images, video, try-on, upscale) | `PRUNA_API_KEY` | [dashboard.pruna.ai](https://dashboard.pruna.ai/) |
| **Replicate** (Music 2.5, TTS, Stable Audio, WhisperX) | `REPLICATE_API_TOKEN` | [replicate.com/account/api-tokens](https://replicate.com/account/api-tokens) |

```bash
export PRUNA_API_KEY="your_pruna_key"
export REPLICATE_API_TOKEN="r8_..."   # when using audio / song tools
```

Pruna uses the **`apikey`** HTTP header — see [pruna-api.md](./catalog/references/shared/pruna-api.md). Replicate uses **`Authorization: Bearer`** — see [replicate-api.md](./catalog/references/shared/replicate-api.md).

**Agents:** if a required key is missing, do not call paid APIs — use the signup templates in [api-credentials.md](./catalog/references/shared/api-credentials.md).

## Contributing

We welcome fixes and improvements to skills, references, and bundled install packages.

### What to change where

| You want to… | Edit here | Then run |
|--------------|-----------|----------|
| Model API usage or examples | `catalog/tools/<modality>/<skill>/SKILL.md` | `./scripts/bundle_skill.sh <skill>` |
| Workflow steps or scene plans | `catalog/workflows/**/SKILL.md` | `./scripts/bundle_skill.sh <skill>` |
| Shared API or quality rules | `catalog/references/shared/` or `catalog/references/<modality>/` | `./scripts/bundle_all_skills.sh` |
| Which files ship in an install | `<skill>/skill.manifest.json` | `./scripts/bundle_skill.sh <skill>` |
| Package version | `VERSION` | `python3 scripts/sync_skill_versions.py` then `./scripts/bundle_all_skills.sh` |

Source of truth is **`catalog/`**. The **`skills/`** folder is generated — edit catalog first; **pre-commit** rebuilds bundles when catalog changes (`pip install pre-commit && pre-commit install`).

### Pull request checklist

1. `SKILL.md` frontmatter `name` matches the folder name ([Agent Skills spec](https://agentskills.io/specification)).
2. New or changed references are listed in `skill.manifest.json`; workflow deps in `tool_skills` (bundled as `depends:`).
3. `./scripts/bundle_all_skills.sh` (or `bundle_skill.sh` for a single skill) and commit the updated `skills/` tree when install bundles change.
4. `npx skills-ref validate ./skills/<skill-name>` passes for skills you touched.
5. No API keys, tokens, or generated media in the commit.

### Style for skill text

- Write for someone new to the repo — avoid insider abbreviations in README and skill intros (say “narration” not “VO”, “background footage” not “B-roll” unless the API field name requires it).
- Prefer full sentences in tables and descriptions over arrow chains (`A → B → C`).
- If another vendor already ships a skill named `p-image`, use a `pruna-` prefix in both folder and frontmatter `name` (for example `pruna-p-image`).
- Pruna-internal campaign work belongs in `.mine/`, not the public `skills/` bundles.

### Questions and larger changes

Open a GitHub issue on [PrunaAI/pruna-ai-content-generation-skills](https://github.com/PrunaAI/pruna-ai-content-generation-skills) before large refactors (new workflow tier, manifest format changes, or removing skills). For typos and small doc fixes, a pull request is enough.

## License

See [LICENSE](./LICENSE).
