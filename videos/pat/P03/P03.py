# -*- coding: utf-8 -*-
"""P03 · Factory: מי יוצר את האובייקט? — video script (build: tools/video/vid.py P03).

Source: courses/pat/P03.js (lesson + goal: when Factory fits, what the calling code sees, Factory vs Abstract
Factory). Exam anchor: 22B-A-Q11 (what problem Factory Method solves -> separating the code that creates objects from
the code that uses them), which no guided quiz uses and has no twin in the bank.
The Java on screen is compiled and run here (w_pat.java): the client asks the factory for "drone" and "ship" and gets
1 and 20 days, without naming a concrete class.
Avoided on purpose: the P03 quiz items (Notifier/Sms/Email, payment methods, "advantage of Factory" = 24S-A-Q8's twin,
Windows/Mac Abstract Factory = 23-EX-Q9's twin, 25S-A-Q9, 21-A-Q9 and its twins 21S-A-Q9 / SP-AMR-Q17 / 24B-A-Q12),
the parser example (boss 25F0a-Q8) and the notification items 26S-A-Q16 / 26CL-Q12. My own example: delivery methods
(truck, drone, ship) and dark/light UI themes.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_pat as w

# ---------------------------------------------------------------- code (compiled and run)
LIB = """interface Delivery { int days(); }
class Truck implements Delivery { public int days() { return 3; } }
class Drone implements Delivery { public int days() { return 1; } }
class Ship implements Delivery { public int days() { return 20; } }

class DeliveryFactory {
  static Delivery create(String kind) {
    if (kind.equals("drone")) return new Drone();
    if (kind.equals("ship")) return new Ship();
    return new Truck();
  }
}"""
MAIN = """public class Main {
  public static void main(String[] args) {
    for (String choice : new String[] {"drone", "ship"}) {
      Delivery d = DeliveryFactory.create(choice);
      System.out.println(choice + " -> " + d.days());
    }
  }
}"""
OUT = "drone -> 1\nship -> 20"
w.java({"Delivery": LIB, "Main": MAIN}, "Main", OUT)
L_SIG, L_IF1, L_IF2, L_DEF = 6, 7, 8, 9
assert "static Delivery create(String kind)" in LIB.split("\n")[L_SIG]
assert "new Truck()" in LIB.split("\n")[L_DEF]
for c in ("Truck", "Drone", "Ship"):            # the client never names a concrete class
    assert c not in MAIN
NEED = {"runtime_type", "hide_concrete_classes", "extensible_types"}
assert [p for p in w.RULES if w.solves(p, NEED)] == ["Factory"]
assert w.solves("AbstractFactory", {"family_of_objects"}) and not w.solves("Factory", {"family_of_objects"})

# exam 22B-A-Q11
Q = BANK["22B-A-Q11"]
assert Q["correctIndex"] == 2 and Q["options"][2].startswith("הפרדה בין הקוד שמיצר")
assert "aggregation" in Q["options"][1] and "בדיקות" in Q["options"][0] and "שיורשים מאותה מחלקה" in Q["options"][3]
OPTS = w.opts_of(Q)

UML = w.uml("u", [
    dict(key="main", name="Main", x=40, y=40, w=200, role="הלקוח"),
    dict(key="fac", name="DeliveryFactory", x=500, y=26, w=460, members=["+ create(kind) : Delivery"], hidden=True),
    dict(key="del", name="Delivery", x=40, y=230, w=260, kind="interface", members=["+ days() : int"]),
    dict(key="tr", name="Truck", x=500, y=450, w=150),
    dict(key="dr", name="Drone", x=670, y=450, w=150),
    dict(key="sh", name="Ship", x=840, y=450, w=150),
], [
    dict(key="mf", a="main", b="fac", kind="call", sides="rl", label="create(kind)", lxy=(280, 40), hidden=True),
    dict(key="md", a="main", b="del", kind="call", sides="bt", fa=0.85, fb=0.65, hidden=False),
    dict(key="i1", a="tr", b="del", kind="impl", sides="tb", fb=0.5, elbow=True, hidden=False),
    dict(key="i2", a="dr", b="del", kind="impl", sides="tb", fb=0.5, elbow=True, hidden=False),
    dict(key="i3", a="sh", b="del", kind="impl", sides="tb", fb=0.5, elbow=True, hidden=False),
    dict(key="c1", a="fac", b="tr", kind="dep", sides="bt", fa=75 / 460),
    dict(key="c2", a="fac", b="dr", kind="dep", sides="bt", fa=245 / 460, label="«creates»", lxy=(765, 300)),
    dict(key="c3", a="fac", b="sh", kind="dep", sides="bt", fa=415 / 460),
], w=1000, h=520, scale=0.95)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נשאל: מי יוצר את האובייקט, ומי משתמש בו?"),
    P("נכיר את Factory, נריץ אותה, ונראה במה היא שונה מ-Abstract Factory."),
    P("ובסוף נפתור שאלה ממבחן.", hold=0.4),
], stage='<div class="kicker">P03 · תבניות עיצוב</div><h1>Factory: מי יוצר את האובייקט?</h1>'
         '<p>לזהות מתי Factory מתאימה, להסביר מה הקוד הקורא רואה, ולהבדיל בין Factory ל-Abstract Factory.</p>', layout="title")

idea = Scene("idea", "הבעיה", [
    P("חנות מקוונת שולחת חבילות: במשאית, ברחפן או באונייה. הלקוח בוחר בזמן ההזמנה.", do=show("i-1")),
    P("הדרך הישירה: בכל מקום בקוד בודקים מה נבחר, ויוצרים בעצמנו משאית, רחפן או אונייה.", do=show("i-2")),
    P("אז הקוד שמשתמש במשלוח **מכיר את כל המחלקות הקונקרטיות**.", do=show("i-c1")),
    P("ומחר מוסיפים משלוח באופניים? צריך לעבור על כל המקומות האלה ולשנות אותם.", do=show("i-c2")),
    P("הצורך: סוג האובייקט נקבע רק בזמן ריצה, והקוד הקורא לא רוצה להכיר את המחלקות. זו Factory.",
      do=show("i-3"), hold=0.4),
], stage=w.stack(st.card("i-1", "ex", "🚚 משאית · 🛸 רחפן · 🚢 אונייה, לפי בחירת הלקוח"),
                 w.code("i-2", 'if (choice.equals("drone")) d = new Drone();\nelse if (choice.equals("ship")) d = new Ship();\n'
                        'else d = new Truck();', hidden=True, size=26, title="בכל מקום שצריך משלוח:"),
                 f'<div id="i-3" class="card rule h" style="font-size:34px">🔑 סוג בזמן ריצה + לא להכיר מחלקות ← <b>Factory</b></div>',
                 gap=24),
   panel=st.card("i-c1", "trap", "⚠️ הקוד הקורא תלוי במחלקות הקונקרטיות")
         + st.card("i-c2", "trap", "⚠️ סוג חדש = שינוי בכל המקומות"))

fac = Scene("factory", "בית החרושת", [
    P("Factory היא מחלקה שתפקידה ליצור עצמים של מחלקות אחרות. הנה היא.", do=show("f")),
    P("קודם, ממשק משותף: כל משלוח יודע לומר בכמה ימים הוא מגיע.", do=show("f-m0")),
    P("שלוש מחלקות קונקרטיות מממשות אותו: משאית, רחפן ואונייה.", do=hide("f-m0") + show("f-m1", "f-m2", "f-m3")),
    P("ועכשיו הטריק: המתודה של בית החרושת מחזירה את **הממשק**, ולא מחלקה קונקרטית.",
      do=hide("f-m1", "f-m2", "f-m3") + show(f"f-m{L_SIG}", "f-c1")),
    P("היא מקבלת פרמטר, הבקשה של הלקוח, ולפיו מחליטה איזה מופע ליצור.",
      do=hide(f"f-m{L_SIG}") + show(f"f-m{L_IF1}", f"f-m{L_IF2}", f"f-m{L_DEF}")),
    P("כל היצירה הישירה של המשלוחים נמצאת עכשיו במקום **אחד**: בתוך בית החרושת.", do=show("f-c2"), hold=0.4),
], stage=w.code("f", LIB, hidden=True, size=23),
   panel=st.card("f-c1", "rule", "🔑 טיפוס ההחזרה: הממשק " + w.mono("Delivery"))
         + st.card("f-c2", "rule", "🔑 כל היצירה במקום אחד"))

client = Scene("client", "הקוד הקורא", [
    P("ומה רואה הקוד הקורא? הוא מבקש מבית החרושת משלוח, ומעביר את הבחירה.", do=show("m", "m-m3")),
    P("הרצנו: רחפן מגיע ביום אחד, ואונייה בעשרים ימים.", do=show("o")),
    P("שימו לב: בקוד הקורא לא מופיע אף שם של מחלקה קונקרטית. רק הממשק.", do=hide("m-m3") + show("m-m4", "c-c1"), hold=0.3),
    P("ובתרשים: הלקוח מחובר לממשק ולבית החרושת. אין לו שום קו אל המשאית, הרחפן או האונייה.",
      do=hide("m", "o", "m-m4") + show("u", "u-b-fac", "u-a-mf")),
    P("רק בית החרושת יוצר אותן.", do=show("u-a-c1", "u-a-c2", "u-a-c3", "u-hb-fac")),
    P("ואם נוסיף משלוח באופניים? מחלקה חדשה, ועוד שורה בבית החרושת. בקוד הקורא לא נוגעים.", do=show("c-c2"), hold=0.4),
], stage='<div class="swap" style="--swap-h:640px">'
         + f'<div id="cm">{w.stack(w.code("m", MAIN, hidden=True, size=24), w.out("o", OUT, size=26), gap=24)}</div>'
         + f'<div>{UML.replace(chr(60) + "svg class=" + chr(34) + "pt-uml", chr(60) + "svg class=" + chr(34) + "pt-uml h", 1)}</div>'
         + "</div>",
   panel=st.card("c-c1", "rule", "🔑 הלקוח מכיר רק את הממשק")
         + st.card("c-c2", "ex", "🚲 סוג חדש: מחלקה + שורה בבית החרושת. הלקוח לא משתנה"))

abst = Scene("abstract", "Abstract Factory", [
    P("ומה זה Abstract Factory? בית חרושת שיוצר **משפחה** של אובייקטים שמתאימים זה לזה."),
    P("למשל ערכת נושא באפליקציה: מצב כהה ומצב בהיר.", do=show("a-0")),
    P("בית החרושת הכהה יוצר כפתור כהה ותפריט כהה. הבהיר יוצר כפתור בהיר ותפריט בהיר.", do=show("a-1", "a-2")),
    P("כך אי אפשר לקבל בטעות כפתור כהה עם תפריט בהיר: כל המשפחה באה מאותו מקום.", do=show("a-c1")),
    P("ההבדל: Factory Method יוצרת מוצר **אחד** לפי בקשה. Abstract Factory יוצרת משפחה שלמה.", do=show("a-c2"), hold=0.4),
], stage=w.stack(
    w.chip("a-0", "ממשק: " + w.mono("ThemeFactory") + " · " + w.mono("button()") + " · " + w.mono("menu()"), "st"),
    f'<div id="a-1" class="pt-row h" style="gap:16px"><span class="pt-chip be pt-mono">DarkFactory</span><span class="pt-fa">→</span>'
    f'<span class="pt-chip pt-mono">DarkButton</span><span class="pt-chip pt-mono">DarkMenu</span></div>',
    f'<div id="a-2" class="pt-row h" style="gap:16px"><span class="pt-chip cr pt-mono">LightFactory</span><span class="pt-fa">→</span>'
    f'<span class="pt-chip pt-mono">LightButton</span><span class="pt-chip pt-mono">LightMenu</span></div>', gap=34),
   panel=st.card("a-c1", "rule", "🔑 משפחה של מוצרים שמתאימים זה לזה")
         + st.card("a-c2", "ex", "Factory Method: מוצר אחד · Abstract Factory: משפחה"))

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו שאלה ממבחן: איזו בעיה פותרת התבנית Factory Method?"),
    P("ראינו את זה בקוד: היצירה עברה לבית החרושת, והקוד הקורא רק משתמש במשלוח.", do=show("x-1")),
    P("כלומר, הפרדה בין הקוד שמייצר את האובייקטים לבין הקוד שמשתמש בהם. זו התשובה.", do=show("q-ok-2")),
    P("״ליצור אובייקטים שונים שיורשים מאותה מחלקה״ נשמע קרוב מאוד. אבל זו המלכודת.", do=show("x-t")),
    P("את זה אפשר לעשות בלי שום תבנית: יוצרים משאית, ויוצרים רחפן. ירושה רגילה מספיקה.",
      do=show("q-x-3", "q-n-3")),
    P("הבעיה ש-Factory פותרת היא **איפה** היצירה קורית, ומי צריך להכיר את המחלקות.", do=show("x-2")),
    P("ממשק אחיד למחלקות עם קשר של הכלה? הממשק ב-Factory משותף למוצרים, ולא קשור להכלה.",
      do=show("q-x-1", "q-n-1")),
    P("וכתיבת בדיקות לפרויקטי ייצור? זו תבנית עיצוב, ולא שיטת בדיקות. המילה ״ייצור״ פשוט מבלבלת.",
      do=show("q-x-0", "q-n-0"), hold=0.5),
], stage=w.stack(st.card("x-1", "ex", "יצירה: בבית החרושת · שימוש: בקוד הקורא"),
                 st.card("x-t", "trap", "⚠️ ״אובייקטים שונים שיורשים מאותה מחלקה״: אפשרי גם בלי Factory"),
                 st.card("x-2", "rule", "🔑 Factory = <b>איפה</b> יוצרים, ומי לא צריך להכיר את המחלקות"), gap=26),
   panel=w.tight(w.stem(Q["id"], "תבנית העיצוב Factory Method פותרת איזו בעיה?")
                 + st.options("q", OPTS, notes={0: "לא בדיקות", 1: "לא הכלה", 3: "ירושה רגילה"})))

recap = Scene("recap", "סיכום", [
    P("לסיכום: Factory מתאימה כשהסוג נקבע בזמן ריצה, והקוד הקורא לא צריך להכיר מחלקות קונקרטיות.", do=show("r-1")),
    P("המתודה מקבלת פרמטר ומחזירה ממשק. כל היצירה במקום אחד, וסוג חדש לא משנה את הלקוח.", do=show("r-2")),
    P("ו-Abstract Factory יוצרת משפחה של אובייקטים מתאימים. נתראה ברמה הבאה.", do=show("r-3"), hold=0.6),
], stage=w.stack(w.reprefix(UML, "u", "zu", reveal=True), gap=20),
   panel=st.card("r-1", "rule", "🔑 סוג בזמן ריצה ← Factory")
         + st.card("r-2", "rule", "🔑 מחזירה ממשק · הלקוח מנותק מהמחלקות")
         + st.card("r-3", "rule", "🔑 משפחה של מוצרים ← Abstract Factory"))

SCENES = [title, idea, fac, client, abst, exam, recap]
w.no_latin(SCENES)
VIDEO = Video("P03", "pat", "Factory: מי יוצר את האובייקט?", SCENES, bank={"22B-A-Q11": 2})
