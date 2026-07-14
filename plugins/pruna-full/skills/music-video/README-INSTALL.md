# music-video

Portable install:

```bash
npx skills add PrunaAI/pruna-skills/plugins/music-video/skills --skill music-video --agent cursor -y
```

Requires `REPLICATE_API_TOKEN`, `PRUNA_API_KEY`, `ffmpeg`, and `ffprobe`.

Copy [`templates/music-video-plan.template.json`](./templates/music-video-plan.template.json) to your output folder and edit lyrics before running `generate_song.py`.
