# -*- coding: utf-8 -*-
"""Process / Agile / requirements widgets for the proc videos (R01..R09). Every CSS class is prefixed pr-.

  cascade(pfx, steps)        the Waterfall staircase (SVG): {pfx}-s<k> step, {pfx}-a<k> arrow k -> k+1,
                             {pfx}-hs<k> step highlight, {pfx}-back the dashed "change goes back" arrow
  cycle(pfx, nodes)          the Scrum sprint loop (SVG): {pfx}-n-<key> node, {pfx}-h-<key> its highlight,
                             {pfx}-e<k> arc k (node k -> node k+1), {pfx}-loop the daily self-loop, {pfx}-mid centre text
  board(pfx, cols, cards)    a sorting board: every card starts in the pool ({pfx}-p-<key}); "moving" it = hide the pool
                             card and show its copy in the column ({pfx}-c-<key>), which may carry a reason ({pfx}-w-<key>)
  backlog(pfx, items, ...)   Product Backlog (all items, priority order) and Sprint Backlog (copies of the chosen ones):
                             {pfx}-ph-<k> highlight in the product list, {pfx}-s-<k> the copy in the sprint list
  table(pfx, head, rows)     a small RTL table, rows {pfx}-r<k} (hidden unless shown=True), row highlight {pfx}-m<k>
  swap(pfx, items, h)        one slot, several layers {pfx}-<k>

Correctness: CHK = the course checker's rule tables (SUITS, OWNER, SCRUM_ROLES, SM_TASKS, EVENT, DAILY, ELICITATION,
REQ), read from tools/verify/needhelp/proc/check.py with ast (the checker runs node on import, so it is not imported),
plus the checker's own classify() and good_requirement() rules re-stated below and asserted against its REQ table.
no_latin(scenes): the voice misreads Latin letters, so every spoken phrase must be Hebrew and digits only.
"""
import ast
import html as _html
import math
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]
LATIN = re.compile(r"[A-Za-z]")


def esc(s):
    return _html.escape(s, quote=True)


def _h(hidden):
    return " h" if hidden else ""


# ---------------------------------------------------------------- the course checker's tables (read, not run)
_WANT = {"SUITS", "OWNER", "SCRUM_ROLES", "SM_TASKS", "EVENT", "DAILY", "ELICITATION", "REQ", "BAD_FOR_WATERFALL",
         "PRACTICE", "FACTS", "COST_PEAK", "ESTIMATION"}


def _checker():
    src = (ROOT / "tools/verify/needhelp/proc/check.py").read_text(encoding="utf-8")
    out = {}
    for node in ast.parse(src).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            if node.targets[0].id in _WANT:
                out[node.targets[0].id] = ast.literal_eval(node.value)
    return out


CHK = _checker()
assert _WANT <= set(CHK), _WANT - set(CHK)


def classify(is_action, is_quality_or_constraint):
    """the checker's rule (check.py R07): an action with no quality/limit/technology constraint is functional"""
    return "functional" if is_action and not is_quality_or_constraint else "non-functional"


def good_requirement(testable, describes_what_not_how):
    """the checker's rule (check.py R08)"""
    return testable and describes_what_not_how


# the re-stated classifier agrees with the checker's own verdicts on its REQ table (check.py asserts these keys)
assert classify(*CHK["REQ"]["send_sms_reminder"]) == "functional"
assert classify(*CHK["REQ"]["report_in_3s"]) == "non-functional"
assert classify(*CHK["REQ"]["aes_passwords"]) == "non-functional"
assert classify(*CHK["REQ"]["home_under_2s_95"]) == "non-functional"


def fits(model, needs):
    return set(needs) <= CHK["SUITS"][model]


# ---------------------------------------------------------------- small layout pieces
def stack(*items, gap=22, cls=""):
    return f'<div class="pr-stack {cls}" style="gap:{gap}px">{"".join(items)}</div>'


def row(*items, gap=26, cls=""):
    return f'<div class="pr-row {cls}" style="gap:{gap}px">{"".join(items)}</div>'


def chip(id_, html_, kind="", hidden=True):
    return f'<span id="{id_}" class="pr-chip {kind}{_h(hidden)}">{html_}</span>'


def en(s):
    """an English term inside Hebrew HTML: Segoe UI, isolated LTR"""
    return f'<bdi class="pr-en" dir="ltr">{esc(s)}</bdi>'


def stem(qid, html_):
    return f'<div class="qstem pr-qstem"><span class="qid">{esc(qid)}</span>{html_}</div>'


def ltr_runs(text):
    """escape Hebrew text and wrap each Latin run in an LTR isolate"""
    parts = re.split(r"(\(?[A-Za-z][A-Za-z0-9_.()\-' ]*[A-Za-z0-9)])", text)
    return "".join(f'<bdi dir="ltr">{esc(p)}</bdi>' if k % 2 else esc(p) for k, p in enumerate(parts))


def opts_of(q, short=None):
    """bank options in bank order as (index, html). short: {index: shorter display text} for very long options
    (the stem panel is narrow); every shortened text must keep the option's meaning."""
    short = short or {}
    out = [(k, ltr_runs(short.get(k, o))) for k, o in enumerate(q["options"])]
    # "all the other answers ..." always renders last in the app: show it last here too
    return sorted(out, key=lambda kv: q["options"][kv[0]].startswith("כל התשובות"))


def swap(pfx, items, height, first_visible=True, width=None):
    w = f"width:{width}px;" if width else ""
    layers = "".join(f'<div id="{pfx}-{k}" class="{_h(k > 0 or not first_visible).strip()}">{it}</div>'
                     for k, it in enumerate(items))
    return f'<div class="swap pr-swap" id="{pfx}" style="--swap-h:{height}px;{w}">{layers}</div>'


def table(pfx, head, rows, shown=False, widths=None, size=28):
    """head: [html]; rows: [[html]] (RTL). Row k: {pfx}-r<k> (hidden unless shown), highlight {pfx}-m<k>."""
    widths = widths or [None] * len(head)
    th = "".join(f'<th style="width:{w}px">{h}</th>' if w else f"<th>{h}</th>" for h, w in zip(head, widths))
    body = []
    for k, r in enumerate(rows):
        cells = "".join(f"<td>{c}</td>" for c in r)
        body.append(f'<tr id="{pfx}-r{k}" class="{"" if shown else "h"}">{cells.replace("<td>", f"<td><i id=\"{pfx}-m{k}\" class=\"pr-mk h\"></i>", 1)}</tr>')
    return (f'<table class="pr-tab" id="{pfx}" dir="rtl" style="font-size:{size}px">'
            f'<thead><tr>{th}</tr></thead><tbody>{"".join(body)}</tbody></table>')


# ---------------------------------------------------------------- Waterfall staircase
def cascade(pfx, steps, w=1000, h=520, bw=250, bh=78, rtl=True, back=None, hidden_steps=True, scale=1.0):
    """steps: [(hebrew, english or '')] top to bottom. rtl: the staircase descends from the top-right to the bottom-left.
    back: (from_k, to_k, label) a dashed red arrow from step from_k back up to step to_k (hidden, id {pfx}-back)."""
    n = len(steps)
    dx = (w - bw - 20) / (n - 1)
    dy = (h - bh - 20) / (n - 1)
    pos = []
    for k in range(n):
        x = (w - bw - 10 - k * dx) if rtl else (10 + k * dx)
        pos.append((x, 10 + k * dy))
    o = [f'<svg class="pr-svg" id="{pfx}" viewBox="0 0 {w} {h}" width="{w * scale:.0f}" height="{h * scale:.0f}" direction="ltr">',
         f'<defs><marker id="{pfx}-ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto">'
         f'<path d="M0,0 L10,5 L0,10 z" fill="#c9cdf0"/></marker>'
         f'<marker id="{pfx}-ahb" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">'
         f'<path d="M0,0 L10,5 L0,10 z" fill="#fb7185"/></marker></defs>']
    for k in range(n - 1):
        x, y = pos[k]
        nx, ny = pos[k + 1]
        sx = x if rtl else x + bw                       # leave from the side facing the next step
        sy = y + bh / 2
        ex = nx + bw / 2
        ey = ny - 2
        d = f"M{sx:.1f},{sy:.1f} L{ex:.1f},{sy:.1f} L{ex:.1f},{ey:.1f}"
        o.append(f'<path id="{pfx}-a{k}" d="{d}" class="pr-ln{_h(hidden_steps)}" marker-end="url(#{pfx}-ah)"/>')
    if back:
        f, t, label = back
        fx, fy = pos[f]
        tx, ty = pos[t]
        ax = (fx + bw + 40) if rtl else (fx - 40)
        side = 1 if rtl else -1
        x0, y0 = fx + (bw if rtl else 0), fy + bh / 2
        x1, y1 = tx + (bw if rtl else 0) * 0 + (bw / 2), ty + bh + 4
        mx = max(x0, x1) + 160 if rtl else min(x0, x1) - 160
        d = f"M{x0:.1f},{y0:.1f} C{mx:.1f},{y0:.1f} {x1 + side * 40:.1f},{y1 + 120:.1f} {x1:.1f},{y1:.1f}"
        lx, ly = ((w - 230, h - 40) if rtl else (230, h - 40))
        o.append(f'<g id="{pfx}-back" class="h"><path d="{d}" class="pr-lnb" marker-end="url(#{pfx}-ahb)"/>'
                 f'<text x="{lx:.1f}" y="{ly:.1f}" class="pr-blab" direction="rtl" text-anchor="middle">{esc(label)}</text></g>')
    for k, (he, enl) in enumerate(steps):
        x, y = pos[k]
        sub = (f'<text x="{x + bw / 2:.1f}" y="{y + bh - 14:.1f}" class="pr-sten" text-anchor="middle">{esc(enl)}</text>'
               if enl else "")
        ty = y + (bh / 2 - 2 if enl else bh / 2 + 11)
        o.append(f'<g id="{pfx}-s{k}" class="{_h(hidden_steps).strip()}"><rect x="{x:.1f}" y="{y:.1f}" width="{bw}" height="{bh}" rx="14" class="pr-box"/>'
                 f'<text x="{x + bw / 2:.1f}" y="{ty:.1f}" class="pr-sthe" direction="rtl" text-anchor="middle">{esc(he)}</text>{sub}</g>'
                 f'<rect id="{pfx}-hs{k}" x="{x - 7:.1f}" y="{y - 7:.1f}" width="{bw + 14}" height="{bh + 14}" rx="18" class="pr-ring h"/>')
    o.append("</svg>")
    return "".join(o)


# ---------------------------------------------------------------- Scrum sprint loop
def cycle(pfx, nodes, w=1000, h=640, r=230, bw=290, bh=104, mid=("ספרינט", "2–4 שבועות"), loop_on=None,
          loop_label="כל יום", hidden=True, scale=1.0):
    """nodes: [(key, hebrew, english)] clockwise from the top. loop_on: key of the node that gets the daily self-loop."""
    cx, cy = w / 2, h / 2
    n = len(nodes)
    P = {}
    for k, (key, _, _) in enumerate(nodes):
        a = -math.pi / 2 + 2 * math.pi * k / n
        P[key] = (cx + r * 1.55 * math.cos(a), cy + r * math.sin(a))
    o = [f'<svg class="pr-svg" id="{pfx}" viewBox="0 0 {w} {h}" width="{w * scale:.0f}" height="{h * scale:.0f}" direction="ltr">',
         f'<defs><marker id="{pfx}-ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">'
         f'<path d="M0,0 L10,5 L0,10 z" fill="#2dd4bf"/></marker></defs>']
    rx, ry = r * 1.55, r
    for k in range(n):
        a0 = -math.pi / 2 + 2 * math.pi * k / n
        a1 = -math.pi / 2 + 2 * math.pi * (k + 1) / n
        # leave / enter each node a bit away from its box
        pad0, pad1 = 0.30, 0.30
        b0, b1 = a0 + pad0, a1 - pad1
        x0, y0 = cx + rx * math.cos(b0), cy + ry * math.sin(b0)
        x1, y1 = cx + rx * math.cos(b1), cy + ry * math.sin(b1)
        d = f"M{x0:.1f},{y0:.1f} A{rx:.1f},{ry:.1f} 0 0 1 {x1:.1f},{y1:.1f}"
        o.append(f'<path id="{pfx}-e{k}" d="{d}" class="pr-arc{_h(hidden)}" marker-end="url(#{pfx}-ah)"/>')
    if loop_on:
        x, y = P[loop_on]
        lx = x + bw / 2 - 30
        top = y + bh / 2
        d = f"M{lx - 50:.1f},{top:.1f} C{lx - 70:.1f},{top + 95:.1f} {lx + 70:.1f},{top + 95:.1f} {lx + 20:.1f},{top + 4:.1f}"
        o.append(f'<g id="{pfx}-loop" class="h"><path d="{d}" class="pr-arc" marker-end="url(#{pfx}-ah)"/>'
                 f'<text x="{lx - 15:.1f}" y="{top + 112:.1f}" class="pr-loopl" direction="rtl" text-anchor="middle">{esc(loop_label)}</text></g>')
    if mid:
        o.append(f'<g id="{pfx}-mid" class="{_h(hidden).strip()}"><text x="{cx}" y="{cy - 6}" class="pr-midh" direction="rtl" text-anchor="middle">{esc(mid[0])}</text>'
                 f'<text x="{cx}" y="{cy + 34}" class="pr-mids" direction="rtl" text-anchor="middle">{esc(mid[1])}</text></g>')
    for key, he, enl in nodes:
        x, y = P[key]
        o.append(f'<g id="{pfx}-n-{key}" class="{_h(hidden).strip()}"><rect x="{x - bw / 2:.1f}" y="{y - bh / 2:.1f}" width="{bw}" height="{bh}" rx="16" class="pr-box"/>'
                 f'<text x="{x:.1f}" y="{y - 6:.1f}" class="pr-sten2" text-anchor="middle">{esc(enl)}</text>'
                 f'<text x="{x:.1f}" y="{y + 32:.1f}" class="pr-sthe2" direction="rtl" text-anchor="middle">{esc(he)}</text></g>'
                 f'<rect id="{pfx}-h-{key}" x="{x - bw / 2 - 7:.1f}" y="{y - bh / 2 - 7:.1f}" width="{bw + 14}" height="{bh + 14}" rx="20" class="pr-ring h"/>')
    o.append("</svg>")
    return "".join(o)


# ---------------------------------------------------------------- sorting board
def board(pfx, cols, cards, pool_title="", card_w=470, pool_cols=2, size=26, hidden=False, col_w=None):
    """cols: [(key, title_html, cls)]; cards: [(key, text_html, col_key, why_html or '')] in pool order.
    A card with a 5th element True is fixed: it sits visible in its column from the start (no pool copy);
    "h" = fixed but hidden (no pool copy, shown later with show({pfx}-c-<key>))."""
    cards = [tuple(c) + (False,) * (5 - len(c)) for c in cards]
    pool = "".join(f'<div id="{pfx}-p-{k}" class="pr-card">{t}</div>' for k, t, _, _, fx in cards if not fx)
    colh = []
    for ck, title, cls in cols:
        inner = "".join(
            f'<div id="{pfx}-c-{k}" class="pr-card {cls}{"" if fx is True else " h"}">{t}'
            + (f'<span id="{pfx}-w-{k}" class="pr-why h">{w}</span>' if w else "") + "</div>"
            for k, t, c, w, fx in cards if c == ck)
        colh.append(f'<div class="pr-col {cls}" id="{pfx}-col-{ck}"><div class="pr-colh">{title}</div>{inner}</div>')
    pt = f'<div class="pr-poolh">{pool_title}</div>' if pool_title else ""
    pool_html = (f'<div class="pr-pool" style="grid-template-columns:repeat({pool_cols},var(--cw))">{pool}</div>' if pool else "")
    return (f'<div class="pr-board{_h(hidden)}" id="{pfx}" style="font-size:{size}px;--cw:{card_w}px;--colw:{col_w or card_w}px">'
            f'{pt}{pool_html}<div class="pr-cols">{"".join(colh)}</div></div>')


# ---------------------------------------------------------------- backlogs
def backlog(pfx, items, chosen, cap=None, size=25, hidden_sprint=True):
    """items: [(text_html, points)] in priority order (top = most important); chosen: indices that enter the sprint.
    Ids: {pfx}-p<k> product item, {pfx}-ph<k> its highlight, {pfx}-s<k> its copy in the sprint list,
    {pfx}-pb the product box, {pfx}-sb the sprint box."""
    prod = "".join(f'<div id="{pfx}-p{k}" class="pr-pbi"><i id="{pfx}-ph{k}" class="pr-mk h"></i><span class="pr-pt">{p}</span>'
                   f'<span class="pr-pbt">{t}</span></div>' for k, (t, p) in enumerate(items))
    spr = "".join(f'<div id="{pfx}-s{k}" class="pr-pbi s{_h(hidden_sprint)}"><span class="pr-pt">{items[k][1]}</span>'
                  f'<span class="pr-pbt">{items[k][0]}</span></div>' for k in chosen)
    capl = f'<div class="pr-cap">{cap}</div>' if cap else ""
    return (f'<div class="pr-bl" style="font-size:{size}px">'
            f'<div class="pr-blcol" id="{pfx}-pb"><div class="pr-colh">{en("Product Backlog")}<span class="pr-colsub">כל מה שרוצים במוצר</span></div>{prod}</div>'
            f'<div class="pr-blcol spr" id="{pfx}-sb"><div class="pr-colh">{en("Sprint Backlog")}<span class="pr-colsub">מה שנבחר לספרינט הזה</span></div>{spr}{capl}</div>'
            f'</div>')


# ---------------------------------------------------------------- script checks
def no_latin(scenes):
    bad = [(S.key, p.say) for S in scenes for p in S.phrases if LATIN.search(p.say)]
    assert not bad, "Latin letters in spoken text:\n" + "\n".join(f"  [{k}] {s}" for k, s in bad)


def opt_index(q, needle):
    """index of the single option containing needle (so a script never relies on a position it did not check)"""
    hits = [k for k, o in enumerate(q["options"]) if needle in o]
    assert len(hits) == 1, (q["id"], needle, hits)
    return hits[0]


def qpanel(*parts):
    """the exam side panel in a compact size (stem + options)"""
    return f'<div class="pr-qp">{"".join(parts)}</div>'
