# -*- coding: utf-8 -*-
"""Prepare the YouTube upload folder (Adir drags the MP4s into YouTube Studio; then Claude finishes the drafts:
title, description, not-for-kids, Unlisted — see course-factory/docs/video-course-playbook.md).

Writes <dest>/ with one MP4 per video named "NN · <ID> · <title>.mp4" (only characters YouTube keeps in a title;
NN keeps course order), titles_and_descriptions.txt and README.txt (Hebrew). A video is copied only when its MP4
is current: its source_hash.txt matches the scripts, lexicon, widgets and engine as they are now.

Run:  PYTHONUTF8=1 python tools/video/prepare_upload.py ["C:/Users/Adir/Desktop/YouTube upload"] [--only T01,T02,…]
"""
import json, pathlib, re, shutil, sys

ENGINE = pathlib.Path(__file__).resolve().parent
ROOT = ENGINE.parents[1]
sys.path.insert(0, str(ROOT / "videos"))
sys.path.insert(0, str(ENGINE))
import app_config  # noqa: E402

SITE = app_config.SITE
BAD = re.compile(r'[<>:"/\\|?*()]')        # Windows-unsafe characters, and ( ) which Studio drops from titles


def manifest():
    s = (ROOT / "videos.js").read_text(encoding="utf-8")
    return json.loads(s[s.index("{"): s.rindex("}") + 1])


def goal(course, vid, level):
    return app_config.BONUS_GOAL.get(vid) or app_config.level_goal(course, level)


def main():
    import vid as engine
    args = sys.argv[1:]
    only = None
    if "--only" in args:
        i = args.index("--only")
        only = set(args[i + 1].split(","))
        del args[i:i + 2]
    dest = pathlib.Path(args[0] if args else pathlib.Path.home() / "Desktop" / "YouTube upload")
    dest.mkdir(parents=True, exist_ok=True)
    blocks, problems, n = [], [], 0
    for c in manifest()["courses"]:
        for v in c["videos"]:
            n += 1
            vid = v["id"]
            if only is not None and vid not in only:
                continue
            out = ROOT / "videos" / "out" / vid
            mp4 = out / f"{vid}.mp4"
            if not mp4.exists():
                problems.append(f"{vid}: not rendered")
                continue
            h = (out / "source_hash.txt").read_text(encoding="utf-8").strip() if (out / "source_hash.txt").exists() else ""
            if h != engine.source_hash(vid):
                problems.append(f"{vid}: stale (the scripts, lexicon, widgets or engine changed since the render)")
                continue
            title = f"{vid} · {v['title']} | {app_config.APP_NAME}"
            if len(title) > 100:
                title = f"{vid} · {v['title']}"[:100]
            name = BAD.sub("", f"{n:02d} · {vid} · {v['title']}".replace(": ", " · ")) + ".mp4"
            shutil.copy2(mp4, dest / name)
            desc = (f"{c['title']} · {vid}{' (סרטון בונוס)' if v.get('bonus') else ''}\n\n"
                    f"{goal(c['id'], vid, v['level'])}\n\n"
                    "הסבר, דוגמאות שרצות צעד אחר צעד, ושאלה אמיתית ממבחן עם המלכודת שלה — "
                    f"במושגים ובסימונים של הקורס {app_config.APP_NAME} ({app_config.COURSE_CODE}).\n\n"
                    f"לתרגול השלב הזה ולכל שאר הסרטונים: {SITE}?video={vid}\n"
                    "מגישה: שוש 😊")
            blocks.append(f"===== {name}\nכותרת:\n{title}\n\nתיאור:\n{desc}\n")
    (dest / "titles_and_descriptions.txt").write_text("\n".join(blocks), encoding="utf-8")
    (dest / "README.txt").write_text(
        "העלאה ל-YouTube\n"
        "================\n"
        "1. YouTube Studio ← יצירה ← העלאת סרטונים. מסמנים את כל קבצי ה-MP4 וגוררים פנימה.\n"
        "2. כשההעלאה מתחילה אפשר לסגור את החלון. לא צריך למלא כלום.\n"
        "3. אומרים לClaude שהעלית, והוא ישלים את השאר: כותרת, תיאור, לא מיועד לילדים, לא רשום, וחיבור לאתר.\n",
        encoding="utf-8")
    print(f"{len(blocks)} videos -> {dest}")
    if problems:
        print("NOT copied:\n  " + "\n  ".join(problems))


if __name__ == "__main__":
    main()
