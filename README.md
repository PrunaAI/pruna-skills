# Pruna Skills

![Pruna Skills — images, video, music, explainers, avatars, and workflows for agent coding tools](docs/assets/readme-hero-pruna-skills.png)

Generate images, video, and audio with the [Pruna AI API](https://docs.api.pruna.ai/guides/models), plus multi-step workflows like explainers, music videos, and avatars. Skills follow the [Agent Skills](https://agentskills.io/specification) format and work in Cursor, Claude Code, Copilot, Codex, and [many more agents](https://skills.sh).

## How this works

A **skill** is a short playbook (`SKILL.md`) your coding agent picks up when you ask for something it knows how to do — make an image, edit a photo, build a music video, and so on.

A **plugin** is how you install that playbook. For a single tool it’s basically one skill. For a bigger production it also brings the helpers along (image gen, TTS, video, and the rest) so you’re not hunting missing pieces.

What’s in the box:

- **Tools** — one paid API call: images, edits, upscales, try-on, a short clip, voiceover, a song, lyric timing
- **Guides** — prompting tips, quality checks, recipe ideas — nothing that spends API credits
- **Workflows** — full productions that chain tools together (music video, explainer, avatar reel, narrated story…). Most of them pause for your OK before the expensive steps
- **Routers** — shortcuts when you want a quick one-off (`pruna-run`), help choosing a pipeline (`pruna-generative-pipeline`), or a gate before spend (`requesting-generation-feedback`)

**Rule of thumb:** `npx skills` for one tool or guide. `npx plugins` for a workflow or the whole suite. Don’t install the same tool twice — once alone and again inside a workflow plugin.

### Where you get them

Everything lives on [GitHub](https://github.com/PrunaAI/pruna-skills). We tag releases as `skills-v*`. Day to day you pull with `npx skills` or `npx plugins` — there’s no separate Cursor or Claude app-store submit.

- **[skills.sh](https://skills.sh)** — public catalog for the skills CLI. It shows packages based on real installs, so a few team installs help us show up there.
- **ClawHub / OpenClaw** — optional if you already use OpenClaw (`clawhub install @PrunaAI/…`). CI publishes on each tag.
- **Claude marketplace** — same repo. Add `PrunaAI/pruna-skills` once, then `/plugin install name@pruna-skills`.

## Quickstart

Set your key, then pick a path:

```bash
export PRUNA_API_KEY="your_key"   # see [api-setup.md](api-setup.md)
```

**Try one tool**

```bash
npx skills add PrunaAI/pruna-skills@p-image -y
```

Open a new chat and say: `Generate a product hero image`

**Try a workflow or the full suite**

```bash
npx plugins add PrunaAI/pruna-skills
```

When the list appears, pick `music-video` or `pruna-full`.

**Install everything**

```bash
npx plugins add PrunaAI/pruna-skills -y
```

**Browse what’s available**

```bash
npx skills add PrunaAI/pruna-skills -l
npx plugins discover PrunaAI/pruna-skills
```

One gotcha: the plugins CLI doesn’t take `@name` the way skills does. This fails with “No plugins found”:

```bash
npx plugins add PrunaAI/pruna-skills@pruna-full
```

Use the picker above instead, or in Claude Code:

```text
/plugin marketplace add PrunaAI/pruna-skills
/plugin install pruna-full@pruna-skills
```

`pruna-full` gives you all 26 skills. On multi-scene work it asks you to approve the plan, then stills, then clips before paid video — you stay in control of spend.

Not sure what to install? See [Choosing what to install](#choosing-what-to-install). And skim [agent safety](references/shared/agent-safety.md) before enabling skills in untrusted repos.

## Contents

- [How this works](#how-this-works)
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

Start with Quickstart if you’re new. Come back here when you know roughly what you need. The full catalog lives in [README.skills.md](README.skills.md).

| Tier | What it is | Install with |
|------|------------|--------------|
| **Tools** | One paid API call — image, video, or audio | `npx skills` |
| **Guides** | Prompting, quality, routing — no API | `npx skills` |
| **Workflows** | Multi-step productions with tool deps | Prefer `npx plugins` |

### Tools

| You want… | Skill | Install |
|-----------|-------|---------|
| Fast text-to-image | `p-image` | `npx skills add PrunaAI/pruna-skills@p-image -y` |
| Edit / compose from refs | `p-image-edit` | `npx skills add PrunaAI/pruna-skills@p-image-edit -y` |
| Virtual try-on | `p-image-try-on` | `npx skills add PrunaAI/pruna-skills@p-image-try-on -y` |
| Upscale | `p-image-upscale` | `npx skills add PrunaAI/pruna-skills@p-image-upscale -y` |
| One video clip | `p-video` | `npx skills add PrunaAI/pruna-skills@p-video -y` |
| Motion-transfer | `p-video-animate` | `npx skills add PrunaAI/pruna-skills@p-video-animate -y` |
| Person on camera speaking | `p-video-avatar` | `npx skills add PrunaAI/pruna-skills@p-video-avatar -y` |
| Swap person or product in video | `p-video-replace` | `npx skills add PrunaAI/pruna-skills@p-video-replace -y` |
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

#### Routers

| You want… | Skill | Install |
|-----------|-------|---------|
| Quick single shot | `pruna-run` | `npx skills add PrunaAI/pruna-skills@pruna-run -y` |
| Help choosing a workflow | `pruna-generative-pipeline` | `npx skills add PrunaAI/pruna-skills@pruna-generative-pipeline -y` |
| Sign-off before paid calls | `requesting-generation-feedback` | `npx skills add PrunaAI/pruna-skills@requesting-generation-feedback -y` |

#### Core

These are multi-step. Plugins are the nicer install because the tools come with them. Skills install is fine if you already have the pieces.

| You want… | Skill | Install |
|-----------|-------|---------|
| One narrated scene or B-roll from images | `image-to-video` | `npx skills add PrunaAI/pruna-skills@image-to-video -y` |
| Multi-part story with voiceover | `narrated-multi-scene` | `npx skills add PrunaAI/pruna-skills@narrated-multi-scene -y` |
| Montage with transitions | `visual-transition-reel` | `npx skills add PrunaAI/pruna-skills@visual-transition-reel -y` |
| One host-on-camera beat | `avatar-single-scene` | `npx skills add PrunaAI/pruna-skills@avatar-single-scene -y` |
| Same person hosting several clips | `avatar-multi-scene` | `npx skills add PrunaAI/pruna-skills@avatar-multi-scene -y` |

#### Verticals

| You want… | Skill | Install |
|-----------|-------|---------|
| Explainer with host and characters | `interactive-explainer` | `npx skills add PrunaAI/pruna-skills@interactive-explainer -y` |
| Full music video | `music-video` | `npx skills add PrunaAI/pruna-skills@music-video -y` |
| Slideshow story with narration | `illustrated-story-reel` | `npx skills add PrunaAI/pruna-skills@illustrated-story-reel -y` |

#### Full suite

| You want… | Plugin | Install |
|-----------|--------|---------|
| Everything | `pruna-full` | `npx plugins add PrunaAI/pruna-skills` then pick `pruna-full` |

To install a workflow with its dependencies in one go:

```bash
npx plugins add PrunaAI/pruna-skills
# pick music-video, avatar-multi-scene, pruna-full, …
```

Or grab every plugin:

```bash
npx plugins add PrunaAI/pruna-skills -y
```

<!-- BEGIN README.skills.md -->
<!-- generated by scripts/write_readme_skills_section.py; do not edit -->

## Available Skills

### Tools — image (Pruna API)

| Skill | Description |
|-------|-------------|
| [p-image](https://github.com/PrunaAI/pruna-skills/tree/main/tools/image/p-image/SKILL.md) | Use when someone wants a fast AI image — product shots, hero visuals, mood boards, or draft photos from a text prompt. |
| [p-image-edit](https://github.com/PrunaAI/pruna-skills/tree/main/tools/image/p-image-edit/SKILL.md) | Use when someone wants to edit an existing photo — change outfits or backgrounds, compose from reference images, or a… |
| [p-image-try-on](https://github.com/PrunaAI/pruna-skills/tree/main/tools/image/p-image-try-on/SKILL.md) | Use when someone wants virtual try-on — dress a person in clothes from reference photos for fashion or ecommerce. |
| [p-image-upscale](https://github.com/PrunaAI/pruna-skills/tree/main/tools/image/p-image-upscale/SKILL.md) | Use when someone wants to upscale or sharpen an existing image for print, large crops, or higher-quality delivery. |

### Tools — video (Pruna API)

| Skill | Description |
|-------|-------------|
| [p-video](https://github.com/PrunaAI/pruna-skills/tree/main/tools/video/p-video/SKILL.md) | Use when someone wants one short video clip from text or images — B-roll, start/end frame animation, or a quick motio… |
| [p-video-animate](https://github.com/PrunaAI/pruna-skills/tree/main/tools/video/p-video-animate/SKILL.md) | Use when someone wants a photo to move like another video — motion transfer, dance remixes, or performance variations… |
| [p-video-avatar](https://github.com/PrunaAI/pruna-skills/tree/main/tools/video/p-video-avatar/SKILL.md) | Use when someone wants a person on camera speaking a script — lip-synced host, spokesperson, or narrated avatar from … |
| [p-video-replace](https://github.com/PrunaAI/pruna-skills/tree/main/tools/video/p-video-replace/SKILL.md) | Use when someone wants to swap a person, outfit, or product inside existing footage while keeping the camera move and… |

### Tools — audio (Replicate)

| Skill | Description |
|-------|-------------|
| [gemini-3.1-flash-tts](https://github.com/PrunaAI/pruna-skills/tree/main/tools/audio/gemini-3.1-flash-tts/SKILL.md) | Use when someone needs spoken narration or voiceover — explainer tracks, documentary lines, or voice to pair with gen… |
| [music-2.5](https://github.com/PrunaAI/pruna-skills/tree/main/tools/audio/music-2.5/SKILL.md) | Use when someone wants an original AI song with vocals — sung lyrics, a style prompt track, or source audio for a mus… |
| [stable-audio-2.5](https://github.com/PrunaAI/pruna-skills/tree/main/tools/audio/stable-audio-2.5/SKILL.md) | Use when someone wants light instrumental background music — an ambient bed under dialogue or underscore for reels an… |
| [whisperx](https://github.com/PrunaAI/pruna-skills/tree/main/tools/audio/whisperx/SKILL.md) | Use when someone needs word-level lyric timestamps or cut-safe line boundaries before editing music-video clips. |

### Guides — prompting, quality, routing

| Skill | Description |
|-------|-------------|
| [generation-diversity](https://github.com/PrunaAI/pruna-skills/tree/main/guides/prompting/generation-diversity/SKILL.md) | Use when generations look generic or samey — vary seeds, prompt structure, and scenario axes before the next paid ima… |
| [generation-quality-checklists](https://github.com/PrunaAI/pruna-skills/tree/main/guides/quality/generation-quality-checklists/SKILL.md) | Use when reviewing generated images, videos, or audio before shipping — run the quality checklists before asking for … |
| [recipe-catalog](https://github.com/PrunaAI/pruna-skills/tree/main/guides/routing/recipe-catalog/SKILL.md) | Use when browsing recipe ideas for mood boards, hero images, explainers, music videos, or avatar reels and need the l… |

### Workflows — router

| Skill | Description |
|-------|-------------|
| [pruna-generative-pipeline](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/router/pruna-generative-pipeline/SKILL.md) | Use when someone is unsure which production fits — need a menu for chained images, video, and audio with staged appro… |
| [pruna-run](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/router/pruna-run/SKILL.md) | Use when someone wants a quick one-off generation — one image, video clip, edit, or speaking avatar from a prompt, wi… |
| [requesting-generation-feedback](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/router/requesting-generation-feedback/SKILL.md) | Use when about to spend on generation — pause for review of prompts, images, or clips before the next paid step. Not … |

### Workflows — core

| Skill | Description |
|-------|-------------|
| [avatar-multi-scene](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/core/avatar-multi-scene/SKILL.md) | Use when someone wants the same person hosting several clips — multi-segment UGC, comparison reels, or mixed speaking… |
| [avatar-single-scene](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/core/avatar-single-scene/SKILL.md) | Use when someone wants one polished host-on-camera beat — a speaking person with intake and approval gates before gen… |
| [image-to-video](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/core/image-to-video/SKILL.md) | Use when someone wants one short film beat from images — a narrated scene, story moment, or cinematic B-roll with opt… |
| [narrated-multi-scene](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/core/narrated-multi-scene/SKILL.md) | Use when someone wants a multi-part story with voiceover — episodic B-roll, chaptered promo, or several linked video … |
| [visual-transition-reel](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/core/visual-transition-reel/SKILL.md) | Use when someone wants a montage with transitions between shots — action-sequence reel or multi-scene piece where nar… |

### Workflows — verticals

| Skill | Description |
|-------|-------------|
| [illustrated-story-reel](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/verticals/illustrated-story-reel/SKILL.md) | Use when someone wants a slideshow story with narration or music — picture-book style illustrated frames, not full mo… |
| [interactive-explainer](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/verticals/interactive-explainer/SKILL.md) | Use when someone wants an educational explainer with a host and characters — history or science shorts with dialogue,… |
| [music-video](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/verticals/music-video/SKILL.md) | Use when someone wants a full music video — original song or vocals, performance clips, B-roll, and lyric-synced edits. |
<!-- END README.skills.md -->

---

## Install skills (`npx skills`)

The [skills CLI](https://github.com/vercel-labs/skills) drops `SKILL.md` folders into your agent (Cursor, Codex, Claude Code, Copilot, and [more](https://skills.sh)).

```bash
npx skills add PrunaAI/pruna-skills -l
npx skills add PrunaAI/pruna-skills@p-image -y
npx skills add PrunaAI/pruna-skills@music-video -y
```

After install, start a **new chat**. Listing on [skills.sh](https://skills.sh) follows install telemetry — no separate submit step.

---

## Install plugins (`npx plugins`)

The [plugins CLI](https://github.com/vercel-labs/plugins) installs full bundles — manifest, skills, and workflow deps — into Claude Code, Cursor, Copilot CLI, VS Code, Codex, and others.

```bash
npx plugins discover PrunaAI/pruna-skills

# pick one from the list, e.g. music-video or pruna-full
npx plugins add PrunaAI/pruna-skills

# install all 27 plugins
npx plugins add PrunaAI/pruna-skills -y

npx plugins add PrunaAI/pruna-skills --target cursor
```

Unlike skills, plugins doesn’t understand `@name`. This fails:

```bash
npx plugins add PrunaAI/pruna-skills@pruna-full
```

In Claude Code you can name the plugin directly:

```text
/plugin marketplace add PrunaAI/pruna-skills
/plugin install pruna-full@pruna-skills
```

Each folder under `plugins/<name>/` is one plugin. Workflow plugins embed their tools — for example `music-video` includes `p-image`, `p-video`, TTS, and friends.

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
