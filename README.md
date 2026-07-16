# Pruna Skills

![Pruna Skills — images, video, music, explainers, avatars, and workflows for agent coding tools](docs/assets/readme-hero-pruna-skills.png)

Generate images, video, and audio with the [Pruna AI API](https://docs.api.pruna.ai/guides/models), plus multi-step workflows (explainers, music videos, avatars). Skills follow the [Agent Skills](https://agentskills.io/specification) format and work across Cursor, Claude Code, Copilot, Codex, and [many more agents](https://skills.sh).

**Default install:** `npx skills` for one capability, `npx plugins` for a workflow (deps included). Browse the catalog on [skills.sh](https://skills.sh) after installs land there (listing is telemetry-driven).

## Quickstart

```bash
export PRUNA_API_KEY="your_key"   # see [api-setup.md](api-setup.md)
npx skills add PrunaAI/pruna-skills@p-image -y
```

Then open a **new chat** and try: "Generate a product hero still with p-image."

| Goal | Command |
|------|---------|
| One tool or guide | `npx skills add PrunaAI/pruna-skills@<name> -y` |
| One workflow (deps bundled) | `npx plugins add PrunaAI/pruna-skills -y` → pick the workflow |
| List everything | `npx skills add PrunaAI/pruna-skills -l` |
| Full suite (`pruna-full`) | `npx plugins add PrunaAI/pruna-skills -y` → pick `pruna-full` |

**pruna-full** installs all 26 skills. Multi-scene workflows use **staged approval** (plan → stills → clips before paid video) via `requesting-generation-feedback`, and **parallel subagents per scene lane** after you confirm — the parent agent merges results.

**Skill vs plugin:** use **skills** for a single tool/guide; use **plugins** for workflows so embedded tools (`p-image`, TTS, …) come with it. Don't install the same tools twice (standalone + inside a workflow plugin).

Not sure which skill? See [Choosing what to install](#choosing-what-to-install). Review skills before enabling them in untrusted repos — [agent safety](references/shared/agent-safety.md).

## Contents

- [Quickstart](#quickstart)
- [Choosing what to install](#choosing-what-to-install)
- [Install skills (`npx skills`)](#install-skills-npx-skills)
- [Install plugins (`npx plugins`)](#install-plugins-npx-plugins)
- [Other ways to install](#other-ways-to-install)
- [API setup](#api-setup)
- [How this repo works](#how-this-repo-works)
- [Contributing](#contributing)

---

## Choosing what to install

Three tiers:

| Tier | What it is | Install with |
|------|------------|--------------|
| **Tools** | One paid API call (image, video, audio) | `npx skills` |
| **Guides** | Prompting / quality / routing — no API | `npx skills` |
| **Workflows** | Multi-step pipelines with tool deps | Prefer `npx plugins` |

### Tools

| You want… | Skill | Install |
|-----------|-------|---------|
| Fast text-to-image | `p-image` | `npx skills add PrunaAI/pruna-skills@p-image -y` |
| Edit / compose from refs | `p-image-edit` | `npx skills add PrunaAI/pruna-skills@p-image-edit -y` |
| Virtual try-on | `p-image-try-on` | `npx skills add PrunaAI/pruna-skills@p-image-try-on -y` |
| Upscale | `p-image-upscale` | `npx skills add PrunaAI/pruna-skills@p-image-upscale -y` |
| One video clip | `p-video` | `npx skills add PrunaAI/pruna-skills@p-video -y` |
| Motion-transfer | `p-video-animate` | `npx skills add PrunaAI/pruna-skills@p-video-animate -y` |
| Talking-head | `p-video-avatar` | `npx skills add PrunaAI/pruna-skills@p-video-avatar -y` |
| Swap person/product in video | `p-video-replace` | `npx skills add PrunaAI/pruna-skills@p-video-replace -y` |
| Narration / voiceover | `gemini-3.1-flash-tts` | `npx skills add PrunaAI/pruna-skills@gemini-3.1-flash-tts -y` |
| Song with vocals | `music-2.5` | `npx skills add PrunaAI/pruna-skills@music-2.5 -y` |
| Background music bed | `stable-audio-2.5` | `npx skills add PrunaAI/pruna-skills@stable-audio-2.5 -y` |
| Lyric timestamps | `whisperx` | `npx skills add PrunaAI/pruna-skills@whisperx -y` |

### Guides

| You want… | Skill | Install |
|-----------|-------|---------|
| Less generic outputs | `generation-diversity` | `npx skills add PrunaAI/pruna-skills@generation-diversity -y` |
| QA before shipping | `generation-quality-checklists` | `npx skills add PrunaAI/pruna-skills@generation-quality-checklists -y` |
| Pick a pipeline | `recipe-catalog` | `npx skills add PrunaAI/pruna-skills@recipe-catalog -y` |

### Workflows

Routers (skills-only is enough):

| You want… | Skill |
|-----------|-------|
| Quick single shot | `npx skills add PrunaAI/pruna-skills@pruna-run -y` |
| Unsure which workflow | `npx skills add PrunaAI/pruna-skills@pruna-generative-pipeline -y` |
| Sign-off before paid calls | `npx skills add PrunaAI/pruna-skills@requesting-generation-feedback -y` |

Core and verticals — install with **plugins** so dependencies are included:

```bash
npx plugins add PrunaAI/pruna-skills -y
# pick: image-to-video | avatar-single-scene | avatar-multi-scene |
#       narrated-multi-scene | visual-transition-reel |
#       illustrated-story-reel | interactive-explainer | music-video | pruna-full
```

Or as skills only (no embedded deps): `npx skills add PrunaAI/pruna-skills@music-video -y`

<!-- BEGIN README.skills.md -->
<!-- generated by scripts/write_readme_skills_section.py; do not edit -->

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
| [p-video](https://github.com/PrunaAI/pruna-skills/tree/main/tools/video/p-video/SKILL.md) | Use when the user wants one video clip from text or stills, start/end frame animation, or B-roll—not multi-scene film… |
| [p-video-animate](https://github.com/PrunaAI/pruna-skills/tree/main/tools/video/p-video-animate/SKILL.md) | Use when the user wants to animate a still using motion from another video, motion-transfer remixes, or performance v… |
| [p-video-avatar](https://github.com/PrunaAI/pruna-skills/tree/main/tools/video/p-video-avatar/SKILL.md) | Use when the user wants one talking-head API call from a portrait plus script. Prefer avatar-single-scene for a full … |
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
| [recipe-catalog](https://github.com/PrunaAI/pruna-skills/tree/main/guides/routing/recipe-catalog/SKILL.md) | Use when choosing among recipe letters A–R (mood boards, hero variants, explainers, music videos, avatar reels) and n… |

### Workflows — router

| Skill | Description |
|-------|-------------|
| [pruna-generative-pipeline](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/router/pruna-generative-pipeline/SKILL.md) | Use when the user is unsure which production workflow fits, needs a recipe menu for multi-step media, or wants chaine… |
| [pruna-run](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/router/pruna-run/SKILL.md) | Use when the user wants a quick single-shot generation with minimal intake—one image, video clip, or avatar call from… |
| [requesting-generation-feedback](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/router/requesting-generation-feedback/SKILL.md) | Use when about to call paid generation APIs, skip user review of prompts/stills/clips, or mux final audio without cli… |

### Workflows — core

| Skill | Description |
|-------|-------------|
| [avatar-multi-scene](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/core/avatar-multi-scene/SKILL.md) | Use when the user needs multiple talking-head segments, motion-transfer comparison reels, mixed host and animate clip… |
| [avatar-single-scene](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/core/avatar-single-scene/SKILL.md) | Use when the user needs one talking-head beat with intake and approval gates—not a raw p-video-avatar call, multi-seg… |
| [image-to-video](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/core/image-to-video/SKILL.md) | Use when the user needs one narrated or B-roll scene from stills with optional TTS—not a bare p-video API call, multi… |
| [narrated-multi-scene](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/core/narrated-multi-scene/SKILL.md) | Use when the user needs a multi-scene narrated film, episodic B-roll story, chaptered promo, or several linked video … |
| [visual-transition-reel](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/core/visual-transition-reel/SKILL.md) | Use when the user needs a visual montage, transitions between stills, action-sequence reel, or multi-scene piece wher… |

### Workflows — verticals

| Skill | Description |
|-------|-------------|
| [illustrated-story-reel](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/verticals/illustrated-story-reel/SKILL.md) | Use when the user wants a still-image story reel or slideshow, picture-book narrative with voiceover or music—and exp… |
| [interactive-explainer](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/verticals/interactive-explainer/SKILL.md) | Use when the user wants educational explainers with a host plus in-story characters, history or science shorts, or wi… |
| [music-video](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/verticals/music-video/SKILL.md) | Use when the user wants a music video, lyric video, sung promo, or original song paired with performance and B-roll c… |
<!-- END README.skills.md -->

---

## Install skills (`npx skills`)

The [skills CLI](https://github.com/vercel-labs/skills) installs `SKILL.md` folders into your agent (Cursor, Codex, Claude Code, Copilot, and [more](https://skills.sh)).

```bash
npx skills add PrunaAI/pruna-skills -l              # list
npx skills add PrunaAI/pruna-skills@p-image -y      # one tool
npx skills add PrunaAI/pruna-skills@music-video -y  # one workflow (skills only)
```

After install, start a **new chat**. Discoverability on [skills.sh](https://skills.sh) follows install telemetry — no separate submit step.

---

## Install plugins (`npx plugins`)

The [plugins CLI](https://github.com/vercel-labs/plugins) installs full bundles (manifest + skills + workflow deps) into Claude Code, Cursor, Copilot CLI, VS Code, Codex, and others.

```bash
npx plugins discover PrunaAI/pruna-skills
npx plugins add PrunaAI/pruna-skills -y              # interactive picker
npx plugins add PrunaAI/pruna-skills -y --target cursor
```

Each folder under `plugins/<name>/` is one plugin.

---

## Other ways to install

Same packages, different installers. Prefer `npx skills` / `npx plugins` above unless you already use these channels.

**Claude Code / Copilot CLI** — marketplace:

```bash
/plugin marketplace add PrunaAI/pruna-skills
/plugin install p-image@pruna-skills
/plugin install music-video@pruna-skills
```

Copilot CLI: `copilot plugin install music-video@pruna-skills`

**OpenClaw / ClawHub** — versioned registry (CI publishes on each `skills-v*` tag). Docs use `@PrunaAI/…`; package.json scope is `@pruna-ai/…` (same org, different casing):

```bash
clawhub install @PrunaAI/p-image
openclaw plugins install clawhub:@PrunaAI/music-video
```

Dots in skill names become hyphens on ClawHub (`music-2.5` → `@PrunaAI/music-2-5`).

**APM** — team lockfiles:

```bash
apm install PrunaAI/pruna-skills/plugins/p-image/skills/p-image
```

**ChatGPT** (Enterprise / Edu) — no `npx` path. Upload or share the skill's `SKILL.md` (and refs) via the ChatGPT skills / plugins admin UI.

More detail: [skill-package-managers.md](references/shared/skill-package-managers.md). Releases: [PUBLISHING.md](PUBLISHING.md).

---

## API setup

See [api-setup.md](api-setup.md) for `PRUNA_API_KEY`, `REPLICATE_API_TOKEN`, and HTTP details.

---

## How this repo works

Edit source in `tools/`, `guides/`, and `workflows/`. Bundling copies that into `plugins/<name>/` for plugin installs — don't edit `plugins/` by hand; pre-commit rebuilds it.

```text
tools/  guides/  workflows/     ──bundle──►  plugins/<name>/
     (author here)                            (install as plugin)
```

| | Source | Generated plugins |
|--|--------|-------------------|
| Paths | `tools/`, `guides/`, `workflows/` | `plugins/<name>/` |
| Edit? | Yes | No |
| Contents | Primary `SKILL.md` + refs/scripts | Manifest + `skills/<name>/` (+ embedded deps for workflows) |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

```bash
make bundle     # rebuild plugins/
make verify     # check plugins/ is current
make validate   # skills-ref + clawhub + install smoke
```

## License

See [LICENSE](./LICENSE).
