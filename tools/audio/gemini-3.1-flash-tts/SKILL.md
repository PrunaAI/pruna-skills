---
name: gemini-3.1-flash-tts
description: Generates narration and voiceover via Replicate google/gemini-3.1-flash-tts (30 voices, style prompts, inline tags). Upload to Pruna as input.audio in the scene anchor triple (image + last_frame_image + audio) on p-video or p-video-avatar.
license: MIT
metadata:
  version: "0.0.1"
  provider: replicate
  replicate_model: google/gemini-3.1-flash-tts
---

# Gemini 3.1 Flash TTS (Replicate)

Natural **text-to-speech** with style control via a director **`prompt`** and inline **`[tags]`** in the spoken text. Not a Pruna P-model — runs on [Replicate](https://replicate.com/google/gemini-3.1-flash-tts).

**Typical downstream (preferred):** upload MP3/WAV to Pruna `/v1/files` → pass as **`input.audio`** with **`input.image`** and **`input.last_frame_image`** on [`p-video`](../../video/p-video/SKILL.md) ([scene anchor triple](../../../references/scene-anchor-triple.md)). Same upload pattern on [`p-video-avatar`](../../video/p-video-avatar/SKILL.md) for lip-sync narration.

For **narration + instrumental bed**, render video with embedded VO first, then mix bed in post — [audio-post-production.md](../../../references/audio-post-production.md).

## When to use

| Goal | Use this |
|------|----------|
| Documentary / story narrator over B-roll | Yes — per-scene or full-reel script |
| Character dialogue in a talking head | No — use [`p-video-avatar`](../../video/p-video-avatar/SKILL.md) native voice |
| Full sung song | No — use [music-2.5](../music-2.5/SKILL.md) |
| Instrumental mood bed only | No — use [stable-audio-2.5](../stable-audio-2.5/SKILL.md) |
| Lip-sync from uploaded VO | Upload TTS → [`p-video`](../../video/p-video/SKILL.md) with `audio` (duration follows audio) |

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

Shared client: [`replicate_api.py`](../../../guides/workflows/_shared/scripts/replicate_api.py).

## Multi-scene narration patterns

| Pattern | When | Steps |
|---------|------|-------|
| **Per-scene VO → scene anchor triple** (**preferred**) | Story B-roll | TTS → upload → `p-video` with `image` + `last_frame_image` + `audio` — [scene-anchor-triple.md](../../../references/scene-anchor-triple.md) |
| **Per-scene VO → `p-video-avatar`** | Talking-head narration | TTS or script → upload → `p-video-avatar` with portrait + `audio` |
| **Per-scene VO → post mux** | Fallback: silent clips already rendered | TTS per scene → concat → ffmpeg mux (may truncate long lines) |
| **One continuous narrator track** | Single voice-over bed for whole reel | TTS full script once → mux under concat with [`launch_background_music.py`](../../../guides/workflows/_shared/scripts/launch_background_music.py)-style `amix` (narration = primary stream) |
| **Narration + instrumental bed** | Story film with music | TTS + [stable-audio-2.5](../stable-audio-2.5/SKILL.md) bed → mix narration loud, bed quiet (~0.08–0.15) — see [audio-post-production.md](../../../references/audio-post-production.md) |

Record **`voice`**, **`prompt`**, and **`language_code`** in the project manifest for consistency across scene regens.

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

- [scene-anchor-triple.md](../../../references/scene-anchor-triple.md) — **`image` + `last_frame_image` + `audio`** per scene
- [audio-post-production.md](../../../references/audio-post-production.md) — narration + bed layering
- [multi-scene-ai-video](../../../guides/workflows/multi-scene-ai-video/SKILL.md) — scene table + assembly
- [stable-audio-2.5](../stable-audio-2.5/SKILL.md) — instrumental beds
- [music-2.5](../music-2.5/SKILL.md) — full songs with vocals
- [replicate-api.md](../../../references/replicate-api.md)
