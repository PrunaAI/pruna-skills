#!/usr/bin/env python3
"""Run music-video plan: song → cuts → align → stills → clips → assemble.

Phased execution (default --phase song): see references/shared/staged-generation-gate.md
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
_workflows = SCRIPT_DIR.parent
while _workflows.name != "workflows" and _workflows.parent != _workflows:
    _workflows = _workflows.parent
SHARED = _workflows / "_shared" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SHARED))

from generation_gate import (  # noqa: E402
    apply_approve_flags,
    ensure_phase_a_allowed,
    ensure_phase_b_allowed,
    ensure_phase_song_allowed,
    load_generation_status,
    write_generation_status,
)
from pruna_api import (  # noqa: E402
    api_seed_from_plan,
    download_file,
    require_api_key,
    run_prediction,
    upload_file,
)
from p_video_payload import build_p_video_payload  # noqa: E402
from cut_timing import build_clips_meta_entry  # noqa: E402


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


def phase_align(plan_path: Path, out_dir: Path, cuts_path: Path) -> None:
    song = out_dir / "song.mp3"
    transcript_path = out_dir / "whisperx_transcript.json"
    if not song.exists():
        raise SystemExit(f"Missing {song} — run --phase song first")
    if not cuts_path.exists():
        raise SystemExit(f"Missing {cuts_path} — run --phase cuts first")

    plan = json.loads(plan_path.read_text())
    lyrics_hint = " ".join(plan.get("lyrics", "").split())[:400]

    if not transcript_path.exists():
        run_script(
            "transcribe_song.py",
            [
                "--song",
                str(song),
                "--out",
                str(transcript_path),
                "--initial-prompt",
                lyrics_hint,
            ],
        )
    run_script(
        "align_lyric_cuts.py",
        ["--cuts", str(cuts_path), "--transcript", str(transcript_path), "--song", str(song)],
    )


def phase_stills(
    plan_path: Path,
    out_dir: Path,
    cuts_path: Path,
    *,
    only: list[str] | None = None,
) -> None:
    api_key = require_api_key()
    plan = json.loads(plan_path.read_text())
    data = json.loads(cuts_path.read_text())
    stills_dir = out_dir / "stills"
    stills_dir.mkdir(parents=True, exist_ok=True)
    api_seed = api_seed_from_plan(plan)
    cast = plan.get("cast", {})
    cast_descriptor = cast.get("cast_descriptor", "character")

    hero_url: str | None = None
    hero_rel = plan.get("hero_still")
    if hero_rel:
        hero_path = Path(hero_rel)
        if not hero_path.is_absolute():
            hero_path = out_dir / hero_path
        if hero_path.exists():
            hero_url = upload_file(hero_path, api_key)
            print(f"Hero still: {hero_path.name}")
        else:
            print(f"Warning: hero_still missing at {hero_path} — falling back to p-image")

    for cut in data["cuts"]:
        if only and cut["id"] not in only:
            continue
        if cut.get("skip_clip"):
            continue
        still_path = stills_dir / f"{cut['id']}.jpeg"
        if still_path.exists() and not only:
            print(f"Skip still {still_path.name} (exists)")
            continue

        prompt = cut.get("still_prompt") or "Cinematic abstract purple light, single frame"
        style = plan.get("style_bible", "")
        beat = cut.get("beat_type", "broll")

        if beat == "performance" and hero_url:
            edit_prompt = (
                f"Using attached reference as exact identity — same {cast_descriptor}, "
                f"same purple knit texture, same golden crown, same face and body proportions. "
                f"Change only: {prompt}"
            )
            if style:
                edit_prompt = f"{edit_prompt}. {style}"
            result = run_prediction(
                "p-image-edit",
                {
                    "prompt": edit_prompt,
                    "images": [hero_url],
                    "aspect_ratio": plan.get("aspect_ratio", "16:9"),
                },
                api_key,
                label=f"still {cut['id']} (edit)",
            )
        else:
            full_prompt = f"{prompt}. {style}" if style else prompt
            p_image_payload: dict = {
                "prompt": full_prompt,
                "aspect_ratio": plan.get("aspect_ratio", "16:9"),
            }
            if api_seed is not None:
                p_image_payload["seed"] = api_seed
            result = run_prediction(
                "p-image",
                p_image_payload,
                api_key,
                label=f"still {cut['id']}",
            )
        url = result.get("generation_url") or result.get("output")
        if not url:
            raise RuntimeError(f"No image URL for {cut['id']}")
        download_file(url, still_path, api_key)
        print(f"Wrote {still_path}")


def phase_video(
    plan_path: Path,
    out_dir: Path,
    cuts_path: Path,
    *,
    only: list[str] | None = None,
) -> None:
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
    api_seed = api_seed_from_plan(plan)

    for cut in data["cuts"]:
        if only and cut["id"] not in only:
            continue
        if cut.get("skip_clip"):
            continue
        clip_name = cut.get("clip") or f"{cut['id']}.mp4"
        clip_path = clips_dir / clip_name
        if clip_path.exists() and not only:
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
            }
            if api_seed is not None:
                payload["seed"] = api_seed
            cast = plan.get("cast", {})
            if cast.get("voice_prompt"):
                payload["voice_prompt"] = cast["voice_prompt"]
        else:
            model = "p-video"
            if beat == "performance":
                prompt = f"{sync_prompt}. {base_motion}"
            else:
                prompt = base_motion
            video_kw: dict = {
                "prompt": prompt,
                "image_url": image_url,
                "audio_url": audio_url,
                "resolution": resolution,
                "fps": 24,
                "save_audio": True,
            }
            if api_seed is not None:
                video_kw["seed"] = api_seed
            payload = build_p_video_payload(**video_kw)

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
        meta[cut["id"]] = build_clips_meta_entry(
            cut,
            model=model,
            host_type=host_type,
            prediction_id=result.get("id"),
            clip=clip_name,
        )
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
            "music_video.mp4",
        ],
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument(
        "--phase",
        choices=("song", "cuts", "align", "stills", "video", "assemble", "all"),
        default="song",
        help="Generation phase (default: song)",
    )
    parser.add_argument(
        "--approve-song",
        action="store_true",
        help="Mark song approved; allow stills/align after song phase",
    )
    parser.add_argument(
        "--approve-stills",
        action="store_true",
        help="Mark Phase A approved; allow video",
    )
    parser.add_argument(
        "--approve-clips",
        action="store_true",
        help="Mark Phase B approved; allow assemble",
    )
    parser.add_argument("--yes-skip-song-gate", action="store_true")
    parser.add_argument("--yes-skip-stills-gate", action="store_true")
    parser.add_argument("--yes-skip-clips-gate", action="store_true")
    parser.add_argument(
        "--only",
        nargs="+",
        metavar="CUT_ID",
        help="Regenerate only these cut ids (overwrites existing stills/clips)",
    )
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    plan = json.loads(args.plan.read_text())
    target = plan.get("target_duration_sec")
    run_phase = args.phase

    apply_approve_flags(args, args.out_dir)
    if run_phase == "song" and args.approve_song and not args.approve_stills and not args.approve_clips:
        if not args.only:
            return

    cuts_path = args.out_dir / "cut_manifest.json"

    if run_phase in ("stills", "video", "align", "all"):
        ensure_phase_song_allowed(
            args.out_dir,
            approve_flag=args.approve_song,
            skip_gate=args.yes_skip_song_gate,
            label=f"Phase {run_phase}",
        )
    if run_phase in ("video", "assemble", "all"):
        ensure_phase_a_allowed(
            args.out_dir,
            approve_flag=args.approve_stills,
            skip_gate=args.yes_skip_stills_gate,
            label=f"Phase {run_phase}",
        )
    if run_phase in ("assemble", "all"):
        ensure_phase_b_allowed(
            args.out_dir,
            approve_flag=args.approve_clips,
            skip_gate=args.yes_skip_clips_gate,
            label="Assembly",
        )

    if run_phase in ("song", "all"):
        phase_song(args.plan, args.out_dir)
        status = load_generation_status(args.out_dir)
        status["phase_song_approved"] = False
        status["phase_a_approved"] = False
        status["phase_b_approved"] = False
        write_generation_status(args.out_dir, status)
        if run_phase == "song":
            print(f"Phase song complete — listen to {args.out_dir / 'song.mp3'}")
            print("Reply with fixes or re-run with --approve-song --phase align")
            return

    if run_phase in ("cuts", "all"):
        cuts_path = phase_cuts(args.plan, args.out_dir, target)
    elif not cuts_path.exists() and run_phase not in ("song",):
        raise SystemExit("Missing cut_manifest.json — run --phase cuts")

    if run_phase in ("align", "all"):
        phase_align(args.plan, args.out_dir, cuts_path)
        if run_phase == "align":
            print(f"Phase align complete — review {cuts_path} alignment_stats")
            print("Re-run with --approve-song --phase stills when ready")
            return

    if run_phase in ("stills", "all"):
        phase_stills(args.plan, args.out_dir, cuts_path, only=args.only)
        status = load_generation_status(args.out_dir)
        status["phase_a_approved"] = False
        status["phase_b_approved"] = False
        write_generation_status(args.out_dir, status)
        if run_phase == "stills":
            print(f"Phase stills complete — review {args.out_dir / 'stills'}")
            print("Reply with fixes or re-run with --approve-stills --phase video")
            return

    if run_phase in ("video", "all"):
        phase_video(args.plan, args.out_dir, cuts_path, only=args.only)
        status = load_generation_status(args.out_dir)
        status["phase_b_approved"] = False
        write_generation_status(args.out_dir, status)
        if run_phase == "video":
            print(f"Phase video complete — review {args.out_dir / 'clips'}")
            print("Reply with fixes or re-run with --approve-clips --phase assemble")
            return

    if run_phase in ("assemble", "all"):
        phase_assemble(args.plan, args.out_dir, cuts_path)
        print(f"Done! {args.out_dir / 'music_video.mp4'}")


if __name__ == "__main__":
    main()
