# p-image-edit quality checklist

After each `p-image-edit` output is saved, **open the file and review it visually** against this checklist (agent vision review — see [generation-quality-checklists.md](../policies/generation-quality-checklists.md#who-applies-these-checklists)).

## Applies to

See the canonical mapping in [`generation-quality-checklists.md`](../policies/generation-quality-checklists.md).

## Edit intent and preservation

- Requested change is present and obvious.
- Locked regions remain stable (identity, product geometry, key wardrobe/details).
- "Change only X" constraints are respected; unrelated regions do not drift.

## Multi-image composition (when used)

- Source images blend coherently (lighting, scale, perspective).
- Subject edges are clean (no obvious cutout seams or ghosting).
- Final composition reads as one scene, not pasted layers.

## Technical and handoff checks

- Output dimensions and `aspect_ratio` match target use.
- Artifacts introduced by edit are absent (smears, repeated textures, malformed hands/faces).
- Result is ready for downstream `p-video` / `p-video-avatar`, or flagged for another pass.
