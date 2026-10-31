# Shared video engine

Canonical copy of the course-video tooling. `scripts/sync_video.py <app>` copies it into `<app>/tools/video/` and
the GitHub Actions workflow into `<app>/.github/workflows/`. Edit here, then re-sync every app that has videos.
Process and lessons: `docs/video-course-playbook.md`.

| File | What |
|---|---|
| vid.py | builder: script -> gates -> TTS -> HyperFrames composition -> [--check: layout + STT] -> render |
| layout_lint.js | box checks at every phrase end (out of area, subtitle, presenter, overlap, overflow, squeezed slot) |
| preview.js | screenshots of a composition at given times, without rendering |
| lexicon_base.py | shared pronunciation rules; each app's videos/lexicon.py imports it and adds its terms |
| mathml.js | KaTeX -> MathML (double-struck letters fixed for Chrome) |
| stage.py, video.css, shosh.py | generic widgets, styles, the presenter |
| build_manifest.py, prepare_upload.py, import_youtube_links.py, fetch_renders.py | app manifest, YouTube folder, links, CI downloads |
| render-videos.yml | GitHub Actions: one Windows runner per video |
| app_config_template.py | template for the app's videos/app_config.py |
