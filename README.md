# Pruna Skills

![Pruna Skills — images, video, music, explainers, avatars, and workflows for agent coding tools](docs/assets/readme-hero-pruna-skills.png)

Agent skills for generating images, video, and audio with the [Pruna AI API](https://docs.api.pruna.ai/guides/models), plus multi-step workflows for explainers, music videos, and similar projects. Source: [PrunaAI/pruna-skills](https://github.com/PrunaAI/pruna-skills).

Skills follow the [Agent Skills](https://agentskills.io/specification) format. Install a single **skill** (one capability) or a **plugin** bundle (manifest + skills + workflow dependencies). The [quickstart](#quickstart) gets you running in one command.

## Quickstart

You'll need a Pruna API key — see [api-setup.md](api-setup.md):

```bash
export PRUNA_API_KEY="your_key"
```

### One image skill (`p-image`)

```bash
npx skills add PrunaAI/pruna-skills@p-image -y
```

Restart the agent or open a new chat, then try: "Generate a product hero still with p-image."

### One image plugin (`p-image`)

For native plugin support in Claude Code, Cursor, Copilot CLI, or VS Code:

```bash
npx plugins add PrunaAI/pruna-skills -y
# pick p-image from the list
```

### Everything at once

All skills:

```bash
npx skills add PrunaAI/pruna-skills/plugins/pruna-full/skills -y
```

Full suite as a plugin:

```bash
npx plugins add PrunaAI/pruna-skills -y
# pick pruna-full from the list
```

Not sure what you need? See [Choosing what to install](#choosing-what-to-install).

## Contents

- [Quickstart](#quickstart)
- [Choosing what to install](#choosing-what-to-install)
- [Install skills (`npx skills`)](#install-skills-npx-skills)
- [Install plugins (`npx plugins`)](#install-plugins-npx-plugins)
- [Other ways to install](#other-ways-to-install)
- [API Setup](#api-setup)
- [How this repo works](#how-this-repo-works)
- [Contributing](#contributing)

---

## Choosing what to install

There are three tiers — **tools**, **guides**, and **workflows**. Pick a skill by name with `npx skills`, or a plugin bundle with `npx plugins` when you want native agent integration or a workflow with its tool dependencies included.

### By use case

**Tools** — one paid API call (image, video, or audio). Install any tool as a skill:

| You want to… | Skill | Command |
|--------------|-------|---------|
| Fast text-to-image stills | `p-image` | `npx skills add PrunaAI/pruna-skills@p-image -y` |
| Edit wardrobe, background, or compose refs | `p-image-edit` | `npx skills add PrunaAI/pruna-skills@p-image-edit -y` |
| Virtual try-on | `p-image-try-on` | `npx skills add PrunaAI/pruna-skills@p-image-try-on -y` |
| Upscale for print or detail | `p-image-upscale` | `npx skills add PrunaAI/pruna-skills@p-image-upscale -y` |
| One video clip from text or stills | `p-video` | `npx skills add PrunaAI/pruna-skills@p-video -y` |
| Motion-transfer / animate a still | `p-video-animate` | `npx skills add PrunaAI/pruna-skills@p-video-animate -y` |
| Talking-head from a portrait | `p-video-avatar` | `npx skills add PrunaAI/pruna-skills@p-video-avatar -y` |
| Swap person or product in video | `p-video-replace` | `npx skills add PrunaAI/pruna-skills@p-video-replace -y` |
| Narration or voiceover | `gemini-3.1-flash-tts` | `npx skills add PrunaAI/pruna-skills@gemini-3.1-flash-tts -y` |
| Full song with vocals | `music-2.5` | `npx skills add PrunaAI/pruna-skills@music-2.5 -y` |
| Background music bed | `stable-audio-2.5` | `npx skills add PrunaAI/pruna-skills@stable-audio-2.5 -y` |
| Word-level lyric timestamps | `whisperx` | `npx skills add PrunaAI/pruna-skills@whisperx -y` |

**Guides** — prompting, quality, and routing. No API calls; pair with any tool:

| You want to… | Skill | Command |
|--------------|-------|---------|
| Fix generic or repetitive outputs | `generation-diversity` | `npx skills add PrunaAI/pruna-skills@generation-diversity -y` |
| Review stills/clips before shipping | `generation-quality-checklists` | `npx skills add PrunaAI/pruna-skills@generation-quality-checklists -y` |
| Pick the right multi-step pipeline | `recipe-catalog` | `npx skills add PrunaAI/pruna-skills@recipe-catalog -y` |

**Workflows** — multi-step production (tools + guides orchestrated). Prefer a **plugin** so dependencies are bundled; skills-only install works too.

Plugin install for any workflow: `npx plugins add PrunaAI/pruna-skills -y` → pick the name in the **Plugin** column.

| You want to… | Tier | Skill | Plugin |
|--------------|------|-------|--------|
| Quick single shot, minimal intake | Router | `npx skills add PrunaAI/pruna-skills@pruna-run -y` | — |
| Unsure which workflow fits | Router | `npx skills add PrunaAI/pruna-skills@pruna-generative-pipeline -y` | — |
| User sign-off before paid calls | Router | `npx skills add PrunaAI/pruna-skills@requesting-generation-feedback -y` | — |
| One narrated clip from stills | Core | `npx skills add PrunaAI/pruna-skills@image-to-video -y` | `image-to-video` |
| One talking-head beat | Core | `npx skills add PrunaAI/pruna-skills@avatar-single-scene -y` | `avatar-single-scene` |
| Multi-segment host or motion reel | Core | `npx skills add PrunaAI/pruna-skills@avatar-multi-scene -y` | `avatar-multi-scene` |
| Multi-scene narrated film | Core | `npx skills add PrunaAI/pruna-skills@narrated-multi-scene -y` | `narrated-multi-scene` |
| Visual montage / transition reel | Core | `npx skills add PrunaAI/pruna-skills@visual-transition-reel -y` | `visual-transition-reel` |
| Still-image story slideshow | Vertical | `npx skills add PrunaAI/pruna-skills@illustrated-story-reel -y` | `illustrated-story-reel` |
| Educational explainer with host | Vertical | `npx skills add PrunaAI/pruna-skills@interactive-explainer -y` | `interactive-explainer` |
| Full music video | Vertical | `npx skills add PrunaAI/pruna-skills@music-video -y` | `music-video` |
| Everything (27 skills) | Suite | `npx skills add PrunaAI/pruna-skills/plugins/pruna-full/skills -y` | `pruna-full` |

### Skill vs plugin

| | **Skill** (`npx skills`) | **Plugin** (`npx plugins`) |
|--|--------------------------|----------------------------|
| What you get | One `SKILL.md` folder | Plugin manifest + skills (+ embedded tool copies for workflows) |
| Best for | A single **tool** or **guide** | **Workflows**, native agent hooks, installing deps in one step |
| Install | `npx skills add PrunaAI/pruna-skills@p-image -y` | `npx plugins add PrunaAI/pruna-skills -y` → pick from list |
| Examples | `p-image`, `generation-diversity`, `p-video-avatar` | `music-video`, `avatar-multi-scene`, `pruna-full` |

Use **`npx skills`** when you want one capability. Use **`npx plugins`** for workflows (so `p-image`, TTS, etc. come bundled) or when your agent expects a native plugin install.

Don't install a workflow plugin **and** the same tools as standalone skills — you'll get duplicate names.

<!-- README.skills.md inserted below -->
## Available Skills

### Tools — image (Pruna API)

| Skill | Description |
|-------|-------------|
| [p-image](https://github.com/PrunaAI/pruna-skills/tree/main/tools/image/p-image/SKILL.md) | Use when the user wants the fastest text-to-image stills, quick draft photos, mood boards, or bulk panels where good … |
| [p-image-edit](https://github.com/PrunaAI/pruna-skills/tree/main/tools/image/p-image-edit/SKILL.md) | Use when the user wants to edit an existing image, change wardrobe or background, compose from reference photos, inpa… |
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

---

## Install skills (`npx skills`)

The [skills CLI](https://github.com/vercel-labs/skills) copies `SKILL.md` folders into your agent. Works with Cursor, Codex, Claude Code, and [68+ agents](https://skills.sh).

```bash
# List everything in the repo
npx skills add PrunaAI/pruna-skills -l

# One tool or guide from the source tree
npx skills add PrunaAI/pruna-skills@p-image -y
npx skills add PrunaAI/pruna-skills@generation-diversity -y

# One workflow (skills only — no plugin manifest)
npx skills add PrunaAI/pruna-skills/plugins/music-video/skills --skill music-video -y

# Full suite
npx skills add PrunaAI/pruna-skills/plugins/pruna-full/skills -y
```

Restart your agent or start a new chat after install.

**Also available:** Claude `/plugin install`, [ClawHub](https://docs.openclaw.ai/clawhub), and [APM](https://microsoft.github.io/apm/) — see [Other ways to install](#other-ways-to-install).

---

## Install plugins (`npx plugins`)

The [plugins CLI](https://github.com/vercel-labs/plugins) installs full plugin bundles into Claude Code, Cursor, Copilot CLI, VS Code, Codex, and others.

```bash
# Install from GitHub (interactive picker)
npx plugins add PrunaAI/pruna-skills -y
npx plugins add https://github.com/PrunaAI/pruna-skills -y

# Preview without installing
npx plugins discover PrunaAI/pruna-skills

# Target one agent
npx plugins add PrunaAI/pruna-skills -y --target cursor
```

Each bundle under `plugins/<name>/` is one plugin — standalone tools (`p-image`), workflows with embedded deps (`music-video`), or the full suite (`pruna-full`).

**Also available:** Claude `/plugin marketplace`, [ClawHub](https://docs.openclaw.ai/clawhub) — see [Other ways to install](#other-ways-to-install).

---

## Other ways to install

Same skills and plugins, different installers:

**Claude Code / Copilot CLI** — native marketplace:

```bash
/plugin marketplace add PrunaAI/pruna-skills
/plugin install p-image@pruna-skills
/plugin install music-video@pruna-skills
/plugin install pruna-full@pruna-skills
```

Copilot CLI: `copilot plugin install pruna-full@pruna-skills`

**OpenClaw / ClawHub** — versioned registry (published on each release tag):

```bash
clawhub install @PrunaAI/p-image
openclaw plugins install clawhub:@PrunaAI/music-video
openclaw plugins install clawhub:@PrunaAI/pruna-full
```

ClawHub slugs hyphenate dots (`music-2.5` → `@PrunaAI/music-2-5`).

**APM** — team lockfiles:

```bash
apm install PrunaAI/pruna-skills/plugins/p-image/skills/p-image
apm install PrunaAI/pruna-skills/plugins/music-video/skills/music-video
```

More detail on how these relate: [skill-package-managers.md](references/shared/skill-package-managers.md). Publishing: [PUBLISHING.md](PUBLISHING.md).

---

## API Setup

See [api-setup.md](api-setup.md) for `PRUNA_API_KEY`, `REPLICATE_API_TOKEN`, and HTTP details.

---

## How this repo works

You edit source in `tools/`, `guides/`, and `workflows/`. `./scripts/bundle_all_skills.sh` copies that into `plugins/<name>/` for plugin-based installs — don't edit `plugins/` directly; pre-commit rebuilds it.

| | Source tree | Generated plugins |
|--|-------------|-------------------|
| Paths | `tools/`, `guides/`, `workflows/` | `plugins/<name>/` |
| Edit? | Yes | No |
| Contents | Primary `SKILL.md` + refs/scripts | `.claude-plugin/plugin.json` + `skills/<name>/` (+ embedded deps for workflows) |

There are three content tiers — **tools** (`p-image`, `p-video`, …) call paid APIs; **guides** (`generation-diversity`, `recipe-catalog`) don't; **workflows** (`music-video`, `pruna-run`) orchestrate tools and do.

```text
tools/  guides/  workflows/     ──bundle──►  plugins/<name>/
     (author here)                            (install as plugin)
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Quick commands:

```bash
make bundle    # rebuild plugins/
make verify    # check plugins/ is current
make validate  # skills-ref on all primaries
```

## License

See [LICENSE](./LICENSE).
