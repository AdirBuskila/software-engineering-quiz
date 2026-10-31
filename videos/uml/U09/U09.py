# -*- coding: utf-8 -*-
"""U09 · מבחן גמר: UML ומידול (boss) — exam walkthrough (build: tools/video/vid.py U09).

Source: courses/uml/U09.js (boss: the whole course in one table). A boss video walks through exam questions that the
boss quiz does not use: 23-EX-Q12 (association can be drawn in all the listed ways), 26S-A-Q15 (the missing mark in
a user/Server/myDB sequence diagram -> activate the Server), 25F0a-Q11 (call-center server classes -> validation,
cloud connection, DB saving). None is a guided-quiz item (the gate checks ids); twins checked: 25-EX-Q7 has a
different answer and is not used; 24B-A-Q26 (same figure, missing returns) is not used.
Facts from the course checker: CHK.CLASS_RELATIONS, CHK.SEQ_NOTATION, CHK.missing_returns.
Avoided on purpose: the six boss items (25F0a-Q15, 24B-A-Q18, 26CL-Q11, 24B-B-Q16, 25B-N-Q17, 24S-A-Q12) and every
level quiz item; no lesson example is reused.
Bank note: 26S-A-Q15's explanation calls response messages optional; the video gives the stronger reason that both
response options have the wrong order or direction.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_uml as w

C = w.CHK
assert {"association", "aggregation", "composition"} <= C.CLASS_RELATIONS
assert "activation" in C.SEQ_NOTATION and "return" in C.SEQ_NOTATION
assert C.missing_returns([("user", "Server", "save data"), ("Server", "myDB", "save data")]) == [("myDB", "Server"), ("Server", "user")]

Q1, Q2, Q3 = BANK["23-EX-Q12"], BANK["26S-A-Q15"], BANK["25F0a-Q11"]
assert Q1["correctIndex"] == 4 and Q1["options"][4] == "כל התשובות נכונות"
assert [Q1["options"][k] for k in range(4)] == ["חץ רגיל עם כוכבית ליד קצה אחד", "קטע קו (linear segment) רגיל ללא ראש חץ",
                                               "חץ רגיל חד-כיווני", "חץ רגיל אשר בקצה השני קיים מעוין"]
assert Q2["correctIndex"] == 2 and "activate ל-Server" in Q2["options"][2] and Q2["image"] == "images/exams/26S-A-Q15.png"
assert "activate ל-User" in Q2["options"][0] and "לפני הפנייה ל-DB" in Q2["options"][1] and "מה-DB למשתמש" in Q2["options"][4]
assert Q3["correctIndex"] == 1 and Q3["options"][1].startswith("מחלקת ולידציה")
assert "Text to Speech" in Q3["options"][3] and "Speech to Text" in Q3["options"][4] and "LLM" in Q3["options"][2]
assert "לבצע ולידציה על קבצי השמע" in Q3["question"] and "פונה לשירותי ענן" in Q3["question"]

# ---------------------------------------------------------------- Q1 stage: four drawings, all associations
AS = w.Dia("as", 1000, 560)
for i, (k, kind, mb, note) in enumerate((("a0", "nav", "*", "חץ + כוכבית"), ("a1", "assoc", None, "קו בלי ראש"),
                                         ("a2", "nav", None, "חץ חד כיווני"), ("a3", "aggr", None, "קו עם מעוין"))):
    y = 70 + i * 135
    AS.klass(f"{k}x", 20, y - 25, 180, "A", hidden=True)
    AS.klass(f"{k}y", 560, y - 25, 180, "B", hidden=True)
    AS.rel(k, f"{k}x", f"{k}y", kind, mb=mb)
    AS.text(f"{k}t", 870, y + 9, note, cls="u-lab warn")
AS.ring("dia", 190, 70 + 3 * 135 - 30, 70, 60, rx=24)

title = Scene("title", "", [
    P("זה מבחן הגמר של קורס ה־UML. נפתור יחד שלוש שאלות אמיתיות מהמבחנים."),
    P("אחת על תרשים מחלקות, אחת על תרשים רצף, ואחת על בחירת מחלקות מתוך תיאור מערכת."),
    P("ובכל אחת נמצא את המלכודת.", hold=0.4),
], stage='<div class="kicker">U09 · UML ומידול</div><h1>מבחן גמר: UML ומידול</h1>'
         '<p>שלוש שאלות אמיתיות מהמבחנים, פתורות צעד אחר צעד: סימון association, הסימון החסר בתרשים רצף, '
         'ובחירת מחלקות לשרת.</p>', layout="title")

q1 = Scene("q1", "שאלה 1: association", [
    P("שאלה ראשונה: קישור, כלומר association, בין מחלקות יכול להיות מיוצג על ידי?"),
    P("association היא הקשר **הכללי** בין מחלקות. נבדוק כל ציור.", do=show("as")),
    P("קו רגיל, בלי ראש בכלל: זו הצורה הבסיסית.", do=show("as-a1x", "as-a1y", "as-a1", "as-a1t", "q1-ok-1")),
    P("חץ רגיל לכיוון אחד: association עם כיוון ניווט. גם נכון.", do=show("as-a2x", "as-a2y", "as-a2", "as-a2t", "q1-ok-2")),
    P("חץ עם כוכבית ליד הקצה: הכוכבית היא ריבוי, ״הרבה״. עדיין association.",
      do=show("as-a0x", "as-a0y", "as-a0", "as-a0t", "q1-ok-0")),
    P("וקו עם מעוין בקצה? aggregation ו-composition הן **סוגים מיוחדים** של association: אותו קו, עם מעוין בצד השלם.",
      do=show("as-a3x", "as-a3y", "as-a3", "as-a3t", "as-dia", "q1-ok-3")),
    P("כל ארבעת הציורים הם association, ולכן התשובה: כל התשובות נכונות.", do=hide("as-dia") + show("q1-ok-4"), hold=0.3),
    P("המלכודת: לחשוב שמעוין הוא ״לא association״. הכלה היא סוג של association. רק המשולש, הירושה, הוא קשר אחר.",
      do=show("t1")),
], stage=w.stack(AS.svg(hidden=True), st.card("t1", "trap", "⚠️ מעוין = הכלה = סוג של association. משולש = ירושה"), gap=6),
   panel=w.stem(Q1["id"], "קישור (association) בין מחלקות יכול להיות מיוצג על ידי:") + st.options("q1", w.opts_of(Q1)))

q2 = Scene("q2", "שאלה 2: מה חסר בתרשים הרצף", [
    P("שאלה שנייה: בתרשים יש משתמש, שרת ומסד נתונים. המשתמש שולח לשרת שמירת נתונים, והשרת שולח שמירה למסד."),
    P("בהנחה שאלה כל היישויות, איזה סימון חסר?"),
    P("השרת קיבל הודעה, התחיל לעבוד, ואפילו שלח הודעה הלאה. אבל אין אצלו **סרגל הפעלה**.", do=show("rs-ring-sv")),
    P("לכן חסר activate לשרת, מהרגע שקיבל את ההודעה מהמשתמש. זו התשובה.", do=show("q2-ok-2"),
      say="לכן חסר אַקְטִיבֵייט לשרת, מהרגע שקיבל את ההודעה מהמשתמש. זו התשובה.", hold=0.3),
    P("activate למשתמש לא מתאים: המשתמש לא קיבל שום הודעה. הוא זה ששלח.", do=show("rs-ring-us", "q2-x-0", "q2-n-0"),
      say="אַקְטִיבֵייט למשתמש לא מתאים: המשתמש לא קיבל שום הודעה. הוא זה ששלח."),
    P("תשובה מהשרת למשתמש **לפני** הפנייה למסד? השרת עוד לא יודע אם השמירה הצליחה. הסדר הפוך.",
      do=hide("rs-ring-us") + show("q2-x-1", "q2-n-1")),
    P("ותשובה מהמסד ישר למשתמש? המסד לא קיבל כלום מהמשתמש. הוא עונה למי שפנה אליו: לשרת.",
      do=show("rs-ring-db", "q2-x-4", "q2-n-4")),
    P("אף אחת משתי אפשרויות התשובה לא מתאימה לתרשים. לכן ״כל התשובות שגויות״ נופלת, והחסר הוא הסרגל של השרת.",
      do=hide("rs-ring-db") + show("q2-x-3")),
    P("המלכודת: אפשרויות של תשובה שנשמעות טבעיות, אבל לא מתאימות למה שקרה בתרשים.", do=show("t2"), hold=0.3),
], stage=w.stack(st.raster("rs", "images/exams/26S-A-Q15.png", 560, (515, 456),
                           rings=[("sv", 245, 305, 60), ("us", 47, 280, 45), ("db", 442, 330, 50)]),
                 st.card("t2", "trap", "⚠️ תשובה הולכת אל מי שפנה, ורק כשהיא מוכנה"), gap=10),
   panel='<div class="u-tight">' + w.stem(Q2["id"], "בהנחה שאלה כל היישויות, מה הסימון שחסר בתרשים?")
         + st.options("q2", w.opts_of(Q2), notes={0: "הוא שלח", 1: "סדר הפוך", 4: "כיוון שגוי"}) + "</div>")

OPT3 = w.opts_of(Q3)
q3 = Scene("q3", "שאלה 3: מחלקות בשרת", [
    P("שאלה שלישית: מוקד טלפוני מבוסס בינה מלאכותית. השרת מקבל קבצי שמע מהמרכזייה, ופונה לשירותי ענן.", do=show("d1")),
    P("לפי התיאור, שרת האפליקציה עושה שלושה דברים: ולידציה על קבצי השמע, שמירת נתוני לקוחות, וחיבור לשירותי הענן.",
      do=show("d2")),
    P("ומה עושים שירותי הענן? המרת טקסט לשמע, שמע לטקסט, וניתוח טקסט. הם **חיצוניים** לשרת.", do=show("d3")),
    P("השאלה: אילו מחלקות יהיו בתרשים המחלקות של השרת?"),
    P("אפשרות שיש בה מחלקה לתרגום טקסט לשמע נופלת: התרגום קורה בענן, לא בשרת.", do=show("q3-x-3", "q3-n-3")),
    P("ומאותה סיבה גם האפשרות עם תרגום שמע לטקסט, והאפשרות עם מחלקת ניתוח טקסט.",
      do=show("q3-x-4", "q3-n-4", "q3-x-2", "q3-n-2")),
    P("נשארה האפשרות שמתאימה בדיוק לשלושת התפקידים: ולידציה, חיבור לשירותי ענן, ושמירה למסד.", do=show("q3-ok-1")),
    P("ולכן ״כל התשובות האחרות שגויות״ לא נכונה.", do=show("q3-x-0"), hold=0.3),
    P("המלכודת: לבנות מחלקה לכל יכולת שמוזכרת בתיאור. בשרת יש מחלקה רק למה שהשרת עצמו עושה.", do=show("t3"), hold=0.5),
], stage=w.stack(st.card("d1", "ex", "☎️ מרכזייה ← <b>שרת אפליקציה</b> ← שירותי ענן"),
                 st.card("d2", "rule", "השרת: <b>ולידציה</b> לקבצי שמע · <b>שמירה</b> ל-DB · <b>חיבור</b> לשירותי ענן"),
                 st.card("d3", "plain", "בענן (מחוץ לשרת): Text to Speech · Speech to Text · LLM"),
                 st.card("t3", "trap", "⚠️ מחלקה בשרת = מה שהשרת <b>עצמו</b> עושה"), gap=22),
   panel='<div class="u-tight">' + w.stem(Q3["id"], "תרשים המחלקות של שרת האפליקציה יכיל ככל הנראה את המחלקות:")
         + st.options("q3", OPT3, notes={2: "בענן", 3: "בענן", 4: "בענן"}) + "</div>")

ROWS = [("c", ["<b>Class</b>", "משולש = ירושה · מעוין = הכלה · קו = association"]),
        ("s", ["<b>Sequence</b>", "סרגל אצל מי שעובד · תשובה אל מי שקרא"]),
        ("u", ["<b>Use Case</b>", "include = תמיד · extend = רק לפעמים"]),
        ("a", ["<b>Activity</b>", "פס מפצל · פס מאחד = סנכרון"]),
        ("b", ["<b>Statechart</b>", "XOR = או · AND = אזורים במקביל"])]
recap = Scene("recap", "סיכום הקורס", [
    P("לסיכום הקורס כולו, טבלה אחת."),
    P("בתרשים המחלקות: משולש לירושה, מעוין להכלה, וקו ל-association.", do=show("m-c")),
    P("בתרשים רצף, סרגל אצל מי שעובד ותשובה אל מי שקרא. וב-Use Case, include ו-extend.", do=show("m-s", "m-u"),
      say="בתרשים רצף, סרגל אצל מי שעובד ותשובה אל מי שקרא. וביוּז קֵייס, אִינְקְלוּד ואִקְסְטֶנְד."),
    P("בתרשים פעילות, פסים מלאים מפצלים ומאחדים. ובתרשים מצבים, אזורים מקבילים.", do=show("m-a", "m-b")),
    P("בהצלחה במבחן הגמר באפליקציה, ובמבחן האמיתי.", hold=0.6),
], stage=w.grid("m", ROWS, cls="wide2"),
   panel=st.card("x", "rule", "🔑 קשרים לא עוברים בין תרשימים: include/extend רק ב-Use Case, ירושה והכלה רק במחלקות").replace(' h"', '"'))

SCENES = [title, q1, q2, q3, recap]
w.no_latin(SCENES)
VIDEO = Video("U09", "uml", "מבחן גמר: UML ומידול", SCENES, bank={"23-EX-Q12": 4, "26S-A-Q15": 2, "25F0a-Q11": 1})
