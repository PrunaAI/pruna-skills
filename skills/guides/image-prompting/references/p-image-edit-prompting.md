# p-image-edit prompting

Surgical edit prompts for `p-image-edit`. Shared still craft: [prompt-golden-rules.md](./prompt-golden-rules.md). Identity sheets: [character-turnaround-sheet.md](./character-turnaround-sheet.md).

## Core formula

```text
Change [specific thing]. Keep [identity / medium / lighting era] identical.
```

| Do | Don't |
|----|-------|
| `Change background to soft #e8e4dc gradient, keep subject identical` | `Make it better` |
| `Same woman, identical face and coat; turn torso 30° toward camera` | `Regenerate in a new pose` (prefer edit from locked URL) |
| Name which ref: `face from image 1, outfit from image 2` | Vague `combine these images` |

## Identity lock (required when subject continues)

Append when the person/product must survive the edit:

```text
same [subject], identical face/uniform, do not remove the person, do not change species or age
```

Prefer editing a locked photo or turnaround plate over running photo generation again.

## Typography edits

Change readable copy on a surface — not spoken dialogue (that is `p-video` Mode A). Full still rules: [prompt-golden-rules.md](./prompt-golden-rules.md) §5.

```text
Change [surface] text to "[EXACT STRING]" in [weight], [placement]. Keep subject and lighting identical.
```

Quote the exact string; name surface + placement. Do not use Gemini TTS `[tags]` here.

## Scene-anchor stills (pair / triple)

| Plan field | Prefix | Role |
|------------|--------|------|
| `edit_prompt` | `OPENING:` or `OPEN:` | Start composition |
| `last_frame_edit_prompt` | `CLOSING:` or `CLOSE:` | End composition — physically reachable from start |

Rules: `video-prompting` · `video-prompting`.

- Subject must appear in **both** stills when the beat follows that subject.
- Change only pose, camera, background beat, or prop state — not medium mid-scene.
- Append the shared `style_bible` to every edit.

## Multi-reference composition

Index refs by role:

```text
Use face and hair from image 1. Outfit from image 2. Place subject in the cafe interior from image 3.
Match lighting to image 3. Keep face identical to image 1.
```

Max 5 images on `p-image-edit`.

## Turbo

| Setting | When |
|---------|------|
| `turbo: true` (default) | Simple background / color / light tweaks |
| `turbo: false` | Hard identity preserves, multi-ref composites, scene-anchor CLOSING plates that drop subjects |

## Edit, don't re-roll

If the still is ~80% right, edit surgically. Regenerating the photo drifts identity and wastes the approved plate.

## Worked example — three-reference composite

User lock: face from portrait ref, navy blazer from product flat-lay, cafe interior from location still. Keep face identical.

```text
Use face and hair from image 1. Outfit from image 2 (navy blazer, white tee). Place subject seated at the window table from image 3.
Match warm afternoon lighting to image 3. Keep face identical to image 1; same woman, do not change age or species.
Change nothing except outfit and background — keep pose from image 1.
```

`turbo: false` — hard multi-ref composite. Upload all three via `POST /v1/files` before `POST /v1/predictions`.

## Good / bad

**Good**

```text
OPENING: Wide alley, same courier in rain jacket small in frame, neon kanji, wet asphalt — style lock appended
```

```text
CLOSING: Same courier, identical face and jacket, closer in frame, hand on railing, do not remove the person
```

**Bad**

```text
Make it more cinematic and epic
```

```text
CLOSING: Empty rooftop view at night
```
(drops subject)

## Pre-send checklist

- [ ] Golden rules applied (positive framing, no banned filler)
- [ ] Change + keep clauses present
- [ ] Identity lock when continuity matters
- [ ] OPENING/CLOSING prefixes for anchor stills
- [ ] `turbo` chosen for edit difficulty
- [ ] Params (`aspect_ratio`, etc.) outside the prompt string

Validate outputs: [p-image-edit-quality-checklist.md](./p-image-edit-quality-checklist.md).
