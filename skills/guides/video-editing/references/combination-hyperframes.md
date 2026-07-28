# Combination videos (Hyperframes)

Optional path for **designed multi-layer videos** — chat UI mocks, kinetic type, multi-panel grids, product montages. Not a linear ffmpeg concat.

**External project:** [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) — install their agent skills; do not copy Hyperframes craft into Pruna skills.

Before building: resolve open decisions via **`generation-diversity`** clarification intake and, when HyperFrames is installed, **`hyperframes`** clarification-before-build reference (generate vs existing assets, palette, VO, music, captions, canvas 720/1080).

## When to use Hyperframes

- Product or feature promo with designed frames and UI chrome
- Beat-synced kinetic layouts that are awkward in raw ffmpeg filter graphs
- Multi-scene montages where each “scene” is a full HTML layout (not just a clip cut)

## When to stay on ffmpeg (this guide)

- Simple clip concat or crossfade
- Post-render caption burn on a **plain** clip (no HTML composition) → [captions.md](./captions.md)
- Bed under VO on a finished render → [background-music.md](./background-music.md)
- Aspect export and loudness normalization → [export-presets.md](./export-presets.md)

---

## Core pattern — render, then polish

Split responsibilities:

| Phase | Tool | Output |
|-------|------|--------|
| **1. Compose + render** | HyperFrames (HTML → MP4) | Motion, visuals, embedded audio — **no burned captions** |
| **2. Post-render polish** | ffmpeg (+ `whisperx` when captions needed) | Captions, optional bed remix, crop, loudnorm |

Do **not** ffmpeg-concat the main deliverable when it needs UI chrome — use HyperFrames scenes instead.

**Why two phases:** caption style, placement, and bed level iterate faster on a finished MP4 than by re-rendering the HTML composition. Social platforms need **burned-in** subs; HyperFrames’ embedded-caption path is for preview/HTML export, not the default promo deliverable.

```text
HyperFrames: npm run check && npm run render  →  render.mp4
whisperx on narration source (isolated VO)     →  word JSON
phrase-bar + word-accent ASS                   →  captioned.mp4   (see captions.md)
optional: amix bed under captioned render      →  final.mp4       (see background-music.md)
```

---

## 1. Spec before pixels

Write a short spec (acts, target duration, VO lines, on-screen beats) **before** authoring HTML. For **design language, act patterns, instructional beats, and motion habits** (vendor-neutral, open on layout), read [motion-composition-craft.md](./motion-composition-craft.md).

Example skeleton (adapt act count and labels to the brief):

| Act | Time (example) | Visual | VO |
|-----|----------------|--------|-----|
| Hook | 0–5s | Title + hero visual | Opening line |
| Explain or demo | 5–20s | Steps, flow, or UI mock | What to do / how it works |
| Evidence | 20–35s | Examples or grid | Proof or samples |
| Close | 35–45s | Logo + link / command | One clear action |

Lock root **`data-duration`** to **actual narration length + tail** — not the first draft estimate. Mismatch causes black frames, cut-off VO, or misaligned captions.

Generate VO **before** scene timing so `data-start` / `data-duration` match real speech.

---

## 2. Project layout (generic)

```text
<project>/
├── spec.md                 # acts, VO script, asset list (human notes)
├── hyperframes/
│   ├── index.html          # seekable composition — no caption burn
│   ├── package.json        # pinned hyperframes CLI scripts
│   ├── hyperframes.json    # assets path, autoProxy
│   └── assets/             # narration, demo clips, stills, optional bed
├── audio/
│   └── narration_full.mp3  # whisperx source (keep even if also in assets/)
├── captions/               # post-render: transcript, ASS, burn outputs
└── render.mp4              # copy from hyperframes/renders/
```

Reuse existing demo media where possible — do not regenerate every tile for a promo reel.

Portrait **workflow demo** reels: suggested act order, full-length output clip, optional intro, CTA, bar, and logo. See [social-usecase-reel.md](./social-usecase-reel.md) for structure; visuals there are example proposals only.

---

## 3. Install HyperFrames skills (agents)

Optional — only for combination / launch-reel deliverables. Not in `@pruna`. Install and load before composing (skip if already in context):

| Skill | Description | Install |
| --- | --- | --- |
| `hyperframes` | Entry point for HTML → MP4 composition — routes to product-launch-video, general-video, and related workflows. | `npx skills add heygen-com/hyperframes@hyperframes -y` |

Full HyperFrames bundle (all domain skills): `npx skills add heygen-com/hyperframes --full-depth -y`

Read **`hyperframes`** first — it routes to `/product-launch-video`, `/general-video`, etc., and installs owning workflows on demand (same idea as a Pruna workflow pulling its tool prerequisites).

**Maintainers** of this repo: `make install-companion-skills` copies the full bundle into gitignored `.agents/skills/`.

---

## 4. Composition basics

Root composition:

```html
<div id="root" data-composition-id="main" data-duration="45" data-width="1920" data-height="1080">
```

Use **`class="clip"`** with `data-start`, `data-duration`, `data-track-index` on every timed layer:

| Track range | Typical layer |
|-------------|----------------|
| `0` | Background |
| `1–N` | Scenes (hook → CTA) |
| `10–11` | Narration (+ optional bed audio) |
| higher | Overlays — **not** social captions (see §6); brand **logo** watermark (full timeline, track ~95) |

Scenes are full-bleed `<div class="scene clip">` blocks; nested `<video class="clip">` for demo tiles.

Register seek-safe motion on `window.__timelines["main"]` (GSAP `paused: true`). Prefer **step eases** for typing and **clip-path reveals** for UI — deterministic on seek/render.

When you adopt a look, **consistency** helps: carry the same background, accent, and fonts through CSS for the composition. Match caption accent colour in post-render ASS if using word highlight (see [captions.md](./captions.md)). Token choices themselves come from the brief or brand guide, not this doc.

---

## 5. Audio — narration-first

| Track | Typical source | HyperFrames pattern |
|-------|----------------|---------------------|
| **Narration** | TTS (`gemini-3.1-flash-tts`) or recorded VO | `<audio class="clip" data-volume="1" src="assets/narration_full.mp3">` starting at **t=0** |
| **Bed** (optional) | Reuse instrumental or `stable-audio-2.5` | See embed vs post-mux below |

**Narration at t=0:** the rendered MP4 timeline must match the standalone narration file used for whisperx. If VO is delayed inside the composition, caption timestamps will drift unless you offset ASS or re-align on the mux (last resort).

### Bed — embed in HTML or mux after captions

| Approach | When | Tradeoff |
|----------|------|----------|
| **Embed** bed in HyperFrames (`data-volume` ~0.10–0.20 vs narration) | One render, bed locked to motion | whisperx must use **narration only**, not the rendered mux — bed can mask quiet VO |
| **Post-mux** bed after caption burn (`-c:v copy`) | Caption iteration, bed level tweaks | Extra ffmpeg step; render can be VO-only for a cleaner alignment source |

Default for promo reels with karaoke-style captions: **VO in HyperFrames render → burn captions → amix bed** ([background-music.md](./background-music.md)). Embed the bed when you will not iterate captions or bed level.

Bed prompt craft: `audio-prompting`.

---

## 6. Post-render polish

HyperFrames output is **never** the final social deliverable when captions are required.

### Captions

1. Run **whisperx** on **`narration_full.mp3`** (or the same isolated VO track embedded in the render) — **not** the bed-heavy master unless narration-only is unavailable.
2. Build **phrase-bar + word-accent ASS** from word JSON ([captions.md](./captions.md)).
3. Burn with **`ffmpeg-full`** (`ass=` filter — default Homebrew ffmpeg often lacks libass).

Regenerate phrase **SRT cues from the whisperx transcript** when building ASS — stale or hand-edited SRT with wrong timestamp units silently drops or merges cues.

Do **not** add subtitle `<div>` clips in `index.html` **and** post-burn captions — double subs and slower iteration.

### Optional bed remix

After burn-in, mux bed with `-c:v copy` so video (including captions) is not re-encoded:

```bash
ffmpeg -y -i captioned.mp4 -i bed.mp3 \
  -filter_complex "[1:a]volume=0.12,aloop=loop=-1:size=2e+09[bed];[0:a][bed]amix=inputs=2:duration=first:dropout_transition=2[aout]" \
  -map 0:v -map "[aout]" -c:v copy -c:a aac -b:a 192k -shortest final.mp4
```

### Export

Platform crop / loudnorm → [export-presets.md](./export-presets.md).

---

## 7. Dev loop (pinned CLI)

Pin HyperFrames in `package.json` for reproducible renders:

```json
"scripts": {
  "check": "npx --yes hyperframes@0.7.68 check",
  "render": "npx --yes hyperframes@0.7.68 render"
}
```

```bash
cd hyperframes
npm run dev      # preview — long-running; keep alive in background
npm run check    # lint + runtime + layout + motion — run before every render
npm run render   # → hyperframes/renders/hyperframes_*.mp4
cp hyperframes/renders/hyperframes_*.mp4 ../render.mp4
```

**Always `check` before `render`.** Preview with `npm run dev` when tuning GSAP timing against VO.

---

## 8. Generative handoff (typical promo)

| Phase | Skill | Output |
|-------|-------|--------|
| VO | `gemini-3.1-flash-tts` | `audio/narration_full.mp3` |
| Bed | reuse or `stable-audio-2.5` | `bed.mp3` |
| Demo tiles | existing assets or video/image tools | `assets/*` |
| Assembly | HyperFrames (`/hyperframes`, `/product-launch-video`) | `index.html` → MP4 (caption-free) |
| Captions | `whisperx` + [captions.md](./captions.md) | ASS → ffmpeg burn |
| Polish | [background-music.md](./background-music.md), [export-presets.md](./export-presets.md) | final deliverable |

---

## 9. Anti-patterns

| Mistake | Fix |
|---------|-----|
| whisperx on the final mux with loud bed | Align on **isolated narration** |
| Subtitle layers in HTML + post-render burn | HTML render stays caption-free |
| ffmpeg concat for chat/terminal UI | HyperFrames scenes |
| Skip `npm run check` | Catches seek/layout issues before slow render |
| `data-duration` ≠ VO + tail | Measure narration; add hold on last frame |
| Stale SRT with wrong comma decimals | Regenerate cues from whisperx JSON |
| Default ffmpeg for ASS burn | Install **ffmpeg-full** (libass) |
| Copy HyperFrames docs into Pruna skills | `npx skills add heygen-com/hyperframes@hyperframes -y` |
| Clone another reel’s scene order for a different brief | Re-spec using [motion-composition-craft.md](./motion-composition-craft.md) |
| Truncate demo `<video>` with short `data-duration` | Probe file; set duration to full clip ([social-usecase-reel.md](./social-usecase-reel.md)) |

---

## Requirements

- Node.js **22+**
- **FFmpeg** (HyperFrames render + post-pass; **ffmpeg-full** for caption burn)
- Media on disk (clips, stills, VO, optional bed)

## Typical next steps after render

- **Burned captions** (promo default) → [captions.md](./captions.md)
- Bed under captioned VO → [background-music.md](./background-music.md)
- Platform crop / loudnorm → [export-presets.md](./export-presets.md)
