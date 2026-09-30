# -*- coding: utf-8 -*-
"""build_learn.py — build the Learning-section data for the SE quiz site.

Reads the Hebrew course summaries listed in DOCS, splits each into sections by
'## ' headings, renders them to HTML, optionally appends curated figures, and emits:

    ../learn.js   ->  window.LEARN_DOCS = [{id, title, md, pdf, sections:[{id, title, html}]}]
    ../study/<id>.md, ../study/<id>.pdf   (download copies)

Obsidian syntax (frontmatter, > [!callout], ^block-ids, ```mermaid) is handled here;
mermaid diagrams and the PDFs are rendered with headless Chrome (render_study.js),
so the site stays 100% static and offline (no runtime markdown/mermaid, no CDN).
Run:  python tools/build_learn.py
"""
import os, re, json, html, datetime, io, sys, shutil, subprocess
import markdown
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HERE    = os.path.dirname(os.path.abspath(__file__))
ROOT    = os.path.dirname(HERE)
OUT_IMG = os.path.join(ROOT, "images")
OUT_JS  = os.path.join(ROOT, "learn.js")
STUDY   = os.path.join(ROOT, "study")
TMP     = os.path.join(HERE, "raw")

# Summaries shown in learn mode (first = default). `src` is the markdown source; it is
# copied to study/<id>.md (unless it already lives there) and printed to study/<id>.pdf.
DOCS = [
    {"id": "se-exam-summary",   "title": "סיכום למבחן",      "src": os.path.join(STUDY, "se-exam-summary.md")},
    {"id": "se-topics-summary", "title": "סיכום לפי נושאים", "src": os.path.join(HERE, "se_summary.md")},
]

# section-id -> [(image filename already in images/, Hebrew caption), ...]
# Empty for now (text-first learn mode); add entries to enrich a chapter with figures.
CURATION = {}


def section_id(idx, title, prefix=""):
    t = title.strip()
    m = re.search(r"[A-Za-z][\w+/&-]*", t)   # first latin token → readable slug
    if m:
        return f"{prefix}ch{idx}-" + re.sub(r"[^\w]+", "", m.group(0)).lower()[:16]
    return f"{prefix}ch{idx}"


def split_sections(md_text, prefix=""):
    lines = md_text.splitlines()
    page_title = "תרגול הנדסת תוכנה"
    for ln in lines:
        if ln.startswith("# ") and not ln.startswith("## "):
            page_title = ln[2:].strip(); break
    sections = []; cur_title, cur_buf, preamble = None, [], []
    seen_h1 = False
    for ln in lines:
        if ln.startswith("# ") and not ln.startswith("## "):
            seen_h1 = True; continue
        if ln.startswith("## "):
            if cur_title is not None:
                sections.append((cur_title, "\n".join(cur_buf)))
            cur_title = ln[3:].strip(); cur_buf = []
        elif cur_title is None:
            if seen_h1: preamble.append(ln)
        else:
            cur_buf.append(ln)
    if cur_title is not None:
        sections.append((cur_title, "\n".join(cur_buf)))
    preamble_md = "\n".join(preamble).strip()
    out = []
    for i, (title, body) in enumerate(sections):
        sid = section_id(i, title, prefix)
        body = body.strip()
        if i == 0 and preamble_md:
            body = preamble_md + "\n\n" + body
        out.append((sid, title, body))
    return page_title, out


_LIST_RE = re.compile(r"^(\s*)([-*+]|\d+\.)\s+")

def normalize_lists(md):
    """Insert a blank line before a list that directly follows a text line."""
    out = []
    for ln in md.split("\n"):
        if _LIST_RE.match(ln):
            prev = out[-1] if out else ""
            p = prev.strip()
            if p and not _LIST_RE.match(prev) and not p.startswith("#") and not p.startswith("|"):
                out.append("")
        out.append(ln)
    return "\n".join(out)


_FRONT_RE   = re.compile(r"\A---\n.*?\n---\n", re.S)
_MERMAID_RE = re.compile(r"^```mermaid\n(.*?)^```[ \t]*$", re.S | re.M)
_CALLOUT_RE = re.compile(r"^>\s*\[!(\w+)\][+-]?\s*(.*)$")
_BLOCKID_RE = re.compile(r"^\^[\w-]+\s*$")


def obsidian_to_md(text, mermaid):
    """Strip frontmatter and ^block-ids, pull out mermaid blocks (appended to `mermaid`,
    left as a placeholder paragraph) and turn > [!type] callouts into divs."""
    text = _FRONT_RE.sub("", text.replace("\r\n", "\n"), count=1)
    def grab(m):
        mermaid.append(m.group(1).strip())
        return f"\nMMDPLACEHOLDER{len(mermaid) - 1}\n"
    text = _MERMAID_RE.sub(grab, text)
    out, lines, i = [], text.split("\n"), 0
    while i < len(lines):
        ln = lines[i]
        if _BLOCKID_RE.match(ln):
            i += 1; continue
        m = _CALLOUT_RE.match(ln)
        if m:
            kind, title = m.group(1).lower(), m.group(2).strip()
            body = []; i += 1
            while i < len(lines) and lines[i].startswith(">"):
                body.append(re.sub(r"^>\s?", "", lines[i])); i += 1
            out += ["", f'<div class="callout callout-{kind}" markdown="1">']
            if title:
                out.append(f'<div class="callout-title" markdown="span">{title}</div>')
            out += ["", normalize_lists("\n".join(body)), "", "</div>", ""]
            continue
        out.append(ln); i += 1
    return "\n".join(out)


def fill_mermaid(html_text, svgs):
    return re.sub(r"<p>MMDPLACEHOLDER(\d+)</p>",
                  lambda m: f'<figure class="learn-mmd">{svgs[int(m.group(1))]}</figure>', html_text)


def run_node(*args):
    subprocess.run(["node", os.path.join(HERE, "render_study.js"), *args], check=True)


def render_mermaid(sources):
    if not sources:
        return []
    os.makedirs(TMP, exist_ok=True)
    fin, fout = os.path.join(TMP, "_mermaid_in.json"), os.path.join(TMP, "_mermaid_out.json")
    with open(fin, "w", encoding="utf-8") as f:
        json.dump(sources, f, ensure_ascii=False)
    run_node("mermaid", fin, fout)
    with open(fout, encoding="utf-8") as f:
        svgs = json.load(f)
    os.remove(fin); os.remove(fout)
    return svgs


PRINT_CSS = """
body{font-family:"Segoe UI",Arial,sans-serif;color:#1c2333;line-height:1.6;font-size:11pt;margin:0}
h1{font-size:20pt;margin:0 0 .6em}
h2{font-size:15pt;margin:1.4em 0 .5em;padding-bottom:.2em;border-bottom:2px solid #059669;break-after:avoid}
h3{font-size:12.5pt;margin:1.1em 0 .35em;break-after:avoid}
table{width:100%;border-collapse:collapse;margin:.7em 0;font-size:9.5pt}
tr{break-inside:avoid}
th,td{border:1px solid #c9cfdd;padding:.3em .5em;text-align:right;vertical-align:top}
thead th{background:#eef0f7}
code{font-family:Consolas,monospace;background:#f1f3f8;border-radius:4px;padding:0 .25em}
pre{background:#f1f3f8;padding:.6em .8em;border-radius:6px;direction:ltr;text-align:left;white-space:pre-wrap;break-inside:avoid}
pre code{background:none;padding:0}
ul,ol{padding-inline-start:1.3em}
hr{border:none;border-top:1px solid #d5d9e4;margin:1em 0}
.callout{border:1px solid #d5d9e4;border-inline-start:4px solid #059669;background:#f0fbf6;border-radius:6px;padding:.3em .9em;margin:.8em 0;break-inside:avoid}
.callout-title{font-weight:800;margin:.3em 0}
.learn-mmd{margin:.8em 0;text-align:center;break-inside:avoid}
.learn-mmd svg{max-width:100%;height:auto}
"""


def write_print_html(path, title, sections):
    parts = [f"<h1>{html.escape(title)}</h1>"]
    for s in sections:
        parts.append(f"<h2>{html.escape(s['title'])}</h2>" + s["html"])
    with open(path, "w", encoding="utf-8") as f:
        f.write('<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8">'
                f"<title>{html.escape(title)}</title><style>{PRINT_CSS}</style></head>"
                f"<body>{''.join(parts)}</body></html>")


def figures_html(sid):
    items = CURATION.get(sid, [])
    if not items:
        return ""
    figs = []
    for out_name, caption in items:
        cap = html.escape(caption)
        figs.append(
            f'<figure class="learn-fig"><img loading="lazy" src="images/{out_name}" '
            f'alt="{cap}"><figcaption>{cap}</figcaption></figure>')
    return '<div class="learn-figs">' + "".join(figs) + "</div>"


def build_doc(doc, md, prefix):
    with open(doc["src"], encoding="utf-8") as f:
        raw = f.read()
    mermaid = []
    page_title, sections = split_sections(obsidian_to_md(raw, mermaid), prefix)
    svgs = render_mermaid(mermaid)
    out = []
    for sid, title, body in sections:
        md.reset()
        out.append({"id": sid, "title": title,
                    "html": fill_mermaid(md.convert(normalize_lists(body)), svgs) + figures_html(sid)})

    # download copies: the markdown as written + a printed PDF
    os.makedirs(STUDY, exist_ok=True); os.makedirs(TMP, exist_ok=True)
    md_out  = os.path.join(STUDY, doc["id"] + ".md")
    pdf_out = os.path.join(STUDY, doc["id"] + ".pdf")
    if os.path.abspath(doc["src"]) != os.path.abspath(md_out):
        shutil.copyfile(doc["src"], md_out)
    tmp_html = os.path.join(TMP, f"_print_{doc['id']}.html")
    write_print_html(tmp_html, page_title, out)
    run_node("pdf", tmp_html, pdf_out)
    os.remove(tmp_html)
    print(f"doc        : {doc['id']} ({page_title}) -> {len(out)} sections, {len(svgs)} diagrams")
    return {"id": doc["id"], "title": doc["title"], "fullTitle": page_title,
            "md": f"study/{doc['id']}.md", "pdf": f"study/{doc['id']}.pdf", "sections": out}


def main():
    md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists", "attr_list", "md_in_html"])
    docs = [build_doc(d, md, "" if i == 0 else f"d{i}-") for i, d in enumerate(DOCS)]
    meta = {"generated": datetime.date.today().isoformat(), "docs": len(docs)}
    payload = ("/* AUTO-GENERATED by tools/build_learn.py — do not edit by hand. */\n"
               "window.LEARN_DOCS = " + json.dumps(docs, ensure_ascii=False) + ";\n"
               "window.LEARN_META = " + json.dumps(meta, ensure_ascii=False) + ";\n")
    with open(OUT_JS, "w", encoding="utf-8") as f:
        f.write(payload)
    print(f"wrote      : {OUT_JS}")


if __name__ == "__main__":
    main()
