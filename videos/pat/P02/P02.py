# -*- coding: utf-8 -*-
"""P02 · Singleton: מופע אחד בלבד — video script (build: tools/video/vid.py P02).

Source: courses/pat/P02.js (lesson + goal: when Singleton is needed, its three ingredients, why it can produce several
instances). Exam anchor: 26B-A-Q18 (how many classes in Singleton's class diagram -> "all other answers are wrong",
since the answer, one, is not listed), which no guided quiz uses.
Every Java snippet on screen is compiled and run here (w_pat.java, when a JDK is present): the shared clock prints
"clock created" once and 2; with a public constructor the same main makes a second clock (2 0); with the private one
javac refuses `new GameClock()`.
The constructor rule is shown by running the GameClock code (public vs private), never in the wording of P02-Q1 /
26CL-Q16 ("several instances? the constructor is not private").
Avoided on purpose: the P02 quiz items (the Logger with a public constructor, the structure description, the print
queue, `a == b` with Config, 26CL-Q16) and their twins 24B-B-Q12 / 24B-B-Q10, the boss item 25S-A-Q10 (two
instances), and 24B-A-Q15 (uml twin of the anchor). My own class: a network game's shared clock.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_pat as w

# ---------------------------------------------------------------- code (compiled and run)
CLOCK = """public class GameClock {
  private static GameClock instance;
  private int seconds;
  private GameClock() { System.out.println("clock created"); }
  public static GameClock getInstance() {
    if (instance == null) instance = new GameClock();
    return instance;
  }
  public void tick() { seconds++; }
  public int time() { return seconds; }
}"""
MAIN = """public class Main {
  public static void main(String[] args) {
    GameClock.getInstance().tick();   // the map
    GameClock.getInstance().tick();   // the scoreboard
    System.out.println(GameClock.getInstance().time());
  }
}"""
OUT1 = "clock created\n2"
w.java({"GameClock": CLOCK, "Main": MAIN}, "Main", OUT1)
L_FIELD, L_CTOR, L_GET0, L_IF, L_RET = 1, 3, 4, 5, 6
assert CLOCK.split("\n")[L_FIELD].strip().startswith("private static GameClock instance")
assert CLOCK.split("\n")[L_CTOR].strip().startswith("private GameClock()")
assert "getInstance" in CLOCK.split("\n")[L_GET0] and "null" in CLOCK.split("\n")[L_IF]

BREAK = """GameClock.getInstance().tick();
GameClock.getInstance().tick();
GameClock other = new GameClock();
System.out.println(GameClock.getInstance().time() + " " + other.time());"""
MAIN2 = "public class Main {\n  public static void main(String[] args) {\n" + \
        "\n".join("    " + l for l in BREAK.split("\n")) + "\n  }\n}"
OUT_PUB = "clock created\nclock created\n2 0"
w.java({"GameClock": CLOCK.replace("private GameClock()", "public GameClock()"), "Main": MAIN2}, "Main", OUT_PUB)
w.expect_compile_error({"GameClock": CLOCK, "Main": MAIN2}, "GameClock() has private access in GameClock")

# exam 26B-A-Q18
Q = BANK["26B-A-Q18"]
assert Q["correctIndex"] == 3 and Q["options"][3] == "כל התשובות האחרות שגויות"
assert [Q["options"][k] for k in (0, 1, 2, 4)] == ["ארבעה", "שלושה", "תלוי בסוג ה-Singleton", "שניים"]
N_CLASSES = 1                                  # the Java above: GameClock is the whole pattern (Main is the client)
assert CLOCK.count("class ") == N_CLASSES
OPTS = w.opts_of(Q)

ONE = w.uml("one", [dict(key="gc", name="GameClock", x=220, y=20, w=560,
                         members=["- instance : GameClock   (static)", "- GameClock()", "+ getInstance() : GameClock"])],
            w=1000, h=210)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נכיר את Singleton: תבנית שמבטיחה מופע אחד בלבד."),
    P("נכתוב את שלושת המרכיבים שלה, נריץ אותה, ונראה מה שובר אותה."),
    P("ובסוף נפתור שאלה ממבחן.", hold=0.4),
], stage='<div class="kicker">P02 · תבניות עיצוב</div><h1>Singleton: מופע אחד בלבד</h1>'
         '<p>לזהות מתי צריך Singleton, לכתוב את שלושת המרכיבים שלה, ולמצוא למה היא מייצרת כמה מופעים.</p>', layout="title")

idea = Scene("idea", "הרעיון", [
    P("במשחק רשת יש שעון משחק. המפה מקדמת אותו, ולוח התוצאות מציג אותו.", do=show("i-1")),
    P("אם כל רכיב ייצור לעצמו שעון, כל אחד יראה זמן אחר, והמשחק יתפרק.", do=show("i-2")),
    P("הצורך: **מופע אחד** של השעון, שכל המערכת ניגשת אליו מנקודה אחת.", do=show("i-3")),
    P("זו Singleton, ממשפחת היצירה. היא שימושית כשהאובייקט שולט במשאב שחייב להיות אחד.", do=show("i-c1")),
    P("ומה היא לא עושה? היא לא עוסקת באמינות, בזמינות, או במספר הלקוחות של המערכת. רק במספר המופעים.",
      do=show("i-c2"), hold=0.4),
], stage=w.stack(st.card("i-1", "ex", "🗺️ המפה מקדמת את השעון · 🏆 לוח התוצאות קורא אותו"),
                 st.card("i-2", "trap", "⚠️ שני שעונים = שני זמנים שונים"),
                 f'<div id="i-3" class="card rule h" style="font-size:36px">🔑 מופע <b>אחד</b>, נקודת גישה <b>אחת</b></div>',
                 gap=30),
   panel=st.card("i-c1", "rule", "🔑 משאב שחייב להיות אחד ← Singleton")
         + st.card("i-c2", "plain", "לא אמינות, לא זמינות, לא ״לקוח אחד״"))

parts = Scene("parts", "שלושה מרכיבים", [
    P("הנה המחלקה. יש בה שלושה מרכיבים, וכולם בתוך מחלקה אחת.", do=show("c")),
    P("אחת: **שדה סטטי** מהטיפוס של המחלקה עצמה. הוא מחזיק את המופע היחיד.", do=show(f"c-m{L_FIELD}", "p-1")),
    P("סטטי, כי הוא שייך למחלקה ולא לאף מופע, ולכן יש ממנו עותק אחד בלבד."),
    P("שתיים: **בנאי פרטי**. אף קוד מחוץ למחלקה לא יכול ליצור ממנה אובייקט חדש.",
      do=hide(f"c-m{L_FIELD}") + show(f"c-m{L_CTOR}", "p-2")),
    P("שלוש: **מתודה סטטית ציבורית** שמחזירה את המופע. קוראים לה בלי אובייקט, דרך שם המחלקה.",
      do=hide(f"c-m{L_CTOR}") + show(f"c-m{L_GET0}", "p-3")),
    P("בקריאה הראשונה השדה ריק, ולכן היא יוצרת את המופע. בכל קריאה אחר כך היא מחזירה אותו.",
      do=hide(f"c-m{L_GET0}") + show(f"c-m{L_IF}", f"c-m{L_RET}"), hold=0.4),
], stage=w.code("c", CLOCK, hidden=True, size=25),
   panel=st.card("p-1", "ex", "1️⃣ שדה " + w.mono("static") + " שמחזיק את המופע")
         + st.card("p-2", "ex", "2️⃣ בנאי " + w.mono("private"))
         + st.card("p-3", "ex", "3️⃣ " + w.mono("static getInstance()") + " שיוצרת פעם אחת"))

STATE = w.swap("s", [w.chip("s-null", "השדה: " + w.mono("null"), "bad", False),
                     w.chip("s-one", "השדה: מופע אחד של השעון", "ok", False)], 70, width=700)
run = Scene("run", "הרצה", [
    P("נריץ. המפה מבקשת את השעון ומקדמת אותו בשנייה.", do=show("m", "m-m2")),
    P("זו הקריאה הראשונה, והשדה עדיין ריק. לכן נוצר שעון, והבנאי מדפיס הודעה.", do=hide("s-0") + show("s-1", "o-1")),
    P("עכשיו לוח התוצאות מבקש את השעון. השדה כבר מלא, ולכן הוא מקבל את **אותו** שעון, ומקדם אותו.",
      do=hide("m-m2") + show("m-m3")),
    P("ובסוף מדפיסים את הזמן: שתיים. שתי השניות נספרו על אותו אובייקט.", do=hide("m-m3") + show("m-m4", "o-2")),
    P("וההודעה של הבנאי הודפסה פעם אחת בלבד: נוצר שעון אחד.", do=show("r-c1"), hold=0.4),
], stage=w.stack(w.code("m", MAIN, hidden=True, size=23), STATE,
                 f'<div class="pt-out h" id="o" style="font-size:26px"><span class="pt-olab">פלט</span><div class="pt-obody" dir="ltr">'
                 f'<div id="o-1" class="h">clock created</div><div id="o-2" class="h">2</div></div></div>', gap=22),
   panel=st.card("r-c1", "rule", "🔑 שלוש קריאות, <b>מופע אחד</b>. ההודעה של הבנאי הודפסה פעם אחת"))
run.phrases[0].do += show("o")

brk = Scene("break", "מה שובר אותה", [
    P("ומה שובר את התבנית? נניח שמישהו שכח, וכתב את הבנאי **ציבורי**.", do=show("b-pub")),
    P("עכשיו כל קוד יכול לכתוב new ולייצר שעון בעצמו.", do=show("b", "b-m2"),
      say="עכשיו כל קוד יכול לכתוב נְיוּ ולייצר שעון בעצמו."),
    P("הרצנו את זה: נוצרים **שני** שעונים, והשני מראה אפס. במערכת יש שני זמנים.", do=show("b-o")),
    P("עם בנאי פרטי, אותה שורה בכלל לא עוברת קומפילציה: הבנאי לא נגיש מחוץ למחלקה.", do=show("b-err")),
    P("כך הבנאי הפרטי והמתודה הסטטית עובדים יחד: הדרך היחידה לקבל שעון עוברת דרך המתודה.", do=show("b-c1"), hold=0.4),
], stage=w.stack(w.code("b-pub", "public GameClock() { ... }   // the mistake", hidden=True, size=24),
                 w.code("b", BREAK, hidden=True, size=22),
                 w.out("b-o", OUT_PUB, label="פלט, עם בנאי ציבורי", size=24),
                 w.out("b-err", "error: GameClock() has private access in GameClock", label="קומפילציה, עם בנאי פרטי", size=22),
                 gap=18),
   panel=st.card("b-c1", "rule", "🔑 בנאי " + w.mono("private") + " ← הדרך היחידה לשעון: " + w.mono("getInstance()")))

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו שאלה ממבחן: כמה מחלקות יש בתרשים המחלקות של Singleton?"),
    P("נסתכל על מה שכתבנו. כל התבנית היא מחלקה **אחת**: השעון.", do=show("one")),
    P("השדה שמחזיק את המופע הוא מהטיפוס של המחלקה עצמה. זו לא מחלקה נוספת.", do=show("one-hb-gc")),
    P("ואין צורך במחלקה אחרת שתיצור את המופע: המחלקה יוצרת את עצמה, בתוך המתודה הסטטית.", do=show("x-1")),
    P("אז התשובה היא אחת. ואחת לא מופיעה ברשימה! לכן כל המספרים נופלים: שתיים, שלוש וארבע.",
      do=show("q-x-4", "q-x-1", "q-x-0", "q-n-4", "q-n-1", "q-n-0")),
    P("ו״תלוי בסוג״? גם כשמממשים אחרת, למשל יוצרים את המופע מראש, זו אותה מחלקה אחת.",
      do=show("q-x-2", "q-n-2", "x-2")),
    P("לכן התשובה היא ״כל התשובות האחרות שגויות״.", do=show("q-ok-3")),
    P("וזו המלכודת: כשהמספר הנכון חסר, לא בוחרים את הקרוב אליו. בודקים קודם את כל האפשרויות.", do=show("x-t"), hold=0.5),
], stage=w.stack(ONE, st.card("x-1", "rule", "🔑 המחלקה יוצרת את עצמה ← אין מחלקה נוספת"),
                 st.card("x-2", "ex", "גם יצירה מראש (בלי " + w.mono("if") + ") = אותה מחלקה אחת"),
                 st.card("x-t", "trap", "⚠️ התשובה הנכונה (אחת) חסרה ← ״כל האחרות שגויות״"), gap=18),
   panel=w.stem(Q["id"], "בתרשים מחלקות של התבנית Singleton מספר המחלקות הוא:")
         + st.options("q", OPTS, notes={0: "לא 4", 1: "לא 3", 4: "לא 2", 2: "תמיד אחת"}))

recap = Scene("recap", "סיכום", [
    P("לסיכום: Singleton מבטיחה מופע אחד, כשהאובייקט שולט במשאב שחייב להיות אחד.", do=show("r-1")),
    P("שלושה מרכיבים במחלקה אחת: שדה סטטי, בנאי פרטי, ומתודה סטטית שמחזירה את המופע.", do=show("r-2")),
    P("ובהרצה ראינו: עם בנאי פרטי, שורת היצירה מבחוץ לא עברה קומפילציה. נתראה ברמה הבאה.", do=show("r-3"), hold=0.6),
], stage=w.stack(ONE.replace('id="one', 'id="z'), gap=20),
   panel=st.card("r-1", "rule", "🔑 משאב אחד ← Singleton")
         + st.card("r-2", "rule", "🔑 " + w.mono("static") + " · " + w.mono("private") + " · " + w.mono("getInstance()"))
         + st.card("r-3", "ex", w.mono("new GameClock()") + " מבחוץ ← שגיאת קומפילציה"))

SCENES = [title, idea, parts, run, brk, exam, recap]
w.no_latin(SCENES)
VIDEO = Video("P02", "pat", "Singleton: מופע אחד בלבד", SCENES, bank={"26B-A-Q18": 3})
