# -*- coding: utf-8 -*-
"""Download the MP4s of a render-videos workflow run into videos/out/<ID>/ (mp4, frames, timeline, source hash).

usage:  PYTHONUTF8=1 python tools/video/fetch_renders.py <run id>      (needs the gh CLI, logged in)
Prints, per video, whether its source hash matches the current scripts (a mismatch = stale, render again).
"""
import pathlib, shutil, subprocess, sys, tempfile

ENGINE = pathlib.Path(__file__).resolve().parent
ROOT = ENGINE.parents[1]
OUT = ROOT / "videos" / "out"


def main():
    run = sys.argv[1]
    sys.path.insert(0, str(ENGINE))
    import vid
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["gh", "run", "download", run, "-D", tmp], cwd=ROOT, check=True)
        for art in sorted(pathlib.Path(tmp).iterdir()):
            vid_id = art.name.removeprefix("video-")
            dst = OUT / vid_id
            dst.mkdir(parents=True, exist_ok=True)
            for f in art.iterdir():
                target = dst / f.name
                if target.is_dir():
                    shutil.rmtree(target)
                (shutil.copytree if f.is_dir() else shutil.copy2)(f, target)
            h = (dst / "source_hash.txt").read_text(encoding="utf-8").strip() if (dst / "source_hash.txt").exists() else ""
            state = "current" if h and h == vid.source_hash(vid_id) else "STALE (scripts changed since this render)"
            print(f"{vid_id}: {state}")


if __name__ == "__main__":
    main()
