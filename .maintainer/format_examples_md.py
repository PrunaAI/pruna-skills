#!/usr/bin/env python3
"""Put **Output** first and wrap prompts in <details> for docs/EXAMPLES.md."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "docs" / "EXAMPLES.md"

SECTION_RE = re.compile(r"(^## .+$)", re.MULTILINE)
OUTPUT_RE = re.compile(
    r"(^!\[[^\]]*\]\([^\)]+\)\s*$|^<video src=\"[^\"]+\"[^>]*></video>\s*$|^\*\*Output\*\*[^\n]*\n(?:.*\n)*?)(?=^```bash|^---|\Z)",
    re.MULTILINE,
)
PROMPT_START = re.compile(r"^\*\*Ask your agent\*\*", re.MULTILINE)


def _extract_output(block: str) -> tuple[str, str]:
    """Return (output_md, rest_without_output_lines)."""
    lines = block.splitlines(keepends=True)
    out_idx: list[int] = []
    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith("![") or s.startswith("<video "):
            out_idx.append(i)
        if s.startswith("**Output"):
            # already formatted — grab until bash or details
            j = i + 1
            while j < len(lines) and not lines[j].startswith("```bash") and not lines[j].startswith("<details"):
                if lines[j].strip().startswith("![") or lines[j].strip().startswith("<video"):
                    out_idx.append(j)
                j += 1

    if not out_idx:
        return "", block

    output_lines = [lines[i] for i in out_idx]
    rest = [line for i, line in enumerate(lines) if i not in out_idx]
    output = "**Output**\n\n" + "".join(output_lines).strip() + "\n\n"
    return output, "".join(rest)


def format_section(body: str) -> str:
    if "<details>" in body and "**Output**" in body:
        return body
    if not PROMPT_START.search(body):
        return body

    output, rest = _extract_output(body)
    rest = rest.strip()
    if not output:
        return body

    # drop duplicate blank lines before bash
    rest = re.sub(r"\n{3,}", "\n\n", rest)
    m = re.search(r"(```bash[\s\S]*?```)", rest)
    install = m.group(1) if m else ""
    middle = rest[: m.start()].strip() if m else rest.strip()
    middle = re.sub(r"\n{3,}", "\n\n", middle)

    parts = [output.rstrip(), ""]
    if middle:
        parts.extend(
            [
                "<details>",
                "<summary>Prompts & inputs</summary>",
                "",
                middle,
                "",
                "</details>",
                "",
            ]
        )
    if install:
        parts.extend([install, ""])
    return "\n".join(parts).rstrip() + "\n"


def main() -> None:
    text = EXAMPLES.read_text(encoding="utf-8")
    chunks = SECTION_RE.split(text)
    if len(chunks) < 2:
        raise SystemExit("no ## sections found")

    out = [chunks[0]]
    headers = chunks[1::2]
    bodies = chunks[2::2]
    for header, body in zip(headers, bodies):
        out.append(header + "\n\n")
        out.append(format_section(body))

    EXAMPLES.write_text("".join(out), encoding="utf-8")
    print(f"formatted {EXAMPLES.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
