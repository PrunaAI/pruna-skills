# Clip chaining (multi-scene video)

When and how to continue motion across `p-video` clips. Plan JSON examples stay in [scene-anchor-pair.md](./scene-anchor-pair.md) and [scene-anchor-triple.md](./scene-anchor-triple.md); this page is the decision tree + prompt rules.

Workflows: `visual-transition-reel` · `narrated-multi-scene`.

## Decision tree

```text
Does motion continue in the same place/moment (no time jump)?
  NO  → chain_from_previous: false — hard cut; compose a new OPENING still
  YES → chain_from_previous: true
        Prefer frame_chain_mode: extract_last_frame (sequential renders)
        Only use planned_stills if you accept possible cut jumps
```

| Situation | `chain_from_previous` | Join |
|-----------|----------------------|------|
| Continuous action (run → leap) | `true` | Short crossfade ~0.12–0.15s after extract |
| New beat / location / pause | `false` | Hard cut (0 crossfade) |
| First scene | `false` | — |
| Montage vignettes (no shared motion) | `false` + `parallel_vignettes` | Hard cuts; parallel renders OK |

| `frame_chain_mode` | Next scene `image` | Render order |
|--------------------|--------------------|--------------|
| **`extract_last_frame`** | ffmpeg last frame of prior clip | **Sequential** when any scene chains |
| **`parallel_vignettes`** | each scene’s own start still | **Parallel** |
| **`planned_stills`** | prior scene end still URL | Parallel once stills exist — higher jump risk |

**Why extract?** Planned end stills often differ from the model’s actual last frame → visible jump.

## Prompt rules for chained beats

1. **Same subject language** — repeat “same [character]” in OPEN/MID/CLOSE.  
2. **No teleport** — ban `cut to`, `suddenly in`, `walls disappear`; use `gradually`, `walks through`, `ease into`.  
3. **Match lighting era** — chained clips share `style_bible` and time-of-day.  
4. **Exit / enter continuity** — if scene 1 CLOSE faces right, scene 2 OPEN should not hard-flip screen direction without a motivated turn.  
5. **Hard-cut scenes** — treat as fresh OPENING; do not assume prior pose.

## Assembly notes

1. Concat in scene order (ffmpeg concat — see the workflow skill).  
2. Per-join `crossfades`: chain ~0.12–0.15s; hard cuts 0.  
3. Normalize audio (48 kHz stereo) when mixing formats.  
4. Optional bed under native SFX — [audio-post-production.md](../../audio-prompting/references/audio-post-production.md).

## Intake checklist

- [ ] Each scene: chain flag only if motion truly continues  
- [ ] `frame_chain_mode` chosen  
- [ ] Chained prompts pass Details Law ([prompt-dramaturgy.md](./prompt-dramaturgy.md))  
- [ ] Physics tier OK ([physics-safe-motion.md](./physics-safe-motion.md))
