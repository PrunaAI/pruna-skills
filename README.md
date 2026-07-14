# Pruna Skills

![Pruna Skills — images, video, music, explainers, avatars, and workflows for agent coding tools](docs/assets/readme-hero-pruna-skills.png)

Agent skills for generating images, video, and audio with the [Pruna AI API](https://docs.api.pruna.ai/guides/models), plus multi-step workflows for explainers, music videos, and similar projects. Source: [PrunaAI/pruna-skills](https://github.com/PrunaAI/pruna-skills).

Skills follow the [Agent Skills](https://agentskills.io/specification) format. You author in `tools/`, `guides/`, and `workflows/` at the repo root. To install, pick either a single **skill** (one `SKILL.md` folder) or a **plugin** bundle from `plugins/<name>/` — the latter includes the manifest, skills, and any workflow dependencies in one package. Your agent's installer determines which command to use; the [quickstart](#quickstart) covers the common cases.

## Quickstart

You'll need a Pruna API key — see [api-setup.md](api-setup.md):

```bash
export PRUNA_API_KEY="your_key"
```

### One image skill (`p-image`)

The fastest way in, no clone required:

```bash
npx skills add PrunaAI/pruna-skills@p-image -y
```

Restart the agent or open a new chat, then try: "Generate a product hero still with p-image."

If you want a native plugin install instead (Claude Code, Cursor, Copilot CLI, VS Code), clone the repo first:

```bash
git clone https://github.com/PrunaAI/pruna-skills && cd pruna-skills
npx plugins add ./plugins/p-image -y
```

In Claude Code you can also run `/plugin marketplace add PrunaAI/pruna-skills` and then `/plugin install p-image@pruna-skills`.

### Everything at once

All skills, without a plugin manifest:

```bash
npx skills add PrunaAI/pruna-skills/plugins/pruna-full/skills -y
```

Or the full suite as a plugin (clone required):

```bash
git clone https://github.com/PrunaAI/pruna-skills && cd pruna-skills
npx plugins add ./plugins/pruna-full -y
```

In Claude Code: `/plugin marketplace add PrunaAI/pruna-skills` then `/plugin install pruna-full@pruna-skills`.

After cloning, `npx plugins discover ./plugins` lists every bundle. For other agents and install paths, see [Install channels](#install-channels).

## Contents

- [Quickstart](#quickstart)
- [How this repo works](#how-this-repo-works)
- [Install channels](#install-channels)
- [Choosing an approach](#choosing-an-approach)
- [Install skills (`npx skills`)](#install-skills-npx-skills)
- [Install plugins (`npx plugins`)](#install-plugins-npx-plugins)
- [Claude / Copilot marketplace](#claude--copilot-marketplace)
- [ClawHub / OpenClaw](#clawhub--openclaw)
- [Other installers](#other-installers)
- [API Setup](#api-setup)
- [Available Skills](#available-skills)
- [Contributing](#contributing)

---

## How this repo works

You edit source in `tools/`, `guides/`, and `workflows/`. `./scripts/bundle_all_skills.sh` copies that into `plugins/<name>/` for plugin-based installs — don't edit `plugins/` directly; pre-commit rebuilds it.

| | Source tree | Generated plugins |
|--|-------------|-------------------|
| Paths | `tools/`, `guides/`, `workflows/` | `plugins/<name>/` |
| Edit? | Yes | No |
| Contents | Primary `SKILL.md` + refs/scripts | `.claude-plugin/plugin.json` + `skills/<name>/` (+ embedded deps for workflows) |
| Typical install | `npx skills add …@<name>` | `npx plugins add ./plugins/<name>`, `/plugin install`, ClawHub |

There are three content tiers — **tools** (`p-image`, `p-video`, …) call paid APIs; **guides** (`generation-diversity`, `recipe-catalog`) don't; **workflows** (`music-video`, `pruna-run`) orchestrate tools and do.

Plugin bundles come in three sizes: standalone (`plugins/p-image/`), workflow with embedded deps (`plugins/music-video/`), or the full suite (`plugins/pruna-full/`).

```text
tools/  guides/  workflows/     ──bundle──►  plugins/<name>/
     (author here)                            (install as plugin)
```

---

## Install channels

`npx skills`, `npx plugins`, Claude's marketplace, and ClawHub all install from this repo but not always the same way. Skills are individual `SKILL.md` folders; plugins are the bundled packages under `plugins/`. For a workflow, install either the fat plugin or the individual tool skills — not both, or you'll get duplicate names.

| Channel | Skill install | Plugin install | Agents |
|---------|---------------|----------------|--------|
| [skills CLI](https://github.com/vercel-labs/skills) + [skills.sh](https://skills.sh) | `npx skills add PrunaAI/pruna-skills@p-image -y` | `npx skills add …/plugins/music-video/skills --skill music-video -y` | Cursor, Codex, Claude Code, 68+ |
| [plugins CLI](https://www.npmjs.com/package/plugins) | — | `npx plugins add ./plugins/p-image -y` | Claude Code, Cursor, Copilot CLI, VS Code, Codex, … |
| Claude marketplace | — | `/plugin install music-video@pruna-skills` | Claude Code, Copilot CLI, VS Code |
| ClawHub | `clawhub install @PrunaAI/p-image` | `openclaw plugins install clawhub:@PrunaAI/music-video` | OpenClaw |
| APM | `apm install PrunaAI/pruna-skills/plugins/p-image/skills/p-image` | same path for bundles | Copilot, Claude, Cursor, Codex, … |
| Git copy | `cp -r tools/image/p-image ~/.cursor/skills/p-image` | `cp -r plugins/p-image …` | Any |

More on how these relate: [skill-package-managers.md](references/shared/skill-package-managers.md).

---

## Choosing an approach

| Goal | Command |
|------|---------|
| One image tool in Cursor | `npx skills add PrunaAI/pruna-skills@p-image -y` |
| Same tool as a native plugin | `npx plugins add ./plugins/p-image -y` |
| Music video in Claude Code | `/plugin install music-video@pruna-skills` |
| Music video via plugins CLI | `npx plugins add ./plugins/music-video -y` |
| Music video, skills only | `npx skills add …/plugins/music-video/skills --skill music-video -y` |
| Full suite | `npx plugins add ./plugins/pruna-full -y` or `/plugin install pruna-full@pruna-skills` |
| Team lockfile | `apm install PrunaAI/pruna-skills/plugins/music-video/skills/music-video` |
| OpenClaw, one skill | `clawhub install @PrunaAI/p-image` |
| OpenClaw, workflow bundle | `openclaw plugins install clawhub:@PrunaAI/music-video` |

**Which skill to start with:**

| Situation | Start with |
|-----------|------------|
| Generate one image | Tool: `p-image` |
| Prompts look repetitive | Guide: `generation-diversity` |
| Which workflow fits? | Guide: `recipe-catalog` or Router: `pruna-generative-pipeline` |
| One narrated clip from stills | Core: `image-to-video` |
| Full music video | Vertical: `music-video` |
| Not sure yet | Router: `pruna-run` |

**Watch out for:**

- Editing `plugins/` by hand — pre-commit overwrites it; change `tools/`, `guides/`, or `workflows/` instead.
- Installing a workflow plugin and the same tools as standalone skills.
- Expecting one publish command for every channel — see [PUBLISHING.md](PUBLISHING.md).

---

## Install skills (`npx skills`)

The [skills CLI](https://github.com/vercel-labs/skills) copies `SKILL.md` folders into your agent. It won't install plugin manifests, hooks, or MCP configs — use [`npx plugins`](#install-plugins-npx-plugins) or a marketplace for that.

You can install from the source tree (`@p-image`) for a thin single skill, or from `plugins/<name>/skills` to get the same skill files a plugin bundle would include:

```bash
# List all
npx skills add PrunaAI/pruna-skills -l

# From source tree
npx skills add PrunaAI/pruna-skills@p-image -y
npx skills add PrunaAI/pruna-skills@generation-diversity -y

# From a plugin bundle (skills only)
npx skills add PrunaAI/pruna-skills/plugins/music-video/skills --skill music-video -y
npx skills add PrunaAI/pruna-skills/plugins/p-image/skills --skill p-image -y
npx skills add PrunaAI/pruna-skills/plugins/pruna-full/skills -y

# Local clone
npx skills add ./tools/image/p-image -y
npx skills add ./plugins/music-video/skills --skill music-video -y
```

Publishing is a git push plus tag `skills-v<VERSION>`; [skills.sh](https://skills.sh) indexes installs from telemetry. Details in [PUBLISHING.md](PUBLISHING.md).

Restart Cursor or start a new chat after install.

---

## Install plugins (`npx plugins`)

The [plugins CLI](https://www.npmjs.com/package/plugins) installs full plugin bundles into Claude Code, Cursor, Copilot CLI, VS Code, Codex, and others. Each folder under `plugins/<name>/` is one plugin.

Clone the repo first, then:

```bash
npx plugins discover ./plugins
npx plugins add ./plugins/p-image -y
npx plugins add ./plugins/music-video -y
npx plugins add ./plugins/pruna-full -y

# Optional: target one agent
npx plugins add ./plugins/p-image -y --target cursor
```

Publishing is just pushing `plugins/` and `.claude-plugin/marketplace.json` to GitHub — see [PUBLISHING.md](PUBLISHING.md).

---

## Claude / Copilot marketplace

In Claude Code:

```bash
/plugin marketplace add PrunaAI/pruna-skills
/plugin install pruna-full@pruna-skills
/plugin install p-image@pruna-skills
/plugin install music-video@pruna-skills
```

Copilot CLI: `copilot plugin install pruna-full@pruna-skills`

The marketplace lives in the repo — commit `.claude-plugin/marketplace.json` and `plugins/`; no separate store upload ([PUBLISHING.md](PUBLISHING.md)).

---

## ClawHub / OpenClaw

Released to [ClawHub](https://docs.openclaw.ai/clawhub) on each version tag.

Single skill:

```bash
clawhub install @PrunaAI/p-image
```

Plugin bundle (workflow + embedded deps, or full suite):

```bash
openclaw plugins install clawhub:@PrunaAI/music-video
openclaw plugins install clawhub:@PrunaAI/pruna-full
```

ClawHub slugs hyphenate dots in names (`music-2.5` → `@PrunaAI/music-2-5`). Publish via `./scripts/publish_all_skills.sh --execute` — [PUBLISHING.md](PUBLISHING.md).

---

## Other installers

**APM** — team lockfiles from GitHub paths:

```bash
apm install PrunaAI/pruna-skills/plugins/p-image/skills/p-image
apm install PrunaAI/pruna-skills/plugins/music-video/skills/music-video
```

**Manual copy:**

```bash
cp -r tools/image/p-image ~/.claude/skills/p-image
```

---

## API Setup

See [api-setup.md](api-setup.md) for `PRUNA_API_KEY`, `REPLICATE_API_TOKEN`, and HTTP details.

---

<!-- README.skills.md inserted below -->
## Available Skills

### Tools — image (Pruna API)

| Skill | Description |
|-------|-------------|
| [p-image](https://github.com/PrunaAI/pruna-skills/tree/main/tools/image/p-image/SKILL.md) | Use when the user wants the fastest text-to-image stills, quick draft photos, mood boards, or bulk panels where good … |
| [p-image-edit](https://github.com/PrunaAI/pruna-skills/tree/main/tools/image/p-image-edit/SKILL.md) | Use when the user wants to edit an existing image, change wardrobe or background, compose from reference photos, inpa… |
| [p-image-ideogram](https://github.com/PrunaAI/pruna-skills/tree/main/tools/image/p-image-ideogram/SKILL.md) | Use when the user wants high-fidelity photoreal stills, editorial portraits, hero plates, legible text rendering, or … |
| [p-image-try-on](https://github.com/PrunaAI/pruna-skills/tree/main/tools/image/p-image-try-on/SKILL.md) | Use when the user wants virtual try-on, dress a person in clothing from reference photos, garment fitting on a model … |
| [p-image-upscale](https://github.com/PrunaAI/pruna-skills/tree/main/tools/image/p-image-upscale/SKILL.md) | Use when the user wants to upscale image resolution, enhance detail in an existing still, or prepare photos for print… |

### Tools — video (Pruna API)

| Skill | Description |
|-------|-------------|
| [p-video](https://github.com/PrunaAI/pruna-skills/tree/main/tools/video/p-video/SKILL.md) | Use when the user wants one video clip from text or stills, start/end frame animation, or B-roll and cinematic shots—… |
| [p-video-animate](https://github.com/PrunaAI/pruna-skills/tree/main/tools/video/p-video-animate/SKILL.md) | Use when the user wants to animate a still using motion from another video, motion-transfer remixes, or performance v… |
| [p-video-avatar](https://github.com/PrunaAI/pruna-skills/tree/main/tools/video/p-video-avatar/SKILL.md) | Use when the user wants a talking-head video, lip-synced host or spokesperson clip, on-camera performance from a port… |
| [p-video-replace](https://github.com/PrunaAI/pruna-skills/tree/main/tools/video/p-video-replace/SKILL.md) | Use when the user wants to swap a person, outfit, or product inside existing video, in-footage recast, wardrobe chang… |

### Tools — audio (Replicate)

| Skill | Description |
|-------|-------------|
| [gemini-3.1-flash-tts](https://github.com/PrunaAI/pruna-skills/tree/main/tools/audio/gemini-3.1-flash-tts/SKILL.md) | Use when the user needs narration or voiceover audio for explainers, documentary tracks, scene voice lines, or TTS to… |
| [music-2.5](https://github.com/PrunaAI/pruna-skills/tree/main/tools/audio/music-2.5/SKILL.md) | Use when the user wants AI song generation with vocals, sung lyrics, original tracks from a style prompt, or source a… |
| [stable-audio-2.5](https://github.com/PrunaAI/pruna-skills/tree/main/tools/audio/stable-audio-2.5/SKILL.md) | Use when the user wants light instrumental background music, an ambient bed under dialogue or voiceover, or underscor… |
| [whisperx](https://github.com/PrunaAI/pruna-skills/tree/main/tools/audio/whisperx/SKILL.md) | Use when the user needs word-level lyric timestamps, cut-safe line boundaries for music videos, or alignment after so… |

### Guides — prompting, quality, routing

| Skill | Description |
|-------|-------------|
| [generation-diversity](https://github.com/PrunaAI/pruna-skills/tree/main/guides/prompting/generation-diversity/SKILL.md) | Use when outputs look generic or repetitive — apply the random seed ritual, explicit prompt structure, and scenario a… |
| [generation-quality-checklists](https://github.com/PrunaAI/pruna-skills/tree/main/guides/quality/generation-quality-checklists/SKILL.md) | Use when reviewing generated images, video, or audio — run the core quality checklist and model-specific checklist be… |
| [recipe-catalog](https://github.com/PrunaAI/pruna-skills/tree/main/guides/routing/recipe-catalog/SKILL.md) | Use when choosing a generative pipeline — mood boards, hero variants, explainers, music videos, avatar reels, and oth… |

### Workflows — router

| Skill | Description |
|-------|-------------|
| [pruna-generative-pipeline](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/router/pruna-generative-pipeline/SKILL.md) | Use when the user is unsure which production workflow fits, needs a recipe menu for multi-step media projects, or wan… |
| [pruna-run](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/router/pruna-run/SKILL.md) | Use when the user wants a quick single-shot generation with minimal intake—one image, video clip, or avatar call from… |
| [requesting-generation-feedback](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/router/requesting-generation-feedback/SKILL.md) | Use when the agent is about to call paid generation APIs, deliver a final audio mix, or proceed without user review i… |

### Workflows — core

| Skill | Description |
|-------|-------------|
| [avatar-multi-scene](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/core/avatar-multi-scene/SKILL.md) | Use when the user needs multiple talking-head segments, motion-transfer comparison reels, mixed host and animate clip… |
| [avatar-single-scene](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/core/avatar-single-scene/SKILL.md) | Use when the user needs one talking-head clip, a single host line with lip sync, or one spokesperson beat—not multi-s… |
| [image-to-video](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/core/image-to-video/SKILL.md) | Use when the user needs one video clip from stills, a single narrated story beat, one B-roll shot, or one scene—not a… |
| [narrated-multi-scene](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/core/narrated-multi-scene/SKILL.md) | Use when the user needs a multi-scene narrated film, episodic B-roll story, chaptered promo, or several linked video … |
| [visual-transition-reel](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/core/visual-transition-reel/SKILL.md) | Use when the user needs a visual montage, transitions between stills, action-sequence reel, or multi-scene piece wher… |

### Workflows — verticals

| Skill | Description |
|-------|-------------|
| [illustrated-story-reel](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/verticals/illustrated-story-reel/SKILL.md) | Use when the user wants a still-image story reel or slideshow, picture-book narrative with voiceover or music—and exp… |
| [interactive-explainer](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/verticals/interactive-explainer/SKILL.md) | Use when the user wants educational explainers with a host plus in-story characters, history or science shorts, or wi… |
| [music-video](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/verticals/music-video/SKILL.md) | Use when the user wants a music video, lyric video, sung promo, or original song paired with performance and B-roll c… |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Quick commands:

```bash
make bundle    # rebuild plugins/
make verify    # check plugins/ is current
make validate  # skills-ref on all primaries
```

## License

See [LICENSE](./LICENSE).
