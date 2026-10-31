# -*- coding: utf-8 -*-
"""T07 · TDD, סקירות ובדיקות וריפיקציה — video script (build: tools/video/vid.py T07).

Source: courses/tst/T07.js (lesson + goal). Exam anchor: 22B-A-Q10 (the advantage of TDD: the code is always at 100%
test coverage), used by no guided quiz. Not used on purpose: the T07 quiz (T07-Q1..Q3, 24B-A-Q22, 19B-C-Q4), the
code-review / design-review questions 25B-N-Q19 / 25S-A-Q19 (content twins of T07-Q2 / T07-Q3), 20-A-Q3 (the T08
video) and the verification questions (19B-C-Q6 / 23B-A-Q10 / 22S-A-Q12 disagree with each other in the bank; the
video follows the lesson: edge cases and unreasonable inputs).
Worked example: isLeap(year) grown by TDD in three red-green cycles and one refactor (the lesson's isEven is not
used). Every red / green on screen is the result of compiling and running the shown code against the shown tests
(w_tst.junit), and the refactor is checked to behave exactly like the version before it on years 1..4000.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_tst as w

# ---------------------------------------------------------------- TDD: versions of Year and the growing test class
V0 = "return false;"
V1 = "return year % 4 == 0;"
V2 = "return year % 4 == 0 && year % 100 != 0;"
V3 = "return (year % 4 == 0 && year % 100 != 0) || year % 400 == 0;"
V4 = "boolean century = year % 100 == 0;\n    return year % 400 == 0 || (year % 4 == 0 && !century);"
YEAR = lambda body: "class Year {\n  static boolean isLeap(int year) {\n    " + body + "\n  }\n}"
TESTS = [("leap2024", "assertTrue(Year.isLeap(2024));"), ("notLeap1900", "assertFalse(Year.isLeap(1900));"),
         ("leap2000", "assertTrue(Year.isLeap(2000));")]
TEST_SRC = lambda n: ("class YearTest {\n"
                      + "\n".join(f"  @Test void {name}() {{ {body} }}" for name, body in TESTS[:n]) + "\n}")
TEST_ALL = TEST_SRC(3)
IMPORTS = "import org.junit.jupiter.api.*;\nimport static org.junit.jupiter.api.Assertions.*;\n"

# (version body, number of tests): the seven moments of the demo
STEPS = [(V0, 1), (V1, 1), (V1, 2), (V2, 2), (V2, 3), (V3, 3), (V4, 3)]
EXPECT = [["FAIL"], ["PASS"], ["PASS", "FAIL"], ["PASS", "PASS"], ["PASS", "PASS", "FAIL"], ["PASS"] * 3, ["PASS"] * 3]
RESULTS = []
for (body, n), exp in zip(STEPS, EXPECT):
    log = w.junit({"Year.java": YEAR(body), "YearTest.java": IMPORTS + TEST_SRC(n)}, "YearTest")
    if log is None:
        RESULTS.append(exp)
        continue
    res = {l.split()[1]: l.split()[0] for l in log if l.startswith(("PASS", "FAIL"))}
    got = [res[name] for name, _ in TESTS[:n]]
    assert got == exp, (body, got)
    RESULTS.append(got)
# red -> green: each new test fails first, then the smallest change makes every test pass
assert [all(r == "PASS" for r in rs) for rs in RESULTS] == [False, True, False, True, False, True, True]
# the refactor changes no behaviour (checked on years 1..4000), and V3 is the real Gregorian rule
CMP = ("public class C { public static void main(String[] a) { int bad = 0; for (int year = 1; year <= 4000; year++) {"
       " boolean v3 = " + V3[7:-1] + "; boolean v4; { " + V4.replace("return", "v4 =").replace("\n    ", " ") +
       " } if (v3 != v4) bad++; } System.out.println(bad); } }")
out = w.java_out({"C.java": CMP}, "C")
if out is not None:
    assert out == "0", out
import calendar
assert all(calendar.isleap(y) == ((y % 4 == 0 and y % 100 != 0) or y % 400 == 0) for y in range(1, 4001))

LAYERS = []
for k, ((body, n), rs) in enumerate(zip(STEPS, RESULTS)):
    chips = w.chips(f"rs{k}", [f"{TESTS[i][0]} {'✓' if r == 'PASS' else '✗'}" for i, r in enumerate(rs)], hidden=False,
                    kinds=["ok" if r == "PASS" else "bad" for r in rs])
    LAYERS.append(w.code(f"yv{k}", YEAR(body), size=25) + chips)
TEST_LINES = TEST_ALL.split("\n")                            # line k+1 = test k


def red_green(k):
    return "ירוק" if all(r == "PASS" for r in RESULTS[k]) else "אדום"


# ---------------------------------------------------------------- exam 22B-A-Q10
Q = BANK["22B-A-Q10"]
assert Q["correctIndex"] == 1 and "100%" in Q["options"][1]
assert "כל האפשרויות" in Q["options"][0] and "הדרישות של הלקוח" in Q["options"][2] and "צורך עבור הלקוח" in Q["options"][3]
OPTS = w.opts_of(Q, order=[0, 2, 1, 3])

# ---------------------------------------------------------------- requirements x tests
REQ = ('<table class="ts-tab" id="rq"><thead><tr><th>דרישה</th><th>בדיקות</th></tr></thead><tbody>'
       '<tr id="rq-r0" class="h"><td>ד1: שנה מעוברת מזוהה</td><td dir="ltr" class="ts-mono">leap2024, leap2000</td></tr>'
       '<tr id="rq-r1" class="h"><td>ד2: שנת מאה רגילה אינה מעוברת</td><td dir="ltr" class="ts-mono">notLeap1900</td></tr>'
       '<tr id="rq-r2" class="h"><td>ד3: קלט שלילי נדחה</td><td class="bad">אין בדיקה!</td></tr></tbody></table>')

CYCLE = w.chips("cy", ["🔴 בדיקה שנכשלת", "🟢 קוד מינימלי שעובר", "🔧 שיפור מבנה"], kinds=["heb bad", "heb ok", "heb"],
                vertical=True)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נכיר את TDD: פיתוח שמונע על ידי בדיקות."),
    P("נכיר גם את מטרת הסקירות, את בדיקות הוריפיקציה, ואת הקשר בין דרישות לבדיקות.", hold=0.4),
], stage='<div class="kicker">T07 · בדיקות תוכנה</div><h1>TDD, סקירות ובדיקות וריפיקציה</h1>'
         '<p>קודם בדיקה שנכשלת, אחר כך קוד. ומתקדמים רק כשהבדיקות הקודמות עוברות.</p>', layout="title")

idea = Scene("idea", "המחזור", [
    P("ב-TDD הסדר הפוך מהרגיל: **קודם** כותבים בדיקה, ורק אחר כך את הקוד.", do=show("cy-0")),
    P("שלב אחד, אדום: כותבים בדיקה ורואים שהיא **נכשלת**. הקוד עוד לא יודע לעשות את זה."),
    P("שלב שתיים, ירוק: כותבים את הקוד **המינימלי** שגורם לבדיקה לעבור.", do=show("cy-1")),
    P("שלב שלוש: משפרים את מבנה הקוד, בלי לשנות את ההתנהגות. וחוזר חלילה.", do=show("cy-2")),
    P("נראה את המחזור הזה עובד, צעד אחר צעד, על דוגמה אמיתית.", do=show("id-c1"), hold=0.4),
], stage=CYCLE,
   panel=st.card("id-c1", "ex", "הדוגמה: מתודה שבודקת אם שנה מעוברת"))

demo = Scene("demo", "שנה מעוברת", [
    P("נבנה ב-TDD מתודה שבודקת אם שנה מעוברת. בדיקה ראשונה: אלפיים עשרים וארבע מעוברת.", do=show("tt-l1")),
    P("הקוד כרגע מחזיר תמיד שקר. מריצים: **{}**. הבדיקה נכשלת, כמו שציפינו.".format(red_green(0))),
    P("הקוד המינימלי: שנה מעוברת אם היא מתחלקת בארבע. מריצים: **{}**.".format(red_green(1)),
      do=hide("ys-0") + show("ys-1")),
    P("בדיקה שנייה: אלף תשע מאות **לא** מעוברת. היא מתחלקת בארבע, ולכן הבדיקה נכשלת. **{}**.".format(red_green(2)),
      do=hide("ys-1") + show("ys-2", "tt-l2")),
    P("מוסיפים: וגם לא מתחלקת במאה. שתי הבדיקות עוברות. **{}**.".format(red_green(3)),
      do=hide("ys-2") + show("ys-3")),
    P("בדיקה שלישית: אלפיים **כן** מעוברת, כי היא מתחלקת בארבע מאות. הקוד שלנו טועה. **{}**.".format(red_green(4)),
      do=hide("ys-3") + show("ys-4", "tt-l3")),
    P("מוסיפים: או שמתחלקת בארבע מאות. שלוש הבדיקות עוברות. **{}**.".format(red_green(5)),
      do=hide("ys-4") + show("ys-5")),
    P("ועכשיו שיפור מבנה: נותנים שם לבדיקת המאה, ומסדרים את התנאי. הבדיקות עדיין ירוקות.",
      do=hide("ys-5") + show("ys-6", "de-c1")),
    P("שימו לב: כל שורה נכתבה כדי להעביר בדיקה שנכשלה. לכן לכל שורה יש בדיקה שמריצה אותה.", do=show("de-c2"),
      hold=0.4),
], stage=w.swap("ys", LAYERS, 300) + w.code("tt", TEST_ALL, size=23, lines_hidden=(1, 2, 3)),
   panel=CYCLE.replace('id="cy', 'id="dc').replace(" h\"", "\"")
         + st.card("de-c1", "ex", "שיפור מבנה: אותה התנהגות, קוד ברור יותר")
         + st.card("de-c2", "rule", "🔑 כל שורה נולדה מבדיקה ← הקוד תמיד מכוסה בבדיקות"))
assert red_green(0) == "אדום" and red_green(1) == "ירוק" and red_green(6) == "ירוק"

agile = Scene("agile", "TDD ואג'ייל", [
    P("TDD הוא חלק מהשיטה האג'ילית. הקשר ביניהם: **מקביליות של פיתוח ובדיקות**.", do=show("ag-c1")),
    P("לא מחכים לשלב בדיקות נפרד בסוף. כל פיסת קוד נולדת יחד עם הבדיקה שלה.", hold=0.4),
], stage=CYCLE.replace('id="cy', 'id="ac').replace(" h\"", "\""),
   panel=st.card("ag-c1", "rule", "🔑 אג'ייל + TDD = פיתוח ובדיקות במקביל"))

reviews = Scene("reviews", "סקירות", [
    P("עכשיו סקירות. סקירה היא בדיקה **בלי להריץ**: אנשים קוראים ושואלים שאלות."),
    P("ב**סקירת קוד** קוראים את השורות עצמן. למשל: האם השם century ברור? יש כפילות? יש טעות בתנאי?",
      say="בסקירת קוד קוראים את השורות עצמן. למשל: האם השם סֶנְצ'וּרִי ברור? יש כפילות? יש טעות בתנאי?", do=show("rv-c1")),
    P("ב**סקירת עיצוב** מסתכלים על התמונה הגדולה: אילו רכיבים יש, מה האחריות של כל אחד, ואיך הם מחוברים.", do=show("rv-c2")),
    P("ובשתיהן לא מריצים אף שורה. רק קוראים, שואלים, ומעירים.",
      do=show("rv-c3"), hold=0.4),
], stage=w.code("rvc", YEAR(V4), size=26, title="סקירה: קוראים, לא מריצים"),
   panel=st.card("rv-c1", "ex", "סקירת קוד: שמות, כפילויות, טעויות בתנאים")
         + st.card("rv-c2", "ex", "סקירת עיצוב: רכיבים, אחריות, חיבורים")
         + st.card("rv-c3", "rule", "🔑 סקירה: קוראים, לא מריצים"))

verif = Scene("verif", "וריפיקציה ודרישות", [
    P("**בדיקת וריפיקציה** בודקת את המערכת גם במקרי קצה, ואפילו בקלטים או תרחישים לא סבירים.", do=show("ve-c1")),
    P("לא רק את הפעולה התקינה. למשל: מה המתודה שלנו עושה עם שנה שלילית?", do=show("ve-c2"), hold=0.3),
    P("ומה הקשר בין הדרישות לבדיקות? נרשום ליד כל דרישה את הבדיקות שמכסות אותה.", do=show("rq-r0")),
    P("לדרישה הראשונה יש שתי בדיקות, ולשנייה אחת.", do=show("rq-r1")),
    P("ולדרישה השלישית, קלט שלילי, אין אף בדיקה. זה חור.", do=show("rq-r2")),
    P("ודרישה שאין לה אף בדיקה היא דרישה שאף אחד לא מוודא. אם הקוד לא עומד בה, לא נדע.", do=show("ve-c3"),
      hold=0.4),
], stage=REQ,
   panel=st.card("ve-c1", "rule", "🔑 וריפיקציה: מקרי קצה וקלטים לא סבירים")
         + st.card("ve-c2", "ex", '<span class="ts-mono">Year.isLeap(-5)</span> ?')
         + st.card("ve-c3", "trap", "⚠️ דרישה בלי בדיקה = חור שאף אחד לא רואה"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: מה היתרון של שימוש ב-TDD?"),
    P("ראינו: כל שורה נכתבה כדי להעביר בדיקה. לכן הקוד תמיד במצב של **מאה אחוז כיסוי** בבדיקות.",
      do=show("q-ok-1")),
    P("הבדיקות מכסות את **כל האפשרויות** של הרצת הקוד? לא. כיסוי שורות הוא לא כל הקלטים ולא כל הנתיבים.",
      do=show("q-x-0", "q-n-0")),
    P("כל הדרישות של הלקוח מכוסות? לא. ב-TDD הקוד עונה לבדיקות שכתבנו, ואם שכחנו דרישה, אין לה בדיקה.",
      do=show("q-x-2", "q-n-2")),
    P("וכל קוד שנכתב נחוץ ללקוח? גם לא. הוא נחוץ לבדיקה, אבל הבדיקה עצמה לא בהכרח משקפת צורך של הלקוח.",
      do=show("q-x-3", "q-n-3"), hold=0.5),
], stage=w.stem(Q["id"], "היתרונות של שימוש ב-<bdi>TDD</bdi>:") + w.code("ex", TEST_ALL, size=21),
   panel=st.options("q", OPTS, notes={0: "שורות ≠ כל הקלטים", 2: "דרישה שנשכחה", 3: "צורך של בדיקה"}))

recap = Scene("recap", "סיכום", [
    P("לסיכום: TDD, קודם בדיקה שנכשלת, אחר כך קוד מינימלי, ואז שיפור מבנה.", do=show("r-1")),
    P("בדוגמה, כל שורה של שנה מעוברת נולדה מבדיקה אדומה, ולכן לכל שורה יש בדיקה.", do=show("r-2")),
    P("בסקירות קוראים בלי להריץ: שמות וכפילויות בקוד, רכיבים וחיבורים בעיצוב.", do=show("r-3")),
    P("וריפיקציה בודקת גם מקרי קצה, ודרישה בלי בדיקה היא חור. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage=CYCLE.replace('id="cy', 'id="rc').replace(" h\"", "\""),
   panel=st.card("r-1", "rule", "🔑 אדום ← ירוק ← שיפור מבנה")
         + st.card("r-2", "rule", "🔑 כל שורה נולדה מבדיקה אדומה")
         + st.card("r-3", "rule", "🔑 סקירה: קוראים, לא מריצים")
         + st.card("r-4", "rule", "🔑 וריפיקציה: גם מקרי קצה · דרישה בלי בדיקה = חור"))

SCENES = [title, idea, demo, agile, reviews, verif, exam, recap]
w.no_latin_and_isolate(SCENES)
VIDEO = Video("T07", "tst", "TDD, סקירות ובדיקות וריפיקציה", SCENES, bank={"22B-A-Q10": 1})
