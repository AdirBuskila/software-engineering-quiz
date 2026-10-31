# -*- coding: utf-8 -*-
"""Audit the TTS cache of the given videos: report chunks that are missing or truncated (a dropped edge-tts
connection). Usage:  PYTHONUTF8=1 python tools/video/check_tts.py F01 K01 …
"""
import hashlib, json, sys
import vid


def chunks(V):
    for S in V.scenes:
        g = []
        for p in S.phrases:
            g.append(p)
            if p.hold > 0:
                yield " ".join(q.say for q in g)
                g = []
        if g:
            yield " ".join(q.say for q in g)


def main():
    bad = 0
    for vid_id in sys.argv[1:]:
        V, _ = vid.load(vid_id)
        for text in chunks(V):
            h = hashlib.sha1(f"{vid.VOICE}|{vid.RATE}|{text}".encode()).hexdigest()[:16]
            mp3, js = vid.CACHE / f"{h}.mp3", vid.CACHE / f"{h}.json"
            if not (mp3.exists() and js.exists()):
                print(f"{vid_id}: MISSING  {text[:60]}")
                bad += 1
                continue
            import subprocess
            pcm = subprocess.run(["ffmpeg", "-v", "quiet", "-i", str(mp3), "-f", "s16le", "-ac", "1", "-ar",
                                  str(vid.SR), "-"], capture_output=True).stdout
            if not vid._complete(text, json.loads(js.read_text(encoding="utf-8")), pcm):
                print(f"{vid_id}: TRUNCATED  {text[:60]}")
                bad += 1
    print(f"{bad} bad chunks")


if __name__ == "__main__":
    main()
