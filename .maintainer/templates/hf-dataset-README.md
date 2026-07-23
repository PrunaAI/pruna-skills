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
  p-image-advanced.png
  p-image-advanced.meta.json
  quickstart-knight-still.png
  quickstart-knight-clip.mp4
  chain-monarch-clip.mp4
  …
```

## Regenerate (maintainers)

From the skills repo:

```bash
make download-doc-examples-hf   # pull checked-in examples from HF (no API)
python3 .maintainer/generate_doc_examples.py --only pruna-docs-vendor
make doc-examples               # regenerate API-backed examples
make sync-doc-examples-hf       # upload + refresh EXAMPLES.md HF URLs
```

Requires `PRUNA_API_KEY` for API generation and a Hugging Face token with write access to `PrunaAI/pruna-skills`.

## Direct URL

`https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/<filename>`
