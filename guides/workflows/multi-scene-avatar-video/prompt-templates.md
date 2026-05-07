# Prompt templates (Pruna only)

## Reference gathering (research assistant prompt)

```text
Collect up to [N] high-quality, rights-clear reference images for [SUBJECT / CAST].
Prefer official art packs, style guides, or assets the client can license.
For each file record: character, intended use, source, license note, and image quality (resolution, clarity).
```

## Upload rule

Use **`POST /v1/files`** and then Pruna **`urls.get`** values in **`p-image-edit`** `images` and in **`p-video-avatar`** `image`. Do not pass arbitrary hotlinks you do not control.

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

## p-image-edit: match reference, change only what the scene needs

```text
[Style bible]
Using the attached reference(s) as identity, produce a vertical 9:16 talking-head frame for scene [N]: [POSE / EMOTION / BACKGROUND CHANGE ONLY].
Keep face, species, and costume on-model; mouth unobstructed; no new text or logos in frame.
```

Use 1–5 **`images`** URLs per the [p-image-edit](../../../tools/image/p-image-edit/SKILL.md) skill. Reuse the **hero** URL in every edit that must stay on-model.

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

## video_prompt (do)

```text
[Character] speaks to camera with [tone]. Stable portrait framing, subtle head motion,
natural mouth movement, clean centered face.
```

## video_prompt (avoid)

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

## Beat sheet (conversation)

```text
Scene 1 [CHAR A]: [hook line tied to product beat]
Scene 2 [CHAR B]: [reaction, new information]
Scene 3 [CHAR C]: [proof or demo beat]
...
Final scene: exact CTA wording: "[CTA]"
```
