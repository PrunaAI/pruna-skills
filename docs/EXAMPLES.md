# Examples

Real prompts and outputs from the Pruna API — hosted on the [`PrunaAI/pruna-skills` Hugging Face dataset](https://huggingface.co/datasets/PrunaAI/pruna-skills) (`examples/`). Each PNG or MP4 has a matching `.meta.json` with the exact prompt and model (audio/JSON sidecars where noted). Example binaries are **not** in git; pull locally with `make download-doc-examples-hf` or regenerate with `make doc-examples`.

**Ask your agent** lines are natural-language requests that load that tool or workflow. Model prompts are what hit the API. Open **Prompts & inputs** on each card to expand — outputs (images, clips, audio) stay visible.

Regenerate locally: `make doc-examples` or `python3 .maintainer/generate_doc_examples.py` (requires `PRUNA_API_KEY`; Replicate tools/workflows also need `REPLICATE_API_TOKEN`). To fill in only new examples without wiping existing assets: `python3 .maintainer/generate_doc_examples.py --only missing-tools --missing-only`.

Publish to Hugging Face and refresh markdown URLs: `make sync-doc-examples-hf` (requires `HF_TOKEN` or `huggingface-cli login`).

**CI check (no API):** `make download-doc-examples-hf && make validate-doc-examples` — verifies every skill has assets, audio where expected, and multi-scene sidecars.

Images use max P-API resolution (1440px edge); videos use final **1080p @ 24fps** (720p for some motion-transfer demos).

The [README quickstart](../README.md#quickstart) walks through the **drummer try-on → performance clip** chain (`music-video-garage-drummer*` + `p-image-try-on-drummer` on the dataset).

## Coverage



| Skill | Example asset | Section |
|-------|---------------|---------|
| **Tools** | | |
| `p-image` | `p-image-brass-hummingbird.png` | [below](#single-tool--p-image) |
| `p-image-edit` | `chain-monarch-02-end.png` | [below](#single-tool--p-image-edit) |
| `p-image-upscale` | `p-image-upscale-hummingbird.png` | [below](#single-tool--p-image-upscale) |
| `p-image-try-on` | `p-image-try-on-drummer.png` | [below](#single-tool--p-image-try-on) |
| `p-video` | monarch chain + aurora clip (see [p-video](#single-tool--p-video)) | [chains](#chain--monarch-on-lavender) |
| `p-video-avatar` | `music-video-garage-drummer-clip.mp4` | [below](#single-tool--p-video-avatar) |
| `p-video-animate` | `p-video-animate-monarch.mp4` | [below](#single-tool--p-video-animate) |
| `p-video-replace` | `p-video-replace-jacket.mp4` | [below](#single-tool--p-video-replace) |
| `gemini-3.1-flash-tts` | `illustrated-library-whale-narration.mp3` | [below](#single-tool--gemini-31-flash-tts) |
| `music-2.5` | `music-video-garage-drummer-song.mp3` | [below](#single-tool--music-25) |
| `stable-audio-2.5` | `stable-audio-library-bed.mp3` | [below](#single-tool--stable-audio-25) |
| `whisperx` | `whisperx-drummer-song.json` | [below](#single-tool--whisperx) |
| **Workflows** | | |
| `image-to-video` | `image-to-video-aurora-*` | [below](#workflow--image-to-video) |
| `visual-transition-reel` | `chain-monarch-*` | [monarch chain](#chain--monarch-on-lavender) |
| `narrated-multi-scene` | `narrated-multi-scene-demo.mp4` (2 scenes) | [below](#workflow--narrated-multi-scene) |
| `avatar-single-scene` | `music-video-garage-drummer-clip.mp4` | [below](#workflow--avatar-single-scene) |
| `avatar-multi-scene` | `avatar-multi-scene-demo.meta.json` (2 clips, same still) | [below](#workflow--avatar-multi-scene) |
| `interactive-explainer` | drummer + whale components | [below](#workflow--interactive-explainer) |
| `music-video` | `music-video-garage-drummer-*` | [below](#workflow--music-video) |
| `illustrated-story-reel` | `illustrated-library-whale-*` | [below](#workflow--illustrated-story-reel) |

## Install



```bash
export PRUNA_API_KEY="your_key"   # see [api-setup.md](api-setup.md)

npx skills add PrunaAI/pruna-skills@p-image -y          # one tool
npx plugins add PrunaAI/pruna-skills                    # workflow or pruna-full
npx skills add PrunaAI/pruna-skills -l
npx plugins discover PrunaAI/pruna-skills
```

**All 20 skills at once:** `npx plugins add PrunaAI/pruna-skills` → pick **`pruna-full`**.

---

# Tools

## Single tool — `p-image`

**Output**

![brass hummingbird terrarium](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/p-image-brass-hummingbird.png)

<details>
<summary>Prompts & inputs</summary>

**Ask your agent**

> Generate a 1:1 museum-style product photo of a clockwork brass hummingbird in a glass terrarium.

**Model prompt**

> 1:1 macro product photo, clockwork brass hummingbird frozen mid-flap inside a glass terrarium, tiny gears visible, dew on glass, moody forest bokeh background, museum exhibit lighting, no text

</details>

```bash
npx skills add PrunaAI/pruna-skills@p-image -y
```

---

## Single tool — `p-image-edit`

**Output**

![monarch wings open](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/chain-monarch-02-end.png)

<details>
<summary>Prompts & inputs</summary>

**Ask your agent**

> Edit this monarch-on-lavender still so the wings are open wide — same stem and camera.

Reuses the opening plate from the [monarch chain](#chain--monarch-on-lavender).

**Model prompt**

> Same butterfly same lavender same camera. Wings open wide displaying full orange and black pattern, same dew and bokeh, keep composition identical…

</details>

```bash
npx skills add PrunaAI/pruna-skills@p-image-edit -y
```

---

## Single tool — `p-image-upscale`

**Output**

![upscaled hummingbird](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/p-image-upscale-hummingbird.png)

<details>
<summary>Prompts & inputs</summary>

**Ask your agent**

> Upscale the brass hummingbird product shot for print — more detail, 8 megapixel target.

Upscaled from [`p-image-brass-hummingbird.png`](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/p-image-brass-hummingbird.png) (`target: 8`, `enhance_details: true`).

</details>

```bash
npx skills add PrunaAI/pruna-skills@p-image-upscale -y
```

---

## Single tool — `p-image-try-on`

**Output**

![try-on drummer](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/p-image-try-on-drummer.png)

<details>
<summary>Prompts & inputs</summary>

**Ask your agent**

> Put this vintage red garage band jacket on the drummer portrait — keep pose and background.

Person plate: [`music-video-garage-drummer.png`](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/music-video-garage-drummer.png) · Garment flat-lay: [`p-image-try-on-garage-jacket.png`](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/p-image-try-on-garage-jacket.png)

</details>

```bash
npx skills add PrunaAI/pruna-skills@p-image-try-on -y
```

---

## Single tool — `p-video`

**Output — three patterns**

| Still → clip | Start/end plates | Narration-led (Mode B) |
|--------------|------------------|------------------------|
| <video src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/image-to-video-aurora-clip.mp4" controls width="240"></video> | <video src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/chain-monarch-clip.mp4" controls width="240"></video> | <video src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/illustrated-library-whale-reel.mp4" controls width="240"></video> |

<details>
<summary>Prompts & inputs</summary>

**Ask your agent**

> Animate a still into video — with optional end plate, fixed duration, or narration driving length.

| Pattern | Example | Key inputs |
|---------|---------|------------|
| **Still → clip** (duration) | [`image-to-video-aurora-clip.mp4`](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/image-to-video-aurora-clip.mp4) | `image` + `prompt` + `duration` |
| **Start/end plates** | [`chain-monarch-clip.mp4`](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/chain-monarch-clip.mp4) | `image` + `last_frame_image` + `duration` |
| **Narration-led** (Mode B) | [`illustrated-library-whale-reel.mp4`](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/illustrated-library-whale-reel.mp4) | `image` + `audio` + `save_audio: true` — **omit `duration`** |

</details>

```bash
npx skills add PrunaAI/pruna-skills@p-video -y
```

---

## Single tool — `p-video-avatar`

**Output**

<video src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/music-video-garage-drummer-clip.mp4" controls width="360"></video>

<details>
<summary>Prompts & inputs</summary>

**Ask your agent**

> Make the garage drummer sing along to this song slice — lip sync to the vocal track.

Same clip as the [music-video](#workflow--music-video) performance beat — reuses [`music-video-garage-drummer-song.mp3`](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/music-video-garage-drummer-song.mp3) slice.

</details>

```bash
npx skills add PrunaAI/pruna-skills@p-video-avatar -y
```

---

## Single tool — `p-video-animate`

**Output**

<video src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/p-video-animate-monarch.mp4" controls width="640"></video>

<details>
<summary>Prompts & inputs</summary>

**Ask your agent**

> Animate the monarch still (wings closed) using the wing-open motion from our monarch clip — same butterfly, same framing.

Motion transfer needs **matched framing and pose**: appearance from the still, choreography from the template ([pairing gates](../references/video/p-video-animate-prompting.md)).

| Input | Asset |
|-------|-------|
| Still (`image`) | [`chain-monarch-01-open.png`](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/chain-monarch-01-open.png) — wings closed |
| Motion template (`video`) | 5s trim — [`chain-monarch-animate-template.mp4`](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/chain-monarch-animate-template.mp4) (from [`chain-monarch-clip.mp4`](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/chain-monarch-clip.mp4)) |

No `instruction_prompt` — source motion already opens the wings.

</details>

```bash
npx skills add PrunaAI/pruna-skills@p-video-animate -y
```

---

## Single tool — `p-video-replace`

**Output**

<video src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/p-video-replace-jacket.mp4" controls width="360"></video>

<details>
<summary>Prompts & inputs</summary>

**Ask your agent**

> In this garage drummer clip, swap only her jacket for the red band tour jacket from the reference — keep face, performance, and audio.

**Clothing-only** replace works better than identity swap on lip-sync performance clips ([replace prompting](../references/video/p-video-replace-prompting.md)).

| Input | Asset |
|-------|-------|
| Source (`video`) | 6s trim of [`music-video-garage-drummer-clip.mp4`](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/music-video-garage-drummer-clip.mp4) — **with vocal audio** |
| Garment ref (`images[0]`) | [`p-image-try-on-garage-jacket.png`](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/p-image-try-on-garage-jacket.png) |

Set **`save_audio: true`** so the song/vocal track from the source clip is preserved in the output.

</details>

```bash
npx skills add PrunaAI/pruna-skills@p-video-replace -y
```

---

## Single tool — `gemini-3.1-flash-tts`

**Output**

<audio src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/illustrated-library-whale-narration.mp3" controls></audio>

<details>
<summary>Prompts & inputs</summary>

**Ask your agent**

> Read this library-whale line in a warm storybook narrator voice.

Same narration used by [illustrated-story-reel](#workflow--illustrated-story-reel).

> *[warmly] In a paper-cut library deep below the city, a blue whale swims between the shelves — chasing stories printed on fluttering pages.*

</details>

```bash
npx skills add PrunaAI/pruna-skills@gemini-3.1-flash-tts -y
```

---

## Single tool — `music-2.5`

**Output**

<audio src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/music-video-garage-drummer-song.mp3" controls></audio>

<details>
<summary>Prompts & inputs</summary>

**Ask your agent**

> Write an indie garage-rock song with these lyrics for a teenage drummer music video.

Same song as [music-video](#workflow--music-video). Sidecar includes full lyrics and style prompt.

</details>

```bash
npx skills add PrunaAI/pruna-skills@music-2.5 -y
```

---

## Single tool — `stable-audio-2.5`

**Output**

<audio src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/stable-audio-library-bed.mp3" controls></audio>

<details>
<summary>Prompts & inputs</summary>

**Ask your agent**

> Generate a soft whimsical instrumental bed for a paper-cut library story — no vocals.

Pairs with the [whale illustrated reel](#workflow--illustrated-story-reel) mood (music-mode reels mux this under Ken Burns segments). Native Stable Audio 2.5 render; if Replicate returns a provider error, the maintainer script falls back to an instrumental slice from the [garage song](#single-tool--music-25) (see sidecar `doc_fallback`).

</details>

```bash
npx skills add PrunaAI/pruna-skills@stable-audio-2.5 -y
```

---

## Single tool — `whisperx`

**Output** — [`whisperx-drummer-song.json`](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/whisperx-drummer-song.json) (word timestamps from [`music-video-garage-drummer-song.mp3`](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/music-video-garage-drummer-song.mp3))

<details>
<summary>Prompts & inputs</summary>

**Ask your agent**

> Transcribe the garage drummer song with word-level timestamps for lyric-aligned cuts.

</details>

```bash
npx skills add PrunaAI/pruna-skills@whisperx -y
```

---

# Chains (multi-tool)

## Chain — monarch on lavender (`p-image` → `p-image-edit` → `p-video`)

**Output**

<video src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/chain-monarch-clip.mp4" controls width="640"></video>

<details>
<summary>Prompts & inputs</summary>

**Ask your agent**

> Make a short clip of a monarch butterfly on lavender — start with wings closed, edit to wings open, then animate a slow wing spread.

Also demonstrates **`visual-transition-reel`** (start/end plates + motion).

| Step | Model | Prompt |
|------|-------|--------|
| 1 | `p-image` | Monarch on lavender, **wings closed**… |
| 2 | `p-image-edit` | Same stem — **wings open wide**… |
| 3 | `p-video` | Static camera → wings open slowly → one gentle flutter |

| Opening image | Edited end image |
|---------------|------------------|
| ![wings closed](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/chain-monarch-01-open.png) | ![wings open](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/chain-monarch-02-end.png) |

</details>

```bash
npx plugins add PrunaAI/pruna-skills   # pick visual-transition-reel
```

---

## Workflow — `image-to-video`

**Output**

<video src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/image-to-video-aurora-clip.mp4" controls width="640"></video>

<details>
<summary>Prompts & inputs</summary>

**Ask your agent**

> Turn a still of the northern lights over a frozen lake into a short pan clip with drifting snow.

![aurora still](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/image-to-video-aurora-still.png)

</details>

```bash
npx plugins add PrunaAI/pruna-skills   # pick image-to-video
```

---

## Workflow — `visual-transition-reel`

**Output**

<video src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/chain-monarch-clip.mp4" controls width="640"></video>

<details>
<summary>Prompts & inputs</summary>

Same assets as the [monarch chain](#chain--monarch-on-lavender) — hero still → edit end plate → `p-video` between composed frames.

| Opening image | Edited end image |
|---------------|------------------|
| ![wings closed](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/chain-monarch-01-open.png) | ![wings open](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/chain-monarch-02-end.png) |

</details>

```bash
npx plugins add PrunaAI/pruna-skills   # pick visual-transition-reel
```

---

## Workflow — `narrated-multi-scene`

**Output**

<video src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/narrated-multi-scene-demo.mp4" controls width="640"></video>

<details>
<summary>Prompts & inputs</summary>

**Ask your agent**

> Two-scene nature documentary — monarch on lavender, then aurora over a frozen lake — each beat with its own narration and start/end plates, concatenated.

Each scene is one **scene anchor triple** (`p-video` with `image` + `last_frame_image` + uploaded TTS). Assembly is local ffmpeg concat ([workflow SKILL](../workflows/narrated-multi-scene/SKILL.md)).

| Scene | Stills | Narration |
|-------|--------|-----------|
| **1 — Monarch** | [`chain-monarch-01-open.png`](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/chain-monarch-01-open.png) → [`chain-monarch-02-end.png`](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/chain-monarch-02-end.png) | *[calm] On lavender, the monarch rests — wings folded tight, waiting for the morning sun.* |
| **2 — Aurora** | [`image-to-video-aurora-still.png`](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/image-to-video-aurora-still.png) → [`narrated-multi-scene-02-aurora-end.png`](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/narrated-multi-scene-02-aurora-end.png) | *[wonder] By night, the aurora unfurls above the frozen lake — green curtains rippling in silence.* |

Per-scene clips: `narrated-multi-scene-01-monarch.mp4`, `narrated-multi-scene-02-aurora.mp4` · Sidecar lists full scene table.

</details>

```bash
npx plugins add PrunaAI/pruna-skills   # pick narrated-multi-scene
```

---

## Workflow — `avatar-single-scene`

**Output**

<video src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/music-video-garage-drummer-clip.mp4" controls width="360"></video>

<details>
<summary>Prompts & inputs</summary>

**Ask your agent**

> One talking-head clip of the garage drummer singing along to the chorus.

Same performance clip as [music-video](#workflow--music-video) / [`p-video-avatar`](#single-tool--p-video-avatar) — one beat, one plate, one avatar render.

</details>

```bash
npx plugins add PrunaAI/pruna-skills   # pick avatar-single-scene
```

---

## Workflow — `avatar-multi-scene`

**Output — scene 1 (chorus) · scene 2 (count-in)**

| Scene 1 — chorus | Scene 2 — count-in |
|------------------|--------------------|
| <video src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/music-video-garage-drummer-clip.mp4" controls width="240"></video> | <video src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/avatar-multi-scene-02-count-in.mp4" controls width="240"></video> |

<details>
<summary>Prompts & inputs</summary>

**Ask your agent**

> Same drummer presenter across two beats — lock the portrait, different lines per scene.

Same hero still ([`music-video-garage-drummer.png`](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/music-video-garage-drummer.png)) on both **`p-video-avatar`** jobs:

| Scene | Clip | Audio |
|-------|------|-------|
| **1 — Chorus performance** | [`music-video-garage-drummer-clip.mp4`](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/music-video-garage-drummer-clip.mp4) | Song slice |
| **2 — Count-in** | [`avatar-multi-scene-02-count-in.mp4`](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/avatar-multi-scene-02-count-in.mp4) | Gemini TTS count-in |

Sidecar: [`avatar-multi-scene-demo.meta.json`](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/avatar-multi-scene-demo.meta.json)

</details>

```bash
npx plugins add PrunaAI/pruna-skills   # pick avatar-multi-scene
```

---

## Workflow — `interactive-explainer`

**Output — host + B-roll components** (assemble in plan runner)

| Host (`p-video-avatar`) | B-roll (`p-video` + TTS) |
|-------------------------|---------------------------|
| <video src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/music-video-garage-drummer-clip.mp4" controls width="240"></video> | <video src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/illustrated-library-whale-reel.mp4" controls width="240"></video> |

<details>
<summary>Prompts & inputs</summary>

**Ask your agent**

> Educational explainer mixing a talking-head host with narrated B-roll — not VO-only slideshow.

| Beat type | Example asset | Model |
|-----------|---------------|-------|
| Character (host) | [`music-video-garage-drummer-clip.mp4`](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/music-video-garage-drummer-clip.mp4) | `p-video-avatar` |
| Narrator B-roll | [`illustrated-library-whale-reel.mp4`](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/illustrated-library-whale-reel.mp4) | `p-video` + TTS |

</details>

```bash
npx plugins add PrunaAI/pruna-skills   # pick interactive-explainer
```

---

## Workflow — `music-video`

**Output**

<video src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/music-video-garage-drummer-clip.mp4" controls width="360"></video>

<details>
<summary>Prompts & inputs</summary>

**Ask your agent**

> Make a garage-band music video around a teenage girl drummer — song, stills, then performance clips.

![garage drummer](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/music-video-garage-drummer.png)

Pipeline: lyrics → `music-2.5` → slice → `p-video-avatar` → assembly.

</details>

```bash
npx plugins add PrunaAI/pruna-skills   # pick music-video
```

---

## Workflow — `illustrated-story-reel`

**Output**

<video src="https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/illustrated-library-whale-reel.mp4" controls width="640"></video>

<details>
<summary>Prompts & inputs</summary>

**Ask your agent**

> Build an illustrated story reel of a blue whale swimming through a library — paper-cut panels, narration, gentle illustrated motion.

![library whale](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/illustrated-library-whale.png)

**Story reel (`p-video` + Gemini TTS, Mode B)**

> Narration: *[warmly] In a paper-cut library deep below the city, a blue whale swims between the shelves — chasing stories printed on fluttering pages.*

Ken Burns (budget) path uses the same still + [`stable-audio-library-bed.mp3`](https://huggingface.co/datasets/PrunaAI/pruna-skills/resolve/main/examples/stable-audio-library-bed.mp3) or narration-only assembly — see [illustrated-story-reel](../workflows/illustrated-story-reel/SKILL.md).

</details>

```bash
npx plugins add PrunaAI/pruna-skills   # pick illustrated-story-reel
```
