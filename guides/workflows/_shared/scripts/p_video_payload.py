"""Build p-video payloads with audio-led duration (scene anchor triple pattern)."""

from __future__ import annotations


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
