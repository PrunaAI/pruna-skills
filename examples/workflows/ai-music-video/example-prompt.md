# AI music video

Build a lyric-synced music video: **lyrics → MiniMax Music 2.5 song → cut map → p-video-avatar performance + p-video B-roll → assembly**.

## Quick start prompt

> Use the **ai-music-video** workflow. Genre: indie pop, warm female vocal, 92 BPM, uplifting skills-library theme. Write lyrics with `[Verse]` / `[Chorus]` / `[Inst]` tags — one phrase per line so we never cut mid-word. After I approve lyrics, generate the song with music-2.5, build a cut manifest, then alternate performance avatar clips (audio slices) and cinematic B-roll. 16:9, 1080p.

## Copy plan template

```bash
mkdir -p output/my-music-video/{clips,audio,stills}
cp guides/workflows/ai-music-video/templates/music-video-plan.template.json \
   output/my-music-video/music_video_plan.json
```

Edit `lyrics` and `music.prompt`, then follow [examples.md](../../guides/workflows/ai-music-video/examples.md).

## Install skill bundle

```bash
./scripts/install_skill.sh ai-music-video
```
