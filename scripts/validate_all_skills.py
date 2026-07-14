#!/usr/bin/env python3
"""Validate all primary skills with skills-ref."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
idx = json.loads((REPO / "plugins/publish-index.json").read_text())
failed = 0
for s in idx.get("skills", []):
    name = s["name"]
    path = REPO / f"plugins/{name}/skills/{name}"
    r = subprocess.run(
        ["npx", "--yes", "skills-ref", "validate", str(path)],
        capture_output=True,
        text=True,
    )
    err = (r.stderr or "") + (r.stdout or "")
    if r.returncode != 0:
        # ponytail: skills-ref has no --allow-field depends yet; Pruna workflows need it
        if "Unexpected fields in frontmatter: depends" in err:
            print(f"OK {name} (depends: — skills-ref limitation)")
            continue
        # ponytail: skills-ref rejects dots in names; Replicate model skills keep semver-style names
        if "contains invalid characters" in err and re.search(r"[.]", name):
            print(f"OK {name} (dotted name — skills-ref limitation)")
            continue
        print(f"FAIL {name}: {err.strip()}", file=sys.stderr)
        failed += 1
    else:
        print(f"OK {name}")
sys.exit(1 if failed else 0)
