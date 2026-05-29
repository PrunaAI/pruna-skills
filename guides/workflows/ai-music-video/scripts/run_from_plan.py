#!/usr/bin/env python3
"""Run ai-music-video plan: song → cuts → stills → clips → assemble."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SHARED = SCRIPT_DIR.parent.parent / "_shared" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SHARED))

from pruna_api import (  # noqa: E402
    download_file,
    require_api_key,
    run_prediction,
    upload_file,
)


def run_script(name: str, args: list[str]) -> None:
    cmd = [sys.executable, str(SCRIPT_DIR / name), *args]
    subprocess.run(cmd, check=True)


def merge_segment_prompts(plan: dict, cuts: list[dict]) -> list[dict]:
    segments = plan.get("segments", {})
    merged = []
    for cut in cuts:
        entry = dict(cut)
        seg = segments.get(cut["id"], {})
        entry["beat_type"] = seg.get("beat_type", cut.get("beat_type", "broll"))
        entry["still_prompt"] = seg.get("still_prompt", "")
        entry["video_prompt"] = seg.get("video_prompt", "Cinematic smooth motion")
        entry["clip"] = f"{cut['id']}.mp4"
        merged.append(entry)
    return merged


def phase_song(plan_path: Path, out_dir: Path) -> None:
    run_script("generate_song.py", ["--plan", str(plan_path), "--out-dir", str(out_dir)])


def phase_cuts(plan_path: Path, out_dir: Path, target_sec: float | None) -> Path:
    song = out_dir / "song.mp3"
    if not song.exists():
        raise SystemExit(f"Missing {song} — run --phase song first")
    cuts_path = out_dir / "cut_manifest.json"
    run_script(
        "parse_lyric_cuts.py",
        ["--plan", str(plan_path), "--song", str(song), "--out", str(cuts_path)],
    )
    data = json.loads(cuts_path.read_text())
    cuts = data["cuts"]

    if target_sec and data.get("song_duration_sec", 0) > target_sec:
        scale = target_sec / data["song_duration_sec"]
        for cut in cuts:
            cut["start_sec"] = round(cut["start_sec"] * scale, 3)
            cut["end_sec"] = round(cut["end_sec"] * scale, 3)
            cut["duration_sec"] = round(cut["end_sec"] - cut["start_sec"], 3)
        data["song_duration_sec"] = target_sec
        data["cuts"] = cuts

    plan = json.loads(plan_path.read_text())
    data["cuts"] = merge_segment_prompts(plan, cuts)
    cuts_path.write_text(json.dumps(data, indent=2) + "\n")
    return cuts_path


def phase_stills(plan_path: Path, out_dir: Path, cuts_path: Path) -> None:
    api_key = require_api_key()
    plan = json.loads(plan_path.read_text())
    data = json.loads(cuts_path.read_text())
    stills_dir = out_dir / "stills"
    stills_dir.mkdir(parents=True, exist_ok=True)
    seed = plan.get("project_seed", 991001)

    for cut in data["cuts"]:
        still_path = stills_dir / f"{cut['id']}.jpeg"
        if still_path.exists():
            print(f"Skip still {still_path.name} (exists)")
            continue
        prompt = cut.get("still_prompt") or "Cinematic abstract purple light, single frame"
        style = plan.get("style_bible", "")
        full_prompt = f"{prompt}. {style}" if style else prompt
        result = run_prediction(
            "p-image",
            {
                "prompt": full_prompt,
                "aspect_ratio": plan.get("aspect_ratio", "16:9"),
                "seed": seed + hash(cut["id"]) % 10000,
            },
            api_key,
            label=f"still {cut['id']}",
        )
        url = result.get("generation_url") or result.get("output")
        if not url:
            raise RuntimeError(f"No image URL for {cut['id']}")
        download_file(url, still_path, api_key)
        print(f"Wrote {still_path}")


def phase_video(plan_path: Path, out_dir: Path, cuts_path: Path) -> None:
    api_key = require_api_key()
    plan = json.loads(plan_path.read_text())
    data = json.loads(cuts_path.read_text())
    song = out_dir / "song.mp3"
    clips_dir = out_dir / "clips"
    audio_dir = out_dir / "audio"
    stills_dir = out_dir / "stills"
    clips_dir.mkdir(parents=True, exist_ok=True)
    audio_dir.mkdir(parents=True, exist_ok=True)
    resolution = plan.get("resolution", "1080p")
    seed = plan.get("project_seed", 991001)

    for cut in data["cuts"]:
        clip_name = cut.get("clip") or f"{cut['id']}.mp4"
        clip_path = clips_dir / clip_name
        if clip_path.exists():
            print(f"Skip clip {clip_path.name} (exists)")
            continue

        start = cut["start_sec"]
        end = cut["end_sec"]
        audio_slice = audio_dir / f"{cut['id']}.mp3"
        if not audio_slice.exists():
            run_script(
                "slice_audio.py",
                [
                    "--song",
                    str(song),
                    "--start",
                    str(start),
                    "--end",
                    str(end),
                    "--out",
                    str(audio_slice),
                ],
            )

        still_path = stills_dir / f"{cut['id']}.jpeg"
        if not still_path.exists():
            raise SystemExit(f"Missing still {still_path}")

        image_url = upload_file(still_path, api_key)
        audio_url = upload_file(audio_slice, api_key)
        beat = cut.get("beat_type", "broll")
        host_type = plan.get("cast", {}).get("host_type", "human")
        performance_model = plan.get("cast", {}).get("performance_model")

        use_avatar = beat == "performance" and (
            performance_model == "p-video-avatar"
            or (performance_model is None and host_type == "human")
        )

        sync_prompt = (
            "Raps and sings along to the vocal track, mouth opening and closing in sync "
            "with every syllable, energetic hip-hop performance, clear visible lip movement"
        )
        base_motion = cut.get("video_prompt", "Cinematic smooth motion")

        meta_path = out_dir / "clips_meta.json"
        meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}

        if use_avatar:
            model = "p-video-avatar"
            payload = {
                "image": image_url,
                "audio": audio_url,
                "video_prompt": f"{sync_prompt}. {base_motion}",
                "resolution": resolution,
                "seed": seed + abs(hash(cut["id"])) % 10000,
            }
            cast = plan.get("cast", {})
            if cast.get("voice_prompt"):
                payload["voice_prompt"] = cast["voice_prompt"]
        else:
            model = "p-video"
            if beat == "performance":
                prompt = f"{sync_prompt}. {base_motion}"
            else:
                prompt = base_motion
            payload = {
                "prompt": prompt,
                "image": image_url,
                "audio": audio_url,
                "resolution": resolution,
                "save_audio": True,
                "seed": seed + abs(hash(cut["id"])) % 10000,
            }

        result = run_prediction(
            model,
            payload,
            api_key,
            label=f"{model} {cut['id']}",
        )

        url = result.get("generation_url") or result.get("output")
        if not url:
            raise RuntimeError(f"No video URL for {cut['id']}")
        download_file(url, clip_path, api_key)
        meta[cut["id"]] = {
            "model": model,
            "beat_type": beat,
            "host_type": host_type,
            "prediction_id": result.get("id"),
            "clip": clip_name,
        }
        meta_path.write_text(json.dumps(meta, indent=2) + "\n")
        print(f"Wrote {clip_path} ({model})")


def phase_assemble(plan_path: Path, out_dir: Path, cuts_path: Path) -> None:
    song = out_dir / "song.mp3"
    run_script(
        "assemble_music_video.py",
        [
            "--plan",
            str(plan_path),
            "--cuts",
            str(cuts_path),
            "--clips-dir",
            str(out_dir / "clips"),
            "--song",
            str(song),
            "--out-dir",
            str(out_dir),
            "--output-name",
            "purple_pruna_rap.mp4",
        ],
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument(
        "--phase",
        choices=("song", "cuts", "stills", "video", "assemble", "all"),
        default="all",
    )
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    plan = json.loads(args.plan.read_text())
    target = plan.get("target_duration_sec")

    cuts_path = args.out_dir / "cut_manifest.json"

    if args.phase in ("song", "all"):
        phase_song(args.plan, args.out_dir)
    if args.phase in ("cuts", "all"):
        cuts_path = phase_cuts(args.plan, args.out_dir, target)
    elif not cuts_path.exists():
        raise SystemExit("Missing cut_manifest.json — run --phase cuts")
    if args.phase in ("stills", "all"):
        phase_stills(args.plan, args.out_dir, cuts_path)
    if args.phase in ("video", "all"):
        phase_video(args.plan, args.out_dir, cuts_path)
    if args.phase in ("assemble", "all"):
        phase_assemble(args.plan, args.out_dir, cuts_path)


if __name__ == "__main__":
    main()
