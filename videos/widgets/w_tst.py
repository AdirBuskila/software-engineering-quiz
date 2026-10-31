# -*- coding: utf-8 -*-
"""Software-testing widgets for the tst videos (T01..T08), every CSS class prefixed ts-.

Stage pieces (ids are what the scripts show/hide):
  code(pfx, src)            Java panel. {pfx}-l<k> line k, {pfx}-m<k> highlight bar behind line k (covered line),
                            {pfx}-x<k> red bar (a line a test did NOT reach)
  numline(pfx, f, lo, hi)   equivalence classes of an int function as coloured runs on a number line; boundary
                            ticks {pfx}-b<k>; test points {pfx}-p<v>; class labels {pfx}-c<k>
  path_tree(pfx, paths)     the decision tree of a method: one leaf per path ({pfx}-leaf<k>), nodes {pfx}-n<id>
  vmodel(pfx)               the V: left leg (develop / plan), right leg (tests / run), links, order badges
  boxes(pfx, ...)           a small component diagram (boxes, arrows, scope frames)
  chips(pfx, items)         a row/column of chips revealed one by one ({pfx}-<k>)

Correctness helpers (they RUN the Java that is shown, with the local JDK):
  coverage(method, inputs)  instruments every statement/decision line of a Java method, runs it on each input and
                            returns per-input (result, lines hit, branch outcomes). min_tests() brute-forces the
                            smallest test set for statement / branch coverage; paths() = distinct outcome sequences.
  junit(classes, test_cls)  compiles the classes against a tiny JUnit-5 stand-in (@Test/@BeforeEach/@AfterEach,
                            assertEquals/assertTrue/assertFalse, a fresh instance per test) and returns the run log.
  no_latin(scenes)          the voice misreads Latin letters: every spoken phrase must be Hebrew and digits only.
"""
import html as _html
import itertools
import json
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


# ---------------------------------------------------------------- the course checker's tables (read, not run)
def checker_src():
    return (ROOT / "tools/verify/needhelp/tst/check.py").read_text(encoding="utf-8")


# ---------------------------------------------------------------- Java
def jdk():
    return bool(shutil.which("javac") and shutil.which("java"))


def _compile_run(files, main, args=()):
    with tempfile.TemporaryDirectory() as d:
        for rel, src in files.items():
            p = pathlib.Path(d) / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(src, encoding="utf-8")
        r = subprocess.run(["javac", "-encoding", "UTF-8", "-d", d, *files.keys()], cwd=d, capture_output=True,
                           text=True)
        assert r.returncode == 0, "javac failed:\n" + r.stdout + r.stderr
        r = subprocess.run(["java", "-cp", d, main, *args], capture_output=True, text=True, encoding="utf-8")
        assert r.returncode == 0, r.stdout + r.stderr
        return r.stdout.replace("\r\n", "\n")


JUNIT = {
    "org/junit/jupiter/api/Test.java": "package org.junit.jupiter.api; import java.lang.annotation.*; "
                                       "@Retention(RetentionPolicy.RUNTIME) @Target(ElementType.METHOD) public @interface Test {}",
    "org/junit/jupiter/api/BeforeEach.java": "package org.junit.jupiter.api; import java.lang.annotation.*; "
                                             "@Retention(RetentionPolicy.RUNTIME) @Target(ElementType.METHOD) public @interface BeforeEach {}",
    "org/junit/jupiter/api/AfterEach.java": "package org.junit.jupiter.api; import java.lang.annotation.*; "
                                            "@Retention(RetentionPolicy.RUNTIME) @Target(ElementType.METHOD) public @interface AfterEach {}",
    "org/junit/jupiter/api/Assertions.java": """package org.junit.jupiter.api;
public final class Assertions {
  public static void assertEquals(int e, int a) { if (e != a) throw new AssertionError("expected: <" + e + "> but was: <" + a + ">"); }
  public static void assertEquals(Object e, Object a) { if (!java.util.Objects.equals(e, a)) throw new AssertionError("expected: <" + e + "> but was: <" + a + ">"); }
  public static void assertTrue(boolean c) { if (!c) throw new AssertionError("expected: <true> but was: <false>"); }
  public static void assertFalse(boolean c) { if (c) throw new AssertionError("expected: <false> but was: <true>"); }
}""",
    "MiniRunner.java": """import java.lang.reflect.*; import java.util.*;
import org.junit.jupiter.api.*;
public class MiniRunner {
  static void call(Method m, Object o) throws Exception { m.setAccessible(true); System.out.println("RUN " + m.getName()); m.invoke(o); }
  public static void main(String[] a) throws Exception {
    Class<?> c = Class.forName(a[0]);
    List<Method> tests = new ArrayList<>(), be = new ArrayList<>(), ae = new ArrayList<>();
    for (Method m : c.getDeclaredMethods()) {
      if (m.isAnnotationPresent(Test.class)) tests.add(m);
      if (m.isAnnotationPresent(BeforeEach.class)) be.add(m);
      if (m.isAnnotationPresent(AfterEach.class)) ae.add(m);
    }
    tests.sort(Comparator.comparing(Method::getName));
    for (Method t : tests) {
      Constructor<?> k = c.getDeclaredConstructor(); k.setAccessible(true);
      Object o = k.newInstance();
      String res;
      try { for (Method m : be) call(m, o); call(t, o); res = "PASS " + t.getName(); }
      catch (InvocationTargetException e) { res = "FAIL " + t.getName() + " " + e.getCause().getMessage(); }
      for (Method m : ae) call(m, o);
      System.out.println(res);
    }
  }
}""",
}


def junit(classes, test_cls):
    """classes: {FileName.java: source}. Returns the run log lines: 'RUN m', 'PASS t', 'FAIL t <msg>'."""
    if not jdk():
        return None
    return _compile_run({**JUNIT, **classes}, "MiniRunner", [test_cls]).strip().split("\n")


def java_out(classes, main):
    if not jdk():
        return None
    return _compile_run(classes, main).strip()


# ---------------------------------------------------------------- coverage by instrumentation
DECL = re.compile(r"^(int|String|boolean|double|long)\s+\w+")
IF = re.compile(r"^(\}?\s*(?:else\s+)?)if\s*\((.*)\)(\s*\{?)\s*$")


def instrument(method):
    """method: Java source of ONE method, one statement or decision per line (bodies of if/else on their own line).
    Returns (instrumented source, {line: 'stmt'|'dec'}, {line: condition text})."""
    out, kinds, conds = [], {}, {}
    lines = method.split("\n")
    for k, raw in enumerate(lines):
        ind = raw[:len(raw) - len(raw.lstrip())]
        s = raw.strip()
        if k == 0:
            out.append(ind + "static " + s)
            continue
        m = IF.match(s)
        if m:
            kinds[k] = "dec"
            conds[k] = m.group(2)
            out.append(f"{ind}{m.group(1)}if (Cov.b({k}, {m.group(2)})){m.group(3)}")
        elif s in ("}", "} else {", "} else", "else", "else {", ""):
            out.append(raw)
        elif s.endswith(";"):
            kinds[k] = "stmt"
            out.append(f"{ind}Cov.h({k}); {s}" if DECL.match(s) else f"{ind}{{ Cov.h({k}); {s} }}")
        else:
            raise ValueError(f"cannot instrument line {k}: {raw!r}")
    return "\n".join(out), kinds, conds


COV = """import java.util.*;
public class Cov {
  static TreeSet<Integer> hits = new TreeSet<>();
  static List<String> br = new ArrayList<>();
  static void h(int k) { hits.add(k); }
  static boolean b(int k, boolean c) { hits.add(k); br.add(k + ":" + c); return c; }
  static void reset() { hits.clear(); br.clear(); }
}"""


def coverage(method, inputs, extra=""):
    """run the instrumented method on every input (a tuple of Java literals as strings).
    Returns (records, kinds, conds); records[i] = {"in": input, "out": str, "hits": set, "br": tuple((line, bool))}"""
    assert jdk(), "coverage() needs a JDK"
    src, kinds, conds = instrument(method)
    name = re.search(r"(\w+)\s*\(", method.split("\n")[0]).group(1)
    calls = "\n".join(f'    Cov.reset(); Object r{i} = Snip.{name}({", ".join(a)}); '
                      f'System.out.println(r{i} + "|" + Cov.hits + "|" + Cov.br);' for i, a in enumerate(inputs))
    files = {"Cov.java": COV, "Snip.java": f"public class Snip {{\n{extra}\n{src}\n}}",
             "Main.java": f"public class Main {{ public static void main(String[] a) {{\n{calls}\n}} }}"}
    lines = _compile_run(files, "Main").strip().split("\n")
    recs = []
    for inp, ln in zip(inputs, lines):
        out, hits, br = ln.split("|")
        hits = {int(x) for x in hits.strip("[]").split(",") if x.strip()}
        br = tuple((int(a), b == "true") for a, b in (x.strip().split(":") for x in br.strip("[]").split(",") if x.strip()))
        recs.append({"in": inp, "out": out, "hits": hits, "br": br})
    assert len(recs) == len(inputs)
    return recs, kinds, conds


def all_lines(kinds):
    return set(kinds)


def all_branches(kinds):
    return {(k, v) for k, t in kinds.items() if t == "dec" for v in (True, False)}


def covers_stmt(recs, kinds):
    return set().union(*(r["hits"] for r in recs)) == all_lines(kinds)


def covers_branch(recs, kinds):
    return {b for r in recs for b in r["br"]} == all_branches(kinds)


def min_tests(recs, kinds, goal):
    """smallest number of inputs (from recs) that reaches the goal ('stmt' or 'branch'), and one such set"""
    test = covers_stmt if goal == "stmt" else covers_branch
    uniq = list({(frozenset(r["hits"]), r["br"]): r for r in recs}.values())
    for k in range(1, len(uniq) + 1):
        for sub in itertools.combinations(uniq, k):
            if test(list(sub), kinds):
                return k, list(sub)
    raise AssertionError("goal unreachable over these inputs")


def paths(recs):
    return sorted({r["br"] for r in recs})


# ---------------------------------------------------------------- code panel (Java)
KW = (r"\b(abstract|class|interface|implements|extends|public|private|protected|static|final|new|return|if|else|"
      r"void|null|this|int|boolean|String|true|false|import)\b")


def _hl_plain(s):
    """one pass over the raw text, so inserted markup is never matched again"""
    def tok(m):
        t = m.group(0)
        if t.startswith("@"):
            return f'<span class="ts-an">{esc(t)}</span>'
        if t[0].isdigit():
            return f'<span class="ts-num">{t}</span>'
        if re.fullmatch(KW, t):
            return f'<span class="ts-kw">{t}</span>'
        return esc(t)
    return re.sub(r"@\w+|\d+|\w+|[^\w@]+", tok, s)


def _hl(line):
    out, pos = [], 0
    for m in re.finditer(r'("[^"]*"|//.*$)', line):
        out.append(_hl_plain(line[pos:m.start()]))
        cls = "ts-cm" if m.group(0).startswith("//") else "ts-str"
        out.append(f'<span class="{cls}">{esc(m.group(0))}</span>')
        pos = m.end()
    out.append(_hl_plain(line[pos:]))
    return "".join(out)


def code(pfx, src, hidden=False, size=27, lines_hidden=(), title=None, width=None):
    lines = src.split("\n")
    body = "".join(f'<div id="{pfx}-l{k}" class="ts-ln{_h(k in lines_hidden)}"><i id="{pfx}-m{k}" class="ts-mark h"></i>'
                   f'<i id="{pfx}-x{k}" class="ts-miss h"></i><span class="ts-tx">{_hl(l) or "&nbsp;"}</span></div>'
                   for k, l in enumerate(lines))
    head = f'<div class="ts-ctitle">{esc(title)}</div>' if title else ""
    w = f"width:{width}px;" if width else ""
    return f'<div class="ts-code{_h(hidden)}" id="{pfx}" dir="ltr" style="font-size:{size}px;{w}">{head}{body}</div>'


def mono(s):
    return f'<span class="ts-mono" dir="ltr">{esc(s)}</span>'


def stem(qid, html_):
    tag = f'<span class="qid">{esc(qid)}</span>' if qid else '<span class="qid">בסגנון מבחן</span>'
    return f'<div class="qstem">{tag}{html_}</div>'


def ltr_runs(text):
    """escape Hebrew text and wrap each Latin run (with @, digits, parentheses) in an LTR isolate"""
    parts = re.split(r"(\(?[@A-Za-z][@A-Za-z0-9_.()\-' ]*[A-Za-z0-9)])", text)
    return "".join(f'<bdi dir="ltr">{esc(p)}</bdi>' if k % 2 else esc(p) for k, p in enumerate(parts))


def opts_of(q, order=None):
    """bank options as (index, html); `order` = display order of indices (default: bank order)"""
    idx = order if order is not None else range(len(q["options"]))
    return [(k, ltr_runs(q["options"][k])) for k in idx]


def chips(pfx, items, vertical=False, hidden=True, kinds=None, rtl=False):
    """items: html strings; ids {pfx}-<k>; kinds: per-item extra class (ok, bad, an, …)"""
    kinds = kinds or [""] * len(items)
    c = "".join(f'<span id="{pfx}-{k}" class="ts-chip {kd}{_h(hidden)}">{it}</span>' for k, (it, kd) in enumerate(zip(items, kinds)))
    return f'<div class="ts-chips{" col" if vertical else ""}{" rtl" if rtl else ""}" id="{pfx}">{c}</div>'


def swap(pfx, items, height, width=None):
    w = f"width:{width}px;" if width else ""
    layers = "".join(f'<div id="{pfx}-{k}" class="{_h(k > 0).strip()}">{it}</div>' for k, it in enumerate(items))
    return f'<div class="swap ts-swap" id="{pfx}" style="--swap-h:{height}px;{w}">{layers}</div>'


# ---------------------------------------------------------------- number line of equivalence classes
COLORS = ["#38bdf8", "#34d399", "#fbbf24", "#c084fc", "#fb7185"]


def runs(f, lo, hi):
    """maximal runs of equal output over the integers lo..hi: [(start, end, output)]"""
    out = []
    for v in range(lo, hi + 1):
        y = f(v)
        if out and out[-1][2] == y:
            out[-1][1] = v
        else:
            out.append([v, v, y])
    return [tuple(r) for r in out]


def boundaries(f, lo, hi):
    """pairs (last value before, first value after) wherever the output changes"""
    rs = runs(f, lo, hi)
    return [(rs[i][1], rs[i + 1][0]) for i in range(len(rs) - 1)]


def numline(pfx, f, lo, hi, labels, points=(), w=1000, segs_hidden=True, ticks_hidden=True, view=None,
            colors=None, tick_dy=None):
    """labels: Hebrew/HTML label per run (in order). points: test values drawn as dots ({pfx}-p<v>, hidden).
    view = (vlo, vhi) the drawn range (runs are clipped; arrows at the ends mean 'and beyond')."""
    rs = runs(f, lo, hi)
    assert len(labels) == len(rs), (len(labels), rs)
    vlo, vhi = view or (lo, hi)
    pad = 50
    X = lambda v: pad + (v - vlo) / (vhi - vlo) * (w - 2 * pad)
    colors = colors or COLORS
    H = 250
    y = 120
    o = [f'<svg class="ts-nl" id="{pfx}" viewBox="0 0 {w} {H}" width="{w}" height="{H}" direction="ltr">',
         f'<line x1="10" x2="{w - 10}" y1="{y}" y2="{y}" class="ts-axis"/>',
         f'<path d="M{w - 10},{y} l-16,-9 l0,18 z" class="ts-axh"/><path d="M10,{y} l16,-9 l0,18 z" class="ts-axh"/>']
    for k, (a, b, _) in enumerate(rs):
        x1 = X(max(a, vlo) - (0.5 if a > lo else 0)) if a > lo else 14
        x2 = X(min(b, vhi) + (0.5 if b < hi else 0)) if b < hi else w - 14
        c = colors[k % len(colors)]
        o.append(f'<g id="{pfx}-c{k}" class="{_h(segs_hidden).strip()}"><rect x="{x1:.1f}" y="{y - 16}" width="{x2 - x1:.1f}" '
                 f'height="32" rx="6" fill="{c}" opacity=".85"/>'
                 f'<foreignObject x="{x1:.1f}" y="{y - 108}" width="{x2 - x1:.1f}" height="80"><div class="ts-nlab" '
                 f'style="color:{c}">{labels[k]}</div></foreignObject></g>')
    for k, (a, b) in enumerate(boundaries(f, lo, hi)):
        xm = X(a + 0.5)
        dy = (tick_dy or {}).get(k, 0)
        o.append(f'<g id="{pfx}-b{k}" class="{_h(ticks_hidden).strip()}"><line x1="{xm:.1f}" x2="{xm:.1f}" y1="{y - 34}" '
                 f'y2="{y + 34}" class="ts-tick"/>'
                 f'<text x="{X(a) - 6:.1f}" y="{y + 70 + dy}" class="ts-tv" text-anchor="end">{a}</text>'
                 f'<text x="{X(b) + 6:.1f}" y="{y + 70 + dy}" class="ts-tv" text-anchor="start">{b}</text></g>')
    for v in points:
        o.append(f'<g id="{pfx}-p{v}" class="h"><circle cx="{X(v):.1f}" cy="{y}" r="13" class="ts-pt"/>'
                 f'<text x="{X(v):.1f}" y="{y + 112}" class="ts-pv">{v}</text></g>')
    o.append("</svg>")
    return "".join(o)


# ---------------------------------------------------------------- decision tree of paths
def path_tree(pfx, pth, conds, w=900, h=430, leaf_text=None, hidden=False, reveal=False):
    """pth: list of outcome sequences ((line, bool), ...) as returned by paths(); conds: {line: condition text}.
    Ids: {pfx}-n<i> decision node i (in creation order), {pfx}-e<i> the edge into node/leaf i, {pfx}-leaf<k> leaf k
    (k = index in pth), {pfx}-hl<k> highlight of leaf k's whole path."""
    nodes = {(): {"kids": {}, "line": None}}
    for p in pth:
        for d in range(len(p)):
            pre = p[:d]
            nodes[pre]["line"] = p[d][0]
            nodes.setdefault(p[:d + 1], {"kids": {}, "line": None})
            nodes[pre]["kids"][p[d][1]] = p[:d + 1]
    leaves = [p for p in pth]
    depth = max(len(p) for p in pth)
    xs = {}
    for k, p in enumerate(leaves):
        xs[p] = 70 + k * (w - 140) / max(1, len(leaves) - 1)

    def xof(n):
        if n in xs:
            return xs[n]
        kids = [xof(c) for c in nodes[n]["kids"].values()]
        xs[n] = sum(kids) / len(kids)
        return xs[n]
    xof(())
    gy = (h - 120) / depth
    Y = lambda n: 40 + len(n) * gy
    ids = {n: i for i, n in enumerate(sorted(nodes, key=lambda n: (len(n), xs[n])))}
    o = [f'<svg class="ts-tree{_h(hidden)}" id="{pfx}" viewBox="0 0 {w} {h}" width="{w}" height="{h}" direction="ltr">']
    hl = []
    for k, p in enumerate(leaves):
        pts = [((xs[p[:d]]), Y(p[:d])) for d in range(len(p) + 1)]
        hl.append(f'<polyline id="{pfx}-hl{k}" points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" class="ts-thl h"/>')
    o += hl
    for n, d in nodes.items():
        for v, c in d["kids"].items():
            x1, y1, x2, y2 = xs[n], Y(n), xs[c], Y(c)
            o.append(f'<g id="{pfx}-e{ids[c]}" class="{_h(reveal).strip()}"><line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="ts-te"/>'
                     f'<text x="{(x1 + x2) / 2 + (-24 if v else 24):.1f}" y="{(y1 + y2) / 2 + 2:.1f}" '
                     f'class="ts-tb {"t" if v else "f"}" text-anchor="{"end" if v else "start"}">{"true" if v else "false"}</text></g>')
    for n, d in nodes.items():
        x, y = xs[n], Y(n)
        if d["line"] is not None:
            t = conds[d["line"]]
            bw = 24 + 15.5 * len(t)
            o.append(f'<g id="{pfx}-n{ids[n]}" class="{_h(reveal).strip()}"><rect x="{x - bw / 2:.1f}" y="{y - 26}" width="{bw:.1f}" height="52" rx="12" '
                     f'class="ts-tn"/><text x="{x:.1f}" y="{y + 9}" class="ts-tt">{esc(t)}</text></g>')
    for k, p in enumerate(leaves):
        x, y = xs[p], Y(p)
        lab = leaf_text[k] if leaf_text else str(k + 1)
        o.append(f'<g id="{pfx}-leaf{k}" class="h"><circle cx="{x:.1f}" cy="{y + 4:.1f}" r="27" class="ts-tl"/>'
                 f'<text x="{x:.1f}" y="{y + 15:.1f}" class="ts-tlt">{esc(lab)}</text></g>')
    o.append("</svg>")
    return "".join(o)


# ---------------------------------------------------------------- the V model
def vmodel(pfx, left, right, bottom, w=1040, h=560, links_hidden=False, arrows_hidden=False):
    """left: [(key, Hebrew label)] top->down (development stages), right: [(key, label)] top->down (tests, same
    rows), bottom: label of the tip. Ids: {pfx}-L<k>, {pfx}-R<k>, {pfx}-k<k> the dashed link of row k,
    {pfx}-B the tip, {pfx}-pl<k> planning badge of row k, {pfx}-ex<k> execution badge, {pfx}-arL / -arR leg arrows."""
    n = len(left)
    assert len(right) == n
    bw, bh = 300, 74
    rows = [70 + k * 120 for k in range(n)]
    lx = [30 + k * 70 for k in range(n)]
    rx = [w - 30 - bw - k * 70 for k in range(n)]
    o = [f'<svg class="ts-v" id="{pfx}" viewBox="0 0 {w} {h}" width="{w}" height="{h}" direction="ltr">',
         f'<defs><marker id="{pfx}-ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" '
         f'orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#c9cdf0"/></marker></defs>']
    tipy = rows[-1] + 130
    o.append(f'<path id="{pfx}-arL" class="ts-varr{_h(arrows_hidden)}" d="M{lx[0] + bw / 2 - 120},{rows[0] + bh + 4} L{w / 2 - 70},{tipy - 4}" marker-end="url(#{pfx}-ah)"/>')
    o.append(f'<path id="{pfx}-arR" class="ts-varr{_h(arrows_hidden)}" d="M{w / 2 + 70},{tipy - 4} L{rx[0] + bw / 2 + 120},{rows[0] + bh + 4}" marker-end="url(#{pfx}-ah)"/>')
    for k in range(n):
        y = rows[k]
        o.append(f'<line id="{pfx}-k{k}" class="ts-vlink{_h(links_hidden)}" x1="{lx[k] + bw}" y1="{y + bh / 2}" x2="{rx[k]}" y2="{y + bh / 2}"/>')
        o.append(f'<g id="{pfx}-L{left[k][0]}"><rect x="{lx[k]}" y="{y}" width="{bw}" height="{bh}" rx="14" class="ts-vb dev"/>'
                 f'<text x="{lx[k] + bw / 2}" y="{y + 47}" class="ts-vt" direction="rtl">{esc(left[k][1])}</text></g>')
        o.append(f'<g id="{pfx}-R{right[k][0]}"><rect x="{rx[k]}" y="{y}" width="{bw}" height="{bh}" rx="14" class="ts-vb tst"/>'
                 f'<text x="{rx[k] + bw / 2}" y="{y + 47}" class="ts-vt" direction="rtl">{esc(right[k][1])}</text></g>')
        o.append(f'<g id="{pfx}-pl{k}" class="h"><circle cx="{lx[k] + bw - 4}" cy="{y + 4}" r="22" class="ts-badge pl"/>'
                 f'<text x="{lx[k] + bw - 4}" y="{y + 14}" class="ts-bt">{k + 1}</text></g>')
        o.append(f'<g id="{pfx}-ex{k}" class="h"><circle cx="{rx[k] + 4}" cy="{y + 4}" r="22" class="ts-badge ex"/>'
                 f'<text x="{rx[k] + 4}" y="{y + 14}" class="ts-bt">{n - k}</text></g>')
    o.append(f'<g id="{pfx}-B"><rect x="{w / 2 - 130}" y="{tipy}" width="260" height="{bh}" rx="14" class="ts-vb code"/>'
             f'<text x="{w / 2}" y="{tipy + 47}" class="ts-vt" direction="rtl">{esc(bottom)}</text></g>')
    o.append("</svg>")
    return "".join(o)


# ---------------------------------------------------------------- component boxes
def boxes(pfx, items, arrows=(), frames=(), w=1000, h=520):
    """items: [{key, x, y, w, h, label, sub (Hebrew, optional), kind: '', 'mock', 'real', 'user', hidden}]
    arrows: [{key, a, b, label, hidden}] from box a to box b (horizontal or vertical centre to centre).
    frames: [{key, x, y, w, h, label}] dashed scope frames, hidden. Ids {pfx}-b-<key>, {pfx}-a-<key>, {pfx}-f-<key>."""
    B = {b["key"]: b for b in items}
    o = [f'<svg class="ts-bx" id="{pfx}" viewBox="0 0 {w} {h}" width="{w}" height="{h}" direction="ltr">',
         f'<defs><marker id="{pfx}-ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" '
         f'orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#c9cdf0"/></marker></defs>']
    for f in frames:
        lab = (f'<text x="{f["x"] + f["w"] - 14}" y="{f["y"] + f["h"] + 34}" class="ts-fl" direction="rtl" '
               f'text-anchor="start">{esc(f["label"])}</text>') if f.get("label") else ""
        o.append(f'<g id="{pfx}-f-{f["key"]}" class="h"><rect x="{f["x"]}" y="{f["y"]}" width="{f["w"]}" height="{f["h"]}" '
                 f'rx="20" class="ts-frame {f.get("kind", "")}"/>{lab}</g>')
    for a in arrows:
        p, q = B[a["a"]], B[a["b"]]
        pcx, pcy, qcx, qcy = p["x"] + p["w"] / 2, p["y"] + p["h"] / 2, q["x"] + q["w"] / 2, q["y"] + q["h"] / 2
        if abs(pcy - qcy) < 5:
            x1, x2 = (p["x"] + p["w"], q["x"]) if qcx > pcx else (p["x"], q["x"] + q["w"])
            y1 = y2 = pcy
        else:
            x1 = x2 = pcx
            y1, y2 = (p["y"] + p["h"], q["y"]) if qcy > pcy else (p["y"], q["y"] + q["h"])
        lab = ""
        if a.get("label"):
            heb = bool(re.search(r"[֐-׿]", a["label"]))
            lx, ly = a.get("lxy", ((x1 + x2) / 2, (y1 + y2) / 2 - 14))
            lab = (f'<text x="{lx}" y="{ly}" class="ts-al{" heb" if heb else ""}"'
                   f'{" direction=\"rtl\"" if heb else ""}>{esc(a["label"])}</text>')
        o.append(f'<g id="{pfx}-a-{a["key"]}" class="{_h(a.get("hidden", False)).strip()}"><line x1="{x1}" y1="{y1}" '
                 f'x2="{x2}" y2="{y2}" class="ts-ar" marker-end="url(#{pfx}-ah)"/>{lab}</g>')
    for b in items:
        kind = b.get("kind", "")
        sub = (f'<text x="{b["x"] + b["w"] / 2}" y="{b["y"] + b["h"] - 18}" class="ts-bs" direction="rtl">{esc(b["sub"])}</text>'
               if b.get("sub") else "")
        ty = b["y"] + (b["h"] / 2 + 10 if not b.get("sub") else 44)
        o.append(f'<g id="{pfx}-b-{b["key"]}" class="{_h(b.get("hidden", False)).strip()}"><rect x="{b["x"]}" y="{b["y"]}" '
                 f'width="{b["w"]}" height="{b["h"]}" rx="14" class="ts-box {kind}"/>'
                 f'<text x="{b["x"] + b["w"] / 2}" y="{ty}" class="ts-bl">{esc(b["label"])}</text>{sub}</g>')
    o.append("</svg>")
    return "".join(o)


# ---------------------------------------------------------------- script checks
def no_latin(scenes):
    bad = [(S.key, p.say) for S in scenes for p in S.phrases if LATIN.search(p.say)]
    assert not bad, "Latin letters in spoken text:\n" + "\n".join(f"  [{k}] {s}" for k, s in bad)


AT_TOKEN = re.compile(r"(?<![\w>])(@\w+)")


def no_latin_and_isolate(scenes):
    """no_latin(), then wrap every @Annotation of a subtitle in <bdi> (in RTL text the @ would jump to the far side)"""
    no_latin(scenes)
    for S in scenes:
        for p in S.phrases:
            p.sub = AT_TOKEN.sub(r"<bdi>\1</bdi>", p.sub)
