# -*- coding: utf-8 -*-
"""P01 · מה זה תבנית עיצוב ואיך בוחרים? — video script (build: tools/video/vid.py P01).

Source: courses/pat/P01.js (lesson + goal: what a pattern gives, the three families, need sentence -> pattern name).
Exam anchor: 19B-B-Q13 (an aircraft that must also drive on the road -> Adapter), which no guided quiz uses and which
has no twin in the bank. Families and needs are checked against the course checker's rule table
(tools/verify/needhelp/pat/check.py, read through w_pat.RULES); Adapter is not in that table, so its family is
checked against the lesson's own family table.
Avoided on purpose: the P01 quiz items (19B-C-Q3, 23B-A-Q4, the Singleton-family question, the shop settings object,
the graphics-editor toolbar, the "ready code" statement) and the stock-price example of the lesson. Worked needs are
mine: a network game clock, a music editor's export format, a live sports score.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_pat as w
from app_config import SRC

# ---------------------------------------------------------------- facts (checked)
FAM = {"Creational": ["Singleton", "Factory", "AbstractFactory"], "Structural": ["Flyweight"],
       "Behavioral": ["Observer", "Command", "Mediator", "Chain"]}
for fam, pats in FAM.items():
    for p in pats:
        assert w.family(p) == fam, (p, w.family(p), fam)
assert w.family("MVC") == "Architectural"
LESSON = (SRC / "pat" / "P01.js").read_text(encoding="utf-8")
assert "<td><b>Structural</b> (מבנה)</td><td>איך מחברים מחלקות לשלם</td><td>Adapter, Flyweight</td>" in LESSON

# the three worked needs: each names exactly one pattern of the table
NEEDS = [("e1", {"single_instance"}, "Singleton"), ("e2", {"runtime_type"}, "Factory"),
         ("e3", {"notify_many_on_change"}, "Observer")]
for _, nd, pat in NEEDS:
    assert [p for p in w.RULES if w.solves(p, nd)] == [pat], (nd, pat)

# exam 19B-B-Q13
Q = BANK["19B-B-Q13"]
assert Q["correctIndex"] == 0 and "Adapter" in Q["options"][0] and "Interface" in Q["options"][1]
assert "Singleton" in Q["options"][2] and "Factory" in Q["options"][3]
OPTS = w.opts_of(Q)

ADAPT = w.uml("ad", [
    dict(key="game", name="Game", x=20, y=56, w=200, role="הלקוח"),
    dict(key="road", name="RoadVehicle", x=330, y=20, w=300, kind="interface", members=["+ drive()"]),
    dict(key="adp", name="PlaneAdapter", x=330, y=300, w=300, members=["- plane : Aircraft", "+ drive()"],
         role="המתאם", hidden=True),
    dict(key="air", name="Aircraft", x=760, y=300, w=220, members=["+ fly()", "+ taxi()"], role="מחלקה קיימת"),
], [
    dict(key="use", a="game", b="road", kind="call", sides="rl", hidden=False),
    dict(key="impl", a="adp", b="road", kind="impl", sides="tb"),
    dict(key="has", a="adp", b="air", kind="has", sides="rl", label="taxi()", lxy=(662, 330)),
], w=1000, h=480)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נבין מה זו תבנית עיצוב, ולמה צריך אותה."),
    P("נכיר את שלוש המשפחות, ונלמד מתכון קצר לשאלה ״באיזו תבנית תשתמשו״."),
    P("ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">P01 · תבניות עיצוב</div><h1>מה זה תבנית עיצוב ואיך בוחרים?</h1>'
         '<p>להסביר מה תבנית עיצוב נותנת, לשייך תבנית למשפחה שלה, ולהמיר משפט צורך בתיאור מערכת לשם של תבנית.</p>',
   layout="title")

idea = Scene("idea", "הרעיון", [
    P("מתכנתים נתקלים שוב ושוב באותן בעיות עיצוב.", do=show("i-p1")),
    P("איך מוודאים שיש רק אובייקט אחד מסוג מסוים? איך מעדכנים כמה מסכים כשמשהו משתנה?", do=show("i-p2")),
    P("תבנית עיצוב היא **פתרון כללי ומוכח** לבעיה כזו, בעיה שחוזרת.", do=show("i-def")),
    P("היא לא קוד שמעתיקים. היא רעיון, ובכל מערכת מממשים אותו קצת אחרת.", do=show("i-c1")),
    P("והיא שומרת ידע של מתכננים מנוסים: ״כשיש בעיה כזו, כך פותרים אותה״.", do=show("i-c2")),
    P("יש לה גם שם. אומרים ״כאן צריך Observer״, וכל הצוות מבין את כל המבנה בבת אחת.", do=show("i-c3"), hold=0.4),
], stage=w.stack(
    f'<div id="i-p1" class="card ex h">בעיה: ״רק אובייקט אחד מהסוג הזה!״</div>',
    f'<div id="i-p2" class="card ex h">בעיה: ״כשהנתון משתנה, שלושה מסכים חייבים לדעת״</div>',
    f'<div id="i-def" class="card rule h" style="font-size:36px">🔑 <b>תבנית עיצוב</b> = פתרון כללי ומוכח לבעיית עיצוב שחוזרת</div>',
    gap=30),
   panel=st.card("i-c1", "trap", "⚠️ לא קוד להעתקה: רעיון שמתאימים למערכת")
         + st.card("i-c2", "rule", "🔑 שימור והעברה של ידע עיצובי")
         + st.card("i-c3", "ex", "שם משותף = שפה משותפת לצוות"))

def fam_col(cls, he, en, sub, chips):
    return (f'<div class="pt-fam {cls}" id="f-{cls}"><span class="pt-fh">{he}</span><span class="pt-fs pt-mono">{en}</span>'
            f'<span class="pt-fs">{sub}</span>' + "".join(w.chip(f"f-{cls}-{k}", w.mono(c), cls) for k, c in enumerate(chips))
            + "</div>")


FAMS = ('<div class="pt-fams" id="fams">'
        + fam_col("cr", "יצירה", "Creational", "איך יוצרים אובייקטים", ["Singleton", "Factory Method", "Abstract Factory"])
        + fam_col("st", "מבנה", "Structural", "איך מחברים מחלקות לשלם", ["Adapter", "Flyweight"])
        + fam_col("be", "התנהגות", "Behavioral", "איך אובייקטים מדברים", ["Observer", "Command", "Mediator", "Chain"])
        + "</div>")

families = Scene("fam", "שלוש המשפחות", [
    P("את התבניות מחלקים לשלוש משפחות, לפי השאלה שהן עונות עליה."),
    P("משפחת **היצירה** עונה על השאלה: איך יוצרים אובייקטים.", do=show("f-c1")),
    P("כאן Singleton, Factory Method ו-Abstract Factory.", do=show("f-cr-0", "f-cr-1", "f-cr-2")),
    P("משפחת **המבנה**: איך מחברים מחלקות לשלם אחד. כאן Adapter ו-Flyweight.", do=show("f-c2", "f-st-0", "f-st-1")),
    P("משפחת **ההתנהגות**: איך אובייקטים מדברים זה עם זה.", do=show("f-c3")),
    P("כאן Observer, Command, Mediator, ושרשרת האחריות.", do=show("f-be-0", "f-be-1", "f-be-2", "f-be-3"),
      say="כאן אוֹבְּזֶרְבֶר, קוֹמָאנְד, מֶדְיֵאטוֹר, ושרשרת האחריות."),
    P("ובקורס יש גם את MVC. היא מחלקת מערכת שלמה לשכבות של נתונים, תצוגה ובקרה.", do=show("f-mvc"), hold=0.4),
], stage=w.stack(FAMS, w.chip("f-mvc", "ומחוץ למשפחות: " + w.mono("MVC") + " · שכבות של מערכת שלמה", "", True), gap=26),
   panel=st.card("f-c1", "rule", "🔑 יצירה: <b>מי יוצר</b> ואיך")
         + st.card("f-c2", "rule", "🔑 מבנה: <b>איך מחברים</b> מחלקות")
         + st.card("f-c3", "rule", "🔑 התנהגות: <b>מי מדבר עם מי</b>"))

recipe = Scene("recipe", "המתכון", [
    P("ועכשיו המתכון לשאלה ״באיזו תבנית תשתמשו?״. שלושה צעדים.", do=show("r-s1")),
    P("אחת: קוראים את התיאור, וכותבים את **הצורך** במשפט אחד."),
    P("שתיים: מוצאים את התבנית שעונה על הצורך הזה.", do=show("r-s2")),
    P("שלוש: רק עכשיו קוראים את התשובות, ובודקים שגם **התפקידים** בהן נכונים.", do=show("r-s3"), hold=0.3),
    P("ננסה. במשחק רשת יש שעון משחק, וכל הרכיבים חייבים לקרוא את **אותו** זמן.", do=show("e1")),
    P("הצורך: מופע אחד בלבד, שכולם ניגשים אליו. זו Singleton.", do=show("e1-p")),
    P("עורך מוזיקה מייצא שיר לקובץ, והמשתמש בוחר בכל פעם פורמט אחר.", do=show("e2")),
    P("הצורך: סוג האובייקט שנוצר ידוע רק בזמן ריצה. זו Factory.", do=show("e2-p")),
    P("ואפליקציית ספורט: כשהתוצאה משתנה, האפליקציה, האתר והלוח באצטדיון חייבים להתעדכן.", do=show("e3")),
    P("הצורך: דבר אחד משתנה, וכמה רכיבים צריכים לדעת. זו Observer.", do=show("e3-p"), hold=0.3),
    P("ושימו לב: מילה טכנית בתשובה, כמו ״ירושה״ או ״מופע גלובלי״, היא לא סיבה לבחור. הצורך קובע.",
      do=show("r-t"), hold=0.4),
], stage=w.stack(
    *[f'<div id="{i}" class="pt-need h"><span class="pt-nd">{t}</span><span class="pt-arr">←</span>'
      f'<span id="{i}-p" class="pt-pat h">{p}</span></div>'
      for i, t, p in [("e1", "שעון משחק אחד, שכולם קוראים ממנו", "Singleton"),
                      ("e2", "פורמט הייצוא נבחר רק בזמן ריצה", "Factory"),
                      ("e3", "התוצאה משתנה ← שלושה מסכים מתעדכנים", "Observer")]],
    st.card("r-t", "trap", "⚠️ מילה טכנית בתשובה ≠ התאמה. קודם הצורך, אחר כך התבנית"),
    gap=26),
   panel=st.card("r-s1", "ex", "1️⃣ הצורך במשפט אחד")
         + st.card("r-s2", "ex", "2️⃣ התבנית שעונה עליו")
         + st.card("r-s3", "ex", "3️⃣ רק אז התשובות, כולל התפקידים"))

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו שאלה ממבחן. במשחק יש אובייקטים שנוסעים על הכביש, ואובייקטים שטסים באוויר."),
    P("רוצים להוסיף כלי טיס שיודע גם לנסוע על הכביש. באיזו תבנית נשתמש?"),
    P("צעד ראשון, הצורך. המשחק עובד מול ממשק של כלי כביש, שיש לו פעולת נסיעה.", do=show("ad")),
    P("וכלי הטיס הוא מחלקה **קיימת**, עם ממשק אחר לגמרי: לטוס, ולנסוע על המסלול.", do=show("ad-hb-air")),
    P("הצורך: **להתאים** ממשק קיים לממשק שהמשחק מצפה לו. זו Adapter, ממשפחת המבנה.", do=hide("ad-hb-air") + show("x-1")),
    P("המתאם מממש את הממשק של הכביש, ומחזיק בתוכו את כלי הטיס.", do=show("ad-b-adp", "ad-a-impl", "ad-a-has")),
    P("כשהמשחק מבקש לנסוע, המתאם מעביר את הבקשה לנסיעה של המטוס על הקרקע.", do=show("ad-hb-adp")),
    P("כמו מתאם לשקע בחו״ל: לא משנים את המכשיר ולא את השקע. רק מוסיפים חתיכה באמצע.", do=show("x-2")),
    P("לכן התשובה היא Adapter.", do=show("q-ok-0")),
    P("Interface מפתה, כי באמת יש כאן ממשק. אבל ממשק הוא כלי של השפה, ולא תבנית עיצוב.",
      do=show("q-x-1", "q-n-1")),
    P("Singleton עונה על מופע אחד בלבד. אין כאן שום דרישה כזו.", do=show("q-x-2", "q-n-2")),
    P("ו-Factory עונה על בחירת הסוג שנוצר בזמן ריצה. גם זה לא הצורך כאן.", do=show("q-x-3", "q-n-3"), hold=0.5),
], stage=w.stack(ADAPT, w.row(st.card("x-1", "rule", "🔑 להתאים ממשק קיים ← <b>Adapter</b>"),
                                        st.card("x-2", "ex", "🔌 מתאם לשקע: שום צד לא משתנה"), gap=20), gap=18),
   panel=w.stem(Q["id"], "במשחק יש אובייקטים שנוסעים על כביש ואובייקטים שטסים. רוצים כלי טיס שיודע גם לנסוע על הכביש. "
                          "באיזו תבנית נשתמש?")
         + st.options("q", OPTS, notes={1: "כלי של השפה", 2: "מופע יחיד", 3: "יצירה לפי סוג"}))

recap = Scene("recap", "סיכום", [
    P("לסיכום: תבנית עיצוב היא פתרון כללי ומוכח לבעיה שחוזרת. רעיון, לא קוד להעתקה.", do=show("s-1")),
    P("שלוש משפחות: יצירה, מבנה והתנהגות.", do=show("s-2")),
    P("ובכל שאלה: קודם הצורך במשפט אחד, אחר כך התבנית, ורק בסוף התשובות. נתראה ברמה הבאה.", do=show("s-3"), hold=0.6),
], stage=w.stack(FAMS.replace('id="', 'id="z').replace(' h"', '"'), gap=20),
   panel=st.card("s-1", "rule", "🔑 תבנית = פתרון כללי ומוכח")
         + st.card("s-2", "rule", "🔑 יצירה · מבנה · התנהגות")
         + st.card("s-3", "rule", "🔑 צורך ← תבנית ← תשובות"))

SCENES = [title, idea, families, recipe, exam, recap]
w.no_latin(SCENES)
VIDEO = Video("P01", "pat", "מה זה תבנית עיצוב ואיך בוחרים?", SCENES, bank={"19B-B-Q13": 0})
