"""Build p-video payloads with audio-led duration (scene anchor triple pattern)."""

from __future__ import annotations

import subprocess
from pathlib import Path

# P-API allows duration 1–20s; audio-led clips cannot exceed this ceiling.
P_VIDEO_MAX_DURATION_SECONDS = 20.0
# Leave headroom for encoder rounding and TTS tail silence.
P_VIDEO_NARRATION_SAFE_MAX_SECONDS = 19.0


def probe_media_duration_seconds(path: Path) -> float:
    result = subprocess.run(
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
    return float(result.stdout.strip())


def validate_narration_duration(
    seconds: float,
    *,
    scene_id: str,
    max_seconds: float = P_VIDEO_NARRATION_SAFE_MAX_SECONDS,
) -> None:
    if seconds <= max_seconds:
        return
    raise SystemExit(
        f"{scene_id}: narration is {seconds:.1f}s but p-video audio-led clips cap at "
        f"{P_VIDEO_MAX_DURATION_SECONDS:.0f}s (keep TTS ≤ {max_seconds:.0f}s). "
        "Shorten the line, split the scene, or pass --skip-narration-check to override."
    )


def build_p_video_payload(
    *,
    prompt: str,
    image_url: str,
    audio_url: str | None = None,
    last_frame_image_url: str | None = None,
    resolution: str = "720p",
    fps: int = 24,
    save_audio: bool = True,
    duration: float | int | None = None,
    **extra: object,
) -> dict:
    """Return a p-video input dict. When audio_url is set, duration is omitted (clip length = audio).

    This matches the dog-plush / scene-anchor-triple pattern: upload narration or a song slice
    to /v1/files, pass as input.audio, set save_audio so the full line plays in the output clip.
    Do not post-mux narration over silent clips — that truncates long TTS lines.
    P-API caps audio-led clips at 20s; probe TTS with validate_narration_duration before render.
    """
    if audio_url and duration is not None:
        raise ValueError("omit duration when audio_url is set — clip length follows audio")

    payload: dict = {
        "prompt": prompt,
        "image": image_url,
        "resolution": resolution,
        "fps": fps,
    }
    if audio_url:
        payload["audio"] = audio_url
        if save_audio:
            payload["save_audio"] = True
    elif duration is not None:
        payload["duration"] = duration

    if last_frame_image_url:
        payload["last_frame_image"] = last_frame_image_url

    payload.update(extra)
    return payload
