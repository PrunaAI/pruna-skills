#!/usr/bin/env python3
"""Run a P-Video-Animate comparison reel from a JSON scene plan.

Default phase is ``stills``. See references/staged-generation-gate.md.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from pruna_api import download_file, require_api_key, run_prediction, upload_file  # noqa: E402
from pruna_paths import default_out_dir, default_template, repo_root, sibling_script  # noqa: E402

_REPO = repo_root()
DEFAULT_PLAN = _REPO / "output/p-video-animate-announcement/announcement_plan.json"
DEFAULT_OUT = default_out_dir("p-video-animate-announcement")


def voice_prompt_for(motion: dict, cast: dict) -> str:
    return motion.get("voice_prompt") or cast["voice_prompt"]


VOICE_BY_GENDER = {
    "female": "Zephyr (Female)",
    "male": "Puck (Male)",
}


def motion_cast_for(scene: dict, motion: dict, cast: dict) -> dict[str, str]:
    voice = motion.get("voice")
    if not voice:
        gender = str(scene.get("persona_gender", "")).lower()
        voice = VOICE_BY_GENDER.get(gender, cast["voice"])
    return {
        "voice": voice,
        "voice_language": motion.get("voice_language") or cast["voice_language"],
        "voice_prompt": voice_prompt_for(motion, cast),
    }


def trim_video(source: Path, destination: Path, seconds: float) -> None:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg not found on PATH")
    destination.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [ffmpeg, "-y", "-i", str(source), "-t", str(seconds), "-c", "copy", str(destination)],
        check=True,
        capture_output=True,
    )



def generate_hero(path: Path, plan: dict, api_key: str, *, fresh: bool) -> str:
    if path.exists() and not fresh:
        print(f"Reusing hero {path}")
        return upload_file(path, api_key)
    result = run_prediction(
        "p-image",
        {
            "prompt": f"{plan['style_bible']} {plan['hero_prompt']}",
            "aspect_ratio": "16:9",
            "seed": plan.get("hero_seed", plan["project_seed"]),
        },
        api_key,
        label="hero p-image",
    )
    download_file(result["generation_url"], path, api_key)
    return upload_file(path, api_key)


def edit_still(
    *,
    hero_url: str,
    edit_prompt: str,
    style_bible: str,
    out_path: Path,
    api_key: str,
    label: str,
) -> str:
    if out_path.exists():
        print(f"Reusing still {out_path}")
        return upload_file(out_path, api_key)
    result = run_prediction(
        "p-image-edit",
        {
            "prompt": f"{style_bible} {edit_prompt}",
            "images": [hero_url],
        },
        api_key,
        label=f"{label} edit",
    )
    download_file(result["generation_url"], out_path, api_key)
    return upload_file(out_path, api_key)


def generate_persona_still(
    *,
    prompt: str,
    seed: int,
    style_bible: str,
    out_path: Path,
    api_key: str,
    label: str,
) -> str:
    if out_path.exists():
        print(f"Reusing persona {out_path}")
        return upload_file(out_path, api_key)
    result = run_prediction(
        "p-image",
        {
            "prompt": f"{style_bible} {prompt}",
            "aspect_ratio": "16:9",
            "seed": seed,
        },
        api_key,
        label=f"{label} p-image",
    )
    download_file(result["generation_url"], out_path, api_key)
    return upload_file(out_path, api_key)


def render_avatar_scene(scene: dict, ctx: dict, api_key: str) -> dict:
    scene_id = scene["id"]
    out_dir = ctx["out_dir"]
    clip_path = out_dir / "clips" / f"{scene_id:02d}_avatar.mp4"
    if clip_path.exists():
        print(f"Reusing {clip_path}")
        return {"id": scene_id, "type": "avatar", "clip": str(clip_path)}

    still_path = out_dir / "stills" / f"scene{scene_id:02d}.jpeg"
    still_url = edit_still(
        hero_url=ctx["hero_url"],
        edit_prompt=scene["still_edit"],
        style_bible=ctx["style_bible"],
        out_path=still_path,
        api_key=api_key,
        label=f"scene {scene_id}",
    )
    result = run_prediction(
        "p-video-avatar",
        {
            "image": still_url,
            "voice_script": scene["voice_script"],
            "voice": ctx["cast"]["voice"],
            "voice_language": ctx["cast"]["voice_language"],
            "voice_prompt": ctx["cast"]["voice_prompt"],
            "video_prompt": scene["video_prompt"],
            "resolution": ctx["avatar_resolution"],
            "seed": ctx["project_seed"],
        },
        api_key,
        label=f"scene {scene_id} avatar",
    )
    download_file(result["generation_url"], clip_path, api_key)
    return {"id": scene_id, "type": "avatar", "clip": str(clip_path), "still": str(still_path)}


def motion_video_prompt(motion: dict) -> str:
    prompt = motion["video_prompt"].strip()
    if prompt.lower().startswith("camera moves continuously"):
        return prompt
    return (
        "Camera moves continuously for the full clip — never static or locked-off. "
        + prompt
    )


def render_motion_template(scene: dict, ctx: dict, api_key: str) -> Path:
    scene_id = scene["id"]
    motion = scene["motion_source"]
    motion_cast = motion_cast_for(scene, motion, ctx["cast"])
    out_dir = ctx["out_dir"]
    motion_full = out_dir / "motion" / f"scene{scene_id:02d}_motion_full.mp4"
    motion_trim = out_dir / "motion" / f"scene{scene_id:02d}_motion.mp4"
    if motion_trim.exists() and motion_trim.stat().st_size > 0:
        print(f"Reusing {motion_trim}")
        sys.stdout.flush()
        return motion_trim

    still_path = out_dir / "stills" / f"scene{scene_id:02d}_motion_source.jpeg"
    still_url = edit_still(
        hero_url=ctx["hero_url"],
        edit_prompt=motion["still_edit"],
        style_bible=ctx["style_bible"],
        out_path=still_path,
        api_key=api_key,
        label=f"scene {scene_id} motion source",
    )
    result = run_prediction(
        "p-video-avatar",
        {
            "image": still_url,
            "voice_script": motion["voice_script"],
            "voice": motion_cast["voice"],
            "voice_language": motion_cast["voice_language"],
            "voice_prompt": motion_cast["voice_prompt"],
            "video_prompt": motion_video_prompt(motion),
            "resolution": ctx["avatar_resolution"],
            "seed": ctx["project_seed"] + scene_id * 1000,
        },
        api_key,
        label=f"scene {scene_id} motion template",
    )
    download_file(result["generation_url"], motion_full, api_key)
    trim_seconds = ctx.get("motion_trim_seconds")
    if trim_seconds:
        trim_video(motion_full, motion_trim, trim_seconds)
    else:
        shutil.copy2(motion_full, motion_trim)
    return motion_trim


def scene_personas(scene: dict) -> list[dict]:
    if "personas" in scene:
        return scene["personas"]
    return [
        {
            "prompt": scene["persona_prompt"],
            "seed": scene["persona_seed"],
            "output_label": scene.get("output_label", "Animated subject"),
            "beat_label": "Variation 1",
        }
    ]


def render_animate_scene(scene: dict, ctx: dict, api_key: str) -> dict:
    scene_id = scene["id"]
    out_dir = ctx["out_dir"]
    compare_path = out_dir / "clips" / f"{scene_id:02d}_compare.mp4"
    personas = scene_personas(scene)
    compare_config_path = out_dir / "clips" / f"{scene_id:02d}_compare_config.json"
    animated_paths = [
        out_dir / "clips" / f"{scene_id:02d}_animated_{index:02d}.mp4"
        for index in range(1, len(personas) + 1)
    ]
    if compare_path.exists() and compare_path.stat().st_size > 0 and scene_id < ctx.get("from_scene", 1):
        print(f"Reusing {compare_path}")
        sys.stdout.flush()
        return {
            "id": scene_id,
            "type": "animate",
            "compare": str(compare_path),
            "animated": [str(path) for path in animated_paths],
        }

    if scene_id >= ctx.get("from_scene", 1):
        for path in (compare_path, compare_config_path):
            if path.exists():
                path.unlink()
        for pattern in (
            f"scene{scene_id:02d}_*.jpeg",
            f"scene{scene_id:02d}.jpeg",
            f"scene{scene_id:02d}.raw.jpeg",
        ):
            for path in (out_dir / "personas").glob(pattern):
                path.unlink()
        for path in (out_dir / "clips").glob(f"{scene_id:02d}_animated*.mp4"):
            path.unlink()
        motion_trim_old = out_dir / "motion" / f"scene{scene_id:02d}_motion.mp4"
        motion_full_old = out_dir / "motion" / f"scene{scene_id:02d}_motion_full.mp4"
        for path in (motion_trim_old, motion_full_old):
            if path.exists():
                path.unlink()

    motion_trim = render_motion_template(scene, ctx, api_key)
    motion_url = upload_file(motion_trim, api_key)

    sample_specs: list[dict] = []
    persona_paths: list[str] = []

    for index, persona in enumerate(personas, start=1):
        persona_path = out_dir / "personas" / f"scene{scene_id:02d}_{index:02d}.jpeg"
        animated_path = animated_paths[index - 1]
        label = f"scene {scene_id} persona {index}"
        if persona_path.exists() and persona_path.stat().st_size > 0:
            print(f"Reusing {persona_path}")
            sys.stdout.flush()
        else:
            generate_persona_still(
                prompt=persona["prompt"],
                seed=persona["seed"],
                style_bible=ctx["style_bible"],
                out_path=persona_path,
                api_key=api_key,
                label=label,
            )
        persona_url = upload_file(persona_path, api_key)
        persona_paths.append(str(persona_path))

        if animated_path.exists() and animated_path.stat().st_size > 0:
            print(f"Reusing {animated_path}")
            sys.stdout.flush()
        else:
            result = run_prediction(
                "p-video-animate",
                {
                    "video": motion_url,
                    "image": persona_url,
                    "resolution": ctx["animate_resolution"],
                    "target_fps": "original",
                    "save_audio": True,
                    "instruction_prompt": scene["instruction_prompt"],
                },
                api_key,
                label=f"scene {scene_id} animate {index}",
            )
            download_file(result["generation_url"], animated_path, api_key)

        sample_specs.append(
            {
                "output": str(animated_path.relative_to(out_dir)),
                "output_label": persona.get("output_label", scene.get("output_label", "Animated subject")),
                "beat_label": persona.get("beat_label", f"Variation {index}"),
            }
        )

    compare_config = {
        "source": str(motion_trim.relative_to(out_dir)),
        "render": str(compare_path.relative_to(out_dir)),
        "title": scene["slider_title"],
        "source_label": scene["source_label"],
        "compare_mode": "single_pass_multi_slider",
        "samples": sample_specs,
        "timing": {
            "hook_seconds": 0,
            "slider_seconds": 2.5,
            "hold_output_seconds": 0,
            "outro_seconds": 0,
            "transition_seconds": 0,
        },
    }
    compare_config_path.write_text(json.dumps(compare_config, indent=2) + "\n", encoding="utf-8")

    slider_script = sibling_script("generate_video_comparison.py")
    subprocess.run(
        [
            sys.executable,
            str(slider_script),
            "--config",
            str(compare_config_path),
        ],
        check=True,
        cwd=str(out_dir),
    )
    nested_compare = out_dir / "clips" / "clips" / compare_path.name
    if nested_compare.exists() and nested_compare != compare_path:
        compare_path.parent.mkdir(parents=True, exist_ok=True)
        if compare_path.exists():
            compare_path.unlink()
        nested_compare.replace(compare_path)
        nested_dir = nested_compare.parent
        if nested_dir.exists() and not any(nested_dir.iterdir()):
            nested_dir.rmdir()
    return {
        "id": scene_id,
        "type": "animate",
        "motion": str(motion_trim),
        "personas": persona_paths,
        "animated": [str(path) for path in animated_paths],
        "compare": str(compare_path),
        "compare_config": str(compare_config_path),
    }


def scene_clip_path(out_dir: Path, scene: dict) -> Path:
    scene_id = scene["id"]
    if scene["type"] == "avatar":
        return out_dir / "clips" / f"{scene_id:02d}_avatar.mp4"
    return out_dir / "clips" / f"{scene_id:02d}_compare.mp4"


def all_scenes_ready(out_dir: Path, scenes: list[dict]) -> bool:
    for scene in scenes:
        clip = scene_clip_path(out_dir, scene)
        if not clip.exists() or clip.stat().st_size == 0:
            return False
    return True


def assemble_final(out_dir: Path, scenes: list[dict]) -> Path:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg not found on PATH")
    concat_list = out_dir / "concat_list.txt"
    lines: list[str] = []
    for scene in scenes:
        clip = scene_clip_path(out_dir, scene)
        if not clip.exists():
            raise FileNotFoundError(f"Missing clip for scene {scene['id']}: {clip}")
        lines.append(f"file '{clip.resolve()}'")
    concat_list.write_text("\n".join(lines) + "\n", encoding="utf-8")
    final_path = out_dir / "p_video_animate_announcement.mp4"
    copy_cmd = [
        ffmpeg,
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_list),
        "-c",
        "copy",
        str(final_path),
    ]
    result = subprocess.run(copy_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        reencode_cmd = [
            ffmpeg,
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_list),
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
            "-movflags",
            "+faststart",
            str(final_path),
        ]
        subprocess.run(reencode_cmd, check=True)
    return final_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, default=None, help="Scene plan JSON path")
    parser.add_argument("--out-dir", type=Path, default=None, help="Output directory")
    parser.add_argument(
        "--phase",
        choices=("stills", "video", "render", "all"),
        default="stills",
        help="Generation phase (default: stills)",
    )
    parser.add_argument("--approve-stills", action="store_true", help="Allow --phase video")
    parser.add_argument("--yes-skip-stills-gate", action="store_true", help="Skip stills gate for --phase all")
    parser.add_argument(
        "--fresh",
        action="store_true",
        help="Delete generated stills, motion, personas, and clips before running",
    )
    parser.add_argument(
        "--from-scene",
        type=int,
        default=1,
        help="Start at this scene id (reuse earlier compare clips)",
    )
    parser.add_argument(
        "--through-scene",
        type=int,
        default=None,
        help="Stop after this scene id (inclusive)",
    )
    args = parser.parse_args()

    plan_path = args.plan
    if plan_path is None:
        env_plan = os.environ.get("ANNOUNCEMENT_PLAN", "").strip()
        plan_path = Path(env_plan) if env_plan else default_template("config.template.json")
        if not plan_path.exists():
            plan_path = Path(os.environ.get("ANNOUNCEMENT_PLAN", DEFAULT_PLAN))
    out_dir = args.out_dir or Path(os.environ.get("ANNOUNCEMENT_OUT", DEFAULT_OUT))
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.fresh:
        for sub in ("clips", "stills", "personas", "motion"):
            target = out_dir / sub
            if target.exists():
                shutil.rmtree(target)
        for name in ("generation_status.json", "concat_list.txt", "p_video_animate_announcement.mp4", "run.log"):
            path = out_dir / name
            if path.exists():
                path.unlink()

    for sub in ("clips", "stills", "personas", "motion"):
        (out_dir / sub).mkdir(exist_ok=True)

    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    if args.phase in ("video", "all") and not args.approve_stills and not args.yes_skip_stills_gate:
        status_path = out_dir / "generation_status.json"
        approved = False
        if status_path.exists():
            try:
                doc = json.loads(status_path.read_text(encoding="utf-8"))
                approved = bool(doc.get("phase_a_approved")) if isinstance(doc, dict) else False
            except json.JSONDecodeError:
                approved = False
        if not approved:
            raise SystemExit("Phase B blocked — run --phase stills, review, then --approve-stills --phase video")

    if args.approve_stills:
        (out_dir / "generation_status.json").write_text(
            json.dumps({"phase_a_approved": True, "scenes": []}, indent=2) + "\n",
            encoding="utf-8",
        )
        if args.phase == "stills":
            return 0

    if args.phase == "render":
        for scene in plan["scenes"]:
            if scene["type"] != "animate":
                continue
            compare_config_path = out_dir / "clips" / f"{scene['id']:02d}_compare_config.json"
            compare_path = out_dir / "clips" / f"{scene['id']:02d}_compare.mp4"
            if compare_config_path.exists():
                subprocess.run(
                    [sys.executable, str(sibling_script("generate_video_comparison.py")), "--config", str(compare_config_path)],
                    check=True,
                    cwd=str(out_dir),
                )
        return 0

    api_key = require_api_key()
    ctx = {
        "out_dir": out_dir,
        "project_seed": plan["project_seed"],
        "style_bible": plan["style_bible"],
        "cast": plan["cast"],
        "motion_trim_seconds": plan["motion_trim_seconds"],
        "avatar_resolution": plan["avatar_resolution"],
        "animate_resolution": plan["animate_resolution"],
        "from_scene": args.from_scene,
    }

    hero_path = out_dir / "stills" / "hero.jpeg"
    print("Phase 1 — hero anchor")
    ctx["hero_url"] = generate_hero(hero_path, plan, api_key, fresh=args.fresh)

    results: list[dict] = []
    status_path = out_dir / "generation_status.json"
    if status_path.exists() and not args.fresh:
        try:
            results = json.loads(status_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            results = []

    print("Phase 2 — scenes (sequential; resume supported)")
    sys.stdout.flush()
    for scene in plan["scenes"]:
        if scene["id"] < args.from_scene:
            print(f"Skipping scene {scene['id']} (before --from-scene {args.from_scene})")
            sys.stdout.flush()
            continue
        if args.through_scene is not None and scene["id"] > args.through_scene:
            print(f"Skipping scene {scene['id']} (after --through-scene {args.through_scene})")
            sys.stdout.flush()
            continue
        if args.phase == "stills" and scene["type"] == "animate":
            motion = scene["motion_source"]
            still_path = out_dir / "stills" / f"scene{scene['id']:02d}_motion_source.jpeg"
            edit_still(
                hero_url=ctx["hero_url"],
                edit_prompt=motion["still_edit"],
                style_bible=ctx["style_bible"],
                out_path=still_path,
                api_key=api_key,
                label=f"scene {scene['id']} motion source",
            )
            for index, persona in enumerate(scene_personas(scene), start=1):
                persona_path = out_dir / "personas" / f"scene{scene['id']:02d}_{index:02d}.jpeg"
                generate_persona_still(
                    prompt=persona["prompt"],
                    seed=persona["seed"],
                    style_bible=ctx["style_bible"],
                    out_path=persona_path,
                    api_key=api_key,
                    label=f"scene {scene['id']} persona {index}",
                )
            print(f"Done scene {scene['id']} (stills only)")
            continue
        if scene["type"] == "avatar":
            result = render_avatar_scene(scene, ctx, api_key)
            print(f"Done scene {scene['id']} (avatar CTA)")
        elif scene["type"] == "animate":
            result = render_animate_scene(scene, ctx, api_key)
            print(f"Done scene {scene['id']} (animate slider)")
        else:
            raise ValueError(f"Scene {scene['id']} has unsupported type {scene['type']!r}")
        results = [item for item in results if item.get("id") != scene["id"]]
        results.append(result)
        status_path.write_text(json.dumps(sorted(results, key=lambda x: x["id"]), indent=2) + "\n", encoding="utf-8")
        sys.stdout.flush()

    if args.phase in ("stills", "video"):
        print(f"Phase {args.phase} complete — review stills under {out_dir}")
        return 0

    print("Phase 3 — assembly")
    if not all_scenes_ready(out_dir, plan["scenes"]):
        print("Partial run — skipping final assembly until all scenes are complete")
        return 0
    final_path = assemble_final(out_dir, plan["scenes"])
    print(f"Wrote {final_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
