# -*- coding: utf-8 -*-
"""U06 · תרשים רצף בתרחיש: Actor, participants ומה חסר — video script (build: tools/video/vid.py U06).

Source: courses/uml/U06.js (lesson + goal: cast a scenario's parties as Actor / participants, complete the missing
marks of a sequence diagram, how many sequence diagrams a system has). Exam anchor: 25S-A-Q13 (product catalogue:
the sequence diagram of the scheduled Batch process -> Batch, the scheduler, the DB), which no guided quiz uses and
which has no twin in the bank. Missing returns come from the course checker (w_uml.CHK.missing_returns).
Avoided on purpose: the U06 quiz items (clinic/SMS casting, the load page/read row missing returns, "which relations
in a sequence diagram" and its twin 25F0a-Q14, 24B-B-Q18 and its twin 24S-A-Q16, 26CL-Q10), 25B-N-Q13 (cited in the
lesson), 24B-A-Q26 and 26S-A-Q15 (the lesson's save-data figure; 26S-A-Q15 is solved in the U09 video).
My worked scenario is a smart water meter pushing a reading (a device as the Actor; the server acknowledges at once, then stores), so it is not a request -> server -> service chain and has no nested returns.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_uml as w

C = w.CHK
assert "activation" in C.SEQ_NOTATION and "return" in C.SEQ_NOTATION
# casting: the party that starts the scenario is the Actor (here a device); system parts are participants
CAST = {"מונה": "actor", "שרת": "part", "מסד נתונים": "part"}
assert [k for k, v in CAST.items() if v == "actor"] == ["מונה"]
# the meter scenario: the server acknowledges at once, then stores; every receiver of a call gets a bar, and every
# callee answers its own caller
MSGS = [("mt", "sv", "reading", False), ("sv", "mt", "ack", True), ("sv", "db", "save()", False), ("db", "sv", "ok", True)]
for a, b, _, ret in MSGS:
    if ret:
        assert any(x == b and y == a and not r for x, y, _, r in MSGS), (a, b)     # a return goes back to its caller

# exam 25S-A-Q13
Q = BANK["25S-A-Q13"]
assert Q["correctIndex"] == 4 and Q["options"][4] == "תהליך ה-Batch, המתזמן ומסד הנתונים"
assert "מנהל המערכת" in Q["options"][2] and "הלקוח" in Q["options"][3]
assert Q["options"][0] == "לא ניתן לדעת" and Q["options"][1] == "כל התשובות האחרות שגויות"
assert "תהליך Batch שרץ בצורה מתוזמנת" in Q["question"]
OPTS = w.opts_of(Q)

# ---------------------------------------------------------------- diagrams
D = w.Dia("mt", 1000, 520)
D.lifeline("mt", 120, 20, 510, "מונה מים", kind="actor", hidden=True)
D.lifeline("sv", 500, 50, 510, "Server", w=160, hidden=True)
D.lifeline("db", 860, 40, 510, "DB", kind="db", hidden=True)
D.msg("m1", "mt", "sv", 200, "reading", ob=0)
D.msg("m2", "sv", "db", 330, "save()", ob=0)
D.msg("m1b", "mt", "sv", 200, "reading", ob=12)
D.msg("m2b", "sv", "db", 330, "save()", oa=12, ob=12)
D.act("asv", "sv", 200, 420)
D.act("adb", "db", 330, 410)
D.msg("r1", "sv", "mt", 260, "ack", ret=True, oa=12, ob=0)
D.msg("r2", "db", "sv", 410, "ok", ret=True, oa=12, ob=12)
D.ring("q1", 460, 180, 80, 260, rx=30)
D.ring("q2", 820, 310, 80, 120, rx=30)

SCN = [("מונה שולח קריאה", "המונה"), ("תושב צופה בצריכה שלו", "התושב"), ("טכנאי מחליף מונה", "הטכנאי")]

EX = w.Dia("bt", 1000, 420)
EX.lifeline("sc", 110, 10, 410, "מתזמן", kind="actor", hidden=True)
EX.lifeline("ba", 470, 40, 410, "Batch", w=160, hidden=True)
EX.lifeline("db", 830, 30, 410, "DB", kind="db", hidden=True)
EX.act("aba", "ba", 190, 380)
EX.act("adb", "db", 250, 320)
EX.msg("m1", "sc", "ba", 190, "run()", ob=12)
EX.msg("m2", "ba", "db", 250, "check stock", oa=12, ob=12)
EX.msg("r2", "db", "ba", 320, "rows", ret=True, oa=12, ob=12)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נבנה תרשים רצף מתוך תיאור של מערכת אמיתית."),
    P("נחליט מי הוא ה־Actor ומי הם ה־participants, ונמצא מה חסר בתרשים.",
      say="נחליט מי הוא האַקְטוֹר ומי הם הפַּרְטִיסִיפַּנְטִים, ונמצא מה חסר בתרשים."),
    P("ובסוף נפתור שאלה ממבחן על תהליך שאף אדם לא מפעיל.", hold=0.4),
], stage='<div class="kicker">U06 · UML ומידול</div><h1>תרשים רצף בתרחיש: Actor, participants ומה חסר</h1>'
         '<p>לשבץ גורמים כ-Actor או participant, להשלים סימונים חסרים בתרשים, ולדעת כמה תרשימי רצף יש למערכת.</p>',
   layout="title")

cast = Scene("cast", "מי Actor ומי participant", [
    P("התרחיש: מונה מים חכם בבית שולח פעם בשעה קריאה לשרת של חברת המים. השרת שומר אותה במסד הנתונים.",
      do=show("t-1")),
    P("השאלה הראשונה: מי **מתחיל** את האינטראקציה? המונה. הוא ה־Actor, איש המקל.", do=show("mt", "mt-mt", "c1"),
      say="השאלה הראשונה: מי מתחיל את האינטראקציה? המונה. הוא האַקְטוֹר, איש המקל."),
    P("שימו לב: המונה הוא מכשיר, לא אדם. ובכל זאת הוא ה־Actor, כי הוא זה שפותח את התרחיש.",
      say="שימו לב: המונה הוא מכשיר, לא אדם. ובכל זאת הוא האַקְטוֹר, כי הוא זה שפותח את התרחיש.", hold=0.2),
    P("השרת מקבל את הקריאה ומטפל בה. הוא חלק מהמערכת, ולכן participant.", do=show("mt-sv"),
      say="השרת מקבל את הקריאה ומטפל בה. הוא חלק מהמערכת, ולכן פַּרְטִיסִיפַּנְט."),
    P("וגם מסד הנתונים: הוא לא מתחיל כלום, רק עונה לשרת. גם הוא participant.", do=show("mt-db", "c2"),
      say="וגם מסד הנתונים: הוא לא מתחיל כלום, רק עונה לשרת. גם הוא פַּרְטִיסִיפַּנְט.", hold=0.3),
], stage=w.stack('<div id="t-1" class="card ex h" style="font-size:28px">💧 מונה מים חכם שולח קריאה לשרת · השרת שומר במסד</div>',
                 D.svg(hidden=True), gap=12),
   panel=st.card("c1", "rule", "🔑 מי <b>פותח</b> את התרחיש? ← Actor (גם מכשיר)")
         + st.card("c2", "rule", "🔑 מי שרק <b>מטפל ועונה</b> ← participant"))

miss = Scene("miss", "מה חסר?", [
    P("מישהו צייר טיוטה: המונה שולח קריאה לשרת.", do=show("mt2-m1")),
    P("השרת מאשר מיד למונה שהקריאה הגיעה, בחץ מקווקו.", do=show("mt2-r1")),
    P("ואחר כך השרת שולח שמירה למסד הנתונים.", do=show("mt2-m2"), hold=0.2),
    P("מה חסר? הראשון: השרת קיבל קריאה ועבד עליה, אבל אין אצלו **סרגל הפעלה**.", do=show("mt2-q1")),
    P("מוסיפים לשרת סרגל, מהרגע שהקריאה הגיעה ועד שהשמירה הסתיימה.",
      do=hide("mt2-q1", "mt2-m1", "mt2-m2") + show("mt2-m1b", "mt2-m2b", "mt2-asv", "c4")),
    P("השני: גם מסד הנתונים קיבל קריאה. אז גם הוא מקבל סרגל, וגם הוא צריך לענות.", do=show("mt2-q2", "mt2-adb")),
    P("למי הוא עונה? למי שפנה אליו: לשרת. לא למונה, שבכלל לא דיבר איתו.", do=hide("mt2-q2") + show("mt2-r2", "c5"), hold=0.3),
], stage=D.copy("mt2", shown=("mt", "sv", "db")),
   panel=st.card("c4", "rule", "🔑 מי שקיבל קריאה ועובד עליה ← <b>סרגל הפעלה</b>")
         + st.card("c5", "rule", "🔑 תשובה מקווקוות חוזרת <b>אל מי שקרא</b>: מסד ← שרת"))

count = Scene("count", "כמה תרשימים?", [
    P("ועכשיו: כמה תרשימי רצף נצייר למערכת של חברת המים?"),
    P("תרשים רצף אחד מתאר **תרחיש אחד**. לכן סופרים תרחישים, לא רכיבים.", do=show("n-0")),
    P("מונה ששולח קריאה: תרשים אחד. תושב שצופה בצריכה שלו: תרשים שני.", do=show("n-1", "n-2")),
    P("וטכנאי שמחליף מונה: תרשים שלישי. ובכל תרחיש, ה־Actor הוא מי שפותח אותו: המונה, התושב, או הטכנאי.", do=show("n-3"),
      say="וטכנאי שמחליף מונה: תרשים שלישי. ובכל תרחיש, האַקְטוֹר הוא מי שפותח אותו: המונה, התושב, או הטכנאי.", hold=0.3),
], stage=w.stack(st.card("n-0", "plain", "תרחיש אחד = תרשים רצף אחד"),
                 *[st.card(f"n-{i + 1}", "ex", f"🎬 {t} · Actor: <b>{a}</b>") for i, (t, a) in enumerate(SCN)], gap=22),
   panel=st.card("c7", "rule", "🔑 בכל תרחיש בודקים מחדש: מי פותח אותו?").replace(' h"', '"'))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: קטלוג מוצרים. אחד הרכיבים הוא תהליך שרץ בצורה **מתוזמנת**, ובודק את המלאי והזמינות של המוצרים.",
      do=show("x-1")),
    P("מה יכיל תרשים הרצף של התהליך הזה?"),
    P("תרשים רצף מתאר **תרחיש אחד**. כאן התרחיש הוא הריצה המתוזמנת, ולא שום דבר אחר במערכת.", do=show("x-2")),
    P("מי מתחיל אותו? אף אדם. הוא רץ לפי לוח זמנים, ולכן מי שמפעיל אותו הוא **המתזמן**.", do=show("bt", "bt-sc")),
    P("התהליך עצמו מעבד, ופונה למסד הנתונים כדי לבדוק את המלאי.",
      do=show("bt-ba", "bt-db", "bt-m1", "bt-aba", "bt-m2", "bt-adb", "bt-r2")),
    P("מנהל המערכת לא מפעיל את התהליך: הוא רץ לבד. לכן האפשרות עם המנהל נופלת.", do=show("q-x-2", "q-n-2")),
    P("והלקוח שצופה במוצרים שייך לתרחיש אחר לגמרי. גם האפשרות הזו נופלת.", do=show("q-x-3", "q-n-3")),
    P("התיאור כן נותן את התשובה, ולכן ״לא ניתן לדעת״ נופלת.", do=show("q-x-0", "q-n-0")),
    P("התשובה: התהליך, המתזמן ומסד הנתונים. ולכן גם ״כל התשובות שגויות״ לא נכונה.", do=show("q-ok-4", "q-x-1"), hold=0.3),
    P("המלכודת: לחפש אדם שיהיה ה־Actor. מי שמתחיל יכול להיות גם מתזמן, מרכזייה או מערכת אחרת.", do=show("x-t"),
      say="המלכודת: לחפש אדם שיהיה האַקְטוֹר. מי שמתחיל יכול להיות גם מתזמן, מרכזייה או מערכת אחרת.", hold=0.5),
], stage=w.stack(st.card("x-1", "ex", "⏱️ רכיב 3: תהליך <b>Batch</b> שרץ בצורה <b>מתוזמנת</b> ומוודא מלאי וזמינות"),
                 st.card("x-2", "plain", "תרשים רצף = <b>תרחיש אחד</b>: הריצה המתוזמנת"),
                 EX.svg(hidden=True),
                 st.card("x-t", "trap", "⚠️ ה-Actor לא חייב להיות אדם: כאן זה המתזמן"), gap=10),
   panel=w.stem(Q["id"], "תרשים הרצף של תהליך ה-Batch שמוודא את המלאי והזמינות יכיל:")
         + st.options("q", OPTS, notes={0: "כתוב בתיאור", 2: "רץ לבד", 3: "תרחיש אחר"}))

recap = Scene("recap", "סיכום", [
    P("לסיכום: מי שמתחיל את התרחיש הוא ה־Actor. אדם, מרכזייה, או מתזמן.", do=show("s-1"),
      say="לסיכום: מי שמתחיל את התרחיש הוא האַקְטוֹר. אדם, מרכזייה, או מתזמן."),
    P("רכיבי המערכת והשירותים שהיא פונה אליהם הם ה־participants.", do=show("s-2"),
      say="רכיבי המערכת והשירותים שהיא פונה אליהם הם הפַּרְטִיסִיפַּנְטִים."),
    P("מי שקיבל קריאה ועובד עליה מקבל סרגל, ומי שנקרא עונה למי שקרא לו. ותרשים אחד מתאר תרחיש אחד. נתראה ברמה הבאה.",
      do=show("s-3"), hold=0.6),
], stage=D.copy("mt3", reveal=True, keep=("m1", "m2", "q1", "q2")),
   panel=st.card("s-1", "rule", "🔑 מתחיל = Actor (לא חייב אדם)")
         + st.card("s-2", "rule", "🔑 רכיבים ושירותים = participants")
         + st.card("s-3", "rule", "🔑 סרגל אצל מי שעובד · תשובה אל מי שקרא · תרחיש אחד לתרשים"))

SCENES = [title, cast, miss, count, exam, recap]
w.no_latin(SCENES)
VIDEO = Video("U06", "uml", "תרשים רצף בתרחיש: Actor, participants ומה חסר", SCENES, bank={"25S-A-Q13": 4})
