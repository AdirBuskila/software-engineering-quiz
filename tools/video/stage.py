# -*- coding: utf-8 -*-
"""Stage widgets for the videos: HTML/SVG fragments with stable ids that the timeline shows/hides.

Convention: an element with class `h` starts invisible (opacity 0); actions `show(id)` / `hide(id)` fade it.
Math in HTML fragments is written as $TeX$ and rendered later by the bank's KaTeX pipeline. SVG never contains TeX
(state names are drawn with <tspan> subscripts), so diagrams are exactly the verified machine, nothing more.
"""
import html as _html
import math
import re

R = 44            # state radius (px)


def esc(s):
    return _html.escape(s, quote=True)


def _sub_name(name):
    """'q_0' -> SVG text with a subscript; any other name is drawn as is"""
    m = re.fullmatch(r"q_?\{?(\d+)\}?", name)
    if m:
        return f'q<tspan dy="9" font-size="24">{m.group(1)}</tspan>'
    return esc(name)


def _unit(dx, dy):
    d = math.hypot(dx, dy) or 1.0
    return dx / d, dy / d


def dfa_svg(pfx, D, pos, names, w=900, h=520, bend=None, loops=None, start_side="left", scale=1.15, edges=None):
    """Draw the verified DFA/NFA-like object D (needs .alpha, .delta {(q,a):r}, .start, .acc).

    pos: {state: (x, y)}; names: {state: 'q_0'}; bend: {(p, r): k} curvature override (k>0 bends left of p->r);
    loops: {state: 'up'|'down'}. Works for a DFA (delta values are states), an NFA (delta values are sets,
    letter '' = ε), or any labelled graph via edges=[(p, label, r)] (e.g. PDA labels "a,x→y"). Ids: {pfx}-s-<q> state group, {pfx}-hs-<q> state highlight,
    {pfx}-he-<p>-<r> edge highlight, {pfx}-tag-<q> a hidden caption slot under the state.
    """
    bend = dict(bend or {})
    loops = dict(loops or {})
    pairs = {}
    if edges is not None:
        for p, lab, r in edges:
            pairs.setdefault((p, r), []).append(lab)
    else:
        for (p, a), r in D.delta.items():
            for rr in (sorted(r, key=str) if isinstance(r, (set, frozenset)) else [r]):
                pairs.setdefault((p, rr), []).append(a)
    edges = pairs
    order = {a: i for i, a in enumerate(getattr(D, "alpha", ()))}
    out = [f'<svg class="dfa" id="{pfx}" viewBox="0 0 {w} {h}" width="{w * scale:.0f}" height="{h * scale:.0f}" direction="ltr">',
           '<defs>',
           f'<marker id="{pfx}-ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#c9cdf0"/></marker>',
           f'<marker id="{pfx}-ahh" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#2dd4bf"/></marker>',
           '</defs>']
    base, hi = [], []
    for (p, r), letters in sorted(edges.items(), key=lambda e: (str(e[0][0]), str(e[0][1]))):
        label = ",".join("ε" if a == "" else a for a in sorted(letters, key=lambda a: (order.get(a, 99), a)))
        x1, y1 = pos[p]
        if p == r:
            up = loops.get(p, "up") == "up"
            sgn = -1 if up else 1
            a1, a2 = (-120, -60) if up else (120, 60)
            sx, sy = x1 + R * math.cos(math.radians(a1)), y1 + R * math.sin(math.radians(a1))
            ex, ey = x1 + R * math.cos(math.radians(a2)), y1 + R * math.sin(math.radians(a2))
            cy = y1 + sgn * (R + 78)
            d = f"M{sx:.1f},{sy:.1f} C{x1 - 46:.1f},{cy:.1f} {x1 + 46:.1f},{cy:.1f} {ex:.1f},{ey:.1f}"
            lx, ly = x1, y1 + sgn * (R + 70) + (0 if up else 26)
        else:
            x2, y2 = pos[r]
            k = bend.get((p, r), 0.22 if (r, p) in edges else 0.0)
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ux, uy = _unit(x2 - x1, y2 - y1)
            nx, ny = uy, -ux                       # left normal of p->r (screen coords, y down)
            dist = math.hypot(x2 - x1, y2 - y1)
            cx, cy = mx + nx * k * dist, my + ny * k * dist
            s1 = _unit(cx - x1, cy - y1)
            s2 = _unit(cx - x2, cy - y2)
            sx, sy = x1 + R * s1[0], y1 + R * s1[1]
            ex, ey = x2 + (R + 3) * s2[0], y2 + (R + 3) * s2[1]
            d = f"M{sx:.1f},{sy:.1f} Q{cx:.1f},{cy:.1f} {ex:.1f},{ey:.1f}"
            qx, qy = 0.25 * sx + 0.5 * cx + 0.25 * ex, 0.25 * sy + 0.5 * cy + 0.25 * ey
            side = 1 if k >= 0 else -1
            lx, ly = qx + nx * 26 * side, qy + ny * 26 * side + 10
        base.append(f'<path d="{d}" class="edge" marker-end="url(#{pfx}-ah)"/>'
                    f'<text x="{lx:.1f}" y="{ly:.1f}" class="elabel">{esc(label)}</text>')
        hi.append(f'<path id="{pfx}-he-{p}-{r}" d="{d}" class="edge-hi h" marker-end="url(#{pfx}-ahh)"/>')
    sx0, sy0 = pos[D.start]
    if start_side == "left":
        base.append(f'<path d="M{sx0 - R - 70},{sy0} L{sx0 - R - 4},{sy0}" class="edge" marker-end="url(#{pfx}-ah)"/>')
    else:
        base.append(f'<path d="M{sx0},{sy0 - R - 70} L{sx0},{sy0 - R - 4}" class="edge" marker-end="url(#{pfx}-ah)"/>')
    nodes = []
    for q in sorted(pos, key=str):
        x, y = pos[q]
        ring = f'<circle cx="{x}" cy="{y}" r="{R - 7}" class="node-in"/>' if q in D.acc else ""
        nodes.append(f'<g id="{pfx}-s-{q}"><circle cx="{x}" cy="{y}" r="{R}" class="node"/>{ring}'
                     f'<text x="{x}" y="{y + 9}" class="nlabel">{_sub_name(names[q])}</text></g>'
                     f'<circle id="{pfx}-hs-{q}" cx="{x}" cy="{y}" r="{R + 7}" class="node-hi h"/>')
    out += base + hi + nodes + ["</svg>"]
    return "".join(out)


def dfa_table(pfx, D, names, order=None):
    """δ table, LTR. Ids: {pfx}-c-<q>-<a> cell highlight, {pfx}-row-<q> row highlight."""
    order = order or sorted({q for q, _ in D.delta}, key=str)
    head = "".join(f"<th>${a}$</th>" for a in D.alpha)
    rows = []
    for q in order:
        mark = ("→" if q == D.start else "") + ("*" if q in D.acc else "")
        cells = "".join(f'<td><i id="{pfx}-c-{q}-{a}" class="cell-hi h"></i>${names[D.delta[(q, a)]]}$</td>'
                        for a in D.alpha)
        rows.append(f'<tr><th><i id="{pfx}-row-{q}" class="cell-hi h"></i><span class="mark">{mark}</span>'
                    f'${names[q]}$</th>{cells}</tr>')
    return (f'<table class="delta" id="{pfx}-tab" dir="ltr"><thead><tr><th>$\\delta$</th>{head}</tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table>')


def tape(pfx, word):
    """the input word as boxes; {pfx}-k-<i> = cursor on letter i, {pfx}-d-<i> = letter i already read"""
    cells = "".join(f'<span class="tcell"><i id="{pfx}-d-{i}" class="tdone h"></i><i id="{pfx}-k-{i}" class="tcur h"></i>'
                    f'<b>{esc(c)}</b></span>' for i, c in enumerate(word))
    return f'<div class="tape" id="{pfx}-tape" dir="ltr">{cells}</div>'


def trace(pfx, states, names):
    """q0 → q0 → q1 … revealed step by step: {pfx}-r-<i>"""
    parts = []
    for i, q in enumerate(states):
        arrow = "$\\to$ " if i else ""
        parts.append(f'<span id="{pfx}-r-{i}" class="h">{arrow}${names[q]}$</span>')
    return f'<div class="trace" dir="ltr">{" ".join(parts)}</div>'


def verdict(pfx, ok, yes="מתקבלת ✓", no="לא מתקבלת ✗"):
    return f'<div id="{pfx}-v" class="verdict {"ok" if ok else "bad"} h">{yes if ok else no}</div>'


def card(id_, kind, html_):
    """kind: rule (🔑), trap (⚠️), ex (example box), plain"""
    return f'<div id="{id_}" class="card {kind} h">{html_}</div>'


def options(pfx, opts, notes=None, letters="••••••"):
    """multiple-choice options in the given order. opts: [(oid, html)] — html may be rendered MathML or $TeX$.
    No letters by default: the app shuffles options, so a video must never name one by position.
    notes: {oid: html} short reason shown next to the option. Ids: {pfx}-o-<oid> row, {pfx}-x-<oid> crossed out,
    {pfx}-ok-<oid> marked right, {pfx}-n-<oid> the note."""
    notes = notes or {}
    rows = []
    for (oid, h), L in zip(opts, letters):
        n = f'<span id="{pfx}-n-{oid}" class="onote h">{notes[oid]}</span>' if oid in notes else ""
        rows.append(f'<div class="opt" id="{pfx}-o-{oid}"><span class="ol">{L}</span><span class="ot">{h}</span>{n}'
                    f'<i id="{pfx}-x-{oid}" class="ox h"></i><b id="{pfx}-ok-{oid}" class="ook h">✓</b></div>')
    return f'<div class="opts" id="{pfx}-opts">{"".join(rows)}</div>'


def raster(id_, src, w, size, rings=(), tags=()):
    """an original exam figure (never redrawn) with highlight rings at pixel coords of the source image.
    size = source (w, h); rings: [(name, x, y, r)] -> id {id_}-ring-<name>; tags: [(text, x, y)] small labels."""
    sw, sh = size
    k = w / sw
    h = round(sh * k)
    o = [f'<div class="raster" id="{id_}" style="width:{w}px;height:{h}px"><img src="{esc(src)}" width="{w}" height="{h}">']
    for name, x, y, r in rings:
        o.append(f'<i id="{id_}-ring-{name}" class="ring h" style="left:{(x - r) * k:.0f}px;top:{(y - r) * k:.0f}px;'
                 f'width:{2 * r * k:.0f}px;height:{2 * r * k:.0f}px"></i>')
    for text, x, y in tags:
        o.append(f'<span class="rtag" style="left:{x * k:.0f}px;top:{y * k:.0f}px">{esc(text)}</span>')
    o.append("</div>")
    return "".join(o)
