# pruna-ai-content-generation-skills

Agent skills for content generation with the [Pruna AI API](https://docs.api.pruna.ai/guides/models): image generation and editing, video and avatar video, upscaling, and composed workflows (for example avatar concept pipelines).

Skills follow the [Agent Skills](https://agentskills.io/specification) layout so they can be installed manually in Cursor, via the `skills` CLI, and optionally registered for Claude Code.

## Layout (as implemented)

```text
references/
  pruna-api.md          # Auth, endpoints, sync/async, uploads
  parallel-execution.md # Async parallel batches, phased deps, subagent splits
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
  p-video-animate/      # Animate reference image from source video motion
  p-video-replace/      # Replace people in source video (1–4 identity images per call)
tools/audio/
  stable-audio-2.5/     # Replicate instrumental bed for launch reels (mix under VO)
  music-2.5/            # Replicate full songs with vocals (MiniMax Music 2.5)
guides/workflows/
  pruna-run/                     # Fast prompt -> generation entrypoint
  pruna-generative-pipeline/   # Scenario hub (mood board, I2V, packs…) + intake
  single-scene-avatar-video/   # Intake → one p-video-avatar
  multi-scene-avatar-video/    # Intake → stills + p-video-avatar and/or p-video-animate slider beats + assembly
  single-scene-ai-video/        # Intake → one p-video
  multi-scene-ai-video/        # Intake scene table → p-video per scene + assembly
  p-image-upscale-comparison/  # Before/after zoom + slider demo from any still pair
  p-video-animate-comparison/  # Redirect stub → use multi-scene-avatar-video animate rows
  p-video-replace-comparison/  # Multi-scene replace sliders (p-image + avatar + replace)
  ai-music-video/              # Lyrics → Music 2.5 song → avatar + B-roll music video
examples/workflows/
  */example-prompt.md          # copy/paste prompt starters by workflow
  p-image-upscale-comparison/scripts/  # repo-only gallery batch (not portable)
guides/workflows/
  _shared/scripts/             # Shared renderers + pruna_paths + pruna_api
  */scripts/                   # Portable runners bundled per workflow skill
scripts/
  install_skill.sh             # Assemble portable skill bundle to ~/.cursor/skills/
  generate_upscale_comparison.py       # Backward-compat wrapper → _shared
  generate_video_animate_comparison.py   # Backward-compat wrapper → _shared
  run_p_video_replace_announcement.py  # Backward-compat wrapper → replace run_from_plan
  run_p_video_animate_announcement.py  # Backward-compat wrapper → animate run_from_plan
  requirements-comparison.txt  # Legacy; prefer guides/workflows/*/scripts/requirements.txt
.claude-plugin/
  plugin.json           # Claude Code plugin skill list (optional)
```

Atomic skills link to `references/` instead of duplicating long API tables.

## Skills in this repo

| `name` (folder) | Role |
|-----------------|------|
| `p-image` | `Model: p-image` — T2I, aspect ratios, optional LoRA |
| `p-image-edit` | `Model: p-image-edit` — prompt + 1–5 image URLs |
| `p-image-upscale` | `Model: p-image-upscale` — target MP (1–128), enhance flags |
| `p-video` | `Model: p-video` — T2V, I2V, optional audio |
| `p-video-avatar` | `Model: p-video-avatar` — portrait + `voice_script` or `audio` |
| `p-video-animate` | `Model: p-video-animate` — *animate this picture with motion* — one `image` + motion-template `video` |
| `p-video-replace` | `Model: p-video-replace` — *replace this person in this video* — source `video` + 1–4 identity `images` in one call |
| `stable-audio-2.5` | Replicate — instrumental background bed for launch reels (mix under VO via `launch_background_music.py`) |
| `music-2.5` | Replicate — full songs with vocals from lyrics + style prompt ([MiniMax Music 2.5](https://replicate.com/minimax/music-2.5)) |
| `pruna-generative-pipeline` | Scenario hub: mood board, hero+variants, I2V, audio-led video, draft→final, links to full scene workflows |
| `single-scene-avatar-video` | Workflow: intake → one still + slop + one `p-video-avatar` |
| `multi-scene-avatar-video` | Workflow: character sheet + scene table (`avatar` and/or `animate` rows) + locked seeds + natural voice + hero → edit → parallel async `p-video-avatar` / `p-video-animate` + slider renders + assembly |
| `single-scene-ai-video` | Workflow: intake → one `p-video` |
| `multi-scene-ai-video` | Workflow: intake scene table → parallel async `p-video` per scene + optional subagents + assembly |
| `p-image-upscale-comparison` | Workflow: any pre/post upscale still pair → zoom stops + slider sweeps MP4 |
| `p-video-animate-comparison` | Redirect stub — use `multi-scene-avatar-video` for animate slider beats |
| `p-video-replace-comparison` | Workflow: character/clothing/object/mixed swaps with prompt-guided mapping, dynamic sources, natural VO, slider compare MP4s |
| `ai-music-video` | Workflow: lyrics → Music 2.5 song → cut-safe line map → `p-video-avatar` performance + `p-video` B-roll → ffmpeg assembly |
| `pruna-run` | Fast entrypoint: auto-route prompt to image/i2v/avatar/I-L |

## Portable workflow install

```bash
./scripts/install_skill.sh p-video-replace-comparison
./scripts/install_skill.sh p-video-animate-comparison
./scripts/install_skill.sh p-image-upscale-comparison
./scripts/install_skill.sh multi-scene-avatar-video
```

See each workflow's `README-INSTALL.md` for run commands. Default plan runners use **`--phase stills`** (human-in-the-loop gate).

## Fast path: agent workflows

Use workflow skills with phased curl (see each `tools/*/SKILL.md`) or portable runners:

```bash
export PRUNA_API_KEY="your_key"

# Replace comparison reel — stills first, then video after approval
python3 guides/workflows/p-video-replace-comparison/scripts/run_from_plan.py \
  --plan output/p-video-replace-announcement/announcement_plan.json \
  --out-dir output/p-video-replace-announcement \
  --phase stills

# Upscale before/after slider from any still pair
python3 guides/workflows/p-image-upscale-comparison/scripts/generate_upscale_comparison.py \
  --before assets/before.jpg --after assets/after.jpg \
  --output output/upscale-demo.mp4 --preset portrait
```

For scenario routing, use the [pruna-run](guides/workflows/pruna-run/SKILL.md) and [pruna-generative-pipeline](guides/workflows/pruna-generative-pipeline/SKILL.md) workflow skills in Cursor.

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
