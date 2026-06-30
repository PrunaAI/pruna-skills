# AI music video

Build a lyric-synced music video: **lyrics → MiniMax Music 2.5 song → WhisperX cut alignment → p-video-avatar performance + p-video B-roll → assembly**.

## Quick start prompt

> Use the **ai-music-video** workflow. Genre: indie pop, warm female vocal, 92 BPM, uplifting skills-library theme. Write lyrics with `[Verse]` / `[Chorus]` / `[Inst]` tags — one phrase per line so we never cut mid-word. **Same singer throughout** — lock one hero still, branch performance frames with `p-image-edit`, reuse `project_seed` on avatar clips. After I approve lyrics, generate the song with music-2.5, run **`--phase align`** (WhisperX word timestamps — never use proportional timings for video), then alternate performance avatar clips (audio slices) and cinematic B-roll. 16:9, 720p, 24 fps.

## Copy plan template

```bash
mkdir -p output/verticals/music-video/my-music-video/{clips,audio,stills}
cp catalog/workflows/verticals/music-video/templates/music-video-plan.template.json \
   output/verticals/music-video/my-music-video/music_video_plan.json
```

Edit `lyrics` and `music.prompt`, then follow [examples.md](../../../../catalog/workflows/verticals/music-video/examples.md).

## Install skill bundle

```bash
npx skills add PrunaAI/pruna-ai-content-generation-skills/skills --skill music-video --agent cursor -y
```
