# -*- coding: utf-8 -*-
"""R07 · דרישות: פונקציונליות ולא פונקציונליות — video script (build: tools/video/vid.py R07).

Source: courses/proc/R07.js (lesson + goal: classify each requirement as functional, what the system does, or
non-functional, quality and constraint, also when the wording misleads). Exam anchors: 19B-B-Q12 (which is NOT
non-functional -> talking to a credit-card clearing system) and SP-AMR-Q10 (a logo at the top of every screen ->
functional). No guided quiz uses them and neither has a twin in the bank.
Every requirement on screen is classified by the course checker's rule classify(is_action, is_quality_or_constraint)
(w_proc.classify, asserted against the checker's REQ table), from attributes stated next to it.
Avoided on purpose: the R07 quiz items (22S-A-Q3 and its twin 23B-A-Q2, 25B-N-Q4, and the three originals: the SMS
reminder with the 3-second report, AES passwords vs search / e-mail / cancel, the 2-second home page) and their twins
(26CL-Q4, 25F0a-Q3), and the R09 boss item 26S-A-Q4 with its near twin 26B-A-Q5. Worked requirements are mine: a food
delivery app (live courier map, invalid-address message, iOS version, 2-second delivery estimate, accessibility law,
"sold out" dishes, 99.5% availability).
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_proc as w

F, NF = "functional", "non-functional"
# ---------------------------------------------------------------- facts (checked)
REQS = [  # (key, text, is_action, is_quality_or_constraint, column)
    ("r1", "הלקוח יוכל לעקוב אחרי השליח על מפה", True, False, "f"),
    ("r2", "האפליקציה תעבוד על iOS 16 ומעלה", False, True, "nf"),
    ("r3", "כתובת לא תקינה ← הודעת שגיאה מתחת לשדה", True, False, "f"),
    ("r4", "חישוב זמן המשלוח ייקח עד 2 שניות", True, True, "nf"),
    ("r5", "המסעדה תוכל לסמן מנה כ״אזלה״", True, False, "f"),
    ("r6", "המערכת תעמוד בחוק הנגישות", False, True, "nf"),
    ("r7", "המערכת תהיה זמינה 99.5% מהזמן", False, True, "nf"),
]
for k, _, act, q, col in REQS:
    assert w.classify(act, q) == (F if col == "f" else NF), k
WHY = {"r1": "פעולה", "r2": "פלטפורמה", "r3": "תגובה לקלט לא תקין", "r4": "ביצועים: יש מספר",
       "r5": "פעולה", "r6": "רגולציה", "r7": "זמינות"}

Q = BANK["19B-B-Q12"]
OK = w.opt_index(Q, "סליקת כרטיסי אשראי")
JAVA = w.opt_index(Q, "JAVA")
TIME = w.opt_index(Q, "זמן התגובה")
MEM = w.opt_index(Q, "30MB")
assert Q["correctIndex"] == OK == 0 and sorted([OK, JAVA, TIME, MEM]) == [0, 1, 2, 3]
EXAM = {OK: (True, False), JAVA: (False, True), TIME: (True, True), MEM: (False, True)}
assert [k for k, a in EXAM.items() if w.classify(*a) != NF] == [OK]     # the only one that is NOT non-functional
OPTS = w.opts_of(Q, short={TIME: "זמן התגובה המקסימלי של כל שאילתה לא יעלה על חצי שנייה"})

Q2 = BANK["SP-AMR-Q10"]
OK2 = w.opt_index(Q2, "דרישה פונקציונלית")
NF2 = w.opt_index(Q2, "לא פונקציונלית")
NOT2 = w.opt_index(Q2, "איננו דרישה")
ILL2 = w.opt_index(Q2, "לא חוקית")
assert Q2["correctIndex"] == OK2 == 2 and sorted([OK2, NF2, NOT2, ILL2]) == [0, 1, 2, 3]
assert w.classify(True, False) == F           # showing the logo on every screen: behaviour, no quality bar
OPTS2 = w.opts_of(Q2)

BOARD = w.board("b", [("f", 'פונקציונלית<span class="pr-colsub">מה המערכת עושה</span>', "f"),
                      ("nf", 'לא פונקציונלית<span class="pr-colsub">כמה טוב, ובאילו תנאים</span>', "nf")],
                [(k, w.ltr_runs(t), col, WHY[k]) for k, t, _, _, col in REQS], card_w=470, col_w=470, size=23)


def move(k):
    return hide(f"b-p-{k}") + show(f"b-c-{k}", f"b-w-{k}")


DEF = w.table("d", ["סוג", "על מה זה", "סימנים"], [
    ["פונקציונלית", "<b>מה</b> המערכת עושה: שירות, קלט ופלט, תגובה לקלט", "פעולה של משתמש או של המערכת"],
    ["לא פונקציונלית", "<b>כמה טוב</b> ובאילו תנאים: ביצועים, אבטחה, פלטפורמה, זמינות, רגולציה",
     "מספר, אחוז, מגבלה, שם של טכנולוגיה"],
], widths=[210, 450, 320], size=27)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נלמד לסווג דרישות: פונקציונליות, ולא פונקציונליות."),
    P("נכיר שאלה אחת שמכריעה, ונתרגל אותה גם כשהניסוח מנסה לבלבל."),
    P("ובסוף נפתור שתי שאלות אמיתיות ממבחנים.", hold=0.4),
], stage='<div class="kicker">R07 · תהליכים, Agile ודרישות</div><h1>דרישות: פונקציונליות ולא פונקציונליות</h1>'
         '<p>מה המערכת עושה, מול כמה טוב ובאילו תנאים.</p>', layout="title")

defs = Scene("defs", "שני סוגים", [
    P("דרישה מתארת **מה** המערכת צריכה לעשות, ואת **האילוצים** על הפעולה שלה."),
    P("דרישה **פונקציונלית** מתארת שירות או התנהגות: מה המערכת עושה, מה הקלט, מה הפלט, ואיך היא מגיבה לקלט.",
      do=show("d-r0")),
    P("דרישה **לא פונקציונלית** מתארת איכות או אילוץ: ביצועים, אבטחה, פלטפורמה, זמינות, או רגולציה.", do=show("d-r1")),
    P("והשאלה שמכריעה: האם הדרישה מתארת **פעולה**? או שהיא מתארת **כמה טוב**, ובאילו תנאים?", do=show("k1")),
    P("ורמז שעוזר: מספר, אחוז, מגבלה, או שם של טכנולוגיה, כמעט תמיד מסמנים דרישה לא פונקציונלית.", do=show("k2"),
      hold=0.4),
], stage=DEF,
   panel=st.card("k1", "rule", "🔑 <b>פעולה</b>? פונקציונלית<br><b>כמה טוב / באילו תנאים</b>? לא פונקציונלית")
         + st.card("k2", "ex", "🔢 מספר · אחוז · מגבלה · טכנולוגיה ← כמעט תמיד לא פונקציונלית"))

sort = Scene("sort", "ממיינים", [
    P("נמיין שבע דרישות של אפליקציית משלוחי אוכל.", do=show("b")),
    P("הלקוח יוכל לעקוב אחרי השליח על מפה. זו פעולה שהמערכת נותנת. פונקציונלית.", do=move("r1")),
    P("האפליקציה תעבוד על גרסה שש עשרה של מערכת ההפעלה של אייפון ומעלה. זו פלטפורמה, אילוץ. לא פונקציונלית.",
      do=move("r2")),
    P("כתובת לא תקינה תציג הודעת שגיאה. גם תגובה לקלט **לא** תקין היא התנהגות. פונקציונלית.", do=move("r3")),
    P("חישוב זמן המשלוח ייקח עד שתי שניות. יש כאן פעולה, אבל הדרישה היא על **המהירות** שלה. לא פונקציונלית.",
      do=move("r4")),
    P("המסעדה תוכל לסמן מנה שאזלה. פעולה. פונקציונלית.", do=move("r5")),
    P("המערכת תעמוד בחוק הנגישות. דרישות של רגולציה הן בדרך כלל לא פונקציונליות.", do=move("r6")),
    P("וזמינות של תשעים ותשעה וחצי אחוז. איכות, עם מספר. לא פונקציונלית.", do=move("r7"), hold=0.4),
], stage=BOARD, layout="full")

trap = Scene("trap", "ניסוח מטעה", [
    P("שימו לב לדרישה הרביעית. היא מזכירה פעולה, חישוב זמן משלוח, ובכל זאת היא לא פונקציונלית.", do=show("t1")),
    P("כי היא לא מבקשת שיהיה חישוב, החישוב כבר קיים. היא מבקשת שהוא יהיה **מהיר**. זו דרישת ביצועים.", do=show("t1x")),
    P("והמלכודת ההפוכה: דרישה על משהו שרואים במסך, נשמעת כמו ״עיצוב״ או ״איכות״.", do=show("t2")),
    P("אבל אם היא אומרת מה המערכת **מציגה** או **עושה**, בלי רף של איכות, היא פונקציונלית.", do=show("t2x"), hold=0.4),
], stage=w.stack(st.card("t1", "trap", "⚠️ ״החישוב ייקח עד 2 שניות״: מזכיר פעולה, אבל דורש <b>מהירות</b>"),
                 st.card("t1x", "ex", "← לא פונקציונלית (ביצועים)"),
                 st.card("t2", "trap", "⚠️ דרישה על משהו שמוצג במסך ≠ אוטומטית ״איכות״"),
                 st.card("t2x", "ex", "מה המערכת <b>מציגה או עושה</b>, בלי רף איכות ← פונקציונלית"), gap=24),
   layout="full")

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו שאלה ממבחן. שימו לב למילה ״איננו״: איזו מהדרישות **אינה** לא פונקציונלית?"),
    P("הופכים את השאלה בראש: מחפשים את הדרישה היחידה שהיא כן פונקציונלית.", do=show("x0")),
    P("לתקשר עם מערכת סליקה של כרטיסי אשראי, כדי לבצע חיובים. זו פעולה שהמערכת עושה. פונקציונלית.",
      do=show(f"q-ok-{OK}")),
    P("להיכתב בשפה מסוימת, כדי להתאים לשאר המערכות של הלקוח. זה אילוץ טכנולוגי. לא פונקציונלית.",
      do=show(f"q-x-{JAVA}", f"q-n-{JAVA}")),
    P("זמן תגובה של עד חצי שנייה לשאילתה: ביצועים. לא פונקציונלית.", do=show(f"q-x-{TIME}", f"q-n-{TIME}")),
    P("וצריכת משאבים מוגבלת לשלושים מגה: מגבלה, עם מספר. לא פונקציונלית.", do=show(f"q-x-{MEM}", f"q-n-{MEM}"),
      hold=0.5),
], stage=w.stack(st.card("x0", "rule", "🔑 ״איזו <b>איננה</b> לא פונקציונלית?״ = איזו <b>פונקציונלית</b>?"),
                 st.card("x0b", "trap", "⚠️ קודם הופכים את השלילה, ורק אז קוראים את התשובות").replace(' h"', '"'),
                 gap=26),
   panel=w.qpanel(w.stem(Q["id"], "אילו מהבאים איננו ״דרישה לא פונקציונלית״?"),
                  st.options("q", OPTS, notes={JAVA: "טכנולוגיה", TIME: "ביצועים", MEM: "מגבלה"})))

exam2 = Scene("exam2", "ועוד אחת", [
    P("ועוד שאלה קצרה: דרישה שבכל מסך יופיע, בחלק העליון, הלוגו של החברה. מה היא?"),
    P("נפעיל את השאלה המכריעה. האם יש כאן רף של איכות? מספר, מהירות, מגבלה? לא.", do=show("y1")),
    P("הדרישה אומרת מה המערכת **מציגה**. זו התנהגות, ולכן דרישה פונקציונלית.", do=show(f"p-ok-{OK2}")),
    P("״לא פונקציונלית״ היא המלכודת: לוגו נשמע כמו עיצוב. אבל אין כאן ״כמה טוב״, רק ״מה מוצג״.",
      do=show(f"p-x-{NF2}", f"p-n-{NF2}")),
    P("והיא כן דרישה, וגם חוקית לגמרי. את שתי האפשרויות האחרות פוסלים מיד.",
      do=show(f"p-x-{NOT2}", f"p-x-{ILL2}"), hold=0.5),
], stage=w.stack(st.card("y1", "ex", "🖼️ אין מספר, אין רף איכות ← מה <b>מוצג</b> = התנהגות"), gap=26),
   panel=w.qpanel(w.stem(Q2["id"], Q2["question"]),
                  st.options("p", OPTS2, notes={NF2: "אין ״כמה טוב״"})))

recap = Scene("recap", "סיכום", [
    P("לסיכום: פונקציונלית מתארת מה המערכת עושה. גם תגובה לקלט לא תקין.", do=show("s1")),
    P("לא פונקציונלית מתארת כמה טוב ובאילו תנאים: ביצועים, אבטחה, פלטפורמה, זמינות ורגולציה.", do=show("s2")),
    P("פעולה עם רף מהירות היא לא פונקציונלית. ו״מה מוצג״, בלי רף, היא פונקציונלית. נתראה ברמה הבאה.",
      do=show("s3"), hold=0.6),
], stage=DEF.replace('id="d', 'id="zd').replace(' class="h"', ''),
   panel=st.card("s1", "rule", "🔑 פונקציונלית: <b>מה</b> עושים")
         + st.card("s2", "rule", "🔑 לא פונקציונלית: <b>כמה טוב</b>, באילו תנאים")
         + st.card("s3", "trap", "⚠️ שואלים מה הדרישה <b>דורשת</b>, לא על מה היא מדברת"))

SCENES = [title, defs, sort, trap, exam, exam2, recap]
w.no_latin(SCENES)
VIDEO = Video("R07", "proc", "דרישות: פונקציונליות ולא פונקציונליות", SCENES, bank={"19B-B-Q12": OK, "SP-AMR-Q10": OK2})
