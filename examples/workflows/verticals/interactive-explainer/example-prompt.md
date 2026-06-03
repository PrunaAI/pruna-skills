# Educational explainer (narrator + character)

Build an educational short where the **host narrator** and **experts or characters in the story talk to each other** — not wall-to-wall narration.

Works for history, science, nature, how-it-works, children's topics, and more.

## Quick start prompts

**Science / nature:**
> Use the **interactive-explainer** workflow for [topic]. Alternate **narrator** beats (`p-video` + Gemini TTS, scene anchor triple, lines ≤19s) with **character** beats (`p-video-avatar`, expert `voice_script`, lips-in-frame stills). **1080p, 48 fps.** Every `video_prompt`: `OPEN:` / `MID:` (dynamic camera or light — no physics) / `CLOSE:`. Target ~40% character scenes. Pass the [stand-alone test](../../../../references/workflows/interactive-explainer-scenes.md). Hero via **p-image**, stills via **p-image-edit**.

**History / biography:**
> Same workflow — one through-line (not a life survey), witness-style `voice_scripts`, Ancaster-quality dialogue. **1080p, 48 fps**, physics-safe motion per [interactive-explainer-motion.md](../../../../references/workflows/interactive-explainer-motion.md).

**Children's educational:**
> Same workflow — warm illustrated `style_bible`, friendly guide or kid character, simpler vocabulary, shorter lines.

## Copy template

```bash
mkdir -p output/verticals/interactive-explainer/my-explainer/{stills,clips,audio}
cp guides/workflows/verticals/interactive-explainer/templates/explainer-plan.template.json \
   output/verticals/interactive-explainer/my-explainer/plan.json
```

## Install skill

```bash
./scripts/install_skill.sh interactive-explainer
```
