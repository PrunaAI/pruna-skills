"""Hugging Face dataset URLs for docs/assets/examples."""

from __future__ import annotations

import re

HF_DATASET = "PrunaAI/pruna-skills"
HF_REVISION = "main"
HF_PATH_PREFIX = "examples"

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


def is_hf_example_url(url: str) -> bool:
    return bool(_HF_RESOLVE_RE.match(url))


def rewrite_markdown(text: str) -> str:
    """Replace local example paths with Hugging Face resolve URLs."""

    file_pat = r"[^\s)\]\"'<>]+\.(?:png|mp4|mp3|json|webp|gif|mov|webm)"

    def sub_local(match: re.Match[str]) -> str:
        return hf_url(match.group(1))

    for prefix in _LOCAL_PREFIXES:
        text = re.sub(
            rf"(?<![/\w]){re.escape(prefix)}({file_pat})",
            sub_local,
            text,
        )
    return text
