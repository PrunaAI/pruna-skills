# Scene anchor pair (visual transitions)

Canonical pattern for **smooth visual transitions** with Pruna **`p-video`**: two stills bracket motion; a **`prompt`** describes what happens **between** them. No narration required.

Related: [scene-anchor-triple.md](./scene-anchor-triple.md) (pair + audio) · [prompt-dramaturgy.md](./prompt-dramaturgy.md) · [physics-safe-motion.md](./physics-safe-motion.md) · [clip-chaining.md](./clip-chaining.md) · `p-video` · `p-image` · `p-image-edit`

## The pair

Each scene row supplies **two Pruna file URLs** (from `POST /v1/files`) plus a motion **`prompt`** and explicit **`duration`**:

| Anchor | `input` field | Role |
|--------|---------------|------|
| **First frame** | `image` | Opening composition |
| **Last frame** | `last_frame_image` | Closing composition the clip moves toward |
| **Transition motion** | `prompt` | Camera + action between the two plates — not a description of the stills |
| **Timing** | `duration` | 1–20s on P-API; prefer **8–10s** for character transitions, **5–8s** for simple camera moves |

```json
{
  "prompt": "OPEN: hold wide. MID: slow crane down, neon signs flicker. CLOSE: settle on end pose.",
  "image": "https://api.pruna.ai/v1/files/START_ID",
  "last_frame_image": "https://api.pruna.ai/v1/files/END_ID",
  "duration": 10,
  "resolution": "720p",
  "fps": 24
}
```

**Do not** set `duration` when `audio` is also present — use [scene-anchor-triple.md](./scene-anchor-triple.md) instead.

## Stills phase (`p-image` + `p-image-edit`)

| Still | Source | Plan field |
|-------|--------|------------|
| **Hero** (optional) | `p-image` text prompt | `hero_prompt` |
| **Start** | Hero + `p-image-edit` `edit_prompt` | `edit_prompt` |
| **End** | Start still + `p-image-edit` `last_frame_edit_prompt` | `last_frame_edit_prompt` |

Or skip generation: upload user photos → `/v1/files` → set `image_source: "upload"` with local paths in the runner manifest.

Run **hero** once, then **start stills in parallel**, then **end stills in parallel** from each start still.

### Edit prompt rules

- **Start still:** OPENING composition — what the viewer sees at beat open. Prefix with `OPENING:` or `OPEN:` when helpful.
- **End still:** CLOSING composition — clear end pose before the cut. Prefix with `CLOSING:` or `CLOSE:`.
- **Subject must stay in both stills** when the beat follows a character or product — if the person is in the start plate, they must appear in the end plate. Never edit the subject out.
- Keep subject identity, lighting era, and aspect ratio locked via a shared **`style_bible`** appended to every image prompt.
- Change **only** pose, camera, background beat, or prop state between start and end — not character species, face, uniform, or art medium mid-scene.
- **Physically reachable end state** — the end still must be somewhere the subject could plausibly reach from the start still in one continuous clip. **Share geometry** between plates when possible (same doorway, same vehicle, same room) — e.g. elevator doors closed → same elevator doors open onto a terrace, not elevator interior → unrelated rooftop portrait.

## Video phase — physical transitions

The **`video_prompt`** describes **how** the subject and camera move from start → end. It is not a redescription of the stills. Each OPEN / MID / CLOSE segment must pass the [Details Law](./prompt-dramaturgy.md#details-law-non-negotiable). Physics tier: [physics-safe-motion.md](./physics-safe-motion.md) (Tier A when both stills support travel).

| Rule | Why |
|------|-----|
| **Same subject throughout** | Name the subject in OPEN / MID / CLOSE ("same bellhop", "same red panda") — the model drops characters easily if the prompt only describes scenery. |
| **One continuous camera path** | Pick one move (dolly, track, crane, pan) and hold it — no sudden angle jumps mid-clip. |
| **Camera faces the action** | If the start still is eye-level portrait, keep shoulder-height tracking — don't jump to aerial unless the end still is aerial. |
| **Motion matches the world** | Doors open before walking through; subject walks forward to reach a terrace; steam rises before a dissolve — cause then effect. |
| **OPEN → MID → CLOSE timing** | OPEN: brief hold (1–2s). MID: bulk of travel/morph (most of the clip). CLOSE: settle on end pose (1–2s). |
| **Duration** | Prefer **8–10s** for character transitions; **5–8s** for simple camera moves on landscapes. Rushed 4–5s clips morph abruptly. |
| **No teleport / empty room** | Ban "cut to", "suddenly in", "walls disappear instantly" — use "gradually", "walks through", "ease into". |

Example **`video_prompt`** (character exits a space):

```text
OPEN: bellhop inside elevator, doors closed, brief hold.
MID: doors slide open once and stay open, same bellhop walks forward through the doorway onto the terrace, no teleport.
CLOSE: he stops on terrace tiles, fully outside, open doors behind him.
```

Bad example (doors close, subject teleports):

```text
OPEN: elevator interior. MID: doors close. CLOSE: bellhop suddenly on rooftop.
```

### Exiting a container (elevator, doorway, vehicle)

When a character **leaves** a space, do **not** pair interior and exterior shots with different cameras. `p-video` morphs pixels between plates — it will often **close the container with the subject inside**, then **open it with the subject already outside**.

| Bad pairing | Why it breaks |
|-----------|----------------|
| Inside elevator (front) → on terrace (front) | Different rooms; model closes doors to match start, then jumps to end |
| Over-the-shoulder inside → front view outside | Camera flip mid-clip |
| End still = empty terrace POV from elevator | Subject edited out; video fills with door animation only |

**Fix: fixed exterior camera** looking at the container:

| Plate | Content |
|-------|---------|
| **Start** | Terrace-side view, **doors closed**, subject **visible inside** through doors |
| **End** | **Same camera**, doors **open**, subject **on terrace tiles** in front of elevator |
| **Video** | Doors open **once** → subject **steps forward out** → stop on tiles. Doors **never close again**. |

```text
OPEN: fixed terrace camera, closed elevator doors, bellhop visible inside.
MID: doors open and stay open, same bellhop walks out onto terrace tiles.
CLOSE: stands in front of open elevator, match end pose.
```

After **all** start and end URLs exist for every scene row:

- **`POST /v1/predictions`** with `Model: p-video` — **parallel** when scenes are independent
- **`video_prompt`** uses OPEN → MID → CLOSE structure (motion only) — see [Video phase — physical transitions](#video-phase--physical-transitions)
- Optional **`draft: true`** on the full chain for cheap motion approval, then rerun finals at **1080p**, **`draft: false`**, **8–10s** for character beats

- Pass `duration`; omit `audio` (visual-only). Payload fields: `p-video` skill.

## Frame chain (multi-scene continuity)

Decision tree, prompt rules, and assembly: **[clip-chaining.md](./clip-chaining.md)**. Summary: chain only when motion continues (same place/moment); prefer `extract_last_frame`; hard-cut new beats.

| Situation | `chain_from_previous` | Join style |
|-----------|----------------------|------------|
| Continuous action (run → leap) | `true` | Short crossfade (~0.12–0.15s) after extract |
| New beat / location / pause | `false` | Hard cut — composed OPENING still |
| First scene | `false` | — |

| `frame_chain_mode` | Next scene `image` when chained | Render order |
|--------------------|---------------------------------|--------------|
| **`extract_last_frame`** | ffmpeg last frame from prior clip | **Sequential** when any scene chains |
| **`parallel_vignettes`** | each scene uses its own start still | **Parallel** — hard cuts between vignettes |
| **`planned_stills`** | prior scene end still URL | **Parallel** once all stills exist |

```text
Scene 1: start_1 → end_1   duration=5   chain→2
Scene 2: extract(clip_1) → end_2   duration=4   hard cut→3
Scene 3: start_3 → end_3   duration=5
```

## Assembly

1. **Concat** clips in scene order via `stable-audio-2.5` mixed under native SFX (~0.08–0.15 volume)

## Pair vs triple

| Pattern | Anchors | Duration | Workflow |
|---------|---------|----------|----------|
| **Pair** | `image` + `last_frame_image` + `prompt` | `duration` | `visual-transition-reel` |
| **Triple** | pair + `audio` | follows audio | `narrated-multi-scene` |

Upgrade a pair scene to triple by adding TTS → upload → `audio` and removing `duration`.

## Plan JSON shape

```json
{
  "title": "Neon alley handoff",
  "hero_prompt": "Cinematic cyberpunk alley, single subject, 16:9 one frame",
  "ritual_seed": "k7Qm2xP9",
  "frame_chain_mode": "extract_last_frame",
  "assembly": {
    "chain_crossfade_seconds": 0.15,
    "hard_cut_crossfade_seconds": 0
  },
  "defaults": {
    "resolution": "720p",
    "fps": 24,
    "aspect_ratio": "16:9",
    "duration_seconds": 5
  },
  "style_bible": "Neon magenta cyan, wet pavement reflections, cinematic 16:9",
  "scenes": [
    {
      "id": "01_alley",
      "chain_from_previous": false,
      "duration_seconds": 5,
      "edit_prompt": "OPENING: Wide alley, figure small in frame, neon kanji",
      "last_frame_edit_prompt": "CLOSING: Same alley, figure closer, hand on railing",
      "video_prompt": "OPEN: hold wide. MID: slow dolly in. CLOSE: settle on end pose."
    },
    {
      "id": "02_rooftop",
      "chain_from_previous": true,
      "duration_seconds": 4,
      "edit_prompt": "OPENING: Rooftop edge, city sprawl, figure turns toward camera",
      "last_frame_edit_prompt": "CLOSING: Same rooftop, figure mid-step toward ledge",
      "video_prompt": "OPEN: wind ripples coat. MID: figure turns. CLOSE: step forward — hold."
    }
  ]
}
```

## Intake checklist (per scene)

- [ ] `edit_prompt` — OPENING still (from hero or upload)
- [ ] `last_frame_edit_prompt` — CLOSING still (from start still)
- [ ] `video_prompt` — OPEN / MID / CLOSE **motion** between the two plates
- [ ] `duration_seconds` (or global default)
- [ ] `chain_from_previous` — only if motion truly continues from prior clip
- [ ] `resolution` / `fps` / `draft` policy

## Workflows that implement this

- `visual-transition-reel` — primary workflow
- `image-to-video` — one pair beat
- `p-video` — API reference (visual transition mode)
- Workflow runner: agent follows `visual-transition-reel` (curl + ffmpeg)
