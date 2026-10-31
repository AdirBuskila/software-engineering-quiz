# -*- coding: utf-8 -*-
"""P04 · Observer: Subject, Observer ופעולות Attach ו-Notify — video script (build: tools/video/vid.py P04).

Source: courses/pat/P04.js (lesson + goal: who holds whom, what each of attach / detach / notify / update does, and
who gets an update after a sequence of operations). Exam part: an original question "בסגנון מבחן" (bank={}): after attach / goal / attach /
goal / detach / goal, how many updates did each screen get (app 2, tv 2). 24B-A-Q10 (Detach) was dropped as too close
to the quiz item 24B-B-Q9 (Attach); 24B-A-Q11 and 25S-A-Q8 are not used either. Operation descriptions avoid the
wording of those options ("לחבר/לנתק observer מסויים אל/מן ה-Subject").
Who owns each operation comes from the course checker (w_pat.OBSERVER_OPS). The trace is computed twice: by a
Python mirror below and by compiling and running the Java on screen (w_pat.java); both give
app 1, tv 1, tv 2, bot 2. Java's Object already has a final notify(), so the method is called notifyObservers().
Avoided on purpose: the P04 quiz items (who holds the list, the attach a,b,c / detach b trace, the change -> notify
flow, "which operation runs on the Observer", 24B-B-Q9, 24B-A-Q11). My own case: a football match and three screens.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_pat as w

assert w.OBSERVER_OPS == {"update": "Observer", "attach": "Subject", "detach": "Subject", "notify": "Subject"}

# ---------------------------------------------------------------- code (compiled and run) + a Python mirror
SUBJ = """class Match {                       // the Subject
  private final List<Observer> observers = new ArrayList<>();
  private int score;
  void attach(Observer o) { observers.add(o); }
  void detach(Observer o) { observers.remove(o); }
  void notifyObservers() {
    for (Observer o : observers) o.update(score);
  }
  void goal() { score++; notifyObservers(); }
}"""
OBS = """interface Observer { void update(int score); }

class Screen implements Observer {
  private final String name;
  Screen(String name) { this.name = name; }
  public void update(int score) { System.out.println(name + " got " + score); }
}"""
MAIN_BODY = """m.attach(app);
m.attach(tv);
m.goal();
m.detach(app);
m.attach(bot);
m.goal();"""
MAIN = ("public class Main {\n  public static void main(String[] args) {\n    Match m = new Match();\n"
        '    Screen app = new Screen("app"), tv = new Screen("tv"), bot = new Screen("bot");\n'
        + "\n".join("    " + l for l in MAIN_BODY.split("\n")) + "\n  }\n}")
OUT = "app got 1\ntv got 1\ntv got 2\nbot got 2"
w.java({"Match": "import java.util.ArrayList;\nimport java.util.List;\n\n" + SUBJ, "Observer": OBS, "Main": MAIN},
       "Main", OUT)


def mirror():
    obs, score, got, lists = [], 0, [], []
    for line in MAIN_BODY.split("\n"):
        op, arg = line[2:].split("(")
        arg = arg.rstrip(");")
        if op == "attach":
            obs.append(arg)
        elif op == "detach":
            obs.remove(arg)
        else:
            score += 1
            got += [f"{o} got {score}" for o in obs]
        lists.append(list(obs))
    return got, lists


GOT, LISTS = mirror()
assert "\n".join(GOT) == OUT
assert LISTS == [["app"], ["app", "tv"], ["app", "tv"], ["tv"], ["tv", "bot"], ["tv", "bot"]]

# exam-style question (original): count the updates each screen gets
EX_BODY = """m.attach(app);
m.goal();
m.attach(tv);
m.goal();
m.detach(app);
m.goal();"""
EX_MAIN = ("public class Main {\n  public static void main(String[] args) {\n    Match m = new Match();\n"
           '    Screen app = new Screen("app"), tv = new Screen("tv");\n'
           + "\n".join("    " + l for l in EX_BODY.split("\n")) + "\n  }\n}")
EX_OUT = "app got 1\napp got 2\ntv got 2\ntv got 3"
w.java({"Match": "import java.util.ArrayList;\nimport java.util.List;\n\n" + SUBJ, "Observer": OBS, "Main": EX_MAIN},
       "Main", EX_OUT)
COUNT = {n: EX_OUT.count(n + " got") for n in ("app", "tv")}
assert COUNT == {"app": 2, "tv": 2}
EX_OPTS = [(2, 2), (3, 3), (3, 2), (2, 3)]
assert [c == (COUNT["app"], COUNT["tv"]) for c in EX_OPTS] == [True, False, False, False]
OPTS = [(k, f'{w.mono("app")}: {a} · {w.mono("tv")}: {t}') for k, (a, t) in enumerate(EX_OPTS)]

UML = w.uml("u", [
    dict(key="m", name="Match", x=40, y=40, w=400, role="Subject: מי שמשתנה",
         members=["- observers : List<Observer>", "+ attach(o)", "+ detach(o)", "+ notifyObservers()"]),
    dict(key="o", name="Observer", x=600, y=60, w=360, kind="interface", members=["+ update(score)"]),
    dict(key="s", name="Screen", x=640, y=360, w=280, members=["+ update(score)"], role="Observer: מי שמגיב", hidden=True),
], [
    dict(key="has", a="m", b="o", kind="has", sides="rl", fa=0.3, fb=0.5, label="*", lxy=(560, 95), hidden=True),
    dict(key="impl", a="s", b="o", kind="impl", sides="tb", hidden=True),
], w=1000, h=500, scale=1.0)

ROST = w.swap("ro", [w.roster(f"ro-r{k}", names, "הרשימה של ה-Subject:")
                     for k, names in enumerate([[]] + LISTS)], 70, width=900)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נכיר את Observer: תבנית שבה שינוי במקום אחד מגיע לכל מי שמעוניין."),
    P("נלמד את ארבע הפעולות שלה, ונעקוב צעד אחר צעד אחרי מי מקבל עדכון."),
    P("ובסוף נפתור שאלה ממבחן.", hold=0.4),
], stage='<div class="kicker">P04 · תבניות עיצוב</div><h1>Observer: Subject, Observer ופעולות Attach ו-Notify</h1>'
         '<p>לדעת מי מחזיק את מי ב-Observer, מה עושה כל אחת מהפעולות, ולעקוב אחרי מי מקבל עדכון.</p>', layout="title")

idea = Scene("idea", "שני תפקידים", [
    P("משחק כדורגל. כשנכבש שער, האפליקציה, הטלוויזיה ובוט התוצאות צריכים לדעת.", do=show("u")),
    P("המשחק הוא ה-**Subject**: האובייקט שמשתנה.", do=show("u-hb-m")),
    P("המסכים הם ה-**Observers**: אובייקטים שרוצים לדעת כשה-Subject משתנה.", do=hide("u-hb-m") + show("u-hb-o")),
    P("ה-Subject **מחזיק** רשימה של Observers. זה קשר של הכלה, ולא ירושה.", do=hide("u-hb-o") + show("u-a-has", "i-c1")),
    P("והוא לא מכיר אותם בפרטים. הוא יודע רק שלכל אחד יש פעולת update.", do=show("u-b-s", "u-a-impl")),
    P("לכן אפשר להוסיף מסך חדש בלי לשנות את המשחק בכלל.", do=show("i-c2")),
    P("ומי שנרשם, פשוט מחכה. העדכון יגיע אליו כשיגיע.", hold=0.4),
], stage=UML.replace('class="pt-uml"', 'class="pt-uml h"', 1),
   panel=st.card("i-c1", "rule", "🔑 ה-Subject <b>מחזיק</b> את רשימת ה-Observers")
         + st.card("i-c2", "ex", "מסך חדש = עוד רישום, בלי לשנות את המשחק"))

OPS = [("attach", "Attach", "מוסיפה Observer לרשימה"), ("detach", "Detach", "מסירה Observer מהרשימה"),
       ("notify", "notify", "עוברת על הרשימה ושולחת update לכל אחד"), ("update", "update", "כאן ה-Observer מקבל את העדכון")]
TABLE = ('<table class="delta" id="t" dir="rtl" style="font-size:30px"><thead><tr><th>פעולה</th><th>נקראת על</th>'
         '<th>מה היא עושה</th></tr></thead><tbody>'
         + "".join(f'<tr id="t-{k}" class="h"><td>{w.mono(n)}</td><td>{w.OBSERVER_OPS[k]}</td><td>{d}</td></tr>' for k, n, d in OPS)
         + "</tbody></table>")
ops = Scene("ops", "ארבע פעולות", [
    P("ארבע פעולות, ולכל אחת יש בעלים.", do=show("t")),
    P("Attach: המשחק מקבל מסך, ומכניס אותו לרשימה שלו.", do=show("t-attach", "c", "c-m3")),
    P("Detach: המשחק מקבל מסך, ומוציא **רק אותו** מהרשימה.", do=hide("c-m3") + show("t-detach", "c-m4")),
    P("notify: ה-Subject עובר על כל הרשימה, ושולח לכל Observer עדכון.", do=hide("c-m4") + show("t-notify", "c-m5", "c-m6")),
    P("ו-update: הפעולה של ה-Observer. בה הוא מקבל את העדכון ומגיב.", do=hide("c-m5", "c-m6") + show("t-update")),
    P("בקוד שלנו update מקבלת את התוצאה החדשה, וכל מסך מחליט בעצמו מה לעשות איתה."),
    P("שלוש הראשונות נקראות על ה-Subject, והאחרונה על ה-Observer.", do=show("o-c1")),
    P("ולמסך אין רשימה בכלל. לכן הוספה והסרה קורות תמיד אצל המשחק.", do=show("o-c2"), hold=0.4),
], stage=w.stack(TABLE, w.code("c", SUBJ, hidden=True, size=21), gap=20),
   panel=st.card("o-c1", "rule", "🔑 Attach · Detach · notify ← על ה-Subject<br>update ← על ה-Observer")
         + st.card("o-c2", "ex", "הרשימה רק אצל המשחק"))

trace = Scene("trace", "מי מקבל עדכון?", [
    P("עכשיו נעקוב. המשחק מתחיל, והרשימה שלו ריקה.", do=show("mn")),
    P("מחברים את האפליקציה, ואחריה את הטלוויזיה. ברשימה שני Observers.",
      do=show("mn-m0", "mn-m1") + hide("ro-0") + show("ro-2")),
    P("נכבש שער. notify עוברת על הרשימה: האפליקציה והטלוויזיה מקבלות את התוצאה: אחת.",
      do=hide("mn-m0", "mn-m1") + show("mn-m2", "ot", "ot-0", "ot-1")),
    P("עכשיו מנתקים את האפליקציה. רק היא יוצאת מהרשימה, והטלוויזיה נשארת.",
      do=hide("mn-m2", "ro-2") + show("mn-m3", "ro-4")),
    P("ומחברים את הבוט. ברשימה: הטלוויזיה והבוט.", do=hide("mn-m3", "ro-4") + show("mn-m4", "ro-5")),
    P("שער שני. הפעם מקבלים עדכון הטלוויזיה והבוט. האפליקציה כבר לא שומעת כלום.",
      do=hide("mn-m4") + show("mn-m5", "ot-2", "ot-3")),
    P("הרצנו את הקוד, וזה בדיוק הפלט. מי שמקבל עדכון הוא מי שברשימה **ברגע** ה-notify.", do=show("tr-c1"), hold=0.4),
], stage=w.stack(w.code("mn", MAIN_BODY, hidden=True, size=28), ROST,
                 f'<div class="pt-out h" id="ot" style="font-size:26px"><span class="pt-olab">פלט</span><div class="pt-obody" dir="ltr">'
                 + "".join(f'<div id="ot-{k}" class="h">{l}</div>' for k, l in enumerate(OUT.split("\n"))) + "</div></div>",
                 gap=22),
   panel=st.card("tr-c1", "rule", "🔑 מקבלים update = מי שרשום <b>ברגע</b> ה-notify"))

EX_ROST = w.swap("er", [w.roster(f"er-r{k}", names, "ברשימה:") for k, names in
                         enumerate([[], ["app"], ["app", "tv"], ["tv"]])], 64, width=700)
exam = Scene("exam", "שאלה בסגנון מבחן", [
    P("ועכשיו שאלה בסגנון מבחן: שש פקודות על המשחק. כמה עדכונים יקבל כל מסך?", do=show("ex")),
    P("כלל אחד מספיק: מקבלים עדכון רק מי שברשימה ברגע ה-notify. נעבור לפי הסדר."),
    P("האפליקציה נרשמת, ונכבש שער. רק היא ברשימה: האפליקציה, אחד.", do=show("ex-m0", "ex-m1", "er-1") + hide("er-0")),
    P("הטלוויזיה נרשמת, ושער שני. עכשיו שתיהן ברשימה: האפליקציה שתיים, הטלוויזיה אחד.",
      do=hide("ex-m0", "ex-m1", "er-1") + show("ex-m2", "ex-m3", "er-2")),
    P("האפליקציה יוצאת, ושער שלישי. רק הטלוויזיה שומעת: הטלוויזיה שתיים.",
      do=hide("ex-m2", "ex-m3", "er-2") + show("ex-m4", "ex-m5", "er-3")),
    P("סך הכול: שתיים ושתיים. הרצנו את הקוד, וזה הפלט.", do=hide("ex-m4", "ex-m5") + show("q-ok-0", "eo")),
    P("שלוש ושלוש? זה מניח שכולם שומעים הכול. אבל הטלוויזיה לא הייתה ברשימה בשער הראשון.",
      do=show("q-x-1", "q-n-1")),
    P("שלוש לאפליקציה? היא יצאה מהרשימה לפני השער השלישי.", do=show("q-x-2", "q-n-2")),
    P("ושלוש לטלוויזיה? הרשמה לא משלימה עדכונים שכבר עברו.", do=show("q-x-3", "q-n-3"), hold=0.5),
], stage=w.stack(w.code("ex", EX_BODY, hidden=True, size=26), EX_ROST, w.out("eo", EX_OUT, size=24), gap=18),
   panel=w.tight('<div class="qstem"><span class="qid">בסגנון מבחן</span>על המשחק מתבצעות הפקודות שמשמאל, לפי הסדר. '
                 'כמה עדכונים יקבל כל מסך?</div>'
                 + st.options("q", OPTS, notes={1: "לא כולם", 2: "יצאה", 3: "אין השלמה"})))

recap = Scene("recap", "סיכום", [
    P("לסיכום: ה-Subject משתנה ומחזיק רשימה. ה-Observers מגיבים.", do=show("r-1")),
    P("Attach ו-Detach משנות את הרשימה, אחד בכל פעם. notify עוברת עליה ושולחת update.",
      do=show("r-2")),
    P("ומי מקבל עדכון? מי שברשימה ברגע ה-notify. נתראה ברמה הבאה.", do=show("r-3"), hold=0.6),
], stage=w.stack(TABLE.replace('id="t', 'id="zt').replace(' class="h"', ""), gap=20),
   panel=st.card("r-1", "rule", "🔑 Subject מחזיק · Observers מגיבים")
         + st.card("r-2", "rule", "🔑 Attach / Detach / notify ← Subject · update ← Observer")
         + st.card("r-3", "rule", "🔑 מקבלים = הרשומים ברגע ה-notify"))

SCENES = [title, idea, ops, trace, exam, recap]
w.no_latin(SCENES)
VIDEO = Video("P04", "pat", "Observer: Subject, Observer ופעולות Attach ו-Notify", SCENES, bank={})
