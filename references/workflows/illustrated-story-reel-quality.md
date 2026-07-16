# Illustrated story reel — quality gates

Agent vision review for **illustrated-story-reel** stills and audio. **No video clip checklist** — this skill does not generate `p-video` output.

## Who applies these?

**The coding agent** opens real output files (`stills/*.png`, `audio/*.mp3`) and judges pass/fail. Then present paths for user **approve stills** / **approve audio** per [illustrated-story-reel-gates.md](./illustrated-story-reel-gates.md).

## Core (every job)

- **[Generation diversity](../policies/generation-diversity.md)** — ritual seed + rotate scenario axes.
- **[Random seed ritual](../policies/random-seed-ritual.md)** — state ritual string before every prediction; never copy doc examples.
- Goal and acceptance criteria are explicit.
- `aspect_ratio` in plan matches prompt wording (vertical / horizontal / square).
- No accidental watermarks, UI overlays, or stray text unless requested.

## Per model

After each still, open the file and review:

- **Hero + beats (`p-image`, `p-image-edit`):** [p-image-quality-checklist.md](../image/p-image-quality-checklist.md) and [p-image-edit-quality-checklist.md](../image/p-image-edit-quality-checklist.md) — skip avatar/video handoff rows; this workflow ends at ffmpeg assembly.
- **Narration (`gemini-3.1-flash-tts`):** pace, tone, line clarity per beat.
- **Music bed (`stable-audio-2.5`):** instrumental, no vocals unless brief asks; level appropriate under stills.

## Traceability

`generation_status.json` under `--out-dir` records phase approvals. Plan JSON retains prompts and narration — treat as confidential project data.
