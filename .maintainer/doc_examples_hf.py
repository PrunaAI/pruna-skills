"""Hugging Face dataset URLs for docs/assets/examples."""

from __future__ import annotations

import re

HF_DATASET = "PrunaAI/pruna-skills"
HF_REVISION = "main"
HF_PATH_PREFIX = "examples"

# Vendored from Pruna docs — tracked in git for GitHub rendering (also run make sync-doc-examples-hf)
GIT_VENDORED = {
    "p-image-advanced.png",
    "p-image-advanced.meta.json",
    "p-image-edit-demo.png",
    "p-image-edit-demo.meta.json",
    "p-image-upscale-advanced.png",
    "p-image-upscale-advanced.meta.json",
    "p-image-upscale-source.png",
    "quickstart-knight-still.png",
    "quickstart-knight-still.meta.json",
    "quickstart-knight-clip.mp4",
    "quickstart-knight-clip.meta.json",
    "quickstart-knight-clip.gif",
}

_LOCAL_PREFIXES = ("assets/examples/", "docs/assets/examples/")
_HF_RESOLVE_RE = re.compile(
    rf"https://huggingface\.co/datasets/{re.escape(HF_DATASET)}/resolve/{re.escape(HF_REVISION)}/{re.escape(HF_PATH_PREFIX)}/"
)


def hf_dataset_page() -> str:
    return f"https://huggingface.co/datasets/{HF_DATASET}"


def hf_url(filename: str) -> str:
    name = filename.lstrip("/")
    if name.startswith(f"{HF_PATH_PREFIX}/"):
        name = name[len(HF_PATH_PREFIX) + 1 :]
    return f"https://huggingface.co/datasets/{HF_DATASET}/resolve/{HF_REVISION}/{HF_PATH_PREFIX}/{name}"


def example_media_url(filename: str) -> str:
    """Repo-relative path for git-tracked vendored assets; HF URL for the rest."""
    name = filename.lstrip("/").split("/")[-1]
    if name in GIT_VENDORED:
        return f"assets/examples/{name}"
    return hf_url(name)


def is_hf_example_url(url: str) -> bool:
    return bool(_HF_RESOLVE_RE.match(url))


def rewrite_markdown(text: str) -> str:
    """Replace local example paths with example_media_url (HF or in-repo)."""

    file_pat = r"[^\s)\]\"'<>]+\.(?:png|mp4|mp3|json|webp|gif|mov|webm)"

    def sub_local(match: re.Match[str]) -> str:
        return example_media_url(match.group(1))

    for prefix in _LOCAL_PREFIXES:
        text = re.sub(
            rf"(?<![/\w]){re.escape(prefix)}({file_pat})",
            sub_local,
            text,
        )
    return text
