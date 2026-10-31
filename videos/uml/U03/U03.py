# -*- coding: utf-8 -*-
"""U03 · תרשים מחלקות: ריבוי, קשרים ובחירת מחלקות — video script (build: tools/video/vid.py U03).

Source: courses/uml/U03.js (lesson + goal: multiplicity -> structure in code, which relations a class diagram has,
choosing classes from a system description). Exam anchor: 26B-A-Q12 (IT-support system: the classes used when a user
reports a fault -> User, Ticket, TicketService, AIClassificationService), which no guided quiz uses and which has no
twin in the bank. Every multiplicity -> container verdict comes from the course checker (w_uml.CHK.container).
Avoided on purpose: the U03 quiz items (25S-A-Q16 1..*, 25F0b-Q15 1..10, Course/Lab 2..4, the four-relations list,
the online-shop class pick), 24S-A-Q12 (boss), 25F0a-Q11 (U09 video), 21S-B-Q1 / 21-B-Q1 (1..* -> dynamic structure,
too close to the 25S-A-Q16 quiz item). Worked multiplicities are mine (1..40, 0..*, 0..1), and the class pick is a
greenhouse sensor logger of my own (not a shop: the U03-Q3 quiz item is a shop).
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_uml as w

C = w.CHK
MULT = [("g", "Garage", "ParkingSpot", "1..40", "comp"), ("p", "Playlist", "Song", "0..*", "aggr"),
        ("h", "Person", "Passport", "0..1", "assoc")]
CONT = {k: C.container(m) for k, _, _, m, _ in MULT}
assert CONT == {"g": "array", "p": "list", "h": "field"}
assert C.CLASS_RELATIONS == {"inheritance", "association", "aggregation", "composition"}
assert C.USECASE_RELATIONS == {"include", "extend"} and not (C.CLASS_RELATIONS & C.USECASE_RELATIONS)

# the greenhouse pick: what the system stores and what it does are classes; things of the physical world it does not
# manage, network infrastructure and a mere attribute value are not
CINEMA = {"Sensor": "entity", "Reading": "entity", "Alert": "entity", "ReadingService": "service",
          "AlertNotifier": "service", "Plant": "world", "Cable": "world", "Router": "infra", "Celsius": "value"}
PICK = [n for n, k in CINEMA.items() if k in ("entity", "service")]
assert PICK == ["Sensor", "Reading", "Alert", "ReadingService", "AlertNotifier"]

# exam 26B-A-Q12
Q = BANK["26B-A-Q12"]
assert Q["correctIndex"] == 4 and Q["options"][4] == "User, Ticket, TicketService, AIClassificationService"
assert Q["options"][0] == "Buyer, Ticket, Dashboard, Logger" and Q["options"][1] == "User, Database, Screen, Logger"
assert Q["options"][3] == "User, Printer, TicketService, EmailSender" and Q["options"][2] == "כל התשובות האחרות שגויות"
assert "שירות סיווג טקסט" in Q["question"] and "קליטת קריאות שירות" in Q["question"]
assert "Printer" not in Q["question"] and "Email" not in Q["question"] and "Buyer" not in Q["question"]
OPTS = w.opts_of(Q)

# ---------------------------------------------------------------- diagrams
MD = w.Dia("md", 1000, 600)
for i, (k, a, b, m, kind) in enumerate(MULT):
    y = 30 + i * 200
    MD.klass(f"{k}a", 30, y, 260, a, hidden=True)
    MD.klass(f"{k}b", 690, y, 280, b, hidden=True)
    MD.rel(f"{k}l", f"{k}a", f"{k}b", kind)
    MD.text(f"{k}m", 640, y - 2, m, cls="u-lab warn", size=32)
    MD.ring(f"{k}r", 590, y - 40, 100, 52, rx=14)
CODE = {"g": "class Garage {\n  ParkingSpot[] spots = new ParkingSpot[40];\n}",
        "p": "class Playlist {\n  List<Song> songs = new ArrayList<>();\n}",
        "h": "class Person {\n  Passport passport;   // null = none\n}"}
CODE_PANEL = w.stack(*[w.code(f"cd-{k}", CODE[k]) for k, *_ in MULT], gap=16)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נלמד לקרוא את המספרים שעל הקווים בתרשים מחלקות, ולתרגם אותם לקוד."),
    P("ואחר כך נלמד לבחור מחלקות מתוך תיאור של מערכת."),
    P("ובסוף נפתור שאלה ממבחן על מערכת תמיכה חכמה.", hold=0.4),
], stage='<div class="kicker">U03 · UML ומידול</div><h1>תרשים מחלקות: ריבוי, קשרים ובחירת מחלקות</h1>'
         '<p>לתרגם ריבוי (1..*, 1..10) למבנה בקוד, לדעת אילו קשרים קיימים בתרשים מחלקות, ולבחור מחלקות מתיאור מערכת.</p>',
   layout="title")

mult = Scene("mult", "ריבוי ← מבנה בקוד", [
    P("ריבוי כתוב ליד קצה של קשר, ואומר כמה אובייקטים משתתפים בו."),
    P("והוא קובע איך המחלקה השלמה מחזיקה את החלקים בקוד.", hold=0.2),
    P("חניון ומקומות חנייה. ליד מקום החנייה כתוב: אחת עד ארבעים.", do=show("md-ga", "md-gb", "md-gl", "md-gm", "md-gr"),
      say="חניון ומקומות חנייה. ליד מקום החנייה כתוב: אחת עד ארבעים."),
    P("יש חסם עליון קבוע, ארבעים. לכן מספיק **מערך** בגודל ארבעים.", do=show("cd-g")),
    P("רשימת השמעה ושירים. ליד השיר כתוב: אפס עד כוכבית.", do=hide("md-gr") + show("md-pa", "md-pb", "md-pl", "md-pm", "md-pr"),
      say="רשימת השמעה ושירים. ליד השיר כתוב: אפס עד כוכבית."),
    P("כוכבית אומרת: אין חסם עליון. הגודל משתנה, ולכן **רשימה** שגדלה לפי הצורך.", do=show("cd-p")),
    P("ואדם ודרכון. ליד הדרכון כתוב: אפס עד אחת.", do=hide("md-pr") + show("md-ha", "md-hb", "md-hl", "md-hm", "md-hr"),
      say="ואדם ודרכון. ליד הדרכון כתוב: אפס עד אחת."),
    P("לכל היותר דרכון אחד. אז לא צריך מבנה בכלל: **שדה** אחד, שיכול להיות ריק.", do=show("cd-h"), hold=0.3),
    P("הכלל: חסם עליון קבוע נותן מערך, כוכבית נותנת רשימה, ואחד נותן שדה.", do=hide("md-hr") + show("c2")),
    P("ושימו לב: המבנה תמיד יושב **בתוך המחלקה השלמה**, ומחזיק את החלקים."),
], stage=w.stack(MD.svg(hidden=False), gap=0),
   panel=CODE_PANEL + st.card("c2", "rule", "🔑 חסם קבוע ← מערך · <span dir=\"ltr\">*</span> ← רשימה · 1 ← שדה. "
                                       "המבנה <b>בתוך השלם</b>"))

RELS = w.grid("rl", [("a", ["ירושה, association", "<b>תרשים מחלקות</b>"]),
                     ("b", ["aggregation, composition", "<b>תרשים מחלקות</b>"]),
                     ("c", ["include, extend", "<b>Use Case</b>"]),
                     ("d", ["exclude", "<b>לא קיים</b>"])])
rels = Scene("rels", "אילו קשרים יש כאן?", [
    P("עוד דבר שבודקים במבחן: אילו קשרים בכלל קיימים בתרשים מחלקות.", do=show("rl-a")),
    P("ארבעה: ירושה ו-association, aggregation ו-composition.", do=show("rl-b")),
    P("include ו־extend הם קשרים בין Use Cases. הם לא שייכים לכאן.", do=show("rl-c"),
      say="אִינְקְלוּד ואִקְסְטֶנְד הם קשרים בין יוּז קֵייסִים. הם לא שייכים לכאן."),
    P("ו־exclude לא קיים בכלל, בשום תרשים.", do=show("rl-d", "c4"), say="ואֶקְסְקְלוּד לא קיים בכלל, בשום תרשים.", hold=0.3),
], stage=RELS,
   panel=st.card("c4", "trap", "⚠️ ריבוי מופיע על association ועל הכלה, ואין לו קשר לחץ הירושה"))

CH = "".join(w.chip(f"ch-{n}", n, "") for n in CINEMA)
pick = Scene("pick", "דוגמה: אילו מחלקות?", [
    P("עכשיו בחירת מחלקות. מערכת ניטור לחממה.", do=show("p-d")),
    P("חיישנים שולחים מדידת טמפרטורה כל דקה. השרת שומר את המדידות, ואם יש חריגה, שולח התראה דרך שירות הודעות חיצוני."),
    P("לפניכם תשעה מועמדים. מה נכנס לתרשים המחלקות של השרת?", do=show(*[f"ch-{n}" for n in CINEMA])),
    P("קודם **ישויות הנתונים**: החיישן, המדידה וההתראה. אלה הדברים שהמערכת שומרת ומנהלת.",
      do=show("ok-Sensor", "ok-Reading", "ok-Alert")),
    P("אחר כך **רכיבי השירות**: מחלקה שקולטת ושומרת מדידות, ומחלקה שפונה לשירות ההודעות.",
      do=show("ok-ReadingService", "ok-AlertNotifier")),
    P("הצמח והכבל הם דברים מהעולם הפיזי. המערכת לא שומרת עליהם שום מידע, ולכן הם לא מחלקות.", do=show("no-Plant", "no-Cable")),
    P("הנתב הוא תשתית רשת, לא לוגיקה של השרת. ומעלות צלזיוס הן רק יחידה של ערך המדידה: תכונה, לא מחלקה.",
      do=show("no-Router", "no-Celsius")),
    P("השאלה לשאול על כל מועמד: האם המערכת שומרת עליו נתונים, או מבצעת בו פעולה?", do=show("c5"), hold=0.3),
], stage=w.stack('<div id="p-d" class="card ex h">🌱 חיישנים שולחים מדידות לשרת. השרת שומר אותן, ובחריגה שולח התראה דרך שירות הודעות חיצוני.</div>',
                 '<div class="u-chips">' + CH + "</div>",
                 '<div class="u-chips">' + "".join(
                     w.chip(f"{'ok' if k in ('entity', 'service') else 'no'}-{n}", ("✓ " if k in ("entity", "service") else "✗ ") + n,
                            "ok" if k in ("entity", "service") else "bad") for n, k in CINEMA.items()) + "</div>", gap=30),
   panel=st.card("c5", "rule", "🔑 מחלקה = משהו שהמערכת <b>שומרת</b> עליו, או רכיב <b>שעושה</b> משהו. ערך של תכונה אינו מחלקה"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: מערכת תמיכה חכמה בתקלות מחשוב, עם פורטל לעובדים ושרת שפונה לשירותי בינה מלאכותית."),
    P("עובד מדווח על תקלה חדשה דרך הפורטל. אילו מחלקות ישמשו בתהליך הזה?", do=show("x-1")),
    P("לפי התיאור, השרת קולט קריאות שירות, ופונה לשירות שמסווג את סוג התקלה ואת הדחיפות.", do=show("x-2")),
    P("האפשרות עם הקונה נופלת: במערכת יש עובדים שמדווחים, לא קונים. ולוח הבקרה הוא מסך של המנהל.",
      do=show("q-x-0", "q-n-0")),
    P("האפשרות עם מסד הנתונים והמסך נופלת: המסך הוא ממשק, ומסד הנתונים הוא המקום ששומרים בו. אף אחד מהם לא לוגיקה.",
      do=show("q-x-1", "q-n-1")),
    P("האפשרות עם המדפסת נופלת: מדפסת היא חומרה, ושליחת אימייל בכלל לא מופיעה בתיאור.", do=show("q-x-3", "q-n-3")),
    P("נשארה האפשרות של המשתמש, הקריאה ושני השירותים.", do=show("q-ok-4")),
    P("המשתמש והקריאה הם הישויות, ושירות הקריאות ושירות הסיווג הם רכיבי השירות.", hold=0.3),
    P("ולכן גם ״כל התשובות האחרות שגויות״ לא נכונה.", do=show("q-x-2")),
    P("המלכודת: אפשרות שיש בה גם מחלקה טובה אחת. מספיקה מחלקה לא שייכת אחת, והאפשרות נופלת.", do=show("x-t"), hold=0.5),
], stage=w.stack(st.card("x-1", "ex", "🛠️ עובד מדווח על תקלה דרך הפורטל"),
                 st.card("x-2", "plain", "השרת: <b>קליטת קריאות שירות</b> (Tickets) · שירות ענן: <b>סיווג</b> סוג התקלה והדחיפות"),
                 st.card("x-t", "trap", "⚠️ מחלקה אחת שלא שייכת (מסך, מדפסת, ה-DB) מפילה את כל האפשרות"), gap=26),
   panel=w.stem(Q["id"], "משתמש מדווח על תקלה חדשה בפורטל. אילו מחלקות ישמשו בתהליך?")
         + st.options("q", OPTS, notes={0: "אין קונים", 1: "DB ומסך", 3: "חומרה"}))

recap = Scene("recap", "סיכום", [
    P("לסיכום: חסם עליון קבוע נותן מערך, כוכבית נותנת רשימה, ואחד נותן שדה. והכל בתוך המחלקה השלמה.", do=show("s-1")),
    P("בתרשים מחלקות יש ארבעה קשרים. include ו־extend שייכים ל-Use Case.", do=show("s-2"),
      say="בתרשים מחלקות יש ארבעה קשרים. אִינְקְלוּד ואִקְסְטֶנְד שייכים ליוּז קֵייס."),
    P("ומחלקות בוחרים לפי השאלה: האם המערכת שומרת את זה, או עושה את זה? נתראה ברמה הבאה.", do=show("s-3"), hold=0.6),
], stage=CODE_PANEL.replace('class="u-code h"', 'class="u-code"').replace('id="cd-', 'id="rc-'),
   panel=st.card("s-1", "rule", "🔑 חסם קבוע ← מערך · <span dir=\"ltr\">*</span> ← רשימה")
         + st.card("s-2", "rule", "🔑 במחלקות: משולש · קו · מעוין ריק · מעוין מלא")
         + st.card("s-3", "rule", "🔑 שומרת עליו או עושה אותו ← מחלקה"))

SCENES = [title, mult, rels, pick, exam, recap]
w.no_latin(SCENES)
VIDEO = Video("U03", "uml", "תרשים מחלקות: ריבוי, קשרים ובחירת מחלקות", SCENES, bank={"26B-A-Q12": 4})
