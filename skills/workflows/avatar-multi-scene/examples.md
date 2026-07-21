# Examples

## Dynamic multi-scene avatar (partnership / founder social)

Proven pattern from production runs:

1. **Character sheet** — photoreal founder, early 30s, locked **`seed`**, one **`voice`** preset.
2. **Hero** — `p-image` (documentary photoreal) → slop gate → approve identity anchor.
3. **Per scene** — `p-image-edit` (from hero anchor; change **only** angle + background) → slop gate → `p-video-avatar`. **Run edits and avatar jobs in parallel batches** per phase once dependencies are met ([pruna-api.md#parallel-async-multi-scene--batch](../../guides/pruna-api/references/pruna-api.md#parallel-async-multi-scene--batch)); use **one subagent per scene lane** when the host supports it.
4. **Vary every scene** — e.g. dark close-up → mountain overlook → ISS cupola → desk window light → studio CTA. Never repeat the same office framing twice.
5. **Natural voice** — contractions, conversational hooks; **`voice_prompt`** describes human delivery, not product copy.

Example dialogue (single spokesperson, natural):

```text
Scene 1: "Hey — quick question. When you're making video with AI, how long do you actually wait between ideas?"
Scene 2: "And that's the real problem, right? It's not just slow — you lose momentum. The whole creative loop just breaks."
Scene 3: "So we teamed up with Tellers — our whole model family is live inside their editor now."
Scene 4: "What's actually cool is the speed — cheap enough that you can genuinely explore without worrying about every credit."
Scene 5: "Anyway — check out Tellers. Link's in the post. I'd love to see what you build."
```

Store scenes in JSON (`v2_avatar_only_scripts.json` pattern in `prompt-templates.md`) with **`ritual_seed`**, per-scene **`video_prompt`**, and **`still_prompt`** deltas.

## Mixed announcement (avatar + animate slider beats)

Pattern for product launches that interleave speaking scenes with motion-transfer demos:

| # | Type | Beat |
|---|------|------|
| 1 | avatar | Hook — spokesperson intro |
| 2 | animate | Slider — same UGC motion, new persona still |
| 3 | avatar | Reveal — partnership / feature detail |
| 4 | animate | Slider — second motion template, repose hero to match |
| 5 | avatar | CTA |

**Pipeline:** shared hero anchor → per-row still prep (edit for avatars; optional repose for animate) → parallel **`p-video-avatar`** + parallel **`p-video-animate`** → parallel slider renders for animate rows → ffmpeg concat in scene order.

Model roles and alignment: [animate-beats.md](./animate-beats.md).

**Alignment reminder:** animate rows fail when a meme/mascot still meets human full-body dance motion—pick bust-only templates or repose first (see SKILL **Alignment prep**).

**Style ladder reminder:** each persona still in an animate slider row should use a different **`visual_style_tag`** (photoreal, anime, claymation, Disney 3D, cyberpunk, game cinematic) with its own background, camera angle, and lighting — [generation-diversity.md#visual-variety](../../guides/generation-diversity/references/generation-diversity.md#visual-variety).

## Motion-transfer-only reel (animate rows)

All-slider showcase (UGC variations, recasting demo):

1. Scene table with only **`animate`** rows.
2. Upload motion templates + reference stills in parallel.
3. Parallel **`p-video-animate`** → batch slider render via [`batch.template.json`](./templates/batch.template.json).
4. Concat comparison MP4s:

```bash
# concat_list.txt
file 'output/scene01_compare.mp4'
file 'output/scene02_compare.mp4'

ffmpeg -f concat -safe 0 -i concat_list.txt -c copy output/recast_reel.mp4
```

**End with avatar CTA** when the piece is a product launch — return the hero spokesperson in a clean studio close-up.

**Slider-only** (animate outputs already exist):

Build side-by-side sliders with **ffmpeg hstack** (see `this skill` — agent runs ffmpeg locally; no Python runner).

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

Use (realistic human):

```text
Natural conversational tone — like a founder on LinkedIn, not a TV announcer.
Relaxed pacing, real pauses, slight smile when excited, honest not salesy.
```

Avoid stuffing script, product names, or brand slogans into **`voice_prompt`**—those belong in **`voice_script`** only.

## Manifest skeleton (Pruna-only)

```markdown
# [Project] — multi-scene avatar (Pruna)

## ritual_seed
- ritual_seed: "k7Qm2xP9" (SSoT planning — do not pass to API)

## Character sheet
- role, age, hair, realism, wardrobe baseline, personality

## Style bible
- Text: ...

## Scene table
| # | type | setting/angle or motion template | deliverable |

## Files (POST /v1/files)
- ref_hero: url, id, expires
- scene_02_motion_template: url, id  (animate rows)

## Image predictions (p-image / p-image-edit)
- job id, model, input summary, output url, slop pass y/n

## Avatar predictions (p-video-avatar)
- scene id, job id, seed, image url, voice, voice_script excerpt, video_prompt, output url

## Animate predictions (p-video-animate)
- scene id, job id, motion url, image url, instruction_prompt, animated mp4, slider compare mp4, alignment notes

## Assembly
- ordered clip list, tool used to join (editor name / internal script), final export path

## Failed attempts
- job id, model, error message, corrective action
```
