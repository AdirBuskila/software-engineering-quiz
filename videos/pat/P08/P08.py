# -*- coding: utf-8 -*-
"""P08 · Chain, Flyweight ו-Mediator — video script (build: tools/video/vid.py P08).

Source: courses/pat/P08.js (lesson + goal: recognise from a short description Chain of Responsibility, Flyweight or
Mediator). Exam part: an original question "בסגנון מבחן" (bank={}): every free bank item on these three patterns is
a content twin of a guided-quiz item (23-EX-Q10 ~ 25-EX-Q5, 25-EX-Q1 ~ 23-EX-Q6, 25-EX-Q2 ~ 23-EX-Q7), and the pair
23-EX-Q8 / 25-EX-Q3 ("what differs between Observer and Mediator") is keyed inconsistently in the bank (the same
claim "Observer: dependency of one state on the state of many" is wrong in 23-EX-Q8 and the key in 25-EX-Q3), so
it is not used. The original question maps three new scenarios to patterns; exactly one mapping agrees with the
course checker's rule table (w_pat.RULES), asserted below.
Worked numbers are computed: the approval chain (Python run of the handlers), the shared glyphs (distinct characters
of the text), the links with and without a mediator (n(n-1)/2 vs n).
Avoided on purpose: the P08 quiz items (support tiers, 50,000 trees, the chat room, the Singleton/Flyweight and
Mediator/Observer comparisons, "first capable handler"). Mine: expense approval, a text editor's glyphs, a control
tower; in the question, GUI help requests, smoke particles sharing one texture, a registration form. The pipeline
contrast and the "first capable handler" wording (25-EX-Q5's option) are not used; game tiles/trees (P08-Q2) neither.
"""
import math

from vid import P, Scene, Video, show, hide
import stage as st
import w_pat as w

# ---------------------------------------------------------------- chain: expense approval (run)
HANDLERS = [("tl", "ראש צוות", 500), ("mg", "מנהלת", 5000), ("dr", "סמנכ״ל", math.inf)]


def run_chain(amount):
    asked = []
    for key, _, limit in HANDLERS:
        asked.append(key)
        if amount <= limit:
            return asked, key
    raise AssertionError("no handler")


A1, H1 = run_chain(1200)
A2, H2 = run_chain(300)
assert (A1, H1) == (["tl", "mg"], "mg") and (A2, H2) == (["tl"], "tl")

# ---------------------------------------------------------------- flyweight: glyphs (counted)
TEXT = "the quick brown fox jumps over the lazy dog " * 250
N_CHARS, N_GLYPHS = len(TEXT), len(set(TEXT))
assert (N_CHARS, N_GLYPHS) == (11000, 27)

# ---------------------------------------------------------------- mediator: links (counted)
N_PLANES = 6
MESH, STAR = N_PLANES * (N_PLANES - 1) // 2, N_PLANES
assert (MESH, STAR) == (15, 6)


def net_svg(pfx, star, hidden=True):
    cx, cy, r = 190, 170, 130
    pts = [(cx + r * math.cos(2 * math.pi * k / N_PLANES - math.pi / 2), cy + r * math.sin(2 * math.pi * k / N_PLANES - math.pi / 2))
           for k in range(N_PLANES)]
    lines = ([(p, (cx, cy)) for p in pts] if star else
             [(pts[i], pts[j]) for i in range(N_PLANES) for j in range(i + 1, N_PLANES)])
    assert len(lines) == (STAR if star else MESH)
    o = [f'<svg id="{pfx}" class="pt-uml{" h" if hidden else ""}" viewBox="0 0 380 340" width="380" height="340" direction="ltr">']
    o += [f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" class="pt-ln-s"/>' for a, b in lines]
    o += [f'<circle cx="{x:.1f}" cy="{y:.1f}" r="24" class="pt-box"/><text x="{x:.1f}" y="{y + 9:.1f}" class="pt-name">✈</text>'
          for x, y in pts]
    if star:
        o.append(f'<circle cx="{cx}" cy="{cy}" r="34" class="pt-box interface"/><text x="{cx}" y="{cy + 10}" class="pt-name">🗼</text>')
    o.append("</svg>")
    return "".join(o)


# ---------------------------------------------------------------- the exam-style question (original)
NEEDS = {"help": {"first_capable_handles"}, "smoke": {"many_similar_objects_memory"}, "form": {"central_communication"}}
NAME = {"Chain": "Chain", "Flyweight": "Flyweight", "Mediator": "Mediator", "Singleton": "Singleton", "Observer": "Observer"}
MAPS = [{"help": "Chain", "smoke": "Flyweight", "form": "Mediator"},
        {"help": "Mediator", "smoke": "Flyweight", "form": "Chain"},
        {"help": "Chain", "smoke": "Singleton", "form": "Mediator"},
        {"help": "Observer", "smoke": "Flyweight", "form": "Mediator"}]
OK = [all(w.solves(m[s], NEEDS[s]) for s in NEEDS) for m in MAPS]
assert OK == [True, False, False, False]
assert w.family("Chain") == w.family("Mediator") == "Behavioral" and w.family("Flyweight") == "Structural"
OPTS = [(k, f'עזרה: {w.mono(NAME[m["help"]])} · חלקיקים: {w.mono(NAME[m["smoke"]])} · טופס: {w.mono(NAME[m["form"]])}')
        for k, m in enumerate(MAPS)]


def node(id_, he, sub, tag=None, ok=True):
    t = f'<span id="{id_}-t" class="pt-tag {"ok" if ok else "bad"} h">{tag}</span>' if tag else ""
    return f'<div id="{id_}" class="pt-node">{he}<span class="pt-sub">{sub}</span>{t}</div>'


def chain_row(pfx, asked, handler):
    parts = []
    for k, (key, he, lim) in enumerate(HANDLERS):
        sub = f"עד {lim:,}" if lim != math.inf else "כל סכום"
        tag = ("מטפל ✓" if key == handler else "לא יכול ←") if key in asked else None
        parts.append(node(f"{pfx}-{key}", he, sub, tag, key == handler))
        if k < len(HANDLERS) - 1:
            parts.append('<span class="pt-fa">←</span>')
    return f'<div class="pt-flow" style="direction:rtl;margin-bottom:40px">{"".join(parts)}</div>'


# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נכיר שלוש תבניות קצרות: שרשרת האחריות, Flyweight ו-Mediator.",
      say="בסרטון הזה נכיר שלוש תבניות קצרות: שרשרת האחריות, פְלַיְיווֵייט ומֶדְיֵאטוֹר."),
    P("לא צריך לדעת לממש אותן. צריך לזהות אותן מתיאור קצר."),
    P("ובסוף נפתור שאלה בסגנון מבחן.", hold=0.4),
], stage='<div class="kicker">P08 · תבניות עיצוב</div><h1>Chain, Flyweight ו-Mediator</h1>'
         '<p>לזהות לפי תיאור קצר מתי מדובר ב-Chain of Responsibility, ב-Flyweight או ב-Mediator.</p>', layout="title")

chain = Scene("chain", "שרשרת האחריות", [
    P("נתחיל בשרשרת האחריות. בקשה עוברת בשרשרת של מטפלים, אחד אחרי השני.", do=show("ch-1")),
    P("כל מטפל שואל: אני יכול לטפל בזה? אם כן, הוא מטפל, והשרשרת **נעצרת**. אם לא, הוא מעביר הלאה.", do=show("k-1")),
    P("דוגמה: אישור הוצאות. ראש צוות מאשר עד חמש מאות שקל, המנהלת עד חמשת אלפים, והסמנכ״ל כל סכום."),
    P("בקשה על אלף ומאתיים. ראש הצוות לא יכול, ומעביר.", do=show("c1-tl-t")),
    P("המנהלת יכולה. היא מאשרת, והבקשה לא מגיעה בכלל לסמנכ״ל.", do=show("c1-mg-t")),
    P("ובקשה על שלוש מאות? ראש הצוות מטפל בה בעצמו, וזהו.", do=show("ch-2", "c2-tl-t")),
    P("ואם נוסיף בעתיד דרג חדש, למשל סמנכ״ל כספים, פשוט מכניסים אותו לשרשרת במקום הנכון.", hold=0.4),
], stage=w.stack(f'<div id="ch-1" class="h">{chain_row("c1", A1, H1)}</div>',
                 f'<div id="ch-2" class="h">{chain_row("c2", A2, H2)}</div>', gap=30),
   panel=st.card("k-1", "rule", "🔑 מי שיכול מטפל, והשרשרת נעצרת"))

fly = Scene("flyweight", "Flyweight", [
    P("עכשיו Flyweight. מעבד תמלילים מציג מסמך של אחד עשר אלף תווים.", do=show("f-1")),
    P("אם כל תו יהיה אובייקט שלם, עם הצורה של האות, יהיו אחד עשר אלף אובייקטים כבדים."),
    P("אבל יש רק עשרים ושבעה תווים שונים במסמך הזה: עשרים ושש אותיות, ורווח.", do=show("f-2")),
    P("אז שומרים אובייקט אחד לכל תו, ו**משתפים** אותו. כל מקום במסמך רק מצביע עליו.", do=show("f-3")),
    P("מה שמשותף, צורת האות, נשמר פעם אחת. מה שמשתנה, המיקום, נשמר מחוץ לאובייקט.", do=show("y-1")),
    P("הצורך: המון אובייקטים כמעט זהים, וזיכרון שנגמר. זו Flyweight, ממשפחת המבנה.", do=show("y-2"), hold=0.4),
], stage=w.stack(w.chip("f-1", f"{N_CHARS:,} תווים במסמך", "", True),
                 w.chip("f-2", f"רק {N_GLYPHS} תווים שונים", "st", True),
                 w.chip("f-3", f"{N_GLYPHS} אובייקטים משותפים, במקום {N_CHARS:,}", "ok", True), gap=34),
   panel=st.card("y-1", "ex", "משותף (צורת האות): פעם אחת<br>משתנה (המיקום): בחוץ")
         + st.card("y-2", "rule", "🔑 הרבה אובייקטים דומים + זיכרון ← Flyweight"))

med = Scene("mediator", "Mediator", [
    P("והאחרונה: Mediator, המתווך. שישה מטוסים מתקרבים לשדה תעופה.", do=show("m-1")),
    P("אם כל מטוס ידבר ישירות עם כל האחרים, יש חמישה עשר קווי שיחה, וכל מטוס צריך להכיר את כולם."),
    P("במקום זה, כולם מדברים רק עם מגדל הפיקוח. שישה קווים בלבד.", do=hide("m-1") + show("m-2", "m-c1")),
    P("המטוסים לא מכירים זה את זה. המגדל מתאם ביניהם.", do=show("m-c2")),
    P("הצורך: רכיבים רבים שצריכים לתאם, בלי שכל אחד יכיר את כולם. זו Mediator.", do=show("m-c3"), hold=0.4),
], stage=f'<div class="swap" style="--swap-h:360px;width:400px"><div>{net_svg("m-1", False)}</div><div>{net_svg("m-2", True)}</div></div>',
   panel=st.card("m-c1", "ex", f"ישירות: {MESH} קווים · דרך המגדל: {STAR}")
         + st.card("m-c2", "plain", "הרכיבים לא מכירים זה את זה")
         + st.card("m-c3", "rule", "🔑 תקשורת דרך אובייקט מרכזי ← Mediator"))

SCEN = [("s-h", "עזרה", "בממשק גרפי, בקשת עזרה עוברת מהכפתור לחלון שמכיל אותו ומשם לאפליקציה. מי שיש לו טקסט עזרה מציג אותו, והבקשה לא ממשיכה."),
        ("s-t", "חלקיקים", "אפקט עשן במשחק: מאה אלף חלקיקים, שכולם משתמשים באותה תמונה ובאותה טקסטורה."),
        ("s-f", "טופס", "בטופס הרשמה, התיבות, הרשימות והכפתור לא מכירים זה את זה. אובייקט הטופס מתאם ביניהם.")]
exam = Scene("exam", "שאלה בסגנון מבחן", [
    P("ועכשיו שאלה בסגנון מבחן: שלושה תרחישים. איזו התאמה של תבניות נכונה?",
      do=show("s-h", "s-t", "s-f")),
    P("תרחיש העזרה: הבקשה עוברת מחלון לחלון, עד שמישהו יכול לענות עליה. זו שרשרת האחריות.", do=show("s-h-p")),
    P("החלקיקים: מאה אלף אובייקטים עם אותה טקסטורה. משתפים את מה שזהה. זו Flyweight.", do=show("s-t-p")),
    P("והטופס: רכיבים שלא מכירים זה את זה, ומתאמים דרך אובייקט מרכזי. זו Mediator.", do=show("s-f-p")),
    P("לכן ההתאמה הנכונה: שרשרת, Flyweight, Mediator.", do=show("q-ok-0"),
      say="לכן ההתאמה הנכונה: שרשרת, פְלַיְיווֵייט, מֶדְיֵאטוֹר."),
    P("ההתאמה שמחליפה בין העזרה לטופס נופלת: הטופס לא מעביר בקשה הלאה, והעזרה לא עוברת דרך מתווך.",
      do=show("q-x-1", "q-n-1")),
    P("Singleton לחלקיקים? Singleton היא מופע **אחד**. כאן יש מאה אלף חלקיקים, שמשתפים טקסטורה.",
      do=show("q-x-2", "q-n-2")),
    P("ו-Observer לעזרה? ב-Observer **כל** הרשומים מקבלים עדכון. כאן הבקשה נעצרת אצל מי שיש לו טקסט עזרה.",
      do=show("q-x-3", "q-n-3"), hold=0.5),
], stage=w.stack(*[f'<div id="{i}" class="pt-need h" style="font-size:26px"><span class="pt-nd"><b>{n}:</b> {t}</span>'
                   f'<span id="{i}-p" class="pt-pat h" style="min-width:150px">{p}</span></div>'
                   for (i, n, t), p in zip(SCEN, ["Chain", "Flyweight", "Mediator"])], gap=18),
   panel=w.tight(f'<div class="qstem"><span class="qid">בסגנון מבחן</span>איזו התאמה של תבנית לכל תרחיש נכונה?</div>'
                 + st.options("q", OPTS, notes={1: "הוחלפו", 2: "לא מופע אחד", 3: "לא כולם"})))

recap = Scene("recap", "סיכום", [
    P("לסיכום: בשרשרת האחריות הבקשה עוברת ממטפל למטפל, עד שמישהו יכול לטפל בה.", do=show("r-1")),
    P("Flyweight משתפת אובייקטים זהים כדי לחסוך בזיכרון.", do=show("r-2")),
    P("ו-Mediator מרכזת את התקשורת באובייקט אחד, כך שהרכיבים לא מכירים זה את זה. נתראה ברמה הבאה.",
      do=show("r-3"), hold=0.6),
], stage=w.stack(net_svg("z-net", True, hidden=False), gap=20),
   panel=st.card("r-1", "rule", "🔑 Chain: עוברת עד שמישהו מטפל")
         + st.card("r-2", "rule", "🔑 Flyweight: שיתוף ← חיסכון בזיכרון")
         + st.card("r-3", "rule", "🔑 Mediator: תקשורת דרך מרכז"))

SCENES = [title, chain, fly, med, exam, recap]
w.no_latin(SCENES)
VIDEO = Video("P08", "pat", "Chain, Flyweight ו-Mediator", SCENES, bank={})
