# -*- coding: utf-8 -*-
"""U08 · תרשים פעילות ובחירת התרשים המתאים — video script (build: tools/video/vid.py U08).

Source: courses/uml/U08.js (lesson + goal: what the solid bar of an activity diagram means, and choosing the diagram
that fits a need). Exam anchor: 26B-A-Q16 ("which relations can there be between activities" -> all the other
answers are wrong), which no guided quiz uses and which has no twin in the bank. The join rule is the course checker's
(w_uml.CHK.join_ready) and every need -> diagram choice comes from CHK.NEED; the diagram -> model line from CHK.MODEL.
Avoided on purpose (the join is shown with two branches, no sentence rule): the U08 quiz items (A, B, C into one solid bar; the login message order; the order process with
packing and invoice; the "what is the system built of" need), 23S-A-Q8 (U08 quiz), 25F0a-Q15 (boss), and the
lesson's order-handling example. My process is an employee onboarding; my needs are a library's users, a delivery's
states and a password reset's messages.
Note: 26B-A-Q16's key implies the control flows count as relations between activities (the bank explanation says so),
while 25F0a-Q14 keys "no relations" for a sequence diagram. The video only states what the activity diagram has.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_uml as w

C = w.CHK
INC = ["acc", "lap"]
assert not C.join_ready(["acc"], INC) and C.join_ready(["acc", "lap"], INC)
NEEDS = [("n1", "who_uses", "מי משתמש במערכת ספרייה, ואילו שירותים היא נותנת לו", "Use Case"),
         ("n2", "states", "באילו מצבים יכול להיות משלוח, ואיך הוא עובר ביניהם", "Statechart"),
         ("n3", "message_order", "סדר ההודעות בין האפליקציה, השרת ושירות הדואר, כשמאפסים סיסמה", "Sequence")]
NAME = {"usecase": "Use Case", "statechart": "Statechart", "sequence": "Sequence"}
for _, need, _, d in NEEDS:
    assert NAME[C.NEED[need]] == d
assert C.USECASE_RELATIONS == {"include", "extend"}

# exam 26B-A-Q16
Q = BANK["26B-A-Q16"]
assert Q["correctIndex"] == 3 and Q["options"][3] == "כל התשובות האחרות שגויות"
assert Q["options"][0] == "Include, Extends" and Q["options"][1] == "Extends, Exclude" and Q["options"][4] == "Include, Exclude"
assert Q["options"][2] == "אין קשרים בין היישויות ב-Activity Diagram"
OPTS = w.opts_of(Q)

# ---------------------------------------------------------------- diagram
def onboarding(pfx, final=False, hot=False):
    d = w.Dia(pfx, 1000, 560)
    hid = not final
    d.initial("i", 30, 280, hidden=hid)
    d.action("ct", 62, 245, 200, 70, "חתימת חוזה", hidden=hid)
    d.bar("fk", 300, 70, 16, 420, hidden=hid)
    for k, y, t in (("acc", 110, "פתיחת חשבון"), ("lap", 380, "הזמנת מחשב")):
        d.action(k, 365, y, 240, 70, t, hidden=hid)
        d.text(f"{k}-ok", 625, y + 16, "✓", cls="u-lab ok", size=34)
    d.bar("jn", 660, 70, 16, 420, hidden=hid, hot=hot)
    d.action("dy", 728, 245, 200, 70, "יום ראשון", hidden=hid)
    d.final("f", 965, 280, hidden=hid)
    d.rel("f0", "i", "ct", "flow", hidden=hid, hot=hot)
    d.rel("f1", "ct", "fk", "flow", hidden=hid, hot=hot)
    for k, y in (("acc", 145), ("lap", 415)):
        d.rel(f"o-{k}", "fk", k, "flow", p1=(316, y), hidden=hid, hot=hot)
        d.rel(f"j-{k}", k, "jn", "flow", p2=(660, y), hidden=hid, hot=hot)
    d.rel("f2", "jn", "dy", "flow", hidden=hid, hot=hot)
    d.rel("f3", "dy", "f", "flow", hidden=hid, hot=hot)
    d.cross("no", 668, 280, 30)
    d.ring("rf", 288, 56, 40, 448, rx=16)
    d.ring("rj", 648, 56, 40, 448, rx=16)
    return d


D = onboarding("ob")

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נכיר את תרשים הפעילות, ואת הפס המלא שבו."),
    P("ואחר כך נלמד מתכון קצר: איך בוחרים את התרשים שמתאים לצורך."),
    P("ובסוף נפתור שאלה ממבחן על הקשרים בתרשים פעילות.", hold=0.4),
], stage='<div class="kicker">U08 · UML ומידול</div><h1>תרשים פעילות ובחירת התרשים המתאים</h1>'
         '<p>להסביר מה מסמן ה-solid bar בתרשים פעילות, ולבחור את סוג התרשים המתאים לצורך שמתואר.</p>',
   layout="title")

flow = Scene("flow", "תרשים פעילות", [
    P("תרשים פעילות מתאר **תהליך**: אילו פעילויות יש בו, ובאיזה סדר. ניקח קליטה של עובד חדש.", do=show("ob", "c1")),
    P("העיגול המלא הוא ההתחלה. הפעילות הראשונה: חתימת חוזה.", do=show("ob-i", "ob-ct", "ob-f0")),
    P("ועכשיו שתי פעילויות שקורות **במקביל**: פתיחת חשבון מחשוב, והזמנת מחשב נייד.",
      do=show("ob-acc", "ob-lap")),
    P("לפניהן יש פס מלא שמפצל את הזרימה לשני מסלולים.", do=show("ob-f1", "ob-fk", "ob-o-acc", "ob-o-lap", "ob-rf")),
    P("ואחריהן עוד פס מלא, שמאחד אותן חזרה: זה ה־solid bar שהמבחן שואל עליו.",
      do=hide("ob-rf") + show("ob-jn", "ob-j-acc", "ob-j-lap", "ob-rj")),
    P("ומשם ממשיכים ליום העבודה הראשון, ולסוף התהליך: עיגול בתוך עיגול.", do=hide("ob-rj") + show("ob-f2", "ob-dy", "ob-f3", "ob-f"),
      hold=0.3),
    P("כך רואים בבת אחת את כל זרימת העבודה, מהחוזה ועד היום הראשון.", do=show("c2")),
], stage=D.svg(hidden=True),
   panel=st.card("c1", "rule", "🔑 תרשים פעילות = <b>זרימה של תהליך</b>, כולל מקביליות")
         + st.card("c2", "ex", "פס מלא אחד מפצל, פס מלא שני מאחד"))

join = Scene("join", "מה ה-solid bar אומר", [
    P("מתי העובד יכול להתחיל את היום הראשון? נריץ את התהליך."),
    P("החשבון כבר נפתח. אבל המחשב הנייד עוד בדרך.", do=show("ob2-acc-ok", "ob2-no")),
    P("העובד עומד מול הפס המאחד, ו**מחכה**. בלי מחשב אין טעם ביום ראשון.", do=show("c3")),
    P("המחשב הגיע. עכשיו גם החשבון וגם המחשב מוכנים, והזרימה עוברת את הפס.",
      do=hide("ob2-no") + show("ob2-lap-ok", "ob2-rj")),
    P("זה התפקיד של הפס המאחד: נקודת **סנכרון**. הוא פותח את המשך הדרך רק כשכל המסלולים שלו הגיעו אליו.",
      do=show("c4"), hold=0.3),
], stage=D.copy("ob2", reveal=True, keep=("acc-ok", "lap-ok", "no", "rf", "rj")),
   panel=st.card("c3", "trap", "⚠️ חשבון בלי מחשב: עדיין מחכים")
         + st.card("c4", "rule", "🔑 הפס המאחד = <b>סנכרון</b>: מחכה לחשבון <b>וגם</b> למחשב"))

ROWS = w.grid("nd", [(k, [t, f"<b>{d}</b>"]) for k, _, t, d in NEEDS], cls="wrap")
choose = Scene("choose", "איזה תרשים?", [
    P("עכשיו המתכון לבחירת תרשים: מנסחים את השאלה שרוצים לענות עליה, ובוחרים לפי הטבלה.", do=show("tb")),
    P("ראשון: מי משתמש במערכת ספרייה, ואילו שירותים היא נותנת לו. מי משתמש ולמה: תרשים Use Case.", do=show("nd-n1"),
      say="ראשון: מי משתמש במערכת ספרייה, ואילו שירותים היא נותנת לו. מי משתמש ולמה: תרשים יוּז קֵייס."),
    P("שני: באילו מצבים יכול להיות משלוח, ואיך הוא עובר ביניהם. מצבים ומעברים: תרשים מצבים.", do=show("nd-n2")),
    P("שלישי: סדר ההודעות בין האפליקציה, השרת ושירות הדואר, כשמאפסים סיסמה. הודעות לאורך זמן: תרשים רצף.",
      do=show("nd-n3"), hold=0.3),
    P("ואם רוצים להראות תהליך כזרימה של פעילויות, עם מקביליות, זה תרשים פעילות. ומבנה של מחלקות, תרשים מחלקות.",
      do=show("c6")),
    P("ומלכודת נפוצה: אפשרות שמייחסת לתרשים אחד את התפקיד של אחר. אף תרשים לא עושה הכל.", do=show("c7")),
], stage=w.stack('<div id="tb" class="u-note h">הצורך ← התרשים</div>', ROWS, gap=18),
   panel=st.card("c6", "rule", "🔑 משתמשים = Use Case · מצבים = Statechart · הודעות = Sequence · "
                              "תהליך = Activity · מבנה = Class")
         + st.card("c7", "trap", "⚠️ כל תרשים עונה על שאלה אחת. בודקים שהצורך מתאים"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: בתרשים פעילות, אילו קשרים יכולים להיות בין הפעילויות?"),
    P("נחזור לתרשים שלנו. מה מחבר בין הפעילויות? החיצים: **זרימת הבקרה**, שקובעת מה בא אחרי מה.", do=show("ob3")),
    P("יחד עם הפסים המלאים, שמפצלים ומאחדים. אלה החיבורים בין הפעילויות, ואין ביניהן שום קשר מסוג אחר."),
    P("לכן ״אין קשרים בין היישויות״ שגוי: הפעילויות מחוברות בזרימה.", do=show("q-x-2", "q-n-2")),
    P("include ו־extend הם קשרים בין Use Cases, לא בין פעילויות. שתי האפשרויות שיש בהן include נופלות.",
      do=show("q-x-0", "q-n-0", "q-x-4", "q-n-4"),
      say="אִינְקְלוּד ואִקְסְטֶנְד הם קשרים בין יוּז קֵייסִים, לא בין פעילויות. שתי האפשרויות שיש בהן אִינְקְלוּד נופלות."),
    P("והאפשרות של extend ו־exclude נופלת גם היא: exclude לא קיים בשום תרשים.", do=show("q-x-1", "q-n-1"),
      say="והאפשרות של אִקְסְטֶנְד ואֶקְסְקְלוּד נופלת גם היא: אֶקְסְקְלוּד לא קיים בשום תרשים."),
    P("נשארה התשובה: כל התשובות האחרות שגויות.", do=show("q-ok-3"), hold=0.3),
    P("המלכודת: שמות של קשרים מתרשים אחר. include ו־extend תמיד שייכים ל-Use Case.", do=show("x-t"),
      say="המלכודת: שמות של קשרים מתרשים אחר. אִינְקְלוּד ואִקְסְטֶנְד תמיד שייכים ליוּז קֵייס.", hold=0.5),
], stage=w.stack(onboarding("ob3", final=True, hot=True).svg(hidden=True),
                 st.card("x-t", "trap", "⚠️ include / extend = Use Case בלבד · exclude לא קיים"), gap=8),
   panel=w.stem(Q["id"], "בתרשים Activity Diagram, אילו קשרים יכולים להיות בין הפעילויות?")
         + st.options("q", OPTS, notes={0: "Use Case", 1: "אין exclude", 2: "יש זרימה", 4: "Use Case"}))

recap = Scene("recap", "סיכום", [
    P("לסיכום: תרשים פעילות מתאר תהליך כזרימה של פעילויות, עם מקביליות.", do=show("s-1")),
    P("פס מלא מפצל לפעילויות מקבילות, ופס מלא מאחד אותן, ומחכה לכל המסלולים שלו.", do=show("s-2")),
    P("ולבחירת תרשים: מנסחים את השאלה, ובוחרים את התרשים שעונה עליה. נתראה ברמה הבאה.", do=show("s-3"), hold=0.6),
], stage=onboarding("ob4", final=True).svg(),
   panel=st.card("s-1", "rule", "🔑 Activity = תהליך, כולל מקביליות")
         + st.card("s-2", "rule", "🔑 פס מפצל · פס מאחד = סנכרון")
         + st.card("s-3", "rule", "🔑 צורך ← תרשים, לפי השאלה"))

SCENES = [title, flow, join, choose, exam, recap]
w.no_latin(SCENES)
VIDEO = Video("U08", "uml", "תרשים פעילות ובחירת התרשים המתאים", SCENES, bank={"26B-A-Q16": 3})
