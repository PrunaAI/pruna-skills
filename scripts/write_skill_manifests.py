#!/usr/bin/env python3
"""Write skill.manifest.json for tool skills (stdlib only). Idempotent."""

from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TOOLS = REPO / "tools"

BASE_PRUNA = [
    "pruna-api.md",
    "api-credentials.md",
    "generation-diversity.md",
    "random-seed-ritual.md",
    "generation-quality-checklists.md",
]

TOOL_REFS: dict[str, list[str]] = {
    "p-image": BASE_PRUNA + ["p-image-quality-checklist.md", "realistic-persona-showcase.md"],
    "p-image-edit": BASE_PRUNA
    + [
        "p-image-edit-quality-checklist.md",
        "scene-anchor-triple.md",
        "scene-anchor-pair.md",
        "parallel-execution.md",
    ],
    "p-image-upscale": BASE_PRUNA + ["p-image-upscale-quality-checklist.md"],
    "p-image-try-on": BASE_PRUNA
    + [
        "p-image-try-on-quality-checklist.md",
        "realistic-persona-showcase.md",
        "visual-variety-bible.md",
    ],
    "p-video": BASE_PRUNA
    + [
        "p-video-quality-checklist.md",
        "scene-anchor-triple.md",
        "scene-anchor-pair.md",
        "parallel-execution.md",
    ],
    "p-video-avatar": BASE_PRUNA
    + [
        "p-video-avatar-quality-checklist.md",
        "realistic-persona-showcase.md",
        "scene-anchor-triple.md",
        "parallel-execution.md",
    ],
    "p-video-animate": BASE_PRUNA + ["p-video-animate-quality-checklist.md", "parallel-execution.md"],
    "p-video-replace": BASE_PRUNA + ["p-video-replace-quality-checklist.md", "parallel-execution.md"],
    "gemini-3.1-flash-tts": [
        "replicate-api.md",
        "api-credentials.md",
        "audio-post-production.md",
        "scene-anchor-triple.md",
        "generation-diversity.md",
        "random-seed-ritual.md",
    ],
    "music-2.5": ["replicate-api.md", "api-credentials.md", "generation-diversity.md", "random-seed-ritual.md"],
    "stable-audio-2.5": ["replicate-api.md", "api-credentials.md", "audio-post-production.md"],
    "whisperx": ["replicate-api.md", "api-credentials.md"],
}

WORKFLOW_MANIFESTS: dict[str, dict] = {
    "pruna-generative-pipeline": {
        "references": [
            "pruna-api.md",
            "api-credentials.md",
            "pruna-models.md",
            "recipe-catalog.md",
            "staged-generation-gate.md",
            "generation-diversity.md",
            "random-seed-ritual.md",
            "generation-quality-checklists.md",
            "workflow-feedback-gates.md",
        ],
        "scripts": {"core": [], "shared": []},
    },
    "pruna-run": {
        "references": ["pruna-api.md", "api-credentials.md", "generation-diversity.md", "random-seed-ritual.md", "staged-generation-gate.md"],
        "scripts": {"core": [], "shared": []},
    },
    "requesting-generation-feedback": {
        "references": [
            "staged-generation-gate.md",
            "api-credentials.md",
            "workflow-feedback-gates.md",
            "generation-quality-checklists.md",
        ],
        "scripts": {"core": [], "shared": []},
    },
    "image-to-video": {
        "references": [
            "pruna-api.md",
            "scene-anchor-triple.md",
            "scene-anchor-pair.md",
            "staged-generation-gate.md",
            "workflow-feedback-gates.md",
            "p-video-quality-checklist.md",
            "generation-diversity.md",
            "random-seed-ritual.md",
            "parallel-execution.md",
        ],
        "scripts": {"core": [], "shared": []},
    },
    "narrated-multi-scene": {
        "references": [
            "pruna-api.md",
            "scene-anchor-triple.md",
            "staged-generation-gate.md",
            "workflow-feedback-gates.md",
            "p-video-quality-checklist.md",
            "generation-diversity.md",
            "random-seed-ritual.md",
            "parallel-execution.md",
        ],
        "scripts": {"core": [], "shared": []},
    },
    "avatar-single-scene": {
        "references": [
            "pruna-api.md",
            "staged-generation-gate.md",
            "workflow-feedback-gates.md",
            "p-video-avatar-quality-checklist.md",
            "realistic-persona-showcase.md",
            "generation-diversity.md",
            "random-seed-ritual.md",
        ],
        "scripts": {"core": [], "shared": []},
    },
}


def write_manifest(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n")


def main() -> None:
    for mod in ("image", "video", "audio"):
        for skill_dir in (TOOLS / mod).iterdir():
            if not skill_dir.is_dir() or not (skill_dir / "SKILL.md").exists():
                continue
            name = skill_dir.name
            refs = TOOL_REFS.get(name)
            if not refs:
                continue
            write_manifest(
                skill_dir / "skill.manifest.json",
                {"scripts": {"core": [], "shared": []}, "references": refs},
            )
            print(f"wrote tools/{mod}/{name}/skill.manifest.json")

    wf_roots = [
        REPO / "workflows/router",
        REPO / "workflows/core",
    ]
    for root in wf_roots:
        for name, spec in WORKFLOW_MANIFESTS.items():
            skill_dir = root / name
            if not (skill_dir / "SKILL.md").exists():
                continue
            if (skill_dir / "skill.manifest.json").exists():
                continue
            write_manifest(skill_dir / "skill.manifest.json", spec)
            print(f"wrote {skill_dir.relative_to(REPO)}/skill.manifest.json")


if __name__ == "__main__":
    main()
