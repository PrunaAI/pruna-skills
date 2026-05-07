# pruna-ai-content-generation-skills

Agent skills for content generation with the [Pruna AI API](https://docs.api.pruna.ai/guides/models): image generation and editing, video and avatar video, upscaling, and composed workflows (for example avatar concept pipelines).

Skills follow the [Agent Skills](https://agentskills.io/specification) layout so they can be installed manually in Cursor, via the `skills` CLI, and optionally registered for Claude Code.

## Layout (as implemented)

```text
references/
  pruna-api.md          # Auth, endpoints, sync/async, uploads
  pruna-models.md       # Index of models and skill paths
  generation-quality-checklists.md # QA hub (core gate + links to per-model checklists)
  avatar-still-quality-checklist.md # Compatibility alias to QA hub
tools/image/
  p-image/              # Text-to-image
  p-image-edit/         # Edit / compose 1–5 images
  p-image-upscale/      # Upscale and optional enhance
tools/video/
  p-video/              # Text / image / audio video
  p-video-avatar/       # Talking head from portrait + script or audio
guides/workflows/
  pruna-run/                     # Fast prompt -> generation entrypoint
  pruna-generative-pipeline/   # Scenario hub (mood board, I2V, packs…) + intake
  single-scene-avatar-video/   # Intake → one p-video-avatar
  multi-scene-avatar-video/    # Intake → stills + p-video-avatar per scene + assembly
  single-scene-ai-video/        # Intake → one p-video
  multi-scene-ai-video/        # Intake scene table → p-video per scene + assembly
examples/workflows/
  */example-prompt.md          # copy/paste prompt starters by workflow
scripts/
  pruna_run.py                 # Unified prompt -> run entrypoint
  run_pruna_generative_pipeline_examples.py # Route I-L runner
  run_workflow_examples.py     # Workflow executors used by route runner
.claude-plugin/
  plugin.json           # Claude Code plugin skill list (optional)
```

Atomic skills link to `references/` instead of duplicating long API tables.

## Skills in this repo

| `name` (folder) | Role |
|-----------------|------|
| `p-image` | `Model: p-image` — T2I, aspect ratios, optional LoRA |
| `p-image-edit` | `Model: p-image-edit` — prompt + 1–5 image URLs |
| `p-image-upscale` | `Model: p-image-upscale` — target MP, enhance flags |
| `p-video` | `Model: p-video` — T2V, I2V, optional audio |
| `p-video-avatar` | `Model: p-video-avatar` — portrait + `voice_script` or `audio` |
| `pruna-generative-pipeline` | Scenario hub: mood board, hero+variants, I2V, audio-led video, draft→final, links to full scene workflows |
| `single-scene-avatar-video` | Workflow: intake → one still + slop + one `p-video-avatar` |
| `multi-scene-avatar-video` | Workflow: intake → Pruna stills + `p-video-avatar` per scene + assembly |
| `single-scene-ai-video` | Workflow: intake → one `p-video` |
| `multi-scene-ai-video` | Workflow: intake scene table → one `p-video` per scene + assembly |
| `pruna-run` | Fast entrypoint: auto-route prompt to image/i2v/avatar/I-L |

## Fast path: prompt -> generation

Use this when you want direct execution with minimal ceremony.

```bash
export PRUNA_API_KEY="your_key"

# Auto route from one incoming prompt
python3 scripts/pruna_run.py --prompt "cinematic launch teaser for our product"

# Force a chained path
python3 scripts/pruna_run.py --route i2v --prompt "hand-drawn mascot reveal clip"

# Talking avatar (requires script line)
python3 scripts/pruna_run.py \
  --route avatar \
  --prompt "friendly spokesperson portrait" \
  --voice-script "Hi, here is your one-line launch message."
```

For scenario-hub routes I-L:

```bash
python3 scripts/run_pruna_generative_pipeline_examples.py --route I
python3 scripts/run_pruna_generative_pipeline_examples.py --route all
```

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
cp -R path/to/pruna-ai-content-generation-skills/guides/workflows/multi-scene-avatar-video .cursor/skills/
```

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

Set **`PRUNA_API_KEY`** for shell examples. Pruna uses the **`apikey`** HTTP header (see [references/pruna-api.md](./references/pruna-api.md) and the [Quickstart](https://docs.api.pruna.ai/guides/quickstart)).

## Naming and side-by-side installs

If users might already have another vendor’s skill named `p-image`, consider a **`pruna-` prefix** in both folder name and `name:` frontmatter (for example `pruna-p-image`) so two installs do not collide. Folder name and `name` must still match exactly.

## What to decide for your team

| Topic | Why it matters |
|--------|----------------|
| Cursor vs Claude Code vs both | Drives whether you maintain `.claude-plugin/plugin.json` and which install sections you emphasize. |
| Public vs private GitHub | `npx skills add` against private repos may need auth; document the expected method. |
| Skill discovery from this repo | Run `npx skills add . --list` from the repo root and adjust layout or docs if the CLI does not discover nested paths as expected. |
| Canonical auth and base URL | Already centralized in `references/pruna-api.md`; keep skills linking there. |

## License

See [LICENSE](./LICENSE).
