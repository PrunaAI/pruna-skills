#!/usr/bin/env python3
"""Rewrite docs/EXAMPLES.md embeds: GIF previews + links (GitHub-safe)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

EXAMPLES = ROOT / "docs" / "EXAMPLES.md"
OUT = ROOT / "docs" / "assets" / "examples"

from doc_examples_hf import hf_url, rewrite_markdown  # noqa: E402

HF_MP4 = re.compile(
    r'https://huggingface\.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/([a-z0-9_-]+\.mp4)'
)
VIDEO_TAG = re.compile(
    r'<video\s+src="(https://huggingface\.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/[a-z0-9_-]+\.mp4)"\s+controls(?:\s+width="\d+")?\s*></video>'
)
AUDIO_TAG = re.compile(
    r'<audio\s+src="(https://huggingface\.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/[a-z0-9_-]+\.(?:mp3|wav))"\s+controls\s*></audio>'
)


def _alt(name: str) -> str:
    return name.replace("-", " ").removesuffix(".mp4").removesuffix(".mp3")


def gif_preview_cell(mp4_url: str, *, compact: bool) -> str:
    name = HF_MP4.search(mp4_url)
    if not name:
        return mp4_url
    base = name.group(1)
    gif_name = base.replace(".mp4", ".gif")
    gif_url = hf_url(gif_name)
    alt = _alt(base)
    cell = f"[![{alt}]({gif_url})]({mp4_url})"
    if compact:
        return cell
    return (
        f"[![{alt} preview]({gif_url})]({mp4_url})\n\n"
        f"*Preview (mute). [Full clip with audio →]({mp4_url})*"
    )


def whisperx_sample() -> str:
    wx = OUT / "whisperx-drummer-song.json"
    if not wx.is_file():
        return ""
    import json

    data = json.loads(wx.read_text(encoding="utf-8"))
    words: list[str] = []
    for seg in data.get("segments") or []:
        for w in seg.get("words") or []:
            words.append(str(w.get("word", "")).strip())
        if len(words) >= 12:
            break
    snippet = " ".join(words[:12])
    if len(words) > 12:
        snippet += " …"
    return snippet


def embed(text: str) -> str:
    def sub_video(match: re.Match[str]) -> str:
        url = match.group(1)
        # table cells stay one line
        compact = match.string[max(0, match.start() - 1) : match.start()] == "|"
        return gif_preview_cell(url, compact=compact)

    text = VIDEO_TAG.sub(sub_video, text)

    def sub_audio(match: re.Match[str]) -> str:
        url = match.group(1)
        name = url.rsplit("/", 1)[-1]
        return f"[▶ Listen — `{name}`]({url})"

    text = AUDIO_TAG.sub(sub_audio, text)

    # whisperx: add inline sample when sidecar exists
    wx_url = hf_url("whisperx-drummer-song.json")
    sample = whisperx_sample()
    if sample and wx_url in text and "Word sample:" not in text:
        text = re.sub(
            r"(\*\*Output\*\* — \[`whisperx-drummer-song\.json`\]\("
            + re.escape(wx_url)
            + r"\)[^\n]*)",
            rf"\1\n\n> **Word sample:** {sample}",
            text,
            count=1,
        )

    return text


def main() -> None:
    original = EXAMPLES.read_text(encoding="utf-8")
    updated = embed(rewrite_markdown(original))
    if updated == original:
        print("no embed changes")
        return
    EXAMPLES.write_text(updated, encoding="utf-8")
    print(f"updated {EXAMPLES.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
