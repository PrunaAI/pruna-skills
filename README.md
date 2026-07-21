# Pruna Skills

![Pruna Skills: images, video, music, explainers, avatars, and workflows for agent coding tools](docs/assets/readme-hero-pruna-skills.png)

Pruna Skills teach your coding agent how to generate images, video, and audio with the [Pruna AI API](https://docs.api.pruna.ai/guides/models). They also cover multi-step workflows such as explainers, music videos, avatars, and illustrated reels. Each skill follows the [Agent Skills](https://agentskills.io/specification) format, so it works in Cursor, Claude Code, Copilot, Codex, and [many other agents](https://skills.sh).

## Quickstart

First, set your API key and install the full suite. One command gives you every guide, tool, and workflow.

```bash
export PRUNA_API_KEY="your_key"   # see [api-setup.md](docs/api-setup.md)

npx skills add PrunaAI/pruna-skills@pruna -y
```

Next, start a **new chat** and describe what you want in plain language. Your agent reads the suite and picks the right skills for the job.

Before you enable skills in an untrusted repo, skim [agent safety](skills/guides/pruna-api/references/agent-safety.md).

### Try it: ask your agent

**Portrait, then try-on, then performance**

> Create a portrait of a teenage girl drummer in a garage. Put a vintage red band jacket on her from a garment reference, and keep the pose and background. Then make her sing along to a song slice as a lip-sync performance clip.

| Step 1 · `p-image` | Step 2 · `p-image-try-on` | Step 3 · `p-video-avatar` |
| :-: | :-: | :-: |
| Drummer portrait | Jacket try-on | Performance clip |
| <img src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/readme-music-video-garage-drummer.png" width="280" height="494" alt="Teenage drummer portrait in a garage"> | <img src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/readme-p-image-try-on-drummer.png" width="280" height="494" alt="Same drummer wearing the red band jacket"> | <img src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/readme-music-video-garage-drummer-clip.gif" width="280" height="494" alt="Drummer lip-sync performance clip wearing the red band jacket"> |

**Still, then edit, then clip**

> Generate a monarch butterfly on lavender with wings closed. Edit so the wings open wide, keeping the same stem and camera. Then animate a short clip of the wing-spread.

| Step 1 · `p-image` | Step 2 · `p-image-edit` | Step 3 · `p-video` |
| :-: | :-: | :-: |
| Wings closed | Wings open | Wing-spread clip |
| <img src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/readme-chain-monarch-01-open.png" width="280" height="494" alt="Monarch butterfly on lavender, wings closed"> | <img src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/readme-chain-monarch-02-end.png" width="280" height="494" alt="Same monarch with wings open"> | <img src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/readme-chain-monarch-clip.gif" width="280" height="494" alt="Monarch wing-spread video clip preview"> |

**Workflow: illustrated story reel**

> Make an illustrated story still of a whale in a library, narrate a short line, and assemble a Ken Burns reel.

| Step 1 · `p-image` | Step 2 · `gemini-3.1-flash-tts` | Step 3 · assembly |
| :-: | :-: | :-: |
| Story still | [Narration audio](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/illustrated-library-whale-narration.mp3) | Ken Burns reel |
| <img src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/readme-illustrated-library-whale.png" width="280" height="494" alt="Illustrated whale in a library"> | *MP3 link above* | <img src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/readme-illustrated-library-whale-reel.gif" width="280" height="494" alt="Illustrated story reel preview"> |

For more inspiration, see [docs/EXAMPLES.md](docs/EXAMPLES.md). For ready-made multi-step recipes, see [docs/WORKFLOW-RECIPES.md](docs/WORKFLOW-RECIPES.md).

## How this works

Skills come in four types. Together they take you from a plain-language request to finished media.

| Type | Role | Example |
|------|------|---------|
| **Suite** | Everything in one install: guides, tools, and workflows | `@pruna` |
| **Guide** | Prompting craft and API conventions | `@image-prompting` |
| **Tool** | One paid API call | `@p-image` |
| **Workflow** | A multi-step playbook your agent runs with curl and ffmpeg | `@music-video` |

When you install `@pruna`, you already have every skill listed below. If you install a single tool instead, it pulls in the guides it needs under **Prerequisites**. Workflows list the tools they depend on, so you only need to install those separately when you skip the suite.

### Install one skill at a time

If you prefer to start small, pick a single skill:

```bash
npx skills add PrunaAI/pruna-skills@p-image -y          # one tool (+ its Prerequisites)
npx skills add PrunaAI/pruna-skills@music-video -y      # one workflow
npx skills add PrunaAI/pruna-skills -l                  # list all
```

## What's in the suite

Full descriptions live in [docs/SKILL-CATALOG.md](docs/SKILL-CATALOG.md).

### Guides (5)

| You want… | Skill |
|-----------|-------|
| Diverse prompts and QA gates before you spend on API calls | `generation-diversity` |
| Still-image prompting | `image-prompting` |
| Video and motion prompting | `video-prompting` |
| TTS, music, and background beds | `audio-prompting` |
| Pruna and Replicate HTTP, plus agent safety | `pruna-api` |

### Tools (12)

| You want… | Skill |
|-----------|-------|
| Fast text-to-image | `p-image` |
| Edit or combine from reference photos | `p-image-edit` |
| Virtual try-on | `p-image-try-on` |
| Upscale | `p-image-upscale` |
| One video clip | `p-video` |
| Copy motion from one video to another | `p-video-animate` |
| A person on camera speaking | `p-video-avatar` |
| Swap a person or product in video | `p-video-replace` |
| Narration (text to speech) | `gemini-3.1-flash-tts` |
| A song with vocals | `music-2.5` |
| Background music without vocals | `stable-audio-2.5` |
| Lyric timestamps | `whisperx` |

### Workflows (8)

| You want… | Skill |
|-----------|-------|
| Turn images into video clips | `image-to-video` |
| A multi-part story with narration | `narrated-multi-scene` |
| A scene-to-scene transition montage | `visual-transition-reel` |
| One short presenter clip | `avatar-single-scene` |
| The same presenter across several scenes | `avatar-multi-scene` |
| An educational explainer | `interactive-explainer` |
| A full music video | `music-video` |
| An illustrated slideshow reel | `illustrated-story-reel` |

## Other install channels

You can also install through ClawHub and related channels. See [PUBLISHING.md](docs/PUBLISHING.md) for details.

## API setup

Set `PRUNA_API_KEY` and, for audio tools, `REPLICATE_API_TOKEN`. Step-by-step instructions are in [docs/api-setup.md](docs/api-setup.md).

## Repo layout

All installable skills live under `skills/`. Craft markdown sits next to each guide or workflow in `references/`. There is no top-level `references/` or `plugins/` tree.

```text
skills/
  guides/                 generation-diversity, *-prompting, pruna-api
  image/                  p-image, p-image-edit, p-image-try-on, p-image-upscale
  video/                  p-video, p-video-avatar, p-video-animate, p-video-replace
  audio/                  gemini-3.1-flash-tts, music-2.5, stable-audio-2.5, whisperx
  workflows/              8 multi-step playbooks
  suite/pruna/            umbrella @pruna  ← quickstart
docs/                     human docs (setup, recipes, examples, catalog)
.maintainer/              catalog, bundle, verify, publish
.github/workflows/        verify-skills.yml (PR / main CI)
```

| Path | Role |
|------|------|
| `skills/suite/pruna/` | Full suite; default install |
| `skills/guides/` | Craft SSoT + `pruna-api` |
| `skills/{image,video,audio}/` | Tools (Prerequisites → guides) |
| `skills/workflows/` | Playbooks (Prerequisites → tools) |
| `docs/` | Human docs; not loaded as skills |
| `.maintainer/skills.catalog.json` | Skill name source of truth |

Maintainers: run `make bundle && make verify && make validate`. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

See [LICENSE](./LICENSE).
