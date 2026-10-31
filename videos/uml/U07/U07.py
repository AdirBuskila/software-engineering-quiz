# -*- coding: utf-8 -*-
"""U07 · תרשים מצבים: מצבים, מעברים, XOR ו-AND — video script (build: tools/video/vid.py U07).

Source: courses/uml/U07.js (lesson + goal: what a statechart describes and what it does not include; XOR vs AND).
Exam anchor: 23-EX-Q16 ("a statechart differs from a state machine by" -> concurrency), which no guided quiz uses;
its twin 25-EX-Q16 is not used anywhere either. Components and XOR/AND come from the course checker
(w_uml.CHK.STATE_COMPONENTS, CHK.substate_kind).
Avoided on purpose: the U07 quiz items (the music player XOR and AND questions, "which is not a component", "what fits
a statechart") and their twins 23-EX-Q17 / 25-EX-Q17 / 23-EX-Q20 / 25-EX-Q20 / 23-EX-Q19; 24B-B-Q15 (U07 quiz),
24B-B-Q16 (boss); the lesson's elevator and coffee-machine examples. Mine: a traffic light and a phone.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_uml as w

C = w.CHK
assert C.STATE_COMPONENTS == {"state", "transition", "initial_state", "guard", "history"}
assert "message" not in C.STATE_COMPONENTS
assert C.substate_kind(True, False) == "XOR"          # locked / unlocked: exactly one at a time
assert C.substate_kind(False, True) == "AND"          # screen region and network region: independent, at once

# the traffic light: its transitions, and a run of events that respects the guard
TL = {("red", "timer"): "green", ("green", "timer"): "yellow", ("yellow", "timer"): "red"}
GUARD = {("green", "timer"): "walker"}                # green -> yellow only when a pedestrian waits


def step(state, event, walker):
    if GUARD.get((state, event)) == "walker" and not walker:
        return state
    return TL.get((state, event), state)


assert step("green", "timer", False) == "green" and step("green", "timer", True) == "yellow"
assert step(step(step("red", "timer", False), "timer", True), "timer", False) == "red"

# exam 23-EX-Q16
Q = BANK["23-EX-Q16"]
assert Q["correctIndex"] == 0 and Q["options"][0] == "מקבול"
assert Q["options"][1] == "כל התשובות נכונות" and Q["options"][2] == "שאינו שומר מצב"
assert Q["options"][3] == "תרשים מיצוב הוא רק סידרתי" and Q["options"][4] == "שאין בו מצבים אלא מיצובים"
OPTS = w.opts_of(Q)

# ---------------------------------------------------------------- diagrams
T = w.Dia("tl", 1000, 520)
T.initial("i", 40, 112, hidden=True)
T.state("red", 100, 70, 210, 84, "אדום", hidden=True)
T.state("green", 690, 70, 210, 84, "ירוק", hidden=True)
T.state("yellow", 395, 380, 210, 84, "צהוב", hidden=True)
T.rel("t0", "i", "red", "trans")
T.rel("t1", "red", "green", "trans", label="טיימר", lxy=(500, 98))
T.rel("t2", "green", "yellow", "trans", label="טיימר [הולך רגל ממתין]", lxy=(810, 262))
T.rel("t3", "yellow", "red", "trans", label="טיימר", lxy=(215, 262))
T.ring("g", 660, 232, 300, 50, rx=20)


def phone(pfx, both):
    d = w.Dia(pfx, 1000, 600 if both else 340)
    d.region("on", 40, 10, 920, 580 if both else 320, "טלפון: פועל", hidden=True)
    d.text("ls", 58, 96, "מסך", cls="u-lab mut", anchor="end", hidden=True)
    d.initial("i1", 110, 190, hidden=True)
    d.state("lock", 170, 150, 230, 80, "נעול", hidden=True)
    d.state("open", 640, 150, 230, 80, "פתוח", hidden=True)
    d.rel("ti", "i1", "lock", "trans")
    d.rel("t1", "lock", "open", "trans", via=((520, 120),), label="קוד נכון", lxy=(520, 106))
    d.rel("t2", "open", "lock", "trans", via=((520, 260),), label="טיימר", lxy=(520, 292))
    if both:
        d.divider("div", 40, 330, 960, 330)
        d.text("ln", 58, 376, "רשת", cls="u-lab mut", anchor="end", hidden=True)
        d.initial("i2", 110, 460, hidden=True)
        d.state("wifi", 170, 420, 230, 80, "Wi-Fi", hidden=True)
        d.state("cell", 640, 420, 230, 80, "סלולרי", hidden=True)
        d.rel("ti2", "i2", "wifi", "trans")
        d.rel("t3", "wifi", "cell", "trans", via=((520, 390),), label="אין קליטה", lxy=(520, 376))
        d.rel("t4", "cell", "wifi", "trans", via=((520, 530),), label="יש קליטה", lxy=(520, 562))
        d.ring("rd", 30, 312, 940, 36, rx=18)
    d.ring("rl", 160, 140, 250, 100, rx=26)
    d.ring("ro", 630, 140, 250, 100, rx=26)
    return d


X = phone("xr", False)
A = phone("an", True)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נכיר את תרשים המצבים: באילו מצבים מערכת יכולה להיות, ואיך עוברים ביניהם."),
    P("נראה מה יש בו ומה אין בו, ונבדיל בין מצב XOR למצב AND.", say="נראה מה יש בו ומה אין בו, ונבדיל בין מצב אֶקְס אוֹר למצב אֶנְד."),
    P("ובסוף נפתור שאלה ממבחן על מה שתרשים מצבים מוסיף.", hold=0.4),
], stage='<div class="kicker">U07 · UML ומידול</div><h1>תרשים מצבים: מצבים, מעברים, XOR ו-AND</h1>'
         '<p>לדעת מה מתאר תרשים מצבים ומה לא נכלל בו, ולהבדיל בין מצב XOR למצב AND.</p>',
   layout="title")

basics = Scene("basics", "מצבים ומעברים", [
    P("תרשים מצבים מתאר את **כל המצבים האפשריים** של מערכת, ואת המעברים ביניהם. ניקח רמזור.", do=show("tl", "c1")),
    P("כל מצב הוא מלבן מעוגל: אדום, ירוק וצהוב.", do=show("tl-red", "tl-green", "tl-yellow")),
    P("העיגול המלא הוא **המצב ההתחלתי**. הרמזור נדלק באדום.", do=show("tl-i", "tl-t0")),
    P("חץ הוא **מעבר**, ועליו כתוב האירוע שמפעיל אותו. כאן: טיימר.", do=show("tl-t1", "tl-t3")),
    P("ועל מעבר אפשר לשים **תנאי** בסוגריים מרובעים. מירוק לצהוב עוברים רק אם הולך רגל ממתין.", do=show("tl-t2", "tl-g")),
    P("אם הטיימר נגמר ואף אחד לא ממתין, התנאי לא מתקיים, והרמזור נשאר ירוק.", do=show("c2"), hold=0.3),
    P("ומה **אין** בתרשים מצבים? אין בו הודעות בין עצמים: זה העולם של תרשים רצף.", do=hide("tl-g") + show("c3")),
    P("והוא גם לא מתאר תרחיש אחד מסוים. הוא מתאר את כל ההתנהגות האפשרית.", hold=0.3),
], stage=T.svg(hidden=True),
   panel=st.card("c1", "rule", "🔑 תרשים מצבים = <b>כל המצבים</b> והמעברים · מודל התנהגות")
         + st.card("c2", "ex", "מצב התחלתי · מעבר עם אירוע · תנאי <span dir=\"ltr\">[guard]</span>")
         + st.card("c3", "trap", "⚠️ אין <b>הודעות</b> בין עצמים, ואין תרחיש מסוים"))

xor = Scene("xor", "מצב XOR", [
    P("עכשיו מצבים מורכבים. טלפון במצב גדול אחד: פועל.", do=show("xr", "xr-on")),
    P("בתוכו שני תתי מצבים של המסך: נעול, ופתוח.", do=show("xr-ls", "xr-i1", "xr-lock", "xr-open", "xr-ti")),
    P("קוד נכון פותח את המסך, וטיימר נועל אותו שוב.", do=show("xr-t1", "xr-t2")),
    P("עכשיו המסך נעול.", do=show("xr-rl")),
    P("הקוד נכון, והמסך פתוח. הנעול כבוי, והפתוח דולק.", do=hide("xr-rl") + show("xr-ro")),
    P("נעול **או** פתוח, אף פעם שניהם. מצב כזה נקרא XOR, כמו ״או״ שמוציא את השני.", do=hide("xr-ro") + show("c4"),
      say="נעול או פתוח, אף פעם שניהם. מצב כזה נקרא אֶקְס אוֹר, כמו: או, שמוציא את השני.", hold=0.3),
], stage=X.svg(hidden=True),
   panel=st.card("c4", "rule", "🔑 <b>XOR</b>: נעול <b>או</b> פתוח, אף פעם שניהם"))

and_ = Scene("and", "מצב AND", [
    P("עכשיו נוסיף לטלפון עוד היבט: הרשת. היא יכולה להיות בוואי פיי או בסלולרי.",
      do=show("an-div", "an-ln", "an-i2", "an-wifi", "an-cell", "an-ti2", "an-t3", "an-t4")),
    P("הקו המקווקו מחלק את המצב הגדול לשני אזורים, שפועלים **במקביל**.", do=show("an-rd")),
    P("המסך יכול להיות נעול, ובאותו זמן הרשת בוואי פיי. או פתוח, ובסלולרי. כל צירוף אפשרי.", do=hide("an-rd") + show("c5")),
    P("ונעילת המסך לא מזיזה את הרשת, ואובדן קליטה לא נועל את המסך. כל אזור מתקדם בקצב שלו.", hold=0.3),
    P("מצב גדול שבנוי מאזורים כאלה נקרא AND: מסך **וגם** רשת, באותו רגע.", do=show("c6"),
      say="מצב גדול שבנוי מאזורים כאלה נקרא אֶנְד: מסך וגם רשת, באותו רגע."),
    P("כלומר, בתוך אזור אחד: או זה או זה. ובין האזורים: גם וגם.", do=show("c7")),
], stage=A.copy("an", shown=("on", "ls", "i1", "lock", "open", "ti", "t1", "t2")),
   panel=st.card("c5", "ex", "נעול + <span dir=\"ltr\">Wi-Fi</span> · פתוח + סלולרי · כל צירוף")
         + st.card("c6", "rule", "🔑 <b>AND</b>: אזור המסך <b>וגם</b> אזור הרשת, באותו רגע")
         + st.card("c7", "rule", "🔑 בתוך אזור: או · בין אזורים: גם וגם"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: תרשים מצבים, שבמבחן נקרא תרשים מיצוב, שונה ממכונת מצבים רגילה על ידי מה?"),
    P("במכונת מצבים רגילה, כמו הרמזור, המערכת נמצאת **במצב אחד** בכל רגע."),
    P("תרשים המצבים הוסיף את מה שראינו בטלפון: שני אזורים שרצים בו זמנית.", do=show("an2-rd")),
    P("זה המקבול: היכולת לתאר מצבים מקבילים. וזו התשובה.", do=show("q-ok-0"), hold=0.3),
    P("״שאינו שומר מצב״ שגוי: כל הרעיון של תרשים מצבים הוא לשמור באיזה מצב המערכת נמצאת.", do=show("q-x-2", "q-n-2")),
    P("״רק סדרתי״ שגוי: זה בדיוק ההפך. סדרתי זו מכונת המצבים הרגילה.", do=show("q-x-3", "q-n-3")),
    P("״אין בו מצבים אלא מיצובים״ שגוי: יש בו מצבים. מיצוב הוא רק השם בעברית.", do=show("q-x-4", "q-n-4")),
    P("ומכיוון ששלוש טענות שגויות, ״כל התשובות נכונות״ נופלת.", do=show("q-x-1", "q-n-1"), hold=0.3),
    P("המלכודת: המילה ״מיצוב״ נשמעת כמו משהו אחר. זה פשוט תרשים מצבים.", do=show("x-t"), hold=0.5),
], stage=w.stack(A.copy("an2", reveal=True, keep=("rd", "rl", "ro")),
                 st.card("x-t", "trap", "⚠️ ״תרשים מיצוב״ = תרשים מצבים (Statechart)"), gap=6),
   panel=w.stem(Q["id"], "תרשים מיצוב שונה ממכונת מצבים ע״י:")
         + st.options("q", OPTS, notes={1: "יש שגויות", 2: "שומר מצב", 3: "ההפך", 4: "יש מצבים"}))

recap = Scene("recap", "סיכום", [
    P("לסיכום: תרשים מצבים מתאר את כל המצבים והמעברים. יש בו מצב התחלתי, אירועים, תנאים והיסטוריה.", do=show("s-1")),
    P("אין בו הודעות בין עצמים, והוא לא מתאר תרחיש אחד.", do=show("s-2")),
    P("XOR: נעול או פתוח. AND: מסך וגם רשת, וזה מה שתרשים המצבים מוסיף. נתראה ברמה הבאה.",
      say="אֶקְס אוֹר: נעול או פתוח. אֶנְד: מסך וגם רשת, וזה מה שתרשים המצבים מוסיף. נתראה ברמה הבאה.",
      do=show("s-3"), hold=0.6),
], stage=A.copy("an3", reveal=True, keep=("rd", "rl", "ro")),
   panel=st.card("s-1", "rule", "🔑 מצבים · מעברים · התחלתי · <span dir=\"ltr\">[guard]</span> · היסטוריה")
         + st.card("s-2", "trap", "⚠️ אין הודעות, אין תרחיש")
         + st.card("s-3", "rule", "🔑 XOR: נעול או פתוח · AND: מסך וגם רשת (מקבול)"))

SCENES = [title, basics, xor, and_, exam, recap]
w.no_latin(SCENES)
VIDEO = Video("U07", "uml", "תרשים מצבים: מצבים, מעברים, XOR ו-AND", SCENES, bank={"23-EX-Q16": 0})
