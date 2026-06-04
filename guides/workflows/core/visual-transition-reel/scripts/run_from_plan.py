#!/usr/bin/env python3
"""Scene transition video — p-image hero, p-image-edit stills, p-video pair transitions, concat.

Phased execution (default --phase stills): see references/shared/staged-generation-gate.md
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
_workflows = SCRIPT_DIR.parent
while _workflows.name != "workflows" and _workflows.parent != _workflows:
    _workflows = _workflows.parent
SHARED = _workflows / "_shared" / "scripts"
sys.path.insert(0, str(SHARED))

from concat_clips import concat_clips, extract_last_frame  # noqa: E402
from generation_gate import (  # noqa: E402
    apply_approve_flags,
    ensure_phase_a_allowed,
    ensure_phase_b_allowed,
    load_generation_status,
    write_generation_status,
)
from launch_background_music import generate_bed, mix_bed_under_video, probe_duration_seconds  # noqa: E402
from p_video_payload import build_p_video_payload  # noqa: E402
from pruna_api import create_prediction, download_file, require_api_key, upload_file  # noqa: E402
from replicate_api import require_replicate_token  # noqa: E402

BED_MODEL = "stability-ai/stable-audio-2.5"


def poll_all(jobs: list[dict], api_key: str) -> list[dict]:
    from pruna_api import api_request

    results: list[dict | None] = [None] * len(jobs)
    pending = {i: job for i, job in enumerate(jobs)}
    while pending:
        for i, job in list(pending.items()):
            status, payload = api_request("GET", job["get_url"], headers={"apikey": api_key})
            if status >= 400:
                raise RuntimeError(f"{job['label']} poll failed ({status}): {payload}")
            data = json.loads(payload)
            state = data.get("status", "unknown")
            if state == "succeeded":
                results[i] = data
                del pending[i]
                print(f"{job['label']}: succeeded")
            elif state == "failed":
                raise RuntimeError(f"{job['label']} failed: {payload}")
            else:
                print(f"{job['label']}: {state}...")
        if pending:
            time.sleep(8)
    return results  # type: ignore[return-value]


def create_all(model: str, payloads: list[tuple[str, dict]], api_key: str) -> list[dict]:
    def submit(label: str, payload: dict) -> dict:
        create = create_prediction(model, payload, api_key)
        if create.get("status") == "succeeded":
            return {"label": label, "get_url": None, "result": create}
        get_url = create.get("get_url")
        if not get_url:
            raise RuntimeError(f"{label} missing get_url: {json.dumps(create)}")
        return {"label": label, "get_url": get_url, "result": None}

    with ThreadPoolExecutor(max_workers=min(8, len(payloads))) as pool:
        futures = {pool.submit(submit, label, p): i for i, (label, p) in enumerate(payloads)}
        ordered: list[dict | None] = [None] * len(payloads)
        for future in as_completed(futures):
            ordered[futures[future]] = future.result()
    jobs = ordered  # type: ignore[assignment]
    to_poll = [j for j in jobs if j["get_url"]]
    if to_poll:
        polled = poll_all(to_poll, api_key)
        idx = 0
        for j in jobs:
            if j["get_url"]:
                j["result"] = polled[idx]
                idx += 1
    return jobs


def style_wrap(plan: dict, prompt: str) -> str:
    bible = plan.get("style_bible", "")
    return f"{prompt}. {bible}" if bible else prompt


def chain_from_previous(scene: dict, index: int) -> bool:
    if index == 0:
        return False
    return bool(scene.get("chain_from_previous", False))


def join_crossfades(scenes: list[dict], plan: dict) -> list[float]:
    assembly = plan.get("assembly", {})
    chain_fade = float(assembly.get("chain_crossfade_seconds", 0.15))
    hard_fade = float(assembly.get("hard_cut_crossfade_seconds", 0.0))
    return [chain_fade if chain_from_previous(scenes[i], i) else hard_fade for i in range(1, len(scenes))]


def scene_duration(scene: dict, plan: dict) -> float:
    if scene.get("duration_seconds") is not None:
        return float(scene["duration_seconds"])
    return float(plan.get("defaults", {}).get("duration_seconds", 5))


def ensure_hero(plan: dict, stills: Path, api_key: str) -> Path:
    hero = stills / "hero.png"
    if hero.exists():
        print(f"Reusing hero: {hero}")
        return hero
    print("=== Phase 0: p-image hero ===")
    defaults = plan["defaults"]
    payload: dict = {
        "prompt": style_wrap(plan, plan["hero_prompt"]),
        "aspect_ratio": defaults["aspect_ratio"],
    }
    if plan.get("project_seed") is not None:
        payload["seed"] = plan["project_seed"]
    job = create_all("p-image", [("hero", payload)], api_key)[0]
    url = job["result"].get("generation_url")
    if not url:
        raise RuntimeError("Hero generation failed")
    download_file(url, hero, api_key)
    print(f"Saved hero: {hero}")
    return hero


def ensure_start_stills(scenes: list[dict], plan: dict, stills: Path, api_key: str) -> None:
    missing = [s for s in scenes if not (stills / f"{s['id']}.png").exists()]
    if not missing:
        return
    hero_url = upload_file(ensure_hero(plan, stills, api_key), api_key)
    print(f"=== Phase 1: start stills ({len(missing)}) ===")
    defaults = plan["defaults"]
    payloads = [
        (
            s["id"],
            {
                "prompt": style_wrap(plan, s["edit_prompt"]),
                "images": [hero_url],
                "aspect_ratio": defaults["aspect_ratio"],
            },
        )
        for s in missing
    ]
    jobs = create_all("p-image-edit", payloads, api_key)
    for scene, job in zip(missing, jobs):
        url = job["result"].get("generation_url")
        if not url:
            raise RuntimeError(f"No start still for {scene['id']}")
        download_file(url, stills / f"{scene['id']}.png", api_key)
        print(f"  start: {stills / f'{scene['id']}.png'}")


def ensure_end_stills(scenes: list[dict], plan: dict, stills: Path, api_key: str) -> None:
    missing = [
        s
        for s in scenes
        if s.get("last_frame_edit_prompt") and not (stills / f"{s['id']}_last.png").exists()
    ]
    if not missing:
        return
    print(f"=== Phase 2: end stills ({len(missing)}) ===")
    defaults = plan["defaults"]
    start_urls = {s["id"]: upload_file(stills / f"{s['id']}.png", api_key) for s in missing}
    payloads = [
        (
            f"{s['id']}_last",
            {
                "prompt": style_wrap(plan, s["last_frame_edit_prompt"]),
                "images": [start_urls[s["id"]]],
                "aspect_ratio": defaults["aspect_ratio"],
            },
        )
        for s in missing
    ]
    jobs = create_all("p-image-edit", payloads, api_key)
    for scene, job in zip(missing, jobs):
        url = job["result"].get("generation_url")
        if not url:
            raise RuntimeError(f"No end still for {scene['id']}")
        download_file(url, stills / f"{scene['id']}_last.png", api_key)
        print(f"  end: {stills / f'{scene['id']}_last.png'}")


def normalize_clip_for_concat(src: Path, dst: Path) -> Path:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg not found")
    dst.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            ffmpeg,
            "-y",
            "-i",
            str(src),
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "18",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-ar",
            "48000",
            "-ac",
            "2",
            "-movflags",
            "+faststart",
            str(dst),
        ],
        check=True,
        capture_output=True,
    )
    return dst


def assemble_movie(clip_paths: list[Path], scenes: list[dict], plan: dict, out_dir: Path, output: Path) -> Path:
    norm_dir = out_dir / "clips_norm"
    norm_dir.mkdir(parents=True, exist_ok=True)
    normalized: list[Path] = []
    for src in clip_paths:
        dst = norm_dir / src.name
        if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
            normalize_clip_for_concat(src, dst)
        normalized.append(dst)
    crossfades = join_crossfades(scenes, plan)
    concat_clips(normalized, output, crossfades=crossfades)
    return output


def render_scene(
    i: int,
    scene: dict,
    plan: dict,
    stills: Path,
    clips: Path,
    chain: Path,
    api_key: str,
    *,
    prev_clip: Path | None = None,
    force: bool = False,
) -> Path:
    sid = scene["id"]
    dest = clips / f"{sid}.mp4"
    if dest.exists() and force:
        dest.unlink()
    if dest.exists() and not force:
        print(f"  reusing clip: {dest.name}")
        return dest

    chain_mode = plan.get("frame_chain_mode", "extract_last_frame")
    defaults = plan["defaults"]
    use_chain = chain_from_previous(scene, i) and chain_mode == "extract_last_frame" and prev_clip
    if use_chain:
        start_path = chain / f"into_{sid}.png"
        extract_last_frame(prev_clip, start_path)
        print(f"  {sid}: chained from {prev_clip.name}")
    else:
        start_path = stills / f"{sid}.png"
    end_path = stills / f"{sid}_last.png"
    if not start_path.exists():
        raise SystemExit(f"Missing start still: {start_path}")
    if not end_path.exists():
        raise SystemExit(f"Missing end still: {end_path}")

    prompt = scene.get("video_prompt") or scene.get("prompt", "")
    payload = build_p_video_payload(
        prompt=style_wrap(plan, prompt),
        image_url=upload_file(start_path, api_key),
        last_frame_image_url=upload_file(end_path, api_key),
        resolution=defaults.get("resolution", "720p"),
        fps=defaults.get("fps", 24),
        duration=scene_duration(scene, plan),
        save_audio=False,
    )
    if plan.get("project_seed") is not None:
        payload["seed"] = plan["project_seed"]
    if scene.get("draft") is not None:
        payload["draft"] = scene["draft"]
    elif plan.get("draft") is not None:
        payload["draft"] = plan["draft"]

    result = create_all("p-video", [(sid, payload)], api_key)[0]["result"]
    url = result.get("generation_url")
    if not url:
        raise RuntimeError(f"No video for {sid}")
    download_file(url, dest, api_key)
    print(f"  clip: {dest.name}")
    return dest


def render_videos(
    scenes: list[dict],
    plan: dict,
    stills: Path,
    clips: Path,
    chain: Path,
    api_key: str,
    *,
    only: list[str] | None = None,
) -> list[Path]:
    chain_mode = plan.get("frame_chain_mode", "extract_last_frame")
    sequential = chain_mode == "extract_last_frame" and any(
        chain_from_previous(scenes[i], i) for i in range(1, len(scenes))
    )
    label = "sequential" if sequential else "parallel"
    print(f"=== Phase 3: p-video ({label}, {len(scenes)} scenes) ===")

    if sequential:
        clip_paths: list[Path] = []
        prev_clip: Path | None = None
        for i, scene in enumerate(scenes):
            if only and scene["id"] not in only:
                p = clips / f"{scene['id']}.mp4"
                if p.exists():
                    clip_paths.append(p)
                    prev_clip = p
                continue
            dest = render_scene(i, scene, plan, stills, clips, chain, api_key, prev_clip=prev_clip)
            clip_paths.append(dest)
            prev_clip = dest
        return clip_paths

    results: dict[int, Path] = {}
    to_render: list[tuple[int, dict]] = []
    for i, scene in enumerate(scenes):
        if only and scene["id"] not in only:
            p = clips / f"{scene['id']}.mp4"
            if p.exists():
                results[i] = p
            continue
        if (clips / f"{scene['id']}.mp4").exists() and not only:
            results[i] = clips / f"{scene['id']}.mp4"
        else:
            to_render.append((i, scene))

    def parallel_one(i: int, scene: dict) -> tuple[int, Path]:
        return i, render_scene(i, scene, plan, stills, clips, chain, api_key)

    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(parallel_one, i, s) for i, s in to_render]
        for fut in as_completed(futures):
            i, dest = fut.result()
            results[i] = dest
    return [results[i] for i in range(len(scenes))]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument(
        "--phase",
        choices=("hero", "stills", "video", "assemble", "all"),
        default="stills",
        help="Generation phase (default: stills)",
    )
    parser.add_argument(
        "--approve-stills",
        action="store_true",
        help="Mark Phase A approved; allow video",
    )
    parser.add_argument(
        "--approve-clips",
        action="store_true",
        help="Mark Phase B approved; allow assemble/bed",
    )
    parser.add_argument("--yes-skip-stills-gate", action="store_true")
    parser.add_argument("--yes-skip-clips-gate", action="store_true")
    parser.add_argument(
        "--assemble-only",
        action="store_true",
        help="Concat existing clips and optional bed (no generative API calls)",
    )
    parser.add_argument("--only", nargs="+", metavar="SCENE_ID")
    parser.add_argument("--regen-stills", action="store_true")
    parser.add_argument("--regen-clips", action="store_true")
    parser.add_argument("--skip-assembly", action="store_true")
    args = parser.parse_args()

    plan = json.loads(args.plan.read_text())
    out_dir = args.out_dir
    stills = out_dir / "stills"
    clips = out_dir / "clips"
    chain = out_dir / "chain_frames"
    for d in (stills, clips, chain):
        d.mkdir(parents=True, exist_ok=True)

    scenes = plan["scenes"]
    run_phase = args.phase

    apply_approve_flags(args, out_dir)

    if args.assemble_only:
        ensure_phase_b_allowed(
            out_dir,
            approve_flag=args.approve_clips,
            skip_gate=args.yes_skip_clips_gate,
            label="Assembly",
        )
        clip_paths = [clips / f"{s['id']}.mp4" for s in scenes]
        if not all(p.exists() for p in clip_paths):
            missing = [s["id"] for s in scenes if not (clips / f"{s['id']}.mp4").exists()]
            raise SystemExit(f"Missing clips for scenes: {missing}")
        movie = out_dir / "transition_reel.mp4"
        assemble_movie(clip_paths, scenes, plan, out_dir, movie)
        bed_cfg = plan.get("background_music", {})
        final = out_dir / "transition_reel_final.mp4"
        if bed_cfg.get("enabled"):
            token = require_replicate_token()
            duration = int(probe_duration_seconds(movie) + 1)
            bed_path = out_dir / "audio" / "bed.mp3"
            bed_path.parent.mkdir(parents=True, exist_ok=True)
            generate_bed(
                prompt=bed_cfg.get("prompt", "Ambient instrumental bed, no vocals"),
                duration_seconds=min(190, duration),
                out_path=bed_path,
                token=token,
                model=bed_cfg.get("model", BED_MODEL),
            )
            mix_bed_under_video(
                video_path=movie,
                bed_path=bed_path,
                out_path=final,
                volume=float(bed_cfg.get("volume", 0.12)),
            )
        else:
            shutil.copy(movie, final)
        print(f"Done! {final}")
        return

    if args.regen_stills:
        shutil.rmtree(stills, ignore_errors=True)
        shutil.rmtree(chain, ignore_errors=True)
        stills.mkdir(parents=True, exist_ok=True)
    if args.regen_clips and clips.exists():
        for f in clips.glob("*.mp4"):
            f.unlink()

    needs_api = run_phase in ("hero", "stills", "video", "all")
    if run_phase in ("video", "assemble", "all"):
        ensure_phase_a_allowed(
            out_dir,
            approve_flag=args.approve_stills,
            skip_gate=args.yes_skip_stills_gate,
            label=f"Phase {run_phase}",
        )
    if run_phase in ("assemble", "all"):
        ensure_phase_b_allowed(
            out_dir,
            approve_flag=args.approve_clips,
            skip_gate=args.yes_skip_clips_gate,
            label="Assembly",
        )

    api_key = require_api_key() if needs_api else ""
    phase = run_phase

    if phase in ("hero", "stills", "video", "all"):
        ensure_start_stills(scenes, plan, stills, api_key)
        ensure_end_stills(scenes, plan, stills, api_key)
        status = load_generation_status(out_dir)
        status["phase_a_approved"] = False
        status["phase_b_approved"] = False
        write_generation_status(out_dir, status)
        if phase in ("hero", "stills"):
            print(f"Phase {phase} complete — review stills under {stills}")
            print("Reply with fixes or re-run with --approve-stills --phase video")
            return

    clip_paths: list[Path] = []
    if phase in ("video", "assemble", "all"):
        clip_paths = render_videos(
            scenes, plan, stills, clips, chain, api_key, only=args.only
        )
        status = load_generation_status(out_dir)
        status["phase_b_approved"] = False
        write_generation_status(out_dir, status)
        if args.skip_assembly or phase == "video":
            print(f"Phase video complete — review clips under {clips}")
            print("Reply with fixes or re-run with --approve-clips --phase assemble")
            return

    if phase in ("assemble", "all"):
        if not clip_paths:
            clip_paths = [clips / f"{s['id']}.mp4" for s in scenes]
        movie = out_dir / "transition_reel.mp4"
        print("=== Phase 4: concat ===")
        assemble_movie(clip_paths, scenes, plan, out_dir, movie)

        bed_cfg = plan.get("background_music", {})
        final = out_dir / "transition_reel_final.mp4"
        if bed_cfg.get("enabled"):
            token = require_replicate_token()
            duration = int(probe_duration_seconds(movie) + 1)
            bed_path = out_dir / "audio" / "bed.mp3"
            bed_path.parent.mkdir(parents=True, exist_ok=True)
            print(f"=== Phase 5: bed ({duration}s) ===")
            generate_bed(
                prompt=bed_cfg.get("prompt", "Ambient instrumental bed, no vocals"),
                duration_seconds=min(190, duration),
                out_path=bed_path,
                token=token,
                model=bed_cfg.get("model", BED_MODEL),
            )
            mix_bed_under_video(
                video_path=movie,
                bed_path=bed_path,
                out_path=final,
                volume=float(bed_cfg.get("volume", 0.12)),
            )
        else:
            shutil.copy(movie, final)

        manifest = {
            "title": plan.get("title"),
            "scene_count": len(scenes),
            "final": str(final),
            "crossfades": join_crossfades(scenes, plan),
        }
        (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
        print(f"Done! {final}")


if __name__ == "__main__":
    main()
