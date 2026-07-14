#!/usr/bin/env python3
"""Ken Burns still segments + crossfade concat + narration or music mux."""

from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
import tempfile
from pathlib import Path


def probe_duration(path: Path) -> float:
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        raise RuntimeError("ffprobe not found")
    result = subprocess.run(
        [
            ffprobe,
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def resolution_for_aspect(aspect: str) -> tuple[int, int]:
    if aspect in ("9:16", "portrait"):
        return 1080, 1920
    if aspect in ("1:1", "square"):
        return 1080, 1080
    return 1920, 1080


def ken_burns_filter(mode: str, frames: int, width: int, height: int, fps: int) -> str:
    d = max(frames, 1)
    base = f"d={d}:s={width}x{height}:fps={fps}"
    mode = (mode or "zoom_in").lower()
    if mode == "none":
        return f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1"
    if mode == "zoom_out":
        z = f"if(lte(zoom,1.0),1.08,max(1.001,zoom-0.0015))"
        return f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':{base}"
    if mode in ("pan_left", "pan_right"):
        drift = "-0.15" if mode == "pan_left" else "0.15"
        return (
            f"zoompan=z='1.05':x='iw/2-(iw/zoom/2)+({drift})*on':"
            f"y='ih/2-(ih/zoom/2)':{base}"
        )
    # zoom_in (default)
    return f"zoompan=z='min(zoom+0.0015,1.08)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':{base}"


def render_still_segment(
    still: Path,
    duration: float,
    *,
    ken_burns: str,
    width: int,
    height: int,
    fps: int,
    out: Path,
) -> Path:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg not found")
    frames = max(int(math.ceil(duration * fps)), 1)
    vf = ken_burns_filter(ken_burns, frames, width, height, fps)
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            ffmpeg,
            "-y",
            "-loop",
            "1",
            "-i",
            str(still),
            "-vf",
            vf,
            "-t",
            str(duration),
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "18",
            "-pix_fmt",
            "yuv420p",
            "-an",
            str(out),
        ],
        check=True,
        capture_output=True,
    )
    return out


def concat_segments(segment_paths: list[Path], crossfades: list[float], out: Path, fps: int) -> Path:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg not found")
    if len(segment_paths) == 1:
        shutil.copy(segment_paths[0], out)
        return out

    inputs: list[str] = []
    for p in segment_paths:
        inputs.extend(["-i", str(p)])

    fades = crossfades or [0.0] * (len(segment_paths) - 1)
    if len(fades) < len(segment_paths) - 1:
        fades = fades + [0.0] * (len(segment_paths) - 1 - len(fades))

    # Build xfade chain
    durations = [probe_duration(p) for p in segment_paths]
    filter_parts: list[str] = []
    offset = durations[0]
    last_label = "[0:v]"
    for i in range(1, len(segment_paths)):
        fade = max(0.0, min(fades[i - 1], durations[i - 1] * 0.4, durations[i] * 0.4))
        if fade <= 0.01:
            filter_parts.append(f"{last_label}[{i}:v]concat=n=2:v=1:a=0[v{i}]")
            last_label = f"[v{i}]"
            offset = durations[i]
        else:
            start = offset - fade
            filter_parts.append(
                f"{last_label}[{i}:v]xfade=transition=fade:duration={fade:.3f}:offset={start:.3f}[v{i}]"
            )
            last_label = f"[v{i}]"
            offset = start + durations[i]
    filter_complex = ";".join(filter_parts) + f";{last_label}format=yuv420p[vout]"

    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            ffmpeg,
            "-y",
            *inputs,
            "-filter_complex",
            filter_complex,
            "-map",
            "[vout]",
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "18",
            "-r",
            str(fps),
            str(out),
        ],
        check=True,
        capture_output=True,
    )
    return out


def concat_audio_files(audio_paths: list[Path], out: Path) -> Path:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg not found")
    if len(audio_paths) == 1:
        shutil.copy(audio_paths[0], out)
        return out
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        for p in audio_paths:
            f.write(f"file '{p.resolve()}'\n")
        list_path = f.name
    try:
        subprocess.run(
            [
                ffmpeg,
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                list_path,
                "-c",
                "copy",
                str(out),
            ],
            check=True,
            capture_output=True,
        )
    finally:
        Path(list_path).unlink(missing_ok=True)
    return out


def mux_audio(video: Path, audio: Path, out: Path, *, audio_volume: float = 1.0) -> Path:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg not found")
    vol = max(0.0, min(audio_volume, 2.0))
    cmd = [
        ffmpeg,
        "-y",
        "-i",
        str(video),
        "-i",
        str(audio),
        "-map",
        "0:v",
        "-map",
        "1:a",
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-shortest",
    ]
    if abs(vol - 1.0) > 0.01:
        cmd.extend(["-af", f"volume={vol}"])
    cmd.append(str(out))
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(cmd, check=True, capture_output=True)
    return out


def concat_segments_simple(segment_paths: list[Path], out: Path) -> Path:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg not found")
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        for p in segment_paths:
            f.write(f"file '{p.resolve()}'\n")
        list_path = f.name
    try:
        subprocess.run(
            [
                ffmpeg,
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                list_path,
                "-c",
                "copy",
                str(out),
            ],
            check=True,
            capture_output=True,
        )
    finally:
        Path(list_path).unlink(missing_ok=True)
    return out


def scene_durations(scenes: list[dict], plan: dict, audio_dir: Path) -> list[float]:
    defaults = plan.get("defaults", {})
    pad = float(defaults.get("hold_pad_seconds", 0.35))
    fallback = float(defaults.get("hold_seconds", 4.0))
    mode = plan.get("audio_mode", "narration")
    out: list[float] = []
    for scene in scenes:
        sid = scene["id"]
        if mode == "narration":
            mp3 = audio_dir / f"narration_{sid}.mp3"
            if mp3.exists():
                out.append(probe_duration(mp3) + pad)
            elif scene.get("hold_seconds") is not None:
                out.append(float(scene["hold_seconds"]))
            else:
                out.append(fallback)
        elif scene.get("hold_seconds") is not None:
            out.append(float(scene["hold_seconds"]))
        else:
            out.append(fallback)
    return out


def crossfades_for(scenes: list[dict], plan: dict) -> list[float]:
    assembly = plan.get("assembly", {})
    chain = float(assembly.get("crossfade_seconds", 0.4))
    hard = float(assembly.get("hard_cut_crossfade_seconds", 0.0))
    result: list[float] = []
    for i in range(1, len(scenes)):
        if scenes[i].get("chain_from_previous"):
            result.append(chain)
        else:
            result.append(hard)
    return result


def assemble_from_plan(plan_path: Path, out_dir: Path, *, output_name: str = "story_reel.mp4") -> Path:
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    scenes = plan["scenes"]
    stills_dir = out_dir / "stills"
    audio_dir = out_dir / "audio"
    segments_dir = out_dir / "segments"
    segments_dir.mkdir(parents=True, exist_ok=True)

    defaults = plan.get("defaults", {})
    fps = int(defaults.get("fps", 24))
    aspect = defaults.get("aspect_ratio", "9:16")
    width, height = resolution_for_aspect(aspect)

    durations = scene_durations(scenes, plan, audio_dir)
    segment_paths: list[Path] = []
    for scene, duration in zip(scenes, durations):
        still = stills_dir / f"{scene['id']}.png"
        if not still.exists():
            raise FileNotFoundError(f"Missing still {still}")
        seg = segments_dir / f"{scene['id']}.mp4"
        render_still_segment(
            still,
            duration,
            ken_burns=scene.get("ken_burns", plan.get("defaults", {}).get("ken_burns", "zoom_in")),
            width=width,
            height=height,
            fps=fps,
            out=seg,
        )
        segment_paths.append(seg)

    silent = out_dir / "story_silent.mp4"
    fades = crossfades_for(scenes, plan)
    if any(f > 0.01 for f in fades):
        concat_segments(segment_paths, fades, silent, fps)
    else:
        concat_segments_simple(segment_paths, silent)

    mode = plan.get("audio_mode", "narration")
    final = out_dir / output_name
    if mode == "narration":
        narration_files = [audio_dir / f"narration_{s['id']}.mp3" for s in scenes]
        missing = [str(p) for p in narration_files if not p.exists()]
        if missing:
            raise FileNotFoundError(f"Missing narration: {missing}")
        combined = out_dir / "audio" / "narration_full.mp3"
        concat_audio_files(narration_files, combined)
        mux_audio(silent, combined, final)
    else:
        music_path = out_dir / "audio" / "music.mp3"
        if not music_path.exists():
            raise FileNotFoundError(f"Missing music track {music_path}")
        vol = float(plan.get("music", {}).get("volume", 1.0))
        mux_audio(silent, music_path, final, audio_volume=vol)

    return final


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--output-name", default="story_reel.mp4")
    args = parser.parse_args()
    path = assemble_from_plan(args.plan, args.out_dir, output_name=args.output_name)
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
