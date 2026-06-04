#!/usr/bin/env python3
"""Educational explainer — narrator p-video + character p-video-avatar, p-image/edit stills.

Phased execution (default --phase stills): see references/shared/staged-generation-gate.md
  stills  → hero + cast anchors + start/end PNGs
  tts     → Gemini narration MP3s (after still approval)
  video   → p-video + p-video-avatar clips (after still approval)
  assemble → concat + optional bed (after clip approval)
"""

from __future__ import annotations

import argparse
import json
import re
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
from p_video_avatar_payload import apply_avatar_negative_prompt  # noqa: E402
from p_video_payload import (  # noqa: E402
    P_VIDEO_NARRATION_SAFE_MAX_SECONDS,
    build_p_video_payload,
    probe_media_duration_seconds,
    validate_narration_duration,
)
from pruna_api import create_prediction, download_file, require_api_key, upload_file  # noqa: E402
from replicate_api import download_url, require_replicate_token, run_model_prediction  # noqa: E402
from stills_pipeline import create_all, order_scenes_for_still_deps  # noqa: E402

NARRATION_MODEL = "google/gemini-3.1-flash-tts"
BED_MODEL = "stability-ai/stable-audio-2.5"
DEFAULT_RESOLUTION = "720p"
DEFAULT_FPS = 24

# Motion prompts — see references/workflows/interactive-explainer-motion.md
PHYSICS_TRAP_WORDS = (
    " throw ",
    " throws ",
    " throw.",
    " catch ",
    " catches ",
    " toss ",
    " tosses ",
    " pour ",
    " pours ",
    " spill ",
    " splash ",
    " walk across ",
    " walks across ",
    " run toward ",
    " runs toward ",
    " jump ",
    " jumps ",
    " fall ",
    " falls ",
    " collide ",
    " grab ",
    " grabs ",
    " pick up ",
    " set down ",
    " slam ",
    " handoff ",
    "gesture with",
)

def apply_plan_defaults(plan: dict) -> None:
    defaults = plan.setdefault("defaults", {})
    if defaults.get("resolution", DEFAULT_RESOLUTION) != DEFAULT_RESOLUTION:
        print(
            f"Warning: defaults.resolution is {defaults.get('resolution')!r}; "
            f"interactive-explainer recommends {DEFAULT_RESOLUTION!r}."
        )
    defaults.setdefault("resolution", DEFAULT_RESOLUTION)
    if defaults.get("fps", DEFAULT_FPS) != DEFAULT_FPS:
        print(
            f"Warning: defaults.fps is {defaults.get('fps')!r}; "
            f"interactive-explainer recommends {DEFAULT_FPS}."
        )
    defaults.setdefault("fps", DEFAULT_FPS)
    defaults.setdefault("aspect_ratio", "16:9")


def validate_video_prompt(scene_id: str, prompt: str, *, is_character: bool = False) -> None:
    if not prompt.strip():
        print(f"Warning: {scene_id}: missing video_prompt")
        return
    lower = f" {prompt.lower()} "
    if is_character:
        if "open:" in lower or "mid:" in lower or "close:" in lower:
            print(
                f"Warning: {scene_id}: character video_prompt uses OPEN/MID/CLOSE — "
                "prefer one continuous take (see interactive-explainer-motion.md)."
            )
        return
    if "mid:" not in lower:
        print(
            f"Warning: {scene_id}: video_prompt missing MID: beat — "
            "add dynamic camera/light motion (see interactive-explainer-motion.md)."
        )
    for trap in PHYSICS_TRAP_WORDS:
        if trap in lower:
            print(
                f"Warning: {scene_id}: video_prompt may use physics-trap {trap.strip()!r} — "
                "prefer camera dolly, pan, light shift, atmosphere."
            )
            break


VOICE_BY_GENDER = {
    "female": "Zephyr (Female)",
    "male": "Puck (Male)",
}

# Keep in sync with interactive-explainer/SKILL.md "Positive prompts only".
STILL_PROMPT_TRIGGERS = (
    "side by side",
    "before and after",
    "comparison",
    "collage",
    "montage",
    "contact sheet",
    "grid",
    "split composition",
    "split ",
    " labeled",
    "labeled ",
    "facing camera",
    "to camera",
    "speaks to camera",
    "no text",
    "no cartoon",
    "no rain",
    "graphic tee",
    "neon signs",
    "packshot",
    "flat lay",
    "farmers market",
    "market stall",
    "price tag",
    "signage",
    "storefront",
    "packaging",
    "educational end",
    "educational still",
    "documentary still",
    "food-science documentary",
    " end frame",
    "plated meal",
    "restaurant",
    "menu",
    "napkin",
    "utensil",
    "fork ",
    "knife ",
    "greyscale",
    "grayscale",
    "graphite",
    "muted-tone",
    "desaturated",
    "freezer mist",
    "flicker",
    "strobe",
    " pulsate",
    "pulse ",
    "newspaper",
    "broadside",
    "placard",
    "poster",
    "headline",
    "caption",
    "inscription",
    "lettering",
    "typed text",
    "printed page",
    "open book",
    "ledger",
    "proclamation",
    "banner with",
    " maps ",
    " map ",
    "wall chart",
    "hanging sign",
    "congress",
    "liberty",
    "parliament",
    "meeting house",
    "constitution",
    "declaration",
    "ship name",
    "hull lettering",
    "opening:",
    "closing:",
    "frame by frame",
    "storyboard",
    "triptych",
    "multi-panel",
    "multi panel",
    "multiple angles",
    "two frames",
    "sequence of frames",
    "same harbor",
    "same shop",
    "same hall",
    "same window",
    "same painterly",
    "same man",
    "same three",
    "as opening",
    "educational end",
    "cross-section",
)

CHARACTER_STILL_TRIGGERS = (
    "facing camera",
    "to camera",
    "speaks to camera",
    "ready to speak",
)


_STILL_META_PREFIX = re.compile(r"^(opening|closing)\s*:\s*", re.IGNORECASE)
_STILL_SAME_PREFIX = re.compile(r"^same\s+", re.IGNORECASE)


def sanitize_still_prompt(prompt: str) -> str:
    """Strip meta labels and 'Same …' matching language before p-image / p-image-edit."""
    text = prompt.strip()
    text = _STILL_META_PREFIX.sub("", text)
    text = _STILL_SAME_PREFIX.sub("", text)
    return text.strip()


_STYLE_BIBLE_CLAUSE_TRIGGERS = (
    "identical",
    "side by side",
    "split panel",
    "split ",
    "collage",
    "montage",
    "contact sheet",
    "grid",
    "per frame",
)

# Creative prompts only — not spoken dialogue (scene_lines / voice_scripts).
_POSITIVE_WORDING_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bno\s+", re.IGNORECASE), "no …"),
    (re.compile(r"\bavoid\s+", re.IGNORECASE), "avoid …"),
    (re.compile(r"\bwithout\s+", re.IGNORECASE), "without …"),
    (re.compile(r"\bnever\s+", re.IGNORECASE), "never …"),
    (re.compile(r"\bdon'?t\s+", re.IGNORECASE), "don't …"),
    (re.compile(r"\bdo not\s+", re.IGNORECASE), "do not …"),
    (re.compile(r"\bnot\s+", re.IGNORECASE), "not …"),
]

_SKIP_STYLE_CLAUSE_PREFIXES = ("no", "avoid", "without", "never", "don't", "do not", "not")


def assert_positive_wording(text: str, label: str) -> None:
    """Fail plan validation when creative prompts use negation or avoidance language."""
    if not text.strip():
        return
    for pattern, name in _POSITIVE_WORDING_PATTERNS:
        if pattern.search(text):
            raise RuntimeError(
                f"{label} uses {name} — describe what should appear, not what to exclude. "
                "See interactive-explainer/SKILL.md Positive prompts only."
            )


def positive_style_bible(plan: dict) -> str:
    """Style clauses sent to generative APIs — only positive comma-clauses."""
    raw = (plan.get("style_bible_stills") or plan.get("style_bible") or "").strip()
    if not raw:
        return ""
    parts = [p.strip() for p in re.split(r",\s*", raw) if p.strip()]
    keep: list[str] = []
    for p in parts:
        lower = p.lower()
        if any(lower.startswith(f"{prefix} ") or lower == prefix for prefix in _SKIP_STYLE_CLAUSE_PREFIXES):
            continue
        if any(t in lower for t in _STYLE_BIBLE_CLAUSE_TRIGGERS):
            continue
        keep.append(p)
    return ", ".join(keep)


def style_wrap(plan: dict, prompt: str) -> str:
    bible = positive_style_bible(plan)
    return f"{prompt}. {bible}" if bible else prompt


def still_style_wrap(plan: dict, prompt: str) -> str:
    return style_wrap(plan, sanitize_still_prompt(prompt))


def scene_type(scene: dict) -> str:
    return scene.get("type", "narrator")


def is_narrator_scene(scene: dict) -> bool:
    return scene_type(scene) == "narrator"


def is_character_scene(scene: dict) -> bool:
    return scene_type(scene) == "character"


def cast_for_scene(scene: dict, plan: dict) -> dict:
    key = scene.get("cast")
    if not key:
        raise RuntimeError(f"Character scene {scene['id']} missing cast key")
    cast = plan.get("cast", {}).get(key)
    if not cast:
        raise RuntimeError(f"Missing cast.{key} for scene {scene['id']}")
    return cast


def persona_gender_for(scene: dict, cast: dict) -> str:
    raw = scene.get("persona_gender") or cast.get("persona_gender") or ""
    return str(raw).strip().lower()


def cast_voice_for(scene: dict, cast: dict) -> str:
    """Lock avatar TTS to persona gender; plan voice is fallback only."""
    gender = persona_gender_for(scene, cast)
    if gender in VOICE_BY_GENDER:
        return VOICE_BY_GENDER[gender]
    return cast["voice"]


def character_still_body(scene: dict, plan: dict) -> str:
    """Scene still line; skip long cast descriptor when branching from _cast_* anchor."""
    cast = cast_for_scene(scene, plan)
    parts: list[str] = []
    ref = scene.get("still_from") or ""
    if cast.get("character_descriptor") and not str(ref).startswith("_cast_"):
        parts.append(cast["character_descriptor"].strip())
    parts.append(scene["edit_prompt"].strip())
    return ", ".join(parts)


def character_still_prompt(scene: dict, plan: dict) -> str:
    return still_style_wrap(plan, character_still_body(scene, plan))


def still_prompt_fields(plan: dict, scenes: list[dict]) -> list[tuple[str, str]]:
    """Raw still lines only (excludes style_bible) for trigger-word validation."""
    fields: list[tuple[str, str]] = [("hero_prompt", plan.get("hero_prompt", ""))]
    for scene in scenes:
        sid = scene["id"]
        if is_character_scene(scene):
            fields.append((f"{sid}.edit_prompt", character_still_body(scene, plan)))
        else:
            fields.append((f"{sid}.edit_prompt", scene.get("edit_prompt", "")))
        if scene.get("last_frame_edit_prompt"):
            fields.append((f"{sid}.last_frame_edit_prompt", scene["last_frame_edit_prompt"]))
    return fields


def voice_script_for_scene(scene: dict, plan: dict) -> str:
    if scene.get("voice_script"):
        return scene["voice_script"]
    scripts = plan.get("voice_scripts", {})
    if scene["id"] in scripts:
        return scripts[scene["id"]]
    raise RuntimeError(f"Missing voice_script for character scene {scene['id']}")


def narration_for_scene(scene: dict, plan: dict) -> str:
    if scene.get("narration"):
        return scene["narration"]
    return plan.get("narration", {}).get("scene_lines", {}).get(scene["id"], "")


def ensure_hero(plan: dict, stills: Path, api_key: str) -> Path:
    hero = stills / "hero.png"
    if hero.exists():
        print(f"Reusing hero: {hero}")
        return hero
    stills.mkdir(parents=True, exist_ok=True)
    print("=== Phase 0: p-image hero ===")
    defaults = plan["defaults"]
    payload: dict = {
        "prompt": still_style_wrap(plan, plan["hero_prompt"]),
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


def cast_anchor_path(cast_key: str) -> str:
    return f"_cast_{cast_key}"


def resolve_still_ref(ref: str, stills: Path, *, use_end: bool = False) -> Path | None:
    """Map still_from / cast anchor id to an on-disk PNG (scene start, scene end, or _cast_*)."""
    if ref.startswith("_cast_"):
        path = stills / f"{ref}.png"
        return path if path.exists() else None
    if use_end:
        last = stills / f"{ref}_last.png"
        if last.exists():
            return last
    start = stills / f"{ref}.png"
    return start if start.exists() else None


def start_still_base_path(scene: dict, stills: Path, hero: Path) -> Path:
    """Optional still_from: prior scene or _cast_* anchor so character beats keep the same face."""
    ref = scene.get("still_from")
    if ref:
        use_end = bool(scene.get("still_from_end"))
        ref_path = resolve_still_ref(ref, stills, use_end=use_end)
        if ref_path:
            label = ref_path.name
            if use_end:
                label = f"{ref}_last.png"
            print(f"  {scene['id']}: still_from {label}")
            return ref_path
        print(f"Warning: {scene['id']}: still_from {ref!r} missing — falling back to hero")
    return hero


def ensure_cast_anchor_stills(plan: dict, stills: Path, hero_path: Path, api_key: str) -> None:
    """Generate one portrait per cast entry with anchor_still_prompt (face lock for all character rows)."""
    cast_cfg = plan.get("cast", {})
    to_gen: list[tuple[str, str]] = []
    for key, cast in cast_cfg.items():
        prompt = (cast.get("anchor_still_prompt") or "").strip()
        if not prompt:
            continue
        path = stills / f"{cast_anchor_path(key)}.png"
        if path.exists():
            continue
        to_gen.append((key, prompt))
    if not to_gen:
        return
    print(f"=== Phase 0: cast anchors ({len(to_gen)}) ===")
    defaults = plan["defaults"]
    hero_url = upload_file(hero_path, api_key)
    payloads = [
        (
            cast_anchor_path(key),
            {
                "prompt": still_style_wrap(plan, prompt),
                "images": [hero_url],
                "aspect_ratio": defaults["aspect_ratio"],
            },
        )
        for key, prompt in to_gen
    ]
    jobs = create_all("p-image-edit", payloads, api_key)
    for (key, _), job in zip(to_gen, jobs):
        url = job["result"].get("generation_url")
        if not url:
            raise RuntimeError(f"No cast anchor for {key}")
        dest = stills / f"{cast_anchor_path(key)}.png"
        download_file(url, dest, api_key)
        print(f"  cast anchor: {dest.name}")


def generate_start_stills_batch(
    batch: list[dict],
    plan: dict,
    stills: Path,
    hero_path: Path,
    api_key: str,
    *,
    phase_label: str,
) -> None:
    if not batch:
        return
    print(f"=== {phase_label}: start stills ({len(batch)}) ===")
    defaults = plan["defaults"]
    payloads = [
        (
            s["id"],
            {
                "prompt": character_still_prompt(s, plan)
                if is_character_scene(s)
                else still_style_wrap(plan, s["edit_prompt"]),
                "images": [upload_file(start_still_base_path(s, stills, hero_path), api_key)],
                "aspect_ratio": defaults["aspect_ratio"],
            },
        )
        for s in batch
    ]
    jobs = create_all("p-image-edit", payloads, api_key)
    for scene, job in zip(batch, jobs):
        url = job["result"].get("generation_url")
        if not url:
            raise RuntimeError(f"No start still for {scene['id']}")
        download_file(url, stills / f"{scene['id']}.png", api_key)
        print(f"  start: {stills / f'{scene['id']}.png'}")


def ensure_start_stills(scenes: list[dict], plan: dict, stills: Path, api_key: str) -> None:
    missing = [s for s in scenes if not (stills / f"{s['id']}.png").exists()]
    if not missing:
        return
    hero_path = ensure_hero(plan, stills, api_key)
    ensure_cast_anchor_stills(plan, stills, hero_path, api_key)
    needs_end_ref = [s for s in missing if s.get("still_from_end")]
    no_end_ref = [s for s in missing if not s.get("still_from_end")]
    generate_start_stills_batch(
        order_scenes_for_still_deps(no_end_ref),
        plan,
        stills,
        hero_path,
        api_key,
        phase_label="Phase 1a",
    )
    if needs_end_ref:
        print(
            f"  deferring {len(needs_end_ref)} scene(s) with still_from_end "
            "(run end stills first, then Phase 1b)"
        )


def ensure_start_stills_from_end_refs(scenes: list[dict], plan: dict, stills: Path, api_key: str) -> None:
    missing = [
        s
        for s in scenes
        if s.get("still_from_end")
        and not (stills / f"{s['id']}.png").exists()
    ]
    if not missing:
        return
    hero_path = stills / "hero.png"
    if not hero_path.exists():
        hero_path = ensure_hero(plan, stills, api_key)
    generate_start_stills_batch(
        order_scenes_for_still_deps(missing),
        plan,
        stills,
        hero_path,
        api_key,
        phase_label="Phase 1b",
    )


def ensure_end_stills(scenes: list[dict], plan: dict, stills: Path, api_key: str) -> None:
    narrator = [s for s in scenes if is_narrator_scene(s)]
    missing = [
        s
        for s in narrator
        if s.get("last_frame_edit_prompt")
        and (stills / f"{s['id']}.png").exists()
        and not (stills / f"{s['id']}_last.png").exists()
    ]
    if not missing:
        return
    print(f"=== Phase 2: end stills ({len(missing)} narrator scenes) ===")
    defaults = plan["defaults"]
    start_urls = {s["id"]: upload_file(stills / f"{s['id']}.png", api_key) for s in missing}
    payloads = [
        (
            f"{s['id']}_last",
            {
                "prompt": still_style_wrap(plan, s["last_frame_edit_prompt"]),
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


def fit_narration_to_max(path: Path, max_seconds: float) -> None:
    """Speed up TTS with ffmpeg atempo when Gemini reads slower than the p-video cap."""
    dur = probe_media_duration_seconds(path)
    if dur <= max_seconds:
        return
    target = max(max_seconds - 0.25, 1.0)
    tempo = dur / target
    parts: list[str] = []
    remaining = tempo
    while remaining > 2.0:
        parts.append("atempo=2.0")
        remaining /= 2.0
    if remaining > 1.001:
        parts.append(f"atempo={remaining:.4f}")
    filter_chain = ",".join(parts) if parts else "atempo=2.0"
    tmp = path.with_suffix(".tmp.mp3")
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(path), "-filter:a", filter_chain, str(tmp)],
        check=True,
        capture_output=True,
    )
    tmp.replace(path)
    new_dur = probe_media_duration_seconds(path)
    print(f"  {path.name}: sped {dur:.1f}s -> {new_dur:.1f}s ({filter_chain})")


def run_tts(
    scene_id: str,
    text: str,
    plan: dict,
    voice: str,
    token: str,
    audio_dir: Path,
    *,
    max_seconds: float = P_VIDEO_NARRATION_SAFE_MAX_SECONDS,
) -> Path:
    dest = audio_dir / f"narration_{scene_id}.mp3"
    if dest.exists():
        print(f"Reusing TTS: {dest.name}")
        return dest
    style = plan.get("narration", {}).get("style_prompt", "")
    result = run_model_prediction(
        NARRATION_MODEL,
        {"text": text, "voice": voice, "prompt": style, "language_code": "en-US"},
        token,
        label=f"TTS {scene_id}",
    )
    output = result.get("output")
    if not output:
        raise RuntimeError(f"No TTS for {scene_id}")
    download_url(str(output), dest)
    fit_narration_to_max(dest, max_seconds)
    return dest


def chain_from_previous(scene: dict, index: int) -> bool:
    if index == 0:
        return False
    return bool(scene.get("chain_from_previous", False))


def join_crossfades(scenes: list[dict], plan: dict) -> list[float]:
    assembly = plan.get("assembly", {})
    chain_fade = float(assembly.get("chain_crossfade_seconds", 0.12))
    hard_fade = float(assembly.get("hard_cut_crossfade_seconds", 0.0))
    return [chain_fade if chain_from_previous(scenes[i], i) else hard_fade for i in range(1, len(scenes))]


def normalize_clip_for_concat(src: Path, dst: Path) -> None:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg not found")
    dst.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            ffmpeg, "-y", "-i", str(src),
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
            "-movflags", "+faststart", str(dst),
        ],
        check=True,
        capture_output=True,
    )


def assemble_movie(
    clip_paths: list[Path], scenes: list[dict], plan: dict, out_dir: Path, output: Path
) -> Path:
    norm_dir = out_dir / "clips_norm"
    normalized: list[Path] = []
    for src in clip_paths:
        dst = norm_dir / src.name
        if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
            normalize_clip_for_concat(src, dst)
        normalized.append(dst)
    concat_clips(normalized, output, crossfades=join_crossfades(scenes, plan))
    return output


def render_scene(
    i: int,
    scene: dict,
    scenes: list[dict],
    plan: dict,
    stills: Path,
    clips: Path,
    chain: Path,
    audio_dir: Path,
    api_key: str,
    *,
    prev_clip: Path | None = None,
    chain_mode: str = "parallel_vignettes",
) -> tuple[int, Path]:
    sid = scene["id"]
    stype = scene_type(scene)
    dest = clips / f"{sid}.mp4"
    if dest.exists():
        print(f"  reusing: {dest.name} ({stype})")
        return i, dest

    defaults = plan["defaults"]

    if is_character_scene(scene):
        still_path = stills / f"{sid}.png"
        if not still_path.exists():
            raise SystemExit(f"Missing character still: {still_path}")
        cast = cast_for_scene(scene, plan)
        voice = cast_voice_for(scene, cast)
        payload: dict = {
            "image": upload_file(still_path, api_key),
            "voice_script": voice_script_for_scene(scene, plan),
            "voice": voice,
            "voice_language": cast.get("voice_language", "English (US)"),
            "voice_prompt": cast.get("voice_prompt", ""),
            "video_prompt": scene.get("video_prompt", "Medium close-up speaking to camera"),
            "resolution": defaults.get("resolution", DEFAULT_RESOLUTION),
        }
        if plan.get("project_seed") is not None:
            payload["seed"] = plan["project_seed"]
        apply_avatar_negative_prompt(payload, plan, scene)
        model = "p-video-avatar"
    else:
        chain_mode_plan = plan.get("frame_chain_mode", chain_mode)
        use_chain = chain_from_previous(scene, i) and chain_mode_plan == "extract_last_frame" and prev_clip
        if use_chain:
            start_path = chain / f"into_{sid}.png"
            extract_last_frame(prev_clip, start_path)
        else:
            start_path = stills / f"{sid}.png"
        end_path = stills / f"{sid}_last.png"
        if not start_path.exists() or not end_path.exists():
            raise SystemExit(f"Missing narrator stills for {sid}")
        audio_path = audio_dir / f"narration_{sid}.mp3"
        payload = build_p_video_payload(
            prompt=style_wrap(plan, scene["video_prompt"]),
            image_url=upload_file(start_path, api_key),
            audio_url=upload_file(audio_path, api_key),
            last_frame_image_url=upload_file(end_path, api_key),
            resolution=defaults["resolution"],
            fps=defaults.get("fps", DEFAULT_FPS),
            save_audio=True,
        )
        model = "p-video"
        print(f"  {sid}: narrator p-video ({probe_media_duration_seconds(audio_path):.1f}s)")

    result = create_all(model, [(sid, payload)], api_key)[0]["result"]
    url = result.get("generation_url")
    if not url:
        raise RuntimeError(f"No video for {sid}")
    download_file(url, dest, api_key)
    print(f"  clip ({stype}): {dest.name}")
    return i, dest


def render_videos(
    scenes: list[dict],
    plan: dict,
    stills: Path,
    clips: Path,
    chain: Path,
    audio_dir: Path,
    api_key: str,
    *,
    only: list[str] | None = None,
) -> list[Path]:
    chain_mode = plan.get("frame_chain_mode", "parallel_vignettes")
    sequential = chain_mode == "extract_last_frame" and any(
        chain_from_previous(scenes[i], i) for i in range(1, len(scenes))
    )
    n_narr = sum(1 for s in scenes if is_narrator_scene(s))
    n_char = sum(1 for s in scenes if is_character_scene(s))
    print(f"=== Phase 4: video ({'sequential' if sequential else 'parallel'}) — {n_narr} narrator, {n_char} character ===")

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
            _, dest = render_scene(
                i, scene, scenes, plan, stills, clips, chain, audio_dir, api_key,
                prev_clip=prev_clip, chain_mode=chain_mode,
            )
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

    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = [
            pool.submit(
                render_scene, i, s, scenes, plan, stills, clips, chain, audio_dir, api_key,
                chain_mode=chain_mode,
            )
            for i, s in to_render
        ]
        for fut in as_completed(futures):
            i, dest = fut.result()
            results[i] = dest
    clip_paths: list[Path] = []
    for i, scene in enumerate(scenes):
        if i in results:
            clip_paths.append(results[i])
        else:
            p = clips / f"{scene['id']}.mp4"
            if not p.exists():
                raise FileNotFoundError(f"Missing clip for scene {scene['id']}: {p}")
            clip_paths.append(p)
    return clip_paths


def validate_plan(plan: dict, scenes: list[dict]) -> None:
    if not any(is_character_scene(s) for s in scenes):
        print("Warning: no character scenes — plan is narrator-only; see educational-explainer skill for interaction mix.")

    cast_keys = {s.get("cast") for s in scenes if is_character_scene(s)}
    for key in cast_keys:
        if not key:
            continue
        cast = plan.get("cast", {}).get(key, {})
        gender = str(cast.get("persona_gender", "")).lower()
        if gender not in VOICE_BY_GENDER:
            raise RuntimeError(
                f"cast.{key} must set persona_gender to 'female' or 'male' "
                f"(avatar voice is derived from gender)."
            )
        expected = VOICE_BY_GENDER[gender]
        if cast.get("voice") and cast["voice"] != expected:
            print(
                f"Warning: cast.{key}.voice is {cast['voice']!r}; "
                f"runner will use {expected!r} from persona_gender={gender!r}."
            )
        desc = cast.get("character_descriptor", "").lower()
        if gender == "female" and not any(w in desc for w in ("woman", "female", "girl")):
            print(
                f"Warning: cast.{key}.character_descriptor should name a woman/female "
                f"presenter to match persona_gender={gender!r}."
            )
        if gender == "male" and not any(w in desc for w in ("man", "male", "boy")):
            print(
                f"Warning: cast.{key}.character_descriptor should name a man/male "
                f"presenter to match persona_gender={gender!r}."
            )

    for field in ("style_bible", "style_bible_stills"):
        if plan.get(field):
            assert_positive_wording(plan[field], field)
    if plan.get("hero_prompt"):
        assert_positive_wording(plan["hero_prompt"], "hero_prompt")
    narration = plan.get("narration", {})
    if narration.get("style_prompt"):
        assert_positive_wording(narration["style_prompt"], "narration.style_prompt")
    bed = plan.get("background_music", {})
    if isinstance(bed, dict) and bed.get("prompt"):
        assert_positive_wording(str(bed["prompt"]), "background_music.prompt")
    for key, cast in plan.get("cast", {}).items():
        for attr in ("character_descriptor", "anchor_still_prompt", "voice_prompt"):
            if cast.get(attr):
                assert_positive_wording(cast[attr], f"cast.{key}.{attr}")

    bible_raw = (plan.get("style_bible_stills") or plan.get("style_bible") or "").lower()
    for trig in STILL_PROMPT_TRIGGERS:
        if trig in bible_raw:
            raise RuntimeError(
                f"style_bible contains blocked substring {trig!r} — use positive wording; "
                "see interactive-explainer/SKILL.md"
            )

    for label, text in still_prompt_fields(plan, scenes):
        assert_positive_wording(text, label)
        lower = text.lower()
        for trig in STILL_PROMPT_TRIGGERS:
            if trig in lower:
                raise RuntimeError(
                    f"{label} contains still trigger {trig!r} — use positive single-frame "
                    f"wording; see guides/workflows/launches/p-video-replace-comparison/SKILL.md"
                )
        scene_id = label.split(".", 1)[0] if "." in label else None
        if scene_id and any(s["id"] == scene_id and is_character_scene(s) for s in scenes):
            for trig in CHARACTER_STILL_TRIGGERS:
                if trig in lower:
                    raise RuntimeError(
                        f"{label} contains character-still trigger {trig!r} — use slight angle "
                        f"from the side, lips in frame; keep speaks-to-camera in video_prompt only."
                    )

    for scene in scenes:
        vp = scene.get("video_prompt", "")
        if vp:
            assert_positive_wording(vp, f"{scene['id']}.video_prompt")
            validate_video_prompt(scene["id"], vp, is_character=is_character_scene(scene))
        if not is_character_scene(scene):
            continue
        ep = scene.get("edit_prompt", "").lower()
        if not any(m in ep for m in ("mouth", "lips")):
            print(
                f"Warning: {scene['id']}: character edit_prompt should mention lips in frame for lip sync."
            )




def phase_stills(scenes: list[dict], plan: dict, stills: Path, api_key: str) -> None:
    ensure_start_stills(scenes, plan, stills, api_key)
    ensure_end_stills(scenes, plan, stills, api_key)
    ensure_start_stills_from_end_refs(scenes, plan, stills, api_key)
    ensure_end_stills(scenes, plan, stills, api_key)


def phase_tts(
    narrator_scenes: list[dict],
    plan: dict,
    voice: str,
    replicate_token: str,
    audio_dir: Path,
    *,
    only: list[str] | None,
    skip_narration_check: bool,
    narration_max: float,
) -> None:
    if not narrator_scenes:
        return
    print(f"=== Phase 3: Gemini TTS ({len(narrator_scenes)} narrator scenes) ===")
    tts_targets = [s for s in narrator_scenes if not only or s["id"] in only]
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = {
            pool.submit(
                run_tts,
                s["id"],
                narration_for_scene(s, plan),
                plan,
                voice,
                replicate_token,
                audio_dir,
                max_seconds=narration_max,
            ): s["id"]
            for s in tts_targets
        }
        for fut in as_completed(futures):
            path = fut.result()
            if not skip_narration_check:
                validate_narration_duration(
                    probe_media_duration_seconds(path),
                    scene_id=futures[fut],
                    max_seconds=narration_max,
                )


def all_clips_ready(scenes: list[dict], clips: Path) -> bool:
    return all((clips / f"{s['id']}.mp4").exists() for s in scenes)


def phase_assemble(
    clip_paths: list[Path],
    scenes: list[dict],
    plan: dict,
    out_dir: Path,
    *,
    final_name: str,
    replicate_token: str,
    with_bed: bool,
) -> Path:
    slug = final_name.replace("_final.mp4", "").replace(".mp4", "")
    movie = out_dir / f"{slug}.mp4"
    final = out_dir / final_name
    print("=== Phase 5: concat ===")
    assemble_movie(clip_paths, scenes, plan, out_dir, movie)

    bed_cfg = plan.get("background_music", {})
    if with_bed and bed_cfg.get("enabled"):
        duration = int(probe_duration_seconds(movie) + 1)
        bed_path = out_dir / "audio" / "bed.mp3"
        print(f"=== Phase 6: bed ({duration}s) ===")
        generate_bed(
            prompt=bed_cfg.get("prompt", "Documentary bed, no vocals"),
            duration_seconds=min(190, duration),
            out_path=bed_path,
            token=replicate_token,
            model=bed_cfg.get("model", BED_MODEL),
        )
        mix_bed_under_video(
            video_path=movie,
            bed_path=bed_path,
            out_path=final,
            volume=float(bed_cfg.get("volume", 0.09)),
        )
    else:
        shutil.copy(movie, final)

    manifest = {
        "title": plan.get("title"),
        "final": str(final),
        "scene_types": {s["id"]: scene_type(s) for s in scenes},
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return final


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--final-name", default="explainer_final.mp4")
    parser.add_argument(
        "--phase",
        choices=("stills", "tts", "video", "assemble", "all"),
        default="stills",
        help="Generation phase (default: stills)",
    )
    parser.add_argument(
        "--approve-stills",
        action="store_true",
        help="Mark Phase A approved and allow tts/video phases",
    )
    parser.add_argument(
        "--approve-clips",
        action="store_true",
        help="Mark Phase B approved and allow assemble/bed",
    )
    parser.add_argument(
        "--yes-skip-stills-gate",
        action="store_true",
        help="Allow tts/video/all without stills approval (use with care)",
    )
    parser.add_argument(
        "--yes-skip-clips-gate",
        action="store_true",
        help="Allow assemble/all without clip approval (use with care)",
    )
    parser.add_argument(
        "--assemble-only",
        action="store_true",
        help="Concat existing clips and optional bed (no generative API calls)",
    )
    parser.add_argument("--only", nargs="+", metavar="SCENE_ID")
    parser.add_argument("--regen-stills", action="store_true")
    parser.add_argument("--regen-tts", action="store_true")
    parser.add_argument("--regen-clips", action="store_true")
    parser.add_argument("--skip-assembly", action="store_true")
    parser.add_argument("--skip-narration-check", action="store_true")
    args = parser.parse_args()

    plan = json.loads(args.plan.read_text())
    apply_plan_defaults(plan)
    out_dir = args.out_dir
    stills = out_dir / "stills"
    clips = out_dir / "clips"
    chain = out_dir / "chain_frames"
    audio_dir = out_dir / "audio"
    for d in (stills, clips, chain, audio_dir):
        d.mkdir(parents=True, exist_ok=True)

    scenes = plan["scenes"]
    validate_plan(plan, scenes)
    narration_max = float(
        plan.get("narration", {}).get("max_seconds_per_scene", P_VIDEO_NARRATION_SAFE_MAX_SECONDS)
    )
    narrator_scenes = [s for s in scenes if is_narrator_scene(s)]

    if args.regen_stills:
        shutil.rmtree(stills, ignore_errors=True)
        shutil.rmtree(chain, ignore_errors=True)
        stills.mkdir(parents=True, exist_ok=True)
    if args.regen_tts and audio_dir.exists():
        for f in audio_dir.glob("narration_*.mp3"):
            f.unlink()
    if args.regen_clips and clips.exists():
        if args.only:
            for sid in args.only:
                p = clips / f"{sid}.mp4"
                if p.exists():
                    p.unlink()
        else:
            for f in clips.glob("*.mp4"):
                f.unlink()

    status = load_generation_status(out_dir)

    if args.approve_stills:
        status["phase_a_approved"] = True
        write_generation_status(out_dir, status)
        print("Marked phase_a_approved=true in generation_status.json")
        if args.phase == "stills" and not args.regen_stills:
            return

    if args.approve_clips:
        status["phase_b_approved"] = True
        write_generation_status(out_dir, status)
        print("Marked phase_b_approved=true in generation_status.json")

    run_phase = args.phase

    if args.assemble_only:
        if not all_clips_ready(scenes, clips):
            missing = [s["id"] for s in scenes if not (clips / f"{s['id']}.mp4").exists()]
            raise SystemExit(f"Missing clips for scenes: {missing}")
        ensure_phase_b_allowed(
            out_dir,
            approve_flag=args.approve_clips,
            skip_gate=args.yes_skip_clips_gate,
            label="Assembly",
        )
        replicate_token = require_replicate_token() if plan.get("background_music", {}).get("enabled") else ""
        clip_paths = [clips / f"{s['id']}.mp4" for s in scenes]
        final = phase_assemble(
            clip_paths,
            scenes,
            plan,
            out_dir,
            final_name=args.final_name,
            replicate_token=replicate_token,
            with_bed=True,
        )
        print(f"Done! {final}")
        return

    needs_pruna = run_phase in ("stills", "video", "all")
    missing_tts = [
        s
        for s in narrator_scenes
        if not (audio_dir / f"narration_{s['id']}.mp3").exists()
    ]
    needs_replicate = (
        (run_phase in ("tts", "all") and bool(narrator_scenes))
        or (run_phase == "video" and bool(missing_tts))
        or (
            run_phase in ("assemble", "all")
            and plan.get("background_music", {}).get("enabled")
        )
    )
    api_key = require_api_key() if needs_pruna else ""
    replicate_token = require_replicate_token() if needs_replicate else ""

    if run_phase in ("tts", "video", "assemble", "all"):
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

    if run_phase in ("stills", "all"):
        phase_stills(scenes, plan, stills, api_key)
        status = load_generation_status(out_dir)
        status["phase_a_approved"] = False
        status["phase_b_approved"] = False
        write_generation_status(out_dir, status)
        if run_phase == "stills":
            print(f"Phase stills complete — review PNGs under {stills}")
            print("Reply with fixes or re-run with --approve-stills --phase tts")
            return

    if run_phase in ("tts", "all"):
        phase_tts(
            narrator_scenes,
            plan,
            plan.get("narration", {}).get("voice", "Charon"),
            replicate_token,
            audio_dir,
            only=args.only,
            skip_narration_check=args.skip_narration_check,
            narration_max=narration_max,
        )
        if run_phase == "tts":
            print(f"Phase tts complete — listen to MP3s under {audio_dir}")
            print("Reply with line edits or re-run with --phase video")
            return

    if run_phase in ("video", "all"):
        if not narrator_scenes or all(
            (audio_dir / f"narration_{s['id']}.mp3").exists() for s in narrator_scenes
        ):
            pass
        elif run_phase == "video":
            phase_tts(
                narrator_scenes,
                plan,
                plan.get("narration", {}).get("voice", "Charon"),
                replicate_token,
                audio_dir,
                only=args.only,
                skip_narration_check=args.skip_narration_check,
                narration_max=narration_max,
            )
        else:
            raise SystemExit("Missing narration MP3s — run --approve-stills --phase tts first")

        clip_paths = render_videos(
            scenes, plan, stills, clips, chain, audio_dir, api_key, only=args.only
        )
        status = load_generation_status(out_dir)
        status["phase_b_approved"] = False
        write_generation_status(out_dir, status)
        if args.skip_assembly or run_phase == "video":
            print(f"Phase video complete — review clips under {clips}")
            print("Reply with fixes or re-run with --approve-clips --phase assemble")
            return
        if not all_clips_ready(scenes, clips):
            clip_paths = [clips / f"{s['id']}.mp4" for s in scenes]

    if run_phase in ("assemble", "all"):
        if run_phase == "assemble":
            if not all_clips_ready(scenes, clips):
                missing = [s["id"] for s in scenes if not (clips / f"{s['id']}.mp4").exists()]
                raise SystemExit(f"Missing clips for scenes: {missing}")
            clip_paths = [clips / f"{s['id']}.mp4" for s in scenes]
        final = phase_assemble(
            clip_paths,
            scenes,
            plan,
            out_dir,
            final_name=args.final_name,
            replicate_token=(
                replicate_token
                if replicate_token
                else require_replicate_token()
                if plan.get("background_music", {}).get("enabled")
                else ""
            ),
            with_bed=True,
        )
        print(f"Done! {final}")


if __name__ == "__main__":
    main()
