# -*- coding: utf-8 -*-
"""T03 · JUnit: setup, test ו-tearDown — video script (build: tools/video/vid.py T03).

Source: courses/tst/T03.js (lesson + goal). Exam anchor: 24B-B-Q22 (the parameters of assertEquals), used by no guided
quiz. Not used on purpose: the T03 quiz (T03-Q1..Q3 with Calc/Cart, 20-B-Q4, 24B-A-Q19), the T08 boss item 23B-A-Q5,
the twin 25F0b-Q18 of the anchor, and 22S-A-Q2 / 24S-A-Q17 / 19B-B-Q10 / SP-AMR-Q4 (siblings of quiz items).
Worked example: a new Account class with two tests. The code on screen is compiled and run here against a small
JUnit-5 stand-in (w_tst.junit: a fresh instance per test, @BeforeEach before and @AfterEach after every test); the
run log, the pass/fail results and the two failure messages shown on screen are asserted from that run.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_tst as w

# ---------------------------------------------------------------- the code (compiled and run)
ACCOUNT = """class Account {
  private int balance;
  Account(int start) { balance = start; }
  void deposit(int x) { balance += x; }
  void withdraw(int x) { balance -= x; }
  int balance() { return balance; }
}"""
TEST = """class AccountTest {
  Account acc;

  @BeforeEach void setUp() { acc = new Account(100); }

  @Test void deposit() {
    acc.deposit(50);
    assertEquals(150, acc.balance());
  }

  @Test void withdraw() {
    acc.withdraw(30);
    assertEquals(70, acc.balance());
  }

  @AfterEach void tearDown() { acc = null; }
}"""
IMPORTS = "import org.junit.jupiter.api.*;\nimport static org.junit.jupiter.api.Assertions.*;\n"
LOG = w.junit({"Account.java": ACCOUNT, "AccountTest.java": IMPORTS + TEST}, "AccountTest")
STEPS = ["setUp", "deposit", "tearDown", "setUp", "withdraw", "tearDown"]
if LOG is not None:
    assert [l[4:] for l in LOG if l.startswith("RUN ")] == STEPS, LOG
    assert "PASS deposit" in LOG and "PASS withdraw" in LOG, LOG          # both pass: each starts from 100
    assert LOG.count("RUN setUp") == 2 and LOG.count("RUN tearDown") == 2

# a buggy deposit (adds twice): the failure message, with the parameters in the right and in the swapped order
BUGGY = ACCOUNT.replace("balance += x;", "balance += 2 * x;")
SWAPPED = TEST.replace("assertEquals(150, acc.balance());", "assertEquals(acc.balance(), 150);")
LOG_BUG = w.junit({"Account.java": BUGGY, "AccountTest.java": IMPORTS + TEST}, "AccountTest")
LOG_SW = w.junit({"Account.java": BUGGY, "AccountTest.java": IMPORTS + SWAPPED}, "AccountTest")
MSG_OK, MSG_SW = "expected: <150> but was: <200>", "expected: <200> but was: <150>"
if LOG_BUG is not None:
    assert f"FAIL deposit {MSG_OK}" in LOG_BUG and "PASS withdraw" in LOG_BUG, LOG_BUG
    assert f"FAIL deposit {MSG_SW}" in LOG_SW, LOG_SW

# forgetting @BeforeEach: no account is ever created, both tests fail on a null account
NOSETUP = TEST.replace("  @BeforeEach void setUp() { acc = new Account(100); }" + chr(10), "")
assert NOSETUP != TEST
LOG_NS = w.junit({"Account.java": ACCOUNT, "AccountTest.java": IMPORTS + NOSETUP}, "AccountTest")
if LOG_NS is not None:
    fails = [l for l in LOG_NS if l.startswith("FAIL")]
    assert len(fails) == 2 and all("null" in l for l in fails), LOG_NS

# ---------------------------------------------------------------- exam 24B-B-Q22
Q = BANK["24B-B-Q22"]
assert Q["correctIndex"] == 1 and "ערך מצופה" in Q["options"][1] and "ערך אמיתי" in Q["options"][1]
assert "בוליאני" in Q["options"][0] and "בלבד" in Q["options"][2] and "שגויות" in Q["options"][3]
assert "רשימה" in Q["options"][4]
OPTS = w.opts_of(Q, order=[0, 2, 4, 1, 3])

L = {k: i for i, k in enumerate(TEST.split("\n"))}     # line numbers of the test class, by content
ln = lambda frag: next(i for i, l in enumerate(TEST.split("\n")) if frag in l)
L_BE, L_T1, L_T2, L_AE = ln("@BeforeEach"), ln("@Test void deposit"), ln("@Test void withdraw"), ln("@AfterEach")
L_A1, L_A2 = ln("assertEquals(150"), ln("assertEquals(70")

CHIP_KIND = {"setUp": "an", "tearDown": "an", "deposit": "te", "withdraw": "te"}
LOGCHIPS = lambda pfx, hidden=True: w.chips(pfx, [s + "()" for s in STEPS], hidden=hidden,
                                            kinds=[CHIP_KIND[s] for s in STEPS], rtl=True)
CODE = lambda pfx, **k: w.code(pfx, TEST, size=24, **k)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נכיר את JUnit, הספרייה לבדיקות יחידה ב-Java.", say="בסרטון הזה נכיר את JUnit, הספרייה לבדיקות יחידה בג'אווה."),
    P("נריץ מחלקת בדיקה ונקרא את יומן ההרצה, נראה מה קורה כששוכחים אנוטציה, ומה מעבירים ל-assertEquals.", hold=0.4),
], stage='<div class="kicker">T03 · בדיקות תוכנה</div><h1>JUnit: יומן ההרצה ו-assertEquals</h1>'
         '<p>מריצים מחלקת בדיקה אמיתית, וקוראים בדיוק מה רץ ומתי.</p>',
   layout="title")

idea = Scene("idea", "מחלקת בדיקה", [
    P("נבדוק מחלקה פשוטה של חשבון בנק: מפקידים, מושכים, ובודקים יתרה.", do=show("ac")),
    P("מחלקת הבדיקה מכילה מתודות, ועל כל מתודה יש **אנוטציה** שאומרת ל-JUnit מתי להריץ אותה.",
      do=hide("ac") + show("cd")),
    P("@Test מסמנת מתודה שהיא מקרה בדיקה. כאן יש שתיים: הפקדה ומשיכה.", do=show("cd-m5", "cd-m10")),
    P("@BeforeEach מסמנת את ה-setup: כאן יוצרים חשבון עם מאה שקלים.", do=show("cd-m3")),
    P("@AfterEach מסמנת את ה-tearDown: כאן מנקים.", do=show("cd-m15")),
    P("ומתי בדיוק כל אחת מהן רצה? במקום לשנן, נריץ ונסתכל.", do=show("id-c1"), hold=0.4),
], stage=w.swap("idsw", [w.code("ac", ACCOUNT, size=26), CODE("cd")], 620),
   panel=st.card("id-c1", "ex", "מתי רצות <bdi>setUp</bdi> ו-<bdi>tearDown</bdi>? נריץ ונראה"))
assert (L_BE, L_T1, L_T2, L_AE) == (3, 5, 10, 15)

life = Scene("life", "סדר ההרצה", [
    P("נריץ את המחלקה, ונעקוב אחרי מה ש-JUnit עושה, צעד אחר צעד."),
    P("לפני הטסט הראשון רץ ה-setup, ונוצר חשבון עם מאה.", do=show("lg-0", "cl-m3")),
    P("עכשיו רץ טסט ההפקדה: מפקידים חמישים, והיתרה מאה וחמישים. עבר.", do=show("lg-1", "cl-m5") + hide("cl-m3")),
    P("ואחריו רץ ה-tearDown.", do=show("lg-2", "cl-m15") + hide("cl-m5")),
    P("לפני הטסט השני, שוב setup: חשבון **חדש**, שוב עם מאה.", do=show("lg-3", "cl-m3") + hide("cl-m15")),
    P("טסט המשיכה: מושכים שלושים, והיתרה שבעים. עבר.", do=show("lg-4", "cl-m10") + hide("cl-m3")),
    P("ושוב tearDown.", do=show("lg-5", "cl-m15") + hide("cl-m10"), hold=0.3),
    P("עכשיו קראו את היומן כולו, מימין לשמאל. ספרו בעצמכם כמה פעמים מופיע כל שם."),
    P("ולמה המשיכה מצפה לשבעים, ולא למאה ועשרים? כי כל טסט מתחיל **ממצב נקי**.", do=show("li-c2")),
    P("ההפקדה מהטסט הקודם לא נשארת. וכך הסדר שבו הטסטים רצים לא משנה את התוצאה.", hold=0.4),
], stage=CODE("cl"),
   panel=LOGCHIPS("lg")
         + st.card("li-c2", "ex", "כל טסט מתחיל ממצב נקי: 100, לא 150"))

forgot = Scene("forgot", "שכחנו את ה-setup", [
    P("ומה קורה אם נמחק את השורה של ה-setup?", do=show("ns")),
    P("אף אחד לא יוצר חשבון. השדה של החשבון נשאר ריק.", do=show("fg-c1")),
    P("מריצים: שני הטסטים נכשלים, עוד לפני שהגיעו לבדיקה. הם ניסו להפקיד ולמשוך מחשבון שלא קיים.",
      do=show("nf-0", "nf-1")),
    P("ההכנה של הנתונים היא חלק מהבדיקה. בלי הכנה, אין מה לבדוק.", hold=0.4),
], stage=w.code("ns", NOSETUP, size=24, hidden=True)
         + w.chips("nf", ["deposit ✗", "withdraw ✗"], kinds=["bad", "bad"], rtl=True),
   panel=st.card("fg-c1", "plain", "חשבון שלא נוצר ← <span class=\"ts-mono\">null</span>"))

asrt = Scene("assert", "assertEquals", [
    P("ועכשיו הבדיקה עצמה: assertEquals.", do=show("as-m7")),
    P("היא מקבלת שני ערכים. קודם **הערך המצופה**, מאה וחמישים. אחר כך **הערך האמיתי**, מה שהקוד החזיר.",
      do=show("as-c1")),
    P("אם הם שווים, הבדיקה עוברת. אם לא, היא נכשלת."),
    P("נכניס באג: ההפקדה מוסיפה את הסכום פעמיים.", do=show("as-c2")),
    P("JUnit מדווחת: ציפיתי למאה וחמישים, וקיבלתי מאתיים. ברור מה השתבש.", do=show("as-c3")),
    P("ומה אם נהפוך את הסדר, ונשים את הערך האמיתי ראשון?", do=show("as-c4")),
    P("הבדיקה עדיין נכשלת, אבל ההודעה הפוכה: ציפיתי למאתיים, וקיבלתי מאה וחמישים. מטעה.", do=show("as-c5")),
    P("ההודעה נבנית מהסדר שבו העברנו את הערכים. לכן הסדר חשוב.", hold=0.4),
], stage=CODE("as"),
   panel=st.card("as-c1", "rule", "🔑 <bdi>assertEquals(expected, actual)</bdi>")
         + st.card("as-c2", "plain", "🐞 באג: <span class=\"ts-mono\">balance += 2 * x;</span>")
         + st.card("as-c3", "ex", f'<span class="ts-mono">{w.esc(MSG_OK)}</span>')
         + st.card("as-c4", "plain", '<span class="ts-mono">assertEquals(acc.balance(), 150)</span>')
         + st.card("as-c5", "trap", f'⚠️ <span class="ts-mono">{w.esc(MSG_SW)}</span>'))

exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: בהרצת הפקודה assertEquals, אילו פרמטרים מועברים?"),
    P("בדיוק מה שראינו: **ערך מצופה**, ואחריו **ערך אמיתי**.", do=show("q-ok-1")),
    P("ערך בוליאני בלבד? זה מתאים לסוג אחר של assert. assertEquals משווה שני ערכים.", do=show("q-x-0", "q-n-0"),
      say="ערך בוליאני בלבד? זה מתאים לסוג אחר של אַסֶרְט. אַסֶרְט אִיקְוָולְס משווה שני ערכים."),
    P("ערך אמיתי בלבד? אז אין למה להשוות אותו. צריך גם את המצופה.", do=show("q-x-2", "q-n-2")),
    P("ורשימה של ערכים מצופים? assertEquals משווה ערך מצופה **אחד** לערך אמיתי אחד.", do=show("q-x-4", "q-n-4")),
    P("ומכיוון שיש תשובה נכונה, האפשרות שכל האחרות שגויות נופלת.", do=show("q-x-3"), hold=0.5),
], stage=w.stem(Q["id"], "בהרצת הפקודה <bdi>assertEquals</bdi> מועברים הפרמטרים:")
         + w.code("ex", "assertEquals(150, acc.balance());", size=30),
   panel=st.options("q", OPTS, notes={0: "assert אחר", 2: "אין השוואה", 4: "ערך אחד"}))

recap = Scene("recap", "סיכום", [
    P("לסיכום: הרצנו מחלקת בדיקה, וקראנו ביומן בדיוק מה רץ ומתי.", do=show("r-1")),
    P("ראינו שבלי ה-setup שני הטסטים נופלים, כי אין חשבון לבדוק.", do=show("r-2")),
    P("וב-assertEquals: קודם המצופה, אחר כך האמיתי. נתראה ברמה הבאה.", do=show("r-3"), hold=0.6),
], stage=LOGCHIPS("rl", hidden=False),
   panel=st.card("r-1", "ex", "יומן ההרצה: קוראים, לא משננים")
         + st.card("r-2", "trap", "⚠️ בלי <bdi>setUp</bdi>: אין חשבון, הטסטים נופלים")
         + st.card("r-3", "rule", "🔑 <bdi>assertEquals(expected, actual)</bdi>"))

SCENES = [title, idea, life, forgot, asrt, exam, recap]
w.no_latin_and_isolate(SCENES)
VIDEO = Video("T03", "tst", "JUnit: יומן ההרצה ו-assertEquals", SCENES, bank={"24B-B-Q22": 1})
