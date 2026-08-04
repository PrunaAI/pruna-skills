# Clarification intake — ask before you spend

Use when the user’s request could mean more than one deliverable, more than one media path, or more than one creative default. **Ask in the first reply** (or right after routing), bundle related questions, and **record answers** in the plan or manifest. Do not start paid `POST`s, bulk generation, or long renders until missing decisions are answered or the user explicitly waives them (“use your judgment”, “surprise me”, “just build it”).

Workflow skills with **`Intake: ask before generating`** tables are authoritative for that deliverable. This doc is the **shared topic list** every Pruna guide and tool should use when the brief is silent.

## How to ask

| Do | Don't |
| --- | --- |
| Offer **2–3 concrete options** plus “other” when the choice is structural (acts, route, layout) | Interrogate field-by-field when the user already gave a locked brief |
| **Group** questions (media + audio in one message when both are open) | Same-turn **plan + paid video** without **approve plan** / gates |
| Use structured choice UI when the host supports it (many independent decisions) | Invent brand colors, voice, or “generate vs existing” when cost or look changes |
| Say what you **assume** if they waive, and proceed with a receipt in the summary | Treat inference as confirmation — restate inferred defaults separately |

**Red flags** (must clarify or show plan): skip review, burn credits, automation flags without explicit opt-in → see `generation-diversity` **Red flags** and [workflow-feedback-gates.md](./workflow-feedback-gates.md).

### Example bundles (adapt to the job)

Use when several topics are open at once; trim if the user already locked some:

1. **Deliverable shape:** “Should I **generate** new visuals/audio, **use files you already have**, or **mix** (e.g. your logo + generated B-roll)? Any **aspect ratio** and **resolution** target (720p vs 1080p, 9:16 vs 16:9)?”
2. **Look and sound:** “**Brand palette** (named kit vs custom hex / reference image)? **Narration or VO** (none, TTS, lip-sync host, your upload)? **Music** (silent, bed under VO, full song)? **Captions** (none, burned after render, in-composition)?”
3. **Structure and gates:** “Single clip or **multi-act** piece? If multi-act, I can propose **two orderings** — which direction? OK to pause for **approve plan** before paid video, or run end-to-end?”

For still-only jobs, add **aspect_ratio** and **megapixel / upscale target** when using `p-image-upscale` or print-sized exports.

## Universal topics

Ask when the brief does not already answer these:

| Topic | Clarify |
| --- | --- |
| **Media source** | Generate new assets (image/video/audio API) vs **use existing** files/URLs vs **mix** (e.g. user logo + generated B-roll) |
| **Brand / look** | Named brand kit vs ad-hoc palette (hex or reference), light vs dark, photoreal vs stylized |
| **Narration / VO** | None · on-screen text only · **TTS/narration track** · **lip-sync host** · user-uploaded VO · music-only |
| **Music / bed** | Silent · instrumental bed under VO · full song driving cuts · user-supplied track |
| **Captions** | None · burned after render · embedded in composition · style (promo karaoke vs simple phrase) |
| **Format** | Aspect ratio, duration target, destination (LinkedIn, TikTok, in-app, internal) |
| **Resolution / canvas** | **Video:** 720p vs 1080p vs 4K (and whether to upscale after gen). **HTML/composition:** export width×height (e.g. 1920×1080, 1080×1920). **Stills:** native aspect vs letterbox; target long edge or MP for upscale jobs |
| **Frame rate** | 24 / 25 / 30 fps when the deliverable or platform cares (Reels often 30; cinematic often 24) |
| **Structure** | Single clip vs multi-act / multi-scene; when vague, propose **two act orders** and let the user pick |
| **Approval** | Phase gates (**approve plan** / stills / clips) vs one-shot automation |
| **Locale / voice** | Language, accent, voice preset — never silently default from doc examples |
| **Privacy / upload** | First remote upload in session → `pruna-api` agent-safety acknowledgment |

## By skill type

### Tools (`p-image`, `p-video`, TTS, beds, …)

Minimum before first `POST`:

- What to produce (subject, mandatory copy, refs)
- **Generate vs upload** for each required input
- Aspect / resolution / duration caps where the API cares (`aspect_ratio`, `resolution`, seconds, MP target)
- Point to **generation-diversity** ritual + craft skill for prompt drafting

Tool-specific intake lives in each tool’s **Agent habit**; expand with rows from the universal table when silent.

### Craft guides (`image-prompting`, `video-prompting`, `audio-prompting`)

Clarify **creative locks** before drafting prompts: identity continuity, camera/motion intent, embed-vs-post audio, lyrics vs instrumental.

### `video-editing` / assembly

Confirm **files on disk**, ffmpeg available, and whether missing pieces should be **generated** (redirect to tools) or **skipped**. For multi-act HTML combos, clarify structure, caption timing source, and bed/narration like the universal table.

### Brand / visual identity

When logos, colors, or on-image type might matter, ask before generating:

- **Colors:** reference image, named swatches, or custom hex values?
- **Logo / wordmark:** file the user will supply, none, or text-only labels in the frame?
- **Look:** light vs dark, photoreal vs stylized (see universal **Brand / look** row)

Do not invent palette or logo details when the user did not specify them. When they supplied official assets, use those files — do not redraw trademarks from a text prompt alone.

### Workflows

Run the workflow’s **Intake** table in full. Cross-check universal topics; add rows only when the workflow table is thinner than the job needs.

### HyperFrames (optional companion)

Fresh creation: **`hyperframes`** runs the intent layer (`intent-interview.md`) → `BRIEF.md` — do not duplicate that interview in Pruna skills.

When HyperFrames is used **without** a fresh interview (edit, resume, narrow fix, or Pruna-only assembly):

| Topic | Ask if unclear |
| --- | --- |
| Media | Generate new visuals/audio vs use **existing** project or user assets |
| Design | Existing `frame.md` / design spec vs new palette (offer preset vs custom hex) |
| Narration | VO yes/no, script source, TTS vs upload vs none |
| Music | Bed vs beat-driven vs none |
| Captions | In-composition vs post-render burn (Pruna path: `video-editing`) |
| **Canvas / export** | 1920×1080 vs 1080×1920 vs square; 720 vs 1080 render; fps if not default |

See companion **`hyperframes/references/clarification-before-build.md`** when installed (checklist + question bundles for edit/resume paths).

## When you can skip

- User supplied a **complete** manifest, `BRIEF.md`, or explicit “use these files only”
- **Recipe / remembered defaults** adopted with confirmation (HyperFrames)
- Single trivial op with one obvious input (e.g. upscale this file to 4 MP)
- User already answered in the same thread — do not re-ask; restate in the plan

## See also

- [workflow-feedback-gates.md](./workflow-feedback-gates.md)
- [still-image-prompt-flow.md](./still-image-prompt-flow.md) — brief lock for stills
- `pruna-api` agent-safety reference
- `video-editing` — **Structure and creativity** when act order is open
