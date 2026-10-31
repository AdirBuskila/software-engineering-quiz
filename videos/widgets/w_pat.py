# -*- coding: utf-8 -*-
"""Design-patterns widgets for the pat videos (P01..P09): UML-style class boxes with arrows that appear step by step,
Java code panels whose lines light up, small chip rows, and the checks every script runs.

Ids:
  uml(pfx, boxes, links):  {pfx}-b-<key> class box (group), {pfx}-hb-<key> its highlight ring,
                           {pfx}-a-<key> an arrow (with its label)
  code(pfx, src):          {pfx}-l<k> line k, {pfx}-m<k> the highlight bar behind line k
  swap(pfx, items):        {pfx}-<k> layer k of a slot that shows one item at a time

Correctness helpers:
  RULES / OBSERVER_OPS     read (not run) from tools/verify/needhelp/pat/check.py: the course checker's rule table
  java(files, main, out)   compiles and runs the Java shown on screen when a JDK is present (asserts the output);
                           expect_compile_error() asserts that javac refuses a snippet (e.g. new on a private constructor)
  no_latin(scenes)         the voice misreads Latin letters: every spoken phrase must be Hebrew and digits only
"""
import ast
import html as _html
import pathlib
import re
import shutil
import subprocess
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
LATIN = re.compile(r"[A-Za-z]")


def esc(s):
    return _html.escape(s, quote=True)


def _h(hidden):
    return " h" if hidden else ""


# ---------------------------------------------------------------- the course checker's rule table (read, not run)
def _checker_literals():
    src = (ROOT / "tools/verify/needhelp/pat/check.py").read_text(encoding="utf-8")
    out = {}
    for node in ast.parse(src).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name in ("PATTERNS", "OBSERVER_OPS"):
                out[name] = ast.literal_eval(node.value)
    return out


_LIT = _checker_literals()
RULES = _LIT["PATTERNS"]               # {pattern: {"family": ..., "solves": {...}}}
OBSERVER_OPS = _LIT["OBSERVER_OPS"]    # {op: "Subject" | "Observer"}


def solves(p, needs):
    return set(needs) <= RULES[p]["solves"]


def family(p):
    return RULES[p]["family"]


# ---------------------------------------------------------------- Java: compile and run what is shown
def _jdk():
    return shutil.which("javac") and shutil.which("java")


def java(files, main, expect):
    """files: {ClassName: source}. Compiles them, runs `main`, asserts stdout == expect. Skipped without a JDK
    (the CI render runners); the scripts are checked locally, where javac exists."""
    if not _jdk():
        return None
    with tempfile.TemporaryDirectory() as d:
        for name, src in files.items():
            (pathlib.Path(d) / f"{name}.java").write_text(src, encoding="utf-8")
        r = subprocess.run(["javac", "-d", d, *[f"{n}.java" for n in files]], cwd=d, capture_output=True, text=True)
        assert r.returncode == 0, "javac failed:\n" + r.stdout + r.stderr
        r = subprocess.run(["java", "-cp", d, main], capture_output=True, text=True)
        assert r.returncode == 0, r.stderr
        got = r.stdout.replace("\r\n", "\n").strip()
        assert got == expect.strip(), f"java output:\n{got}\n!= expected:\n{expect}"
        return got


def expect_compile_error(files, needle):
    """javac must refuse these files with a message containing `needle`"""
    if not _jdk():
        return None
    with tempfile.TemporaryDirectory() as d:
        for name, src in files.items():
            (pathlib.Path(d) / f"{name}.java").write_text(src, encoding="utf-8")
        r = subprocess.run(["javac", "-d", d, *[f"{n}.java" for n in files]], cwd=d, capture_output=True, text=True)
        assert r.returncode != 0 and needle in (r.stdout + r.stderr), r.stdout + r.stderr
        return True


# ---------------------------------------------------------------- code panel (Java)
KW = (r"\b(abstract|class|interface|implements|extends|public|private|protected|static|final|new|return|if|else|"
      r"void|null|this|for|while|true|false|int|boolean)\b")


def _hl_plain(s):
    s = esc(s)
    s = re.sub(KW, r'<span class="pt-kw">\1</span>', s)
    s = re.sub(r"(?<![\w.])(\d+)", r'<span class="pt-num">\1</span>', s)
    return s


def _hl(line):
    out, pos = [], 0
    for m in re.finditer(r'("[^"]*"|//.*$)', line):
        out.append(_hl_plain(line[pos:m.start()]))
        cls = "pt-cm" if m.group(0).startswith("//") else "pt-str"
        out.append(f'<span class="{cls}">{esc(m.group(0))}</span>')
        pos = m.end()
    out.append(_hl_plain(line[pos:]))
    return "".join(out)


def code(pfx, src, hidden=False, size=26, lines_hidden=(), title=None):
    """a Java panel; lines_hidden: line numbers that start invisible (they appear with show(f'{pfx}-l{k}'))"""
    lines = src.split("\n")
    body = "".join(f'<div id="{pfx}-l{k}" class="pt-ln{_h(k in lines_hidden)}"><i id="{pfx}-m{k}" class="pt-mark h"></i>'
                   f'<span class="pt-tx">{_hl(l) or "&nbsp;"}</span></div>' for k, l in enumerate(lines))
    head = f'<div class="pt-ctitle">{esc(title)}</div>' if title else ""
    return f'<div class="pt-code{_h(hidden)}" id="{pfx}" dir="ltr" style="font-size:{size}px">{head}{body}</div>'


def out(pfx, text, hidden=True, size=24, label="פלט"):
    body = "".join(f'<div>{esc(l) or "&nbsp;"}</div>' for l in text.split("\n"))
    return (f'<div class="pt-out{_h(hidden)}" id="{pfx}" style="font-size:{size}px"><span class="pt-olab">{label}</span>'
            f'<div class="pt-obody" dir="ltr">{body}</div></div>')


# ---------------------------------------------------------------- UML class diagram
HEAD, STEREO, MEM = 50, 26, 34


def box_h(b):
    return HEAD + (STEREO if b.get("kind") in ("interface", "abstract") else 0) + (12 + MEM * len(b.get("members", ())) if b.get("members") else 0)


def _rect(b):
    return b["x"], b["y"], b["w"], box_h(b)


def _anchor(r, side, frac=0.5):
    x, y, w, h = r
    return {"t": (x + w * frac, y), "b": (x + w * frac, y + h), "l": (x, y + h * frac), "r": (x + w, y + h * frac)}[side]


def _sides(ra, rb):
    ax, ay = ra[0] + ra[2] / 2, ra[1] + ra[3] / 2
    bx, by = rb[0] + rb[2] / 2, rb[1] + rb[3] / 2
    if abs(by - ay) > 0.6 * abs(bx - ax):
        return ("b", "t") if by > ay else ("t", "b")
    return ("r", "l") if bx > ax else ("l", "r")


def uml(pfx, boxes, links=(), w=1000, h=600, scale=1.0, hidden=False):
    """boxes: [{key, name, x, y, w, kind: class|interface|abstract, members: [str], role: Hebrew tag, hidden: bool}]
    links: [{key, a, b, kind: inherit|impl|has|call|flow, label, sides: 'bt', fa/fb: anchor fractions, hidden}]
      inherit / impl: a is the child, a hollow triangle at b (impl dashed).  has: a hollow diamond at a (a holds b).
      call: an open arrow a -> b (dep: dashed, e.g. «creates»).  flow: a thick teal arrow a -> b (data / control flow)."""
    B = {b["key"]: b for b in boxes}
    o = [f'<svg class="pt-uml{_h(hidden)}" id="{pfx}" viewBox="0 0 {w} {h}" width="{w * scale:.0f}" height="{h * scale:.0f}" '
         f'direction="ltr"><defs>'
         f'<marker id="{pfx}-tri" viewBox="0 0 20 20" refX="19" refY="10" markerWidth="22" markerHeight="22" '
         f'markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L19,10 L1,19 z" class="pt-mtri"/></marker>'
         f'<marker id="{pfx}-dia" viewBox="0 0 28 16" refX="1" refY="8" markerWidth="30" markerHeight="17" '
         f'markerUnits="userSpaceOnUse" orient="auto"><path d="M1,8 L14,1 L27,8 L14,15 z" class="pt-mdia"/></marker>'
         f'<marker id="{pfx}-opn" viewBox="0 0 20 20" refX="18" refY="10" markerWidth="18" markerHeight="18" '
         f'markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L18,10 L2,18" class="pt-mopn"/></marker>'
         f'<marker id="{pfx}-flw" viewBox="0 0 20 20" refX="16" refY="10" markerWidth="24" markerHeight="24" '
         f'markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L19,10 L1,19 z" class="pt-mflw"/></marker>'
         f'</defs>']
    for L in links:
        ra, rb = _rect(B[L["a"]]), _rect(B[L["b"]])
        sa, sb = tuple(L["sides"]) if L.get("sides") else _sides(ra, rb)
        x1, y1 = _anchor(ra, sa, L.get("fa", 0.5))
        x2, y2 = _anchor(rb, sb, L.get("fb", 0.5))
        kind = L["kind"]
        if L.get("elbow") and sa in "tb" and sb in "tb" and abs(x1 - x2) > 1:      # vertical - horizontal - vertical
            ym = (y1 + y2) / 2
            d = f"M{x1:.1f},{y1:.1f} L{x1:.1f},{ym:.1f} L{x2:.1f},{ym:.1f} L{x2:.1f},{y2:.1f}"
        else:
            d = f"M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}"
        cls = {"inherit": "pt-ln-s", "impl": "pt-ln-d", "has": "pt-ln-s", "call": "pt-ln-s", "dep": "pt-ln-d",
               "flow": "pt-ln-f"}[kind]
        start = f' marker-start="url(#{pfx}-dia)"' if kind == "has" else ""
        end = {"inherit": "tri", "impl": "tri", "has": "opn", "call": "opn", "dep": "opn", "flow": "flw"}[kind]
        lab = ""
        if L.get("label"):
            lx, ly = L.get("lxy", ((x1 + x2) / 2 + 14, (y1 + y2) / 2 - 10))
            heb = bool(re.search(r"[֐-׿]", L["label"]))
            lab = (f'<text x="{lx:.1f}" y="{ly:.1f}" class="pt-alab{" heb" if heb else ""}"'
                   f'{" direction=\"rtl\"" if heb else ""} text-anchor="{L.get("anchor", "start")}">{esc(L["label"])}</text>')
        o.append(f'<g id="{pfx}-a-{L["key"]}" class="{_h(L.get("hidden", True)).strip()}">'
                 f'<path d="{d}" class="{cls}"{start} marker-end="url(#{pfx}-{end})"/>{lab}</g>')
    for b in boxes:
        x, y, bw, bh = _rect(b)
        kind = b.get("kind", "class")
        parts = [f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="10" class="pt-box {kind}"/>']
        ty = y + 36
        if kind in ("interface", "abstract"):
            st_txt = "«interface»" if kind == "interface" else "{abstract}"
            parts.append(f'<text x="{x + bw / 2}" y="{y + 26}" class="pt-stereo">{esc(st_txt)}</text>')
            ty += STEREO
        parts.append(f'<text x="{x + bw / 2}" y="{ty}" class="pt-name{" it" if kind == "abstract" else ""}">{esc(b["name"])}</text>')
        if b.get("members"):
            sy = y + HEAD + (STEREO if kind in ("interface", "abstract") else 0)
            parts.append(f'<line x1="{x}" x2="{x + bw}" y1="{sy}" y2="{sy}" class="pt-div"/>')
            for k, m in enumerate(b["members"]):
                parts.append(f'<text x="{x + 16}" y="{sy + 34 + k * MEM}" class="pt-mem">{esc(m)}</text>')
        if b.get("role"):
            parts.append(f'<text x="{x + bw / 2}" y="{y + bh + 34}" class="pt-role" direction="rtl">{esc(b["role"])}</text>')
        ring = (f'<rect id="{pfx}-hb-{b["key"]}" x="{x - 8}" y="{y - 8}" width="{bw + 16}" height="{bh + 16}" rx="14" '
                f'class="pt-ring h"/>')
        o.append(f'<g id="{pfx}-b-{b["key"]}" class="{_h(b.get("hidden", False)).strip()}">{"".join(parts)}</g>{ring}')
    o.append("</svg>")
    return "".join(o)


# ---------------------------------------------------------------- small layout pieces
def stack(*items, gap=22, cls=""):
    return f'<div class="pt-stack {cls}" style="gap:{gap}px">{"".join(items)}</div>'


def row(*items, gap=26, cls=""):
    return f'<div class="pt-row {cls}" style="gap:{gap}px">{"".join(items)}</div>'


def chip(id_, html_, kind="", hidden=True):
    return f'<span id="{id_}" class="pt-chip {kind}{_h(hidden)}">{html_}</span>'


def mono(s):
    return f'<span class="pt-mono" dir="ltr">{esc(s)}</span>'


def stem(qid, html_):
    return f'<div class="qstem"><span class="qid">{esc(qid)}</span>{html_}</div>'


def swap(pfx, items, height, first_visible=True, width=None):
    """one slot, several layers (ids {pfx}-0, {pfx}-1, …): hide the old one and show the next in the same phrase"""
    w = f"width:{width}px;" if width else ""
    layers = "".join(f'<div id="{pfx}-{k}" class="{_h(k > 0 or not first_visible).strip()}">{it}</div>'
                     for k, it in enumerate(items))
    return f'<div class="swap pt-swap" id="{pfx}" style="--swap-h:{height}px;{w}">{layers}</div>'


def need(id_, need_html, pattern, hidden=True):
    """a 'need -> pattern' line: the need in Hebrew, an arrow, the pattern name"""
    return (f'<div id="{id_}" class="pt-need{_h(hidden)}"><span class="pt-nd">{need_html}</span><span class="pt-arr">←</span>'
            f'<span class="pt-pat">{esc(pattern)}</span></div>')


def roster(pfx, names, label="", hidden=False):
    """the Subject's list of observers as chips (one version of it)"""
    chips = "".join(f'<span class="pt-chip obs">{esc(n)}</span>' for n in names) or '<span class="pt-empty">(ריקה)</span>'
    lab = f'<span class="pt-rlab">{label}</span>' if label else ""
    return f'<div id="{pfx}" class="pt-roster{_h(hidden)}">{lab}<span class="pt-rchips" dir="ltr">{chips}</span></div>'


# ---------------------------------------------------------------- script checks
def no_latin(scenes):
    bad = [(S.key, p.say) for S in scenes for p in S.phrases if LATIN.search(p.say)]
    assert not bad, "Latin letters in spoken text:\n" + "\n".join(f"  [{k}] {s}" for k, s in bad)


def opts_of(q):
    """bank options in bank order as (index, html); Latin runs are isolated so they read LTR inside the RTL row"""
    return [(k, ltr_runs(o)) for k, o in enumerate(q["options"])]


def ltr_runs(text):
    """escape Hebrew text and wrap each Latin run in an LTR isolate"""
    parts = re.split(r"([A-Za-z][A-Za-z0-9_.()\-' ]*[A-Za-z0-9)])", text)
    return "".join(f'<bdi dir="ltr">{esc(p)}</bdi>' if k % 2 else esc(p) for k, p in enumerate(parts))


def tight(html_):
    """wrap a panel whose exam options are long (smaller type)"""
    return f'<div class="pt-tight">{html_}</div>'


def reprefix(html_, old, new, reveal=False):
    """a copy of a widget under a new id prefix (ids and marker references); reveal=True drops the hidden class"""
    s = html_.replace(f'id="{old}', f'id="{new}').replace(f"url(#{old}-", f"url(#{new}-")
    if reveal:
        s = s.replace('class="h"', 'class=""')
    return s
