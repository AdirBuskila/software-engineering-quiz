# -*- coding: utf-8 -*-
"""T05 · תכנון מקרי בדיקה: מחלקות שקילות וערכי גבול — video script (build: tools/video/vid.py T05).

Source: courses/tst/T05.js (lesson + goal). Exam part: an original question "בסגנון מבחן" (bank={}): the testing
bank has only two boundary-value questions, 24B-B-Q26 and 26CL-Q19, and both are guided-quiz items (T05 / T08).
Not used on purpose: the T05 quiz functions shippingFee (threshold 200) and discount (500 / 1000), the lesson's
examples, and the T05-Q4 wording.
Worked examples are new: water(temp) (ice / liquid / steam, thresholds written with <= and <) and, for the exam-style
question, result(score) with a validity check (error below 0 and above 100, pass from 56).
Every class, boundary and verdict is computed: the Java on screen is run (javac) over a range of inputs and must
match the Python mirror; boundaries are the places where the output changes (w_tst.boundaries, the same scan as the
course checker's thresholds()); the mutants' distinguishing inputs are found by enumeration.
"""
from vid import P, Scene, Video, show, hide
import stage as st
import w_tst as w

LO, HI = -400, 400
RANGE = range(LO, HI + 1)

# ---------------------------------------------------------------- water(temp)
WATER = """String water(int temp) {
  if (temp <= 0) return "ice";
  if (temp < 100) return "liquid";
  return "steam";
}"""
water = lambda t: "ice" if t <= 0 else ("liquid" if t < 100 else "steam")
JRANGE = "for (int t = %d; t <= %d; t++) System.out.println(water(t));" % (LO, HI)
out = w.java_out({"W.java": "public class W {\nstatic " + WATER + "\npublic static void main(String[] a) {" + JRANGE + "} }"}, "W")
if out is not None:
    assert out.split("\n") == [water(t) for t in RANGE]
RW = w.runs(water, LO, HI)
assert [r[2] for r in RW] == ["ice", "liquid", "steam"] and len({water(t) for t in RANGE}) == 3
BW = w.boundaries(water, LO, HI)
assert BW == [(0, 1), (99, 100)]
BVALS = [0, 1, 99, 100]
DEEP = [-20, 50, 120]
assert [water(v) for v in DEEP] == ["ice", "liquid", "steam"]           # one value from each class

# the classic slip: < instead of <= (and <= instead of <). Which inputs tell the mutant from the original?
m1 = lambda t: "ice" if t < 0 else ("liquid" if t < 100 else "steam")
m2 = lambda t: "ice" if t <= 0 else ("liquid" if t <= 100 else "steam")
d1 = [t for t in RANGE if m1(t) != water(t)]
d2 = [t for t in RANGE if m2(t) != water(t)]
assert d1 == [0] and d2 == [100]
assert all(m1(v) == water(v) and m2(v) == water(v) for v in DEEP)       # the deep values pass on both mutants
assert any(m1(v) != water(v) for v in BVALS) and any(m2(v) != water(v) for v in BVALS)

# ---------------------------------------------------------------- exam-style: result(score)
RESULT = """String result(int score) {
  if (score < 0 || score > 100) return "error";
  if (score >= 56) return "pass";
  return "fail";
}"""
result = lambda s: "error" if (s < 0 or s > 100) else ("pass" if s >= 56 else "fail")
JR = "for (int t = %d; t <= %d; t++) System.out.println(result(t));" % (LO, HI)
out = w.java_out({"R.java": "public class R {\nstatic " + RESULT + "\npublic static void main(String[] a) {" + JR + "} }"}, "R")
if out is not None:
    assert out.split("\n") == [result(t) for t in RANGE]
BR = w.boundaries(result, LO, HI)
assert BR == [(-1, 0), (55, 56), (100, 101)]
RR = w.runs(result, LO, HI)
assert [r[2] for r in RR] == ["error", "fail", "pass", "error"]


def covers_all(values):
    """both sides of every boundary are tested"""
    return all({a, b} <= set(values) for a, b in BR)


EX_OPTS = [("a", [-1, 0, 55, 56, 100, 101]), ("b", [0, 56, 100]), ("c", [0, 55, 56, 100]), ("d", [-10, 30, 80, 110])]
TRUTH = {k: covers_all(v) for k, v in EX_OPTS}
assert [k for k, t in TRUTH.items() if t] == ["a"]                     # exactly one option is right
assert {result(v) for v in dict(EX_OPTS)["d"]} == {"error", "fail", "pass"}      # d: one value per region, no boundary
missing_c = [p for p in BR if not set(p) <= set(dict(EX_OPTS)["c"])]
assert missing_c == [(-1, 0), (100, 101)]                              # c forgot the validity check's two boundaries
fmt = lambda vs: '<span class="ts-mono" dir="ltr">' + ", ".join(str(v) for v in vs) + "</span>"
OPTS = [(k, fmt(v)) for k, v in EX_OPTS]

NL_W = lambda pfx, **k: w.numline(pfx, water, LO, HI, ["קרח<br><span class=\"ts-mono\">ice</span>",
                                                     "מים<br><span class=\"ts-mono\">liquid</span>",
                                                     "אדים<br><span class=\"ts-mono\">steam</span>"],
                                  points=DEEP, view=(-40, 140), w=1000, **k)
NL_R = lambda pfx, **k: w.numline(pfx, result, LO, HI, ["שגיאה", "נכשל", "עובר", "שגיאה"], view=(-25, 125), w=1000,
                                  colors=["#fb7185", "#fbbf24", "#34d399", "#fb7185"], **k)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נלמד לבחור ערכים לבדיקה."),
    P("נכיר מחלקות שקילות וערכי גבול, ונכניס באג קטן כדי לראות איזה ערך תופס אותו.", hold=0.4),
], stage='<div class="kicker">T05 · בדיקות תוכנה</div><h1>תכנון מקרי בדיקה: מחלקות שקילות וערכי גבול</h1>'
         '<p>ערך אחד מכל מחלקה, ושני ערכים סביב כל גבול: האחרון לפני, והראשון אחרי.</p>', layout="title")

idea = Scene("idea", "הרעיון", [
    P("הנה מתודה שמקבלת טמפרטורה במעלות, ומחזירה את מצב המים: קרח, מים, או אדים.", do=show("wa")),
    P("אפשר לבדוק את כל המספרים השלמים? יש יותר מארבעה מיליארד. אי אפשר.", do=show("id-c1")),
    P("אז **בוחרים** מקרי בדיקה. ויש לנו שני כלים: מחלקות שקילות, וערכי גבול.", do=show("id-c2"), hold=0.4),
], stage=w.code("wa", WATER, hidden=True, size=32),
   panel=st.card("id-c1", "trap", "⚠️ לבדוק הכל? אי אפשר")
         + st.card("id-c2", "rule", "🔑 בוחרים: מחלקות שקילות + ערכי גבול"))

classes = Scene("classes", "מחלקות שקילות", [
    P("**מחלקת שקילות** היא קבוצת קלטים שהמתודה מתייחסת אליהם אותו דבר."),
    P("כל טמפרטורה של אפס ומטה נותנת קרח. זו מחלקה אחת.", do=show("na-c0", "cl-m1")),
    P("מאחת עד תשעים ותשע: מים. מחלקה שנייה.", do=show("na-c1", "cl-m2") + hide("cl-m1")),
    P("ומאה ומעלה: אדים. מחלקה שלישית.", do=show("na-c2", "cl-m3") + hide("cl-m2")),
    P("שלוש התנהגויות, ולכן שלוש מחלקות. בודקים **לפחות ערך אחד מכל מחלקה**.", do=hide("cl-m3") + show("cl-c1")),
    P("למשל מינוס עשרים, חמישים, ומאה עשרים.", do=show("na-p-20", "na-p50", "na-p120"), hold=0.4),
], stage=w.code("cl", WATER, size=28) + NL_W("na"),
   panel=st.card("cl-c1", "rule", "🔑 ערך אחד לפחות מכל מחלקה"))

bounds = Scene("bounds", "ערכי גבול", [
    P("עכשיו נסתכל על המקומות שבהם הפלט משתנה: **הגבולות**."),
    P("הגבול הראשון: בין אפס לאחת. באפס עדיין קרח, ובאחת כבר מים.", do=show("nb-b0", "bo-m1")),
    P("שימו לב לסימן: **קטן או שווה** לאפס. לכן אפס עצמו עוד בצד של הקרח.", do=show("bo-c1")),
    P("הגבול השני: בין תשעים ותשע למאה. כאן הסימן הוא **קטן ממש**, ולכן מאה כבר אדים.",
      do=hide("bo-m1") + show("nb-b1", "bo-m2")),
    P("המתכון: לכל גבול, הערך **האחרון לפני** והערך **הראשון אחרי**.", do=hide("bo-m2") + show("bo-c2")),
    P("שני גבולות, ולכן ארבעה ערכים: אפס, אחת, תשעים ותשע, ומאה.", do=show("bo-c3"), hold=0.4),
], stage=w.code("bo", WATER, size=28) + NL_W("nb", segs_hidden=False),
   panel=st.card("bo-c1", "trap", "⚠️ <span class=\"ts-mono\">&lt;=</span> מול <span class=\"ts-mono\">&lt;</span>: "
                                  "הסימן קובע איפה בדיוק הגבול")
         + st.card("bo-c2", "rule", "🔑 לכל גבול: האחרון לפני + הראשון אחרי")
         + st.card("bo-c3", "ex", 'ערכי הגבול: ' + fmt(BVALS)))

why = Scene("why", "למה גבולות?", [
    P("ולמה זה כל כך חשוב? נכניס טעות נפוצה: במקום קטן או שווה לאפס, נכתוב **קטן** מאפס.", do=show("wy-m1", "wy-c1")),
    P("נריץ את שלושת הערכים מאמצע המחלקות: מינוס עשרים, חמישים ומאה עשרים.", do=show("wy-c2")),
    P("כולם נותנים בדיוק את אותה תשובה כמו קודם. הבדיקות עוברות, והבאג לא נתפס.", do=show("wy-c3")),
    P("יש רק קלט **אחד** שמגלה את הטעות הזו: אפס. הקוד השגוי אומר מים, במקום קרח.", do=show("wy-c4")),
    P("ואפס הוא בדיוק ערך גבול. וגם טעות בגבול של מאה מתגלה רק במאה עצמה.", do=show("wy-c5"), hold=0.4),
], stage=w.code("wy", WATER.replace("temp <= 0", "temp < 0"), size=28, title="עם טעות"),
   panel=st.card("wy-c1", "plain", "🐞 <span class=\"ts-mono\">temp &lt; 0</span> במקום <span class=\"ts-mono\">temp &lt;= 0</span>")
         + st.card("wy-c2", "ex", fmt(DEEP) + " ← אותן תשובות ✓")
         + st.card("wy-c3", "trap", "⚠️ ערכים מאמצע המחלקות לא תופסים את הבאג")
         + st.card("wy-c4", "rule", "🔑 רק <span class=\"ts-mono\">0</span> מגלה אותו: מים במקום קרח")
         + st.card("wy-c5", "ex", "טעות במאה ← רק <span class=\"ts-mono\">100</span> מגלה"))

exam = Scene("exam", "בסגנון מבחן", [
    P("ועכשיו שאלה בסגנון מבחן. המתודה מחזירה שגיאה לציון מחוץ לטווח אפס עד מאה."),
    P("בתוך הטווח: מחמישים ושש ומעלה עובר, ומתחת נכשל. אילו ערכים בודקים את שני הצדדים של כל הגבולות?"),
    P("נמצא את הגבולות. קודם בדיקת התקינות: היא יוצרת **שני** גבולות.", do=show("ne-c0", "ne-c1", "ne-c2", "ne-c3")),
    P("בין מינוס אחת לאפס, ובין מאה למאה ואחת.", do=show("ne-b0", "ne-b2")),
    P("ועוד גבול אחד בין חמישים וחמש לחמישים ושש.", do=show("ne-b1")),
    P("שלושה גבולות, שישה ערכים: מינוס אחת, אפס, חמישים וחמש, חמישים ושש, מאה, ומאה ואחת.", do=show("q-ok-a")),
    P("אפס, חמישים ושש ומאה: רק צד **אחד** של כל גבול.", do=show("q-x-b", "q-n-b")),
    P("והמלכודת: ארבעה ערכים סביב אפס, חמישים ושש ומאה. שכחו את הצד הלא תקין: מינוס אחת, ומאה ואחת.",
      do=show("q-x-c", "q-n-c")),
    P("ומינוס עשר, שלושים, שמונים ומאה ועשר: ערך מכל אזור, אבל אף אחד לא ליד גבול.", do=show("q-x-d", "q-n-d"),
      hold=0.5),
], stage=w.code("er", RESULT, size=25) + NL_R("ne", tick_dy={1: 0}),
   panel=w.stem("", "אילו ערכים בודקים את שני הצדדים של כל גבול במתודה <bdi>result</bdi>?")
         + st.options("q", OPTS, notes={"b": "צד אחד", "c": "בלי הלא-תקין", "d": "בלי גבולות"}))

recap = Scene("recap", "סיכום", [
    P("לסיכום: מחלקת שקילות היא קבוצת קלטים עם אותה התנהגות. בודקים ערך אחד לפחות מכל אחת.", do=show("r-1")),
    P("בכל גבול בודקים את הערך האחרון לפני ואת הראשון אחרי. שימו לב לסימן: קטן, או קטן או שווה.", do=show("r-2")),
    P("וגם בדיקת תקינות יוצרת גבולות. וזכרו את הבאג: רק האפס תפס אותו. נתראה ברמה הבאה.", do=show("r-3"), hold=0.6),
], stage=NL_W("nr", segs_hidden=False, ticks_hidden=False),
   panel=st.card("r-1", "rule", "🔑 ערך אחד מכל מחלקת שקילות")
         + st.card("r-2", "rule", "🔑 לכל גבול: האחרון לפני + הראשון אחרי")
         + st.card("r-3", "trap", "⚠️ גם בדיקת תקינות = גבולות. הבאג נתפס רק ב-<span class='ts-mono'>0</span>"))

SCENES = [title, idea, classes, bounds, why, exam, recap]
w.no_latin_and_isolate(SCENES)
VIDEO = Video("T05", "tst", "תכנון מקרי בדיקה: מחלקות שקילות וערכי גבול", SCENES, bank={})
