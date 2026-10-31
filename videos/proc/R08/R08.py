# -*- coding: utf-8 -*-
"""R08 · דרישה טובה, MRD ו-PRD, גילוי דרישות — video script (build: tools/video/vid.py R08).

Source: courses/proc/R08.js (lesson + goal: spot a bad requirement, vague or dictating the implementation; know MRD
and PRD; know the elicitation methods and who the stakeholders are). Exam anchor: SP-DGM-Q9 (stakeholders = every
person or organization with an interest in the system). No guided quiz uses it and it has no twin in the bank.
Each requirement on the board is judged by the course checker's rule good_requirement(testable, what_not_how)
(w_proc.good_requirement) from the attributes stated next to it; the elicitation methods are the checker's ELICITATION.
Policy: lesson rules are shown as outcomes, never in the wording of a quiz/boss option. MRD/PRD are shown on one
library example (market need, then the product details built from it) without "defined by the customer / expanded by
the product department for development"; elicitation is a story of what one team did, with no "interviews and
observations" card and no list of non-methods (retrospective, code tests: R08-Q3's distractors).
Avoided on purpose: the R08 quiz items (22S-A-Q7 with its twin 23B-A-Q1, 22B-A-Q7 with its twin SP-AMR-Q15, and the
three originals: "pleasant to use", "implement Observer", "which is an elicitation method") with their twins (26CL-Q5,
SP-DGM-Q12, 21-B-Q3, 21S-B-Q3, 23S-A-Q14, SP-AMR-Q11), and the R09 boss item 23S-A-Q4 with its twins 23B-A-Q11,
26B-A-Q6, 25B-N-Q3 (design patterns / MVC in a URD); the "how" example here is a data structure, not a pattern.
Worked requirements are mine: a library app (reliable site, intuitive UI, binary-tree search, 3-minute first loan).
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_proc as w

# ---------------------------------------------------------------- facts (checked)
REQS = [  # (key, text, testable, what_not_how, why)
    ("q1", "״האתר יהיה אמין״", False, True, "עמומה: איך בודקים ״אמין״?"),
    ("q2", "״החיפוש ימומש בעץ חיפוש בינארי״", True, False, "מכתיבה <b>איך</b> לממש"),
    ("q3", "״הממשק יהיה אינטואיטיבי״", False, True, "עמומה: אין רף"),
    ("q4", "״קורא חדש ישאיל ספר ראשון תוך 3 דקות, בלי עזרה״", True, True, "יש רף, אפשר לבדוק"),
    ("q5", "״האתר יהיה זמין 99.5% מהזמן בכל חודש״", True, True, "מדידה"),
    ("q6", "״הקורא יוכל לחפש ספר לפי שם״", True, True, "״מה״, ואפשר לבדוק"),
]
COL = {}
for k, _, t, wh, _ in REQS:
    COL[k] = "ok" if w.good_requirement(t, wh) else "bad"
assert [k for k in COL if COL[k] == "bad"] == ["q1", "q2", "q3"]
assert {"interviews", "observation", "existing_systems", "use_cases"} == w.CHK["ELICITATION"]

Q = BANK["SP-DGM-Q9"]
OK = w.opt_index(Q, "כל אדם או אירגון")
EXT = w.opt_index(Q, "גורמים חיצוניים")
FUND = w.opt_index(Q, "שממנים")
USR = w.opt_index(Q, "משתמשים צפויים")
assert Q["correctIndex"] == OK == 2 and sorted([OK, EXT, FUND, USR]) == [0, 1, 2, 3]
# each narrower option is one group inside the broad definition, so none of them is the definition
GROUPS = {"users": USR, "funders": FUND, "affected_outsiders": EXT}
assert len(set(GROUPS.values())) == 3 and OK not in GROUPS.values()
OPTS = w.opts_of(Q)

BOARD = w.board("b", [("ok", 'דרישה טובה<span class="pr-colsub">בדיקתית, ואומרת ״מה״</span>', "ok"),
                      ("bad", 'דרישה גרועה<span class="pr-colsub">עמומה, או אומרת ״איך״</span>', "bad")],
                [(k, w.ltr_runs(t), COL[k], why) for k, t, _, _, why in REQS], card_w=480, col_w=480, size=23)


def move(k):
    return hide(f"b-p-{k}") + show(f"b-c-{k}", f"b-w-{k}")


DOCS = w.table("dc", ["מסמך", "דוגמה מהספרייה", "מתי"], [
    [w.en("URD"), "״קורא יוכל להשאיל ספר בלי לעמוד בתור״, במילים של הקוראים", "דרישות המשתמש"],
    [w.en("MRD"), "״ספריות רוצות פחות תורים בדלפק״: צורך של השוק", "<b>נכתב ראשון</b>"],
    [w.en("PRD"), "עמדת השאלה עצמית, סריקת ברקוד, אישור במייל", "<b>נבנה מתוך ה-" + w.en("MRD") + "</b>"],
], widths=[130, 560, 290], size=26)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נלמד לזהות דרישה טובה, ודרישה גרועה."),
    P("נכיר את מסמכי הדרישות, ואת הדרכים לגלות דרישות, ונבין מי הם בעלי העניין."),
    P("ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">R08 · תהליכים, Agile ודרישות</div><h1>דרישה טובה, MRD ו-PRD, גילוי דרישות</h1>'
         '<p>דרישה עמומה או שמכתיבה מימוש, מסמכי הדרישות, שיטות הגילוי ובעלי העניין.</p>', layout="title")

good = Scene("good", "דרישה טובה", [
    P("דרישה טובה היא קודם כל **בדיקתית**: אפשר לבדוק, בסוף, אם היא התקיימה או לא.", do=show("k1")),
    P("ויש שתי דרכים להיות דרישה גרועה. אחת: דרישה **עמומה**, שאי אפשר לבדוק.", do=show("k2")),
    P("שתיים: דרישה שמכתיבה **איך** לממש. דרישות עונות על ״מה״, ולא על ״איך״.", do=show("k3"), hold=0.3),
    P("נמיין שש דרישות של אפליקציה לספרייה.", do=show("b")),
    P("האתר יהיה אמין. מה זה אמין? אין דרך לבדוק. עמומה, ולכן גרועה.", do=move("q1")),
    P("החיפוש ימומש בעץ חיפוש בינארי. זו החלטה של המפתחים, **איך** לממש. אין לה מקום בדרישות המשתמש.", do=move("q2")),
    P("הממשק יהיה אינטואיטיבי. שוב, אין רף. עמומה.", do=move("q3")),
    P("ועכשיו אותו רעיון, בניסוח טוב: קורא חדש ישאיל ספר ראשון תוך שלוש דקות, בלי עזרה. את זה אפשר לבדוק.",
      do=move("q4")),
    P("האתר יהיה זמין תשעים ותשעה וחצי אחוז מהזמן, בכל חודש. מדידה. טובה.", do=move("q5")),
    P("והקורא יוכל לחפש ספר לפי שם. זה ״מה״, ואפשר לבדוק שזה עובד. טובה.", do=move("q6"), hold=0.4),
], stage=BOARD,
   panel=st.card("k1", "rule", "🔑 דרישה טובה = <b>בדיקתית</b>")
         + st.card("k2", "trap", "⚠️ גרועה 1: <b>עמומה</b> (״אמין״, ״אינטואיטיבי״)")
         + st.card("k3", "trap", "⚠️ גרועה 2: מכתיבה <b>איך</b> לממש"))

docs = Scene("docs", "מסמכי דרישות", [
    P("את הדרישות כותבים במסמכים. מסמך דרישות המשתמש נכתב במילים של המשתמשים, בלי שום מימוש.", do=show("dc-r0")),
    P("נראה שני מסמכים נוספים על אותה ספרייה. ה-MRD מתאר צורך של השוק: ספריות רוצות פחות תורים בדלפק.",
      do=show("dc-r1")),
    P("ואז מחלקת המוצר לוקחת את הצורך הזה, ומפרטת: עמדת השאלה עצמית, סריקת ברקוד, אישור במייל. זה ה-PRD.",
      do=show("dc-r2")),
    P("כלומר ה-PRD נבנה **מתוך** ה-MRD, ולכן הוא בא אחריו. במבחנים מנסים להפוך את הסדר הזה.", do=show("dc-t"),
      hold=0.4),
], stage=DOCS,
   panel=st.card("dc-k", "rule", "🔑 " + w.en("MRD") + " ← " + w.en("PRD") + "<br>צורך של השוק ← פירוט למוצר").replace(' h"', '"')
         + st.card("dc-t", "trap", "⚠️ הסדר: קודם " + w.en("MRD") + ", אחריו " + w.en("PRD")))

find = Scene("find", "גילוי דרישות", [
    P("ואיך מגלים מה הספרייה באמת צריכה? הצוות של האפליקציה עשה שלושה דברים.", do=show("f0")),
    P("ישבו יום שלם ליד ספרנית: שאלו אותה שאלות, וראו איך היא עובדת בדלפק.", do=show("f1")),
    P("עברו על התוכנה הישנה של הספרייה: מה עובד בה היום, ומה מעצבן.", do=show("f2")),
    P("וכתבו צעד אחרי צעד מה קורא עושה: מחפש, משאיל, מחזיר, ומה המערכת עונה בכל צעד.", do=show("f3")),
    P("כל אחד מהם גילה דרישות שהשניים האחרים פספסו. לכן משתמשים בכמה דרכים יחד.", do=show("f4"), hold=0.4),
], stage=w.stack(st.card("f0", "plain", "📚 הצוות של אפליקציית הספרייה:"),
                 st.card("f1", "ex", "🪑 יום ליד ספרנית: שאלות, וצפייה בעבודה"),
                 st.card("f2", "ex", "🖥️ מעבר על התוכנה הישנה"),
                 st.card("f3", "ex", "📜 צעד אחר צעד: מחפש, משאיל, מחזיר"),
                 st.card("f4", "rule", "🔑 כל דרך מגלה דברים אחרים ← משלבים"), gap=20),
   layout="full")

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו שאלה ממבחן: בעלי עניין במערכת כוללים מה?"),
    P("נחשוב על האפליקציה לספרייה. מי מושפע ממנה, או אכפת לו ממנה?", do=show("x0")),
    P("הקוראים, שישתמשו בה. העירייה, שמממנת אותה. הספרניות, שהעבודה שלהן משתנה.", do=show("x1", "x2", "x3")),
    P("ואפילו הוצאות הספרים, וגוף שבודק נגישות. כולם בעלי עניין.", do=show("x4", "x5")),
    P("לכן ההגדרה היא הרחבה ביותר: כל אדם או ארגון, שיש לו עניין במערכת.", do=show(f"q-ok-{OK}")),
    P("״משתמשים צפויים״ הם רק קבוצה אחת מתוכם. נכון, אבל חלקי.", do=show(f"q-x-{USR}", f"q-n-{USR}")),
    P("גם ״מי שממן את הפיתוח״ הוא רק קבוצה אחת.", do=show(f"q-x-{FUND}", f"q-n-{FUND}")),
    P("וגם ״גורמים חיצוניים שמושפעים ישירות״. וזו המלכודת: כל תשובה חלקית נשמעת נכונה, אבל ההגדרה היא הכי רחבה.",
      do=show(f"q-x-{EXT}", f"q-n-{EXT}", "x6"), hold=0.5),
], stage=w.stack(st.card("x0", "plain", "📚 אפליקציה לספרייה: מי בעל עניין?"),
                 w.row(w.chip("x1", "👩‍🎓 קוראים", "info"), w.chip("x2", "🏛️ העירייה (מממנת)", "info"),
                       w.chip("x3", "📖 ספרניות", "info"), gap=16),
                 w.row(w.chip("x4", "🏢 הוצאות ספרים", "info"), w.chip("x5", "♿ גוף נגישות", "info"), gap=16),
                 st.card("x6", "trap", "⚠️ תשובה חלקית ≠ ההגדרה. בוחרים את <b>הרחבה</b>"), gap=24),
   panel=w.qpanel(w.stem(Q["id"], Q["question"]),
                  st.options("q", OPTS, notes={USR: "רק חלק", FUND: "רק חלק", EXT: "רק חלק"})))

recap = Scene("recap", "סיכום", [
    P("לסיכום: דרישה טובה היא בדיקתית, ואומרת ״מה״. עמומה, או ״איך״, היא גרועה.", do=show("s1")),
    P("ה-MRD מתאר צורך של השוק, וה-PRD מפרט אותו למוצר, אחריו.", do=show("s2")),
    P("ומגלים דרישות בכמה דרכים יחד: לשבת ליד המשתמשים, לבחון את מה שקיים, ולכתוב צעד אחר צעד.", do=show("s3")),
    P("ובעלי עניין: כל מי שיש לו עניין במערכת. נתראה ברמה הבאה.", do=show("s4"), hold=0.6),
], stage=DOCS.replace('id="dc', 'id="zc').replace(' class="h"', ''),
   panel=st.card("s1", "rule", "🔑 בדיקתית + ״מה״ = טובה")
         + st.card("s2", "rule", "🔑 " + w.en("MRD") + " ← " + w.en("PRD") + ": צורך ← פירוט")
         + st.card("s3", "rule", "🔑 גילוי דרישות: כמה דרכים, יחד")
         + st.card("s4", "rule", "🔑 בעלי עניין = <b>כל</b> מי שיש לו עניין"))

SCENES = [title, good, docs, find, exam, recap]
w.no_latin(SCENES)
VIDEO = Video("R08", "proc", "דרישה טובה, MRD ו-PRD, גילוי דרישות", SCENES, bank={"SP-DGM-Q9": OK})
