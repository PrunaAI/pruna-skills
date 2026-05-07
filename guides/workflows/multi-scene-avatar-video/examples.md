# Examples

## Multi-scene rhythm (generic cast)

Pattern:

1. Character A opens with a concrete hook tied to the product.
2. Character B reacts with new information, not a repeat of A.
3. Character C adds proof or stakes.
4. Group tightens the argument.
5. Final line is the exact client CTA.

Example dialogue (fictional cast):

```text
Riva (host): "One portrait, one line, and we already have motion—not a storyboard fantasy."
Kael (skeptic): "Motion is cheap. Staying on-model is the invoice."
Mire (builder): "Same API for the stills and the talk. Fewer handoffs, fewer drift days."
Jax (closer): "Ship the cut when you are ready, [CLIENT TEAM NAME]."
```

## Bad reference frame

Reject:

- extreme action pose
- hair or props across the mouth
- weapon or hand occluding the face
- tiny face in frame
- background that belongs to a different story world than the bible
- stray logos or UI

**Fix:** regenerate with **`p-image-edit`**, narrowing the prompt to “talking-head, shoulders square, hands low, mouth clear, same identity as reference.”

## Voice_prompt hygiene

Use:

```text
Warm, confident, slightly amused; brisk trailer pacing.
```

Avoid stuffing script or brand slogans into **`voice_prompt`**—those belong in **`voice_script`** only.

## Manifest skeleton (Pruna-only)

```markdown
# [Project] — multi-scene avatar (Pruna)

## Style bible
- Text: ...

## Files (POST /v1/files)
- ref_hero: url, id, expires
- scene_02_still: url, id

## Image predictions (p-image / p-image-edit / p-image-upscale)
- job id, model, input summary, output url, slop pass y/n

## Avatar predictions (p-video-avatar)
- scene id, job id, image url, voice, voice_script excerpt, output url

## Assembly
- ordered clip list, tool used to join (editor name / internal script), final export path

## Failed attempts
- job id, model, error message, corrective action
```
