# -*- coding: utf-8 -*-
"""U02 · תרשים מחלקות: מה הוא ואיך מסמנים קשרים — video script (build: tools/video/vid.py U02).

Source: courses/uml/U02.js (lesson + goal: what a class diagram is for; the notation of inheritance, association,
aggregation and composition). Exam anchor: 23-EX-Q13 ("composition is drawn as ..." -> all the other answers are
wrong), which no guided quiz uses; its twin 25-EX-Q8 is not used anywhere either.
Every relation shown is decided by the course checker's rule (w_uml.CHK.relation_for: is-a -> inheritance, part dies
with the whole -> composition, part lives on -> aggregation) and drawn with CHK.SYMBOL's marker.
Avoided on purpose: the U02 quiz items (inheritance notation, Car/Engine, "what can a class diagram help with",
Team/Player, 23-EX-Q11) and their twin 25-EX-Q6; the lesson's own pairs (Animal/Dog, Order/OrderLine, Team/Player,
User/Account); 26CL-Q11 (boss). Worked pairs are mine: Person/Student/Course, Building/Room, Library/Book,
Email/Attachment, Playlist/Song, Square/Shape.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_uml as w

C = w.CHK
assert C.SYMBOL == {"inheritance": "hollow_triangle", "composition": "filled_diamond", "aggregation": "hollow_diamond",
                    "dependency": "dashed_arrow"}
assert C.CLASS_RELATIONS == {"inheritance", "association", "aggregation", "composition"}
KIND = {"inheritance": "inherit", "composition": "comp", "aggregation": "aggr"}      # w_uml connector per relation

# the pairs: (whole/child, part/parent, part_lives_without_whole, is_a) -> relation by the checker
PAIRS = {"building": ("Building", "Room", False, False), "library": ("Library", "Book", True, False),
         "email": ("Email", "Attachment", False, False), "playlist": ("Playlist", "Song", True, False),
         "square": ("Square", "Shape", None, True)}
REL = {k: C.relation_for(v[2], v[3]) for k, v in PAIRS.items()}
assert REL == {"building": "composition", "library": "aggregation", "email": "composition",
               "playlist": "aggregation", "square": "inheritance"}

# exam 23-EX-Q13
Q = BANK["23-EX-Q13"]
assert Q["correctIndex"] == 1 and Q["options"][1] == "כל התשובות האחרות שגויות"
assert Q["options"][3] == "חץ עם ראש משולש" and Q["options"][2] == "חץ רגיל" and Q["options"][4] == "חץ עם ראש מחומש"
assert "תנאי על מעבר" in Q["options"][0]
assert C.SYMBOL["composition"] == "filled_diamond" and C.SYMBOL["inheritance"] == "hollow_triangle"
OPTS = w.opts_of(Q)

# ---------------------------------------------------------------- diagrams
BOOK = w.Dia("bk", 520, 330, scale=1.6)
BOOK.klass("b", 60, 20, 400, "Book", ["- title : String", "- year : int"], ["+ borrow()", "+ giveBack()"])
BOOK.ring("rn", 50, 12, 420, 58)
BOOK.ring("ra", 50, 70, 420, 86)
BOOK.ring("ro", 50, 156, 420, 86)

R1 = w.Dia("r1", 1000, 560)
R1.klass("p", 60, 20, 280, "Person", ["- name : String"], ["+ getName()"])
R1.klass("s", 60, 360, 280, "Student", ["- id : int"], hidden=True)
R1.klass("c", 660, 360, 280, "Course", ["- title : String"], hidden=True)
R1.rel("inh", "s", "p", KIND[C.relation_for(None, is_a=True)])
R1.rel("asc", "s", "c", "assoc")
R1.ring("tri", 170, 148, 60, 44, rx=12)

def whole_part(pfx, final=False):
    d = w.Dia(pfx, 1000, 560)
    for key, x in (("building", 40), ("library", 600)):
        whole, part, _, _ = PAIRS[key]
        d.klass(f"{key}-w", x, 20, 300, whole, hidden=key == "library" and not final)
        d.klass(f"{key}-p", x, 330, 300, part, hidden=key == "library" and not final)
        d.rel(f"{key}-l", f"{key}-w", f"{key}-p", KIND[REL[key]], hidden=not final)
        d.text(f"{key}-t", x + 150, 520, REL[key], cls="u-lab warn", hidden=not final)
    return d.svg(hidden=not final)



EXD = w.Dia("ex", 1000, 600)
for i, key in enumerate(("email", "playlist", "square")):
    a, b, _, _ = PAIRS[key]
    y = 20 + i * 200
    EXD.klass(f"{key}-a", 30, y, 280, a, hidden=True)
    EXD.klass(f"{key}-b", 690, y, 280, b, hidden=True)
    EXD.rel(f"{key}-l", f"{key}-a", f"{key}-b", KIND[REL[key]])
    EXD.text(f"{key}-t", 500, y + 72, REL[key], cls="u-lab warn")

# the exam stage: what each drawn shape really means
SYM = w.Dia("sy", 1000, 520)
for i, (k, kind, name) in enumerate((("tri", "inherit", "ירושה"), ("arr", "nav", "association"),
                                     ("cmp", "comp", "composition"))):
    y = 70 + i * 170
    SYM.point(f"{k}a", 120, y)
    SYM.point(f"{k}b", 560, y)
    SYM.rel(k, f"{k}a", f"{k}b", kind) if kind != "comp" else SYM.rel(k, f"{k}b", f"{k}a", kind)
    SYM.text(f"{k}t", 790, y + 10, name, cls="u-lab warn")
SYM.ring("ring", 508, 375, 70, 70, rx=35)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נכיר את תרשים המחלקות."),
    P("נראה ממה בנויה מחלקה, ואת ארבעת הקשרים: ירושה, association, aggregation ו-composition."),
    P("ובסוף נפתור שאלה ממבחן, שבה התשובה הנכונה בכלל לא ברשימה.", hold=0.4),
], stage='<div class="kicker">U02 · UML ומידול</div><h1>תרשים מחלקות: מה הוא ואיך מסמנים קשרים</h1>'
         '<p>להסביר למה משמש תרשים מחלקות, ולהכיר את הסימון של ירושה, association, aggregation ו-composition.</p>',
   layout="title")

idea = Scene("idea", "מחלקה אחת", [
    P("תרשים מחלקות הוא תרשים **מבנה**: הוא מראה ממה המערכת בנויה.", do=show("i-c1")),
    P("כל מחלקה היא מלבן עם שלושה חלקים. נסתכל על מחלקה של ספר.", do=show("bk")),
    P("למעלה: השם של המחלקה.", do=show("bk-rn")),
    P("באמצע: התכונות, כלומר הנתונים שכל ספר שומר. כאן כותרת ושנה.", do=hide("bk-rn") + show("bk-ra")),
    P("ולמטה: הפעולות, מה שאפשר לעשות עם ספר. להשאיל ולהחזיר.", do=hide("bk-ra") + show("bk-ro")),
    P("המינוס אומר פרטי, והפלוס אומר ציבורי.", do=hide("bk-ro") + show("i-c2"), hold=0.3),
    P("אבל העיקר בתרשים הוא **הקשרים** בין המחלקות. כאן מגיעים הסימנים.", do=show("i-c3")),
], stage=BOOK.svg(hidden=True),
   panel=st.card("i-c1", "rule", "🔑 תרשים מחלקות = מודל <b>מבנה</b>: מחלקות, תכונות וקשרים")
         + st.card("i-c2", "ex", "<span dir=\"ltr\">-</span> פרטי (private) · <span dir=\"ltr\">+</span> ציבורי (public)")
         + st.card("i-c3", "plain", "ועכשיו: ארבעה סוגי קשרים"))

rel1 = Scene("rel1", "ירושה ואסוסיאציה", [
    P("נתחיל במחלקה של אדם, עם שם.", do=show("r1")),
    P("סטודנט הוא **סוג של** אדם. יש לו שם, ויש לו גם מספר סטודנט.", do=show("r1-s")),
    P("זה קשר ירושה. הקו יוצא מהסטודנט ומגיע עד האדם.", do=show("r1-inh")),
    P("ובקצה שליד האדם מצויר **משולש ריק**. הוא מצביע על הכללי יותר.", do=show("r1-tri", "c1"), hold=0.3),
    P("עכשיו מחלקה של קורס. סטודנט רשום לקורסים, אבל הוא לא סוג של קורס, וגם לא מורכב מקורסים.",
      do=hide("r1-tri") + show("r1-c")),
    P("זה קשר כללי: association. מסמנים אותו בקו רגיל, בלי צורה בקצה.", do=show("r1-asc", "c2")),
    P("אפשר לשים בקצה גם חץ רגיל, כדי להראות כיוון. וזה עדיין association.", hold=0.3),
], stage=R1.svg(hidden=True),
   panel=st.card("c1", "rule", "🔑 ירושה: <span dir=\"ltr\">Student → Person</span>, <b>המשולש</b> ליד Person, הכללי יותר")
         + st.card("c2", "rule", "🔑 association = קו רגיל (או חץ רגיל): קשר כללי"))

rel2 = Scene("rel2", "הכלה: מעוין ריק ומלא", [
    P("שני הקשרים הבאים אומרים ״שלם וחלקים״. השאלה היא אחת: האם החלק חי בלי השלם?", do=show("c3")),
    P("בניין וחדרים. חדר לא קיים בלי הבניין שלו. הורסים את הבניין, והחדרים נעלמים איתו.", do=show("r2")),
    P("זו composition: קו עם **מעוין מלא**, בצד של השלם. כאן, ליד הבניין.",
      do=show("r2-building-l", "r2-building-t")),
    P("ספרייה וספרים. ספר ממשיך להתקיים גם אם הספרייה נסגרת: אפשר להעביר אותו לספרייה אחרת.",
      do=show("r2-library-w", "r2-library-p")),
    P("זו aggregation: קו עם **מעוין ריק**, וגם הוא בצד של השלם, ליד הספרייה.",
      do=show("r2-library-l", "r2-library-t", "c4"), hold=0.3),
    P("מלא חזק יותר מריק: ב-composition החלקים תלויים בחיים של השלם.", do=show("c5")),
], stage=whole_part("r2"),
   panel=st.card("c3", "plain", "האם החלק <b>חי בלי</b> השלם?")
         + st.card("c4", "rule", "🔑 מעוין <b>מלא</b> = composition · מעוין <b>ריק</b> = aggregation")
         + st.card("c5", "trap", "⚠️ המעוין תמיד בצד של <b>השלם</b>, לא של החלק"))

ex = Scene("ex", "דוגמה: איזה קשר?", [
    P("עכשיו אתם. שלושה זוגות, ולכל זוג נבחר קשר וסימון."),
    P("ראשון: הודעת דואר וקובץ מצורף. הקובץ שייך להודעה אחת, ונמחק כשמוחקים אותה.", do=show("ex", "ex-email-a", "ex-email-b")),
    P("החלק לא חי בלי השלם, ולכן composition: מעוין מלא ליד ההודעה.", do=show("ex-email-l", "ex-email-t")),
    P("שני: רשימת השמעה ושירים. מוחקים את הרשימה, והשירים נשארים בספרייה.", do=show("ex-playlist-a", "ex-playlist-b")),
    P("החלק חי בלי השלם, ולכן aggregation: מעוין ריק ליד הרשימה.", do=show("ex-playlist-l", "ex-playlist-t")),
    P("שלישי: ריבוע וצורה. כאן אין שלם וחלקים בכלל: ריבוע **הוא סוג של** צורה.", do=show("ex-square-a", "ex-square-b")),
    P("ולכן ירושה: חץ מהריבוע אל הצורה, עם משולש ריק ליד הצורה.", do=show("ex-square-l", "ex-square-t"), hold=0.3),
    P("הסדר הוא תמיד אותו סדר: קודם בודקים ״סוג של״, ורק אחר כך שואלים אם החלק חי בלי השלם.", do=show("c6")),
], stage=EXD.svg(hidden=True),
   panel=st.card("c6", "rule", "🔑 ״סוג של״ ← ירושה. אחרת: החלק מת עם השלם ← מלא. חי בלעדיו ← ריק"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: הרכבה, כלומר composition, בין מחלקות מיוצגת על ידי?"),
    P("לפני שקוראים את האפשרויות, נזכור: composition היא קו עם מעוין מלא בצד השלם.", do=show("sy", "sy-cmp", "sy-cmpt", "sy-ring")),
    P("חץ עם ראש משולש הוא ירושה, לא הרכבה.", do=show("sy-tri", "sy-trit", "q-x-3", "q-n-3")),
    P("חץ רגיל הוא association עם כיוון. גם לא.", do=show("sy-arr", "sy-arrt", "q-x-2", "q-n-2")),
    P("חץ עם ראש מחומש לא קיים בכלל בתרשים מחלקות.", do=show("q-x-4", "q-n-4")),
    P("וחץ עם תנאי על מעבר בין מצבים שייך לתרשים מצבים, לא לתרשים מחלקות.", do=show("q-x-0", "q-n-0")),
    P("המעוין המלא לא מופיע באף אפשרות. לכן התשובה: כל התשובות האחרות שגויות.", do=show("q-ok-1"), hold=0.3),
    P("המלכודת: לבחור את המשולש רק כי הוא ״סימון מיוחד״. משולש הוא תמיד ירושה.", do=show("x-t"), hold=0.5),
], stage=w.stack(SYM.svg(hidden=True), st.card("x-t", "trap", "⚠️ משולש = ירושה. הרכבה = מעוין <b>מלא</b>"), gap=6),
   panel=w.stem(Q["id"], "הרכבה (composition) בין מחלקות מיוצגת על ידי:")
         + st.options("q", OPTS, notes={0: "תרשים מצבים", 2: "association", 3: "ירושה", 4: "לא קיים"}))

recap = Scene("recap", "סיכום", [
    P("לסיכום: תרשים מחלקות הוא תרשים מבנה. כל מחלקה: שם, תכונות ופעולות.", do=show("s-1")),
    P("משולש ריק בצד האב: ירושה. קו רגיל או חץ רגיל: association.", do=show("s-2")),
    P("מעוין בצד השלם: ריק כשהחלק חי בלעדיו, ומלא כשהוא מת איתו.", do=show("s-3")),
    P("ומה שלא ראיתם כאן, כמו ראש מחומש, פשוט לא קיים. נתראה ברמה הבאה.", do=show("s-4"), hold=0.6),
], stage=whole_part("r2b", final=True),
   panel=st.card("s-1", "rule", "🔑 מחלקה: שם · תכונות · פעולות")
         + st.card("s-2", "rule", "🔑 משולש = ירושה · קו = association")
         + st.card("s-3", "rule", "🔑 מעוין מלא = composition · ריק = aggregation")
         + st.card("s-4", "trap", "⚠️ אין ראש מחומש ואין מעוין כפול"))

SCENES = [title, idea, rel1, rel2, ex, exam, recap]
w.no_latin(SCENES)
VIDEO = Video("U02", "uml", "תרשים מחלקות: מה הוא ואיך מסמנים קשרים", SCENES, bank={"23-EX-Q13": 1})
