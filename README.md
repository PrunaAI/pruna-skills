# pruna-ai-content-generation-skills

Agent skills for content generation with the [Pruna AI API](https://docs.api.pruna.ai/guides/models): image generation and editing, video and avatar video, upscaling, and composed workflows (for example avatar concept pipelines).

Skills follow the [Agent Skills](https://agentskills.io/specification) layout so they can be installed manually in Cursor, via the `skills` CLI, and optionally registered for Claude Code.

## Layout (as implemented)

```text
references/                        # specs + QA (by modality — see references/README.md)
  shared/     pruna-api, pruna-models, parallel-execution, generation-quality-checklists, …
  image/      p-image* quality checklists
  video/      p-video* checklists, scene-anchor-triple, scene-anchor-pair
  audio/      audio-post-production
  workflows/  interactive-explainer-scenes, music-video-quality-checklist, …

tools/
  image/   p-image, p-image-edit, p-image-upscale
  video/   p-video, p-video-avatar, p-video-animate, p-video-replace
  audio/   gemini-3.1-flash-tts, music-2.5, stable-audio-2.5

guides/workflows/                  # see “Workflow organization” below
  _shared/scripts/
  router/        pruna-run, pruna-generative-pipeline
  core/          image-to-video, narrated-multi-scene, visual-transition-reel, avatar-*
  verticals/     interactive-explainer, music-video
  launches/      p-image-upscale-comparison, p-video-animate-comparison, p-video-replace-comparison

examples/workflows/              # mirrors core/ + verticals/ + launches (see examples/README.md)
  core/visual-transition-reel/
  verticals/interactive-explainer/, music-video/
  launches/p-image-upscale-comparison/, …

output/                          # generated projects (see output/README.md)
  core/, verticals/, launches/    # same tier names as guides/workflows

scripts/install_skill.sh
.claude-plugin/plugin.json
```

Atomic **tool** skills link to `references/` instead of duplicating API tables. **Workflow** skills layer intake, scene tables, and runners on top of tools + `core/`.

## Workflow organization

| Layer | Path | Pick when |
|-------|------|-----------|
| **Router** | `guides/workflows/router/` (`pruna-run`, `pruna-generative-pipeline`) | User has not chosen a pipeline yet |
| **Core** | `guides/workflows/core/*` | You know the **scene pattern** (one beat, triple + VO, pair transitions, avatar table) |
| **Vertical** | `guides/workflows/verticals/*` | You know the **deliverable** (explainer, music video) |
| **Launches** | `guides/workflows/launches/*` | Before/after or slider demo reels (not a product vertical) |

**Start here:** [pruna-generative-pipeline](guides/workflows/router/pruna-generative-pipeline/SKILL.md) (recipes A–R) or [pruna-run](guides/workflows/router/pruna-run/SKILL.md) (fast single-shot routing).

### Core skills (scene grammar)

| Folder | Former name | Use for |
|--------|-------------|---------|
| [image-to-video](guides/workflows/core/image-to-video/SKILL.md) | `single-scene-ai-video` | One `p-video` beat (triple, I2V, T2V) |
| [narrated-multi-scene](guides/workflows/core/narrated-multi-scene/SKILL.md) | `multi-scene-ai-video` | Scene anchor triple → parallel `p-video` + concat |
| [visual-transition-reel](guides/workflows/core/visual-transition-reel/SKILL.md) | `scene-transition-video` | Pair anchors, motion between stills, no VO |
| [avatar-single-scene](guides/workflows/core/avatar-single-scene/SKILL.md) | `single-scene-avatar-video` | One `p-video-avatar` |
| [avatar-multi-scene](guides/workflows/core/avatar-multi-scene/SKILL.md) | `multi-scene-avatar-video` | Multi-scene avatar / animate + assembly |

### Vertical skills (deliverables)

| Folder | Former name | Use for |
|--------|-------------|---------|
| [interactive-explainer](guides/workflows/verticals/interactive-explainer/SKILL.md) | `educational-explainer` | Learning explainers (history, science, biography): narrator + character dialogue |
| [music-video](guides/workflows/verticals/music-video/SKILL.md) | `ai-music-video` | Song-led video (Music 2.5 + cut map + avatar/B-roll) |

Explainer specs: [interactive-explainer-scenes.md](references/workflows/interactive-explainer-scenes.md). Full model index: [pruna-models.md](references/shared/pruna-models.md).

**Also aligned with workflows:** [examples/](examples/README.md) (`core/`, `verticals/`, `launches/`) and [output/](output/README.md) use the same tier names for project folders.

## Skills in this repo

| `name` (folder) | Role |
|-----------------|------|
| `p-image` | `Model: p-image` — T2I, aspect ratios, optional LoRA |
| `p-image-edit` | `Model: p-image-edit` — prompt + 1–5 image URLs |
| `p-image-upscale` | `Model: p-image-upscale` — target MP (1–128), enhance flags |
| `p-video` | `Model: p-video` — T2V, I2V, first+last frame chaining, optional audio |
| `p-video-avatar` | `Model: p-video-avatar` — portrait + `voice_script` or `audio` |
| `p-video-animate` | `Model: p-video-animate` — *animate this picture with motion* — one `image` + motion-template `video` |
| `p-video-replace` | `Model: p-video-replace` — *replace this person in this video* — source `video` + 1–4 identity `images` in one call |
| `stable-audio-2.5` | Replicate — instrumental background bed for launch reels (mix under VO via `launch_background_music.py`) |
| `music-2.5` | Replicate — full songs with vocals from lyrics + style prompt ([MiniMax Music 2.5](https://replicate.com/minimax/music-2.5)) |
| `gemini-3.1-flash-tts` | Replicate — narration / voiceover with style prompts ([Gemini 3.1 Flash TTS](https://replicate.com/google/gemini-3.1-flash-tts)) |
| `pruna-generative-pipeline` | Scenario hub: mood board, hero+variants, I2V, audio-led video, draft→final, links to core/vertical skills |
| `pruna-run` | Fast entrypoint: auto-route prompt to image/i2v/avatar/I-L |
| **Core** | |
| `image-to-video` | One `p-video` beat — scene anchor triple or I2V/T2V |
| `narrated-multi-scene` | Scene anchor triple → parallel `p-video` + assembly |
| `visual-transition-reel` | Scene anchor pair → transitions + concat (no VO) |
| `avatar-single-scene` | One `p-video-avatar` after intake + slop gate |
| `avatar-multi-scene` | Scene table (`avatar` / `animate` rows) + assembly |
| **Verticals** | |
| `interactive-explainer` | Learning explainers: narrator triple + character `p-video-avatar` |
| `music-video` | Lyrics → Music 2.5 → avatar + B-roll → assembly |
| **Launches** | |
| `p-image-upscale-comparison` | Before/after upscale slider MP4 |
| `p-video-animate-comparison` | Redirect stub — use `avatar-multi-scene` animate rows |
| `p-video-replace-comparison` | In-video replace slider demos |

## Portable workflow install

`install_skill.sh` looks for skills under `router/`, `core/`, `verticals/`, and `launches/`, then bundles `SKILL.md`, manifests, templates, references, and `_shared` scripts into `~/.cursor/skills/<name>/`.

```bash
# Router
./scripts/install_skill.sh pruna-generative-pipeline

# Core
./scripts/install_skill.sh narrated-multi-scene
./scripts/install_skill.sh avatar-multi-scene
./scripts/install_skill.sh visual-transition-reel

# Verticals
./scripts/install_skill.sh interactive-explainer
./scripts/install_skill.sh music-video

# Launches
./scripts/install_skill.sh p-image-upscale-comparison
./scripts/install_skill.sh p-video-replace-comparison
```

**Legacy folder names** (still accepted by `install_skill.sh`):

| Old name | Installs |
|----------|----------|
| `single-scene-ai-video` | `image-to-video` |
| `multi-scene-ai-video` | `narrated-multi-scene` |
| `scene-transition-video` | `visual-transition-reel` |
| `single-scene-avatar-video` | `avatar-single-scene` |
| `multi-scene-avatar-video` | `avatar-multi-scene` |
| `educational-explainer` | `interactive-explainer` |
| `documentary-explainer` | `interactive-explainer` |
| `ai-music-video` | `music-video` |

See each skill's `README-INSTALL.md` under its folder for run commands. Plan runners that support it default to **`--phase stills`** (human-in-the-loop gate).

## Fast path: agent workflows

Use workflow skills with phased curl (see each `tools/*/SKILL.md`) or portable runners:

```bash
export PRUNA_API_KEY="your_key"

# Replace comparison reel — stills first, then video after approval
python3 guides/workflows/launches/p-video-replace-comparison/scripts/run_from_plan.py \
  --plan output/launches/p-video-replace-announcement/announcement_plan.json \
  --out-dir output/launches/p-video-replace-announcement \
  --phase stills

# Upscale before/after slider from any still pair
python3 guides/workflows/launches/p-image-upscale-comparison/scripts/generate_upscale_comparison.py \
  --before assets/before.jpg --after assets/after.jpg \
  --output output/upscale-demo.mp4 --preset portrait

# Learning explainer (vertical) — edit plan.json first
python3 guides/workflows/verticals/interactive-explainer/scripts/run_from_plan.py \
  --plan output/verticals/interactive-explainer/my-explainer/plan.json \
  --out-dir output/verticals/interactive-explainer/my-explainer \
  --final-name my_explainer_final.mp4

# Music video (vertical)
python3 guides/workflows/verticals/music-video/scripts/run_from_plan.py \
  --plan output/verticals/music-video/my-music-video/plan.json \
  --out-dir output/verticals/music-video/my-music-video
```

For scenario routing, use [pruna-run](guides/workflows/router/pruna-run/SKILL.md) or [pruna-generative-pipeline](guides/workflows/router/pruna-generative-pipeline/SKILL.md). Example prompts live under [examples/workflows/](examples/workflows/).

## Skill format (required for installability)

- **Directory name** must match the `name` field in `SKILL.md` YAML frontmatter (lowercase, hyphens, max 64 characters, no leading/trailing hyphen, no `--`). See the [Agent Skills specification](https://agentskills.io/specification).
- **`SKILL.md`** must include at least `name` and `description` (what the skill does and when to use it, including trigger phrases).

Optional: `scripts/`, `references/`, `assets/`, `license`, `compatibility`, `metadata` in frontmatter. For Cursor-only behavior (for example load when explicitly invoked), you can set `disable-model-invocation: true` in frontmatter where appropriate.

## Installing in Cursor (manual)

**Personal (all projects):**

```bash
mkdir -p ~/.cursor/skills
cp -R path/to/pruna-ai-content-generation-skills/tools/image/p-image ~/.cursor/skills/
# repeat for each skill directory you want
```

**Project-only (checked into another repo):**

```bash
mkdir -p .cursor/skills
cp -R path/to/pruna-ai-content-generation-skills/guides/workflows/verticals/interactive-explainer .cursor/skills/
# or: core/narrated-multi-scene, verticals/music-video, tools/image/p-image, …
```

Prefer `./scripts/install_skill.sh <skill-name>` so references and `_shared` scripts are copied automatically.

Restart Cursor or start a new chat so skills are discovered. Installed path should look like:

```text
~/.cursor/skills/<skill-name>/SKILL.md
```

or

```text
.cursor/skills/<skill-name>/SKILL.md
```

Do not install into `~/.cursor/skills-cursor/`; that tree is reserved for Cursor built-in skills.

## Installing with `npx skills` (CLI)

The [skills](https://www.npmjs.com/package/skills) CLI can install skills from a Git repository or a local path into configured agents.

**From GitHub (after this repo is published):**

```bash
npx skills add <org>/pruna-ai-content-generation-skills --agent cursor
```

**From a local clone (smoke test and development):**

```bash
cd /path/to/pruna-ai-content-generation-skills
npx skills add . --agent cursor --list
```

Use `--list` to see which skills the CLI detects before copying. If your CLI version supports installing a subset, use its flag (often `--skill <name>`) to install only selected skills.

**Updates:** use your CLI’s update command (for example `npx skills update`) or re-run `add` after pulling the repo, depending on the version you use.

## Optional: validate skills locally

The Agent Skills project provides a validator to catch frontmatter and naming issues:

```bash
npx skills-ref validate ./tools/image/p-image
```

See [skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref). Run once per skill directory (or in CI over each leaf folder containing `SKILL.md`).

## Optional: Claude Code plugin

This repo includes [`.claude-plugin/plugin.json`](./.claude-plugin/plugin.json) listing every `SKILL.md` for Claude Code–style plugin installs. Adjust `name` / metadata when you publish. This is **not** required for Cursor manual install or for `npx skills add` targeting Cursor.

## API setup

Set **`PRUNA_API_KEY`** for shell examples. Pruna uses the **`apikey`** HTTP header (see [references/shared/pruna-api.md](./references/shared/pruna-api.md) and the [Quickstart](https://docs.api.pruna.ai/guides/quickstart)).

## Naming and side-by-side installs

If users might already have another vendor’s skill named `p-image`, consider a **`pruna-` prefix** in both folder name and `name:` frontmatter (for example `pruna-p-image`) so two installs do not collide. Folder name and `name` must still match exactly.

## What to decide for your team

| Topic | Why it matters |
|--------|----------------|
| Cursor vs Claude Code vs both | Drives whether you maintain `.claude-plugin/plugin.json` and which install sections you emphasize. |
| Public vs private GitHub | `npx skills add` against private repos may need auth; document the expected method. |
| Skill discovery from this repo | Run `npx skills add . --list` from the repo root and adjust layout or docs if the CLI does not discover nested paths as expected. |
| Canonical auth and base URL | Already centralized in `references/shared/pruna-api.md`; keep skills linking there. |

## License

See [LICENSE](./LICENSE).
