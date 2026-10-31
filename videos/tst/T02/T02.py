# -*- coding: utf-8 -*-
"""T02 · מודל V: מתכננים לאורך הדרך, מריצים בסוף — video script (build: tools/video/vid.py T02).

Source: courses/tst/T02.js (lesson + goal). Exam anchor: 21-B-Q5 ("in all V development stages: tests are planned
AND executed"), used by no guided quiz. Not used on purpose: the T02 quiz (T02-Q1..Q3, 25F0b-Q5, 25B-N-Q8), the T08
boss items 25S-A-Q5 / 25F0a-Q6, the twin 21S-B-Q5, and 25F0a-Q4 / 26CL-Q3 (content twins of T02-Q3 / T02-Q2).
Worked example: a new parking-reservation app (a requirement, a module), not any quiz scenario.
The plan / run order is not typed by hand: it is read from the course checker (check.py PLAN_ORDER, executed in
reverse) and the badges on the V are generated from it.
"""
import ast
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_tst as w

# ---------------------------------------------------------------- the checker's order (read, not run)
_lit = {n.targets[0].id: ast.literal_eval(n.value) for n in ast.parse(w.checker_src()).body
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)
        and n.targets[0].id in ("PLAN_ORDER", "STAGE")}
PLAN = _lit["PLAN_ORDER"]                     # ["acceptance", "system", "unit"]: planned top -> down
EXEC = list(reversed(PLAN))                   # executed after coding, small to large
assert PLAN == ["acceptance", "system", "unit"] and EXEC[0] == "unit" and EXEC[-1] == "acceptance"
assert _lit["STAGE"]["acceptance"] == "requirements" and _lit["STAGE"]["unit"] == "module design"

LEFT = [("req", "ניתוח דרישות"), ("sys", "עיצוב המערכת"), ("mod", "עיצוב המודולים")]
RIGHT = [("acceptance", "בדיקות קבלה"), ("system", "מערכת ושילוב"), ("unit", "בדיקות יחידה")]
assert [k for k, _ in RIGHT] == PLAN          # row k of the V = the k-th test planned
# the badge numbers drawn by w_tst.vmodel: plan = row + 1, run = n - row; they must equal the checker's orders
for k, (key, _) in enumerate(RIGHT):
    assert PLAN.index(key) + 1 == k + 1 and EXEC.index(key) + 1 == len(RIGHT) - k

V = lambda pfx, **k: w.vmodel(pfx, LEFT, RIGHT, "קידוד", **k)

# ---------------------------------------------------------------- exam 21-B-Q5
Q = BANK["21-B-Q5"]
assert Q["correctIndex"] == 1 and Q["options"][1] == "מבצעים ומתכננים בדיקות"
assert Q["options"][2] == "מתכננים בדיקות" and Q["options"][3] == "מבצעים בדיקות" and "לא מתבצעות" in Q["options"][0]
OPTS = w.opts_of(Q, order=[2, 3, 1, 0])

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נכיר את מודל V.", say="בסרטון הזה נכיר את מודל וִי."),
    P("נראה איזו בדיקה מתוכננת מול כל שלב פיתוח, ובאיזה סדר הבדיקות רצות."),
    P("ונבין במה הוא שונה ממודל מפל המים.", hold=0.4),
], stage='<div class="kicker">T02 · בדיקות תוכנה</div><h1>מודל V: מתכננים לאורך הדרך, מריצים בסוף</h1>'
         '<p>כל שלב פיתוח מקבל בדיקה תואמת. מה שמתוכנן ראשון, מבוצע אחרון.</p>', layout="title")

idea = Scene("idea", "צורת ה-V", [
    P("מודל V הוא וריאציה של מפל המים. הפיתוח יורד בצד השמאלי של האות V.", do=show("va-arL"),
      say="מודל וִי הוא וריאציה של מפל המים. הפיתוח יורד בצד השמאלי של האות וִי."),
    P("מתחילים בניתוח הדרישות, ממשיכים לעיצוב המערכת, ואז לעיצוב המודולים."),
    P("בתחתית נמצא הקידוד.", hold=0.3),
    P("ומשם עולים בצד הימני: בדיקות יחידה, בדיקות מערכת ושילוב, ובסוף בדיקות קבלה.", do=show("va-arR")),
    P("הרעיון המרכזי: **כל שלב פיתוח מקושר לשלב בדיקה תואם**, באותו גובה.", do=show("va-k0", "va-k1", "va-k2")),
    P("ככה לכל החלטה שקיבלנו בדרך יש בדיקה שתוודא אותה.", do=show("id-c1"), hold=0.4),
], stage=V("va", links_hidden=True, arrows_hidden=True), panel=st.card("id-c1", "rule", "🔑 לכל שלב פיתוח יש שלב בדיקה תואם, באותו גובה"))

pairs = Scene("pairs", "מי מול מי", [
    P("נעבור שורה שורה, עם דוגמה: אפליקציה להזמנת חניה.", do=show("vb-k0")),
    P("בניתוח הדרישות כתוב: משתמש יכול להזמין חניה ולקבל אישור.", do=show("pa-c1")),
    P("כבר עכשיו אפשר לכתוב את תרחיש **בדיקת הקבלה**: הלקוח מזמין, ומקבל אישור.", do=show("pa-c2")),
    P("בעיצוב המערכת מחליטים על הרכיבים ועל החיבורים ביניהם.", do=show("vb-k1")),
    P("מולו מתכננים את **בדיקות המערכת והשילוב**: שהרכיבים עובדים יחד.", do=show("pa-c3")),
    P("ובעיצוב המודולים מתכננים מודול אחד, למשל המודול שמחשב את מחיר החניה.", do=show("vb-k2")),
    P("מולו מתכננים את **בדיקות היחידה** של המודול הזה.", do=show("pa-c4"), hold=0.3),
    P("בדיקה מהירה: רכיב ההזמנות צריך לדבר עם רכיב התשלום. באיזו שורה של ה-V נכתבת הבדיקה של החיבור ביניהם?",
      say="בדיקה מהירה: רכיב ההזמנות צריך לדבר עם רכיב התשלום. באיזו שורה של הוִי נכתבת הבדיקה של החיבור ביניהם?", hold=0.8),
    P("החיבור בין רכיבים הוחלט בעיצוב המערכת, אז השורה האמצעית: מערכת ושילוב.", hold=0.4),
], stage=V("vb", links_hidden=True),
   panel=st.card("pa-c1", "plain", "🅿️ דרישה: מזמינים חניה ומקבלים אישור")
         + st.card("pa-c2", "ex", "דרישות ← <b>בדיקת קבלה</b>")
         + st.card("pa-c3", "ex", "עיצוב המערכת ← <b>מערכת ושילוב</b>")
         + st.card("pa-c4", "ex", "עיצוב המודולים ← <b>בדיקות יחידה</b>"))

order = Scene("order", "תכנון מול ביצוע", [
    P("עכשיו הסדר. נעקוב אחרי הפרויקט מלמעלה: בכל שלב פיתוח כותבים את תוכנית הבדיקה שמולו.", do=show("vc-pl0")),
    P("המספרים הכחולים מראים באיזה סדר נכתבו תוכניות הבדיקה.", do=show("vc-pl1", "vc-pl2", "or-c1")),
    P("אבל להריץ בדיקה אפשר רק כשיש קוד שרץ. אז נרד עד הקידוד, ונעלה בצד השני."),
    P("המספרים הירוקים מראים באיזה סדר הבדיקות באמת רצות.", do=show("vc-ex2", "vc-ex1", "vc-ex0", "or-c2"), hold=0.3),
    P("עצרו רגע, והשוו בעצמכם בכל שורה את המספר הכחול לירוק. מה אתם רואים?", hold=0.6),
    P("בשאלות על מודל V, תמיד בדקו אם שואלים על **תכנון** או על **ביצוע**, וקראו את המספר הנכון.", do=show("or-c3"),
      say="בשאלות על מודל וִי, תמיד בדקו אם שואלים על תכנון או על ביצוע, וקראו את המספר הנכון.", hold=0.4),
], stage=V("vc"),
   panel=st.card("or-c1", "ex", "🔵 מספר כחול: סדר כתיבת תוכנית הבדיקה")
         + st.card("or-c2", "ex", "🟢 מספר ירוק: סדר ההרצה")
         + st.card("or-c3", "trap", "⚠️ שואלים על תכנון או על ביצוע?"))

water = Scene("water", "ומפל המים?", [
    P("ובמה זה שונה ממפל המים? שם השלבים באים בשורה אחת: דרישות, עיצוב, קידוד, ואז בדיקות.", do=show("wa-c1")),
    P("עכשיו הסתכלו על ה-V: הקווים המקווקווים מחברים כל שלב בצד שמאל לשלב בצד ימין.",
      say="עכשיו הסתכלו על הוִי: הקווים המקווקווים מחברים כל שלב בצד שמאל לשלב בצד ימין.", do=show("wa-c2")),
    P("נסו למצוא את הקווים האלה בשורה של מפל המים. אין להם מקום שם.", hold=0.4),
], stage=V("vd"),
   panel=st.card("wa-c1", "plain", "מפל המים: דרישות ← עיצוב ← קידוד ← בדיקות")
         + st.card("wa-c2", "ex", "<bdi>V</bdi>: קו מקווקו בין כל שלב לבדיקה שמולו"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: בפיתוח במודל V, בכל שלבי הפיתוח, מה עושים עם הבדיקות?",
      say="שאלה ממבחן: בפיתוח במודל וִי, בכל שלבי הפיתוח, מה עושים עם הבדיקות?"),
    P("נסתכל על ה-V כולו. בצד השמאלי, בירידה, **מתכננים** בדיקה מול כל שלב.", do=show("ve-pl0", "ve-pl1", "ve-pl2"),
      say="נסתכל על הוִי כולו. בצד השמאלי, בירידה, מתכננים בדיקה מול כל שלב."),
    P("ובצד הימני, בעלייה, **מבצעים** אותן.", do=show("ve-ex0", "ve-ex1", "ve-ex2")),
    P("אז לאורך שלבי המודל עושים את שני הדברים: גם מתכננים וגם מבצעים.", do=show("q-ok-1"), hold=0.3),
    P("רק מתכננים? זה רק הצד השמאלי. הבדיקות המתוכננות גם רצות בסוף.", do=show("q-x-2", "q-n-2")),
    P("רק מבצעים? אז מאבדים את כל הרעיון: התכנון מראש, מול כל שלב.", do=show("q-x-3", "q-n-3")),
    P("והאפשרות שבדיקות לא מתבצעות כלל נופלת מיד: חצי מה-V הוא בדיקות.", do=show("q-x-0", "q-n-0"),
      say="והאפשרות שבדיקות לא מתבצעות כלל נופלת מיד: חצי מהוִי הוא בדיקות.", hold=0.5),
], stage=V("ve"),
   panel=w.stem(Q["id"], "בפיתוח מודל ה-<bdi>V</bdi>, בכל שלבי הפיתוח:")
         + st.options("q", OPTS, notes={2: "רק הצד השמאלי", 3: "בלי תכנון", 0: "חצי מה-V"}))

recap = Scene("recap", "סיכום", [
    P("לסיכום: דרישות מול קבלה, עיצוב המערכת מול מערכת ושילוב, ועיצוב המודולים מול יחידה.", do=show("r-1")),
    P("את הסדר לא צריך לשנן: קראו אותו מהציור. כחול לתכנון, ירוק להרצה.", do=show("r-2")),
    P("ובמפל המים אין את הקווים המקווקווים. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage=V("vf").replace('class="h"', 'class=""'),
   panel=st.card("r-1", "rule", "🔑 כל שלב פיתוח ← בדיקה באותו גובה")
         + st.card("r-2", "rule", "🔑 🔵 תכנון · 🟢 הרצה: קוראים מהציור")
         + st.card("r-4", "trap", "⚠️ מפל המים: בלי הקווים המקווקווים"))

SCENES = [title, idea, pairs, order, water, exam, recap]
w.no_latin_and_isolate(SCENES)
VIDEO = Video("T02", "tst", "מודל V: מתכננים לאורך הדרך, מריצים בסוף", SCENES, bank={"21-B-Q5": 1})
