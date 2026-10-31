# -*- coding: utf-8 -*-
"""Map pasted YouTube links to video ids and write videos/youtube.json.

Paste the links (any order, any surrounding text) into a file and run:
  PYTHONUTF8=1 python tools/video/import_youtube_links.py links.txt
Each video's title is read through YouTube's public oEmbed endpoint (works for unlisted videos) and must start with
the video id the upload folder put in the file name ("01 · F01 · …" or "F01 · …"). Then rerun build_manifest.py.
"""
import json, pathlib, re, sys, urllib.parse, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
LINK = re.compile(r"(?:youtu\.be/|youtube\.com/(?:watch\?v=|shorts/|embed/|live/)|studio\.youtube\.com/video/)([\w-]{11})")
VID = re.compile(r"\b([A-Z]\d\d[a-z]?)\b")


def title_of(yid):
    url = "https://www.youtube.com/oembed?format=json&url=" + urllib.parse.quote(f"https://www.youtube.com/watch?v={yid}")
    with urllib.request.urlopen(url, timeout=20) as r:
        return json.load(r)["title"]


def main():
    text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
    ids = list(dict.fromkeys(LINK.findall(text)))
    path = ROOT / "videos" / "youtube.json"
    out = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    for yid in ids:
        try:
            t = title_of(yid)
        except Exception as e:
            print(f"{yid}: cannot read title ({e})")
            continue
        m = VID.search(t)
        if not m:
            print(f"{yid}: no video id in title {t!r}")
            continue
        if m.group(1) in out and out[m.group(1)] != yid:
            print(f"{m.group(1)}: replacing {out[m.group(1)]} with {yid}")
        out[m.group(1)] = yid
        print(f"{m.group(1)} <- {yid}  ({t})")
    path.write_text(json.dumps(dict(sorted(out.items())), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{len(out)} ids in {path}")


if __name__ == "__main__":
    main()
