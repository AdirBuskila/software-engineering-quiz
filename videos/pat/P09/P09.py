# -*- coding: utf-8 -*-
"""P09 · מבחן גמר: תבניות עיצוב — boss walkthrough (build: tools/video/vid.py P09).

Source: courses/pat/P09.js (boss lesson: the whole-course table and the three steps — need sentence, pattern, check the
roles). Walkthrough of three exam questions that no guided quiz or boss uses and that have no twin in the bank:
  19B-C-Q8   what Factory Method creates per the user's request -> the instance
  19B-B-Q7   when Singleton is useful -> the object controls a limited resource in the system
  25F0b-Q8   the relation between Command and Invoker -> containment
The Java on screen is compiled and run here (w_pat.java): the factory call returns a Circle instance (prints
"circle 3.14"); the Invoker class compiles with a Command field and never extends Command.
Avoided on purpose: the six boss items of P09 (25S-A-Q10, 25F0a-Q8, 26S-A-Q17, 26B-A-Q19, 24B-B-Q11, 24B-B-Q8) and all
quiz items of P01..P08; 21-A-Q9 and its twins (how Factory Method does it) are not shown either. 25B-N-Q10 (stock
prices on several displays) was dropped: its scenario is the one of the P05 quiz item 25F0a-Q10. 19B-B-Q7 is explained
with my own resource (a phone's single GPS chip), not the print queue of P02-Q3 / 24B-B-Q10.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_pat as w

# ---------------------------------------------------------------- code (compiled and run)
FAC = """interface Shape { double area(); }
class Circle implements Shape { public double area() { return 3.14; } }
class Square implements Shape { public double area() { return 1.0; } }
class ShapeFactory {
  static Shape create(String kind) {
    if (kind.equals("circle")) return new Circle();
    return new Square();
  }
}"""
CALL = 'Shape s = ShapeFactory.create("circle");'
MAIN = ("public class Main {\n  public static void main(String[] args) {\n    " + CALL + "\n"
        '    System.out.println(s.getClass().getSimpleName().toLowerCase() + " " + s.area());\n  }\n}')
w.java({"Shape": FAC, "Main": MAIN}, "Main", "circle 3.14")

INV = """interface Command { void execute(); }
class Invoker {
  private Command slot;                 // holds a Command
  void set(Command c) { slot = c; }
  void press() { slot.execute(); }
}"""
w.java({"Command": INV, "Main": 'public class Main {\n  public static void main(String[] args) {\n    Invoker i = new Invoker();\n'
        '    i.set(() -> System.out.println("ran"));\n    i.press();\n  }\n}'}, "Main", "ran")
assert "extends" not in INV and "implements" not in INV.split("class Invoker")[1]

assert w.solves("Observer", {"notify_many_on_change"}) and w.solves("MVC", {"separate_ui_data"})
for p in ("Singleton", "Command", "Factory"):
    assert not w.solves(p, {"notify_many_on_change"})

Q1, Q2, Q3 = BANK["19B-C-Q8"], BANK["19B-B-Q7"], BANK["25F0b-Q8"]
assert Q1["correctIndex"] == 3 and "המופע" in Q1["options"][3]
assert [k for k, o in enumerate(Q1["options"]) if "המשתנה" in o or "הממשק" in o or "המחלקה" in o] == [0, 1, 2]
assert Q2["correctIndex"] == 0 and "משאב מצומצם" in Q2["options"][0]
assert "אמינות" in Q2["options"][1] and "לקוח אחד" in Q2["options"][2] and "מוזיקליות" in Q2["options"][3]
assert w.solves("Singleton", {"shared_resource"}) and not w.solves("Singleton", {"notify_many_on_change"})
assert Q3["correctIndex"] == 2 and Q3["options"] == ["ירושה", "אין קשר ישיר", "הכלה", "כל התשובות האחרות שגויות", "הפעלה"]

INVU = w.uml("iv", [
    dict(key="i", name="Invoker", x=40, y=40, w=330, members=["- slot : Command", "+ press()"]),
    dict(key="c", name="Command", x=600, y=40, w=330, kind="interface", members=["+ execute()"]),
], [dict(key="has", a="i", b="c", kind="has", sides="rl", fa=0.45, fb=0.5, label="הכלה", lxy=(485, 80), anchor="middle")],
    w=1000, h=220)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("זה מבחן הגמר של הקורס. נפתור יחד שלוש שאלות אמיתיות מהמבחנים."),
    P("בכל אחת נשתמש באותם שלושה צעדים, ונפיל כל מסיח עם סיבה.", hold=0.4),
], stage='<div class="kicker">P09 · תבניות עיצוב</div><h1>מבחן גמר: תבניות עיצוב</h1>'
         '<p>שלוש שאלות אמיתיות מהמבחנים על Factory, Singleton ו-Command.</p>', layout="title")

method = Scene("method", "שלושה צעדים", [
    P("תזכורת לשיטה. אחת: מנסחים את הצורך במשפט אחד.", do=show("m-1")),
    P("שתיים: בוחרים את התבנית שעונה עליו.", do=show("m-2")),
    P("שלוש: בודקים את **התפקידים** בתשובה. לפעמים התבנית נכונה, והתפקידים הפוכים.", do=show("m-3"), hold=0.4),
], stage=w.stack(st.card("m-1", "ex", "1️⃣ הצורך במשפט אחד"), st.card("m-2", "ex", "2️⃣ התבנית"),
                 st.card("m-3", "ex", "3️⃣ התפקידים בתשובה, עד הסוף"), gap=26),
   panel=st.card("m-c", "trap", "⚠️ תשובה ארוכה ומפורטת היא לא בהכרח נכונה").replace(" h\"", "\""))

q1 = Scene("q1", "שאלה 1 · Factory", [
    P("שאלה ראשונה: התבנית Factory Method יוצרת את מה, בהתאם לבקשת המשתמש?"),
    P("נסתכל על קריאה אחת. הלקוח מבקש מבית החרושת צורה, ומעביר את המחרוזת עיגול.", do=show("f-call")),
    P("בזמן ריצה, בתוך המתודה, נוצר אובייקט חדש של עיגול. אובייקט שנוצר מתוך מחלקה הוא **מופע**.",
      do=show("f-l-i", "q1-ok-3")),
    P("המחלקה, עיגול, נכתבה בקוד עוד לפני ההרצה. מתודה לא יוצרת מחלקות בזמן ריצה.", do=show("f-l-c", "q1-x-2", "q1-n-2")),
    P("גם הממשק, צורה, כתוב מראש. הוא רק הטיפוס שהמתודה מחזירה.", do=show("f-l-t", "q1-x-1", "q1-n-1")),
    P("והמשתנה נמצא אצל הלקוח: הוא רק מחזיק את מה שהמתודה החזירה.", do=show("f-l-v", "q1-x-0", "q1-n-0")),
    P("אז Factory Method יוצרת את **המופע** הרלוונטי. הרצנו את הקוד, ויצא עיגול.", do=show("f-o")),
    P("המלכודת: ארבע התשובות זהות חוץ ממילה אחת. לכן שואלים על כל מילה: מה באמת נוצר בזמן ריצה?", hold=0.5),
], stage=w.stack(w.code("f-call", CALL, hidden=True, size=30),
                 '<div class="pt-row" style="gap:14px;flex-wrap:wrap;width:980px">'
                 + w.chip("f-l-v", w.mono("s") + " = משתנה, אצל הלקוח", "")
                 + w.chip("f-l-t", w.mono("Shape") + " = ממשק, כתוב מראש", "st")
                 + w.chip("f-l-c", w.mono("Circle") + " = מחלקה, כתובה מראש", "be")
                 + w.chip("f-l-i", "האובייקט החדש = <b>מופע</b>, נוצר בריצה", "ok") + "</div>",
                 w.out("f-o", "circle 3.14", size=26), gap=26),
   panel=w.tight(w.stem(Q1["id"], "תבנית העיצוב Factory Method:")
                 + st.options("q1", w.opts_of(Q1), notes={0: "אצל הלקוח", 1: "כתוב מראש", 2: "כתובה מראש"})))

q2 = Scene("q2", "שאלה 2 · Singleton", [
    P("שאלה שנייה: מתי תבנית Singleton שימושית?"),
    P("צעד ראשון, הצורך של התבנית: בדיוק **מופע אחד** של מחלקה, שכל המערכת ניגשת אליו.", do=show("g-1")),
    P("מתי זה חשוב? כשהאובייקט שולט במשהו שיש ממנו רק אחד. למשל שבב הג׳י פי אס היחיד בטלפון.", do=show("g-2"),
      say="מתי זה חשוב? כשהאובייקט שולט במשהו שיש ממנו רק אחד. למשל שבב הג'י פי אֶס היחיד בטלפון."),
    P("אם שתי אפליקציות ייצרו כל אחת אובייקט משלה ששולט בשבב, הן יתנגשו. לכן משאב מצומצם הוא התשובה.",
      do=show("q2-ok-0")),
    P("דרישות אמינות וזמינות הן דרישות איכות של כל המערכת. הן לא אומרות כלום על מספר המופעים של מחלקה.",
      do=show("q2-x-1", "q2-n-1")),
    P("״מערכת אחת ללקוח אחד״ מבלבלת בין מערכת שלמה לבין אובייקט בתוך הקוד.", do=show("q2-x-2", "q2-n-2")),
    P("ומערכות מוזיקליות? רק משחק מילים על ״סינגל״. אין לזה קשר לתבנית.", do=show("q2-x-3", "q2-n-3")),
    P("המלכודת: המילה ״אחד״ מופיעה גם במסיח. אבל ״אחד״ של התבנית הוא מופע אחד של מחלקה.", do=show("g-t"), hold=0.5),
], stage=w.stack(st.card("g-1", "rule", "🔑 Singleton = מופע <b>אחד</b> של מחלקה"),
                 st.card("g-2", "ex", "📡 שבב GPS אחד בטלפון ← אובייקט אחד ששולט בו"),
                 st.card("g-t", "trap", "⚠️ ״לקוח אחד״ / ״מערכת אחת״ ≠ מופע אחד"), gap=26),
   panel=w.tight(w.stem(Q2["id"], "תבנית תיכון מסוג סינגלטון שימושית כאשר")
                 + st.options("q2", w.opts_of(Q2), notes={1: "דרישת איכות", 2: "מערכת ≠ מופע", 3: "משחק מילים"})))

q3 = Scene("q3", "שאלה 3 · Command", [
    P("שאלה שלישית: בתבנית Command, איזה קשר יש בין ה-Command ל-Invoker?"),
    P("ה-Invoker הוא המפעיל. כדי להפעיל פקודה, הוא צריך **להחזיק** אותה.", do=show("iv", "iv-a-has")),
    P("בקוד: שדה מטיפוס הפקודה, בתוך ה-Invoker. מחלקה שמחזיקה אובייקט אחר בשדה, זה קשר של הכלה.",
      do=show("ic", "ic-m2", "q3-ok-2")),
    P("ירושה? ה-Invoker הוא לא סוג של פקודה. הוא לא יורש ממנה, וגם לא מממש אותה.", do=show("q3-x-0", "q3-n-0")),
    P("״אין קשר ישיר״? יש: השדה הזה הוא בדיוק קשר ישיר.", do=show("q3-x-1", "q3-n-1")),
    P("ובתרשים, הקשר מסומן בקו עם מעוין, בצד של מי שמחזיק: ה-Invoker."),
    P("ו״הפעלה״? זה מה שה-Invoker **עושה** עם הפקודה, אבל זה לא סוג של קשר בין מחלקות.",
      do=show("q3-x-4", "q3-n-4", "ic-m4")),
    P("ויש תשובה נכונה, ולכן ״כל האחרות שגויות״ נופלת.", do=show("q3-x-3", "q3-n-3"), hold=0.5),
], stage=w.stack(INVU.replace('class="pt-uml"', 'class="pt-uml h"', 1), w.code("ic", INV, hidden=True, size=26), gap=24),
   panel=w.tight(w.stem(Q3["id"], "בתבנית ה-Command קיים קשר בין ה-Command ל-Invoker של?")
                 + st.options("q3", w.opts_of(Q3), notes={0: "לא סוג של", 1: "יש שדה", 3: "יש נכונה", 4: "פעולה, לא קשר"})))

recap = Scene("recap", "סיכום הקורס", [
    P("לסיכום הקורס: מופע אחד הוא Singleton. סוג שנקבע בזמן ריצה הוא Factory.", do=show("r-1")),
    P("משהו משתנה וכמה רכיבים מתעדכנים: Observer. פעולות כאובייקטים, עם ביטול: Command.", do=show("r-2")),
    P("והפרדה בין נתונים, תצוגה ובקרה: MVC. ובכל שאלה, בודקים את התפקידים עד הסוף. בהצלחה במבחן!",
      do=show("r-3"), hold=0.6),
], stage=w.stack(*[w.need(f"z-{k}", n, p, hidden=False) for k, (n, p) in enumerate([
    ("מופע אחד, משאב יחיד", "Singleton"), ("סוג נקבע בזמן ריצה", "Factory"),
    ("משתנה ← כמה רכיבים מתעדכנים", "Observer"), ("כפתורים, פעולות, undo", "Command"),
    ("נתונים · תצוגה · בקרה", "MVC")])], gap=16),
   panel=st.card("r-1", "rule", "🔑 Singleton · Factory: יצירה")
         + st.card("r-2", "rule", "🔑 Observer · Command: התנהגות")
         + st.card("r-3", "trap", "⚠️ תבנית נכונה + תפקידים הפוכים = תשובה שגויה"))

SCENES = [title, method, q1, q2, q3, recap]
w.no_latin(SCENES)
VIDEO = Video("P09", "pat", "מבחן גמר: תבניות עיצוב", SCENES, bank={"19B-C-Q8": 3, "19B-B-Q7": 0, "25F0b-Q8": 2})
