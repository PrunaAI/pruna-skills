#!/usr/bin/env python3
"""Fast prompt-to-generation entrypoint (guides/workflows/pruna-run)."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from scripts.pruna_sdk.helpers import get_client, repo_root, require_api_key, run_and_save, write_manifest  # noqa: E402
from scripts.pruna_sdk.registry import ROUTE_ALIASES, resolve_model  # noqa: E402


def _detect_route(prompt: str) -> str:
    text = prompt.lower()
    if re.search(r"\b(avatar|talking head|spokesperson|lip.?sync)\b", text):
        return "avatar"
    if re.search(r"\b(replace|recast|swap person|ugc refresh)\b", text):
        return "replace"
    if re.search(r"\b(animate|motion transfer|meme remix)\b", text):
        return "animate"
    if re.search(r"\b(upscale|higher resolution|print ready)\b", text):
        return "upscale"
    if re.search(r"\b(video|reel|cinematic|b-?roll)\b", text):
        return "i2v"
    return "image"


def _chain_i2v(client, prompt: str, out_dir: Path, extra: dict) -> dict:
    still = out_dir / "hero.jpg"
    img_manifest = run_and_save(
        client,
        model="p-image",
        input_payload={"prompt": prompt, **extra},
        out_path=still,
        sync=True,
        label="p-image (i2v chain)",
    )
    video_manifest = run_and_save(
        client,
        model="p-video",
        input_payload={
            "prompt": prompt,
            "duration": extra.get("duration", 5),
            "resolution": extra.get("resolution", "1080p"),
            **{k: v for k, v in extra.items() if k not in ("duration", "resolution")},
        },
        out_path=out_dir / "video.mp4",
        sync=False,
        label="p-video (i2v chain)",
        upload_paths={"image": still},
    )
    return {
        "route": "i2v",
        "stages": [img_manifest, video_manifest],
        "output": video_manifest["output"],
    }


def _chain_avatar(
    client,
    prompt: str,
    out_dir: Path,
    extra: dict,
    voice_script: str,
) -> dict:
    still = out_dir / "portrait.jpg"
    img_manifest = run_and_save(
        client,
        model="p-image",
        input_payload={"prompt": prompt, "aspect_ratio": extra.get("aspect_ratio", "9:16"), **extra},
        out_path=still,
        sync=True,
        label="p-image (avatar chain)",
    )
    script = voice_script or extra.get("voice_script") or (
        "Hi — here's a quick look at what we're launching today."
    )
    avatar_manifest = run_and_save(
        client,
        model="p-video-avatar",
        input_payload={
            "voice_script": script,
            "video_prompt": extra.get("video_prompt", "The person is talking naturally to camera."),
            "voice_prompt": extra.get(
                "voice_prompt",
                "Natural conversational tone, relaxed pacing, honest delivery.",
            ),
            "resolution": extra.get("resolution", "1080p"),
            **{k: v for k, v in extra.items() if k not in ("voice_script", "video_prompt", "voice_prompt", "resolution", "aspect_ratio")},
        },
        out_path=out_dir / "avatar.mp4",
        sync=False,
        label="p-video-avatar",
        upload_paths={"image": still},
    )
    return {
        "route": "avatar",
        "stages": [img_manifest, avatar_manifest],
        "output": avatar_manifest["output"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Pruna fast run — auto-route from prompt")
    parser.add_argument("--prompt", required=True)
    parser.add_argument(
        "--route",
        choices=["auto", "image", "i2v", "avatar", "video", "edit", "upscale", "animate", "replace"]
        + list(ROUTE_ALIASES.keys()),
        default="auto",
    )
    parser.add_argument("--out", type=Path, default=Path.cwd() / "output" / "pruna-run")
    parser.add_argument("--voice-script", default="")
    parser.add_argument("--extra", default="{}", help="JSON merged into model input")
    args = parser.parse_args()

    require_api_key()
    extra = json.loads(args.extra) if args.extra else {}
    if not isinstance(extra, dict):
        raise SystemExit("--extra must be a JSON object")

    route = _detect_route(args.prompt) if args.route == "auto" else args.route
    out_dir = args.out
    out_dir.mkdir(parents=True, exist_ok=True)
    client = get_client()

    if route in ("I", "J", "K", "L"):
        print(
            f"Route {route} is a multi-step scenario workflow. "
            f"Use guides/workflows/ under {repo_root()}.",
            file=sys.stderr,
        )
        return 2

    if route == "i2v":
        manifest = _chain_i2v(client, args.prompt, out_dir, extra)
    elif route == "avatar":
        manifest = _chain_avatar(client, args.prompt, out_dir, extra, args.voice_script)
    elif route in ("image", "p-image"):
        spec = resolve_model("p-image")
        path = out_dir / f"output{spec.output_ext}"
        manifest = run_and_save(
            client,
            model=spec.model_id,
            input_payload={"prompt": args.prompt, **extra},
            out_path=path,
            label=spec.model_id,
        )
        manifest["route"] = "image"
    elif route in ("video", "p-video"):
        spec = resolve_model("p-video")
        path = out_dir / f"output{spec.output_ext}"
        manifest = run_and_save(
            client,
            model=spec.model_id,
            input_payload={"prompt": args.prompt, **extra},
            out_path=path,
            sync=False,
            label=spec.model_id,
        )
        manifest["route"] = "video"
    else:
        print(
            f"Route {route!r} needs explicit assets (images/video). "
            f"Use: python3 scripts/pruna.py {route} --help",
            file=sys.stderr,
        )
        return 2

    manifest["prompt"] = args.prompt
    write_manifest(out_dir, manifest)
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
