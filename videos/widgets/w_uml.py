# -*- coding: utf-8 -*-
"""UML widgets for the uml videos (U01..U09): one SVG canvas (Dia) on which class boxes, use-case ovals with stick
actors, sequence lifelines, statechart states and activity nodes are drawn, every piece in its own <g id> so the
timeline reveals the diagram step by step. Every CSS class is prefixed u-.

Notation (the course's, see courses/uml/U02..U08 and tools/verify/needhelp/uml/check.py):
  inherit  a -> b, hollow triangle at the parent b          comp  filled diamond at the whole a
  aggr     hollow diamond at the whole a                    assoc plain line (nav: open arrowhead at b)
  include  dashed open arrow base -> included, «include»     extend dashed open arrow extension -> base, «extend»
  msg      solid line, filled arrowhead                      ret   dashed line, open arrowhead (return)
  trans / flow  solid line, open arrowhead (statechart transition, activity control flow)

Ids: Dia(pfx).<shape>(key, ...) draws into <g id="{pfx}-{key}">, hidden (class h) unless hidden=False.

Correctness helpers: CHK = the course checker's rule tables and helpers (MODEL, SYMBOL, CLASS_RELATIONS,
USECASE_RELATIONS, SEQ_NOTATION, STATE_COMPONENTS, PURPOSE, NEED, relation_for, container, join_ready,
missing_returns, uc_relation, substate_kind), read from check.py with ast (check.py runs its report on import).
no_latin(scenes) refuses any Latin letter left in the spoken text.
"""
import ast
import html as _html
import math
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]
LATIN = re.compile(r"[A-Za-z]")
HEB = re.compile(r"[֐-׿]")


def esc(s):
    return _html.escape(s, quote=True)


def _h(hidden):
    return "h" if hidden else ""


# ---------------------------------------------------------------- the course checker (read, not run)
_TABLES = {"MODEL", "SYMBOL", "CLASS_RELATIONS", "USECASE_RELATIONS", "SEQ_NOTATION", "STATE_COMPONENTS", "PURPOSE", "NEED"}
_FUNCS = {"relation_for", "container", "join_ready", "missing_returns", "uc_relation", "substate_kind"}


def _checker():
    src = (ROOT / "tools/verify/needhelp/uml/check.py").read_text(encoding="utf-8")
    ns = {}
    for node in ast.parse(src).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and getattr(node.targets[0], "id", None) in _TABLES:
            ns[node.targets[0].id] = ast.literal_eval(node.value)
        elif isinstance(node, ast.FunctionDef) and node.name in _FUNCS:
            exec(compile(ast.Module([node], []), "check.py", "exec"), ns)
    missing = (_TABLES | _FUNCS) - set(ns)
    assert not missing, f"check.py no longer defines {missing}"
    return type("CHK", (), {k: (staticmethod(v) if callable(v) else v) for k, v in ns.items() if k in _TABLES | _FUNCS})


CHK = _checker()


# ---------------------------------------------------------------- text helpers
def L(s):
    """an LTR isolate for Latin / multiplicities inside a Hebrew subtitle (the isolate marks are dropped from speech
    by lex_uml.WORDS)"""
    return "⁦" + s + "⁩"


def ltr_runs(text):
    """escape Hebrew text and wrap each Latin run in an LTR isolate"""
    parts = re.split(r"([A-Za-z<«][A-Za-z0-9_.,()\-'<>«» ]*[A-Za-z0-9)>»])", text)
    return "".join(f'<bdi dir="ltr">{esc(p)}</bdi>' if k % 2 else esc(p) for k, p in enumerate(parts))


def opts_of(q):
    """bank options in bank order as (index, html)"""
    return [(k, ltr_runs(o)) for k, o in enumerate(q["options"])]


def stem(qid, html_):
    return f'<div class="qstem"><span class="qid">{esc(qid)}</span>{html_}</div>'


def stack(*items, gap=22, cls=""):
    return f'<div class="u-stack {cls}" style="gap:{gap}px">{"".join(items)}</div>'


def row(*items, gap=26, cls=""):
    return f'<div class="u-row {cls}" style="gap:{gap}px">{"".join(items)}</div>'


def chip(id_, html_, kind="", hidden=True):
    return f'<span id="{id_}" class="u-chip {kind} {_h(hidden)}">{html_}</span>'


def mono(s):
    return f'<span class="u-mono" dir="ltr">{esc(s)}</span>'


def grid(pfx, rows, head=None, hidden=True, cls=""):
    """a small table; rows: [(key, [cell html, ...])]; row ids {pfx}-{key} (hidden), each row an atom for the lint"""
    h = ""
    if head:
        h = '<div class="u-gr u-gh">' + "".join(f"<span>{c}</span>" for c in head) + "</div>"
    body = "".join(f'<div id="{pfx}-{k}" class="u-gr u-cell {_h(hidden)}">' + "".join(f"<span>{c}</span>" for c in cells)
                   + "</div>" for k, cells in rows)
    return f'<div class="u-grid {cls}" id="{pfx}">{h}{body}</div>'


def no_latin(scenes):
    bad = [(S.key, p.say) for S in scenes for p in S.phrases if LATIN.search(p.say)]
    assert not bad, "Latin letters in spoken text:\n" + "\n".join(f"  [{k}] {s}" for k, s in bad)


# ---------------------------------------------------------------- the canvas
def _clip(shape, px, py):
    """the point where the ray from the shape's centre toward (px, py) leaves the shape"""
    kind, a, b, c, d = shape
    if kind == "pt":
        return a, b
    if kind == "rect":
        cx, cy, hw, hh = a + c / 2, b + d / 2, c / 2, d / 2
        dx, dy = px - cx, py - cy
        if not dx and not dy:
            return cx, cy
        t = min(hw / abs(dx) if dx else math.inf, hh / abs(dy) if dy else math.inf)
        return cx + dx * t, cy + dy * t
    cx, cy, rx, ry = a, b, c, d                  # ellipse
    dx, dy = px - cx, py - cy
    t = 1 / math.sqrt((dx / rx) ** 2 + (dy / ry) ** 2)
    return cx + dx * t, cy + dy * t


def _centre(shape):
    kind, a, b, c, d = shape
    return (a + c / 2, b + d / 2) if kind == "rect" else (a, b)


class Dia:
    MEM = 31          # class member row height
    HEAD = 50         # class name row height

    def __init__(self, pfx, w, h, scale=1.0, cls=""):
        self.pfx, self.w, self.h, self.scale, self.cls = pfx, w, h, scale, cls
        self.parts, self.shapes, self.life = [], {}, {}

    # ------------------------------------------------ plumbing
    def _g(self, key, body, hidden):
        if key is None:
            self.parts.append(body)
        else:
            self.parts.append(f'<g id="{self.pfx}-{key}" class="{_h(hidden)}">{body}</g>')

    def _text(self, x, y, s, cls="u-lab", anchor="middle", size=None):
        heb = bool(HEB.search(s))
        st = f' style="font-size:{size}px"' if size else ""
        return (f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}{" heb" if heb else ""}" text-anchor="{anchor}"'
                f'{" direction=\"rtl\"" if heb else ""}{st}>{esc(s)}</text>')

    def svg(self, hidden=False):
        p = self.pfx
        defs = (f'<marker id="{p}-tri" viewBox="0 0 24 24" refX="23" refY="12" markerWidth="32" markerHeight="32" '
                f'markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1 L23,12 L1,23 z" class="u-m-hol"/></marker>'
                f'<marker id="{p}-dio" viewBox="0 0 34 18" refX="1" refY="9" markerWidth="46" markerHeight="24" '
                f'markerUnits="userSpaceOnUse" orient="auto"><path d="M1,9 L17,1 L33,9 L17,17 z" class="u-m-hol"/></marker>'
                f'<marker id="{p}-dif" viewBox="0 0 34 18" refX="1" refY="9" markerWidth="46" markerHeight="24" '
                f'markerUnits="userSpaceOnUse" orient="auto"><path d="M1,9 L17,1 L33,9 L17,17 z" class="u-m-fil"/></marker>'
                f'<marker id="{p}-opn" viewBox="0 0 20 20" refX="18" refY="10" markerWidth="20" markerHeight="20" '
                f'markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L18,10 L2,18" class="u-m-opn"/></marker>'
                f'<marker id="{p}-sol" viewBox="0 0 20 20" refX="19" refY="10" markerWidth="20" markerHeight="20" '
                f'markerUnits="userSpaceOnUse" orient="auto"><path d="M1,2 L19,10 L1,18 z" class="u-m-fil"/></marker>'
                f'<marker id="{p}-hot" viewBox="0 0 20 20" refX="18" refY="10" markerWidth="22" markerHeight="22" '
                f'markerUnits="userSpaceOnUse" orient="auto"><path d="M2,2 L18,10 L2,18" class="u-m-hot"/></marker>')
        return (f'<svg class="u-dia {self.cls} {_h(hidden)}" id="{p}" viewBox="0 0 {self.w} {self.h}" '
                f'width="{self.w * self.scale:.0f}" height="{self.h * self.scale:.0f}" direction="ltr"><defs>{defs}</defs>'
                + "".join(self.parts) + "</svg>")

    def _ends(self, a, b, via=(), p1=None, p2=None):
        """end points of a connector from shape a to shape b (clipped at both shapes), through `via`"""
        A, B = self.shapes[a], self.shapes[b]
        first = via[0] if via else (p2 or _centre(B))
        last = via[-1] if via else (p1 or _centre(A))
        s = p1 or _clip(A, *first)
        e = p2 or _clip(B, *last)
        return [s, *via, e]

    @staticmethod
    def _d(pts):
        return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)

    # ------------------------------------------------ generic
    def text(self, key, x, y, s, cls="u-lab", anchor="middle", size=None, hidden=True):
        self._g(key, self._text(x, y, s, cls, anchor, size), hidden)

    def ring(self, key, x, y, w, h, rx=16, hidden=True):
        self._g(key, f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" class="u-ring"/>', hidden)

    def cross(self, key, x, y, r=26, hidden=True):
        """a red X over a point (a wrong reading)"""
        self._g(key, f'<path d="M{x - r},{y - r} L{x + r},{y + r} M{x + r},{y - r} L{x - r},{y + r}" class="u-bad"/>', hidden)

    def point(self, key, x, y):
        self.shapes[key] = ("pt", x, y, 0, 0)

    # ------------------------------------------------ class diagram
    def klass(self, key, x, y, w, name, attrs=(), ops=(), stereo=None, hidden=False, hot=False):
        H = self.HEAD + (26 if stereo else 0)
        comps = [attrs, ops] if (attrs or ops) else []
        h = H + sum(12 + self.MEM * max(1, len(c)) for c in comps)
        o = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" class="u-box{" hot" if hot else ""}"/>']
        ty = y + 34
        if stereo:
            o.append(self._text(x + w / 2, y + 26, stereo, "u-stereo"))
            ty += 26
        o.append(self._text(x + w / 2, ty, name, "u-cname"))
        cy = y + H
        for c in comps:
            o.append(f'<line x1="{x}" x2="{x + w}" y1="{cy}" y2="{cy}" class="u-div"/>')
            for k, m in enumerate(c):
                o.append(self._text(x + 14, cy + 30 + k * self.MEM, m, "u-mem", "start"))
            cy += 12 + self.MEM * max(1, len(c))
        self.shapes[key] = ("rect", x, y, w, h)
        self._g(key, "".join(o), hidden)
        return h

    def rel(self, key, a, b, kind, ma=None, mb=None, label=None, via=(), p1=None, p2=None, lxy=None,
            mside=1, hidden=True, hot=False, lanchor="middle"):
        """a connector a -> b. kind: inherit (triangle at b), assoc, nav (open arrow at b), aggr / comp (diamond at a),
        dep (dashed, open arrow at b), include / extend (dashed, open arrow at b, «stereotype»), msg-like flow
        (trans/flow: open arrow at b). ma / mb: multiplicities at the a / b end."""
        pts = self._ends(a, b, via, p1, p2)
        p = self.pfx
        dashed = kind in ("dep", "include", "extend")
        mk = {"inherit": f' marker-end="url(#{p}-tri)"', "nav": f' marker-end="url(#{p}-opn)"',
              "aggr": f' marker-start="url(#{p}-dio)"', "comp": f' marker-start="url(#{p}-dif)"',
              "dep": f' marker-end="url(#{p}-opn)"', "include": f' marker-end="url(#{p}-opn)"',
              "extend": f' marker-end="url(#{p}-opn)"', "trans": f' marker-end="url(#{p}-opn)"',
              "flow": f' marker-end="url(#{p}-opn)"', "assoc": ""}[kind]
        if hot and kind in ("nav", "trans", "flow", "dep", "include", "extend"):
            mk = f' marker-end="url(#{p}-hot)"'
        cls = "u-ln" + (" dash" if dashed else "") + (" hot" if hot else "")
        o = [f'<path d="{self._d(pts)}" class="{cls}"{mk}/>']

        def near(i, j, m, sgn, along):
            """a multiplicity beside the line near end i, on side mside (sgn keeps both labels on the same side)"""
            (x1, y1), (x2, y2) = pts[i], pts[j]
            d = math.hypot(x2 - x1, y2 - y1) or 1
            ux, uy = (x2 - x1) / d, (y2 - y1) / d
            nx, ny = -uy * mside * sgn, ux * mside * sgn
            x, y = x1 + ux * along + nx * 16, y1 + uy * along + ny * 16
            if abs(nx) > 0.3:
                anchor = "start" if nx > 0 else "end"
            else:                                  # beside a horizontal line: run away from the box
                anchor = "start" if ux > 0 else "end"
                x = x1 + ux * 12
            y += 9 + (ny * 14 if abs(ny) > 0.3 else 0) + (10 if uy > 0.3 else (-4 if uy < -0.3 else 0))
            return self._text(x, y, m, "u-mult", anchor)
        if ma:
            o.append(near(0, 1, ma, 1, 62 if kind in ("aggr", "comp") else 24))
        if mb:
            o.append(near(-1, -2, mb, -1, 34 if kind in ("inherit", "nav") else 24))
        if kind in ("include", "extend") and label is None:
            label = f"«{kind}»"
        if label:
            if lxy is None:
                k = len(pts) // 2
                (x1, y1), (x2, y2) = pts[k - 1], pts[k]
                lxy = ((x1 + x2) / 2, (y1 + y2) / 2 - 14)
            o.append(self._text(*lxy, label, "u-stereo" if label.startswith("«") else "u-elab", lanchor))
        self._g(key, "".join(o), hidden)

    # ------------------------------------------------ use-case diagram
    def boundary(self, key, x, y, w, h, title, hidden=False):
        self._g(key, f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" class="u-sys"/>'
                + self._text(x + w / 2, y + 36, title, "u-systitle"), hidden)

    def actor(self, key, x, y, label, hidden=False, s=1.0):
        """a stick figure, head centre (x, y); label under the feet"""
        r = 17 * s
        o = (f'<circle cx="{x}" cy="{y}" r="{r:.1f}" class="u-stick"/>'
             f'<path d="M{x},{y + r:.1f} L{x},{y + 62 * s:.1f} M{x - 30 * s:.1f},{y + 34 * s:.1f} L{x + 30 * s:.1f},{y + 34 * s:.1f} '
             f'M{x},{y + 62 * s:.1f} L{x - 26 * s:.1f},{y + 98 * s:.1f} M{x},{y + 62 * s:.1f} L{x + 26 * s:.1f},{y + 98 * s:.1f}" class="u-stick"/>'
             + self._text(x, y + 132 * s, label, "u-alab"))
        self.shapes[key] = ("rect", x - 34 * s, y - r - 4, 68 * s, 108 * s + r)
        self._g(key, o, hidden)

    def usecase(self, key, cx, cy, rx, ry, label, hidden=False, hot=False):
        lines = label.split("\n")
        t = "".join(self._text(cx, cy + 10 + (k - (len(lines) - 1) / 2) * 34, s, "u-uctext") for k, s in enumerate(lines))
        self.shapes[key] = ("ell", cx, cy, rx, ry)
        self._g(key, f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" class="u-uc{" hot" if hot else ""}"/>' + t, hidden)

    # ------------------------------------------------ sequence diagram
    def lifeline(self, key, x, top, bottom, label, kind="box", w=170, hidden=False):
        """a participant head (box / actor / db) and its dashed lifeline down to `bottom`"""
        self.life[key] = x
        if kind == "actor":
            head = (f'<circle cx="{x}" cy="{top + 16}" r="14" class="u-stick"/>'
                    f'<path d="M{x},{top + 30} L{x},{top + 62} M{x - 24},{top + 42} L{x + 24},{top + 42} M{x},{top + 62} '
                    f'L{x - 20},{top + 88} M{x},{top + 62} L{x + 20},{top + 88}" class="u-stick"/>'
                    + self._text(x, top + 118, label, "u-alab"))
            y0 = top + 130
        elif kind == "db":
            head = (f'<path d="M{x - 52},{top + 14} L{x - 52},{top + 74} A52,14 0 0 0 {x + 52},{top + 74} L{x + 52},{top + 14}" class="u-box"/>'
                    f'<ellipse cx="{x}" cy="{top + 14}" rx="52" ry="14" class="u-box"/>'
                    + self._text(x, top + 58, label, "u-cname"))
            y0 = top + 90
        else:
            head = (f'<rect x="{x - w / 2}" y="{top}" width="{w}" height="64" rx="6" class="u-box"/>'
                    + self._text(x, top + 42, label, "u-cname"))
            y0 = top + 64
        self._g(key, head + f'<line x1="{x}" x2="{x}" y1="{y0}" y2="{bottom}" class="u-life"/>', hidden)

    def act(self, key, who, y1, y2, hidden=True):
        x = self.life[who]
        self._g(key, f'<rect x="{x - 12}" y="{y1}" width="24" height="{y2 - y1}" class="u-act"/>', hidden)

    def msg(self, key, a, b, y, label, ret=False, oa=0, ob=12, hidden=True, hot=False):
        """a message a -> b at height y (oa / ob: offset from the lifeline, e.g. the half width of an activation bar)"""
        xa, xb = self.life[a], self.life[b]
        sgn = 1 if xb > xa else -1
        x1, x2 = xa + sgn * oa, xb - sgn * ob
        p = self.pfx
        mk = f"url(#{p}-hot)" if hot else (f"url(#{p}-opn)" if ret else f"url(#{p}-sol)")
        cls = "u-ln" + (" dash" if ret else "") + (" hot" if hot else "")
        self._g(key, f'<path d="M{x1},{y} L{x2},{y}" class="{cls}" marker-end="{mk}"/>'
                + self._text((x1 + x2) / 2, y - 14, label, "u-elab"), hidden)

    def destroy(self, key, who, y, hidden=True):
        x = self.life[who]
        self._g(key, f'<path d="M{x - 22},{y - 22} L{x + 22},{y + 22} M{x + 22},{y - 22} L{x - 22},{y + 22}" class="u-x"/>', hidden)

    # ------------------------------------------------ statechart / activity
    def state(self, key, x, y, w, h, label, rx=22, hidden=False, hot=False, cls="u-st"):
        lines = label.split("\n")
        t = "".join(self._text(x + w / 2, y + h / 2 + 10 + (k - (len(lines) - 1) / 2) * 32, s, "u-sttext")
                    for k, s in enumerate(lines))
        self.shapes[key] = ("rect", x, y, w, h)
        self._g(key, f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" class="{cls}{" hot" if hot else ""}"/>' + t,
                hidden)

    def action(self, key, x, y, w, h, label, hidden=False, hot=False):
        self.state(key, x, y, w, h, label, rx=h / 2, hidden=hidden, hot=hot, cls="u-acto")

    def initial(self, key, x, y, hidden=False):
        self.shapes[key] = ("ell", x, y, 13, 13)
        self._g(key, f'<circle cx="{x}" cy="{y}" r="13" class="u-dot"/>', hidden)

    def final(self, key, x, y, hidden=False):
        self.shapes[key] = ("ell", x, y, 18, 18)
        self._g(key, f'<circle cx="{x}" cy="{y}" r="18" class="u-stick"/><circle cx="{x}" cy="{y}" r="10" class="u-dot"/>', hidden)

    def bar(self, key, x, y, w, h=12, hidden=False, hot=False):
        """the activity diagram's solid bar (fork / join)"""
        self.shapes[key] = ("rect", x, y, w, h)
        self._g(key, f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" class="u-bar{" hot" if hot else ""}"/>', hidden)

    def region(self, key, x, y, w, h, title, hidden=False):
        """a composite state: a large rounded box with its name in a top strip"""
        self.shapes[key] = ("rect", x, y, w, h)
        self._g(key, f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="26" class="u-comp"/>'
                f'<line x1="{x}" x2="{x + w}" y1="{y + 50}" y2="{y + 50}" class="u-div"/>'
                + self._text(x + w / 2, y + 36, title, "u-sttext"), hidden)

    def divider(self, key, x1, y1, x2, y2, hidden=True):
        self._g(key, f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="u-ln dash"/>', hidden)


# ---------------------------------------------------------------- one small example of each diagram (U01, U08)
def mini(kind, pfx, scale=1.0):
    """a small, fully visible example diagram of a food-delivery app: class / sequence / usecase / state / activity"""
    if kind == "class":
        d = Dia(pfx, 900, 450, scale)
        d.klass("c", 20, 60, 250, "Customer", ["- name : String"], ["+ order()"])
        d.klass("o", 600, 60, 260, "Order", ["- total : int"], ["+ pay()"])
        d.klass("d", 600, 330, 260, "Dish", ["- price : int"])
        d.rel("co", "c", "o", "assoc", ma="1", mb="0..*", hidden=False)
        d.rel("od", "o", "d", "nav", ma="0..*", mb="1..*", mside=-1, hidden=False)
    elif kind == "sequence":
        d = Dia(pfx, 900, 420, scale)
        d.lifeline("u", 110, 0, 410, "לקוח", kind="actor")
        d.lifeline("a", 450, 30, 410, "App")
        d.lifeline("k", 780, 30, 410, "Courier")
        d.act("aa", "a", 180, 380, hidden=False)
        d.act("kk", "k", 240, 320, hidden=False)
        d.msg("m1", "u", "a", 180, "order()", hidden=False)
        d.msg("m2", "a", "k", 240, "assign()", oa=12, hidden=False)
        d.msg("r2", "k", "a", 320, "ok", ret=True, oa=12, hidden=False)
        d.msg("r1", "a", "u", 380, "id", ret=True, oa=12, ob=0, hidden=False)
    elif kind == "usecase":
        d = Dia(pfx, 900, 420, scale)
        d.boundary("sys", 290, 10, 590, 400, "אפליקציית משלוחים")
        d.actor("c", 110, 130, "לקוח")
        d.usecase("u1", 585, 140, 220, 58, "הזמנת מנה")
        d.usecase("u2", 585, 300, 220, 58, "מעקב משלוח")
        d.rel("l1", "c", "u1", "assoc", hidden=False)
        d.rel("l2", "c", "u2", "assoc", hidden=False)
    elif kind == "state":
        d = Dia(pfx, 900, 400, scale)
        d.initial("i", 40, 200)
        d.state("s1", 110, 160, 200, 80, "התקבלה")
        d.state("s2", 400, 160, 180, 80, "בדרך")
        d.state("s3", 680, 160, 200, 80, "נמסרה")
        d.rel("t0", "i", "s1", "trans", hidden=False)
        d.rel("t1", "s1", "s2", "trans", hidden=False, label="pickup", lxy=(355, 140))
        d.rel("t2", "s2", "s3", "trans", hidden=False, label="arrive", lxy=(630, 140))
    elif kind == "activity":
        d = Dia(pfx, 900, 420, scale)
        d.initial("i", 60, 210)
        d.action("a1", 110, 175, 190, 70, "קבלת הזמנה")
        d.bar("f", 340, 90, 14, 240)
        d.action("a2", 400, 70, 180, 70, "בישול")
        d.action("a3", 400, 280, 180, 70, "חיוב")
        d.bar("j", 620, 90, 14, 240)
        d.action("a4", 680, 175, 170, 70, "משלוח")
        d.rel("f0", "i", "a1", "flow", hidden=False)
        d.rel("f1", "a1", "f", "flow", hidden=False)
        d.rel("f2", "f", "a2", "flow", hidden=False, p1=(354, 105))
        d.rel("f3", "f", "a3", "flow", hidden=False, p1=(354, 315))
        d.rel("f4", "a2", "j", "flow", hidden=False, p2=(620, 105))
        d.rel("f5", "a3", "j", "flow", hidden=False, p2=(620, 315))
        d.rel("f6", "j", "a4", "flow", hidden=False)
    else:
        raise ValueError(kind)
    return d.svg()


def code(id_, src, hidden=True):
    """a short Java snippet (escaped); `//` comments dimmed"""
    lines = []
    for ln in src.split("\n"):
        body, _, cm = ln.partition("//")
        lines.append(esc(body) + (f'<span class="c">//{esc(cm)}</span>' if _ else ""))
    return f'<div id="{id_}" class="u-code {_h(hidden)}">' + "\n".join(lines) + "</div>"


def _copy(self, pfx, shown=(), reveal=False, hidden=False, keep=()):
    """the same diagram under another id prefix (for a later scene): groups in `shown` (keys) start visible,
    or every group when reveal=True"""
    s = self.svg(hidden=hidden)
    for k in shown:
        s = s.replace(f'<g id="{self.pfx}-{k}" class="h">', f'<g id="{self.pfx}-{k}" class="">')
    if reveal:
        s = s.replace(' class="h">', ' class="">')
        for k in keep:                         # ... except these (rings, cursors)
            s = s.replace(f'<g id="{self.pfx}-{k}" class="">', f'<g id="{self.pfx}-{k}" class="h">')
    s = s.replace(f'id="{self.pfx}"', f'id="{pfx}"').replace(f'id="{self.pfx}-', f'id="{pfx}-')
    return s.replace(f'url(#{self.pfx}-', f'url(#{pfx}-')


Dia.copy = _copy


def _hline(self, key, x1, x2, y, label=None, hidden=True):
    """a highlighted horizontal 'now' line across a sequence diagram"""
    t = self._text(x2 + 8, y + 9, label, "u-lab warn", "start") if label else ""
    self._g(key, f'<line x1="{x1}" x2="{x2}" y1="{y}" y2="{y}" class="u-now"/>' + t, hidden)


Dia.hline = _hline
