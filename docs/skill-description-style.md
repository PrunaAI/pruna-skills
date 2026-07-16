# Skill description style

Frontmatter `description:` lines are **trigger phrases for humans**, not internal routing docs. Agents use them to decide when to load a skill.

## Rules

| Do | Don't |
|----|-------|
| Speak like a producer briefing a teammate | Lead with model IDs (`p-video`, `POST /v1/predictions`) |
| Cover the full ask: generate images, edit photos, make video, swap outfits, animate, lip-sync hosts, narrate, sing, score | Fixate on “stills” or “talking heads” as if that's all we do |
| Use everyday words: *person on camera*, *hero image*, *product shot*, *B-roll*, *voiceover*, *full music video* | Jargon chains: “multi-scene films”, “frame chain”, “slop gate” |
| One short “Use when…” + optional “Not for…” for the nearest neighbor | Long negative lists of internal skill names |
| Keep under ~220 characters when possible | Paste workflow phase names into description |

Keep routing boundaries in the **SKILL body**, not the frontmatter.

## Breadth by tier

- **Image tools:** generating, editing, upscaling, try-on, compositing from references
- **Video tools:** clips from text or images, motion transfer, in-footage swap, on-camera hosts
- **Audio tools:** songs, voiceover, beds, lyric timing
- **Workflows:** full productions — say what the user *gets*, not only one step
- **Routers/guides:** menu, quick one-off, sign-off before spend, quality/diversity

## Examples

**Too narrow / internal**

> Use when the user wants the fastest text-to-image stills…

**Natural**

> Use when someone wants a fast AI image — product shots, hero visuals, mood boards, or draft photos from a text prompt.

---

**Too API-centric**

> Use when the user wants one talking-head API call from a portrait plus script…

**Natural**

> Use when someone wants a person on camera speaking a script — lip-synced host, spokesperson, or narrated avatar from a portrait photo.

---

**Thin**

> Use when the user wants a music video, lyric video, sung promo…

**Natural**

> Use when someone wants a full music video — original song or vocals, performance clips, B-roll, and lyric-synced edits.

## After editing descriptions

1. Update trigger / non-trigger notes in [SKILL-TEST-LOG.md](../SKILL-TEST-LOG.md).
2. Run `./scripts/bundle_all_skills.sh` so plugin manifests pick up the new copy.
3. Run `make validate`.
