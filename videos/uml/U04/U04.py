# -*- coding: utf-8 -*-
"""U04 · Use Case: Actors, include ו-extend — video script (build: tools/video/vid.py U04).

Source: courses/uml/U04.js (lesson + goal: read a use-case diagram: who is an Actor, when include and when extend, what
is true about the time axis and the number of diagrams). Exam anchor: 20-A-Q4 (many use cases may be shown in several
diagrams), which no guided quiz uses; its twins 19B-B-Q16 and SP-DGM-Q13 are not used anywhere either.
include/extend come from the course checker (w_uml.CHK.uc_relation: mandatory -> include, optional -> extend);
arrows are drawn in the UML direction: include base -> included, extend extension -> base.
Avoided on purpose: the U04 quiz items (login/password include, coupon extend, the library Actor question,
26S-A-Q14, 22S-A-Q14 and its twin 23B-A-Q9 are not solved; the time-axis fact is stated once, as the lesson does),
25B-N-Q17 (boss), the lesson's payment/credit-check/coupon example. My worked system is an ATM.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_uml as w

C = w.CHK
assert C.USECASE_RELATIONS == {"include", "extend"}
# (base, other, other is mandatory for base?)
RELS = {"wd-vf": ("משיכת מזומן", "אימות כרטיס", True), "rc-wd": ("משיכת מזומן", "הדפסת קבלה", False),
        "pin-vf": ("החלפת קוד סודי", "אימות כרטיס", True), "sms-wd": ("משיכת מזומן", "התראת מסרון", False)}
KIND = {k: C.uc_relation(m) for k, (_, _, m) in RELS.items()}
assert KIND == {"wd-vf": "include", "rc-wd": "extend", "pin-vf": "include", "sms-wd": "extend"}

# exam 20-A-Q4
Q = BANK["20-A-Q4"]
assert Q["correctIndex"] == 2 and "מספר תרשימים" in Q["options"][2]
assert "בתרשים אחד" in Q["options"][0] and "use case יחיד" in Q["options"][1] and "לכל היותר 7" in Q["options"][3]
OPTS = w.opts_of(Q)

# ---------------------------------------------------------------- diagrams
D = w.Dia("d", 1000, 600)
D.boundary("sys", 180, 10, 650, 580, "כספומט", hidden=True)
D.actor("cu", 80, 200, "לקוח", hidden=True)
D.actor("bk", 925, 380, "מערכת הבנק", hidden=True)
D.usecase("wd", 350, 150, 140, 50, "משיכת מזומן", hidden=True)
D.usecase("rc", 690, 150, 120, 50, "הדפסת קבלה", hidden=True)
D.usecase("vf", 350, 470, 140, 50, "אימות כרטיס", hidden=True)
D.usecase("bl", 690, 330, 120, 50, "בדיקת יתרה", hidden=True)
D.rel("cu-wd", "cu", "wd", "assoc")
D.rel("cu-bl", "cu", "bl", "assoc")
D.rel("bk-vf", "bk", "vf", "assoc")
D.rel("wd-vf", "wd", "vf", KIND["wd-vf"], lxy=(338, 300), lanchor="end")
D.rel("rc-wd", "rc", "wd", KIND["rc-wd"], lxy=(530, 94))
D.rel("bl-vf", "bl", "vf", "include", lxy=(600, 420))
D.ring("hb", 200, 95, 300, 110, rx=55)
D.ring("hi", 200, 415, 300, 110, rx=55)
D.ring("he", 565, 95, 250, 110, rx=55)

W = w.Dia("wx", 1000, 560, scale=1.05)
W.usecase("pin", 230, 90, 170, 52, "החלפת קוד סודי", hidden=True)
W.usecase("vf", 230, 450, 170, 52, "אימות כרטיס", hidden=True)
W.usecase("sms", 760, 90, 170, 52, "התראת מסרון", hidden=True)
W.usecase("wd", 760, 450, 170, 52, "משיכת מזומן", hidden=True)
W.rel("pin-vf", "pin", "vf", KIND["pin-vf"], lxy=(244, 280), lanchor="start")
W.rel("sms-wd", "sms", "wd", KIND["sms-wd"], lxy=(774, 280), lanchor="start")

TWO = w.Dia("tw", 1000, 560)
TWO.boundary("a", 20, 20, 460, 520, "כספומט: שירותי לקוח", hidden=True)
TWO.actor("ca", 90, 210, "לקוח", hidden=True)
for i, t in enumerate(("משיכת מזומן", "בדיקת יתרה", "החלפת קוד סודי")):
    TWO.usecase(f"u{i}", 320, 140 + i * 140, 140, 46, t, hidden=True)
    TWO.rel(f"l{i}", "ca", f"u{i}", "assoc")
TWO.boundary("b", 520, 20, 460, 520, "כספומט: תחזוקה", hidden=True)
TWO.actor("tc", 590, 230, "טכנאי", hidden=True)
for i, t in enumerate(("מילוי שטרות", "החלפת גליל נייר")):
    TWO.usecase(f"v{i}", 820, 190 + i * 160, 140, 46, t, hidden=True)
    TWO.rel(f"m{i}", "tc", f"v{i}", "assoc")

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נקרא תרשים Use Case: מי משתמש במערכת, ולמה.", say="בסרטון הזה נקרא תרשים יוּז קֵייס: מי משתמש במערכת, ולמה."),
    P("נבדיל בין שני הקשרים שמבלבלים הכי הרבה: include ו־extend.", say="נבדיל בין שני הקשרים שמבלבלים הכי הרבה: אִינְקְלוּד ואִקְסְטֶנְד."),
    P("ובסוף נפתור שאלה ממבחן על מספר התרשימים.", hold=0.4),
], stage='<div class="kicker">U04 · UML ומידול</div><h1>תרשים Use Case: Actor, include, extend</h1>'
         '<p>לקרוא תרשים Use Case: מי ה-Actor, מתי include ומתי extend, ומה נכון לגבי ציר הזמן ומספר התרשימים.</p>',
   layout="title")

idea = Scene("idea", "שלושה רכיבים", [
    P("נבנה תרשים של כספומט. המלבן הוא **גבול המערכת**: מה שבפנים, זה הכספומט.", do=show("d", "d-sys")),
    P("אליפסה היא Use Case: שירות שהמערכת נותנת. למשל משיכת מזומן.", do=show("d-wd"),
      say="אליפסה היא יוּז קֵייס: שירות שהמערכת נותנת. למשל משיכת מזומן."),
    P("ואיש המקל הוא Actor: גורם **חיצוני** שפועל מול המערכת. כאן, הלקוח.", do=show("d-cu", "d-cu-wd")),
    P("Actor הוא לא חייב להיות אדם. גם מערכת הבנק, שמחוץ לכספומט, היא Actor.", do=show("d-bk", "c1")),
    P("והקו בין Actor לאליפסה אומר: הוא משתמש בשירות הזה.", hold=0.3),
    P("ומה שנמצא בתוך גבול המערכת, כמו המנגנון שמוציא את השטרות, הוא לא Actor: הוא חלק מהכספומט.", do=show("c2")),
], stage=D.svg(hidden=True),
   panel=st.card("c1", "rule", "🔑 Actor = גורם <b>חיצוני</b>: אדם או מערכת אחרת")
         + st.card("c2", "trap", "⚠️ מוציא השטרות נמצא <b>בתוך</b> הכספומט, ולכן אינו Actor"))

rels = Scene("rels", "include מול extend", [
    P("עכשיו קשרים בין Use Cases. כל משיכת מזומן **חייבת** לעבור אימות כרטיס, בכל פעם.",
      do=show("d2-vf", "d2-bk-vf", "d2-hb", "d2-hi"),
      say="עכשיו קשרים בין יוּז קֵייסִים. כל משיכת מזומן חייבת לעבור אימות כרטיס, בכל פעם."),
    P("זה include. חץ מקווקו מהשירות הראשי אל השירות שהוא כולל.", do=show("d2-wd-vf", "c3"),
      say="זה אִינְקְלוּד. חץ מקווקו מהשירות הראשי אל השירות שהוא כולל."),
    P("הדפסת קבלה קורית רק אם הלקוח מבקש. היא **אופציונלית**.", do=hide("d2-hb", "d2-hi") + show("d2-rc", "d2-he")),
    P("זה extend. והחץ הפוך: מהתוספת האופציונלית אל השירות שהיא מרחיבה.", do=show("d2-rc-wd", "c4"),
      say="זה אִקְסְטֶנְד. והחץ הפוך: מהתוספת האופציונלית אל השירות שהיא מרחיבה.", hold=0.3),
    P("ובדיקת יתרה? גם היא חייבת אימות כרטיס. ולכן עוד include.", do=hide("d2-he") + show("d2-bl", "d2-cu-bl", "d2-bl-vf"),
      say="ובדיקת יתרה? גם היא חייבת אימות כרטיס. ולכן עוד אִינְקְלוּד."),
    P("כך שירות אחד, האימות, משותף לשני שירותים בלי לכתוב אותו פעמיים.", hold=0.3),
    P("ועוד שני דברים: בתרשים Use Case **אין ציר זמן**, ואין בו קשרי ירושה והכלה של מחלקות.", do=show("c5"),
      say="ועוד שני דברים: בתרשים יוּז קֵייס אין ציר זמן, ואין בו קשרי ירושה והכלה של מחלקות."),
], stage=D.copy("d2", shown=("sys", "cu", "bk", "wd", "cu-wd")),
   panel=st.card("c3", "rule", "🔑 <b>חובה</b> ← «include», מהבסיס אל הנכלל")
         + st.card("c4", "rule", "🔑 <b>אופציונלי</b> ← «extend», מהתוספת אל הבסיס")
         + st.card("c5", "trap", "⚠️ אין ציר זמן: לא קוראים מלמעלה למטה"))

ex = Scene("ex", "דוגמה: חובה או רשות?", [
    P("עכשיו אתם. שני זוגות חדשים בכספומט, ולכל זוג: include או extend?",
      say="עכשיו אתם. שני זוגות חדשים בכספומט, ולכל זוג: אִינְקְלוּד או אִקְסְטֶנְד?"),
    P("החלפת קוד סודי. אפשר להחליף קוד בלי לאמת קודם את הכרטיס?", do=show("wx", "wx-pin", "wx-vf")),
    P("לא. האימות הוא חלק חובה מהתהליך. לכן include, מהחלפת הקוד אל האימות.", do=show("wx-pin-vf"),
      say="לא. האימות הוא חלק חובה מהתהליך. לכן אִינְקְלוּד, מהחלפת הקוד אל האימות."),
    P("התראת מסרון אחרי משיכה. היא נשלחת רק ללקוחות שנרשמו לשירות.", do=show("wx-sms", "wx-wd")),
    P("זה תנאי, לא חובה. לכן extend, מההתראה אל המשיכה.", do=show("wx-sms-wd", "c6"),
      say="זה תנאי, לא חובה. לכן אִקְסְטֶנְד, מההתראה אל המשיכה.", hold=0.3),
    P("השאלה לשאול: האם השירות הראשי **תמיד** מפעיל את השני? כן, include. רק לפעמים, extend.", do=show("c7"),
      say="השאלה לשאול: האם השירות הראשי תמיד מפעיל את השני? כן, אִינְקְלוּד. רק לפעמים, אִקְסְטֶנְד."),
], stage=W.svg(hidden=True),
   panel=st.card("c6", "ex", "החלפת קוד ← «include» ← אימות · התראה ← «extend» ← משיכה")
         + st.card("c7", "rule", "🔑 <b>תמיד</b> = include · <b>לפעמים, בתנאי</b> = extend"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: מה נכון לגבי תרשים Use Case?", say="שאלה ממבחן: מה נכון לגבי תרשים יוּז קֵייס?"),
    P("לכספומט יש שירותים ללקוח, ויש גם שירותי תחזוקה לטכנאי.", do=show("tw")),
    P("אפשר לצייר אותם בתרשים אחד גדול. אבל אפשר גם לפצל לשני תרשימים, אחד לכל קבוצה.",
      do=show("tw-a", "tw-ca", *[f"tw-u{i}" for i in range(3)], *[f"tw-l{i}" for i in range(3)])),
    P("זו אותה מערכת, בשני תרשימים, וכל אחד ברור יותר.",
      do=show("tw-b", "tw-tc", *[f"tw-v{i}" for i in range(2)], *[f"tw-m{i}" for i in range(2)]), hold=0.3),
    P("לכן ״כל ה-Use Cases בתרשים אחד״ שגוי: זה לא חובה.", do=show("q-x-0", "q-n-0"),
      say="לכן: כל היוּז קֵייסִים בתרשים אחד, שגוי: זה לא חובה."),
    P("״Use Case יחיד בכל תרשים״ שגוי: בתרשים אחד יש בדרך כלל כמה שירותים.", do=show("q-x-1", "q-n-1"),
      say="יוּז קֵייס יחיד בכל תרשים, שגוי: בתרשים אחד יש בדרך כלל כמה שירותים."),
    P("ו״לכל היותר שבעה בתרשים״ שגוי: אין בשפה מגבלה כזו.", do=show("q-x-3", "q-n-3"),
      say="ולכל היותר שבעה בתרשים, שגוי: אין בשפה מגבלה כזו."),
    P("התשובה: כשיש הרבה Use Cases, אפשר להציג אותם בכמה תרשימים.", do=show("q-ok-2"),
      say="התשובה: כשיש הרבה יוּז קֵייסִים, אפשר להציג אותם בכמה תרשימים.", hold=0.3),
    P("המלכודת: מספר שנשמע הגיוני, כמו שבע. בשאלות כאלה, מספר קבוע הוא כמעט תמיד מסיח.", do=show("x-t"), hold=0.5),
], stage=w.stack(TWO.svg(hidden=True), st.card("x-t", "trap", "⚠️ אין מגבלה על מספר היוז קייסים בתרשים"), gap=8),
   panel=w.stem(Q["id"], "בתרשים use case:")
         + st.options("q", OPTS, notes={0: "לא חובה", 1: "יכולים להיות כמה", 3: "אין מגבלה"}))

recap = Scene("recap", "סיכום", [
    P("לסיכום: Actor הוא גורם חיצוני, אדם או מערכת. האליפסות הן השירותים.", do=show("s-1")),
    P("חובה, תמיד: include, מהבסיס אל הנכלל. אופציונלי, בתנאי: extend, מהתוספת אל הבסיס.", do=show("s-2"),
      say="חובה, תמיד: אִינְקְלוּד, מהבסיס אל הנכלל. אופציונלי, בתנאי: אִקְסְטֶנְד, מהתוספת אל הבסיס."),
    P("אין ציר זמן, והרבה Use Cases מותר לפצל לכמה תרשימים. נתראה ברמה הבאה.", do=show("s-3"),
      say="אין ציר זמן, והרבה יוּז קֵייסִים מותר לפצל לכמה תרשימים. נתראה ברמה הבאה.", hold=0.6),
], stage=D.copy("d3", shown=[k for k in ("sys", "cu", "bk", "wd", "rc", "vf", "bl", "cu-wd", "cu-bl", "bk-vf", "wd-vf", "rc-wd", "bl-vf")]),
   panel=st.card("s-1", "rule", "🔑 Actor = חיצוני · אליפסה = שירות")
         + st.card("s-2", "rule", "🔑 include = חובה · extend = בתנאי")
         + st.card("s-3", "rule", "🔑 אין ציר זמן · מותר כמה תרשימים"))

SCENES = [title, idea, rels, ex, exam, recap]
w.no_latin(SCENES)
VIDEO = Video("U04", "uml", "תרשים Use Case: Actor, include, extend", SCENES, bank={"20-A-Q4": 2})
