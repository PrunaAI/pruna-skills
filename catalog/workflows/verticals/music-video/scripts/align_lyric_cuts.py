#!/usr/bin/env python3
"""Align cut_manifest timings to WhisperX word-level timestamps."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from difflib import SequenceMatcher
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from cut_timing import MIN_PVIDEO_AUDIO_SEC, POST_PAD_SEC, PRE_PAD_SEC

PAREN_ONLY = re.compile(r"^\([^)]+\)\s*$")
TOKEN = re.compile(r"[a-z0-9']+")


def normalize_token(word: str) -> str:
    tokens = TOKEN.findall(word.lower())
    return "".join(tokens) if tokens else ""


def line_tokens(line: str) -> list[str]:
    return [t for t in (normalize_token(part) for part in line.split()) if t]


def flatten_words(transcript: dict) -> list[dict]:
    words: list[dict] = []
    for segment in transcript.get("segments") or []:
        for word in segment.get("words") or []:
            text = (word.get("word") or "").strip()
            if not text:
                continue
            words.append(
                {
                    "word": text,
                    "token": normalize_token(text),
                    "start": float(word["start"]),
                    "end": float(word["end"]),
                    "score": float(word.get("score") or 0),
                }
            )
    return words


def token_match(plan_token: str, spoken_token: str) -> bool:
    if not plan_token or not spoken_token:
        return False
    if plan_token == spoken_token:
        return True
    if plan_token in spoken_token or spoken_token in plan_token:
        return True
    if len(plan_token) >= 4 and len(spoken_token) >= 4:
        return plan_token[:4] == spoken_token[:4]
    if len(plan_token) <= 3 and len(spoken_token) <= 3:
        return plan_token[0] == spoken_token[0]
    return False


def token_similarity(plan_token: str, spoken_token: str) -> float:
    if not plan_token or not spoken_token:
        return 0.0
    if token_match(plan_token, spoken_token):
        return 1.0
    return SequenceMatcher(None, plan_token, spoken_token).ratio()


def token_fuzzy_match(plan_token: str, spoken_token: str, *, min_ratio: float = 0.55) -> bool:
    if token_match(plan_token, spoken_token):
        return True
    ratio = token_similarity(plan_token, spoken_token)
    needed = min_ratio if min(len(plan_token), len(spoken_token)) >= 4 else max(0.5, min_ratio - 0.05)
    return ratio >= needed


def spoken_covers_token(plan_token: str, words: list[dict], index: int) -> tuple[bool, int]:
    """Return (matched, last_word_index_consumed)."""
    if index >= len(words):
        return False, index
    if plan_token == "chatgpt" and index + 1 < len(words):
        if words[index]["token"] == "chat" and words[index + 1]["token"] == "gpt":
            return True, index + 1
        if words[index]["token"] == "chatgpt":
            return True, index
    if plan_token == "openai" and index + 1 < len(words):
        if words[index]["token"] == "open" and words[index + 1]["token"] == "ai":
            return True, index + 1
        if words[index]["token"] == "openai":
            return True, index
    if token_fuzzy_match(plan_token, words[index]["token"]):
        return True, index
    return False, index


def score_token_alignment(plan_tokens: list[str], words: list[dict], start: int, end: int) -> tuple[float, int]:
    """Greedy-align plan tokens to spoken words[start:end], allowing extra spoken words and skipped plan words."""
    if start > end or start >= len(words):
        return 0.0, start

    spoken_slice = words[start : end + 1]
    if not spoken_slice or not plan_tokens:
        return 0.0, start

    matched = 0
    pi = 0
    wi = 0
    last_idx = start
    plan_skips = 0
    max_plan_skips = max(2, len(plan_tokens) // 4)

    while pi < len(plan_tokens) and wi < len(spoken_slice):
        token = plan_tokens[pi]
        found = False
        for skip in range(0, min(10, len(spoken_slice) - wi)):
            idx = wi + skip
            ok, _ = spoken_covers_token(token, spoken_slice, idx)
            if ok:
                matched += 1
                last_idx = start + idx
                wi = idx + 1
                pi += 1
                found = True
                break
        if found:
            continue
        if plan_skips < max_plan_skips:
            plan_skips += 1
            pi += 1
            continue
        wi += 1

    effective = max(1, len(plan_tokens) - plan_skips)
    return matched / effective, last_idx


def match_vocal_section(
    words: list[dict],
    cursor: int,
    lines: list[str],
) -> dict | None:
    """Match a multi-line section by aligning each lyric line sequentially."""
    vocal_lines = [line for line in lines if not PAREN_ONLY.match(line)]
    if not vocal_lines:
        return None

    token_budget = sum(len(line_tokens(line)) for line in vocal_lines)
    max_section_words = max(token_budget * 3 + 8, 12)

    line_cursor = cursor
    first_start: int | None = None
    last_end: int | None = None
    confidences: list[float] = []

    for line_index, line in enumerate(vocal_lines):
        line_tokens_count = len(line_tokens(line))
        search_window = 80 if line_index == 0 else max(20, line_tokens_count * 4 + 6)
        match = fuzzy_match_line(words, line_cursor, line, search_window=search_window)
        if match is None:
            return None
        start_idx, end_idx, confidence = match
        if first_start is None:
            first_start = start_idx
        elif start_idx - first_start > max_section_words:
            return None
        last_end = end_idx
        line_cursor = end_idx + 1
        confidences.append(confidence)

    assert first_start is not None and last_end is not None
    if last_end - first_start + 1 > max_section_words * 2:
        return None
    return {
        "word_start": words[first_start]["start"],
        "word_end": words[last_end]["end"],
        "confidence": round(min(confidences), 3),
        "matched_text": " ".join(w["word"] for w in words[first_start : last_end + 1]),
        "word_start_index": first_start,
        "word_end_index": last_end,
    }


def fuzzy_match_line(
    words: list[dict],
    cursor: int,
    line: str,
    *,
    search_window: int = 40,
    min_score: float = 0.62,
) -> tuple[int, int, float] | None:
    tokens = line_tokens(line)
    if not tokens:
        return None

    search_end = min(len(words), cursor + search_window)
    best: tuple[float, int, int] | None = None
    max_spoken_words = max(len(tokens) * 2 + 2, 6)

    for start in range(cursor, search_end):
        for plan_offset in range(min(3, len(tokens))):
            anchor = tokens[plan_offset]
            if not spoken_covers_token(anchor, words, start)[0] and not token_fuzzy_match(
                anchor, words[start]["token"], min_ratio=0.5
            ):
                continue

            sub_tokens = tokens[plan_offset:]
            min_end = start + max(1, len(sub_tokens) // 2)
            max_end = min(len(words) - 1, start + max_spoken_words)
            for end in range(min_end, max_end + 1):
                if end - start + 1 > max_spoken_words:
                    break
                score, last_idx = score_token_alignment(sub_tokens, words, start, end)
                if score < min_score:
                    continue
                score_adj = score - 0.002 * (start - cursor) - 0.01 * plan_offset
                if best is None or score_adj > best[0] or (
                    score_adj == best[0] and start < best[1]
                ):
                    best = (score_adj, start, last_idx)

    if best is None:
        return None
    raw_score = min(1.0, best[0] + 0.002 * (best[1] - cursor))
    return best[1], best[2], round(raw_score, 3)


def nearest_word_index(words: list[dict], time_sec: float) -> int:
    return min(range(len(words)), key=lambda i: abs(words[i]["start"] - time_sec))


def is_instrumental_cut(cut: dict) -> bool:
    lines = cut.get("lines") or []
    if not lines:
        return True
    if cut.get("section_tag") in ("Inst", "Solo", "Interlude", "Break", "Transition"):
        return True
    return all(PAREN_ONLY.match(line) for line in lines)


def probe_duration(path: Path) -> float:
    probe = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(probe.stdout.strip())


def word_records(words: list[dict], start_idx: int, end_idx: int) -> list[dict]:
    return [
        {
            "word": words[i]["word"],
            "start_sec": round(words[i]["start"], 3),
            "end_sec": round(words[i]["end"], 3),
            "index": i,
        }
        for i in range(start_idx, end_idx + 1)
    ]


def next_vocal_start(spans: list[dict | None], from_index: int) -> float | None:
    for span in spans[from_index:]:
        if span:
            return span["word_start"]
    return None


def assign_cut_timing(
    entry: dict,
    *,
    start: float,
    end: float,
    span: dict | None,
    words: list[dict],
) -> dict:
    start = round(max(0.0, start), 3)
    end = round(max(start + 0.05, end), 3)
    entry["start_sec"] = start
    entry["end_sec"] = end
    entry["duration_sec"] = round(end - start, 3)

    alignment = dict(entry.get("alignment") or {})
    alignment["method"] = "whisperx"
    if span:
        alignment["audio_slice_start_sec"] = round(span["word_start"], 3)
        alignment["audio_slice_end_sec"] = round(span["word_end"], 3)
    else:
        alignment["audio_slice_start_sec"] = start
        alignment["audio_slice_end_sec"] = end

    if span:
        alignment["confidence"] = span["confidence"]
        alignment["matched_text"] = span["matched_text"]
        alignment["word_start_index"] = span["word_start_index"]
        alignment["word_end_index"] = span["word_end_index"]
        alignment["words"] = word_records(words, span["word_start_index"], span["word_end_index"])
        alignment.pop("status", None)
        alignment.pop("gap_fill", None)
    entry["alignment"] = alignment
    return entry


def align_cuts(
    cuts: list[dict],
    transcript: dict,
    *,
    song_duration: float,
    pad_ms: float = 100.0,
) -> tuple[list[dict], dict]:
    words = flatten_words(transcript)
    if not words:
        raise RuntimeError("WhisperX transcript has no word timestamps")

    pre_pad = max(PRE_PAD_SEC, pad_ms / 1000.0 * 0.25)
    post_pad = max(POST_PAD_SEC, pad_ms / 1000.0)

    cursor = 0
    matched_spans: list[dict | None] = []
    stats = {"matched": 0, "gap_filled": 0, "failed": 0}

    for cut in cuts:
        lines = cut.get("lines") or []
        vocal_lines = [line for line in lines if not PAREN_ONLY.match(line)]
        span: dict | None = None

        if vocal_lines and not is_instrumental_cut(cut):
            if cut.get("cut_rule") == "section" and len(vocal_lines) > 1:
                span = match_vocal_section(words, cursor, lines)
            else:
                line = vocal_lines[0] if len(vocal_lines) == 1 else " ".join(vocal_lines)
                match = fuzzy_match_line(words, cursor, line)
                if match is not None:
                    start_idx, end_idx, confidence = match
                    span = {
                        "word_start": words[start_idx]["start"],
                        "word_end": words[end_idx]["end"],
                        "confidence": confidence,
                        "matched_text": " ".join(w["word"] for w in words[start_idx : end_idx + 1]),
                        "word_start_index": start_idx,
                        "word_end_index": end_idx,
                    }
            if span is not None:
                cursor = span["word_end_index"] + 1
                stats["matched"] += 1
            else:
                stats["failed"] += 1
        matched_spans.append(span)

    timeline = 0.0
    aligned: list[dict] = []

    for index, (cut, span) in enumerate(zip(cuts, matched_spans, strict=True)):
        entry = dict(cut)

        if span:
            word_start = span["word_start"]
            word_end = span["word_end"]

            start = max(timeline, word_start - pre_pad)
            end = min(song_duration, word_end + post_pad)

            next_start = next_vocal_start(matched_spans, index + 1)
            if next_start is not None:
                end = min(end, next_start - 0.02)

            assign_cut_timing(entry, start=start, end=end, span=span, words=words)
            timeline = end
            aligned.append(entry)
            continue

        next_start = next_vocal_start(matched_spans, index + 1)
        start = timeline

        if cut.get("section_tag") == "Intro" and start == 0.0 and next_start is not None:
            if next_start >= MIN_PVIDEO_AUDIO_SEC:
                end = min(song_duration, max(MIN_PVIDEO_AUDIO_SEC, next_start - 0.02))
            else:
                end = min(song_duration, next_start)
                entry["skip_clip"] = True
                entry["skip_reason"] = "intro shorter than p-video minimum; merge into first vocal"
        elif next_start is not None:
            end = min(song_duration, max(start + 0.05, next_start - 0.02))
        else:
            end = song_duration

        assign_cut_timing(entry, start=start, end=end, span=None, words=words)
        entry["alignment"]["status"] = "instrumental" if is_instrumental_cut(entry) else "unmatched"
        entry["alignment"]["gap_fill"] = True
        entry["alignment"]["confidence"] = None
        timeline = end
        stats["gap_filled"] += 1
        aligned.append(entry)

    if aligned:
        aligned[-1]["end_sec"] = round(song_duration, 3)
        aligned[-1]["duration_sec"] = round(song_duration - aligned[-1]["start_sec"], 3)
        aligned[-1]["alignment"]["audio_slice_end_sec"] = aligned[-1]["end_sec"]

    return aligned, stats


def section_id_from_cut(cut_id: str) -> str:
    return cut_id.split("_")[0]


def coalesce_line_cuts_to_sections(
    line_cuts: list[dict],
    section_cuts: list[dict],
) -> list[dict]:
    """Merge aligned line-level timings into section-level cuts (one clip per verse)."""
    grouped: dict[str, list[dict]] = {}
    for cut in line_cuts:
        grouped.setdefault(section_id_from_cut(cut["id"]), []).append(cut)

    merged: list[dict] = []
    for section in section_cuts:
        sid = section["id"]
        parts = grouped.get(sid, [])
        if not parts:
            merged.append(dict(section))
            continue

        entry = dict(section)
        entry["start_sec"] = round(min(float(p["start_sec"]) for p in parts), 3)
        entry["end_sec"] = round(max(float(p["end_sec"]) for p in parts), 3)
        entry["duration_sec"] = round(entry["end_sec"] - entry["start_sec"], 3)

        words: list[dict] = []
        confidences: list[float] = []
        slice_starts: list[float] = []
        slice_ends: list[float] = []
        for part in parts:
            alignment = part.get("alignment") or {}
            words.extend(alignment.get("words") or [])
            if alignment.get("audio_slice_start_sec") is not None:
                slice_starts.append(float(alignment["audio_slice_start_sec"]))
                slice_ends.append(float(alignment["audio_slice_end_sec"]))
            if alignment.get("confidence") is not None:
                confidences.append(float(alignment["confidence"]))

        alignment = {
            "method": "whisperx",
            "audio_slice_start_sec": round(min(slice_starts or [entry["start_sec"]]), 3),
            "audio_slice_end_sec": round(max(slice_ends or [entry["end_sec"]]), 3),
            "words": words,
            "coalesced_from": [part["id"] for part in parts],
        }
        if confidences:
            alignment["confidence"] = round(min(confidences), 3)
        if all(part.get("skip_clip") for part in parts):
            entry["skip_clip"] = True
            entry["skip_reason"] = parts[0].get("skip_reason", "coalesced skip")
        entry["alignment"] = alignment
        merged.append(entry)

    return merged


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cuts", type=Path, required=True, help="cut_manifest.json")
    parser.add_argument("--transcript", type=Path, required=True, help="whisperx_transcript.json")
    parser.add_argument("--song", type=Path, help="Optional song for duration verification")
    parser.add_argument("--out", type=Path, help="Defaults to --cuts (in place)")
    parser.add_argument("--padding-ms", type=float, default=100.0)
    parser.add_argument(
        "--coalesce-sections",
        action="store_true",
        help="Align at line level, then merge timings into section-level cuts from --cuts",
    )
    args = parser.parse_args()

    manifest = json.loads(args.cuts.read_text())
    transcript = json.loads(args.transcript.read_text())
    song_duration = manifest.get("song_duration_sec")
    if args.song:
        song_duration = probe_duration(args.song)
    if not song_duration:
        words = flatten_words(transcript)
        song_duration = words[-1]["end"] if words else 0.0

    section_cuts = manifest["cuts"]
    cuts_to_align = section_cuts
    if args.coalesce_sections:
        from parse_lyric_cuts import build_cut_manifest, parse_lyrics

        lyrics = manifest.get("sections")
        if lyrics:
            sections = lyrics
        else:
            sections = manifest.get("sections")  # wrong key
        # sections in manifest is parsed sections list under key "sections"
        sections = manifest.get("sections") or []
        if not sections:
            raise SystemExit("cut_manifest missing sections[] — re-run --phase cuts")
        cuts_to_align = build_cut_manifest(sections, default_beat="performance", granularity="line")

    aligned, stats = align_cuts(
        cuts_to_align,
        transcript,
        song_duration=song_duration,
        pad_ms=args.padding_ms,
    )

    if args.coalesce_sections:
        aligned = coalesce_line_cuts_to_sections(aligned, section_cuts)
        stats["coalesced_sections"] = len(section_cuts)

    manifest["cuts"] = aligned
    manifest["song_duration_sec"] = round(song_duration, 3)
    manifest["timing_method"] = "whisperx_word_align"
    manifest["alignment_stats"] = stats
    manifest["cut_rules"] = [
        "start_sec/end_sec = padded assembly window; audio_slice_* = tight first→last matched word span",
        "Each vocal cut stores alignment.words[] with per-word start/end",
        "Instrumental gaps fill between word spans; intros shorter than 1.0s are skip_clip",
    ]

    out = args.out or args.cuts
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, indent=2) + "\n")
    print(
        f"Wrote {out} — matched {stats['matched']}, gap-filled {stats['gap_filled']}, "
        f"failed {stats['failed']}",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
