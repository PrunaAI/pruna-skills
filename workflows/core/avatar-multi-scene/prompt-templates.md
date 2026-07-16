# Prompt templates (Pruna only)

Companion to [avatar-multi-scene/SKILL.md](./SKILL.md) — cast ledger, character sheet, still edits, and per-scene voice/video fields.

## Cast ledger (voice lock)

| Character | Pruna `voice` | `voice_language` | Notes |
|-----------|----------------|------------------|--------|
| (example) | `Zephyr (Female)` | `English (US)` | Same preset every scene this character speaks |

**Rule:** recurring characters **never** change `voice` between scenes unless the user requests a recast. Tweak delivery with **`voice_prompt`** only.

## Reference gathering (research assistant prompt)

```text
Collect up to [N] high-quality, rights-clear reference images for [SUBJECT / CAST].
Prefer official art packs, style guides, or assets the client can license.
For each file record: character, intended use, source, license note, and image quality (resolution, clarity).
```

## Upload rule

Use **`POST /v1/files`** and then Pruna **`urls.get`** values in **`p-image-edit`** `images` and in **`p-video-avatar`** `image`. Do not pass arbitrary hotlinks you do not control.

## Character sheet (fill before hero generation)

```text
Name/role: [e.g. Alex — founder spokesperson]
Age/build: [early 30s, medium build]
Face/hair: [short dark hair, light stubble, brown eyes]
Realism: photorealistic documentary portrait, not CGI, not illustration
Wardrobe baseline: [black crew-neck — keep unless scene script changes outfit]
Personality: [warm, direct, founder-energy, honest]
ritual_seed: [string — SSoT planning only; generate fresh, do not copy examples]
Pruna voice: [e.g. Puck (Male)] / [English (US)]
```

## Scene table (fill during intake — every row must differ)

| # | Setting & camera | Emotion | still_prompt delta (change only) |
|---|------------------|---------|----------------------------------|
| 1 | extreme close-up, dark void | curious hook | (hero — no edit) |
| 2 | 3/4, outdoor location | contemplative | background + angle |
| 3 | medium low-angle, distinctive set | excited reveal | background + angle |
| 4 | over-shoulder at desk | conversational proof | setting + angle |
| 5 | straight-on medium studio | warm CTA | cleaner background |

Pair each row with its own **`voice_script`**, **`voice_prompt`**, and **`video_prompt`** in the manifest JSON.

## Ritual seed (manifest snippet)

```json
{
  "ritual_seed": "k7Qm2xP9",
  "ritual_seed_policy": "ssot_dag_before_every_generation",
  "api_seed": null
}
```

`ritual_seed` is **SSoT planning only** — do not pass to API `input.seed`. Set `api_seed` only when the user explicitly locks API reproducibility.

Replace strings with your [random seed ritual](../../../../../references/shared/random-seed-ritual.md) — do not copy from this template.

**Ritual:** [random-seed-ritual.md](../../../../../references/shared/random-seed-ritual.md) (SSoT) — generate a random string before every generation; derive prompt axes via sum-mod.

## Fashion / ecommerce try-on path

When the deliverable is **dressed model stills** or **fashion UGC avatar**:

1. **`p-image`** photoreal editorial plate → slop gate — [realistic-persona-showcase.md](../../../../../references/shared/realistic-persona-showcase.md)
2. **`p-image-try-on`** with garment refs (normal mode for complex stacks) — [p-image-try-on-quality-checklist.md](../../../../../references/image/p-image-try-on-quality-checklist.md)
3. Optional **`p-image-upscale`** → slop gate → **`p-video-avatar`** with **unique `video_prompt`** and natural **`voice_script`**

Lock **hero plate URL** from step 1 through step 3. Plan cast diversity for public example sets per [visual-variety-bible.md](../../../../../references/shared/visual-variety-bible.md).

## Style bible (paste into every image prompt)

```text
Style lock: [2-4 sentences: medium, line quality, palette, lighting, camera era].
Same character as reference: [identity anchors: species, age, outfit, iconic props].
```

## p-image: new still from text (when you lack a photo reference)

```text
[Style bible]
Vertical 9:16 talking-head portrait, [CHARACTER] in [SETTING], shoulders toward camera,
hands low in frame, face large and centered, mouth clearly visible for speech animation,
neutral relaxed expression ready to speak.
```

## p-image: photoreal hero (preferred for avatar pipelines)

```text
Photorealistic documentary portrait photograph of a real person, not CGI, not 3D render.
[Character sheet: age, hair, wardrobe, personality visible in expression]
Natural skin with pores and subtle imperfections. Shot on 85mm lens, shallow depth of field.
[Setting for scene 1 only]. 16:9 talking-head, face centered, mouth clearly visible mid-speech.
No text, no logos.
```

After hero succeeds: run slop gate on the hero output → approve anchor.

## p-image-edit: match reference, change only what the scene needs

```text
[Style bible]
Using the attached reference(s) as identity, produce a vertical 9:16 talking-head frame for scene [N]: [POSE / EMOTION / BACKGROUND CHANGE ONLY].
Keep face, species, and costume on-model; mouth unobstructed; no new text or logos in frame.
```

Use 1–5 **`images`** URLs per the [p-image-edit](../../../../tools/image/p-image-edit/SKILL.md) skill. Reuse the **hero** URL in every edit that must stay on-model.

## p-video-avatar: JSON field names (snake_case)

| Field | Role |
|--------|------|
| `image` | Still URL from `/v1/files` or prior delivery URL your pipeline trusts |
| `voice_script` | Exact spoken words for this clip |
| `voice` | Pruna voice preset (see model doc list) |
| `voice_language` | e.g. `English (US)` |
| `voice_prompt` | Short performance direction only (not script text) |
| `video_prompt` | Shot motion: framing, energy, head motion—positive wording only |
| `resolution` | `720p` or `1080p` |

## p-image-edit: per-scene still (avatar rows)

```text
Using the attached reference(s) as identity — keep exact same person, face, skin texture, photorealistic quality.
Change only: [ANGLE], [BACKGROUND/SETTING], [EXPRESSION]. [Character sheet wardrobe baseline unless scripted change].
16:9, mouth clearly visible, ready to speak. No text, no logos.
```

Run slop gate on the edit output before **`p-video-avatar`**. Pass the approved still URL from `/v1/files`.

Use 1–5 **`images`** URLs per the [p-image-edit](../../../../tools/image/p-image-edit/SKILL.md) skill. Reuse the **hero** URL in every edit that must stay on-model.

## Motion source still + template (animate rows)

Each **`animate`** row needs a **speaking** motion template. Generate the still with **`p-image-edit`** off hero, then **`p-video-avatar`** on the approved still.

**Motion-source `still_edit`:**

```text
Recast as [character]. Medium close-up in [SETTING], confident warm expression,
mouth clearly visible ready to speak, documentary realism.
```

**Motion-template `video_prompt` (do):**

```text
Camera moves continuously for the full clip — smooth dolly push-in with subtle arc, never locked-off.
Subject speaks directly to camera with natural open-hand explain gestures, clear lip movement,
natural head nods and eyebrow emphasis while talking, warm smile building toward a small wave at the close.
```

**Motion-template `video_prompt` (avoid — silent avatar):**

```text
Subject smile builds then small wave and nod at close, atmospheric fog drifting …
```

**Motion-template `voice_prompt` (do):**

```text
Clear conversational delivery throughout — speaking directly to camera. Natural pacing with real pauses.
```

When motion-source prompts change, delete cached motion-source stills before regen. See [animate-beats.md](./animate-beats.md).

## voice_script — natural human (do)

```text
Hey — quick question. When you're making video with AI, how long do you actually wait between ideas?
Because for most people, it's way too long.
```

```text
So we teamed up with Tellers — they built this agentic video editor — and our whole model family is live inside it now.
```

## voice_script — corporate stiff (avoid)

```text
If you work with AI video, you already know the problem. You ask for something, then you wait — and the creative loop breaks.
```

```text
That is why we are partnering with Tellers. Our full model family — P-Image, P-Video, P-Image-Upscale, and P-Video-Avatar — is now live inside their agentic video editor.
```

## voice_prompt — realistic human delivery (do)

Project-level (reuse across scenes):

```text
Natural conversational tone — like a founder talking on LinkedIn, not a TV announcer.
Relaxed pacing, real pauses, contractions in delivery, slight smile when excited, honest not salesy.
```

Per-scene tweak (optional, still non-spoken):

```text
Slightly urgent on the hook; empathetic on the problem beat; building excitement on the reveal.
```

## voice_prompt — avoid

```text
Say the following about our enterprise AI video platform partnership announcement.
```

```text
P-Image, P-Video, P-Image-Upscale, P-Video-Avatar partnership with Tellers agentic editor.
```

## video_prompt — dynamic per scene (do)

Scene 1 close-up:

```text
Extreme close-up speaking directly to lens, subtle slow push-in, natural eyebrow movement,
conversational energy, slight head tilt, cinematic dark background holds steady.
```

Scene 2 outdoor 3/4:

```text
Three-quarter angle, speaks with natural hand gesture, golden hour light on face,
gentle breeze in hair, lake and peaks softly blurred behind, empathetic honest tone.
```

Scene 3 distinctive setting:

```text
Medium shot, speaks with building excitement, natural head nods, one open palm gesture,
camera holds with gentle float sensation, earth visible through window behind.
```

Scene 4 over-shoulder:

```text
Over-shoulder angle turning toward camera, speaks like explaining to a friend,
relaxed shoulder movement, warm window light, subtle zoom in during key point.
```

Scene 5 CTA:

```text
Camera moves continuously — stable portrait then gentle push-in on final line.
Subject speaks directly to camera with clear lip movement, warm friendly smile building,
subtle wave gesture at end after the spoken line lands.
```

## video_prompt (generic — avoid for multi-scene)

```text
no subtitles, no text, no logos
```

## Shared cast voice direction (for voice_prompt)

One line for the whole project:

```text
Shared read: [one line on pacing, genre, energy for every speaker in this piece].
```

Then per character, one short line each, still in **`voice_prompt`**, never in **`voice_script`**.

## Voice preset lock (same actor, same preset)

Each recurring character uses **one** Pruna **`voice`** + **`voice_language`** across **every** scene they speak—copy the same strings from your cast ledger into each **`p-video-avatar`** call for that character. Adjust performance only with **`voice_prompt`**, not by swapping presets mid-story.

## Client-facing script → confirmation → run package

Draft **`voice_script`** lines in **natural spoken English** (or the target language). Share the full read-through with the client or requester; obtain **explicit approval** before generating. After approval, paste approved lines verbatim into JSON **`voice_script`** fields and execute your chosen **run script** or **`curl`** sequence—no silent edits.

## Manifest JSON (scene package)

Store approved scenes in a machine-readable file (e.g. `v2_avatar_only_scripts.json`) before running API calls:

```json
{
  "ritual_seed": "k7Qm2xP9",
  "cast": {
    "voice": "Puck (Male)",
    "voice_language": "English (US)",
    "voice_prompt": "Natural conversational LinkedIn tone — like a founder talking to camera, not reading a script."
  },
  "character_sheet": {
    "role": "founder spokesperson",
    "age": "early 30s",
    "realism": "photorealistic documentary"
  },
  "scenes": [
    {
      "id": 1,
      "still": "hero",
      "still_prompt": null,
      "video_prompt": "...",
      "voice_script": "..."
    },
    {
      "id": 2,
      "still_prompt": "Change only: 3/4 angle, mountain summit overlooking alpine lake at golden hour...",
      "video_prompt": "...",
      "voice_script": "..."
    }
  ]
}
```

## Beat sheet (conversation)

```text
Scene 1 [CHAR A]: [hook line tied to product beat]
Scene 2 [CHAR B]: [reaction, new information]
Scene 3 [CHAR C]: [proof or demo beat]
...
Final scene: exact CTA wording: "[CTA]"
```
