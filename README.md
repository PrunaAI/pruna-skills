# Pruna Skills

[![Pruna Skills: images, video, music, explainers, avatars, and workflows for agent coding tools](docs/assets/readme-hero-pruna-skills.gif)](https://github.com/PrunaAI/pruna-skills/raw/main/docs/assets/readme-hero-pruna-skills.mp4)

Pruna Skills teach your coding agent how to generate images, video, and audio with the [Pruna AI API](https://docs.api.pruna.ai/guides/models). They also cover multi-step workflows — explainers, music videos, avatars, illustrated reels — that chain those calls together. Each skill follows the [Agent Skills](https://agentskills.io/specification) format, so it works in Cursor, Claude Code, Copilot, Codex, and [many other agents](https://skills.sh).

## Quickstart

Set your API key, install the **`/pruna`** suite skill, and start a new chat.

```bash
export PRUNA_API_KEY="your_key"   # see [api-setup.md](docs/api-setup.md)

npx skills add PrunaAI/pruna-skills@pruna -y
```

That installs the full suite — every guide, tool, and workflow in one shot. After install, open a **new chat** and describe what you want in plain language — your agent picks the right skills from the suite.

### Try it: ask your agent

**Create an image, then try on clothes, then create a video**

> Create a portrait of a teenage girl drummer in a garage. Put a vintage red band jacket on her from a garment reference, and keep the pose and background. Then make her sing along to a song slice as a lip-sync performance clip.

| Step 1 · `p-image` | Step 2 · `p-image-try-on` | Step 3 · `p-video-avatar` |
| :-: | :-: | :-: |
| Image | Try-on | Video |
| <img src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/readme-music-video-garage-drummer.png" width="280" height="494" alt="Teenage drummer portrait in a garage"> | <img src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/readme-p-image-try-on-drummer.png" width="280" height="494" alt="Same drummer wearing the red band jacket"> | <img src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/readme-music-video-garage-drummer-clip.gif" width="280" height="494" alt="Drummer lip-sync performance clip wearing the red band jacket"> |

**Create an image, then edit it, then create a video**

> Create a product photo of a white running sneaker on a shelf. Edit it to the same shoe in bright orange. Animate a color shift, then a hand picking it up.

| Step 1 · `p-image` | Step 2 · `p-image-edit` | Step 3 · `p-video` |
| :-: | :-: | :-: |
| Image | Edit | Video |
| <img src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/readme-chain-sneaker-01-open.png" width="280" height="494" alt="White running sneaker product shot on a shelf"> | <img src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/readme-chain-sneaker-02-end.png" width="280" height="494" alt="Same sneaker edited to bright orange"> | <img src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/readme-chain-sneaker-clip.gif" width="280" height="494" alt="Sneaker color shift and hand pickup clip"> |

**Create an image, then add narration, then assemble a video**

> Create an illustrated story image of a whale in a library, narrate a short line, and assemble a Ken Burns reel.

| Step 1 · `p-image` | Step 2 · `gemini-3.1-flash-tts` | Step 3 · assembly |
| :-: | :-: | :-: |
| Image | [Narration](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/illustrated-library-whale-narration.mp3) | Video |
| <img src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/readme-illustrated-library-whale.png" width="280" height="494" alt="Illustrated whale in a library"> | *MP3 link above* | <img src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/readme-illustrated-library-whale-reel.gif" width="280" height="494" alt="Illustrated story reel preview"> |

More examples: [docs/EXAMPLES.md](docs/EXAMPLES.md). Ready-made multi-step recipes: [docs/WORKFLOW-RECIPES.md](docs/WORKFLOW-RECIPES.md).

## How it works

Skills come in four types:

| Type | What it does | Example |
|------|--------------|---------|
| **Suite** | Everything in one install | `pruna` |
| **Guide** | Prompting craft and API safety — no generation call on its own | `image-prompting` |
| **Tool** | One paid endpoint — a single Pruna or Replicate API call | `p-image` |
| **Workflow** | A multi-step playbook your agent runs with curl and ffmpeg | `music-video` |

Guides teach *how* to prompt and call the API safely. Tools are the endpoints — one model per skill (`p-image`, `p-video`, `music-2.5`, …). Workflows chain tools into finished deliverables.

When you install `pruna`, you get the whole catalog. Installing a single tool instead pulls in only the guides listed under its **Prerequisites**. Workflows list the tools they need — you only install those separately if you skipped the suite.

### Install one skill at a time

Prefer to start small? Pick a single skill:

```bash
npx skills add PrunaAI/pruna-skills@p-image -y          # one tool (+ its guides)
npx skills add PrunaAI/pruna-skills@music-video -y      # one workflow
npx skills add PrunaAI/pruna-skills -l                  # list all
```

## What's in the suite

The `pruna` suite includes 26 skills across guides, tools, and workflows. You don't need to memorize them — describe your goal in chat and your agent picks what fits.

- **Browse by goal:** [docs/SKILL-CATALOG.md](docs/SKILL-CATALOG.md)
- **Per-skill install commands:** [skills/suite/pruna/SKILL.md](skills/suite/pruna/SKILL.md)
- **Multi-step recipes:** [docs/WORKFLOW-RECIPES.md](docs/WORKFLOW-RECIPES.md)

## API setup

Set `PRUNA_API_KEY` for images and video. Audio tools also need `REPLICATE_API_TOKEN`. Step-by-step instructions: [docs/api-setup.md](docs/api-setup.md).

## Other install channels

ClawHub and related channels are supported too. See [PUBLISHING.md](docs/PUBLISHING.md).

## Contributing

Installable skills live under `skills/` (guides, tools, workflows, and the `pruna` suite). Human docs live in `docs/`. Maintainers: `make bundle && make verify && make validate` — see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

See [LICENSE](./LICENSE).
