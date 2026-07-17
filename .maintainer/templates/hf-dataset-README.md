---
license: apache-2.0
task_categories:
- text-to-image
- text-to-video
- text-to-speech
language:
- en
tags:
- pruna
- generative-ai
- agent-skills
pretty_name: Pruna Skills doc examples
size_categories:
- n<1K
---

# Pruna Skills — doc examples

Generated media and sidecars for [PrunaAI/pruna-skills](https://github.com/PrunaAI/pruna-skills) documentation.

Each file under `examples/` matches a skill demo in [docs/EXAMPLES.md](https://github.com/PrunaAI/pruna-skills/blob/main/docs/EXAMPLES.md). PNG/MP3/MP4 outputs have a sibling `.meta.json` with the exact prompt, model, and inputs.

## Layout

```text
examples/
  p-image-brass-hummingbird.png
  p-image-brass-hummingbird.meta.json
  chain-monarch-clip.mp4
  …
```

## Regenerate (maintainers)

From the skills repo:

```bash
make download-doc-examples-hf   # pull checked-in examples from HF (no API)
make doc-examples               # regenerate via Pruna API
make upload-doc-examples-hf
make doc-examples-urls
```

Requires `PRUNA_API_KEY` for generation and a Hugging Face token with write access to `PrunaAI/pruna-skills`.

## Direct URL

`https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/<filename>`
