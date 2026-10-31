# -*- coding: utf-8 -*-
"""R06 · Scrum: Backlogs, ספרינט ושינויים באמצע — video script (build: tools/video/vid.py R06).

Source: courses/proc/R06.js (lesson + goal: Product Backlog vs Sprint Backlog, the sprint's goal, and what to do when a
new requirement arrives mid-sprint). Exam anchor: 26S-A-Q5 (the task "ProductService will be written as a Singleton"
in the Sprint Backlog -> a relevant Sprint Backlog task). No guided quiz uses it and it has no twin in the bank.
The sprint selection is computed below (story points in priority order, against the team's recent pace) and the
containment Sprint Backlog ⊂ Product Backlog is asserted on the very sets drawn; the mid-sprint outcome follows the
course checker's mid_sprint_action (re-stated) and ESTIMATION.
Policy: lesson rules are shown as outcomes, never read in the wording of a quiz/boss option. So containment is shown
(the sprint items highlighted inside the big list) instead of "the Product Backlog contains the Sprint Backlog"; the
estimate is shown as a card-vote round instead of "a discussion on User Story Points"; the sprint-goal line ("a
potentially complete increment") and "all the Sprint Backlog items are meant to be done" are not said; the mid-sprint
case is a different scenario (a librarian's report request, shown queued and picked at the next planning, with no
"PO puts it in the Product Backlog" sentence and no list of the quiz's distractors).
Avoided on purpose: the R06 quiz items (25F0a-Q7, 25S-A-Q7 and the three originals: containment, the day-5 request,
how to estimate) with their twins (25B-N-Q9, 26B-A-Q10, 26B-A-Q7, 24B-A-Q5), and the R09 boss item 26S-A-Q6 (a task
bigger than its estimate). Worked data are mine: a library app backlog and a monthly-loans report request.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_proc as w

# ---------------------------------------------------------------- facts (checked)
assert w.CHK["ESTIMATION"] == "story_points_discussion"
ITEMS = [("חיפוש ספר לפי שם", 8), ("השאלת ספר", 5), ("תזכורת להחזרה", 3), ("דירוג ספרים", 8),
         ("רשימת משאלות", 5), ("מצב לילה", 2), ("המלצות אישיות", 13)]
PAST = [17, 19, 18]
PACE = sum(PAST) / len(PAST)
assert PACE == 18
chosen, total = [], 0
for k, (_, pts) in enumerate(ITEMS):          # in priority order, while the next item still fits
    if total + pts > PACE:
        break
    chosen.append(k)
    total += pts
assert chosen == [0, 1, 2] and total == 16 and ITEMS[3][1] == 8 and total + ITEMS[3][1] == 24 > PACE
product, sprint = set(range(len(ITEMS))), set(chosen)
assert sprint < product                      # the Product Backlog contains the Sprint Backlog, not the other way


def mid_sprint_action(changes_sprint_goal):  # the course checker's rule (check.py R06)
    return "product_backlog_then_next_sprint" if changes_sprint_goal else "team_decides"
assert mid_sprint_action(True) == "product_backlog_then_next_sprint"

Q = BANK["26S-A-Q5"]
OK = w.opt_index(Q, "משימה רלוונטית")
MORE = w.opt_index(Q, "לפרט יותר")
OOP = w.opt_index(Q, "מונחה עצמים")
PRD = w.opt_index(Q, "PRD")
ALL = w.opt_index(Q, "כל התשובות")
assert Q["correctIndex"] == OK == 2 and sorted([OK, MORE, OOP, PRD, ALL]) == [0, 1, 2, 3, 4]
OPTS = w.opts_of(Q)
assert OPTS[-1][0] == ALL

BL = w.backlog("bl", [(t, p) for t, p in ITEMS], chosen, cap=f"קצב הצוות: כ-{PACE:.0f} נקודות לספרינט", size=24)
MID = w.board("md", [("pb", w.en("Product Backlog") + '<span class="pr-colsub">כל המוצר, לפי חשיבות</span>', "f"),
                     ("sb", "הספרינט הנוכחי 🔒", "ok"),
                     ("nb", "התכנון הבא", "nf")],
              [("req", "📊 דוח השאלות חודשי, בקשה של מנהלת הספרייה", "pb", "מקבל מקום בתור"),
               ("s1", "חיפוש ספר לפי שם", "sb", "", True), ("s2", "השאלת ספר", "sb", "", True),
               ("s3", "תזכורת להחזרה", "sb", "", True),
               ("nx", "📊 דוח השאלות חודשי", "nb", "", "h")], card_w=320, col_w=320, size=23)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נכיר את שתי הרשימות של Scrum: ה-Product Backlog וה-Sprint Backlog."),
    P("נראה איך בוחרים מה ייכנס לספרינט, ומה עושים כשמגיעה דרישה חדשה באמצע."),
    P("ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">R06 · תהליכים, Agile ודרישות</div><h1>Scrum: Backlogs, ספרינט ושינויים באמצע</h1>'
         '<p>מה ההבדל בין שתי הרשימות, איך משערכים, ומה עושים כשנכנסת דרישה חדשה באמצע ספרינט.</p>', layout="title")

lists = Scene("lists", "שתי רשימות", [
    P("ה-Product Backlog הוא רשימת **כל** מה שרוצים במוצר. כל שורה בה נקראת פריט.", do=show("l1")),
    P("ה-Product Owner מסדר אותה לפי עדיפות: הכי חשוב למעלה. הנה ה-Backlog של אפליקציה לספרייה."),
    P("ה-Sprint Backlog הוא **חלק** מהרשימה הזו: רק הפריטים שנבחרו לספרינט הנוכחי.", do=show("l2", "bl-s0", "bl-s1", "bl-s2")),
    P("הסתכלו על שלושת הפריטים ברשימת הספרינט: כל אחד מהם מופיע גם ברשימה הגדולה. שום דבר לא נוסף מבחוץ.",
      do=show("bl-ph0", "bl-ph1", "bl-ph2", "l3"), hold=0.4),
], stage=BL,
   panel=st.card("l1", "ex", "📚 " + w.en("Product Backlog") + ": <b>כל</b> הפריטים, לפי עדיפות")
         + st.card("l2", "ex", "🏃 " + w.en("Sprint Backlog") + ": מה שנבחר <b>לספרינט הזה</b>")
         + st.card("l3", "rule", "🔑 כל פריט של הספרינט בא <b>מתוך</b> הרשימה הגדולה"))

pick = Scene("pick", "מה נכנס לספרינט", [
    P("אז איך בוחרים? קודם נותנים לכל פריט מספר נקודות.", do=show("k1")),
    P("כל אחד בצוות מציג קלף עם הערכה. מי שהעריכו הכי גבוה והכי נמוך מסבירים למה, ומצביעים שוב, עד שמגיעים למספר אחד.",
      do=show("k1b")),
    P("נקודה כזו היא לא שעה. היא גודל **יחסי**: פריט של שמונה נקודות הוא בערך פי ארבעה מפריט של שתיים.", do=show("k2"),
      hold=0.2),
    P("בשלושת הספרינטים האחרונים הצוות השלים שבע עשרה, תשע עשרה ושמונה עשרה נקודות. בממוצע, שמונה עשרה.",
      do=show("k3")),
    P("עכשיו לוקחים מלמעלה, לפי העדיפות. חיפוש ספר, שמונה נקודות.", do=show("b2-ph0", "b2-s0")),
    P("השאלת ספר, עוד חמש. יחד שלוש עשרה.", do=show("b2-ph1", "b2-s1")),
    P("תזכורת להחזרה, עוד שלוש. יחד שש עשרה.", do=show("b2-ph2", "b2-s2")),
    P("הפריט הבא שווה שמונה נקודות. שש עשרה ועוד שמונה זה עשרים וארבע, יותר מהקצב של הצוות. לכן עוצרים כאן.",
      do=show("k4"), hold=0.4),
], stage=BL.replace('id="bl', 'id="b2').replace('"bl-', '"b2-'),
   panel=st.card("k1", "ex", "🎯 לכל פריט: מספר נקודות")
         + st.card("k1b", "plain", "🃏 קלפים, הסבר, הצבעה חוזרת ← מספר אחד")
         + st.card("k2", "rule", "🔑 נקודה = גודל <b>יחסי</b>, לא שעה")
         + st.card("k3", "ex", "קצב: <bdi dir=\"ltr\">(17 + 19 + 18) ÷ 3 = <b>18</b></bdi>")
         + st.card("k4", "plain", "<bdi dir=\"ltr\">8 + 5 + 3 = <b>16</b> ✓</bdi><br><bdi dir=\"ltr\">16 + 8 = 24 &gt; 18 ✗</bdi>"))

mid = Scene("mid", "בקשה באמצע", [
    P("ועכשיו הספרינט כבר רץ, והצוות עובד לקראת היעד שנקבע בתכנון.", do=show("m0")),
    P("באמצע, מנהלת הספרייה שולחת בקשה: דוח השאלות חודשי. זה פיצ׳ר חדש, שלא היה ביעד. נראה מה קורה לו."),
    P("הבקשה נרשמת כפריט חדש ברשימה הגדולה, ומקבלת מקום בתור, לפי החשיבות שלה.", do=hide("md-p-req") + show("md-c-req", "md-w-req")),
    P("והספרינט הנוכחי? ממשיך בדיוק כמו שתוכנן. שלושת הפריטים שלו לא זזים.", do=show("m1")),
    P("ובתכנון של הספרינט הבא, הצוות מסתכל שוב על הרשימה, והדוח נבחר.", do=show("md-c-nx"), hold=0.4),
], stage=w.stack(st.card("m0", "rule", "🔑 הספרינט רץ לקראת <b>יעד</b>"), MID, gap=22),
   panel=st.card("m1", "ex", "🔒 הספרינט הנוכחי: בלי שינוי"))

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו שאלה ממבחן. ב-Sprint Backlog מופיעה המשימה: ״המחלקה ProductService תיכתב בתבנית Singleton״. מה דעתכם?"),
    P("נשאל מה יש ב-Sprint Backlog. לא רק פריטים כלליים, אלא גם **המשימות הטכניות** שהצוות יבצע כדי לממש אותם.",
      do=show("x1")),
    P("ואיך לממש, בדיוק כאן מחליטים. איזו מחלקה, ובאיזו תבנית.", do=show("x2")),
    P("לכן זו משימה רלוונטית ל-Sprint Backlog.", do=show(f"q-ok-{OK}")),
    P("״לא טובה, צריך לפרט יותר איך ליישם את התבנית״? המשימה ברורה: מחלקה אחת, תבנית אחת. את הפרטים הצוות יודע לממש.",
      do=show(f"q-x-{MORE}", f"q-n-{MORE}")),
    P("״לא רלוונטית אם המערכת מונחית עצמים״? הפוך. Singleton היא תבנית של תכנות מונחה עצמים.",
      do=show(f"q-x-{OOP}", f"q-n-{OOP}")),
    P("״דרישה למסמך דרישות המוצר״? וזו המלכודת: מסמך דרישות מתאר **מה** המערכת עושה. החלטת מימוש לא נכנסת אליו.",
      do=show(f"q-x-{PRD}", f"q-n-{PRD}", "x3")),
    P("ומכיוון שיש תשובה נכונה, ״כל התשובות האחרות שגויות״ נופלת.", do=show(f"q-x-{ALL}"), hold=0.5),
], stage=w.stack(st.card("x1", "rule", "🔑 " + w.en("Sprint Backlog") + " = הפריטים + <b>המשימות הטכניות</b> למימושם"),
                 st.card("x2", "ex", "🛠️ ״איך לממש״ ← מקומו כאן, אצל הצוות"),
                 st.card("x3", "trap", "⚠️ מסמך דרישות = <b>מה</b>. החלטת מימוש = <b>איך</b>, לא שם"), gap=26),
   panel=w.qpanel(w.stem(Q["id"], "המשימה ״המחלקה " + w.en("ProductService") + " תכתב בתבנית תיכון " + w.en("singleton")
                         + "״ כחלק מה-" + w.en("Sprint Backlog") + " הינה:"),
                  st.options("q", OPTS, notes={MORE: "ברורה מספיק", OOP: "תבנית של OOP", PRD: "זה ״איך״"})))

recap = Scene("recap", "סיכום", [
    P("לסיכום: ה-Product Backlog הוא כל מה שרוצים במוצר, לפי עדיפות. ה-Sprint Backlog הוא החלק שנבחר לספרינט.",
      do=show("s1")),
    P("נותנים לכל פריט נקודות, ובוחרים מלמעלה לפי הקצב של הצוות.", do=show("s2")),
    P("בקשה חדשה באמצע? מחכה בתור, והספרינט ממשיך. והחלטות מימוש? משימות ב-Sprint Backlog. נתראה ברמה הבאה.",
      do=show("s3"), hold=0.6),
], stage=BL.replace('id="bl', 'id="b3').replace('"bl-', '"b3-').replace('class="pr-pbi s h"', 'class="pr-pbi s"'),
   panel=st.card("s1", "rule", "🔑 הספרינט בוחר <b>מתוך</b> הרשימה הגדולה")
         + st.card("s2", "rule", "🔑 נקודות + קצב הצוות ← מה נכנס")
         + st.card("s3", "rule", "🔑 בקשה באמצע: בתור, והספרינט ממשיך"))

SCENES = [title, lists, pick, mid, exam, recap]
w.no_latin(SCENES)
VIDEO = Video("R06", "proc", "Scrum: Backlogs, ספרינט ושינויים באמצע", SCENES, bank={"26S-A-Q5": OK})
