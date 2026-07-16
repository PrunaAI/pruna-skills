#!/usr/bin/env python3
"""Convert WhisperX transcript JSON to YouTube-ready .srt subtitles."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

DEFAULT_MAX_CHARS = 42
DEFAULT_MAX_DURATION = 7.0
DEFAULT_MAX_LINES = 2
WHITESPACE = re.compile(r"\s+")


def format_srt_time(seconds: float) -> str:
    if seconds < 0:
        seconds = 0.0
    total_ms = int(round(seconds * 1000))
    hours, rem = divmod(total_ms, 3_600_000)
    minutes, rem = divmod(rem, 60_000)
    secs, ms = divmod(rem, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"


def normalize_text(text: str) -> str:
    return WHITESPACE.sub(" ", text.strip())


def flatten_words(transcript: dict) -> list[dict]:
    words: list[dict] = []
    for segment in transcript.get("segments") or []:
        for word in segment.get("words") or []:
            text = normalize_text(word.get("word") or "")
            if not text:
                continue
            words.append(
                {
                    "word": text,
                    "start": float(word["start"]),
                    "end": float(word["end"]),
                }
            )
    return words


def wrap_subtitle_text(text: str, *, max_chars: int, max_lines: int) -> str:
    if len(text) <= max_chars:
        return text

    parts = text.split()
    lines: list[str] = []
    current: list[str] = []

    for part in parts:
        candidate = " ".join(current + [part])
        if current and len(candidate) > max_chars:
            lines.append(" ".join(current))
            current = [part]
            if len(lines) >= max_lines:
                break
        else:
            current.append(part)

    if len(lines) < max_lines and current:
        lines.append(" ".join(current))

    if len(lines) == max_lines and len(" ".join(parts)) > len("\n".join(lines)):
        consumed = len(" ".join(lines[:-1]).split()) if len(lines) > 1 else 0
        consumed += len(lines[-1].split()) if lines else 0
        if consumed < len(parts):
            overflow = " ".join(parts[consumed:])
            if overflow:
                lines[-1] = f"{lines[-1]} {overflow}".strip()

    return "\n".join(lines[:max_lines])


def group_words_into_cues(
    words: list[dict],
    *,
    max_chars: int,
    max_duration: float,
    max_lines: int,
    gap_break_sec: float = 0.45,
) -> list[dict]:
    if not words:
        return []

    cues: list[dict] = []
    chunk: list[dict] = []

    def flush() -> None:
        nonlocal chunk
        if not chunk:
            return
        text = wrap_subtitle_text(
            " ".join(item["word"] for item in chunk),
            max_chars=max_chars,
            max_lines=max_lines,
        )
        cues.append({"start": chunk[0]["start"], "end": chunk[-1]["end"], "text": text})
        chunk = []

    for index, word in enumerate(words):
        if chunk:
            gap = word["start"] - chunk[-1]["end"]
            candidate_text = " ".join(item["word"] for item in chunk + [word])
            candidate_duration = word["end"] - chunk[0]["start"]
            if gap >= gap_break_sec or len(candidate_text) > max_chars * max_lines or candidate_duration > max_duration:
                flush()
        chunk.append(word)

        if index == len(words) - 1:
            flush()

    return cues


def cues_from_segments(transcript: dict, *, max_chars: int, max_lines: int) -> list[dict]:
    cues: list[dict] = []
    for segment in transcript.get("segments") or []:
        text = normalize_text(segment.get("text") or "")
        if not text:
            continue
        cues.append(
            {
                "start": float(segment["start"]),
                "end": float(segment["end"]),
                "text": wrap_subtitle_text(text, max_chars=max_chars, max_lines=max_lines),
            }
        )
    return cues


def build_srt_cues(
    transcript: dict,
    *,
    max_chars: int = DEFAULT_MAX_CHARS,
    max_duration: float = DEFAULT_MAX_DURATION,
    max_lines: int = DEFAULT_MAX_LINES,
) -> list[dict]:
    words = flatten_words(transcript)
    if words:
        return group_words_into_cues(
            words,
            max_chars=max_chars,
            max_duration=max_duration,
            max_lines=max_lines,
        )
    return cues_from_segments(transcript, max_chars=max_chars, max_lines=max_lines)


def render_srt(cues: list[dict]) -> str:
    blocks: list[str] = []
    for index, cue in enumerate(cues, start=1):
        start = format_srt_time(float(cue["start"]))
        end = format_srt_time(float(cue["end"]))
        text = str(cue["text"]).strip()
        if not text:
            continue
        blocks.append(f"{index}\n{start} --> {end}\n{text}")
    return "\n\n".join(blocks) + ("\n" if blocks else "")


def transcript_to_srt(
    transcript: dict,
    *,
    max_chars: int = DEFAULT_MAX_CHARS,
    max_duration: float = DEFAULT_MAX_DURATION,
    max_lines: int = DEFAULT_MAX_LINES,
) -> str:
    cues = build_srt_cues(
        transcript,
        max_chars=max_chars,
        max_duration=max_duration,
        max_lines=max_lines,
    )
    return render_srt(cues)


def write_srt_from_transcript(
    transcript: dict,
    out_path: Path,
    *,
    max_chars: int = DEFAULT_MAX_CHARS,
    max_duration: float = DEFAULT_MAX_DURATION,
    max_lines: int = DEFAULT_MAX_LINES,
) -> int:
    cues = build_srt_cues(
        transcript,
        max_chars=max_chars,
        max_duration=max_duration,
        max_lines=max_lines,
    )
    srt = render_srt(cues)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(srt, encoding="utf-8")
    return len([cue for cue in cues if str(cue.get("text", "")).strip()])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--transcript", type=Path, required=True, help="whisperx_transcript.json")
    parser.add_argument("--out", type=Path, help="Output .srt (default: same stem as transcript)")
    parser.add_argument("--max-chars", type=int, default=DEFAULT_MAX_CHARS)
    parser.add_argument("--max-duration", type=float, default=DEFAULT_MAX_DURATION)
    parser.add_argument("--max-lines", type=int, default=DEFAULT_MAX_LINES)
    args = parser.parse_args()

    if not args.transcript.exists():
        raise SystemExit(f"Missing {args.transcript}")

    transcript = json.loads(args.transcript.read_text())
    out_path = args.out or args.transcript.with_suffix(".srt")
    cue_count = write_srt_from_transcript(
        transcript,
        out_path,
        max_chars=args.max_chars,
        max_duration=args.max_duration,
        max_lines=args.max_lines,
    )
    print(f"Wrote {out_path} ({cue_count} cues)")


if __name__ == "__main__":
    main()
