# -*- coding: utf-8 -*-
"""P05 · Observer בתרגיל: תפקידים, תרשים וסינון — video script (build: tools/video/vid.py P05).

Source: courses/pat/P05.js (lesson + goal: cast components as Subject / Observers in a description, read the class
diagram, know that the Subject's own operations decide who gets what). Exam anchor: 24S-A-Q7 (sending updates by
priority -> in Attach the Subject inserts the Observer into a priority queue), which no guided quiz uses and has no
twin in the bank.
The priority Subject on screen is compiled and run here (w_pat.java) and mirrored in Python: attached with priorities
3, 1, 2, the observers hear the bid in the order 1, 2, 3.
Avoided on purpose: the P05 quiz items (WeatherStation roles, one Dashboard on two stations = 25F0b-Q10's twin,
filtering in notify = boss 24B-B-Q8 and its twin 25B-N-Q11, 24B-B-Q7 and its twins 25F0a-Q16 / 26B-A-Q17 on the
inheritance arrow, 25F0a-Q10 StockPriceTracker) and the Ticket item 26S-A-Q17 (boss). The diagram is shown for
reading roles; the video does not pose the inheritance-arrow question.
The title says "סדר עדכונים" (not the level's "סינון"): the video teaches order, set in Attach, and says explicitly that
nobody is filtered out; filtering itself (P05-Q3 / boss 24B-B-Q8) is not taught here. The diagram shows exactly the
Java classes (Auction with attach(o, p), the Observer interface, one Watcher class). The role reversal is described in
general words, not in the wording of 26S-A-Q17's option. My own case: an online auction.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_pat as w

assert w.solves("Observer", {"notify_many_on_change"})
assert w.OBSERVER_OPS["attach"] == "Subject" and w.OBSERVER_OPS["notify"] == "Subject"

# ---------------------------------------------------------------- code (compiled and run) + Python mirror
SUBJ = """class Auction {                        // the Subject
  private final List<Observer> queue = new ArrayList<>();
  private final List<Integer> prio = new ArrayList<>();
  private int bid;
  void attach(Observer o, int p) {
    int i = 0;
    while (i < prio.size() && prio.get(i) <= p) i++;
    queue.add(i, o);
    prio.add(i, p);
  }
  void notifyObservers() { for (Observer o : queue) o.update(bid); }
  void newBid(int amount) { bid = amount; notifyObservers(); }
}"""
OBS = """interface Observer { void update(int bid); }

class Watcher implements Observer {
  private final String name;
  Watcher(String name) { this.name = name; }
  public void update(int bid) { System.out.println(name + " sees " + bid); }
}"""
BODY = """a.attach(log, 3);
a.attach(app, 1);
a.attach(hall, 2);
a.newBid(120);"""
MAIN = ("public class Main {\n  public static void main(String[] args) {\n    Auction a = new Auction();\n"
        '    Watcher log = new Watcher("log"), app = new Watcher("app"), hall = new Watcher("hall");\n'
        + "\n".join("    " + l for l in BODY.split("\n")) + "\n  }\n}")
OUT = "app sees 120\nhall sees 120\nlog sees 120"
w.java({"Auction": "import java.util.ArrayList;\nimport java.util.List;\n\n" + SUBJ, "Observer": OBS, "Main": MAIN},
       "Main", OUT)

q = []                                           # mirror: stable insertion by priority, as in attach above
for name, p in [("log", 3), ("app", 1), ("hall", 2)]:
    i = 0
    while i < len(q) and q[i][1] <= p:
        i += 1
    q.insert(i, (name, p))
assert [n for n, _ in q] == ["app", "hall", "log"] and "\n".join(f"{n} sees 120" for n, _ in q) == OUT
L_ATT, L_WHILE, L_ADD, L_NOT = 4, 6, 7, 10
assert "void attach" in SUBJ.split("\n")[L_ATT] and "while" in SUBJ.split("\n")[L_WHILE]
assert "notifyObservers()" in SUBJ.split("\n")[L_NOT]

# roles of the worked scenario
ROLES = {"Auction": "Subject", "app": "Observer", "hall": "Observer", "log": "Observer"}

# exam 24S-A-Q7
Q = BANK["24S-A-Q7"]
assert Q["correctIndex"] == 1 and "ה – Subject יוסיף את ה – Observer" in Q["options"][1] and "Attach" in Q["options"][1]
assert "Detach" in Q["options"][2] and "notify" in Q["options"][3] and "ה – Observer יוסיף את ה – Subject" in Q["options"][4]
OPTS = w.opts_of(Q)

UML = w.uml("u", [                       # the classes of the Java below, nothing more
    dict(key="a", name="Auction", x=30, y=30, w=420, role="Subject",
         members=["- queue : List<Observer>", "+ attach(o, p)", "+ notifyObservers()"]),
    dict(key="o", name="Observer", x=600, y=40, w=340, kind="interface", members=["+ update(bid)"]),
    dict(key="b1", name="Watcher", x=620, y=330, w=300, role="app · hall · log", hidden=True,
         members=["- name : String", "+ update(bid)"]),
], [
    dict(key="has", a="a", b="o", kind="has", sides="rl", fa=0.3, label="*", lxy=(560, 70), hidden=False),
    dict(key="i1", a="b1", b="o", kind="impl", sides="tb"),
], w=1000, h=520)
assert "List<Observer> queue" in SUBJ and "void attach(Observer o, int p)" in SUBJ and "class Watcher implements Observer" in OBS

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה ניקח את Observer לתרגיל: נשבץ רכיבים בתפקידים, ונקרא את התרשים."),
    P("ונראה מי מחליט באיזה סדר מגיעים העדכונים."),
    P("ובסוף נפתור שאלה ממבחן.", hold=0.4),
], stage='<div class="kicker">P05 · תבניות עיצוב</div><h1>Observer בתרגיל: תפקידים, תרשים וסדר עדכונים</h1>'
         '<p>לשבץ רכיבים בתפקידי Subject ו-Observer בתיאור מערכת, לקרוא את תרשים המחלקות, ולדעת מי קובע את סדר העדכונים.</p>',
   layout="title")

CHIPS = [("Auction", "המכרז: ההצעה הגבוהה משתנה"), ("app", "אפליקציית המציעים"),
         ("hall", "המסך באולם"), ("log", "יומן המחירים")]
roles = Scene("roles", "מי משתנה, מי מגיב", [
    P("מכרז מקוון. בכל פעם שמגיעה הצעה חדשה, המחיר הנוכחי משתנה.", do=show("c-0")),
    P("אפליקציית המציעים, המסך באולם ויומן המחירים צריכים לדעת על כל הצעה.", do=show("c-1", "c-2", "c-3")),
    P("שאלה אחת מסדרת הכול: **מי משתנה, ומי מגיב?**", do=show("r-c1")),
    P("המכרז הוא זה שמשתנה. לכן הוא ה-Subject.", do=show("c-0-r")),
    P("שלושת האחרים מגיבים לשינוי. לכן הם ה-Observers.", do=show("c-1-r", "c-2-r", "c-3-r")),
    P("הטעות הנפוצה היא להפוך את התפקידים, ולשים את המסכים במקום של מי שמשתנה.", do=show("r-c2")),
    P("אבל מסך לא משתנה מעצמו. הוא מציג את מה שהשתנה במקום אחר."),
    P("ולכן בכל שאלת תפקידים בודקים שני דברים: שהתבנית נכונה, ושהתפקידים לא הפוכים.", hold=0.4),
], stage=w.stack(*[f'<div id="c-{k}" class="pt-need h"><span class="pt-nd">{he} · {w.mono(en)}</span><span class="pt-arr">←</span>'
                   f'<span id="c-{k}-r" class="pt-pat h">{ROLES[en]}</span></div>' for k, (en, he) in enumerate(CHIPS)], gap=22),
   panel=st.card("r-c1", "rule", "🔑 משתנה ← Subject · מגיב ← Observer")
         + st.card("r-c2", "trap", "⚠️ הטעות הנפוצה: תפקידים הפוכים"))

diag = Scene("diagram", "התרשים", [
    P("עכשיו התרשים. משמאל המכרז, ה-Subject. בתוכו רשימת ה-Observers.", do=show("u", "u-hb-a")),
    P("הקו עם המעוין אומר שהמכרז **מחזיק** הרבה Observers. זה קשר הכלה.", do=hide("u-hb-a") + show("u-a-has", "d-c1")),
    P("מימין, הממשק של ה-Observer: פעולה אחת, update.", do=show("u-hb-o")),
    P("ובקוד, שלושת הרכיבים הם מופעים של מחלקה אחת שמממשת את הממשק הזה: הצופה.",
      do=hide("u-hb-o") + show("u-b-b1", "u-a-i1")),
    P("המכרז מכיר רק את הממשק. הוא לא יודע שיש אפליקציה, מסך או יומן.", do=show("d-c2")),
    P("ולכן להוסיף מנוי רביעי זה רק עוד Attach. את המכרז לא משנים.", do=show("d-c3"), hold=0.4),
], stage=UML.replace('class="pt-uml"', 'class="pt-uml h"', 1),
   panel=st.card("d-c1", "rule", "🔑 מעוין = <b>הכלה</b>: ה-Subject מחזיק Observers")
         + st.card("d-c2", "ex", "ה-Subject מכיר רק את " + w.mono("update"))
         + st.card("d-c3", "ex", "מנוי חדש = עוד " + w.mono("attach") + ", בלי לשנות את ה-Subject"))

prio = Scene("priority", "סדר העדכונים", [
    P("ומה אם חשוב **הסדר**? האפליקציה צריכה לשמוע ראשונה, אחריה האולם, והיומן אחרון."),
    P("מי מחליט על הסדר? מי שמחזיק את הרשימה: ה-Subject.", do=show("p-c1")),
    P("הנה המכרז. Attach מקבלת Observer וגם עדיפות.", do=show("s", f"s-m{L_ATT}")),
    P("היא מחפשת את המקום הנכון לפי העדיפות, ומכניסה אותו לשם. הרשימה נשארת ממוינת.",
      do=hide(f"s-m{L_ATT}") + show(f"s-m{L_WHILE}", f"s-m{L_ADD}")),
    P("ו-notify פשוט עוברת על הרשימה לפי הסדר. היא בכלל לא צריכה לדעת על עדיפויות.",
      do=hide(f"s-m{L_WHILE}", f"s-m{L_ADD}") + show(f"s-m{L_NOT}")),
    P("נרשמו בסדר: יומן בעדיפות שלוש, אפליקציה באחת, אולם בשתיים.", do=hide("s") + show("b", "b-m0", "b-m1", "b-m2")),
    P("הצעה של מאה עשרים. הרצנו: האפליקציה ראשונה, אחריה האולם, והיומן אחרון.", do=hide("b-m0", "b-m1", "b-m2") + show("b-m3", "bo")),
    P("שימו לב: אף אחד לא סונן. כולם קיבלו את אותו מחיר, ורק הסדר נקבע ב-Attach, כשה-Subject הכניס כל אחד למקומו.",
      do=show("p-c2"), hold=0.4),
], stage='<div class="swap" style="--swap-h:640px">'
         + f'<div>{w.code("s", SUBJ, hidden=True, size=21)}</div>'
         + f'<div>{w.stack(w.code("b", BODY, hidden=True, size=28), w.out("bo", OUT, size=26), gap=24)}</div></div>',
   panel=st.card("p-c1", "rule", "🔑 מי שמחזיק את הרשימה מחליט: ה-Subject")
         + st.card("p-c2", "rule", "🔑 עדיפות: נקבעת ב-" + w.mono("attach") + " של ה-Subject"))

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו השאלה מהמבחן: בתבנית Observer, כיצד אפשר לשלוח עדכונים לפי עדיפות?"),
    P("בדיוק מה שבנינו: ב-Attach, ה-Subject מוסיף את ה-Observer לתור לפי עדיפות. זו התשובה.", do=show("q-ok-1", "x-1")),
    P("ההפוכה שלה, ״ה-Observer מוסיף את ה-Subject״, נראית כמעט זהה. אבל ל-Observer אין רשימה.",
      do=show("q-x-4", "q-n-4")),
    P("וב-notify ה-Observers לא קובעים כלום: זו פעולה של ה-Subject, והם רק מקבלים update.",
      do=show("q-x-3", "q-n-3")),
    P("Detach מסירה Observer מהרשימה. הסרה לא מסדרת את מי שנשאר.", do=show("q-x-2", "q-n-2")),
    P("ויש תשובה נכונה, ולכן ״כל האחרות שגויות״ נופלת.", do=show("q-x-0", "q-n-0")),
    P("המלכודת כאן: שתי תשובות עם Attach. קוראים עד הסוף **מי** מוסיף את **מי**.", do=show("x-t"), hold=0.5),
], stage=w.stack(w.code("xs", "\n".join(l[2:] for l in SUBJ.split("\n")[L_ATT:L_ATT + 6]), hidden=False, size=24),
                 st.card("x-1", "rule", "🔑 Subject.attach(o, p) ← הכנסה לפי עדיפות"),
                 st.card("x-t", "trap", "⚠️ שתי תשובות עם Attach: מי מוסיף את מי?"), gap=24),
   panel=w.tight(w.stem(Q["id"], "בתבנית ה-Observer, כיצד ניתן לשלוח עדכונים ע״פ עדיפות?")
                 + st.options("q", OPTS, notes={0: "יש נכונה", 2: "הסרה", 3: "של ה-Subject", 4: "כיוון הפוך"})))

recap = Scene("recap", "סיכום", [
    P("לסיכום: מי שמשתנה הוא ה-Subject, ומי שמגיב הוא Observer. התפקידים לא מתחלפים.", do=show("r-1")),
    P("בתרשים, ה-Subject מחזיק רשימה של Observers, ומכיר רק את הממשק שלהם.", do=show("r-2")),
    P("וכל החלטה על הרשימה, כמו סדר לפי עדיפות, היא של ה-Subject. נתראה ברמה הבאה.", do=show("r-3"), hold=0.6),
], stage=w.stack(w.reprefix(UML, "u", "zu", reveal=True), gap=20),
   panel=st.card("r-1", "rule", "🔑 משתנה = Subject · מגיב = Observer")
         + st.card("r-2", "rule", "🔑 Subject מחזיק Observers (הכלה)")
         + st.card("r-3", "rule", "🔑 עדיפות ← ב-" + w.mono("attach") + " של ה-Subject"))

SCENES = [title, roles, diag, prio, exam, recap]
w.no_latin(SCENES)
VIDEO = Video("P05", "pat", "Observer בתרגיל: תפקידים, תרשים וסדר עדכונים", SCENES, bank={"24S-A-Q7": 1})
