# -*- coding: utf-8 -*-
"""R04 · Scrum: Product Owner, Scrum Master והצוות — video script (build: tools/video/vid.py R04).

Source: courses/proc/R04.js (lesson + goal: what the Product Owner does, what the Scrum Master does, and who owns each
task in a description). Exam anchor: 24B-B-Q4 ("what is part of the Scrum Master's role?" -> all the other answers are
wrong: managing the team, guarding the budget, the product vision and assigning tasks are not his). No guided quiz uses
it and it has no twin in the bank.
Every card on the sorting board is checked against the course checker's OWNER / SM_TASKS / SCRUM_ROLES tables
(w_proc.CHK); the team's own tasks are checked to be outside SM_TASKS.
Policy: the Product Owner is described as "responsible for what is built, where the product goes, its list and what
tops it", never in the wording of 24B-A-Q4 ("define the product vision and manage the Backlog") or 19B-C-Q5 ("final
priorities from the product backlog"). The Scrum Master's blocker card is an outside-meetings case, not a developer
stuck on another team (R04-Q2's structure).
Avoided on purpose: the R04 quiz items (24B-B-Q1 team size, 19B-C-Q5, the sales-vs-operations dispute, the missing test
environment, "which is the PO's and not the SM's") and their twins (26CL-Q6, 26B-A-Q9, 26S-A-Q9), and the R09 boss item
24B-A-Q4 is never shown. The team size is not stated. Worked tasks are mine: export vs notifications, outside meetings
eating an hour a day, the year's direction for management, keeping the daily short, splitting an item, code and tests.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_proc as w

# ---------------------------------------------------------------- facts (checked)
O = w.CHK["OWNER"]
SMT = w.CHK["SM_TASKS"]
ROLES = w.CHK["SCRUM_ROLES"]
PO, SM, TEAM = "Product Owner", "Scrum Master", "Team"
assert ROLES == {PO, SM, TEAM}
for fake in ("Team Leader", "Project Manager", "DevOps Owner", "Scrum Owner", "Product Master"):
    assert fake not in ROLES

# the board: (key, text, owner, checker fact behind it)
CARDS = [
    ("k1", "להחליט אם ייצוא ל-PDF קודם להתראות", PO, O["set_priorities"]),
    ("k2", "מנהלים מבחוץ קובעים לצוות פגישות, ושעה ביום הולכת לאיבוד", SM, O["remove_impediments"]),
    ("k3", "להציג להנהלה לאן האפליקציה תתפתח השנה", PO, O["product_vision"]),
    ("k4", "לדאוג שהצוות מקיים את התהליך, וה-Daily נשאר קצר", SM, SM if "ensure_scrum_followed" in SMT else None),
    ("k5", "לפרק פריט למשימות ולבחור מי עושה מה", TEAM, TEAM if "assign_tasks" not in SMT else None),
    ("k6", "לכתוב את הקוד ולבדוק אותו", TEAM, TEAM if "write_code" not in SMT else None),
]
for _, _, who, fact in CARDS:
    assert who == fact, (who, fact)
assert O["manage_scrum_process"] == SM and "manage_scrum_process" in SMT and "product_vision" not in SMT

Q = BANK["24B-B-Q4"]
OK = w.opt_index(Q, "כל התשובות")
TEAMM = w.opt_index(Q, "לנהל את צוות")
BUD = w.opt_index(Q, "תקציב")
VIS = w.opt_index(Q, "חזון המוצר")
ASG = w.opt_index(Q, "להקצות משימות")
assert Q["correctIndex"] == OK == 2 and sorted([OK, TEAMM, BUD, VIS, ASG]) == [0, 1, 2, 3, 4]
assert "product_vision" not in SMT and O["product_vision"] == PO
OPTS = w.opts_of(Q)

COLS = [("po", w.en("Product Owner") + '<span class="pr-colsub">מה, ובאיזה סדר</span>', "f"),
        ("sm", w.en("Scrum Master") + '<span class="pr-colsub">התהליך, ומה חוסם</span>', "nf"),
        ("team", 'הצוות<span class="pr-colsub">מבצע את העבודה</span>', "ok")]
KEY = {PO: "po", SM: "sm", TEAM: "team"}
BOARD = w.board("b", COLS, [(k, w.ltr_runs(t), KEY[o], "") for k, t, o, _ in CARDS],
                card_w=500, col_w=330, size=24)


def move(k):
    return hide(f"b-p-{k}") + show(f"b-c-{k}")


ROLES_T = w.table("r", ["תפקיד", "אחריות"], [
    [w.en("Product Owner"), "אחראי על <b>מה</b> בונים: לאן המוצר הולך, הרשימה שלו, ומה בראשה"],
    [w.en("Scrum Master"), "<b>מנהל את תהליך ה-" + w.en("Scrum") + "</b>, ו<b>מסיר חסמים</b> של הצוות"],
    ["הצוות", "מבצע את העבודה. רב-תחומי, ומארגן את עצמו"],
], widths=[260, 700], size=28)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נכיר את התפקידים ב-Scrum: ה-Product Owner, ה-Scrum Master, והצוות."),
    P("נלמד כלל אחד שמשייך כל משימה לבעל התפקיד הנכון."),
    P("ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">R04 · תהליכים, Agile ודרישות</div><h1>Scrum: Product Owner, Scrum Master והצוות</h1>'
         '<p>מה עושה כל בעל תפקיד, ואיך משייכים משימה מתיאור לבעל התפקיד הנכון.</p>', layout="title")

roles = Scene("roles", "התפקידים", [
    P("Scrum היא מסגרת לניהול פיתוח אג׳ילי. יש בה שני תפקידים מרכזיים, ולצידם צוות הפיתוח."),
    P("ה-Product Owner אחראי על **מה** בונים. הוא יודע לאן המוצר הולך, ומחזיק את הרשימה של כל מה שרוצים בו.",
      do=show("r-r0")),
    P("וכשיש ויכוח מה לבנות קודם, הוא זה שמחליט מה עולה לראש הרשימה.", do=show("r-m0")),
    P("ה-Scrum Master אחראי על **התהליך**. הוא דואג שהצוות מבין ומקיים את Scrum.", do=hide("r-m0") + show("r-r1")),
    P("ואם משהו חוסם את הצוות, הוא עוזר **להסיר את החסם**.", do=show("r-m1")),
    P("והצוות? הוא מבצע את העבודה. יש בו את כל המקצועות הדרושים, והוא מחליט בעצמו מי עושה מה.",
      do=hide("r-m1") + show("r-r2"), hold=0.3),
    P("ומכאן הכלל: ״מה״ ו״באיזה סדר״, זה ה-Product Owner. ״איך התהליך עובד״ ו״מה חוסם״, זה ה-Scrum Master.",
      do=show("r-k"), hold=0.4),
], stage=w.stack(ROLES_T, gap=20),
   panel=st.card("r-k", "rule", "🔑 <b>מה ובאיזה סדר</b> ← " + w.en("Product Owner")
                 + "<br><b>התהליך ומה חוסם</b> ← " + w.en("Scrum Master")))

sort = Scene("sort", "מי עושה מה", [
    P("נתרגל. לפניכם שש משימות מפרויקט אחד. נשייך כל אחת לבעל התפקיד שלה.", do=show("b")),
    P("להחליט אם ייצוא לקובץ קודם להתראות. זו שאלה של סדר עדיפויות, ולכן ה-Product Owner.", do=move("k1")),
    P("מנהלים מחוץ לצוות קובעים לו פגישות, ושעה ביום הולכת לאיבוד. משהו מפריע לצוות לעבוד, ולכן ה-Scrum Master מטפל בזה.", do=move("k2")),
    P("להציג להנהלה לאן האפליקציה תתפתח השנה. זו התמונה הגדולה של המוצר, ולכן ה-Product Owner.", do=move("k3")),
    P("לדאוג שהצוות מקיים את התהליך, ושהפגישה היומית נשארת קצרה. זה התהליך, ולכן ה-Scrum Master.", do=move("k4")),
    P("לפרק פריט למשימות, ולבחור מי עושה מה. את זה עושה **הצוות** בעצמו. אף אחד לא מחלק לו משימות.", do=move("k5")),
    P("ולכתוב את הקוד ולבדוק אותו: ברור, הצוות.", do=move("k6"), hold=0.4),
], stage=BOARD, layout="full")

trap = Scene("trap", "המלכודות", [
    P("שתי מלכודות חוזרות במבחנים. הראשונה: ה-Scrum Master **אינו** מנהל פרויקט קלאסי.", do=show("t1")),
    P("הוא לא מקצה משימות, לא שומר על התקציב, ולא מגדיר את חזון המוצר. הוא משרת את הצוות ואת התהליך.", do=show("t1x")),
    P("השנייה: שמות התפקידים מדויקים. ב-Scrum אין Team Leader, אין מנהל פרויקט, ואין תפקיד בשם ״אחראי תשתיות״.",
      do=show("t2")),
    P("ומסיחים אוהבים לערבב שמות. ״סקראם אונר״ או ״פרודקט מאסטר״ לא קיימים.", do=show("t2x"),
      say="ומסיחים אוהבים לערבב שמות. סְקְרָאם אוֹנֶר, או פְּרוֹדַקְט מַאסְטֶר, לא קיימים.", hold=0.4),
], stage=w.stack(st.card("t1", "trap", "⚠️ " + w.en("Scrum Master") + " ≠ מנהל פרויקט"),
                 st.card("t1x", "ex", "לא מקצה משימות · לא שומר על תקציב · לא מגדיר חזון"),
                 st.card("t2", "trap", "⚠️ אין ב-" + w.en("Scrum") + ": " + w.en("Team Leader") + ", " + w.en("Project Manager")
                         + ", " + w.en("DevOps Owner")),
                 st.card("t2x", "ex", w.en("Scrum Owner") + "? " + w.en("Product Master") + "? שמות מעורבבים, לא תפקידים"),
                 gap=24), layout="full")

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו שאלה ממבחן: מה מהבאים נכלל בתפקידו של ה-Scrum Master?"),
    P("נעבור על כל אפשרות, ונבדוק אותה מול הכלל."),
    P("לנהל את צוות ה-Scrum? זה נשמע קרוב, אבל לא. הצוות מארגן את עצמו. ה-Scrum Master מנהל את **התהליך**, לא את האנשים.",
      do=show(f"q-x-{TEAMM}", f"q-n-{TEAMM}")),
    P("לדאוג שמשימות הספרינט לא חורגות מהתקציב? זה תפקיד של מנהל פרויקט קלאסי, ולא שלו.", do=show(f"q-x-{BUD}", f"q-n-{BUD}")),
    P("להגדיר לאן המוצר הולך? זו שאלה של **מה** בונים, ולכן זה תחום של ה-Product Owner, לא שלו.", do=show(f"q-x-{VIS}", f"q-n-{VIS}")),
    P("להקצות משימות לצוות? לא. הצוות בוחר בעצמו מי עושה מה.", do=show(f"q-x-{ASG}", f"q-n-{ASG}")),
    P("אף אחת מהארבע לא נכונה. ולכן התשובה: כל התשובות האחרות שגויות.", do=show(f"q-ok-{OK}")),
    P("והמלכודת כאן היא המילה ״לנהל״. ה-Scrum Master מנהל תהליך, ומסיר חסמים. הוא לא הבוס של הצוות.",
      do=show("x1"), hold=0.5),
], stage=w.stack(st.card("x0", "rule", "🔑 " + w.en("Scrum Master") + ": מנהל את <b>תהליך</b> ה-" + w.en("Scrum") + " ומסיר חסמים"),
                 st.card("x1", "trap", "⚠️ ״לנהל את הצוות״ ≠ ״לנהל את התהליך״"), gap=26).replace('id="x0" class="card rule h"', 'id="x0" class="card rule"'),
   panel=w.qpanel(w.stem(Q["id"], w.ltr_runs(Q["question"])),
                  st.options("q", OPTS, notes={TEAMM: "הצוות מתארגן לבד", BUD: "מנהל פרויקט", VIS: w.en("PO"),
                                               ASG: "הצוות בוחר"})))

recap = Scene("recap", "סיכום", [
    P("לסיכום: ה-Product Owner אחראי על מה בונים, ומה קודם.", do=show("s1")),
    P("ה-Scrum Master מנהל את התהליך, ומסיר חסמים.", do=show("s2")),
    P("הצוות מבצע, ומחלק את העבודה בעצמו.", do=show("s3")),
    P("ואין ב-Scrum מנהל פרויקט או Team Leader. נתראה ברמה הבאה.", do=show("s4"), hold=0.6),
], stage=w.stack(ROLES_T.replace('id="r', 'id="z').replace(' class="h"', ''), gap=20),
   panel=st.card("s1", "rule", "🔑 " + w.en("PO") + ": מה בונים, ומה קודם")
         + st.card("s2", "rule", "🔑 " + w.en("SM") + ": תהליך, הסרת חסמים")
         + st.card("s3", "rule", "🔑 הצוות: מבצע ומתארגן לבד")
         + st.card("s4", "trap", "⚠️ אין מנהל פרויקט ואין " + w.en("Team Leader")))

SCENES = [title, roles, sort, trap, exam, recap]
w.no_latin(SCENES)
VIDEO = Video("R04", "proc", "Scrum: Product Owner, Scrum Master והצוות", SCENES, bank={"24B-B-Q4": OK})
