#!/usr/bin/env python3
"""Generate checked-in docs example images and videos.

Requires PRUNA_API_KEY. Workflow examples (TTS, Music 2.5) also need REPLICATE_API_TOKEN.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "assets" / "examples"
API = "https://api.pruna.ai/v1/predictions"
FILES = "https://api.pruna.ai/v1/files"

STORY_SCRIPTS = ROOT / "workflows" / "illustrated-story-reel" / "scripts"
SHARED_SCRIPTS = ROOT / "workflows" / "_shared" / "scripts"
for _p in (STORY_SCRIPTS, SHARED_SCRIPTS):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from assemble_slideshow import concat_clips_with_audio, mux_audio, probe_duration, render_still_segment  # noqa: E402
from replicate_api import (  # noqa: E402
    download_url,
    require_replicate_token,
    run_model_prediction,
    run_version_prediction,
    upload_file as replicate_upload,
)

# P-API max edge is 1440px. Videos: final 1080p @ 24fps.
VIDEO_BASE = {"resolution": "1080p", "fps": 24, "draft": False}
CHAIN_DURATION = 10
CLIP_DURATION = 8
TTS_MODEL = "google/gemini-3.1-flash-tts"
MUSIC_MODEL = "minimax/music-2.5"
STABLE_AUDIO_MODEL = "stability-ai/stable-audio-2.5"
WHISPERX_VERSION = "655845d6190ef70573c669245f245892cd039df4b880a1e3a65852c09252f5cc"


def api_key() -> str:
    key = os.environ.get("PRUNA_API_KEY", "").strip()
    if not key:
        sys.exit("PRUNA_API_KEY is required")
    return key


def image_input(prompt: str, aspect_ratio: str) -> dict:
    sizes = {
        "16:9": (1440, 816),
        "9:16": (816, 1440),
        "1:1": (1440, 1440),
        "4:3": (1440, 1088),
        "3:4": (1088, 1440),
    }
    if aspect_ratio in sizes:
        w, h = sizes[aspect_ratio]
        return {"prompt": prompt, "aspect_ratio": "custom", "width": w, "height": h}
    return {"prompt": prompt, "aspect_ratio": aspect_ratio}


def post_json(url: str, body: dict, headers: dict) -> dict:
    data = json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.load(resp)


def get_json(url: str, headers: dict) -> dict:
    req = urllib.request.Request(url, headers=headers, method="GET")
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.load(resp)


def output_url(payload: dict) -> str:
    out = payload.get("output") or payload.get("generation_url")
    if isinstance(out, list):
        out = out[0]
    if not isinstance(out, str) or not out:
        raise RuntimeError(f"no output url in {payload!r}")
    return out


def predict(model: str, inp: dict, *, sync: bool = True, poll_secs: int = 3, max_polls: int = 120) -> dict:
    headers = {
        "Content-Type": "application/json",
        "apikey": api_key(),
        "Model": model,
    }
    if sync:
        headers["Try-Sync"] = "true"
    payload = post_json(API, {"input": inp}, headers)
    if payload.get("status") == "succeeded":
        return payload
    get_url = payload.get("get_url")
    if not get_url:
        raise RuntimeError(f"unexpected create response: {payload!r}")
    for _ in range(max_polls):
        status = get_json(get_url, {"apikey": api_key()})
        if status.get("status") in ("succeeded", "failed"):
            if status.get("status") == "failed":
                raise RuntimeError(status)
            return status
        time.sleep(poll_secs)
    raise TimeoutError(get_url)


def upload_file(path: Path) -> str:
    boundary = f"----pruna-{int(time.time() * 1000)}"
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="content"; filename="{path.name}"\r\n'
        f"Content-Type: application/octet-stream\r\n\r\n"
    ).encode("utf-8")
    body += path.read_bytes()
    body += f"\r\n--{boundary}--\r\n".encode("utf-8")
    req = urllib.request.Request(FILES, data=body, method="POST")
    req.add_header("apikey", api_key())
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    with urllib.request.urlopen(req, timeout=600) as resp:
        payload = json.load(resp)
    url = payload.get("urls", {}).get("get")
    if not url:
        raise RuntimeError(f"upload failed: {payload!r}")
    return url


def download_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"apikey": api_key()})
    with urllib.request.urlopen(req, timeout=180) as resp:
        return resp.read()


def wipe_outputs(stem: str) -> None:
    """Remove prior video + sidecar for stem only (not sibling files sharing a prefix)."""
    for suffix in (".mp4", ".meta.json"):
        (OUT / f"{stem}{suffix}").unlink(missing_ok=True)


def wipe(prefix: str) -> None:
    for path in OUT.glob(f"{prefix}*"):
        if path.suffix in {".png", ".mp4", ".json", ".mp3", ".srt"}:
            path.unlink()


def skip_if_exists(path: Path, *, missing_only: bool) -> bool:
    if missing_only and path.exists():
        print(f"skip existing {path.name}")
        return True
    return False


def write_sidecar(path: Path, data: dict) -> None:
    meta = path.with_name(f"{path.stem}.meta.json")
    meta.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {meta.name}")


def trim_video(src: Path, seconds: float, out: Path, *, keep_audio: bool = False, force: bool = False) -> Path:
    if out.exists() and not force:
        return out
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(src),
        "-t",
        str(seconds),
        "-c:v",
        "libx264",
        "-preset",
        "fast",
        "-crf",
        "18",
    ]
    if keep_audio:
        cmd.extend(["-c:a", "aac", "-b:a", "192k"])
    else:
        cmd.append("-an")
    cmd.append(str(out))
    subprocess.run(cmd, check=True, capture_output=True)
    print(f"wrote {out.name} ({seconds:.1f}s trim{' + audio' if keep_audio else ''})")
    return out


def run_stable_audio(prompt: str, dest: Path, *, duration: int = 18) -> Path:
    if dest.exists():
        print(f"reusing {dest.name}")
        return dest
    token = require_replicate_token()
    result = run_model_prediction(
        STABLE_AUDIO_MODEL,
        {"prompt": prompt, "duration": duration, "steps": 8, "cfg_scale": 1.0},
        token,
        label="stable-audio-2.5",
        timeout_seconds=600,
    )
    output = result.get("output")
    if not output:
        raise RuntimeError(f"No stable-audio output: {result!r}")
    download_url(str(output), dest)
    print(f"wrote {dest.name}")
    return dest


def save_png(name: str, model: str, prompt: str, inp: dict, payload: dict) -> Path:
    url = output_url(payload)
    png = OUT / f"{name}.png"
    meta = OUT / f"{name}.meta.json"
    raw = download_bytes(url)
    tmp = png.with_suffix(".bin")
    tmp.write_bytes(raw)
    subprocess.run(["sips", "-s", "format", "png", str(tmp), "--out", str(png)], check=True, capture_output=True)
    tmp.unlink(missing_ok=True)
    dims = subprocess.run(
        ["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(png)],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    meta.write_text(
        json.dumps(
            {"model": model, "prompt": prompt, "input": inp, "output_url": url, "dimensions": dims},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"wrote {png.name}")
    return png


def save_mp4(name: str, model: str, prompt: str, inp: dict, payload: dict) -> Path:
    url = output_url(payload)
    mp4 = OUT / f"{name}.mp4"
    meta = OUT / f"{name}.meta.json"
    mp4.write_bytes(download_bytes(url))
    probe = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height,r_frame_rate",
            "-show_entries",
            "format=duration",
            "-of",
            "default=nw=1",
            str(mp4),
        ],
        capture_output=True,
        text=True,
    )
    meta.write_text(
        json.dumps(
            {
                "model": model,
                "prompt": prompt,
                "input": inp,
                "output_url": url,
                "probe": probe.stdout.strip() if probe.returncode == 0 else None,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"wrote {mp4.name} ({mp4.stat().st_size // 1024}K)")
    return mp4


def render_video(name: str, video_prompt: str, start: Path, end: Path | None, *, duration: int) -> Path:
    wipe_outputs(name)
    video_inp = {"prompt": video_prompt, "image": upload_file(start), **VIDEO_BASE, "duration": duration}
    if end is not None:
        video_inp["last_frame_image"] = upload_file(end)
    payload = predict("p-video", video_inp, sync=False, max_polls=300, poll_secs=4)
    meta_inp = dict(video_inp)
    meta_inp["image"] = start.name
    if end is not None:
        meta_inp["last_frame_image"] = end.name
    return save_mp4(name, "p-video", video_prompt, meta_inp, payload)


def render_avatar_video(name: str, video_prompt: str, image: Path, audio: Path) -> Path:
    wipe_outputs(name)
    video_inp = {
        "image": upload_file(image),
        "audio": upload_file(audio),
        "video_prompt": video_prompt,
        "resolution": "1080p",
    }
    payload = predict("p-video-avatar", video_inp, sync=False, max_polls=300, poll_secs=4)
    meta_inp = {"image": image.name, "audio": audio.name, "video_prompt": video_prompt, "resolution": "1080p"}
    return save_mp4(name, "p-video-avatar", video_prompt, meta_inp, payload)


def run_replicate_tts(text: str, dest: Path, *, style_prompt: str, voice: str = "Kore") -> Path:
    if dest.exists():
        print(f"reusing {dest.name}")
        return dest
    token = require_replicate_token()
    result = run_model_prediction(
        TTS_MODEL,
        {"text": text, "voice": voice, "prompt": style_prompt, "language_code": "en-US"},
        token,
        label="gemini-tts",
        timeout_seconds=600,
    )
    output = result.get("output")
    if not output:
        raise RuntimeError(f"No TTS output: {result!r}")
    download_url(str(output), dest)
    print(f"wrote {dest.name}")
    return dest


def run_music_25(lyrics: str, style_prompt: str, dest: Path) -> Path:
    if dest.exists():
        print(f"reusing {dest.name}")
        return dest
    token = require_replicate_token()
    result = run_model_prediction(
        MUSIC_MODEL,
        {"lyrics": lyrics, "prompt": style_prompt, "sample_rate": 44100, "bitrate": 256000, "audio_format": "mp3"},
        token,
        label="music-2.5",
        timeout_seconds=900,
    )
    output = result.get("output")
    if not output:
        raise RuntimeError(f"No music output: {result!r}")
    download_url(str(output), dest)
    print(f"wrote {dest.name}")
    return dest


def slice_audio(song: Path, start: float, end: float, out: Path) -> Path:
    if end <= start:
        raise ValueError("slice end must be after start")
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(song),
            "-ss",
            str(start),
            "-t",
            str(end - start),
            "-vn",
            "-acodec",
            "libmp3lame",
            "-q:a",
            "2",
            "-avoid_negative_ts",
            "make_zero",
            str(out),
        ],
        check=True,
        capture_output=True,
    )
    print(f"wrote {out.name} ({end - start:.1f}s)")
    return out


def render_narrated_pvideo(out_stem: str, video_prompt: str, image: Path, audio: Path) -> Path:
    wipe(out_stem)
    dur = probe_duration(audio)
    if dur > 19.0:
        sys.exit(f"narration too long for audio-led p-video ({dur:.1f}s > 19s)")
    video_inp = {
        "prompt": video_prompt,
        "image": upload_file(image),
        "audio": upload_file(audio),
        "save_audio": True,
        **VIDEO_BASE,
    }
    payload = predict("p-video", video_inp, sync=False, max_polls=300, poll_secs=4)
    meta_inp = {
        "prompt": video_prompt,
        "image": image.name,
        "audio": audio.name,
        "save_audio": True,
        **VIDEO_BASE,
    }
    reel = save_mp4(out_stem, "p-video", video_prompt, meta_inp, payload)
    meta = OUT / f"{out_stem}.meta.json"
    base = json.loads(meta.read_text(encoding="utf-8"))
    base.update(
        {
            "workflow": "illustrated-story-reel",
            "motion_mode": "p-video",
            "models": [TTS_MODEL, "p-video"],
            "narration_text": WHALE_NARRATION,
            "tts_style_prompt": WHALE_TTS_PROMPT,
            "still": image.name,
            "narration": audio.name,
            "video_prompt": video_prompt,
        }
    )
    meta.write_text(json.dumps(base, indent=2) + "\n", encoding="utf-8")
    return reel


def assemble_ken_burns_reel(still: Path, narration: Path, out: Path, *, ken_burns: str = "pan_right") -> Path:
    wipe(out.stem)
    pad = 0.35
    duration = probe_duration(narration) + pad
    silent = OUT / f"{out.stem}-silent.mp4"
    render_still_segment(still, duration, ken_burns=ken_burns, width=1920, height=1080, fps=24, out=silent)
    mux_audio(silent, narration, out, pad_tail_sec=pad)
    silent.unlink(missing_ok=True)
    meta = OUT / f"{out.stem}.meta.json"
    meta.write_text(
        json.dumps(
            {
                "workflow": "illustrated-story-reel",
                "models": [TTS_MODEL, "ffmpeg-ken-burns"],
                "narration_text": WHALE_NARRATION,
                "tts_style_prompt": WHALE_TTS_PROMPT,
                "still": still.name,
                "narration": narration.name,
                "ken_burns": ken_burns,
                "duration_sec": round(duration, 2),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"wrote {out.name} ({out.stat().st_size // 1024}K)")
    return out


def image_chain(
    prefix: str,
    open_prompt: str,
    end_prompt: str,
    video_prompt: str,
    *,
    aspect_ratio: str = "16:9",
    open_path: Path | None = None,
    duration: int = CHAIN_DURATION,
) -> tuple[Path, Path, Path]:
    wipe(prefix)
    if open_path is None:
        open_inp = image_input(open_prompt, aspect_ratio)
        open_path = save_png(f"{prefix}-01-open", "p-image", open_prompt, open_inp, predict("p-image", open_inp))
    else:
        link = OUT / f"{prefix}-01-open.png"
        link.write_bytes(open_path.read_bytes())
        open_path = link
        print(f"linked {open_path.name}")

    file_url = upload_file(open_path)
    end_inp = {"prompt": end_prompt, "images": [file_url], "aspect_ratio": aspect_ratio, "turbo": False}
    end_path = save_png(
        f"{prefix}-02-end",
        "p-image-edit",
        end_prompt,
        {**end_inp, "images": ["<open upload>"]},
        predict("p-image-edit", end_inp),
    )
    clip = render_video(f"{prefix}-clip", video_prompt, open_path, end_path, duration=duration)
    return open_path, end_path, clip


def image_to_video(
    prefix: str,
    image_prompt: str,
    video_prompt: str,
    *,
    aspect_ratio: str = "16:9",
    duration: int = CLIP_DURATION,
    regen_video_only: bool = False,
) -> tuple[Path, Path]:
    if regen_video_only:
        still = OUT / f"{prefix}-still.png"
        if not still.exists():
            sys.exit(f"missing {still} for video-only regen")
    else:
        wipe(prefix)
        inp = image_input(image_prompt, aspect_ratio)
        still = save_png(f"{prefix}-still", "p-image", image_prompt, inp, predict("p-image", inp))
    clip = render_video(f"{prefix}-clip", video_prompt, still, None, duration=duration)
    return still, clip


def save_image(name: str, prompt: str, aspect_ratio: str) -> Path:
    wipe(name)
    inp = image_input(prompt, aspect_ratio)
    return save_png(name, "p-image", prompt, inp, predict("p-image", inp))


def gen_quickstart_panda(*, video_only: bool = False) -> None:
    panda_open = (
        "9:16 whimsical photoreal portrait, fluffy red panda in a tiny apron pulling latte art "
        "in a sunlit Kyoto café, steam curls, ceramic cups, warm wood interior, mouth not "
        "obscured, charming and detailed, no text"
    )
    end_prompt = (
        "Same red panda barista character and face, inside a Mars habitat room with a large "
        "panoramic window showing red desert outside, small Earth visible in the sky, olive "
        "flight suit with helmet off, keep fur colors and facial features identical, cinematic "
        "sci-fi interior lighting, not inside a glass jar, no text"
    )
    video_prompt = (
        "OPEN: locked eye-level camera, gentle steam rise, two second hold. "
        "MID: same red panda stays centered and same scale, extremely smooth slow dissolve — café walls and "
        "tables fade gradually into deep starfield over six seconds, no hard cuts, no pops, no morphing away the subject. "
        "CLOSE: ease gently into Mars habitat by the window, same panda in flight suit, subtle dust outside, calm settle."
    )
    if video_only:
        open_path = OUT / "quickstart-panda-01-open.png"
        end_path = OUT / "quickstart-panda-02-end.png"
        if not open_path.exists() or not end_path.exists():
            sys.exit("missing quickstart panda stills for video-only regen")
        render_video("quickstart-panda-clip", video_prompt, open_path, end_path, duration=CHAIN_DURATION)
        return

    panda_path = save_image("quickstart-panda-01-open", panda_open, "9:16")
    image_chain(
        "quickstart-panda",
        open_prompt=panda_open,
        open_path=panda_path,
        end_prompt=end_prompt,
        video_prompt=video_prompt,
        aspect_ratio="9:16",
        duration=CHAIN_DURATION,
    )


def gen_chain_monarch(*, video_only: bool = False) -> None:
    style = "soft purple garden bokeh, morning dew, photoreal cinematic 16:9"
    open_prompt = (
        "16:9 macro still, monarch butterfly perched on lavender stem, wings closed upright "
        f"showing orange edge only, dew drops, {style}, no text"
    )
    end_prompt = (
        "Same butterfly same lavender same camera. Wings open wide displaying full orange and "
        f"black pattern, same dew and bokeh, keep composition identical, {style}, no text"
    )
    video_prompt = (
        "Monarch butterfly on lavender, static camera, morning garden, two second hold. "
        "Subtle elegant motion: wings open slowly then one soft flutter, controlled minimal "
        "motion, nature documentary style, no camera move."
    )
    if video_only:
        open_path = OUT / "chain-monarch-01-open.png"
        end_path = OUT / "chain-monarch-02-end.png"
        if not open_path.exists() or not end_path.exists():
            sys.exit("missing monarch stills for video-only regen")
        render_video("chain-monarch-clip", video_prompt, open_path, end_path, duration=CHAIN_DURATION)
        return

    image_chain(
        "chain-monarch",
        open_prompt,
        end_prompt,
        video_prompt,
        aspect_ratio="16:9",
        duration=CHAIN_DURATION,
    )


DRUMMER_IMAGE = (
    "9:16 documentary portrait, exactly one teenage girl drummer, solo subject only, no other people, "
    "centered in frame sitting at drum kit, mid-strike on snare drum, cluttered garage rehearsal space, "
    "afternoon sun through dusty window behind her, natural skin pores, mouth clearly visible and "
    "unobstructed, photoreal, shallow depth of field, no band logos or text"
)

WHALE_IMAGE = (
    "4:3 paper-cut illustration panel, blue whale swimming between towering library shelves, "
    "books flutter like fish, warm amber reading lamps, whimsical collage texture, no caption"
)
WHALE_NARRATION = (
    "[warmly] In a paper-cut library deep below the city, a blue whale swims between the shelves — "
    "chasing stories printed on fluttering pages."
)
WHALE_TTS_PROMPT = "Warm storybook narrator, gentle pace, whimsical and curious, no announcer voice."
WHALE_VIDEO = (
    "OPEN: hold on paper-cut blue whale between library shelves, warm amber lamp glow. "
    "MID: whale drifts slowly forward; a few books flutter past like fish; motion matches narrator energy. "
    "CLOSE: settle in the aisle, collage texture stable, gentle drift only."
)

DRUMMER_LYRICS = """[Intro]
(Soft room tone, sticks counting in)

[Verse]
Garage light cutting through the dust
Stick on snare — that's the only trust
Every afternoon the kit stays loud
Drummer girl above the neighborhood

[Pre Chorus]
Feel the pulse before the drop

[Chorus]
Play it loud in the afternoon sun
Drummer girl — until the set's done
Hit the snare and let the chorus run

[Outro]
(Fading kit ring)
"""
DRUMMER_MUSIC_PROMPT = (
    "Indie garage rock, teenage female vocal, energetic drums-forward, 128 BPM, "
    "gritty rehearsal room energy, live kit, raw and upbeat"
)
DRUMMER_AVATAR_PROMPT = (
    "Sings along to the vocal track, mouth opening and closing in sync with every syllable, "
    "energetic performance, clear visible lip movement. "
    "Static documentary camera on teenage girl at drum kit, afternoon garage light."
)
DRUMMER_PERFORMANCE_VOCAL = (
    "[energetic] Play it loud in the afternoon sun.\n"
    "Drummer girl — until the set's done.\n"
    "Hit the snare and let the chorus run."
)
DRUMMER_VOCAL_TTS_PROMPT = (
    "Teenage female garage-rock singer, rhythmic and upbeat delivery, "
    "clear consonants for lip sync, live rehearsal room energy."
)
SONG_SLICE_START = 22.0
SONG_SLICE_LEN = 12.0


def ensure_performance_audio(song: Path, vocal: Path) -> tuple[Path, str]:
    """Return (audio_for_avatar, source_label). Prefer music-2.5 song slice; fall back to TTS vocal."""
    try:
        run_music_25(DRUMMER_LYRICS, DRUMMER_MUSIC_PROMPT, song)
    except RuntimeError as exc:
        print(f"music-2.5 failed ({exc}); falling back to Gemini TTS performance vocal")
        run_replicate_tts(DRUMMER_PERFORMANCE_VOCAL, vocal, style_prompt=DRUMMER_VOCAL_TTS_PROMPT, voice="Aoede")
        return vocal, TTS_MODEL
    song_dur = probe_duration(song)
    start = min(SONG_SLICE_START, max(0.0, song_dur - SONG_SLICE_LEN - 1.0))
    end = min(start + SONG_SLICE_LEN, song_dur)
    slice_path = OUT / "music-video-garage-drummer-audio-slice.mp3"
    slice_audio(song, start, end, slice_path)
    return slice_path, MUSIC_MODEL


def _remove_legacy(path: Path) -> None:
    if path.exists():
        path.unlink()


def gen_music_video_drummer(*, video_only: bool = False) -> None:
    still = OUT / "music-video-garage-drummer.png"
    song = OUT / "music-video-garage-drummer-song.mp3"
    vocal = OUT / "music-video-garage-drummer-performance-vocal.mp3"
    if video_only:
        if not still.exists():
            sys.exit(f"missing {still} for video-only regen")
    else:
        save_image("music-video-garage-drummer", DRUMMER_IMAGE, "9:16")
    audio_path, audio_source = ensure_performance_audio(song, vocal)
    render_avatar_video("music-video-garage-drummer-clip", DRUMMER_AVATAR_PROMPT, still, audio_path)
    meta = OUT / "music-video-garage-drummer-clip.meta.json"
    base = json.loads(meta.read_text(encoding="utf-8"))
    base["workflow"] = "music-video"
    base["audio_source"] = audio_source
    base["models"] = [audio_source, "p-video-avatar"]
    base["lyrics"] = DRUMMER_LYRICS
    base["music_prompt"] = DRUMMER_MUSIC_PROMPT
    base["performance_vocal_text"] = DRUMMER_PERFORMANCE_VOCAL
    base["audio"] = audio_path.name
    if audio_source == MUSIC_MODEL:
        base["song"] = song.name
        base["audio_slice_start_sec"] = round(
            min(SONG_SLICE_START, max(0.0, probe_duration(song) - SONG_SLICE_LEN - 1.0)), 2
        )
    meta.write_text(json.dumps(base, indent=2) + "\n", encoding="utf-8")


def gen_illustrated_library_whale(*, video_only: bool = False, assemble_only: bool = False) -> None:
    still = OUT / "illustrated-library-whale.png"
    narration = OUT / "illustrated-library-whale-narration.mp3"
    reel = OUT / "illustrated-library-whale-reel.mp4"
    _remove_legacy(OUT / "illustrated-library-whale-clip.mp4")
    _remove_legacy(OUT / "illustrated-library-whale-clip.meta.json")
    if assemble_only:
        if not still.exists() or not narration.exists():
            sys.exit("missing still or narration for assemble-only")
        render_narrated_pvideo("illustrated-library-whale-reel", WHALE_VIDEO, still, narration)
        return
    if video_only:
        if not still.exists() or not narration.exists():
            sys.exit(f"missing {still.name} or {narration.name} for video-only regen")
    else:
        save_image("illustrated-library-whale", WHALE_IMAGE, "4:3")
        run_replicate_tts(WHALE_NARRATION, narration, style_prompt=WHALE_TTS_PROMPT)
    render_narrated_pvideo("illustrated-library-whale-reel", WHALE_VIDEO, still, narration)


AVATAR_MS_COUNT_IN = "[friendly] One, two, three, four — let's run it."
AVATAR_MS_SCENE2_PROMPT = (
    "Counts in on sticks before the take, clear lip movement on every syllable, "
    "static documentary camera, garage afternoon light."
)
AVATAR_MS_COUNT_TTS = "Friendly teenage drummer, crisp count-in delivery, clear consonants for lip sync."

GARMENT_FLATLAY_PROMPT = (
    "Flat lay product photo, vintage red garage band tour jacket with embroidered patches on "
    "clean white background, no person, no text"
)
REPLACE_JACKET_INSTRUCTION = (
    "Replace the plain top the teenage girl drummer is wearing with the vintage red garage "
    "band tour jacket from the reference image. Preserve her face, hair, drumming performance, "
    "garage background, drum kit, camera angle, lighting, and audio. "
    "Only the jacket she is wearing should change; everything else stays as the source."
)
WHALE_BED_PROMPT = (
    "Soft whimsical storybook underscore, gentle piano and harp, paper-cut library mood, "
    "no vocals, 72 BPM"
)
MONARCH_NARRATION = (
    "[calm] On lavender, the monarch rests — wings folded tight, waiting for the morning sun."
)
MONARCH_NARRATION_STYLE = "Calm nature documentary narrator, unhurried pace, warm tone."
MONARCH_NMS_VIDEO = (
    "OPEN: hold on monarch with wings closed on lavender stem, dew drops, static camera. "
    "MID: wings open slowly to full span; motion matches narrator calm energy. "
    "CLOSE: settle with wings open wide, same composition."
)
NMS_SCENE2_NARRATION = (
    "[wonder] By night, the aurora unfurls above the frozen lake — green curtains rippling in silence."
)
NMS_SCENE2_NARRATION_STYLE = "Calm documentary narrator, quiet awe, unhurried pace."
AURORA_END_PROMPT = (
    "Same 16:9 frozen lake aurora vista, aurora curtains ripple higher and brighter toward zenith, "
    "soft snow flurries drift, ice fishing huts glow warmer, identical composition, no text"
)
NMS_SCENE2_VIDEO = (
    "OPEN: hold wide on aurora over frozen lake, huts glowing, static camera. "
    "MID: aurora curtains ripple upward; snow flurries drift; motion matches narrator wonder. "
    "CLOSE: settle as aurora intensifies gently toward zenith."
)


def ensure_sidecars(*, missing_only: bool = True) -> None:
    """Write .meta.json for reused audio without re-calling APIs."""
    song = OUT / "music-video-garage-drummer-song.mp3"
    if song.exists():
        meta = OUT / "music-video-garage-drummer-song.meta.json"
        if not (missing_only and meta.exists()):
            write_sidecar(
                song,
                {
                    "model": MUSIC_MODEL,
                    "tool": "music-2.5",
                    "prompt": DRUMMER_MUSIC_PROMPT,
                    "lyrics": DRUMMER_LYRICS,
                    "reused_by": ["music-video", "music-2.5", "whisperx"],
                },
            )
    narration = OUT / "illustrated-library-whale-narration.mp3"
    if narration.exists():
        meta = OUT / "illustrated-library-whale-narration.meta.json"
        if not (missing_only and meta.exists()):
            write_sidecar(
                narration,
                {
                    "model": TTS_MODEL,
                    "tool": "gemini-3.1-flash-tts",
                    "text": WHALE_NARRATION,
                    "style_prompt": WHALE_TTS_PROMPT,
                    "voice": "Kore",
                    "reused_by": ["illustrated-story-reel", "gemini-3.1-flash-tts"],
                },
            )


def gen_p_image_upscale_hummingbird(*, missing_only: bool = False) -> None:
    out = OUT / "p-image-upscale-hummingbird.png"
    if skip_if_exists(out, missing_only=missing_only):
        return
    src = OUT / "p-image-brass-hummingbird.png"
    if not src.exists():
        save_image(
            "p-image-brass-hummingbird",
            (
                "1:1 macro product photo, clockwork brass hummingbird frozen mid-flap inside a glass "
                "terrarium, tiny gears visible, dew on glass, moody forest bokeh background, museum "
                "exhibit lighting, no text"
            ),
            "1:1",
        )
        src = OUT / "p-image-brass-hummingbird.png"
    wipe("p-image-upscale-hummingbird")
    inp = {
        "image": upload_file(src),
        "target": 8,
        "enhance_details": True,
        "output_format": "png",
    }
    meta_inp = {**inp, "image": src.name}
    save_png(
        "p-image-upscale-hummingbird",
        "p-image-upscale",
        "Upscale brass hummingbird for print delivery",
        meta_inp,
        predict("p-image-upscale", inp, sync=False, max_polls=120, poll_secs=4),
    )


def gen_p_image_try_on_drummer(*, missing_only: bool = False) -> None:
    out = OUT / "p-image-try-on-drummer.png"
    if skip_if_exists(out, missing_only=missing_only):
        return
    person = OUT / "music-video-garage-drummer.png"
    if not person.exists():
        save_image("music-video-garage-drummer", DRUMMER_IMAGE, "9:16")
    garment = OUT / "p-image-try-on-garage-jacket.png"
    if not garment.exists():
        save_image("p-image-try-on-garage-jacket", GARMENT_FLATLAY_PROMPT, "1:1")
    wipe("p-image-try-on-drummer")
    inp = {
        "person_image": upload_file(person),
        "garment_images": [upload_file(garment)],
    }
    meta_inp = {"person_image": person.name, "garment_images": [garment.name]}
    save_png(
        "p-image-try-on-drummer",
        "p-image-try-on",
        "Virtual try-on: garage band jacket on drummer portrait",
        meta_inp,
        predict("p-image-try-on", inp),
    )


def _remove_stale(prefixes: tuple[str, ...]) -> None:
    for prefix in prefixes:
        for path in OUT.glob(f"{prefix}*"):
            path.unlink(missing_ok=True)


def gen_p_video_animate_monarch(*, missing_only: bool = False) -> None:
    out = OUT / "p-video-animate-monarch.mp4"
    if skip_if_exists(out, missing_only=missing_only):
        return
    image = OUT / "chain-monarch-01-open.png"
    motion_src = OUT / "chain-monarch-clip.mp4"
    if not image.exists() or not motion_src.exists():
        sys.exit("need chain-monarch still + clip for p-video-animate")
    _remove_stale(("p-video-animate-hummingbird", "p-video-animate-motion-template"))
    motion = trim_video(motion_src, 5.0, OUT / "chain-monarch-animate-template.mp4")
    for p in (out, OUT / "p-video-animate-monarch.meta.json"):
        p.unlink(missing_ok=True)
    # Same subject + framing as template; motion already describes wing opening — leave instruction blank.
    video_inp = {
        "image": upload_file(image),
        "video": upload_file(motion),
        "resolution": "720p",
        "save_audio": False,
    }
    payload = predict("p-video-animate", video_inp, sync=False, max_polls=300, poll_secs=4)
    meta_inp = {**video_inp, "image": image.name, "video": motion.name}
    save_mp4(
        "p-video-animate-monarch",
        "p-video-animate",
        "Monarch (wings closed still) follows wing-open motion from chain-monarch clip",
        meta_inp,
        payload,
    )


def gen_p_video_replace_jacket(*, missing_only: bool = False) -> None:
    out = OUT / "p-video-replace-jacket.mp4"
    if skip_if_exists(out, missing_only=missing_only):
        return
    source = OUT / "music-video-garage-drummer-clip.mp4"
    garment = OUT / "p-image-try-on-garage-jacket.png"
    if not source.exists():
        sys.exit("need music-video-garage-drummer-clip.mp4 for p-video-replace")
    if not garment.exists():
        save_image("p-image-try-on-garage-jacket", GARMENT_FLATLAY_PROMPT, "1:1")
    _remove_stale(("p-video-replace-drummer", "replace-drummer-ref"))
    trimmed = trim_video(
        source,
        6.0,
        OUT / "p-video-replace-source.mp4",
        keep_audio=True,
        force=True,
    )
    instruction = REPLACE_JACKET_INSTRUCTION
    for p in (out, OUT / "p-video-replace-jacket.meta.json"):
        p.unlink(missing_ok=True)
    video_inp = {
        "video": upload_file(trimmed),
        "images": [upload_file(garment)],
        "instruction_prompt": instruction,
        "resolution": "720p",
        "save_audio": True,
    }
    payload = predict("p-video-replace", video_inp, sync=False, max_polls=300, poll_secs=4)
    meta_inp = {**video_inp, "video": trimmed.name, "images": [garment.name]}
    save_mp4("p-video-replace-jacket", "p-video-replace", instruction, meta_inp, payload)


def gen_stable_audio_library_bed(*, missing_only: bool = False) -> None:
    out = OUT / "stable-audio-library-bed.mp3"
    if skip_if_exists(out, missing_only=missing_only):
        return
    fallback = False
    try:
        run_stable_audio(WHALE_BED_PROMPT, out, duration=18)
    except RuntimeError as exc:
        print(f"stable-audio-2.5 failed ({exc}); using instrumental intro from drummer song")
        song = OUT / "music-video-garage-drummer-song.mp3"
        if not song.exists():
            raise
        end = min(18.0, probe_duration(song))
        slice_audio(song, 0.0, end, out)
        fallback = True
    write_sidecar(
        out,
        {
            "model": STABLE_AUDIO_MODEL,
            "tool": "stable-audio-2.5",
            "prompt": WHALE_BED_PROMPT,
            "duration": 18,
            "reused_by": ["illustrated-story-reel", "stable-audio-2.5"],
            **({"doc_fallback": "instrumental slice from music-2.5 song — re-run stable-audio when available"} if fallback else {}),
        },
    )


def gen_whisperx_drummer_song(*, missing_only: bool = False) -> None:
    out = OUT / "whisperx-drummer-song.json"
    if skip_if_exists(out, missing_only=missing_only):
        return
    song = OUT / "music-video-garage-drummer-song.mp3"
    if not song.exists():
        sys.exit(f"need {song.name} for whisperx example")
    token = require_replicate_token()
    audio_url = replicate_upload(song, token)
    payload = {
        "audio_file": audio_url,
        "language": "en",
        "align_output": True,
        "diarization": False,
        "initial_prompt": "Play it loud in the afternoon sun, drummer girl",
    }
    result = run_version_prediction(
        WHISPERX_VERSION,
        payload,
        token,
        label="whisperx",
        timeout_seconds=900,
    )
    output = result.get("output")
    if not output:
        raise RuntimeError(f"No whisperx output: {result!r}")
    out.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    write_sidecar(
        out,
        {
            "model": "victor-upmeet/whisperx",
            "tool": "whisperx",
            "source_audio": song.name,
            "initial_prompt": payload["initial_prompt"],
            "segment_count": len(output.get("segments") or []),
            "reused_by": ["music-video", "whisperx"],
        },
    )
    print(f"wrote {out.name}")


def render_nms_scene_clip(
    stem: str,
    *,
    open_still: Path,
    end_still: Path,
    narration: Path,
    video_prompt: str,
) -> Path:
    dur = probe_duration(narration)
    if dur > 19.0:
        sys.exit(f"{stem} narration too long for p-video ({dur:.1f}s > 19s)")
    for p in (OUT / f"{stem}.mp4", OUT / f"{stem}.meta.json"):
        p.unlink(missing_ok=True)
    video_inp = {
        "prompt": video_prompt,
        "image": upload_file(open_still),
        "last_frame_image": upload_file(end_still),
        "audio": upload_file(narration),
        "save_audio": True,
        **VIDEO_BASE,
    }
    payload = predict("p-video", video_inp, sync=False, max_polls=300, poll_secs=4)
    meta_inp = {
        **video_inp,
        "image": open_still.name,
        "last_frame_image": end_still.name,
        "audio": narration.name,
    }
    save_mp4(stem, "p-video", video_prompt, meta_inp, payload)
    return OUT / f"{stem}.mp4"


def gen_narrated_multi_scene_demo(*, missing_only: bool = False) -> None:
    final = OUT / "narrated-multi-scene-demo.mp4"
    if skip_if_exists(final, missing_only=missing_only):
        return

    open_monarch = OUT / "chain-monarch-01-open.png"
    end_monarch = OUT / "chain-monarch-02-end.png"
    aurora_start = OUT / "image-to-video-aurora-still.png"
    if not open_monarch.exists() or not end_monarch.exists():
        sys.exit("need chain-monarch stills for narrated-multi-scene scene 1")
    if not aurora_start.exists():
        sys.exit("need image-to-video-aurora-still.png for narrated-multi-scene scene 2")

    _remove_stale(("narrated-multi-scene-monarch",))

    narration1 = OUT / "narrated-multi-scene-01-monarch-narration.mp3"
    run_replicate_tts(MONARCH_NARRATION, narration1, style_prompt=MONARCH_NARRATION_STYLE)
    scene1 = OUT / "narrated-multi-scene-01-monarch.mp4"
    if not (missing_only and scene1.exists()):
        render_nms_scene_clip(
            "narrated-multi-scene-01-monarch",
            open_still=open_monarch,
            end_still=end_monarch,
            narration=narration1,
            video_prompt=MONARCH_NMS_VIDEO,
        )

    aurora_end = OUT / "narrated-multi-scene-02-aurora-end.png"
    if not aurora_end.exists():
        file_url = upload_file(aurora_start)
        end_inp = {
            "prompt": AURORA_END_PROMPT,
            "images": [file_url],
            "aspect_ratio": "16:9",
            "turbo": False,
        }
        save_png(
            "narrated-multi-scene-02-aurora-end",
            "p-image-edit",
            AURORA_END_PROMPT,
            {**end_inp, "images": [aurora_start.name]},
            predict("p-image-edit", end_inp),
        )

    narration2 = OUT / "narrated-multi-scene-02-aurora-narration.mp3"
    run_replicate_tts(NMS_SCENE2_NARRATION, narration2, style_prompt=NMS_SCENE2_NARRATION_STYLE)
    scene2 = OUT / "narrated-multi-scene-02-aurora.mp4"
    if not (missing_only and scene2.exists()):
        render_nms_scene_clip(
            "narrated-multi-scene-02-aurora",
            open_still=aurora_start,
            end_still=aurora_end,
            narration=narration2,
            video_prompt=NMS_SCENE2_VIDEO,
        )

    final.unlink(missing_ok=True)
    concat_clips_with_audio([scene1, scene2], final)
    write_sidecar(
        final,
        {
            "workflow": "narrated-multi-scene",
            "scene_count": 2,
            "models": [TTS_MODEL, "p-image-edit", "p-video"],
            "assembly": "ffmpeg concat demuxer (hard cut; narration embedded per clip)",
            "output": final.name,
            "scenes": [
                {
                    "id": "01_monarch",
                    "clip": scene1.name,
                    "image": open_monarch.name,
                    "last_frame_image": end_monarch.name,
                    "narration": narration1.name,
                    "narration_text": MONARCH_NARRATION,
                    "video_prompt": MONARCH_NMS_VIDEO,
                    "chain_from_previous": False,
                },
                {
                    "id": "02_aurora",
                    "clip": scene2.name,
                    "image": aurora_start.name,
                    "last_frame_image": aurora_end.name,
                    "narration": narration2.name,
                    "narration_text": NMS_SCENE2_NARRATION,
                    "video_prompt": NMS_SCENE2_VIDEO,
                    "chain_from_previous": False,
                },
            ],
        },
    )
    print(f"wrote {final.name} ({final.stat().st_size // 1024}K, 2 scenes)")


def gen_avatar_single_scene_drummer(*, missing_only: bool = False) -> None:
    """Alias drummer clip meta for avatar-single-scene (same asset as music-video beat)."""
    src = OUT / "music-video-garage-drummer-clip.mp4"
    if not src.exists():
        return
    meta = OUT / "avatar-single-scene-drummer.meta.json"
    if missing_only and meta.exists():
        return
    clip_meta = OUT / "music-video-garage-drummer-clip.meta.json"
    base = json.loads(clip_meta.read_text(encoding="utf-8")) if clip_meta.exists() else {}
    base.update(
        {
            "workflow": "avatar-single-scene",
            "video": src.name,
            "note": "Reuses music-video-garage-drummer-clip.mp4 — one talking-head performance beat.",
        }
    )
    meta.write_text(json.dumps(base, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {meta.name}")


def gen_avatar_multi_scene_demo(*, missing_only: bool = False) -> None:
    """Two avatar beats, same hero still — count-in then chorus performance."""
    scene1 = OUT / "music-video-garage-drummer-clip.mp4"
    scene2 = OUT / "avatar-multi-scene-02-count-in.mp4"
    meta_path = OUT / "avatar-multi-scene-demo.meta.json"
    if missing_only and scene2.exists() and meta_path.exists():
        return
    still = OUT / "music-video-garage-drummer.png"
    if not still.exists() or not scene1.exists():
        sys.exit("need drummer still + clip for avatar-multi-scene demo")
    vocal = OUT / "avatar-multi-scene-02-count-in-vocal.mp3"
    run_replicate_tts(
        AVATAR_MS_COUNT_IN,
        vocal,
        style_prompt=AVATAR_MS_COUNT_TTS,
        voice="Aoede",
    )
    wipe_outputs("avatar-multi-scene-02-count-in")
    render_avatar_video("avatar-multi-scene-02-count-in", AVATAR_MS_SCENE2_PROMPT, still, vocal)
    meta_path.write_text(
        json.dumps(
            {
                "workflow": "avatar-multi-scene",
                "scene_count": 2,
                "hero_still": still.name,
                "note": "Same approved portrait URL on both beats — lock plate before batch avatar.",
                "scenes": [
                    {
                        "id": "01_chorus",
                        "clip": scene1.name,
                        "audio": "music-video-garage-drummer-audio-slice.mp3",
                        "model": "p-video-avatar",
                        "beat": "Sings chorus to song slice",
                    },
                    {
                        "id": "02_count_in",
                        "clip": scene2.name,
                        "audio": vocal.name,
                        "model": "p-video-avatar",
                        "beat": "Count-in before the take",
                    },
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"wrote {meta_path.name}")


def gen_missing_tools(*, missing_only: bool = True) -> None:
    ensure_sidecars(missing_only=missing_only)
    gen_p_image_upscale_hummingbird(missing_only=missing_only)
    gen_p_image_try_on_drummer(missing_only=missing_only)
    gen_p_video_animate_monarch(missing_only=missing_only)
    gen_p_video_replace_jacket(missing_only=missing_only)
    gen_stable_audio_library_bed(missing_only=missing_only)
    gen_whisperx_drummer_song(missing_only=missing_only)
    gen_narrated_multi_scene_demo(missing_only=missing_only)
    gen_avatar_single_scene_drummer(missing_only=missing_only)
    gen_avatar_multi_scene_demo(missing_only=missing_only)


def gen_all() -> None:
    for path in OUT.iterdir():
        if path.suffix in {".png", ".mp4", ".json"}:
            path.unlink()

    gen_quickstart_panda()
    save_image(
        "p-image-brass-hummingbird",
        (
            "1:1 macro product photo, clockwork brass hummingbird frozen mid-flap inside a glass "
            "terrarium, tiny gears visible, dew on glass, moody forest bokeh background, museum "
            "exhibit lighting, no text"
        ),
        "1:1",
    )
    gen_chain_monarch()
    image_to_video(
        "image-to-video-aurora",
        image_prompt=(
            "16:9 wide landscape, aurora borealis rippling green and violet over frozen lake, "
            "tiny ice fishing huts with warm window glow, footprints in snow, crisp arctic night, "
            "no text"
        ),
        video_prompt="Slow gentle pan across aurora curtains, soft snow flurries, hut windows glow warmly",
        duration=CLIP_DURATION,
    )
    gen_music_video_drummer()
    gen_illustrated_library_whale()
    gen_missing_tools(missing_only=False)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    parser = argparse.ArgumentParser(description="Generate docs example assets")
    parser.add_argument(
        "--only",
        help=(
            "comma-separated keys: quickstart-panda,chain-monarch,music-video-garage-drummer,"
            "illustrated-library-whale,image-to-video-aurora,missing-tools,sidecars,"
            "p-image-upscale-hummingbird,p-image-try-on-drummer,p-video-animate-monarch,"
            "p-video-replace-jacket,stable-audio-library-bed,whisperx-drummer-song,"
            "narrated-multi-scene-demo,avatar-multi-scene-demo"
        ),
    )
    parser.add_argument(
        "--missing-only",
        action="store_true",
        help="skip outputs that already exist (use with --only missing-tools or individual keys)",
    )
    parser.add_argument(
        "--video-only",
        action="store_true",
        help="with --only, regen clip from existing stills when supported",
    )
    parser.add_argument(
        "--assemble-only",
        action="store_true",
        help="with --only illustrated-library-whale, re-run p-video from existing still + narration",
    )
    args = parser.parse_args()

    if args.assemble_only:
        render_narrated_pvideo(
            "illustrated-library-whale-reel",
            WHALE_VIDEO,
            OUT / "illustrated-library-whale.png",
            OUT / "illustrated-library-whale-narration.mp3",
        )
        print(f"done — regenerated {OUT.relative_to(ROOT)}/illustrated-library-whale-reel.mp4")
        return

    if not args.only:
        gen_all()
    else:
        keys = {k.strip() for k in args.only.split(",")}
        mo = args.missing_only
        if "missing-tools" in keys:
            gen_missing_tools(missing_only=mo)
        if "sidecars" in keys:
            ensure_sidecars(missing_only=mo)
        if "p-image-upscale-hummingbird" in keys:
            gen_p_image_upscale_hummingbird(missing_only=mo)
        if "p-image-try-on-drummer" in keys:
            gen_p_image_try_on_drummer(missing_only=mo)
        if "p-video-animate-monarch" in keys:
            gen_p_video_animate_monarch(missing_only=mo)
        if "p-video-replace-jacket" in keys:
            gen_p_video_replace_jacket(missing_only=mo)
        if "stable-audio-library-bed" in keys:
            gen_stable_audio_library_bed(missing_only=mo)
        if "whisperx-drummer-song" in keys:
            gen_whisperx_drummer_song(missing_only=mo)
        if "avatar-multi-scene-demo" in keys:
            gen_avatar_multi_scene_demo(missing_only=mo)
        if "narrated-multi-scene-demo" in keys:
            gen_narrated_multi_scene_demo(missing_only=mo)
        if "quickstart-panda" in keys:
            gen_quickstart_panda(video_only=args.video_only)
        if "chain-monarch" in keys:
            gen_chain_monarch(video_only=args.video_only)
        if "music-video-garage-drummer" in keys:
            gen_music_video_drummer(video_only=args.video_only)
        if "illustrated-library-whale" in keys:
            gen_illustrated_library_whale(video_only=args.video_only, assemble_only=args.assemble_only)
        if "image-to-video-aurora" in keys:
            image_to_video(
                "image-to-video-aurora",
                image_prompt="unused",
                video_prompt="Slow gentle pan across aurora curtains, soft snow flurries, hut windows glow warmly",
                duration=CLIP_DURATION,
                regen_video_only=args.video_only,
            )

    pngs = len(list(OUT.glob("*.png")))
    mp4s = len(list(OUT.glob("*.mp4")))
    print(f"done — {pngs} pngs, {mp4s} mp4s in {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
