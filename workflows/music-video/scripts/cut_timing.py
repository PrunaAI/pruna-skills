"""Shared cut timing helpers — single source of truth from WhisperX word spans."""

from __future__ import annotations

PRE_PAD_SEC = 0.05
POST_PAD_SEC = 0.10
MIN_PVIDEO_AUDIO_SEC = 1.0


def matched_words(alignment: dict) -> list[dict]:
    return list(alignment.get("words") or [])


def assembly_bounds(cut: dict) -> tuple[float, float]:
    """Padded song window for assembly trim / timeline gaps between lines."""
    return float(cut["start_sec"]), float(cut["end_sec"])


def audio_slice_bounds(cut: dict) -> tuple[float, float]:
    """Tight vocal span for slice_audio and model input.audio (first→last matched word)."""
    alignment = cut.get("alignment") or {}
    if alignment.get("audio_slice_start_sec") is not None:
        return float(alignment["audio_slice_start_sec"]), float(alignment["audio_slice_end_sec"])
    return assembly_bounds(cut)


def clip_duration_sec(cut: dict) -> float:
    if cut.get("duration_sec") is not None:
        return float(cut["duration_sec"])
    start, end = assembly_bounds(cut)
    return end - start


def build_clips_meta_entry(cut: dict, *, model: str, host_type: str, prediction_id: str | None, clip: str) -> dict:
    asm_start, asm_end = assembly_bounds(cut)
    slice_start, slice_end = audio_slice_bounds(cut)
    alignment = cut.get("alignment") or {}
    return {
        "model": model,
        "beat_type": cut.get("beat_type"),
        "host_type": host_type,
        "prediction_id": prediction_id,
        "clip": clip,
        "start_sec": round(asm_start, 3),
        "end_sec": round(asm_end, 3),
        "duration_sec": round(asm_end - asm_start, 3),
        "audio_slice_start_sec": round(slice_start, 3),
        "audio_slice_end_sec": round(slice_end, 3),
        "audio_slice_duration_sec": round(slice_end - slice_start, 3),
        "lines": cut.get("lines") or [],
        "matched_text": alignment.get("matched_text"),
        "alignment_confidence": alignment.get("confidence"),
        "words": matched_words(alignment),
    }
