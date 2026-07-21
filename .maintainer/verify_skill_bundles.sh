#!/usr/bin/env bash
# Verify skills-only layout: no references/, no plugins/, no scripts, Prerequisites present.
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${REPO_ROOT}"

python3 - <<'PY'
import json
import re
import sys
from pathlib import Path

repo = Path(".")
sys.path.insert(0, str(repo / ".maintainer"))
from skill_catalog import all_primary_skills, load_catalog

bad: list[str] = []

if (repo / "references").is_dir():
    bad.append("references/ still present — craft lives under skills/ only")

plugins = repo / "plugins"
if plugins.is_dir():
    entries = [p for p in plugins.iterdir() if not p.name.startswith(".")]
    if entries:
        bad.append(f"plugins/ still present ({len(entries)} entries)")

for scripts_dir in (repo / "skills" / "workflows").rglob("scripts"):
    if scripts_dir.is_dir() and any(scripts_dir.iterdir()):
        bad.append(f"workflow scripts still present: {scripts_dir}")

RETIRED = {
    "pruna-full",
    "recipe-catalog",
    "requesting-generation-feedback",
    "pruna-generative-pipeline",
    "pruna-run",
}

catalog = load_catalog()
if "pruna-full" in catalog.get("suite", []):
    bad.append("catalog suite still lists pruna-full — should be pruna")

for name in all_primary_skills():
    if name in RETIRED:
        bad.append(f"retired skill still in catalog: {name}")
        continue
    skill_dir = None
    for base in (
        repo / "skills" / "guides",
        repo / "skills" / "image",
        repo / "skills" / "video",
        repo / "skills" / "audio",
        repo / "skills" / "suite",
        repo / "skills" / "workflows",
    ):
        cand = base / name
        if (cand / "SKILL.md").is_file():
            skill_dir = cand
            break
    if not skill_dir:
        bad.append(f"catalog skill missing source: {name}")
        continue
    skill_md = skill_dir / "SKILL.md"
    text = skill_md.read_text()
    if name != "pruna" and "## Prerequisites" not in text:
        if skill_dir.parent.name == "guides" or name == "pruna":
            if "## Install" not in text:
                bad.append(f"{skill_md}: missing ## Install")
        else:
            bad.append(f"{skill_md}: missing ## Prerequisites")
    if skill_dir.parent.name == "guides" and name != "pruna-api":
        m = re.search(r"^description:\s*(.+)$", text, re.M)
        if m and re.match(r'(?i)["\']?pruna\b', m.group(1).strip()):
            bad.append(f"{skill_md}: guide description should not lead with Pruna")

    # Guides: every catalog skill named in prose must have npx skills add …@name
    if skill_dir.parent.name == "guides":
        from skill_catalog import tools, guides, workflows, suite_skills

        installable = set(tools()) | set(guides()) | set(workflows()) | set(suite_skills())
        installable.discard(name)
        mentioned = set(re.findall(r"`([a-z0-9][a-z0-9.-]*)`", text))
        # also backtick-free tool names in Works with lines: p-video / p-image-edit
        mentioned |= set(re.findall(r"\b(p-(?:image|video)(?:-[a-z0-9]+)*)\b", text))
        mentioned |= set(
            re.findall(
                r"\b(gemini-3\.1-flash-tts|music-2\.5|stable-audio-2\.5|whisperx|pruna-api|generation-diversity|image-prompting|video-prompting|audio-prompting)\b",
                text,
            )
        )
        for other in sorted(mentioned & installable):
            if f"@{other}" not in text and f"pruna-skills@{other}" not in text:
                bad.append(
                    f"{skill_md}: mentions `{other}` but missing "
                    f"`npx skills add PrunaAI/pruna-skills@{other}`"
                )

    manifest_path = skill_dir / "skill.manifest.json"
    if manifest_path.is_file():
        manifest = json.loads(manifest_path.read_text())
        if "scripts" in manifest:
            bad.append(f"{manifest_path}: scripts key retired")
        if "tool_skills" in manifest:
            bad.append(f"{manifest_path}: tool_skills key retired")
        for ref in manifest.get("references", []):
            ref_path = skill_dir / "references" / Path(ref).name
            if not ref_path.is_file():
                bad.append(f"{skill_dir}: missing reference {ref}")

    if "<!-- shared-generation-policy -->" in text:
        bad.append(f"{skill_md}: leftover policy injection marker")

# Ban stale patterns under skills/ and key docs
skip_names = {"CHANGELOG.md", "BACKLOG.md", "SKILL-TEST-LOG.md"}
scan_roots = [repo / "skills", repo / "docs", repo / "AGENTS.md", repo / "CONTRIBUTING.md", repo / "README.md"]
for root in scan_roots:
    paths = [root] if root.is_file() else list(root.rglob("*.md"))
    for path in paths:
        if not path.is_file() or path.name in skip_names:
            continue
        # Allow local skill references/ folders (./references/foo.md beside SKILL.md)
        body = path.read_text()
        for i, line in enumerate(body.splitlines(), 1):
            if "run_from_plan" in line or "_shared/scripts" in line:
                bad.append(f"{path}:{i}: stale script reference")
            if "npx plugins add" in line:
                bad.append(f"{path}:{i}: plugins CLI retired")
            if re.search(r"(?<!\./)(?<![a-zA-Z])/references/(policies|shared|image|video|audio|workflows)/", line):
                bad.append(f"{path}:{i}: top-level references/ path")
            if re.search(r"\]\([^)]*SKILL\.md\)", line):
                # Cross-skill hyperlinks only under skills/ — same-package ./SKILL.md ok;
                # docs/SKILL-CATALOG.md keeps GitHub browse links.
                if "skills" not in path.parts:
                    continue
                if re.search(r"\]\(\./SKILL\.md\)", line) or re.search(r"\]\(\.\./SKILL\.md\)", line):
                    continue
                bad.append(f"{path}:{i}: cross-skill SKILL.md hyperlink — use `skill-name` + overview table")
            if "skills" in path.parts and re.search(r"\]\(\.\./(shared|policies)/", line):
                bad.append(f"{path}:{i}: stale ../shared/ or ../policies/ path")

# Relative markdown links under skills/ must resolve
link_re = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
for path in (repo / "skills").rglob("*.md"):
    for i, line in enumerate(path.read_text().splitlines(), 1):
        for m in link_re.finditer(line):
            target = m.group(2).strip()
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            file_part = target.split("#", 1)[0]
            if not file_part:
                continue
            dest = (path.parent / file_part).resolve()
            if not dest.is_file():
                bad.append(f"{path}:{i}: broken link {file_part}")

if bad:
    # Dedupe
    seen = []
    for b in bad:
        if b not in seen:
            seen.append(b)
    print("Skill layout checks failed:", file=sys.stderr)
    print("\n".join(seen[:80]), file=sys.stderr)
    if len(seen) > 80:
        print(f"... and {len(seen) - 80} more", file=sys.stderr)
    sys.exit(1)

print(f"Skill layout OK ({len(all_primary_skills())} catalog skills)")
PY
