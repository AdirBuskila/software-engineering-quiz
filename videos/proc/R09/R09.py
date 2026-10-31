# -*- coding: utf-8 -*-
"""R09 · מבחן גמר: תהליכים, Agile ודרישות — boss walkthrough (build: tools/video/vid.py R09).

Source: courses/proc/R09.js (the course in one table, and the solving routine: name the topic, find its row, only then
filter the answers). Three exam questions, none of them a guided-quiz or boss item and none a twin of one:
  25S-A-Q4  how work progresses in an Agile project -> small iterations with frequent feedback loops
  25B-N-Q6  which is part of Agile -> planning the test phases alongside the project's progress
  19B-B-Q9  "the UI allows a short training, at most two hours" -> a good non-functional requirement
(25S-A-Q4's twin 25B-N-Q7 is not a quiz item either.) Per the review: the table names "Waterfall or Plan Driven", says "a new
requirement that changes the sprint goal", and mentions the under-estimated task (adjust the remaining work) as a
lesson rule only; that boss question (26S-A-Q6) is not shown. Checked with the course checker's tables: SUITS / FACTS for the
Agile vs Waterfall traits, classify() and good_requirement() for the requirement.
Avoided on purpose: the six R09 boss items (26S-A-Q8, 24B-A-Q4, 24B-A-Q2, 26S-A-Q6, 26S-A-Q4, 23S-A-Q4) and every
quiz item of R01..R08, with their twins (24S-A-Q2, 26B-A-Q5, 23B-A-Q11, 26B-A-Q6, 25B-N-Q3).
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_proc as w

# ---------------------------------------------------------------- facts (checked)
F = w.CHK["FACTS"]
assert F["agile_flexible"] and not F["waterfall_easy_to_change"]
assert w.fits("Agile", {"changing_reqs"}) and w.fits("Waterfall", {"stable_reqs"})

Q1 = BANK["25S-A-Q4"]
A1 = w.opt_index(Q1, "איטרציות קטנות")
SCOPE1 = w.opt_index(Q1, "היקף הפרויקט קבוע")
SEQ1 = w.opt_index(Q1, "עוקבים לחלוטין")
END1 = w.opt_index(Q1, "רק בסוף הפרויקט")
ALL1 = w.opt_index(Q1, "כל התשובות")
assert Q1["correctIndex"] == A1 == 0 and sorted([A1, SCOPE1, SEQ1, END1, ALL1]) == [0, 1, 2, 3, 4]

Q2 = BANK["25B-N-Q6"]
A2 = w.opt_index(Q2, "במקביל")
DOC2 = w.opt_index(Q2, "תיעוד מקיף")
TEST2 = w.opt_index(Q2, "רק לאחר פיתוח")
PLAN2 = w.opt_index(Q2, "בלתי ניתנת לשינוי")
ALL2 = w.opt_index(Q2, "כל התשובות")
assert Q2["correctIndex"] == A2 == 2 and sorted([A2, DOC2, TEST2, PLAN2, ALL2]) == [0, 1, 2, 3, 4]

Q3 = BANK["19B-B-Q9"]
A3 = w.opt_index(Q3, "\"לא פונקציונלית\" טובה")
F3 = w.opt_index(Q3, "\"פונקציונלית\" טובה")
IMP3 = w.opt_index(Q3, "בלתי אפשרית")
CPX3 = w.opt_index(Q3, "מורכבת למימוש")
assert Q3["correctIndex"] == A3 == 1 and sorted([A3, F3, IMP3, CPX3]) == [0, 1, 2, 3]
# "the UI allows a short training (at most two hours)": a learnability bar, not an action; it has a number
assert w.classify(False, True) == "non-functional" and w.good_requirement(True, True)

TAB = w.table("t", ["הנושא", "מה זוכרים"], [
    ["בחירת מודל", "דרישות יציבות ובקרה ← " + w.en("Waterfall") + " או " + w.en("Plan Driven") + " · משתנות ← אג׳ייל · הוכחת יכולת ← " + w.en("Build and Fix")],
    ["תפקידים", w.en("PO") + ": מה בונים, ומה קודם · " + w.en("SM") + ": תהליך, חסמים"],
    ["פגישות", "תכנון: קדימה · יומית: היום · " + w.en("Review") + ": המוצר · " + w.en("Retro") + ": התהליך"],
    ["באמצע ספרינט", "דרישה שמשנה את היעד ← " + w.en("Product Backlog") + " ← הספרינט הבא · משימה גדולה מההערכה ← מתאימים את מה שנשאר"],
    ["דרישות", "פעולה ← פונקציונלית · איכות ואילוץ ← לא פונקציונלית · עמומה או ״איך״ ← גרועה"],
], widths=[200, 800], size=25)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("זה סרטון הסיום של הקורס: תהליכים, אג׳ייל ודרישות."),
    P("נעבור על הקורס כולו בטבלה אחת, ואז נפתור שלוש שאלות אמיתיות ממבחנים, מנושאים שונים."),
    P("ובכל אחת נראה איפה המלכודת.", hold=0.4),
], stage='<div class="kicker">R09 · מבחן גמר</div><h1>מבחן גמר: תהליכים, Agile ודרישות</h1>'
         '<p>הקורס בטבלה אחת, ושלוש שאלות אמיתיות ממבחנים, פתורות צעד אחר צעד.</p>', layout="title")

table = Scene("table", "הקורס בטבלה", [
    P("בחירת מודל: דרישות יציבות ובקרה, Waterfall או Plan Driven. דרישות משתנות, אג׳ייל. רק להוכיח רעיון, Build and Fix.",
      do=show("t-r0")),
    P("תפקידים: בעל המוצר אחראי על מה בונים ומה קודם. מנהל הסקראם אחראי על התהליך ועל החסמים.", do=show("t-r1")),
    P("פגישות: תכנון מסתכל קדימה, היומית על היום, הסקירה על המוצר, והרטרוספקטיבה על התהליך.", do=show("t-r2")),
    P("באמצע ספרינט: דרישה חדשה שמשנה את היעד הולכת לרשימת המוצר, ולספרינט הבא.", do=show("t-r3")),
    P("ומשימה שיצאה גדולה מההערכה? לא עוצרים את הספרינט, אלא מתאימים את העבודה שנשארה."),
    P("ודרישות: פעולה היא פונקציונלית. איכות ואילוץ, לא פונקציונלית. ועמומה, או ״איך״, היא גרועה.", do=show("t-r4")),
    P("והשיטה: מזהים את הנושא, מוצאים את השורה בטבלה, ורק אז קוראים את התשובות.", do=show("t-k"), hold=0.4),
], stage=TAB, layout="full")
table.stage = w.stack(TAB, st.card("t-k", "rule", "🔑 נושא ← שורה בטבלה ← רק אז התשובות"), gap=24)

q1 = Scene("q1", "שאלה 1", [
    P("שאלה ראשונה: איזו טענה מתארת הכי טוב את התקדמות העבודה בפרויקט אג׳ייל?"),
    P("הנושא: אג׳ייל מול Waterfall. אג׳ייל מצטבר ואיטרטיבי, ומטרתו להגיב לשינויים.", do=show("a1")),
    P("ולכן: העבודה מחולקת לאיטרציות קטנות, עם משוב תכוף.", do=show(f"a-ok-{A1}")),
    P("שלוש מהטענות האחרות מתארות דווקא את Waterfall. היקף קבוע שאי אפשר לשנות אחרי התכנון.",
      do=show(f"a-x-{SCOPE1}", f"a-n-{SCOPE1}")),
    P("שלבים עוקבים לחלוטין: דרישות, תכנון, יישום ובדיקה.", do=show(f"a-x-{SEQ1}", f"a-n-{SEQ1}")),
    P("ומוצר שעובד רק בסוף הפרויקט. באג׳ייל יש גרסה עובדת בסוף כל איטרציה.", do=show(f"a-x-{END1}", f"a-n-{END1}")),
    P("ויש תשובה נכונה, אז ״כל התשובות האחרות שגויות״ נופלת.", do=show(f"a-x-{ALL1}")),
    P("המלכודת: תשובות שנשמעות מסודרות ובטוחות. אבל ״קבוע״ ו״רק בסוף״ הם סימנים של מפל מים.", do=show("a2"), hold=0.5),
], stage=w.stack(st.card("a1", "rule", "🔑 אג׳ייל = איטרציות קטנות + משוב תכוף"),
                 st.card("a2", "trap", "⚠️ ״קבוע״, ״עוקבים לחלוטין״, ״רק בסוף״ ← " + w.en("Waterfall")), gap=26),
   panel=w.qpanel(w.stem(Q1["id"], Q1["question"]),
                  st.options("a", w.opts_of(Q1), notes={SCOPE1: w.en("Waterfall"), SEQ1: w.en("Waterfall"),
                                                        END1: w.en("Waterfall")})))

q2 = Scene("q2", "שאלה 2", [
    P("שאלה שנייה: אילו מהמאפיינים הבאים הם חלק ממתודולוגיות אג׳ייל?"),
    P("שוב הנושא הוא אג׳ייל. בכל איטרציה יוצאת גרסה **עובדת**, ולכן גם בודקים אותה באותה איטרציה.", do=show("b1")),
    P("כלומר, את הבדיקות מתכננים במקביל להתקדמות הפרויקט, ולא דוחים אותן לסוף.", do=show(f"b-ok-{A2}")),
    P("השלמת כל הבדיקות רק אחרי שכל התוכנה פותחה? זה מפל מים, עם שלב בדיקות אחד בסוף.",
      do=show(f"b-x-{TEST2}", f"b-n-{TEST2}")),
    P("תיעוד מקיף לפני כל קידוד? אג׳ייל מעדיף תוכנה עובדת על פני תיעוד מלא.", do=show(f"b-x-{DOC2}", f"b-n-{DOC2}")),
    P("ותוכנית קפדנית שאי אפשר לשנות? הפוך מהמטרה של אג׳ייל, להגיב לשינוי.", do=show(f"b-x-{PLAN2}", f"b-n-{PLAN2}")),
    P("ויש תשובה נכונה, אז ״כל התשובות האחרות שגויות״ נופלת.", do=show(f"b-x-{ALL2}"), hold=0.5),
], stage=w.stack(st.card("b1", "rule", "🔑 בכל איטרציה גרסה <b>עובדת</b> ← בודקים לאורך הדרך"),
                 st.card("b2", "trap", "⚠️ ״לפני כל קידוד״, ״רק אחרי הכל״, ״בלתי ניתנת לשינוי״ ← מפל מים").replace(' h"', '"'),
                 gap=26),
   panel=w.qpanel(w.stem(Q2["id"], Q2["question"]),
                  st.options("b", w.opts_of(Q2), notes={TEST2: "בדיקות בסוף", DOC2: "תיעוד קודם", PLAN2: "תוכנית נוקשה"})))

q3 = Scene("q3", "שאלה 3", [
    P("שאלה שלישית: דרישה שממשק המשתמש יאפשר הדרכה קצרה, לכל היותר שעתיים. מה היא?"),
    P("הנושא: דרישות. שתי שאלות. ראשונה, האם היא מתארת פעולה, או כמה טוב?", do=show("c1")),
    P("היא לא אומרת מה המערכת עושה. היא אומרת כמה **קל ללמוד** אותה. זו איכות, ולכן לא פונקציונלית.", do=show("c1x")),
    P("שנייה, האם היא טובה? יש בה מספר, שעתיים, ואפשר לבדוק אותו: מדריכים משתמש, ומודדים זמן.", do=show("c2")),
    P("בדיקתית, ואומרת ״מה״, לא ״איך״. לכן: דרישה לא פונקציונלית טובה.", do=show(f"c-ok-{A3}")),
    P("״פונקציונלית טובה״? היא טובה, אבל היא לא מתארת פעולה. הסיווג שגוי.", do=show(f"c-x-{F3}", f"c-n-{F3}")),
    P("״בלתי אפשרית״? שעתיים הדרכה זה רף סביר לגמרי.", do=show(f"c-x-{IMP3}", f"c-n-{IMP3}")),
    P("ו״מורכבת למימוש״? וזו המלכודת: מורכבות היא לא מה שקובע אם דרישה טובה. השאלה היא אם אפשר לבדוק אותה.",
      do=show(f"c-x-{CPX3}", f"c-n-{CPX3}", "c3"), hold=0.5),
], stage=w.stack(st.card("c1", "ex", "❓ פעולה, או <b>כמה טוב</b>?"),
                 st.card("c1x", "rule", "🔑 קל ללמוד = איכות ← <b>לא פונקציונלית</b>"),
                 st.card("c2", "rule", "🔑 ״עד שעתיים״ = רף מדיד ← <b>טובה</b>"),
                 st.card("c3", "trap", "⚠️ מורכבות מימוש ≠ איכות הדרישה"), gap=22),
   panel=w.qpanel(w.stem(Q3["id"], Q3["question"]),
                  st.options("c", w.opts_of(Q3), notes={F3: "לא פעולה", IMP3: "רף סביר", CPX3: "לא הקריטריון"})))

recap = Scene("recap", "סיכום", [
    P("סיכמנו את הקורס. בכל שאלה: מזהים נושא, מוצאים את השורה, ורק אז מסננים תשובות.", do=show("s1")),
    P("מילים כמו ״קבוע״, ״רק בסוף״ ו״תמיד״ מסמנות בדרך כלל מסיח.", do=show("s2")),
    P("ובשאלות על דרישות, שואלים מה הדרישה דורשת, והאם אפשר לבדוק אותה. בהצלחה במבחן!", do=show("s3"), hold=0.6),
], stage=TAB.replace('id="t', 'id="zt').replace(' class="h"', ''),
   panel=st.card("s1", "rule", "🔑 נושא ← שורה ← תשובות")
         + st.card("s2", "trap", "⚠️ ״קבוע״, ״רק בסוף״, ״תמיד״ ← חשד למסיח")
         + st.card("s3", "rule", "🔑 דרישה: מה היא דורשת? אפשר לבדוק?"))

SCENES = [title, table, q1, q2, q3, recap]
w.no_latin(SCENES)
VIDEO = Video("R09", "proc", "מבחן גמר: תהליכים, Agile ודרישות", SCENES,
              bank={"25S-A-Q4": A1, "25B-N-Q6": A2, "19B-B-Q9": A3})
