# -*- coding: utf-8 -*-
"""T04 · Mock: לבדוק יחידה בלי התלויות שלה — video script (build: tools/video/vid.py T04).

Source: courses/tst/T04.js (lesson + goal). Exam anchor: 24B-B-Q23 ("in testing, what is a Mock?"), used by no guided
quiz. Not used on purpose: the T04 quiz (T04-Q1..Q3 with OrderService / TicketService, 24S-A-Q18, 25S-A-Q18), the
T08 boss item 26S-A-Q20 (AIService), 26CL-Q18 (SMS, the lesson's example), 25B-N-Q18 / 25F0a-Q18 (who contains whom,
the topic of T04-Q3) and SP-DGM-Q7 (the T08 video).
Worked example: a new UmbrellaAdvisor that asks a weather web service; the test replaces the service with a
hand-written FakeWeather whose answer is set in advance. The code on screen is compiled and run here against the
JUnit-5 stand-in of w_tst (both tests pass), and a Mock of the unit itself is shown to test nothing.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_tst as w

# ---------------------------------------------------------------- the code (compiled and run)
API = """interface WeatherApi {
  int rainChance(String city);
}"""
ADVISOR = """class UmbrellaAdvisor {
  private final WeatherApi api;
  UmbrellaAdvisor(WeatherApi api) { this.api = api; }
  boolean needUmbrella(String city) {
    return api.rainChance(city) >= 50;
  }
}"""
FAKE = """class FakeWeather implements WeatherApi {
  private final int answer;
  FakeWeather(int answer) { this.answer = answer; }
  public int rainChance(String city) { return answer; }
}"""
TEST = """class UmbrellaAdvisorTest {
  @Test void rainyDay() {
    UmbrellaAdvisor adv = new UmbrellaAdvisor(new FakeWeather(80));
    assertTrue(adv.needUmbrella("Haifa"));
  }
  @Test void dryDay() {
    UmbrellaAdvisor adv = new UmbrellaAdvisor(new FakeWeather(10));
    assertFalse(adv.needUmbrella("Haifa"));
  }
}"""
IMPORTS = "import org.junit.jupiter.api.*;\nimport static org.junit.jupiter.api.Assertions.*;\n"
FILES = {"WeatherApi.java": API, "UmbrellaAdvisor.java": ADVISOR, "FakeWeather.java": FAKE,
         "UmbrellaAdvisorTest.java": IMPORTS + TEST}
LOG = w.junit(FILES, "UmbrellaAdvisorTest")
if LOG is not None:
    assert "PASS rainyDay" in LOG and "PASS dryDay" in LOG, LOG
    # an advisor with a bug (always true) fails dryDay: the fake's answer really steers the unit
    BAD = ADVISOR.replace("return api.rainChance(city) >= 50;", "return true;")
    LOG2 = w.junit({**FILES, "UmbrellaAdvisor.java": BAD}, "UmbrellaAdvisorTest")
    assert "FAIL dryDay expected: <false> but was: <true>" in LOG2 and "PASS rainyDay" in LOG2, LOG2

# ---------------------------------------------------------------- a second Mock: one that only records the call
MAIL = """interface EmailSender {
  void send(String to, String text);
}
class Checkout {
  private final EmailSender mail;
  Checkout(EmailSender mail) { this.mail = mail; }
  int pay(String user, int total) {
    mail.send(user, "Paid " + total);
    return total;
  }
}"""
FAKE_MAIL = """class FakeEmail implements EmailSender {
  int sent = 0;
  public void send(String to, String text) { sent++; }
}"""
MAIL_TEST = """class CheckoutTest {
  @Test void sendsOneReceipt() {
    FakeEmail fake = new FakeEmail();
    new Checkout(fake).pay("dana@mail.com", 120);
    assertEquals(1, fake.sent);
  }
}"""
LOG3 = w.junit({"EmailSender.java": MAIL.split("class Checkout")[0],
                "Checkout.java": "class Checkout" + MAIL.split("class Checkout")[1],
                "FakeEmail.java": FAKE_MAIL, "CheckoutTest.java": IMPORTS + MAIL_TEST}, "CheckoutTest")
if LOG3 is not None:
    assert "PASS sendsOneReceipt" in LOG3, LOG3
    # a Checkout that sends the receipt twice is caught by the counter
    ONE = 'mail.send(user, "Paid " + total);'
    TWICE = MAIL.replace(ONE, ONE + "\n    " + ONE)
    LOG4 = w.junit({"EmailSender.java": TWICE.split("class Checkout")[0],
                    "Checkout.java": "class Checkout" + TWICE.split("class Checkout")[1],
                    "FakeEmail.java": FAKE_MAIL, "CheckoutTest.java": IMPORTS + MAIL_TEST}, "CheckoutTest")
    assert "FAIL sendsOneReceipt expected: <1> but was: <2>" in LOG4, LOG4

# ---------------------------------------------------------------- exam 24B-B-Q23
Q = BANK["24B-B-Q23"]
assert Q["correctIndex"] == 2 and "אובייקט מדומה" in Q["options"][2]
assert "יישום אמיתי" in Q["options"][0] and "כלי רישום" in Q["options"][1] and "מערכת ייצור" in Q["options"][3]
assert "שגויות" in Q["options"][4]
OPTS = w.opts_of(Q, order=[0, 1, 3, 2, 4])

# ---------------------------------------------------------------- diagram: the unit, the real service, the mock
def DIAG(pfx, mock_shown=False, real_shown=True):
    items = [
        {"key": "test", "x": 330, "y": 10, "w": 340, "h": 90, "label": "UmbrellaAdvisorTest", "kind": "test"},
        {"key": "adv", "x": 330, "y": 200, "w": 340, "h": 100, "label": "UmbrellaAdvisor", "sub": "היחידה הנבדקת"},
        {"key": "real", "x": 300, "y": 400, "w": 400, "h": 100, "label": "RealWeather", "sub": "שירות רשת חיצוני",
         "kind": "real", "hidden": not real_shown},
        {"key": "fake", "x": 300, "y": 400, "w": 400, "h": 100, "label": "FakeWeather", "sub": "Mock: תשובה מוכנה מראש",
         "kind": "mock", "hidden": not mock_shown},
    ]
    arrows = [{"key": "t", "a": "test", "b": "adv", "label": "needUmbrella(\"Haifa\")", "lxy": (660, 160)},
              {"key": "r", "a": "adv", "b": "real", "label": "rainChance", "lxy": (612, 360), "hidden": not real_shown},
              {"key": "f", "a": "adv", "b": "fake", "label": "rainChance", "lxy": (612, 360), "hidden": not mock_shown}]
    return w.boxes(pfx, items, arrows, w=1000, h=520)


# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נכיר את ה-Mock: איך בודקים יחידה, כשהיא תלויה ביחידה אחרת."),
    P("נראה מה מחליפים, מה לא מחליפים, ולמה.", hold=0.4),
], stage='<div class="kicker">T04 · בדיקות תוכנה</div><h1>Mock: לבדוק יחידה בלי התלויות שלה</h1>'
         '<p>מחליפים את התלות באובייקט מדומה שעונה תשובה מוכנה מראש. את היחידה הנבדקת לא מחליפים.</p>', layout="title")

prob = Scene("problem", "הבעיה", [
    P("נבנה יועץ מטרייה: מחלקה שמחליטה אם לקחת מטרייה.", do=show("pr-c1")),
    P("כדי להחליט, היא שואלת שירות מזג אוויר ברשת: מה הסיכוי לגשם בעיר?"),
    P("אם הסיכוי חמישים אחוז או יותר, היא ממליצה לקחת מטרייה.", hold=0.3),
    P("עכשיו נכתוב בדיקת יחידה ליועץ. אבל הוא **תלוי** בשירות חיצוני.", do=show("pr-c2")),
    P("השירות האמיתי איטי, דורש רשת, ועונה כל יום משהו אחר.", do=show("pr-c3")),
    P("אז אם הבדיקה נכשלת, לא נדע: זה באג ביועץ, או סתם שהיום לא יורד גשם?", hold=0.4),
], stage=DIAG("da"),
   panel=st.card("pr-c1", "plain", "☂️ <bdi>UmbrellaAdvisor</bdi>: מטרייה אם סיכוי הגשם 50% ומעלה")
         + st.card("pr-c2", "trap", "⚠️ היחידה תלויה בשירות רשת חיצוני")
         + st.card("pr-c3", "ex", "איטי · דורש רשת · משתנה מיום ליום"))

idea = Scene("idea", "הרעיון", [
    P("הפתרון: מחליפים את השירות האמיתי ב-**Mock**.", do=hide("db-b-real", "db-a-r") + show("db-b-fake", "db-a-f")),
    P("Mock הוא **אובייקט מדומה**, שמחקה את ההתנהגות של האובייקט האמיתי, בדרך **מבוקרת**.", do=show("id-c1")),
    P("כאן הוא לא שואל אף אחד. הוא פשוט מחזיר את ה-80 שבחרנו.", do=show("id-c2")),
    P("היועץ מקבל אותו כאילו היה השירות האמיתי, ולא יודע את ההבדל.", hold=0.3),
    P("וכך בודקים **רק את הלוגיקה של היועץ**, בלי רשת ובלי מזג אוויר אמיתי.", do=show("id-c3"), hold=0.4),
], stage=DIAG("db"),
   panel=st.card("id-c1", "rule", "🔑 <bdi>Mock</bdi> = אובייקט מדומה שמחקה את האמיתי בדרך מבוקרת")
         + st.card("id-c2", "ex", "מחזיר 80, או 10: מה שבחרנו בטסט")
         + st.card("id-c3", "rule", "🔑 בודקים את היחידה <b>בבידוד</b> מהתלות"))

code = Scene("code", "בקוד", [
    P("כך זה נראה בקוד. היועץ מקבל את השירות בבנאי, דרך ממשק.", do=show("cs-0")),
    P("ה-Mock מממש את אותו ממשק, ומחזיר את התשובה שנתנו לו כשיצרנו אותו.", do=hide("cs-0") + show("cs-1")),
    P("בטסט הראשון ה-Mock מחזיר שמונים. היועץ צריך להמליץ על מטרייה.",
      do=hide("cs-1") + show("cs-2", "ct-m2", "ct-m3")),
    P("בטסט השני הוא מחזיר עשר. היועץ צריך להגיד שלא צריך.", do=hide("ct-m2", "ct-m3") + show("ct-m6", "ct-m7")),
    P("שני הטסטים עוברים, היום ובכל יום, כי **אנחנו** קובעים את התשובה.", do=show("co-c1")),
    P("ואם נכניס ליועץ באג, ונגרום לו להמליץ תמיד על מטרייה, הטסט השני ייכשל.", do=show("co-c2"),
      hold=0.4),
], stage=w.swap("cs", [w.code("ca", API + chr(10) + ADVISOR, size=24), w.code("cf", FAKE, size=24),
                         w.code("ct", TEST, size=23)], 560),
   panel=st.card("co-c1", "rule", "🔑 התשובה בידיים שלנו ← הבדיקה יציבה")
         + st.card("co-c2", "ex", "באג: <span class=\"ts-mono\">return true;</span> ← <bdi>dryDay</bdi> נכשל"))

record = Scene("record", "Mock שלא שולח באמת, רק סופר", [
    P("עוד דוגמה: Mock שלא שולח באמת, רק סופר. הנה קופה ששולחת קבלה במייל.", do=show("rc-0")),
    P("בבדיקת יחידה לא רוצים לשלוח מיילים אמיתיים. אז מחליפים את שולח המיילים ב-Mock.", do=hide("rc-0") + show("rc-1")),
    P("ה-Mock לא שולח כלום. הוא רק סופר כמה פעמים קראו לו.", do=show("m1-m2")),
    P("והבדיקה מוודאת שבתשלום אחד נשלחה בדיוק קבלה אחת.", do=hide("rc-1") + show("rc-2", "m2-m4")),
    P("אם הקופה תשלח בטעות שתי קבלות, הבדיקה תיכשל: ציפינו לאחת, וקיבלנו שתיים.", do=show("re-c1"), hold=0.4),
], stage=w.swap("rc", [w.code("m0", MAIL, size=24), w.code("m1", FAKE_MAIL, size=24), w.code("m2", MAIL_TEST, size=24)], 460),
   panel=st.card("re-c1", "ex", "שתי קבלות ← הבדיקה נכשלת:<br><span class=\"ts-mono ts-nw\">expected: &lt;1&gt; but was: &lt;2&gt;</span>"))

which = Scene("which", "את מה מחליפים?", [
    P("עכשיו המלכודת הכי נפוצה: **את מה** מחליפים ב-Mock?"),
    P("בדוגמה שלנו החלפנו את שירות מזג האוויר, שהיועץ משתמש בו. את היועץ עצמו השארנו אמיתי.",
      do=show("de-b-fake", "de-a-f", "wh-c1")),
    P("מה היה קורה אם היינו מחליפים את היועץ עצמו ב-Mock?", do=show("de-f-x")),
    P("ה-Mock היה מחזיר את מה שהכנו מראש, והבדיקה הייתה עוברת. אבל **אף שורה** של היועץ לא הייתה רצה.",
      do=show("wh-c2")),
    P("בדיקה כזו לא בודקת כלום.", hold=0.4),
], stage=w.boxes("de", [
        {"key": "adv", "x": 330, "y": 200, "w": 340, "h": 100, "label": "UmbrellaAdvisor", "sub": "היחידה הנבדקת"},
        {"key": "fake", "x": 300, "y": 400, "w": 400, "h": 100, "label": "FakeWeather", "sub": "Mock של התלות",
         "kind": "mock", "hidden": True},
        {"key": "test", "x": 330, "y": 10, "w": 340, "h": 90, "label": "UmbrellaAdvisorTest", "kind": "test"}],
       [{"key": "t", "a": "test", "b": "adv"},
        {"key": "f", "a": "adv", "b": "fake", "label": "rainChance", "lxy": (612, 360), "hidden": True}],
       [{"key": "x", "x": 310, "y": 180, "w": 380, "h": 140, "label": "לא את זה!", "kind": "warn"}], w=1000, h=520),
   panel=st.card("wh-c1", "rule", "🔑 מזג האוויר: מדומה. היועץ: <b>אמיתי</b>")
         + st.card("wh-c2", "trap", "⚠️ <bdi>Mock</bdi> של הנבדק = שום קוד שלו לא רץ"))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: בהקשר של בדיקות, מה זה Mock?"),
    P("בדיוק ההגדרה שראינו: **אובייקט מדומה**, שמחקה את ההתנהגות של עצמים אמיתיים בדרכים מבוקרות.",
      do=show("q-ok-2")),
    P("יישום אמיתי של מחלקה שמבצע חישובים בפועל? זה ההפך. ה-Mock מזויף, ועונה תשובה מוכנה.",
      do=show("q-x-0", "q-n-0")),
    P("כלי רישום? נכון שראינו Mock שסופר קריאות, אבל הספירה רק משרתת את ההחלפה. היא לא המטרה שלו.",
      do=show("q-x-1", "q-n-1")),
    P("החלפה מלאה של מערכת הייצור? לא. מחליפים יחידה אחת, את התלות, ולא את כל המערכת.",
      do=show("q-x-3", "q-n-3")),
    P("ומכיוון שיש תשובה נכונה, האפשרות שכל האחרות שגויות נופלת.", do=show("q-x-4"), hold=0.5),
], stage=w.stem(Q["id"], "בהקשר של בדיקות, מה זה <bdi>Mock</bdi>?")
         + DIAG("dx", mock_shown=True, real_shown=False),
   panel=st.options("q", OPTS, notes={0: "ההפך", 1: "לא תיעוד", 3: "יחידה אחת"}))

recap = Scene("recap", "סיכום", [
    P("לסיכום: החלפנו שירות אמיתי באובייקט מדומה, שעונה בדיוק מה שבחרנו.", do=show("r-1")),
    P("כך הבדיקה של היועץ לא תלויה ברשת, ולא במזג האוויר של היום.", do=show("r-2")),
    P("והיועץ עצמו נשאר אמיתי, כי אותו אנחנו בודקים. נתראה ברמה הבאה.", do=show("r-3"), hold=0.6),
], stage=DIAG("dr", mock_shown=True, real_shown=False),
   panel=st.card("r-1", "rule", "🔑 אובייקט מדומה שעונה מה שבחרנו")
         + st.card("r-2", "rule", "🔑 בלי רשת, בלי מזג אוויר אמיתי")
         + st.card("r-3", "trap", "⚠️ היועץ נשאר אמיתי: אותו בודקים"))

SCENES = [title, prob, idea, code, record, which, exam, recap]
w.no_latin_and_isolate(SCENES)
VIDEO = Video("T04", "tst", "Mock: לבדוק יחידה בלי התלויות שלה", SCENES, bank={"24B-B-Q23": 2})
