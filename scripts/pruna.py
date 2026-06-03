#!/usr/bin/env python3
"""Unified CLI for all first-party Pruna models via pruna_client."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from pruna_client.models import PredictionStatus  # noqa: E402

from scripts.pruna_sdk.helpers import (  # noqa: E402
    get_client,
    poll_until_done,
    repo_root,
    require_api_key,
    run_and_save,
    write_manifest,
)
from scripts.pruna_sdk.registry import MODELS, resolve_model  # noqa: E402


def _add_common_output(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--out",
        type=Path,
        default=Path.cwd() / "output" / "pruna-cli",
        help="Output directory or file path",
    )
    parser.add_argument(
        "--sync",
        action="store_true",
        help="Force synchronous API (Try-Sync)",
    )
    parser.add_argument(
        "--async",
        dest="use_async",
        action="store_true",
        help="Force asynchronous API + poll",
    )
    parser.add_argument(
        "--extra",
        type=str,
        default="{}",
        help='JSON object merged into model input (e.g. \'{"seed": 42}\')',
    )


def _sync_flag(args: argparse.Namespace, model: str) -> bool | None:
    if args.sync:
        return True
    if args.use_async:
        return False
    return None


def _parse_extra(raw: str) -> dict:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"--extra must be valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit("--extra must be a JSON object")
    return data


def cmd_list(_: argparse.Namespace) -> int:
    for spec in MODELS.values():
        mode = "sync" if spec.default_sync else "async"
        print(f"{spec.model_id:18} {mode:5}  {spec.description}")
    return 0


def cmd_image(args: argparse.Namespace) -> int:
    extra = _parse_extra(args.extra)
    out = args.out / "p-image.jpg" if args.out.is_dir() else args.out
    manifest = run_and_save(
        get_client(),
        model="p-image",
        input_payload={"prompt": args.prompt, **extra},
        out_path=out,
        sync=_sync_flag(args, "p-image"),
        label="p-image",
    )
    write_manifest(out.parent, manifest)
    print(manifest["output"])
    return 0


def cmd_edit(args: argparse.Namespace) -> int:
    extra = _parse_extra(args.extra)
    images = [Path(p) for p in args.images]
    out = args.out / "p-image-edit.jpg" if args.out.is_dir() else args.out
    client = get_client()
    spec = resolve_model("p-image-edit")
    sync = _sync_flag(args, spec.model_id)
    response = client.generate_image_edit(
        model=spec.model_id,
        prompt=args.prompt,
        images=images,
        sync=sync if sync is not None else spec.default_sync,
        **extra,
    )
    if response.status != PredictionStatus.SUCCEEDED:
        response = poll_until_done(client, response, label=spec.model_id)
    from scripts.pruna_sdk.helpers import download_generation, save_bytes

    content = download_generation(client, response)
    save_bytes(content, out)
    manifest = {"model": spec.model_id, "output": str(out.resolve()), "prompt": args.prompt}
    write_manifest(out.parent, manifest)
    print(out)
    return 0


def cmd_upscale(args: argparse.Namespace) -> int:
    extra = _parse_extra(args.extra)
    out = args.out / "p-image-upscale.jpg" if args.out.is_dir() else args.out
    manifest = run_and_save(
        get_client(),
        model="p-image-upscale",
        input_payload={"image": str(args.image), **extra},
        out_path=out,
        sync=_sync_flag(args, "p-image-upscale"),
        label="p-image-upscale",
        upload_paths={"image": args.image},
    )
    write_manifest(out.parent, manifest)
    print(manifest["output"])
    return 0


def cmd_video(args: argparse.Namespace) -> int:
    extra = _parse_extra(args.extra)
    upload_paths: dict[str, Path] = {}
    if args.image:
        upload_paths["image"] = args.image
    if args.audio:
        upload_paths["audio"] = args.audio
    out = args.out / "p-video.mp4" if args.out.is_dir() else args.out
    manifest = run_and_save(
        get_client(),
        model="p-video",
        input_payload={"prompt": args.prompt, **extra},
        out_path=out,
        sync=_sync_flag(args, "p-video"),
        label="p-video",
        upload_paths=upload_paths or None,
    )
    write_manifest(out.parent, manifest)
    print(manifest["output"])
    return 0


def cmd_avatar(args: argparse.Namespace) -> int:
    extra = _parse_extra(args.extra)
    upload_paths = {"image": args.image}
    if args.audio:
        upload_paths["audio"] = args.audio
    payload: dict = {**extra}
    if args.voice_script:
        payload["voice_script"] = args.voice_script
    out = args.out / "p-video-avatar.mp4" if args.out.is_dir() else args.out
    manifest = run_and_save(
        get_client(),
        model="p-video-avatar",
        input_payload=payload,
        out_path=out,
        sync=_sync_flag(args, "p-video-avatar"),
        label="p-video-avatar",
        upload_paths=upload_paths,
    )
    write_manifest(out.parent, manifest)
    print(manifest["output"])
    return 0


def cmd_animate(args: argparse.Namespace) -> int:
    extra = _parse_extra(args.extra)
    out = args.out / "p-video-animate.mp4" if args.out.is_dir() else args.out
    manifest = run_and_save(
        get_client(),
        model="p-video-animate",
        input_payload={
            "instruction_prompt": args.instruction_prompt,
            **extra,
        },
        out_path=out,
        sync=_sync_flag(args, "p-video-animate"),
        label="p-video-animate",
        upload_paths={"image": args.image, "video": args.video},
    )
    write_manifest(out.parent, manifest)
    print(manifest["output"])
    return 0


def cmd_replace(args: argparse.Namespace) -> int:
    extra = _parse_extra(args.extra)
    out = args.out / "p-video-replace.mp4" if args.out.is_dir() else args.out
    manifest = run_and_save(
        get_client(),
        model="p-video-replace",
        input_payload={"instruction_prompt": args.instruction_prompt, **extra},
        out_path=out,
        sync=_sync_flag(args, "p-video-replace"),
        label="p-video-replace",
        upload_paths={"video": args.video},
        upload_lists={"images": [Path(p) for p in args.images]},
    )
    write_manifest(out.parent, manifest)
    print(manifest["output"])
    return 0


def cmd_generate(args: argparse.Namespace) -> int:
    extra = _parse_extra(args.extra)
    input_path = Path(args.input_json)
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit("input JSON must be an object (prediction input fields)")
    payload.update(extra)
    spec = resolve_model(args.model)
    out = args.out
    if out.is_dir():
        out = out / f"{spec.model_id}{spec.output_ext}"
    manifest = run_and_save(
        get_client(),
        model=spec.model_id,
        input_payload=payload,
        out_path=out,
        sync=_sync_flag(args, spec.model_id),
        label=spec.model_id,
    )
    write_manifest(out.parent, manifest)
    print(manifest["output"])
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Pruna P-API CLI (official pruna_client SDK)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="List supported models")
    p_list.set_defaults(func=cmd_list)

    p_img = sub.add_parser("image", help="p-image text-to-image")
    p_img.add_argument("--prompt", required=True)
    _add_common_output(p_img)
    p_img.set_defaults(func=cmd_image)

    p_edit = sub.add_parser("edit", help="p-image-edit")
    p_edit.add_argument("--prompt", required=True)
    p_edit.add_argument("--images", nargs="+", required=True, help="1–5 image paths")
    _add_common_output(p_edit)
    p_edit.set_defaults(func=cmd_edit)

    p_up = sub.add_parser("upscale", help="p-image-upscale")
    p_up.add_argument("--image", type=Path, required=True)
    _add_common_output(p_up)
    p_up.set_defaults(func=cmd_upscale)

    p_vid = sub.add_parser("video", help="p-video")
    p_vid.add_argument("--prompt", required=True)
    p_vid.add_argument("--image", type=Path, help="Optional first frame for I2V")
    p_vid.add_argument("--audio", type=Path, help="Optional audio-conditioned mode")
    _add_common_output(p_vid)
    p_vid.set_defaults(func=cmd_video)

    p_av = sub.add_parser("avatar", help="p-video-avatar")
    p_av.add_argument("--image", type=Path, required=True)
    p_av.add_argument("--voice-script", dest="voice_script", default="")
    p_av.add_argument("--audio", type=Path, help="Uploaded audio (overrides voice-script)")
    _add_common_output(p_av)
    p_av.set_defaults(func=cmd_avatar)

    p_an = sub.add_parser("animate", help="p-video-animate")
    p_an.add_argument("--image", type=Path, required=True)
    p_an.add_argument("--video", type=Path, required=True, help="Motion template video")
    p_an.add_argument("--instruction-prompt", required=True)
    _add_common_output(p_an)
    p_an.set_defaults(func=cmd_animate)

    p_rep = sub.add_parser("replace", help="p-video-replace")
    p_rep.add_argument("--video", type=Path, required=True)
    p_rep.add_argument("--images", nargs="+", required=True, help="1–4 reference images")
    p_rep.add_argument("--instruction-prompt", required=True)
    _add_common_output(p_rep)
    p_rep.set_defaults(func=cmd_replace)

    p_gen = sub.add_parser("generate", help="Any model from JSON input file")
    p_gen.add_argument("--model", required=True)
    p_gen.add_argument("--input-json", required=True)
    _add_common_output(p_gen)
    p_gen.set_defaults(func=cmd_generate)

    args = parser.parse_args()
    if args.command != "list":
        require_api_key()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
