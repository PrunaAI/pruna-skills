# Illustrated story reel — quality gates

Agent vision review for **illustrated-story-reel** stills, audio, and optional p-video clips.

## Who applies these?

**The coding agent** opens real output files (`stills/*.png`, `audio/*.mp3`, `clips/*.mp4` when p-video) and judges pass/fail. Then present paths for user **approve stills** / **approve audio** / **approve clips** per [illustrated-story-reel-gates.md](./illustrated-story-reel-gates.md).

## Core (every job)

- **`generation-diversity`** — ritual seed + rotate scenario axes.
- **Random seed ritual (`generation-diversity`)** — state ritual string before every prediction; never copy doc examples.
- Goal and acceptance criteria are explicit.
- `aspect_ratio` in plan matches prompt wording (vertical / horizontal / square).
- No accidental watermarks, UI overlays, or stray text unless requested.

## Per model

After each still, open the file and review:

- **Hero + beats (`p-image`, `p-image-edit`):** `image-prompting` and `image-prompting` — skip avatar handoff rows.
- **Narration (`gemini-3.1-flash-tts`):** pace, tone, line clarity per beat; probe ≤ ~19s before p-video.
- **Music bed (`stable-audio-2.5`):** instrumental, no vocals unless brief asks; level appropriate under stills.
- **Motion clips (`p-video`, when `motion_mode: p-video`):** style matches still; gentle illustrated drift; no photoreal morph; audio sync; no VO transcript leaked into motion.
- **Assembled reel (`story_reel.mp4`, Ken Burns):** motion is **smooth** — no tremor/jitter. Fix with `ken_burns` pan + re-assemble — `illustrated-story-reel` **Motion + assemble**. Do not use p-video to fix tremor.

## Traceability

`generation_status.json` under `--out-dir` records phase approvals. Plan JSON retains prompts and narration — treat as confidential project data.
