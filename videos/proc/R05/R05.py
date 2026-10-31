# -*- coding: utf-8 -*-
"""R05 · Scrum: ארבע הפגישות של הספרינט — video script (build: tools/video/vid.py R05).

Source: courses/proc/R05.js (lesson + goal: match each event, Planning, Daily, Review, Retrospective, to its purpose,
its time and what is discussed in it). Exam anchor: 26CL-Q7 (a half-hour technical debate inside the Daily Scrum ->
stop it and continue after the meeting with the people involved). No guided quiz uses it and it has no twin in the bank.
Each worked situation is checked against the course checker's EVENT table, and the Daily facts against DAILY
(w_proc.CHK).
Avoided on purpose: the R05 quiz items (24B-B-Q6 the retrospective, 24B-B-Q3 the burn-down chart, and the three
originals) with their twins (25F0b-Q4, 26CL-Q8, 22S-A-Q6, 23B-A-Q7, 21-B-Q8, 21S-B-Q8, 24B-A-Q6, 23S-A-Q7, 23B-A-Q14,
22B-A-Q3), and the R09 boss item 24B-A-Q2 with its twin 24S-A-Q2: the Review is taught as "show the completed work and
get feedback", never as "update the Backlog". Per the review policy the Daily is "very short, before the day's
work" (not "10-20 minutes at the start of the day", R05-Q2's key), the Retrospective is "what helped, what got
in the way" (not 24B-B-Q6's "what worked well and what can be improved"), and the Review case is not R05-Q3's
"customer watches a demo of the finished features". The burn-down chart is left out. Worked situations are mine: choosing
the next two weeks' items, a sign-up screen status, a finished search judged by a librarian ("useless without a year
filter"), bugs waiting two days for
testing.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_proc as w

# ---------------------------------------------------------------- facts (checked)
E = w.CHK["EVENT"]
D = w.CHK["DAILY"]
assert D["minutes"] == (10, 20) and D["when"] == "start_of_day" and D["purpose"] == "status" and D["exists"]
SIT = [  # (key, situation, checker purpose)
    ("e1", "הצוות בוחר אילו פריטים ייכנסו לשבועיים הקרובים", "plan_next_sprint"),
    ("e2", "״אתמול סיימתי את מסך ההרשמה, היום אתחיל בתשלום״", "daily_status"),
    ("e3", "החיפוש שנגמר רץ מול הספרנית: ״בלי סינון לפי שנה הוא לא שימושי״", "show_completed"),
    ("e4", "״באגים מחכים יומיים לבדיקה. איך נשפר את זה?״", "improve_process"),
]
WANT = {"e1": "Sprint Planning", "e2": "Daily Scrum", "e3": "Sprint Review", "e4": "Sprint Retrospective"}
for k, _, purpose in SIT:
    assert E[purpose] == WANT[k], (k, E[purpose])

Q = BANK["26CL-Q7"]
OK = w.opt_index(Q, "לעצור את הדיון")
CAN = w.opt_index(Q, "לבטל את ה-Daily")
EXT = w.opt_index(Q, "להאריך את הפגישה")
POD = w.opt_index(Q, "יכריע מיד")
ALL = w.opt_index(Q, "כל התשובות")
assert Q["correctIndex"] == OK == 3 and sorted([OK, CAN, EXT, POD, ALL]) == [0, 1, 2, 3, 4]
assert D["purpose"] == "status"            # the daily is a sync, so a technical debate does not belong in it
OPTS = w.opts_of(Q, short={OK: "לעצור את הדיון ולהמשיך אותו אחרי הפגישה עם המעורבים בלבד. ה-Daily Scrum היא פגישה "
                                "קצרה (כ-15 דקות) לסנכרון: מה עשיתי, מה אעשה ומה חוסם אותי"})
assert OPTS[-1][0] == ALL

NODES = [("plan", "תכנון: מה נעשה", "Sprint Planning"), ("work", "עבודה + פגישה יומית", "Daily Scrum"),
         ("rev", "מציגים מה הושלם", "Sprint Review"), ("retro", "משפרים את התהליך", "Retrospective")]
CYC = w.cycle("cy", NODES, w=1000, h=600, r=215, loop_on="work")
EVT = w.table("ev", ["הפגישה", "מתי", "על מה מדברים"], [
    [w.en("Sprint Planning"), "תחילת הספרינט", "<b>קדימה</b>: יעדי הספרינט, ומה ייכנס אליו"],
    [w.en("Daily Scrum"), "כל יום, קצרה", "<b>היום</b>: מה עשיתי, מה אעשה, מה חוסם"],
    [w.en("Sprint Review"), "סוף הספרינט", "<b>המוצר</b>: הצגת מה שהושלם, ומשוב"],
    [w.en("Retrospective"), "סוף הספרינט", "<b>איך עבדנו</b>: מה עזר, ומה הפריע"],
], widths=[260, 250, 470], size=26)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נכיר את ארבע הפגישות של הספרינט ב-Scrum."),
    P("נלמד שאלה אחת שמזהה כל פגישה: ״על מה מדברים בה?״"),
    P("ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">R05 · תהליכים, Agile ודרישות</div><h1>Scrum: ארבע הפגישות של הספרינט</h1>'
         '<p>Planning, Daily, Review ו-Retrospective: מתי כל אחת, ועל מה מדברים בה.</p>', layout="title")

loop = Scene("loop", "מחזור הספרינט", [
    P("ב-Scrum העבודה מחולקת ל**ספרינטים**: איטרציות באורך קבוע, לרוב שבועיים עד ארבעה.", do=show("cy-mid")),
    P("ספרינט נפתח ב-Sprint Planning. מתכננים את יעדי הספרינט, ובוחרים מה ייכנס אליו.", do=show("cy-n-plan", "cy-e0")),
    P("אחר כך עובדים. ובכל יום, בבוקר, יש פגישה קצרה: ה-Daily Scrum.", do=show("cy-n-work", "cy-loop", "cy-e1")),
    P("בסוף הספרינט יש שתי פגישות. ב-Sprint Review מציגים את מה שהושלם.", do=show("cy-n-rev", "cy-e2")),
    P("וב-Retrospective הצוות מסתכל על **עצמו**: מה עזר לו לעבוד, ומה הפריע.", do=show("cy-n-retro", "cy-e3")),
    P("ומשם, ספרינט חדש מתחיל, עם Planning חדש.", do=show("cy-h-plan"), hold=0.4),
], stage=CYC, layout="full")

table = Scene("table", "על מה מדברים", [
    P("עכשיו כל פגישה, ועל מה מדברים בה. Planning מסתכלת **קדימה**: מה היעד, ומה ייכנס לספרינט.", do=show("ev-r0")),
    P("Daily מסתכלת על **היום**: כל אחד אומר מה עשה אתמול, מה יעשה היום, ומה חוסם אותו.", do=show("ev-r1")),
    P("והיא קצרה מאוד, לפני שהעבודה של היום מתחילה. אם היא מתארכת, היא הפסיקה להיות סנכרון.", do=show("ev-m1")),
    P("Review מסתכלת על **המוצר**: מציגים את מה שהושלם בספרינט הזה, ומקבלים משוב.", do=hide("ev-m1") + show("ev-r2")),
    P("ו-Retrospective מסתכלת על **הדרך שבה הצוות עובד**: מה עזר בספרינט, מה הפריע, ומה ינסו אחרת.", do=show("ev-r3")),
    P("וזו המלכודת הכי נפוצה: Review היא על המוצר. Retrospective היא על התהליך.", do=show("ev-t"), hold=0.4),
], stage=EVT,
   panel=st.card("ev-k", "rule", "🔑 קדימה ← " + w.en("Planning") + "<br>היום ← " + w.en("Daily")
                 + "<br>המוצר ← " + w.en("Review") + "<br>התהליך ← " + w.en("Retrospective")).replace(' h"', '"')
         + st.card("ev-t", "trap", "⚠️ " + w.en("Review") + " = המוצר · " + w.en("Retrospective") + " = התהליך"))

ex = Scene("ex", "איזו פגישה?", [
    P("נתרגל. ארבעה מצבים, ולכל אחד נשאל: על מה מדברים כאן?"),
    P("הצוות בוחר אילו פריטים ייכנסו לשבועיים הקרובים. מסתכלים קדימה, ולכן Sprint Planning.", do=show("e1", "e1-p")),
    P("מפתח אומר: אתמול סיימתי את מסך ההרשמה, והיום אתחיל בתשלום. זה סטטוס, ולכן Daily.", do=show("e2", "e2-p")),
    P("החיפוש שנגמר רץ מול הספרנית, והיא אומרת: בלי סינון לפי שנה, הוא לא שימושי. מדברים על המוצר, ולכן Review.", do=show("e3", "e3-p")),
    P("ובסוף הספרינט מישהו אומר: באגים מחכים יומיים לבדיקה, איך נשפר את זה? זה התהליך, ולכן Retrospective.",
      do=show("e4", "e4-p"), hold=0.4),
], stage=w.stack(*[f'<div id="{k}" class="pr-need h"><span class="pr-nd">{w.ltr_runs(t)}</span><span class="pr-arr">←</span>'
                   f'<span id="{k}-p" class="pr-pat h">{w.en(WANT[k])}</span></div>' for k, t, _ in SIT], gap=24),
   layout="full")

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו שאלה ממבחן. באמצע ה-Daily Scrum, שני מפתחים פותחים דיון טכני של חצי שעה, על הדרך לממש את מודול התשלומים."),
    P("מה הפעולה הנכונה? קודם נזכור מה ה-Daily: פגישה קצרה, **לסנכרון**. לא פותרים בה בעיות.", do=show("x1")),
    P("ולכן עוצרים את הדיון, וממשיכים אותו אחרי הפגישה, רק עם מי שמעורב בו.", do=show(f"q-ok-{OK}", "x2")),
    P("ככה כל השאר לא מחכים חצי שעה, והבעיה עדיין נפתרת, באותו יום.", hold=0.2),
    P("להאריך את הפגישה עד שכולם מסכימים? זה בדיוק הופך אותה לדיון טכני ארוך. לא.",
      do=show(f"q-x-{EXT}", f"q-n-{EXT}")),
    P("לבטל את ה-Daily ולקיים Planning חדש? Planning פותחת ספרינט. היא לא פותרת ויכוח טכני.",
      do=show(f"q-x-{CAN}", f"q-n-{CAN}")),
    P("ה-Product Owner יכריע בדיון הטכני? הוא קובע **מה** בונים ובאיזה סדר. **איך** לממש, מחליט הצוות.",
      do=show(f"q-x-{POD}", f"q-n-{POD}")),
    P("ומכיוון שיש תשובה נכונה, ״כל התשובות האחרות שגויות״ נופלת.", do=show(f"q-x-{ALL}"), hold=0.5),
], stage=w.stack(st.card("x1", "rule", "🔑 " + w.en("Daily") + " = סנכרון קצר: מה עשיתי, מה אעשה, מה חוסם"),
                 st.card("x2", "ex", "💬 דיון טכני ← <b>אחרי</b> הפגישה, רק עם המעורבים"), gap=26),
   panel=w.qpanel(w.stem(Q["id"], "באמצע ה-" + w.en("Daily Scrum") + " שני מפתחים פותחים דיון טכני של חצי שעה. מה הפעולה הנכונה?"),
                  st.options("q", OPTS, notes={EXT: "הופך לדיון", CAN: "לא קשור", POD: "איך = הצוות"})))

recap = Scene("recap", "סיכום", [
    P("לסיכום: Planning בתחילת הספרינט, ומסתכלת קדימה.", do=show("s1")),
    P("Daily בכל בוקר, קצרה, לסנכרון בלבד. דיונים ארוכים, אחריה.", do=show("s2")),
    P("Review בסוף הספרינט, על המוצר. Retrospective בסוף הספרינט, על התהליך. נתראה ברמה הבאה.", do=show("s3"), hold=0.6),
], stage=EVT.replace('id="ev', 'id="zv').replace(' class="h"', ''),
   panel=st.card("s1", "rule", "🔑 " + w.en("Planning") + ": קדימה")
         + st.card("s2", "rule", "🔑 " + w.en("Daily") + ": סנכרון קצר, בלי פתרון בעיות")
         + st.card("s3", "rule", "🔑 " + w.en("Review") + ": המוצר · " + w.en("Retrospective") + ": התהליך"))

SCENES = [title, loop, table, ex, exam, recap]
w.no_latin(SCENES)
VIDEO = Video("R05", "proc", "Scrum: ארבע הפגישות של הספרינט", SCENES, bank={"26CL-Q7": OK})
