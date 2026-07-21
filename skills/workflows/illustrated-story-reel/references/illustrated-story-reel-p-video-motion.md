# Illustrated story reel — p-video motion (Mode B)

Optional **illustrated movement** per beat: upload the beat still + Gemini TTS narration to **`p-video`** (Mode B). Clip length follows audio — **omit `duration`**, set **`save_audio: true`**.

Ken Burns (ffmpeg only) remains the **budget** path — prefer `pan_left` / `pan_right` and follow **Motion + assemble** in `illustrated-story-reel`.

## When to use

| Path | Cost | Motion |
|------|------|--------|
| **`ken_burns`** (default) | images + TTS only | Slow pan/zoom on still |
| **`p-video`** | + one video API call per beat | Books flutter, whale drifts, gentle illustrated drift |

Set `defaults.motion_mode` or per-scene `motion_mode`: `"ken_burns"` \| `"p-video"`.

**Requires `audio_mode: narration`.** Music-mode reels stay Ken Burns + `hold_seconds`.

## Plan fields

| Field | Role |
|-------|------|
| `defaults.motion_mode` | `"ken_burns"` (default) or `"p-video"` |
| `scenes[].motion_mode` | Override per beat |
| `scenes[].video_prompt` | Mode B motion prompt (OPEN/MID/CLOSE) — **no VO transcript** |

TTS per beat must be **≤ ~19s** (P-API audio-led cap ~20s). Probe before render — see [audio-in-video-prompting.md](../../../guides/video-prompting/references/audio-in-video-prompting.md).

## Mode B prompt template

```text
OPEN: hold on paper-cut whale between library shelves, warm amber lamp glow.
MID: whale drifts slowly forward; a few books flutter past; motion matches narrator energy.
CLOSE: settle in the aisle, collage texture stable, gentle drift only.
```

Rules (full ref: [audio-in-video-prompting.md](../../../guides/video-prompting/references/audio-in-video-prompting.md)):

- Describe **picture motion**, not spoken words.
- Match narrator mood — calm story → slow drift; wonder → slightly livelier flutter.
- Keep style stable — no morphing from paper-cut to photoreal.
- Static or slow camera; physics-safe motion on illustrated elements.

## API payload

Use Build the `p-video` payload (see `p-video` skill):

```python
build_p_video_payload(
    prompt=scene["video_prompt"],
    image_url=upload_file(still_path, api_key),
    audio_url=upload_file(narration_path, api_key),
    resolution=plan["defaults"].get("resolution", "1080p"),
    fps=plan["defaults"].get("fps", 24),
    save_audio=True,
    # duration omitted — clip length = narration
)
```

Do **not** post-mux narration over a silent clip — long lines truncate.

## Phases (p-video)

1. Stills → approve
2. TTS per beat → approve audio
3. `p-video` per beat (narration as `audio`) → approve clips
4. ffmpeg concat

Ken Burns path skips video generation; assemble muxes narration over ffmpeg Ken Burns segments. See `illustrated-story-reel`.

## QA

- [ ] Narration probed ≤ ~19s per beat
- [ ] `video_prompt` has no VO transcript
- [ ] Still matches `style_bible` before video
- [ ] Clip motion stays illustrated — no photoreal drift
- [ ] Listen to `clips/*.mp4` before assemble

## Anti-patterns

| Do not | Do instead |
|--------|------------|
| Paste narration text into `video_prompt` | Mode B mood + motion only |
| Set `duration` with uploaded `audio` | Omit `duration` |
| Switch to p-video for Ken Burns tremor | Tune `ken_burns` + re-assemble |
| Mix `ken_burns` and `p-video` beats in one reel (v1) | Uniform `motion_mode` across all beats |
