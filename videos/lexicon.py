# -*- coding: utf-8 -*-
"""Pronunciation lexicon for the הנדסת תוכנה videos: the shared machinery (tools/video/lexicon_base.py) plus the course's
own terms. TeX is spoken token by token (TEX_TOKENS, longest first); a span with any token outside the table is
refused, and the script must give P(..., say=...) — the usual case for real formulas (fractions, integrals, limits).
Per-course additions go in videos/lex_<course>.py (WORDS, HOMOPHONES, TEX_TOKENS), merged below.
Latin letters in say= text are misread by the voice: write them in Hebrew letters (אִקְס, וַואי, אֶן).
"""
import re
from lexicon_base import *          # noqa: F401,F403
from lexicon_base import WORDS, SYMBOL, base_tex_say

# meaning-flipping mishearings to flag in the STT report: {what the recognizer wrote: what was said}
HOMOPHONES = {"שלא": "שלו", "הקלה": "הכלה", "לו": "לא"}

TEX_TOKENS = {
    r"\infty": "אינסוף", r"\to": "שואף ל", r"\rightarrow": "שואף ל", r"\Rightarrow": "גורר", r"\iff": "אם ורק אם",
    r"\in": "שייך ל", r"\notin": "לא שייך ל", r"\ne": "שונה מ", r"\neq": "שונה מ",
    r"=": "שווה", r"<": "קטן מ", r">": "גדול מ", r"\le": "קטן או שווה ל", r"\leq": "קטן או שווה ל",
    r"\ge": "גדול או שווה ל", r"\geq": "גדול או שווה ל", r"\cdot": "כפול", r"\times": "כפול", r"+": "ועוד", r"-": "פחות",
    r",": ",", r"^2": "בריבוע", r"^3": "בשלישית", r"\pi": "פאי", r"\alpha": "אלפא", r"\theta": "תטא", r"\varepsilon": "אפסילון",
    r"\epsilon": "אפסילון", r"\delta": "דלתא", r"\lambda": "למדא", r"\nabla": "נאבלה",
    "x": "אִקְס", "y": "וַואי", "z": "זֶד", "n": "אֶן", "k": "קֵיי", "r": "אָר", "t": "טִי", "u": "יוּ", "v": "וִי",
    "a": "אֵיי", "b": "בִּי", "c": "סִי", "f": "אֶף", "g": "גִ'י", "h": "אֵייץ'", "q": "קְיוּ", "p": "פִּי", "R": "אָר", "D": "דִּי",
}
import importlib, pathlib
for _f in sorted(pathlib.Path(__file__).parent.glob("lex_*.py")):   # per-course additions: lex_dec.py, lex_np.py, …
    _m = importlib.import_module(_f.stem)
    WORDS.update(getattr(_m, "WORDS", {}))
    HOMOPHONES.update(getattr(_m, "HOMOPHONES", {}))
    TEX_TOKENS.update(getattr(_m, "TEX_TOKENS", {}))
for d, s in DIGIT.items():                       # noqa: F405
    TEX_TOKENS[d] = s
_TOK = sorted(TEX_TOKENS, key=len, reverse=True)


def _spell(t):
    """speak a TeX span token by token; None if a token is unknown"""
    t = t.replace(r"\,", " ").replace(r"\ ", " ").replace(r"\mathrm", "").replace(r"\text", "")
    out, i = [], 0
    t = re.sub(r"\\overline\{([^{}]+)\}", r"⟨overline⟩{\1}", t)
    while i < len(t):
        c = t[i]
        if c in " {}":
            i += 1
            continue
        if t.startswith("⟨overline⟩", i):
            out.append("המשלים של")
            i += len("⟨overline⟩")
            continue
        m = re.match(r"_\{?(\d+)\}?", t[i:])
        if m:                                    # M_1, q_0: the index as a number word
            out.append(" ".join(DIGIT[d] for d in m.group(1)))   # noqa: F405
            i += m.end()
            continue
        if c == "(" and out:                     # f(x), L(M): "של"
            out.append("של")
            i += 1
            continue
        if c == ")":
            i += 1
            continue
        m = re.match(r"\d+(?:\.\d+)?", t[i:])
        if m and len(m.group(0)) > 1:            # 12, 0.9: as a number (the voice reads numerals well), not digit by digit
            out.append(m.group(0))
            i += m.end()
            continue
        hit = next((k for k in _TOK if t.startswith(k, i)), None)
        if hit is None:
            return None
        out.append(TEX_TOKENS[hit])
        i += len(hit)
    s = " ".join(out).replace(" ,", ",")
    s = re.sub(r"(^|\s)([לבמ])\s+", r"\1\2", s)      # "שייכת ל" + "אָר": one word, not the letter's name
    return re.sub(r"\s+", " ", s).strip() or None


def tex_say(tex):
    t = tex.strip()
    if re.fullmatch(r"q_\{?\d+\}?", t.replace(" ", "")):
        return base_tex_say(t)
    if re.fullmatch(r"[01]+", t):
        return word_say(t)                       # noqa: F405 — a word over {0,1}: digit by digit
    return _spell(t)
