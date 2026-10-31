# -*- coding: utf-8 -*-
"""T01 · רמות בדיקה: יחידה, שילוב, מערכת וסקירה — video script (build: tools/video/vid.py T01).

Source: courses/tst/T01.js (lesson + goal). Exam anchor: 24B-A-Q20 (what a Unit test is), used by no guided quiz.
Not used on purpose: the T01 quiz (T01-Q1..Q3, 25F0a-Q19, 21-A-Q5) and its scenario (OrderService + PaymentService),
24S-A-Q19 / 24B-B-Q24 (integration, close to T01-Q2), 24B-B-Q25 (close to T01-Q3), 21-B-Q7 (the T08 video),
and the twin 24S-A-Q20 of the anchor.
Worked examples are new: a library system (Catalog, Loans, Notifier, UserDb) for the levels, and max3(), whose three
tests pass while a tie input returns a wrong maximum. The Java is compiled and run here (javac) to prove both.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_tst as w

# ---------------------------------------------------------------- max3: three passing tests, one bug (verified)
MAX3 = """int max3(int a, int b, int c) {
  if (a > b && a > c) return a;
  if (b > a && b > c) return b;
  return c;
}"""
TESTS = [((1, 2, 3), 3), ((9, 2, 3), 9), ((1, 8, 3), 8)]
BUG = ((5, 5, 1), 5)
calls = "".join(f'System.out.println(max3({a}, {b}, {c}));' for (a, b, c), _ in TESTS + [BUG])
out = w.java_out({"M.java": "public class M {\nstatic " + MAX3 + "\npublic static void main(String[] x) {" + calls + "} }"},
                 "M")
if out is not None:
    got = [int(v) for v in out.split()]
    assert got[:3] == [e for _, e in TESTS], got          # the three tests pass
    assert got[3] == 1 and BUG[1] == max(BUG[0]) == 5      # the tie: max3(5,5,1) returns 1, the true maximum is 5
py_max3 = lambda a, b, c: a if (a > b and a > c) else (b if (b > a and b > c) else c)
assert all(py_max3(*i) == e for i, e in TESTS) and py_max3(*BUG[0]) == 1

# ---------------------------------------------------------------- exam 24B-A-Q20
Q = BANK["24B-A-Q20"]
assert Q["correctIndex"] == 1 and "יחידת תוכנה קטנה" in Q["options"][1]
assert "בו-זמנית" in Q["options"][0] and "מוסד אקדמי" in Q["options"][2] and "שגויות" in Q["options"][3]
assert "פעם אחת בלבד" in Q["options"][4]
OPTS = w.opts_of(Q, order=[0, 2, 4, 1, 3])               # "all the others are wrong" stays last, as in the app

# ---------------------------------------------------------------- the library system
BX = [
    {"key": "cat", "x": 30, "y": 170, "w": 210, "h": 90, "label": "Catalog"},
    {"key": "loan", "x": 280, "y": 170, "w": 210, "h": 90, "label": "Loans"},
    {"key": "note", "x": 530, "y": 170, "w": 210, "h": 90, "label": "Notifier"},
    {"key": "db", "x": 780, "y": 170, "w": 190, "h": 90, "label": "UserDb"},
    {"key": "cust", "x": 380, "y": 400, "w": 260, "h": 90, "label": "לקוח", "kind": "user", "hidden": True},
]
AR = [{"key": "1", "a": "loan", "b": "cat"}, {"key": "2", "a": "loan", "b": "note"}, {"key": "3", "a": "note", "b": "db"},
      {"key": "4", "a": "cust", "b": "loan", "label": "האם זה מה שביקשתי?", "lxy": (770, 345), "hidden": True}]
FR = [{"key": "u", "x": 265, "y": 150, "w": 240, "h": 130, "label": "Unit"},
      {"key": "i", "x": 265, "y": 150, "w": 490, "h": 130, "label": "Integration", "kind": "blue"},
      {"key": "s", "x": 15, "y": 140, "w": 970, "h": 150, "label": "System", "kind": "warn"}]
SYS = lambda pfx: w.boxes(pfx, BX, AR, FR, w=1000, h=520)

TBL = ('<table class="ts-tab" id="lv-tab"><thead><tr><th>רמה</th><th>מה בודקים</th></tr></thead><tbody>'
         '<tr id="lv-r0" class="h"><td><bdi>Unit</bdi></td><td>יחידה אחת</td></tr>'
         '<tr id="lv-r1" class="h"><td><bdi>Integration</bdi></td><td>כמה יחידות יחד</td></tr>'
         '<tr id="lv-r2" class="h"><td><bdi>System</bdi></td><td>המערכת כולה</td></tr>'
         '<tr id="lv-r3" class="h"><td><bdi>Acceptance</bdi></td><td>מול דרישות הלקוח</td></tr>'
         '<tr id="lv-r4" class="h"><td><bdi>Inspection</bdi></td><td>קריאה, בלי להריץ</td></tr></tbody></table>')


def TABLE(pfx, shown=()):
    """the levels table with ids {pfx}-r<k>; rows in `shown` start visible"""
    t = TBL.replace("lv-", pfx + "-")
    for k in shown:
        t = t.replace(f'id="{pfx}-r{k}" class="h"', f'id="{pfx}-r{k}"')
    return t

RES = ('<table class="ts-tab" id="mx-tab"><thead><tr><th>קלט</th><th>מצופה</th><th>התקבל</th></tr></thead><tbody>'
       + "".join(f'<tr id="mx-r{k}" class="h"><td dir="ltr">{a}, {b}, {c}</td><td>{e}</td><td class="ok">{e} ✓</td></tr>'
                 for k, ((a, b, c), e) in enumerate(TESTS))
       + f'<tr id="mx-r3" class="h"><td dir="ltr">5, 5, 1</td><td>5</td><td class="bad">1 ✗</td></tr></tbody></table>')

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נכיר את רמות הבדיקה של תוכנה."),
    P("נראה מה בודקת כל רמה, ומי עושה אותה."),
    P("נראה מתודה שעוברת את כל הבדיקות שלה, ובכל זאת טועה. ובסוף נפתור שאלה ממבחן.", hold=0.4),
], stage='<div class="kicker">T01 · בדיקות תוכנה</div><h1>רמות בדיקה: יחידה, שילוב, מערכת וסקירה</h1>'
         '<p>גודל הנבדק קובע את שם הבדיקה. ומתודה שעברה את הבדיקות שלה עדיין יכולה לטעות.</p>', layout="title")

idea = Scene("idea", "הרעיון", [
    P("נניח שבנינו מערכת לספרייה. יש בה ארבעה רכיבים.", do=show("la")),
    P("קטלוג הספרים, רכיב ההשאלות, רכיב ההתראות, ומאגר המשתמשים.",
      say="קטלוג הספרים, רכיב ההשאלות, רכיב ההתראות, ומאגר המשתמשים."),
    P("השאלה הראשונה בכל בדיקה היא: **כמה גדול** החלק שאנחנו בודקים?", do=show("id-c1")),
    P("התשובה קובעת את שם הבדיקה. נעבור על הרמות אחת אחת.", hold=0.4),
], stage=SYS("la"), panel=st.card("id-c1", "rule", "🔑 גודל הנבדק קובע את שם הבדיקה"))

unit = Scene("unit", "יחידה ושילוב", [
    P("מתחילים מהקטן: בודקים את רכיב ההשאלות **לבד**.", do=show("lb-f-u")),
    P("זו בדיקת **Unit test**: יחידת תוכנה קטנה, מחלקה אחת או מתודה אחת.", do=show("tb-r0")),
    P("את בדיקות היחידה כותבים המפתחים עצמם, בדרך כלל בספריית JUnit."),
    P("עכשיו מחברים את ההשאלות עם ההתראות. כל אחת כבר נבדקה לחוד.", do=hide("lb-f-u") + show("lb-f-i")),
    P("בודקים שהן **עובדות יחד**: השאלה שמסתיימת שולחת תזכורת.", do=show("tb-r1")),
    P("זו בדיקת **Integration test**, בדיקת שילוב.", hold=0.4),
], stage=SYS("lb"), panel=TABLE("tb"))

system = Scene("system", "מערכת וקבלה", [
    P("הרמה הבאה: **המערכת כולה**, כל הרכיבים יחד, כמו שהיא תרוץ אצל המשתמש.",
      do=show("lc-f-s", "tc-r2")),
    P("זו בדיקת **System test**, ובדרך כלל צוות הבדיקות מריץ אותה."),
    P("ואחרונה: האם המערכת עונה על מה ש**הלקוח** ביקש?", do=show("lc-b-cust", "lc-a-4")),
    P("זו בדיקת **Acceptance test**, בדיקת קבלה. הלקוח או נציג שלו בודקים מול הדרישות.", do=show("tc-r3")),
    P("שימו לב: מערכת יכולה לעבוד בלי שום תקלה, ועדיין להיכשל בבדיקת הקבלה.", do=show("sy-c1")),
    P("למשל, אם היא עושה משהו אחר ממה שהלקוח ביקש.", hold=0.4),
], stage=SYS("lc"), panel=TABLE("tc", (0, 1)) + st.card("sy-c1", "trap", "⚠️ עובדת ≠ עונה על הדרישות"))

zero = Scene("zero", "עבר = תקין?", [
    P("עכשיו ננסה משהו. הנה מתודה שמחזירה את המקסימום של שלושה מספרים.",
      do=show("mx")),
    P("שלוש בדיקות: אחת שבה השלישי הגדול, אחת שבה הראשון, ואחת שבה השני.", do=show("mx-r0", "mx-r1", "mx-r2")),
    P("שלושתן עוברות. נראה מושלם, נכון?", hold=0.3),
    P("ועכשיו הקלט חמש, חמש, אחת. המקסימום הוא חמש.", do=show("mx-r3")),
    P("אבל התנאי הראשון דורש ש-a גדול **ממש** מ-b, וגם התנאי השני. אף אחד לא מתקיים.",
      say="אבל התנאי הראשון דורש שהראשון יהיה גדול ממש מהשני, וגם התנאי השני דורש גדול ממש. אף אחד לא מתקיים.",
      do=show("mx-m1", "mx-m2")),
    P("אז המתודה מחזירה את השלישי, **אחת**. שגיאה, שאף אחת משלוש הבדיקות לא תפסה.", do=show("mx-m3")),
    P("שלוש הבדיקות בדקו שלושה מקרים, ובהם המתודה באמת עובדת. אבל הן לא בדקו את כל המקרים.", do=show("ze-c1")),
    P("ועל מקרה שאף בדיקה לא ניסתה, הבדיקות לא אומרות לנו כלום.", hold=0.4),
], stage=w.code("mx", MAX3, hidden=True, size=30) + RES,
   panel=st.card("ze-c1", "rule", "🔑 שלוש בדיקות עברו = שלושה מקרים עובדים. לא כל המקרים"))

insp = Scene("insp", "סקירה", [
    P("יש עוד רמה אחת, שלא מריצה כלום: **Inspection**, סקירה.", do=show("td-r4")),
    P("בסקירה אנשים **קוראים** את הקוד או את המסמכים, בלי להריץ אותם.", do=show("in-c1")),
    P("סוקרת שקוראת את המתודה שלנו יכולה לשאול: ומה אם שני מספרים שווים?", do=show("in-m1", "in-m2")),
    P("וכך למצוא את השגיאה בלי בדיקה אחת שרצה.", hold=0.4),
], stage=w.code("in", MAX3, size=30),
   panel=TABLE("td", (0, 1, 2, 3))
         + st.card("in-c1", "rule", "🔑 Inspection = קוראים, <b>לא מריצים</b>"))

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו שאלה ממבחן: מהי המשמעות של בדיקת יחידה?"),
    P("בדיקת יחידה היא בדיקה של **יחידת תוכנה קטנה**: מחלקה, או מתודה.", do=show("q-ok-1")),
    P("המלכודת כאן היא המילה **יחידה**. היא לא אומרת פעם יחידה.", do=show("q-x-4", "q-n-4")),
    P("אז לבצע בדיקה פעם אחת בלבד, זה לא הפירוש. בדיקת יחידה מריצים שוב ושוב."),
    P("וגם לא שתי בדיקות בבת אחת. זה משחק מילים, לא הגדרה.", do=show("q-x-0", "q-n-0")),
    P("ויחידה של מוסד אקדמי? יחידה כאן היא חלק **בתוכנה**, לא מחלקה באוניברסיטה.", do=show("q-x-2", "q-n-2")),
    P("ומכיוון שיש תשובה נכונה, האפשרות שכל התשובות האחרות שגויות נופלת.", do=show("q-x-3"), hold=0.5),
], stage=w.stem(Q["id"], "מהי המשמעות של בדיקת יחידה (<bdi>Unit Test</bdi>)?"),
   panel=st.options("q", OPTS, notes={4: "פעם יחידה?", 0: "משחק מילים", 2: "לא תוכנה"}))

recap = Scene("recap", "סיכום", [
    P("לסיכום: יחידה אחת, **Unit**. כמה יחידות יחד, **Integration**.", do=show("r-1")),
    P("המערכת כולה, **System**. מול הלקוח והדרישות, **Acceptance**.", do=show("r-2")),
    P("קוראים בלי להריץ, **Inspection**.", do=show("r-3")),
    P("וזכרו את המקסימום: שלוש בדיקות עברו, והבאג נשאר. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage=TABLE("te", (0, 1, 2, 3, 4)),
   panel=st.card("r-1", "rule", "🔑 <bdi>Unit</bdi> ← <bdi>Integration</bdi>")
         + st.card("r-2", "rule", "🔑 <bdi>System</bdi> ← <bdi>Acceptance</bdi>")
         + st.card("r-3", "rule", "🔑 <bdi>Inspection</bdi>: בלי הרצה")
         + st.card("r-4", "trap", "⚠️ <span class='ts-mono'>max3(5, 5, 1)</span>: עבר 3 בדיקות, ועדיין טועה"))

SCENES = [title, idea, unit, system, zero, insp, exam, recap]
w.no_latin_and_isolate(SCENES)
VIDEO = Video("T01", "tst", "רמות בדיקה: יחידה, שילוב, מערכת וסקירה", SCENES, bank={"24B-A-Q20": 1})
