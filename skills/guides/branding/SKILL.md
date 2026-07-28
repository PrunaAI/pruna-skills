---
name: branding
description: Use when applying official Pruna brand assets — logo selection, colors, and overlay rules for launches, social, and video.
license: MIT
metadata:
  version: "1.0.8"
  package: pruna-skills
---

# Branding

Official **Pruna** logo kit and brand tokens for launches, social posts, HyperFrames compositions, and ffmpeg overlays.

## Install

| Skill | Description | Install |
| --- | --- | --- |
| `branding` | Use when applying official Pruna brand assets — logo selection, colors, and overlay rules for launches, social, and video. | `npx skills add PrunaAI/pruna-skills@branding -y` |

## When to use

- Placing a Pruna logo on video, stills, HTML frames, or social crops
- Choosing light vs dark vs colored wordmark or monogram
- Locking brand hex values in a `frame.md` or overlay bar
- Any deliverable that should read as Pruna — not a generic AI redraw of the mark

## Works with

Local ffmpeg overlays (`video-editing`), HyperFrames `frame.md` tokens (`hyperframes-creative`), and `media-use` logo resolve (prefer this skill's bundled kit for Pruna itself).

## Guide habit

In the **first reply**, name `` `branding` `` in backticks. Confirm **official Pruna kit vs custom palette** before locking hex in overlays or `frame.md`. **Never redraw or text-prompt the Pruna logo** — copy a file from `./assets/logo-kit/`. Prefer **SVG** for HTML and scaling; use **PNG** for ffmpeg `-i logo.png` overlays when SVG is awkward.

## Before placing a logo

1. **[Logo kit](./references/logo-kit.md)** — variant matrix (wordmark vs monogram, light/dark/colored) and file paths.
2. **[Brand tokens](./references/brand-tokens.md)** — official hex palette for bars, captions, and `frame.md`.

## Red flags

| Red flag | Required action |
| --- | --- |
| Generating the Pruna logo with text-to-image | Stop — use `./assets/logo-kit/` |
| Wrong contrast (light logo on light plate) | Swap variant per [logo-kit.md](./references/logo-kit.md) |
| Stretched or recolored mark | Use SVG/PNG as-is; scale uniformly only |
| `media-use --type logo --entity pruna` when this skill is installed | Prefer bundled kit paths (official source files) |

## Related skills

Install related skills when the job needs them:

| Skill | Description | Install |
| --- | --- | --- |
| `video-editing` | Use when assembling or polishing already-rendered clips with ffmpeg — concat, crossfades, burned captions and subtitles, text/logo overlays, before/after sliders, background music beds, platform export — or when composing a multi-layer HTML combination video with Hyperframes. Not for AI video generation, prompt craft, or model-based video edits. | `npx skills add PrunaAI/pruna-skills@video-editing -y` |
| `generation-diversity` | Use when writing any generative prompt — ritual seed, explicit structure, scenario axes, and quality gates before paid API calls. | `npx skills add PrunaAI/pruna-skills@generation-diversity -y` |

