# Pruna Skills

![Pruna Skills — images, video, music, explainers, avatars, and workflows for agent coding tools](docs/assets/readme-hero-pruna-skills.png)

Generate images, video, and audio with the [Pruna AI API](https://docs.api.pruna.ai/guides/models), plus multi-step workflows (explainers, music videos, avatars, and more). Skills follow the [Agent Skills](https://agentskills.io/specification) format and work in Cursor, Claude Code, Copilot, Codex, and [many more agents](https://skills.sh).

## Quickstart — install the suite

One command installs **everything**: guides, tools, and workflows.

```bash
export PRUNA_API_KEY="your_key"   # see [api-setup.md](docs/api-setup.md)

npx skills add PrunaAI/pruna-skills@pruna -y
```

Start a **new chat**, then ask for what you want — your agent picks the right skills from the suite.

Skim [agent safety](skills/guides/pruna-api/references/agent-safety.md) before enabling skills in untrusted repos.

### Try it — ask your agent

**Portrait → try-on → performance**

> Create a portrait of a teenage girl drummer in a garage. Put a vintage red band jacket on her from a garment reference — keep pose and background. Then make her sing along to a song slice as a lip-sync performance clip.

| Step 1 · `p-image` | Step 2 · `p-image-try-on` | Step 3 · `p-video-avatar` |
| :-: | :-: | :-: |
| Drummer portrait | Jacket try-on | Performance clip |
| <img src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/readme-music-video-garage-drummer.png" width="280" height="494" alt="Teenage drummer portrait in a garage"> | <img src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/readme-p-image-try-on-drummer.png" width="280" height="494" alt="Same drummer wearing the red band jacket"> | <img src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/readme-music-video-garage-drummer-clip.gif" width="280" height="494" alt="Drummer lip-sync performance clip wearing the red band jacket"> |

**Still → edit → clip**

> Generate a monarch butterfly on lavender with wings closed. Edit so the wings open wide — same stem and camera. Then animate a short clip of the wing-spread.

| Step 1 · `p-image` | Step 2 · `p-image-edit` | Step 3 · `p-video` |
| :-: | :-: | :-: |
| Wings closed | Wings open | Wing-spread clip |
| <img src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/readme-chain-monarch-01-open.png" width="280" height="494" alt="Monarch butterfly on lavender, wings closed"> | <img src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/readme-chain-monarch-02-end.png" width="280" height="494" alt="Same monarch with wings open"> | <img src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/readme-chain-monarch-clip.gif" width="280" height="494" alt="Monarch wing-spread video clip preview"> |

**Workflow — illustrated story reel**

> Make an illustrated story still of a whale in a library, narrate a short line, and assemble a Ken Burns reel.

| Step 1 · `p-image` | Step 2 · `gemini-3.1-flash-tts` | Step 3 · assembly |
| :-: | :-: | :-: |
| Story still | [Narration audio](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/illustrated-library-whale-narration.mp3) | Ken Burns reel |
| <img src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/readme-illustrated-library-whale.png" width="280" height="494" alt="Illustrated whale in a library"> | *MP3 link above* | <img src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/readme-illustrated-library-whale-reel.gif" width="280" height="494" alt="Illustrated story reel preview"> |

More examples: [docs/EXAMPLES.md](docs/EXAMPLES.md). Recipes: [docs/WORKFLOW-RECIPES.md](docs/WORKFLOW-RECIPES.md).

## How this works

| Type | Role | Example |
|------|------|---------|
| **Suite** | Happy path — all guides, tools, and workflows | `@pruna` |
| **Guide** | Vendor-neutral craft or Pruna HTTP | `@image-prompting` |
| **Tool** | One paid API call | `@p-image` |
| **Workflow** | Multi-step playbook (curl + ffmpeg) | `@music-video` |

With `@pruna` you already have every skill below. Tools list guides under **Prerequisites**; workflows list tools — install those only if you skip the suite.

### Optional — install one skill

```bash
npx skills add PrunaAI/pruna-skills@p-image -y          # one tool (+ its Prerequisites)
npx skills add PrunaAI/pruna-skills@music-video -y      # one workflow
npx skills add PrunaAI/pruna-skills -l                  # list all
```

## What’s in the suite

Full descriptions: [docs/SKILL-CATALOG.md](docs/SKILL-CATALOG.md).

### Guides (5)

| You want… | Skill |
|-----------|-------|
| Diverse prompts + QA gates | `generation-diversity` |
| Still-image prompting | `image-prompting` |
| Video / motion prompting | `video-prompting` |
| TTS, music, beds | `audio-prompting` |
| Pruna / Replicate HTTP + safety | `pruna-api` |

### Tools (12)

| You want… | Skill |
|-----------|-------|
| Fast text-to-image | `p-image` |
| Edit or combine from reference photos | `p-image-edit` |
| Virtual try-on | `p-image-try-on` |
| Upscale | `p-image-upscale` |
| One video clip | `p-video` |
| Copy motion from one video to another | `p-video-animate` |
| Person on camera speaking | `p-video-avatar` |
| Swap person or product in video | `p-video-replace` |
| Narration (text to speech) | `gemini-3.1-flash-tts` |
| Song with vocals | `music-2.5` |
| Background music (no vocals) | `stable-audio-2.5` |
| Lyric timestamps | `whisperx` |

### Workflows (8)

| You want… | Skill |
|-----------|-------|
| Turn images into video clips | `image-to-video` |
| Multi-part story with narration | `narrated-multi-scene` |
| Scene-to-scene transition montage | `visual-transition-reel` |
| One short presenter clip | `avatar-single-scene` |
| Presenter across several scenes | `avatar-multi-scene` |
| Educational explainer | `interactive-explainer` |
| Full music video | `music-video` |
| Illustrated slideshow reel | `illustrated-story-reel` |

## Other install channels

ClawHub and related — [PUBLISHING.md](docs/PUBLISHING.md).

## API setup

[docs/api-setup.md](docs/api-setup.md) — `PRUNA_API_KEY`, `REPLICATE_API_TOKEN`.

## Repo layout

All installable skills live under `skills/`. Craft markdown sits next to each guide or workflow (`references/`). There is no top-level `references/` or `plugins/` tree.

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
| `skills/suite/pruna/` | Full suite — default install |
| `skills/guides/` | Craft SSoT + `pruna-api` |
| `skills/{image,video,audio}/` | Tools (Prerequisites → guides) |
| `skills/workflows/` | Playbooks (Prerequisites → tools) |
| `docs/` | Humans — not loaded as skills |
| `.maintainer/skills.catalog.json` | Skill name source of truth |

Maintainers: `make bundle && make verify && make validate` — [CONTRIBUTING.md](CONTRIBUTING.md).

## License

See [LICENSE](./LICENSE).
