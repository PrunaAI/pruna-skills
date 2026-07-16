"""Shared p-image hero + p-image-edit still batch helpers for plan runners."""

from __future__ import annotations

import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Callable

from pruna_api import create_prediction, download_file, upload_file, api_seed_from_plan


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


def style_wrap(plan: dict, prompt: str, *, wrap_fn: Callable[[dict, str], str] | None = None) -> str:
    if wrap_fn:
        return wrap_fn(plan, prompt)
    bible = plan.get("style_bible_stills") or plan.get("style_bible") or ""
    return f"{prompt}. {bible}" if bible else prompt


def ensure_hero(
    plan: dict,
    stills: Path,
    api_key: str,
    *,
    wrap_fn: Callable[[dict, str], str] | None = None,
) -> Path:
    hero = stills / "hero.png"
    if hero.exists():
        print(f"Reusing hero: {hero}")
        return hero
    stills.mkdir(parents=True, exist_ok=True)
    print("=== Phase 0: p-image hero ===")
    defaults = plan["defaults"]
    payload: dict = {
        "prompt": style_wrap(plan, plan["hero_prompt"], wrap_fn=wrap_fn),
        "aspect_ratio": defaults["aspect_ratio"],
    }
    api_seed = api_seed_from_plan(plan)
    if api_seed is not None:
        payload["seed"] = api_seed
    job = create_all("p-image", [("hero", payload)], api_key)[0]
    url = job["result"].get("generation_url")
    if not url:
        raise RuntimeError("Hero generation failed")
    download_file(url, hero, api_key)
    print(f"Saved hero: {hero}")
    return hero


def order_scenes_for_still_deps(scenes: list[dict]) -> list[dict]:
    by_id = {s["id"]: s for s in scenes}
    ordered: list[dict] = []
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(s: dict) -> None:
        sid = s["id"]
        if sid in visited:
            return
        if sid in visiting:
            return
        visiting.add(sid)
        ref = s.get("still_from")
        if ref and ref in by_id:
            visit(by_id[ref])
        visiting.remove(sid)
        visited.add(sid)
        ordered.append(s)

    for s in scenes:
        visit(s)
    return ordered


def ensure_start_stills(
    scenes: list[dict],
    plan: dict,
    stills: Path,
    api_key: str,
    *,
    wrap_fn: Callable[[dict, str], str] | None = None,
    edit_prompt_fn: Callable[[dict, dict], str] | None = None,
) -> None:
    missing = [s for s in scenes if not (stills / f"{s['id']}.png").exists()]
    if not missing:
        return
    hero_url = upload_file(ensure_hero(plan, stills, api_key, wrap_fn=wrap_fn), api_key)
    print(f"=== Phase 1: start stills ({len(missing)}) ===")
    defaults = plan["defaults"]
    payloads = []
    for s in missing:
        raw = s["edit_prompt"]
        if edit_prompt_fn:
            raw = edit_prompt_fn(s, plan)
        payloads.append(
            (
                s["id"],
                {
                    "prompt": style_wrap(plan, raw, wrap_fn=wrap_fn),
                    "images": [hero_url],
                    "aspect_ratio": defaults["aspect_ratio"],
                },
            )
        )
    jobs = create_all("p-image-edit", payloads, api_key)
    for scene, job in zip(missing, jobs):
        url = job["result"].get("generation_url")
        if not url:
            raise RuntimeError(f"No start still for {scene['id']}")
        download_file(url, stills / f"{scene['id']}.png", api_key)
        print(f"  start: {stills / f'{scene['id']}.png'}")


def _edit_base_path(scene: dict, scenes: list[dict], index: int, stills: Path, hero: Path) -> Path:
    ref = scene.get("still_from")
    if ref:
        path = stills / f"{ref}.png"
        if path.exists():
            return path
    if index > 0 and scene.get("chain_from_previous"):
        prev = stills / f"{scenes[index - 1]['id']}.png"
        if prev.exists():
            return prev
    return hero


def ensure_chained_start_stills(
    scenes: list[dict],
    plan: dict,
    stills: Path,
    api_key: str,
    *,
    wrap_fn: Callable[[dict, str], str] | None = None,
    edit_prompt_fn: Callable[[dict, dict], str] | None = None,
) -> None:
    """Generate stills in plan order; chain_from_previous / still_from use prior plate."""
    hero_path = ensure_hero(plan, stills, api_key, wrap_fn=wrap_fn)
    defaults = plan["defaults"]
    for i, s in enumerate(scenes):
        dest = stills / f"{s['id']}.png"
        if dest.exists():
            continue
        base = _edit_base_path(s, scenes, i, stills, hero_path)
        label = "hero" if base == hero_path else base.name
        raw = s["edit_prompt"]
        if edit_prompt_fn:
            raw = edit_prompt_fn(s, plan)
        print(f"=== Phase 1: {s['id']} (ref {label}) ===")
        payload = {
            "prompt": style_wrap(plan, raw, wrap_fn=wrap_fn),
            "images": [upload_file(base, api_key)],
            "aspect_ratio": defaults["aspect_ratio"],
        }
        job = create_all("p-image-edit", [(s["id"], payload)], api_key)[0]
        url = job["result"].get("generation_url")
        if not url:
            raise RuntimeError(f"No still for {s['id']}")
        download_file(url, dest, api_key)
        print(f"  start: {dest}")


def ensure_end_stills(
    scenes: list[dict],
    plan: dict,
    stills: Path,
    api_key: str,
    *,
    wrap_fn: Callable[[dict, str], str] | None = None,
    scene_filter: Callable[[dict], bool] | None = None,
) -> None:
    filt = scene_filter or (lambda s: True)
    missing = [
        s
        for s in scenes
        if filt(s)
        and s.get("last_frame_edit_prompt")
        and not (stills / f"{s['id']}_last.png").exists()
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
                "prompt": style_wrap(plan, s["last_frame_edit_prompt"], wrap_fn=wrap_fn),
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
