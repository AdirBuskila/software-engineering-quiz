# -*- coding: utf-8 -*-
"""U05 · תרשים רצף: קו חיים, סרגל הפעלה והודעות — video script (build: tools/video/vid.py U05).

Source: courses/uml/U05.js (lesson + goal: lifeline, activation bar, solid arrow, dashed arrow, X, reading direction).
Exam anchor: 22S-A-Q13 (the circled part of a sequence diagram: B active and A not), shown as the original figure with
a ring. No guided quiz uses it; its twins 19B-C-Q11 (same figure, same key) and 24B-B-Q21 are not used anywhere.
Notation is the course checker's (w_uml.CHK.SEQ_NOTATION) and the order of returns comes from CHK.missing_returns.
Avoided on purpose: the U05 quiz items (lifeline, activation-bar, dashed-arrow and X definitions are taught, not asked)
and their twins 24B-B-Q19 / 24S-A-Q15 / 25F0b-Q17 / 24B-B-Q17; 24B-A-Q16 (U05 quiz), 24B-A-Q18 (boss);
the lesson's user/Server/myDB "save data" example. My worked scenario is a shop with a stock service and a
temporary receipt.
Doubt noted for the report: 24B-B-Q21 (key "A active, B not") circles an empty area left of A's lifeline.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_uml as w

C = w.CHK
assert C.SEQ_NOTATION == {"message", "return", "activation", "destruction", "lifeline"}
CALLS = [("cu", "sh", "buy()"), ("sh", "st", "reserve()")]
assert C.missing_returns(CALLS) == [("st", "sh"), ("sh", "cu")]      # answered in reverse order: inner call first

# the "who is active now" checks: a participant is active at y iff an activation bar covers y
BARS = {"sh": (200, 560), "st": (250, 330), "rc": (470, 500)}
active = lambda y: sorted(k for k, (a, b) in BARS.items() if a <= y <= b)
assert active(290) == ["sh", "st"] and active(420) == ["sh"]

# exam 22S-A-Q13
Q = BANK["22S-A-Q13"]
assert Q["correctIndex"] == 3 and Q["options"][3] == "B פעיל ו-A לא פעיל" and Q["image"] == "images/exams/22S-A-Q13.png"
assert Q["options"][0] == "A פעיל ו-B לא פעיל"
OPTS = w.opts_of(Q)

# ---------------------------------------------------------------- diagram
D = w.Dia("sq", 1000, 610)
D.lifeline("cu", 110, 40, 600, "לקוח", kind="actor", hidden=True)
D.lifeline("sh", 420, 70, 600, "Shop", hidden=True)
D.lifeline("st", 700, 70, 600, "Stock", hidden=True)
D.lifeline("rc", 900, 368, 600, "Receipt", w=150, hidden=True)
D.act("ash", "sh", *BARS["sh"])
D.act("ast", "st", *BARS["st"])
D.act("arc", "rc", *BARS["rc"])
D.msg("m1", "cu", "sh", 200, "buy()", ob=12)
D.msg("m2", "sh", "st", 250, "reserve()", oa=12, ob=12)
D.msg("r2", "st", "sh", 330, "ok", ret=True, oa=12, ob=12)
D.msg("mc", "sh", "rc", 400, "«create»", oa=12, ob=75)
D.msg("m3", "sh", "rc", 470, "print()", oa=12, ob=12)
D.destroy("x", "rc", 540)
D.msg("r1", "sh", "cu", 560, "receipt", ret=True, oa=12, ob=0)
D.hline("now1", 40, 790, 290, "?")
D.hline("now2", 40, 790, 420, "?")
D.ring("rl", 385, 132, 70, 470, rx=30)
D.ring("rb", 400, 188, 40, 384, rx=14)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נלמד לקרוא תרשים רצף, רכיב אחרי רכיב."),
    P("קו חיים, סרגל הפעלה, חץ מלא, חץ מקווקו, והסימן איקס."),
    P("ובסוף נקרא קטע אמיתי מתרשים במבחן.", hold=0.4),
], stage='<div class="kicker">U05 · UML ומידול</div><h1>תרשים רצף: קו חיים, סרגל הפעלה והודעות</h1>'
         '<p>לקרוא תרשים רצף: מה מייצג קו חיים, סרגל הפעלה, חץ מלא, חץ מקווקו וסימן X, ובאיזה כיוון קוראים.</p>',
   layout="title")

build = Scene("build", "בונים תרשים רצף", [
    P("תרשים רצף מתאר **הודעות בין משתתפים לאורך זמן**. ניקח לקוח שקונה בחנות מקוונת.", do=show("sq")),
    P("בראש התרשים: המשתתפים. הלקוח הוא איש מקל, והחנות ושירות המלאי הם מלבנים.", do=show("sq-cu", "sq-sh", "sq-st")),
    P("מתחת לכל משתתף יורד קו מקווקו: **קו החיים**. הוא מייצג את המשתתף הזה לאורך הזמן.", do=show("sq-rl", "c1")),
    P("והזמן זורם **מלמעלה למטה**. מה שלמעלה קרה קודם.", do=hide("sq-rl") + show("c2"), hold=0.3),
    P("הלקוח שולח לחנות הודעה: קנייה. הודעה היא **חץ מלא**.", do=show("sq-m1")),
    P("החנות מתחילה לעבוד, ולכן מופיע אצלה מלבן צר: **סרגל הפעלה**.", do=show("sq-ash", "sq-rb")),
    P("הסרגל אומר: עכשיו החנות **עסוקה** בטיפול בקריאה של הלקוח. הוא נמשך עד שהיא עונה לו.", do=show("c3")),
    P("החנות שולחת לשירות המלאי הודעה: לשריין את המוצר. ועכשיו גם למלאי יש סרגל.", do=hide("sq-rb") + show("sq-m2", "sq-ast")),
    P("המלאי מסיים ועונה. תשובה היא **חץ מקווקו**, חזרה למי ששלח.", do=show("sq-r2", "c4"), hold=0.3),
], stage=D.svg(hidden=True),
   panel=st.card("c1", "rule", "🔑 קו חיים = <b>משתתף אחד</b> לאורך זמן")
         + st.card("c2", "plain", "⬇️ קוראים מלמעלה למטה")
         + st.card("c3", "rule", "🔑 סרגל הפעלה = המשתתף <b>עסוק בטיפול בקריאה</b>")
         + st.card("c4", "rule", "🔑 חץ מלא = הודעה · חץ מקווקו = תשובה"))

life = Scene("life", "עצם זמני ו-X", [
    P("עכשיו החנות יוצרת עצם זמני: קבלה. הוא נולד באמצע התרשים, ולכן הראש שלו נמוך יותר.",
      do=show("sq2-rc", "sq2-mc")),
    P("החנות מבקשת מהקבלה להדפיס את עצמה.", do=show("sq2-m3", "sq2-arc")),
    P("וכשהקבלה סיימה, היא נהרסת. הסימן **איקס** בסוף קו החיים אומר: הריסה של העצם הזמני.", do=show("sq2-x", "c5")),
    P("ובסוף החנות עונה ללקוח, עם חץ מקווקו. שימו לב לסדר: קודם המלאי ענה לחנות, ורק אחר כך החנות ענתה ללקוח.",
      do=show("sq2-r1"), hold=0.3),
    P("התשובות חוזרות בסדר הפוך: הקריאה הפנימית נסגרת ראשונה.", do=show("c6")),
], stage=D.copy("sq2", shown=("cu", "sh", "st", "ash", "ast", "m1", "m2", "r2")),
   panel=st.card("c5", "rule", "🔑 <b>X</b> בסוף קו חיים = הריסה של עצם זמני")
         + st.card("c6", "ex", "תשובות בסדר הפוך: מלאי ← חנות, ואז חנות ← לקוח"))

who = Scene("who", "מי פעיל עכשיו?", [
    P("עכשיו תרגיל קריאה. נעצור בנקודת זמן אחת, ונשאל: מי פעיל ברגע הזה?", do=show("sq3-now1")),
    P("בקו הזה יש סרגל אצל החנות, וגם אצל המלאי. שניהם פעילים.", do=show("c7")),
    P("והלקוח? אין לו סרגל כאן: אף אחד לא קרא לו, ואין לו קריאה לטפל בה.", hold=0.3),
    P("נרד למטה. כאן המלאי כבר ענה, והסרגל שלו נגמר. נשארה פעילה רק החנות.", do=hide("sq3-now1") + show("sq3-now2", "c8")),
    P("הכלל פשוט: פעיל הוא מי שיש לו סרגל הפעלה בגובה הזה. מי שאין לו סרגל, לא פעיל.", do=show("c9")),
], stage=D.copy("sq3", reveal=True, keep=("now1", "now2", "rl", "rb")),
   panel=st.card("c7", "ex", "קו עליון: <b>Shop</b> ו-<b>Stock</b> פעילים")
         + st.card("c8", "ex", "קו תחתון: רק <b>Shop</b> פעיל")
         + st.card("c9", "rule", "🔑 פעיל = יש לו <b>סרגל הפעלה</b> באותו גובה"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: מה המשמעות של הסימון המוקף באדום בתרשים הרצף?"),
    P("בתוך העיגול: הודעה מאיי לבי, תשובה מבי לאיי, ומלבן צר על הקו של בי.", do=show("rs-ring-bar"),
      say="בתוך העיגול: הודעה מאֵיי לבִּי, תשובה מבִּי לאֵיי, ומלבן צר על הקו של בִּי."),
    P("המלבן הוא סרגל הפעלה, והוא נמצא אצל בי. לכן בי פעיל: הוא עסוק בקריאה שקיבל.", say="המלבן הוא סרגל הפעלה, והוא נמצא אצל בִּי. לכן בִּי פעיל: הוא עסוק בקריאה שקיבל."),
    P("ועל הקו של איי אין פס באותו קטע: אף אחד לא קרא לו. לכן איי לא פעיל.", do=show("rs-ring-a"),
      say="ועל הקו של אֵיי אין פס באותו קטע: אף אחד לא קרא לו. לכן אֵיי לא פעיל."),
    P("התשובה ההפוכה, שאיי פעיל ובי לא, הופכת את התפקידים.", do=show("q-x-0", "q-n-0"),
      say="התשובה ההפוכה, שאֵיי פעיל ובִּי לא, הופכת את התפקידים."),
    P("תוכן ההודעה לא משנה מי פעיל, ולכן ״תלוי איזה מידע התקבל״ נופלת.", do=show("q-x-1", "q-n-1")),
    P("והקטע כן מספיק: רואים בו את הסרגל, אז אפשר לדעת.", do=show("q-x-2", "q-n-2")),
    P("התשובה: בי פעיל, ואיי לא פעיל.", do=show("q-ok-3"), say="התשובה: בִּי פעיל, ואֵיי לא פעיל.", hold=0.3),
    P("המלכודת: לחשוב שמי ששלח את ההודעה הוא הפעיל. פעיל הוא מי שהסרגל אצלו.", do=show("x-t"), hold=0.5),
], stage=w.stack(st.raster("rs", "images/exams/22S-A-Q13.png", 410, (318, 438),
                           rings=[("bar", 222, 258, 46), ("a", 90, 258, 40)]),
                 st.card("x-t", "trap", "⚠️ פעיל = מי שיש לו <b>סרגל</b>, לא מי ששלח"), gap=14),
   panel=w.stem(Q["id"], "מה המשמעות של הסימון המוקף באדום בתרשים ה-sequence?")
         + st.options("q", OPTS, notes={0: "הפוך", 1: "לא תלוי בתוכן", 2: "הסרגל נראה"}))

recap = Scene("recap", "סיכום", [
    P("לסיכום: משתתפים למעלה, וקוראים מלמעלה למטה.", do=show("s-1")),
    P("קו חיים הוא משתתף אחד לאורך הזמן, וסרגל הפעלה אומר שהוא עסוק בטיפול בקריאה.", do=show("s-2")),
    P("חץ מלא הוא הודעה, חץ מקווקו הוא תשובה, ואיקס הוא הריסה של עצם זמני. נתראה ברמה הבאה.", do=show("s-3"), hold=0.6),
], stage=D.copy("sq4", reveal=True, keep=("now1", "now2", "rl", "rb")),
   panel=st.card("s-1", "rule", "🔑 מלמעלה למטה")
         + st.card("s-2", "rule", "🔑 קו חיים = משתתף · סרגל = עסוק בקריאה")
         + st.card("s-3", "rule", "🔑 מלא = הודעה · מקווקו = תשובה · X = הריסה"))

SCENES = [title, build, life, who, exam, recap]
w.no_latin(SCENES)
VIDEO = Video("U05", "uml", "תרשים רצף: קו חיים, סרגל הפעלה והודעות", SCENES, bank={"22S-A-Q13": 3})
