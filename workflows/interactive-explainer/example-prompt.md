# Educational explainer (narrator + character)

Build an educational short where the **host narrator** and **experts or characters in the story talk to each other** — not wall-to-wall narration.

Works for history, science, nature, how-it-works, children's topics, and more.

## Quick start prompts

**Science / nature:**
> Use the **interactive-explainer** workflow for [topic]. Alternate **narrator** beats (`p-video` + Gemini TTS, scene anchor triple, lines ≤19s) with **character** beats (`p-video-avatar`, expert `voice_script`, lips-in-frame stills). **720p, 24 fps** (unless user wants higher delivery). Narrator `video_prompt`: `OPEN:` / `MID:` (camera or light — physics-safe) / `CLOSE:`. Character `video_prompt`: **one continuous take** (slow push-in). **Still prompts: positive only** — plain surfaces, unprinted props, one camera angle; never `no …` or `avoid …` in creative fields (see skill **Positive prompts only**). Use **`still_from`** on character rows after object/B-roll heroes. Target ~40% character scenes. Pass the [stand-alone test](../../../../references/workflows/interactive-explainer-scenes.md).

**History / biography:**
> Same workflow — one through-line (not a life survey), witness-style `voice_scripts`, causal chain for events (mechanism → act → response → aftermath). Pick one **visual mode** for the whole film and lock it in `style_bible` and all stills. Close with **three beats**: narrator aftermath (≥3 concrete facts) → final character witness → **`NN_wrap` narrator recap** that answers the hook (bookend stills when possible). **720p, 24 fps**, physics-safe motion per [interactive-explainer-motion.md](../../../../references/workflows/interactive-explainer-motion.md).

**Children's educational:**
> Same workflow — warm illustrated `style_bible`, friendly guide or kid character, simpler vocabulary, shorter lines.

## Copy template

```bash
mkdir -p output/verticals/interactive-explainer/my-explainer/{stills,clips,audio}
cp workflows/interactive-explainer/templates/explainer-plan.template.json \
   output/verticals/interactive-explainer/my-explainer/plan.json
```

## Install skill

```bash
npx skills add PrunaAI/pruna-skills@interactive-explainer -y
# or: npx plugins add PrunaAI/pruna-skills -y  # pick interactive-explainer
```
