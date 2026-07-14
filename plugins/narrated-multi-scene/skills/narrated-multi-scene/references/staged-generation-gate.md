# Staged generation gate

Human-in-the-loop phases for workflow skills and plan runners. **Video and replace jobs are expensive** — gate on approved stills before any `p-video-*` call. **Final audio** (bed mix, full-song mux) runs only after clip review.

See also: [parallel-execution.md](./parallel-execution.md) Phase 0, [generation-quality-checklists.md](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/core/generation-quality-checklists/SKILL.md), [workflow-feedback-gates.md](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/workflow-feedback-gates.md) (per-skill index), [requesting-generation-feedback](https://github.com/PrunaAI/pruna-skills/tree/main/plugins/requesting-generation-feedback/skills/requesting-generation-feedback/SKILL.md) (red flags before paid generation).

## Phases

| Phase | Models | Cost | User interaction |
|-------|--------|------|------------------|
| **0 — Plan** | none | free | Present scene table, cast, scripts, `style_bible`; explicit **approve plan / go** |
| **A — Stills** | `p-image`, `p-image-edit` | low | Show hero + start/end plates; run checklists; **approve stills** |
| **A2 — Audio prep** | Gemini TTS, Music 2.5, WhisperX align | low–medium | **Listen / read** narration or song; fix copy before video |
| **B — Video** | `p-video`, `p-video-avatar`, `p-video-animate`, `p-video-replace` | **high** | Only after Phase A approval; **approve clips** before assembly |
| **C — Assembly** | local ffmpeg concat / slider scripts | free | Review concat (embedded VO); compare MP4s before final mux |
| **D — Final audio** | Stable Audio bed, bed mix, full-song mux | low | Only after Phase B clip approval |

## Agent rules

1. **Never** run Phase B in the same turn as Phase A without showing stills and waiting for approval.
2. **Never** run Phase D (bed / final mux) until the user has reviewed Phase B clips (or concat with embedded VO).
3. **Parallelize within a phase**, not across phases.
4. **Per-scene approval** for persona ladders, face recasts, and performance identity — show JPEG/PNG paths or thumbnails.
5. **Regeneration loop** — reject → rerun only the failed asset (still, TTS, or clip), not the whole pipeline.
5. Run model checklists on every still before Phase B — **open each image and review it visually** against the checklist (see [generation-quality-checklists.md](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/core/generation-quality-checklists/SKILL.md#who-applies-these-checklists)); then present paths for user approval.
7. **Ask when art direction is unclear** — visual mode, cast, continuity, motion energy, bed yes/no. Do not guess and burn video credits.
8. **[Generation diversity](./generation-diversity.md)** — ritual seed + rotate ≥2 scenario axes vs the previous output in session.
9. **[Random seed ritual](./random-seed-ritual.md) (SSoT)** — before **every** `POST /v1/predictions`, generate and state a ritual string; derive prompt axes via sum-mod. **Do not** pass ritual string to API `seed`. Never copy doc example strings for new work.

## Art direction — ask the user when unclear

| Decision | Why it matters |
|----------|----------------|
| **`style_bible` / visual mode** | Photoreal vs painterly vs illustrated changes every frame |
| **Cast + voice** | Wrong gender/voice pairing; face drift without hero + edit chain |
| **Narrator ↔ character mix** | Lecture vs conversation |
| **Continuity** | Same singer/character vs deliberate recasts |
| **Motion / `video_prompt`** | Static clips, physics traps, text burn-in |
| **Background music** | Bed can clash with VO or mask bad narration |
| **Draft vs final** | `720p/24` preview vs `1080p/48` delivery |

## Wording templates

After Phase 0 (plan):

> Here is the scene plan: style, cast, and sample prompts. Reply **approve plan** to generate stills, or tell me what to change.

After Phase A (stills):

> Stills are in `stills/` (hero, start/end plates). Reply **approve stills** to run narration TTS and video jobs, or name scenes to fix.

After Phase A2 (audio prep):

> Narration MP3s are in `audio/narration_*.mp3`. Listen for pace and tone. Reply **approve audio** (or **approve stills** if you already did) to run video, or tell me lines to rewrite.

Before Phase B (cost warning):

> Phase B will call `p-video` / `p-video-avatar` (paid). Confirm you have reviewed stills and narration.

After Phase B (clips):

> Clips are in `clips/`. Reply **approve clips** to concat and add background music, or name clips to regenerate.

Before Phase D (final audio):

> Assembly will mix the Stable Audio bed under the film. Confirm clip review is complete.

## Plan runners

Default **`--phase stills`**. Phase B requires **`--approve-stills`** or `"phase_a_approved": true` in `generation_status.json`. Assembly and bed mix require **`--approve-clips`** or `"phase_b_approved": true`.

### Replace / animate comparison

```bash
python3 ./scripts/run_from_plan.py --plan ./my-plan.json --out-dir ./output/reel --phase stills
python3 ./scripts/run_from_plan.py --plan ./my-plan.json --out-dir ./output/reel --phase video --approve-stills
python3 ./scripts/run_from_plan.py --plan ./my-plan.json --out-dir ./output/reel --phase render
python3 ./scripts/run_from_plan.py --plan ./my-plan.json --out-dir ./output/reel --phase all --yes-skip-stills-gate
```

### Interactive explainer

```bash
python3 workflows/verticals/interactive-explainer/scripts/run_from_plan.py \
  --plan ./output/.../plan.json --out-dir ./output/... --phase stills
# review stills/
python3 .../run_from_plan.py --plan ... --out-dir ... --approve-stills --phase tts
# listen to audio/narration_*.mp3
python3 .../run_from_plan.py --plan ... --out-dir ... --phase video
# review clips/
python3 .../run_from_plan.py --plan ... --out-dir ... --approve-clips --phase assemble --final-name my_explainer_final.mp4
```

Skip gates for automation only: **`--yes-skip-stills-gate`**, **`--yes-skip-clips-gate`**.

## Anti-patterns

- Full `--phase all` end-to-end without still or clip review
- Batch `p-video-replace` before reference QA
- Same-turn plan approval + video generation
- Running TTS or video before still approval
- Mixing background music before clip review
- **Scoped still regen without delete/`--fresh`** — prompt edits silently have no effect until still files are removed or `--regen-stills` is passed
- **`--phase all` on partial regen** when other scenes' clips are missing — assembly fails; regen the target scene then use **`--assemble-only`**
- **VO change without deleting `audio/narration_*.mp3` and `clips/`** — narrator keeps old dialogue; delete affected files before regen

## Partial regen (decision tree)

| Goal | Delete | Then run |
|------|--------|----------|
| Plan / prompt text only (no API yet) | nothing | edit `plan.json`; re-present Phase 0 |
| Hero / still prompt / seed | `stills/hero.png`, scene PNGs | `--regen-stills --phase stills` → approve → continue |
| TTS line change | `audio/narration_{id}.mp3` | `--approve-stills --phase tts` → `--phase video` for that scene (`--only ID`) |
| `voice_script` change | scene still + `clips/{id}.mp4` | `--only ID --regen-clips --phase video` |
| Reconcat only (clips exist) | nothing | `--assemble-only --approve-clips` |
| Bed only | `{slug}.mp4` final (keep concat) | `--assemble-only --approve-clips` |

For replace-slider plans, map partial regen to the table above; blocked still trigger words: [visual-variety-bible.md](https://github.com/PrunaAI/pruna-skills/tree/main/workflows/core/visual-variety-bible/SKILL.md#prompt-patterns).
