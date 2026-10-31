# -*- coding: utf-8 -*-
"""Video builder for the guided levels of a course-factory app:  videos/<course>/<ID>/<ID>.py -> videos/out/<ID>/<ID>.mp4

Canonical copy: course-factory/video/ (synced into each app's tools/video/ by course-factory/scripts/sync_video.py;
edit it there, not in the app). App-specific parts live in the app:
  videos/app_config.py   bank path, boss ids, simulator paths, course list, site url (see app_config_template.py)
  videos/lexicon.py      `from lexicon_base import *` + the course's own terms
  videos/widgets/        the course's stage widgets (w_<course>.py), on sys.path

A video script defines VIDEO = Video(...): scenes, each with stage HTML (stage.py / widget helpers), a side panel,
and a list of phrases P(sub, say=None, do=[...]). `sub` is the subtitle in course spelling ($TeX$ allowed); `say` is
what the TTS reads (derived from `sub` through the lexicon when omitted; a TeX span the lexicon can't speak is an
error, so nothing is read wrongly by accident). `do` = show()/hide() actions fired when the phrase starts.

Pipeline: import the script (its simulator asserts run here) -> gates (bank ids/keys, boss ids, no Hebrew in TeX,
subtitle length) -> edge-tts per chunk (cached) -> HyperFrames composition (MathML via KaTeX, mathml.js) -> lint
-> [layout lint] -> render -> loudness normalization -> review frames.

Run:  PYTHONUTF8=1 python tools/video/vid.py T01 [--check] [--no-render] [--draft] [--stt] [--layout] [--workers N]
  --check   everything except the render: gates, TTS, composition + lint, STT and layout lint (the pre-render gate)
  --stt     Hebrew speech-to-text round trip per chunk -> videos/out/<ID>/stt_report.md (needs faster-whisper)
  --layout  layout lint at every phrase end -> videos/out/<ID>/layout_report.md (needs puppeteer-core + Chrome)
"""
import asyncio, difflib, hashlib, importlib.util, json, os, pathlib, re, shutil, subprocess, sys, wave

ENGINE = pathlib.Path(__file__).resolve().parent
TOOLS = ENGINE.parent
ROOT = TOOLS.parent
VIDEOS = ROOT / "videos"
OUT = VIDEOS / "out"
for p in (ENGINE, VIDEOS, VIDEOS / "widgets"):
    sys.path.insert(0, str(p))
import app_config  # noqa: E402
for p in getattr(app_config, "SIM_PATHS", []):
    sys.path.insert(0, str(ROOT / p))
import lexicon  # noqa: E402

VOICE = "he-IL-HilaNeural"
RATE = "-6%"
SR = 24000
HEB = re.compile(r"[֐-׿]")
MATH = re.compile(r"\$([^$]+)\$")
_bank = json.loads((ROOT / getattr(app_config, "BANK", "questions.json")).read_text(encoding="utf-8"))
BANK = {q["id"]: q for q in (_bank["questions"] if isinstance(_bank, dict) else _bank)}


# ----------------------------------------------------------------------------- script DSL
class P:
    """one subtitle line = one narration phrase. hold: silence after it (s); a hold ends the TTS chunk."""
    def __init__(self, sub, say=None, do=(), hold=0.0):
        self.sub, self.say_override, self.do, self.hold = sub, say, list(do), hold

    @property
    def say(self):
        if self.say_override is not None:
            return lexicon.say_hebrew(self.say_override)
        def tex(m):
            s = lexicon.tex_say(m.group(1))
            if s is None:
                raise ValueError(f"no spoken form for ${m.group(1)}$ in: {self.sub}\n  -> give P(..., say=...)")
            return s
        s = MATH.sub(tex, self.sub.replace("**", ""))
        return lexicon.say_hebrew(re.sub(r"<[^>]+>", "", s))


def show(*ids):
    return [("show", i) for i in ids]


def hide(*ids):
    return [("hide", i) for i in ids]


class Scene:
    """layout: 'split' (stage left, panel right), 'full' (stage only), 'title'"""
    def __init__(self, key, label, phrases, stage="", panel="", layout="split"):
        self.key, self.label, self.phrases, self.stage, self.panel, self.layout = key, label, phrases, stage, panel, layout


class Video:
    def __init__(self, id, course, title, scenes, bank=None):
        """bank: {bank_id: option id the video presents as correct} — checked against the app's bank"""
        self.id, self.course, self.title, self.scenes, self.bank = id, course, title, scenes, dict(bank or {})


# ----------------------------------------------------------------------------- loading + gates
def script_path(vid_id):
    hits = list(VIDEOS.glob(f"*/{vid_id}/{vid_id}.py"))
    if len(hits) != 1:
        sys.exit(f"{vid_id}: expected one videos/<course>/{vid_id}/{vid_id}.py, found {hits}")
    return hits[0]


def load(vid_id):
    path = script_path(vid_id)
    spec = importlib.util.spec_from_file_location(f"video_{vid_id}", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)      # simulator asserts run here
    return m.VIDEO, path.parent


def source_hash(vid_id):
    """fingerprint of everything that shapes the MP4: the script, the app's lexicon/config/widgets, the engine.
    Stored next to the MP4; an MP4 whose hash differs is stale (a lexicon change, a widget fix, …)."""
    h = hashlib.sha1()
    files = [script_path(vid_id), VIDEOS / "lexicon.py", VIDEOS / "app_config.py"]
    files += sorted(VIDEOS.glob("lex_*.py"))                     # per-course lexicon additions
    files += sorted((VIDEOS / "widgets").glob("*.py")) + sorted((VIDEOS / "widgets").glob("*.css")) + sorted(ENGINE.glob("*.py")) + sorted(ENGINE.glob("*.css"))
    files += sorted(script_path(vid_id).parent.glob("*.py"))
    for f in dict.fromkeys(files):
        if f.exists():
            h.update(f.name.encode() + b"\0" + f.read_bytes().replace(b"\r\n", b"\n"))   # CRLF checkouts hash alike
    return h.hexdigest()[:16]


def visible_len(sub):
    return len(MATH.sub(lambda m: "x" * max(1, len(m.group(1)) // 2), sub.replace("**", "")))


def gates(V):
    errs = []
    bosses = set(app_config.boss_ids())
    boss_video = app_config.is_boss(V.id)
    for bid, oid in V.bank.items():
        if bid not in BANK:
            errs.append(f"unknown bank id {bid}")
        else:
            q = BANK[bid]       # MCQ keyed by option id, MCQ keyed by index, or an open question (bank={id: None})
            key = q.get("correctId", q.get("correctIndex"))
            if oid != key and oid not in q.get("acceptedIds", []):
                errs.append(f"{bid}: video says {oid}, bank key is {key}")
        if bid in bosses:
            errs.append(f"{bid} is a boss-quiz question" + (" (spoiler)" if boss_video else ""))
    texts = []
    for S in V.scenes:
        texts += [S.stage, S.panel] + [p.sub for p in S.phrases]
        for p in S.phrases:
            if visible_len(p.sub) > 120:
                errs.append(f"[{S.key}] subtitle too long ({visible_len(p.sub)}): {p.sub}")
            try:
                p.say
            except ValueError as e:
                errs.append(f"[{S.key}] {e}")
    for t in texts:
        for m in MATH.finditer(t):
            if HEB.search(m.group(1)):
                errs.append(f"Hebrew inside TeX: ${m.group(1)}$")
    if errs:
        sys.exit("gates failed:\n  " + "\n  ".join(errs))


# ----------------------------------------------------------------------------- TTS + timing
CACHE = OUT / "_tts"
TOK = re.compile(r"[\w֐-׿]+")


async def _tts(text, mp3):
    import edge_tts
    c = edge_tts.Communicate(text, VOICE, rate=RATE, boundary="WordBoundary")
    bounds, audio = [], bytearray()
    async for ch in c.stream():
        if ch["type"] == "audio":
            audio += ch["data"]
        elif ch["type"] == "WordBoundary":
            bounds.append((ch["offset"] / 1e7, ch["text"], ch["duration"] / 1e7))
    mp3.write_bytes(bytes(audio))
    return bounds


def _complete(text, bounds, pcm):
    """edge-tts can drop mid-stream and still return audio: require word events for most of the words, the last
    event near the end of the audio, and a plausible length (Hebrew at this rate: >= ~0.035 s per letter)"""
    words = len(TOK.findall(text))
    dur = len(pcm) / 2 / SR
    if not bounds or len(bounds) < 0.7 * words:
        return False
    if bounds[-1][0] > dur or dur - bounds[-1][0] > 4.0:
        return False
    return dur >= 0.035 * len(re.sub(r"\W", "", text))


def tts(text):
    CACHE.mkdir(parents=True, exist_ok=True)
    h = hashlib.sha1(f"{VOICE}|{RATE}|{text}".encode()).hexdigest()[:16]
    mp3, js = CACHE / f"{h}.mp3", CACHE / f"{h}.json"
    decode = lambda: subprocess.run(["ffmpeg", "-v", "quiet", "-i", str(mp3), "-f", "s16le", "-ac", "1", "-ar", str(SR),
                                     "-"], capture_output=True, check=True).stdout
    for attempt in range(5):
        if js.exists() and mp3.exists():
            pcm, bounds = decode(), json.loads(js.read_text(encoding="utf-8"))
            if _complete(text, bounds, pcm):
                return pcm, bounds
            js.unlink()           # truncated chunk (a dropped connection): never let it into a video
        try:
            js.write_text(json.dumps(asyncio.run(_tts(text, mp3)), ensure_ascii=False), encoding="utf-8")
        except Exception as e:    # "No audio was received" and friends: retry
            print(f"tts retry {attempt + 1}: {e}", file=sys.stderr)
            if js.exists():
                js.unlink()
    sys.exit(f"TTS failed 5 times for: {text[:80]}…")


def phrase_starts(says, bounds, dur):
    """start time of each phrase inside one TTS chunk, by aligning phrase tokens with the word-boundary events"""
    toks, owner = [], []
    for i, s in enumerate(says):
        for t in TOK.findall(s):
            toks.append(t)
            owner.append(i)
    ev_toks, ev_time = [], []
    for b in bounds:
        for w in TOK.findall(b[1]):
            ev_toks.append(w)
            ev_time.append(b[0])
    tok_time = [None] * len(toks)
    for a, b, n in difflib.SequenceMatcher(None, toks, ev_toks, autojunk=False).get_matching_blocks():
        for k in range(n):
            tok_time[a + k] = ev_time[b + k]
    starts = []
    for i in range(len(says)):
        idx = [k for k, o in enumerate(owner) if o == i]
        t = next((tok_time[k] for k in idx if tok_time[k] is not None), None)
        if t is None:   # no matched token: interpolate by token position
            t = dur * (idx[0] / max(1, len(toks))) if idx else (starts[-1] if starts else 0.0)
        starts.append(max(0.0, t - 0.08))
    starts[0] = 0.0
    for i in range(1, len(starts)):
        starts[i] = max(starts[i], starts[i - 1] + 0.3)
    return starts


def build_timeline(V):
    """synthesize every chunk; return (pcm bytes, timeline) with absolute times per phrase and scene"""
    pcm = bytearray()
    t = 0.0
    sil = lambda s: b"\x00\x00" * int(SR * s)
    scenes, phrases, words = [], [], []
    LEAD, SCENE_GAP, CHUNK_GAP = 0.5, 0.7, 0.28
    for S in V.scenes:
        pcm += sil(LEAD)
        t += LEAD
        s_start = t - LEAD
        chunk, groups = [], []
        for p in S.phrases:
            chunk.append(p)
            if p.hold > 0:
                groups.append(chunk)
                chunk = []
        if chunk:
            groups.append(chunk)
        for g in groups:
            text = " ".join(p.say for p in g)
            audio, bounds = tts(text)
            dur = len(audio) / 2 / SR
            starts = phrase_starts([p.say for p in g], bounds, dur)
            for k, b in enumerate(bounds):      # (start, duration) of every spoken word, for Shosh's mouth
                d = b[2] if len(b) > 2 else ((bounds[k + 1][0] if k + 1 < len(bounds) else dur) - b[0]) * 0.8
                words.append((t + b[0], d))
            for k, p in enumerate(g):
                end = t + (starts[k + 1] if k + 1 < len(g) else dur + 0.15)
                phrases.append({"scene": S.key, "p": p, "start": t + starts[k], "end": end, "text": text})
            pcm += audio
            t += dur
            gap = max(CHUNK_GAP, g[-1].hold)
            pcm += sil(gap)
            t += gap
        pcm += sil(SCENE_GAP)
        t += SCENE_GAP
        scenes.append({"scene": S, "start": s_start, "end": t})
    return bytes(pcm), scenes, phrases, words, t


# ----------------------------------------------------------------------------- composition
DISPLAY = re.compile(r"\$\$(.+?)\$\$", re.S)


def render_math(chunks):
    """$TeX$ / $$TeX$$ inside a list of HTML strings -> MathML (KaTeX through mathml.js), same order"""
    items, keyed = [], []
    def grab(display):
        def f(m):
            items.append({"tex": _unescape(m.group(1)), "display": display})
            return f"\x00M{len(items) - 1}\x00"
        return f
    for c in chunks:
        c = DISPLAY.sub(grab(True), c)
        keyed.append(MATH.sub(grab(False), c))
    if not items:
        return keyed
    env = {**os.environ, "NODE_PATH": str(TOOLS / "node_modules")}
    r = subprocess.run(["node", str(ENGINE / "mathml.js")], input=json.dumps({"items": items}), capture_output=True,
                       text=True, encoding="utf-8", env=env)
    if r.returncode != 0:
        sys.exit("mathml.js failed:\n" + r.stderr[-2000:])
    res = json.loads(r.stdout)
    if res["errors"]:
        sys.exit("KaTeX errors:\n  " + "\n  ".join(f"{e['tex']}: {e['err']}" for e in res["errors"]))
    html = res["html"]
    return [re.sub("\x00M(\\d+)\x00", lambda m: html[int(m.group(1))], c) for c in keyed]


def _unescape(tex):
    return tex.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")


def compose(V, scenes, phrases, words, total):
    import shosh
    css = (ENGINE / "video.css").read_text(encoding="utf-8")
    for extra in sorted((VIDEOS / "widgets").glob("*.css")):      # widgets.css + one file per course widget
        css += "\n" + extra.read_text(encoding="utf-8")
    blocks = []
    for sc in scenes:
        S = sc["scene"]
        blocks += [S.stage, S.panel]
    subs = [re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", ph["p"].sub) for ph in phrases]
    rendered = render_math(blocks + subs)
    rb, rs = rendered[:len(blocks)], rendered[len(blocks):]
    body = []
    for i, sc in enumerate(scenes):
        S = sc["scene"]
        stage, panel = rb[2 * i], rb[2 * i + 1]
        top = (f'<header class="top"><span class="vid">{V.id}</span><span class="ttl">{V.title}</span>'
               f'<span class="lbl">{S.label}</span></header>') if S.layout != "title" else ""
        inner = {"split": f'<div class="stage">{stage}</div><aside class="panel">{panel}</aside>',
                 "full": f'<div class="stage full">{stage}</div>',
                 "title": f'<div class="titlecard">{stage}</div>'}[S.layout]
        body.append(f'<section class="scene clip {S.layout}" id="sc-{S.key}" data-start="{sc["start"]:.3f}" '
                    f'data-duration="{sc["end"] - sc["start"]:.3f}">{top}{inner}</section>')
    for i, ph in enumerate(phrases):
        body.append(f'<div class="sub clip" id="sub-{i}" data-start="{ph["start"]:.3f}" '
                    f'data-duration="{ph["end"] - ph["start"]:.3f}"><span>{rs[i]}</span></div>')
    js = []
    for ph in phrases:
        last = {}                       # hide+show of one element in one phrase (a self-loop step): the last wins
        for kind, el in ph["p"].do:
            last.pop(el, None)
            last[el] = kind
        for el, kind in last.items():
            op = 1 if kind == "show" else 0
            js.append(f'tl.to("#{el}",{{opacity:{op},duration:.25}},{ph["start"]:.3f});')
    ids = set(re.findall(r'id="([^"]+)"', "".join(body)))
    missing = sorted({el for ph in phrases for _, el in ph["p"].do} - ids)
    if missing:
        sys.exit(f"actions refer to missing ids: {missing}")
    return f"""<!doctype html>
<html lang="he" dir="rtl"><head><meta charset="utf-8"><title>{V.id}</title><style>{css}</style></head><body>
<div id="root" data-composition-id="root" data-width="1920" data-height="1080" data-start="0" data-duration="{total:.3f}">
{"".join(body)}
{shosh.svg()}
<audio id="narr" src="narration.wav" data-start="0" data-duration="{total:.3f}"></audio>
</div>
<script src="gsap.min.js"></script>
<script>const tl=gsap.timeline({{paused:true}});
{"".join(js)}
{shosh.timeline_js(words, total)}
window.__timelines={{root:tl}};</script>
</body></html>"""


# ----------------------------------------------------------------------------- render + checks
def hf(*args, cwd):
    exe = TOOLS / "node_modules" / ".bin" / ("hyperframes.cmd" if sys.platform == "win32" else "hyperframes")
    # the 60 s stall watchdog tripped on a 9-minute video after every frame was captured, while the encoder drained
    env = {**os.environ, "HF_DE_STALL_MS": os.environ.get("HF_DE_STALL_MS", "600000")}
    return subprocess.run([str(exe), *args], cwd=cwd, env=env, capture_output=True, text=True, encoding="utf-8",
                          errors="replace")


def stt_check(phrases, outdir):
    """Hebrew speech-to-text round trip per chunk: flags chunks whose transcript drifts from the spoken text.
    Also flags known meaning-flipping homophones (lexicon.HOMOPHONES: {heard: what was said}) found in a transcript."""
    import numpy as np
    from faster_whisper import WhisperModel
    m = WhisperModel("ivrit-ai/whisper-large-v3-turbo-ct2", device="cpu", compute_type="int8")
    sym = {**lexicon.DIGIT, "q": "קיו", "a": "איי", "b": "בי", "e": "איי", "i": "איי", "c": "סי", "d": "די",
           "n": "אן", "m": "אם", "k": "קיי", "x": "אקס", "y": "וואי", "z": "זד", "l": "אל", "r": "אר", "t": "טי",
           "s": "אס", "j": "גיי", "w": "דאבליו", "u": "יו", "v": "וי", "p": "פי", "g": "גיי", "f": "אף", "h": "אייץ"}
    homo = getattr(lexicon, "HOMOPHONES", {})

    def norm(s):
        """letters only; the recognizer writes digits/Latin letters (0110, Q0, AB) where we spelled them out"""
        s = re.sub(r"[0-9a-z]", lambda m: sym.get(m.group(0), m.group(0)), s.lower())
        return re.sub(r"[^א-ת]", "", s)
    seen, rows = set(), []
    for ph in phrases:
        if ph["text"] in seen:
            continue
        seen.add(ph["text"])
        pcm, _ = tts(ph["text"])
        a = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
        a = np.interp(np.arange(0, len(a), SR / 16000), np.arange(len(a)), a).astype(np.float32)
        segs, _ = m.transcribe(a, language="he")
        heard = " ".join(s.text.strip() for s in segs)
        r = difflib.SequenceMatcher(None, norm(ph["text"]), norm(heard)).ratio()
        flips = [f"{h}<-{s}" for h, s in homo.items() if h in heard and s in ph["text"] and h not in ph["text"]]
        rows.append((r, ph["scene"], ph["text"], heard, flips))
    rows.sort(key=lambda x: (not x[4], x[0]))
    lines = ["# STT round trip (homophone hits first, then lowest similarity)", "",
             "Similarity of the normalized letters of the spoken text vs the ivrit-ai Whisper transcript.",
             "Digits/letters in the transcript (0110, Q0) vs spelled-out text lower the score; read the flagged rows.", ""]
    for r, sc, said, heard, flips in rows:
        flag = "🔁 " + ", ".join(flips) + " " if flips else ("⚠️ " if r < 0.8 else "")
        lines += [f"- {flag}**{r:.2f}** [{sc}]", f"  - said:  {said}", f"  - heard: {heard}"]
    (outdir / "stt_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    bad = sum(1 for r in rows if r[0] < 0.8)
    hits = sum(1 for r in rows if r[4])
    print(f"stt: {len(rows)} chunks, {bad} below 0.8, {hits} homophone hits -> {outdir / 'stt_report.md'}")
    return hits


def layout_check(proj, phrases, outdir):
    """seek the composition to the end of every phrase and report boxes that leave the stage or run into the
    subtitle / presenter (layout_lint.js). Returns the number of findings."""
    times = [round(p["end"] - 0.05, 3) for p in phrases]
    env = {**os.environ, "NODE_PATH": str(TOOLS / "node_modules")}
    r = subprocess.run(["node", str(ENGINE / "layout_lint.js"), str(proj / "index.html"), json.dumps(times)],
                       capture_output=True, text=True, encoding="utf-8", env=env)
    if r.returncode != 0:
        sys.exit("layout_lint.js failed:\n" + (r.stdout + r.stderr)[-2000:])
    found = json.loads(r.stdout)
    # squeezed = a slot's content is taller than the slot: harmless when nothing is below it, so a warning to look at
    # in a draft frame; everything else is an error. (On automata G05 the real bug showed as squeezed 47px + out-of-area.)
    errors = [f for f in found if f["kind"] != "squeezed"]
    lines = ["# Layout lint (box checks at every phrase end)", "", f"{len(errors)} errors, {len(found) - len(errors)} warnings", ""]
    for f in sorted(found, key=lambda f: (f["kind"] == "squeezed", f["t"])):
        tag = "warning" if f["kind"] == "squeezed" else "ERROR"
        lines.append(f"- {tag} t={f['t']:.1f}s [{phrases[f['i']]['scene']}] {f['kind']}: `{f['what']}` — while: "
                     f"{phrases[f['i']]['p'].sub}")
    (outdir / "layout_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"layout: {len(errors)} errors, {len(found) - len(errors)} warnings -> {outdir / 'layout_report.md'}")
    return len(errors)


def main():
    args = sys.argv[1:]
    vid_id = next(a for a in args if not a.startswith("--") and not a.isdigit())
    workers = args[args.index("--workers") + 1] if "--workers" in args else "4"
    check = "--check" in args
    V, src = load(vid_id)
    gates(V)
    out = OUT / V.id
    proj = out / "proj"
    if proj.exists():
        shutil.rmtree(proj)
    proj.mkdir(parents=True)
    pcm, scenes, phrases, words, total = build_timeline(V)
    if "--stt-only" in args:                        # CI job next to the render: narration -> transcript, no HTML
        stt_check(phrases, out)
        return
    with wave.open(str(proj / "narration.wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm)
    shutil.copy(TOOLS / "node_modules" / "gsap" / "dist" / "gsap.min.js", proj)
    html = compose(V, scenes, phrases, words, total)
    for src_img in set(re.findall(r'src="(images/[^"]+)"', html)):
        dst = proj / src_img
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(ROOT / src_img, dst)
    (proj / "index.html").write_text(html, encoding="utf-8")
    (out / "timeline.json").write_text(json.dumps(
        {"total": total, "scenes": [{"key": s["scene"].key, "start": s["start"], "end": s["end"]} for s in scenes],
         "phrases": [{"scene": p["scene"], "start": p["start"], "end": p["end"], "sub": p["p"].sub, "say": p["p"].say}
                     for p in phrases]}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{V.id}: {len(scenes)} scenes, {len(phrases)} phrases, {total / 60:.1f} min")
    lint = hf("lint", cwd=proj)
    if not re.search(r"\b0 error", lint.stdout):    # warnings are Studio-only (nested <math> in timed divs)
        sys.exit("hyperframes lint failed:\n" + lint.stdout[-3000:])
    problems = 0
    if check or "--layout" in args:
        problems += layout_check(proj, phrases, out)
    if check or "--stt" in args:
        problems += stt_check(phrases, out)
    if check:
        print(f"{V.id}: check done, {problems} findings to read")
        return
    if "--no-render" not in args:
        raw = out / f"{V.id}_raw.mp4"
        r = hf("render", "-o", str(raw), "-q", "draft" if "--draft" in args else "looks", "-w", workers, cwd=proj)
        if r.returncode != 0 or not raw.exists():
            sys.exit("render failed:\n" + (r.stdout + r.stderr)[-3000:])
        final = out / f"{V.id}.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-c:v", "copy", "-af",
                        "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "160k", str(final)],
                       check=True)
        raw.unlink()
        (out / "source_hash.txt").write_text(source_hash(V.id) + "\n", encoding="utf-8")
        frames = out / "frames"
        if frames.exists():
            shutil.rmtree(frames)
        frames.mkdir()
        shots = []
        for s in scenes:
            ps = [p for p in phrases if p["scene"] == s["scene"].key]
            for p in ps[:: max(1, len(ps) // 3)]:
                shots.append((s["scene"].key, p["end"] - 0.05))
            shots.append((s["scene"].key, s["end"] - 0.3))
        for i, (k, t) in enumerate(shots):
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", str(final), "-frames:v", "1",
                            "-vf", "scale=1280:-1", str(frames / f"{i:03d}_{k}_{t:06.1f}.png")], check=True)
        print(f"-> {final}  ({len(shots)} review frames in {frames})")


if __name__ == "__main__":
    main()
