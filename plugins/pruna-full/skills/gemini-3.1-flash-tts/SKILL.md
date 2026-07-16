---
name: gemini-3.1-flash-tts
description: Use when someone needs spoken narration or voiceover — explainer tracks, documentary lines, or voice to pair with generated video.
license: MIT
metadata:
  version: "1.0.6"
  provider: replicate
  replicate_model: google/gemini-3.1-flash-tts
---

## Shared generation policy

<!-- shared-generation-policy -->

Before any paid `POST /v1/predictions`:

1. **[Random seed ritual](./references/random-seed-ritual.md)** — always first; derive axes via sum-mod.
2. **[Generation diversity](./references/generation-diversity.md)** — explicit prompts; rotate ≥2 scenario axes per session.
3. **[Quality checklists](./references/generation-quality-checklists.md)** — open output files and judge pass/fail before advancing.

# Gemini 3.1 Flash TTS (Replicate)

Natural **text-to-speech** with style control via a director **`prompt`** and inline **`[tags]`** in the spoken text. Not a Pruna P-model — runs on [Replicate](https://replicate.com/google/gemini-3.1-flash-tts).

**Typical downstream (preferred):** upload MP3/WAV to Pruna `/v1/files` → pass as **`input.audio`** with **`input.image`** and **`input.last_frame_image`** on [`p-video`](../p-video/SKILL.md) ([scene anchor triple](./references/scene-anchor-triple.md)). Same upload pattern on [`p-video-avatar`](../p-video-avatar/SKILL.md) for lip-sync narration.

For **narration + instrumental bed**, render video with embedded VO first, then mix bed in post — [audio-post-production.md](./references/audio-post-production.md).

## When to use

| Goal | Use this |
|------|----------|
| Documentary / story narrator over B-roll | Yes — per-scene or full-reel script |
| Character dialogue in a talking head | No — use [`p-video-avatar`](../p-video-avatar/SKILL.md) native voice |
| Full sung song | No — use [music-2.5](../music-2.5/SKILL.md) |
| Instrumental mood bed only | No — use [stable-audio-2.5](../stable-audio-2.5/SKILL.md) |
| Lip-sync from uploaded VO | Upload TTS → [`p-video`](../p-video/SKILL.md) with `audio` (duration follows audio) |

## Environment

```bash
export REPLICATE_API_TOKEN=r8_...
```

Requires **`ffmpeg`** / **`ffprobe`** when trimming, concatenating scene VO, or mixing with a bed.

## Model input (Replicate)

| Field | Notes |
|-------|-------|
| `text` | **Required.** Spoken copy; supports inline `[tags]`. Max ~4,000 bytes. |
| `voice` | One of 30 preset voices (default `Kore`). See [voice table](#voices). |
| `prompt` | Style / scene / director notes — tone, pace, accent, character. Max ~4,000 bytes. |
| `language_code` | BCP-47 (default `en-US`). Set explicitly for non-English. |

Combined `text` + `prompt` ≤ ~8,000 bytes. Output is capped at ~655 seconds.

## Style prompting

Align **`prompt`**, **`text`**, and any **`[tags]`** — all should point the same emotional direction.

**Example prompt:**

```text
AUDIO PROFILE: Warm documentary narrator, gentle and empathetic.

THE SCENE: A short nature film about a dog who loses a favorite toy.

DIRECTOR'S NOTES:
- Style: Soft, curious, slightly playful — like a children's storybook read aloud.
- Pace: Unhurried; leave room for visuals to breathe.
- Do not sound like a hard-sell announcer.
```

**Example text:**

```text
[warmly] Every afternoon, the meadow was theirs.
[short pause] But today, something small went missing.
[concerned] And for the first time, the world felt a little too big.
```

## Inline tags

| Tag | Effect |
|-----|--------|
| `[sigh]` `[laughing]` `[uhm]` | Non-speech vocalizations |
| `[whispering]` `[shouting]` `[sarcasm]` `[robotic]` `[extremely fast]` | Delivery modifiers for following text |
| `[short pause]` `[medium pause]` `[long pause]` | Silence (~250ms / ~500ms / ~1000ms+) |
| `[excitedly]` `[bored]` `[reluctantly]` etc. | Descriptive tags — test before production |

## Voices (common picks)

| Voice | Gender | Character | Good for |
|-------|--------|-----------|----------|
| `Kore` | Female | Firm | Default narrator |
| `Aoede` | Female | Breezy | Light documentary |
| `Sulafat` | Female | Warm | Storybook / emotional beats |
| `Achird` | Male | Friendly | Casual explainer |
| `Charon` | Male | Informative | Product / tech VO |
| `Puck` | Male | Upbeat | Short social hooks |
| `Vindemiatrix` | Female | Gentle | Soft narration under music |

Full list: [Replicate readme](https://replicate.com/google/gemini-3.1-flash-tts/readme).

## HTTP (curl)

```bash
curl -s -X POST \
  -H "Authorization: Bearer ${REPLICATE_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "text": "[warmly] The plush went flying. [short pause] And then it was gone.",
      "voice": "Sulafat",
      "prompt": "Warm storybook narrator, gentle pace, empathetic, no announcer voice.",
      "language_code": "en-US"
    }
  }' \
  "https://api.replicate.com/v1/models/google/gemini-3.1-flash-tts/predictions"
```

Poll `urls.get` until `status` is `succeeded`; download `output` (audio URL).

Shared client: [`replicate_api.py`](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/_shared/scripts/replicate_api.py).

## Multi-scene narration patterns

| Pattern | When | Steps |
|---------|------|-------|
| **Per-scene VO → scene anchor triple** (**preferred**) | Story B-roll | TTS → upload → `p-video` with `image` + `last_frame_image` + `audio` — [scene-anchor-triple.md](./references/scene-anchor-triple.md) |
| **Per-scene VO → `p-video-avatar`** | Talking-head narration | TTS or script → upload → `p-video-avatar` with portrait + `audio` |
| **Per-scene VO → post mux** | Fallback: silent clips already rendered | TTS per scene → concat → ffmpeg mux (may truncate long lines) |
| **One continuous narrator track** | Single voice-over bed for whole reel | TTS full script once → mux under concat with [`launch_background_music.py`](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/_shared/scripts/launch_background_music.py)-style `amix` (narration = primary stream) |
| **Narration + instrumental bed** | Story film with music | TTS + [stable-audio-2.5](../stable-audio-2.5/SKILL.md) bed → mix narration loud, bed quiet (~0.08–0.15) — see [audio-post-production.md](./references/audio-post-production.md) |

Record **`voice`**, **`prompt`**, and **`language_code`** in the project manifest for consistency across scene regens.

## Duration limit (scene anchor triple)

When TTS feeds **`p-video`** as `input.audio`, clip length follows the MP3 but **cannot exceed 20 seconds** on P-API. After each scene file is downloaded:

1. Run `ffprobe` (or [`probe_media_duration_seconds`](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/_shared/scripts/p_video_payload.py)) on the MP3.
2. Keep each line **≤ ~19 seconds** — shorten copy or split into two scenes if over.
3. Upload to Pruna and pass as `input.audio` with `image` + `last_frame_image`; omit `duration`.

Truncated narration mid-sentence usually means the line exceeded the cap, not that audio was omitted from the prediction.

**If `ffprobe` > ~19s:** shorten the `text` first; if still long, add *brisk pace, ~2.3 words per second, no filler* to `style_prompt` and regenerate; if two beats remain, split into two scenes in the plan (separate TTS files).

## Plan JSON (`narration`)

```json
"narration": {
  "enabled": true,
  "voice": "Sulafat",
  "language_code": "en-US",
  "style_prompt": "Warm storybook narrator, gentle pace, empathetic.",
  "mode": "per_scene",
  "scenes": {
    "01_playtime": {
      "text": "[warmly] This was their favorite game."
    },
    "02_toss": {
      "text": "[excitedly] Up it went — higher than ever."
    }
  }
}
```

`mode`: `p_video_audio` (**preferred** — scene anchor triple) | `per_scene` | `full_reel`

## Related

- [scene-anchor-triple.md](./references/scene-anchor-triple.md) — **`image` + `last_frame_image` + `audio`** per scene
- [audio-post-production.md](./references/audio-post-production.md) — narration + bed layering
- [narrated-multi-scene](../narrated-multi-scene/SKILL.md) — scene table + assembly
- [stable-audio-2.5](../stable-audio-2.5/SKILL.md) — instrumental beds
- [music-2.5](../music-2.5/SKILL.md) — full songs with vocals
- [replicate-api.md](https://github.com/PrunaAI/pruna-skills/tree/main/references/policies/replicate-api.md)
