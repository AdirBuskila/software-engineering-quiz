# -*- coding: utf-8 -*-
"""T08 · מבחן גמר: בדיקות תוכנה (boss) — a walkthrough of three exam questions (build: tools/video/vid.py T08).

Source: courses/tst/T08.js (boss: the lesson table + its six quiz refs). Exam anchors, used by no guided quiz:
SP-DGM-Q4 (what @Test is for), SP-DGM-Q7 (what mockups are for while writing tests), 20-A-Q3 (how Agile uses
TDD). Not used on purpose: the six boss refs (24B-A-Q23, 25S-A-Q5, 25F0a-Q6, 23B-A-Q5, 26S-A-Q20, 26CL-Q19), every
level's quiz, 21-B-Q7 and its twins 21S-B-Q7 / 21-A-Q5 / 21S-A-Q5 / 23S-A-Q11 (automated tests vs Inspection) and SP-AMR-Q6 /
23S-A-Q12 (Agile and TDD), and the anchors of T01..T07.
Options that cite siblings by number ({@n}) are shown by content. The JUnit fact is shown, not just told: a JUnit test
runs code (the stand-in runner of w_tst executes a test), while an inspection has nothing to execute.
"""
import re
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_tst as w

# ---------------------------------------------------------------- Q1 SP-DGM-Q4 ({@n} cites siblings: show by content)
Q1 = BANK["SP-DGM-Q4"]
assert Q1["correctIndex"] == 3 and "Test Case" in Q1["options"][3] and Q1["options"][1] == "לתיעוד המטודה"
assert "JAVA" in Q1["options"][2] and re.fullmatch(r"תשובות \{@1\} ו – \{@3\} נכונות", Q1["options"][0])
O1_TEXT = {0: "התשובות ״לתיעוד״ ו״להרצה״ נכונות שתיהן", 1: Q1["options"][1], 2: Q1["options"][2], 3: Q1["options"][3]}
O1 = [(k, w.ltr_runs(O1_TEXT[k])) for k in (1, 2, 3, 0)]
# @Test marks a method that JUnit runs as a test case: the stand-in runner finds it, runs it and reports
SAMPLE = """class PriceTest {
  @Test void vat() {
    assertEquals(117, Price.withVat(100));
  }
}"""
PRICE = "class Price { static int withVat(int p) { return p * 117 / 100; } }"
LOG = w.junit({"Price.java": PRICE, "PriceTest.java": "import org.junit.jupiter.api.*;\n"
               "import static org.junit.jupiter.api.Assertions.*;\n" + SAMPLE}, "PriceTest")
if LOG is not None:
    assert LOG == ["RUN vat", "PASS vat"], LOG

# ---------------------------------------------------------------- Q2 SP-DGM-Q7
Q2 = BANK["SP-DGM-Q7"]
assert Q2["correctIndex"] == 3 and "חלקי דמה בקוד" in Q2["options"][3]
assert "לא חלק" in Q2["options"][0] and "setup" in Q2["options"][1] and Q2["options"][2] == "תכנון הבדיקות"
O2 = w.opts_of(Q2, order=[0, 1, 2, 3])

# ---------------------------------------------------------------- Q3 20-A-Q3 ({@n} cites siblings: show by content)
Q3 = BANK["20-A-Q3"]
assert Q3["correctIndex"] == 2 and Q3["options"][2] == "מקביליות של פיתוח ובדיקות"
assert re.fullmatch(r"תשובות \{@2\} ו-\{@1\} נכונות", Q3["options"][0]) and "גמיש" in Q3["options"][1]
assert "אין קשר" in Q3["options"][3]
O3_TEXT = {0: "התשובות ״מקביליות״ ו״גמיש״ נכונות שתיהן", 1: Q3["options"][1], 2: Q3["options"][2], 3: Q3["options"][3]}
O3 = [(k, w.ltr_runs(O3_TEXT[k])) for k in (1, 3, 2, 0)]

TABLE = ('<table class="ts-tab" id="bt"><thead><tr><th>שאלה לפני שעונים</th><th>למשל</th></tr></thead><tbody>'
         '<tr id="bt-r0" class="h"><td>מה גודל הנבדק? מריצים בכלל?</td><td>רמות הבדיקה</td></tr>'
         '<tr id="bt-r1" class="h"><td>תכנון או ביצוע?</td><td>מודל <bdi>V</bdi></td></tr>'
         '<tr id="bt-r2" class="h"><td>מה בדיוק מוחלף?</td><td><bdi>Mock</bdi></td></tr>'
         '<tr id="bt-r3" class="h"><td>מה רץ, ומתי?</td><td><bdi>JUnit</bdi></td></tr></tbody></table>')

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("זה מבחן הגמר של קורס הבדיקות. נפתור יחד שלוש שאלות אמיתיות ממבחנים."),
    P("בכל שאלה נשאל קודם: מה בדיוק נשאל, ואיזה כלל מהקורס סוגר אותה.", hold=0.4),
], stage='<div class="kicker">T08 · בדיקות תוכנה · מבחן גמר</div><h1>מבחן גמר: בדיקות תוכנה</h1>'
         '<p>שלוש שאלות ממבחנים: מה עושה <bdi>@Test</bdi>, למה משמש Mock, ואיך האג׳ייל משתמש ב-TDD.</p>', layout="title")

method = Scene("method", "לפני שעונים", [
    P("לפני כל שאלה בבדיקות, עברו על כמה שאלות קצרות."),
    P("מה גודל הנבדק, והאם בכלל מריצים קוד?", do=show("bt-r0")),
    P("שואלים על תכנון, או על ביצוע?", do=show("bt-r1")),
    P("מה בדיוק מוחלף ב-Mock, ומה רץ ומתי ב-JUnit?", do=show("bt-r2", "bt-r3")),
    P("עכשיו נראה איך השאלות האלה סוגרות שלוש שאלות אמיתיות.", hold=0.4),
], stage=TABLE, layout="full")

q1 = Scene("q1", "שאלה 1", [
    P("שאלה ראשונה: האנוטציה @Test משמשת את ספריית JUnit למה?"),
    P("במקום לנחש, נריץ. הנה מחלקת בדיקה עם מתודה אחת, ומעליה @Test.", do=show("j1-m1")),
    P("מריצים את המחלקה ב-JUnit. היא מוצאת את המתודה המסומנת, מריצה אותה, ומדווחת: עברה.", do=show("j1r-0")),
    P("בלי הסימון, JUnit לא הייתה מריצה את המתודה בכלל. אז @Test אומרת: הרץ אותי כמקרה בדיקה.",
      do=show("q1-c1", "a-ok-3")),
    P("לתיעוד המתודה? לא. האנוטציה לא כותבת תיעוד, היא גורמת למתודה לרוץ.", do=show("a-x-1", "a-n-1")),
    P("ומשמשת את ספריות ה-Java? לא. @Test שייכת ל-JUnit, ולא לספריות הבסיס של השפה.",
      say="ומשמשת את ספריות הג'אווה? לא. אֶט טֶסְט שייכת לגֵ'יי יוּנִיט, ולא לספריות הבסיס של השפה.",
      do=show("a-x-2", "a-n-2")),
    P("והאפשרות שתיעוד והרצה נכונות שתיהן נופלת, כי התיעוד לא נכון.", do=show("a-x-0", "a-n-0"), hold=0.5),
], stage=w.stem(Q1["id"], "<bdi>@Test annotation</bdi> משמש את סיפריות ה-<bdi>JUnit</bdi> ל:")
         + w.code("j1", SAMPLE, size=27)
         + w.chips("j1r", [f"{l.split()[1]}() ✓" for l in (LOG or ["PASS vat"]) if l.startswith("PASS")], kinds=["ok"])
         + st.card("q1-c1", "rule", "🔑 <bdi>@Test</bdi> = מתודה ש-<bdi>JUnit</bdi> מריצה כמקרה בדיקה"),
   panel=st.options("a", O1, notes={1: "לא תיעוד", 2: "של JUnit", 0: "תיעוד לא נכון"}))

q2 = Scene("q2", "שאלה 2", [
    P("שאלה שנייה: למה משמש ה-mockup, ה-Mock, בשלב כתיבת הבדיקות?",
      say="שאלה שנייה: למה משמש המוֹקאַפּ, המוֹק, בשלב כתיבת הבדיקות?"),
    P("המילה כאן היא mockup, אבל הכוונה ל-Mock שהכרנו: אובייקט מדומה בבדיקה.", say="המילה כאן היא מוֹקאַפּ, אבל הכוונה למוֹק שהכרנו: אובייקט מדומה בבדיקה."),
    P("זוכרים את יועץ המטרייה? החלפנו את שירות מזג האוויר בחלק דמה, שעונה תשובה מוכנה.", do=show("b2-c1")),
    P("זה התפקיד: **בונים חלקי דמה בקוד**, כדי לבדוק יחידה בבידוד, בצורה טובה יותר.", do=show("b-ok-3")),
    P("שה-Mock לא חלק מכתיבת הבדיקות? להפך: כותבים אותו בדיוק בשביל הבדיקה.", do=show("b-x-0", "b-n-0")),
    P("סימון מתודה כדי ליצור setup תקין? זה תפקיד של אנוטציה, @BeforeEach, ולא של Mock.",
      do=show("b-x-1", "b-n-1")),
    P("ב-setup אפשר ליצור את ה-Mock, אבל ה-Mock עצמו הוא אובייקט שמחליף תלות, לא סימון של מתודה.",
      do=show("b2-t")),
    P("ותכנון הבדיקות? ה-Mock הוא קוד שרץ בזמן הבדיקה, לא שלב תכנון.", do=show("b-x-2", "b-n-2"), hold=0.5),
], stage=w.stem(Q2["id"], "למה משמש ה-<bdi>mockup</bdi> בשלב כתיבת הבדיקות?")
         + w.boxes("bx", [{"key": "u", "x": 40, "y": 60, "w": 360, "h": 100, "label": "UmbrellaAdvisor",
                           "sub": "היחידה הנבדקת"},
                          {"key": "m", "x": 560, "y": 60, "w": 380, "h": 100, "label": "FakeWeather",
                           "sub": "חלק דמה: מחזיר 80", "kind": "mock"}],
                   [{"key": "a", "a": "u", "b": "m", "label": "rainChance"}], w=1000, h=200)
         + st.card("b2-c1", "ex", "חלק דמה בקוד ← בדיקת יחידה בבידוד")
         + st.card("b2-t", "trap", "⚠️ <bdi>Mock</bdi> = אובייקט. <bdi>@BeforeEach</bdi> = סימון של מתודה"),
   panel=st.options("b", O2, notes={0: "להפך", 1: "זו אנוטציה", 2: "זה קוד, לא תכנון"}))

q3 = Scene("q3", "שאלה 3", [
    P("שאלה שלישית: כיצד השיטה האג'ילית עושה שימוש ב-TDD?"),
    P("ב-TDD כל פיסת קוד נולדת יחד עם הבדיקה שלה. אין שלב בדיקות נפרד בסוף.", do=show("c3-0", "c3-1", "c3-2")),
    P("ובאג'ייל עובדים באיטרציות קצרות. בכל איטרציה נכתבים גם קוד וגם בדיקות, ולא מחכים לסוף.", do=show("c3-c1")),
    P("אז הפיתוח והבדיקות קורים **במקביל**. זו התשובה.", do=show("c-ok-2")),
    P("ה-TDD גמיש ביכולות שלו? זה משפט כללי, שלא מתאר איך משתמשים בו.", do=show("c-x-1", "c-n-1")),
    P("אין קשר בין השניים? יש: TDD הוא חלק מהשיטה האג'ילית.", do=show("c-x-3", "c-n-3")),
    P("והאפשרות ששתי התשובות נכונות, המקביליות והגמישות? נופלת, כי הגמישות לא נכונה.",
      do=show("c-x-0", "c-n-0", "c3-t")),
    P("כלל לשאלות כאלה: אפשרות שאומרת ששתי תשובות נכונות, נכונה רק אם **שתיהן** נכונות.", hold=0.5),
], stage=w.stem(Q3["id"], "כיצד השיטה האגילית עושה שימוש ב-<bdi>TDD</bdi>?")
         + w.chips("c3", ["🔴 בדיקה", "🟢 קוד", "🔧 שיפור"], kinds=["heb bad", "heb ok", "heb"], rtl=True)
         + st.card("c3-c1", "rule", "🔑 אג'ייל + <bdi>TDD</bdi> = פיתוח ובדיקות <b>במקביל</b>")
         + st.card("c3-t", "trap", "⚠️ ״שתיהן נכונות״ נופלת אם אחת שגויה"),
   panel=st.options("c", O3, notes={1: "לא מתאר שימוש", 3: "יש קשר", 0: "גמישות לא נכונה"}))

recap = Scene("recap", "סיכום", [
    P("לסיכום שלוש השאלות. ראשונה: הרצנו מחלקת בדיקה, וראינו מה @Test עושה.", do=show("r-1")),
    P("שנייה: חזרנו ליועץ המטרייה, וראינו מה החלק המדומה עושה בבדיקה.", do=show("r-2")),
    P("שלישית: נזכרנו איך נראה מחזור של TDD, ומשם הגענו לתשובה.", do=show("r-3")),
    P("והשיטה: קודם מבינים מה נשאל, ואז בודקים כל אפשרות לגופה. בהצלחה במבחן!", do=show("r-4"), hold=0.6),
], stage=TABLE.replace(' class="h"', ""),
   panel=st.card("r-1", "ex", "שאלה 1: מריצים, ורואים")
         + st.card("r-2", "ex", "שאלה 2: חוזרים לדוגמה מוכרת")
         + st.card("r-3", "ex", "שאלה 3: אפשרות ״שתיהן נכונות״ דורשת את שתיהן")
         + st.card("r-4", "rule", "🔑 מה נשאל? ואז כל אפשרות לגופה"))

SCENES = [title, method, q1, q2, q3, recap]
w.no_latin_and_isolate(SCENES)
VIDEO = Video("T08", "tst", "מבחן גמר: בדיקות תוכנה", SCENES,
              bank={"SP-DGM-Q4": 3, "SP-DGM-Q7": 3, "20-A-Q3": 2})
