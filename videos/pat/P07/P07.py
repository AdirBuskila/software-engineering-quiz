# -*- coding: utf-8 -*-
"""P07 · MVC: Model, View ו-Controller — video script (build: tools/video/vid.py P07).

Source: courses/pat/P07.js (lesson + goal: cast classes into the three MVC layers, how information flows between them,
why a view is easy to replace). Exam anchor: 25F0b-Q14 (a product catalogue with four components; which sentence can
describe it under MVC -> the graphical user interface, component 4, acts as the View), which no guided quiz uses.
The Java on screen is compiled and run here (w_pat.java): borrowing "Dune" twice prints "Dune borrowed" and then
"Dune not available"; the rule lives in the Model, the Controller only passes it on, the View only shows.
The allowed edges are the course checker's: view <-> controller <-> model (no view <-> model edge).
Lesson rules are taught through the library case only, never in the wording of a quiz or boss
option (no "useful for complex UIs", no "Model manages data and business logic / Controller updates the Model",
no "view and model never talk", no "easy to replace the View").
Avoided on purpose: the P07 quiz items (CartScreen / CartController / Cart, "who receives the click", adding a mobile
screen = 25F0a-Q13's twin, 19B-B-Q8, SP-DGM-Q15), the boss item 24B-B-Q11, the lesson's Ticket example (26B-A-Q14)
and the MVC + Observer stock item 25B-N-Q10 (used in the P09 walkthrough). My own case: a library's loan screen.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_pat as w

assert w.solves("MVC", {"separate_ui_data"})
EDGES = {("View", "Controller"), ("Controller", "Model"), ("Model", "Controller"), ("Controller", "View")}
assert ("View", "Model") not in EDGES and ("Model", "View") not in EDGES

# ---------------------------------------------------------------- code (compiled and run)
LIB = """class Library {                          // Model: data + business rule
  private final Set<String> onLoan = new HashSet<>();
  boolean borrow(String title) { return onLoan.add(title); }
}

class SearchScreen {                     // View: shows, decides nothing
  void show(String msg) { System.out.println(msg); }
}

class LoanController {                   // Controller: between the two
  private final Library model;
  private final SearchScreen view;
  LoanController(Library m, SearchScreen v) { model = m; view = v; }
  void onBorrowClicked(String title) {
    boolean ok = model.borrow(title);
    view.show(ok ? title + " borrowed" : title + " not available");
  }
}"""
BODY = """LoanController c = new LoanController(new Library(), new SearchScreen());
c.onBorrowClicked("Dune");
c.onBorrowClicked("Dune");"""
MAIN = "public class Main {\n  public static void main(String[] args) {\n" + "\n".join("    " + l for l in BODY.split("\n")) + "\n  }\n}"
OUT = "Dune borrowed\nDune not available"
w.java({"Library": "import java.util.HashSet;\nimport java.util.Set;\n\n" + LIB, "Main": MAIN}, "Main", OUT)
on_loan = set()
got = []
for _ in range(2):                                       # Python mirror: Set.add returns False the second time
    ok = "Dune" not in on_loan
    on_loan.add("Dune")
    got.append("Dune borrowed" if ok else "Dune not available")
assert "\n".join(got) == OUT
L = LIB.split("\n")
L_MODEL, L_RULE, L_VIEW, L_CTRL, L_CALL, L_SHOW = 0, 2, 5, 9, 14, 15
assert L[L_MODEL].startswith("class Library") and "onLoan.add" in L[L_RULE] and L[L_VIEW].startswith("class SearchScreen")
assert L[L_CTRL].startswith("class LoanController") and "model.borrow" in L[L_CALL] and "view.show" in L[L_SHOW]
assert "Library" not in "\n".join(L[L_VIEW:L_CTRL])      # the View never touches the Model

# exam 25F0b-Q14
Q = BANK["25F0b-Q14"]
assert Q["correctIndex"] == 3 and Q["options"][3] == "רכיב 4 יתפקד כ – VIEW"
assert Q["options"][2] == "רכיב 2 יתפקד כ – VIEW" and Q["options"][4] == "רכיב 3 יתפקד כ – VIEW"
assert Q["options"][0] == "לא ניתן לדעת" and "4. ממשק משתמש גרפי" in Q["question"]
assert "2. שירות שמאפשר לחשב תמחור" in Q["question"] and "3. תהליך Batch" in Q["question"]
OPTS = w.opts_of(Q)


def node(id_, he, en, hidden=False):
    return f'<div id="{id_}" class="pt-node{" h" if hidden else ""}">{he}<span class="pt-sub pt-mono">{en}</span></div>'


FLOW = ('<div class="pt-flow" id="fl">'
        + node("n-v", "תצוגה", "View · SearchScreen") + '<span class="pt-fa">⇄</span>'
        + node("n-c", "בקר", "Controller · LoanController") + '<span class="pt-fa">⇄</span>'
        + node("n-m", "מודל", "Model · Library") + "</div>")

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נפרק אפליקציה לשלוש שכבות: Model, View ו-Controller."),
    P("נראה מה כל שכבה עושה, איך המידע זורם ביניהן, ולמה זה משתלם."),
    P("ובסוף נפתור שאלה ממבחן.", hold=0.4),
], stage='<div class="kicker">P07 · תבניות עיצוב</div><h1>MVC: Model, View ו-Controller</h1>'
         '<p>לשבץ מחלקות בשלוש השכבות של MVC, לדעת איך המידע זורם ביניהן, ולהסביר למה קל להחליף תצוגה.</p>', layout="title")

LAYERS = [("l-m", "Model", "מה שהאפליקציה יודעת, והכללים שלה", "אילו ספרים מושאלים, ומתי מותר להשאיל"),
          ("l-v", "View", "מה שהמשתמש רואה ולוחץ עליו", "מסך החיפוש והכפתור ״השאל״"),
          ("l-c", "Controller", "המתווך: מתרגם לחיצה לבקשה מהמודל", "מקבל את הלחיצה ומבקש מהספרייה להשאיל")]
layers = Scene("layers", "שלוש שכבות", [
    P("אפליקציה של ספרייה. משתמש מחפש ספר, ולוחץ ״השאל״."),
    P("איפה כל חלק של הקוד צריך לשבת? בשביל זה שלוש שכבות."),
    P("ה-**Model**: מה שהאפליקציה יודעת, והכללים שלה. כאן רשום אילו ספרים מושאלים, ומתי מותר להשאיל.", do=show("l-m")),
    P("ה-**View**: מה שהמשתמש רואה. מסך החיפוש והכפתור. הוא מציג, ולא מחליט שום דבר.", do=show("l-v")),
    P("וה-**Controller**: המתווך. הוא שומע את הלחיצה, ומבקש מהספרייה להשאיל.", do=show("l-c")),
    P("לכל שורת קוד יש עכשיו בית אחד: כללים במודל, מסכים בתצוגה, ותיווך בבקר.", do=show("y-c1"), hold=0.4),
], stage=w.stack(*[f'<div id="{i}" class="pt-need h"><span class="pt-pat" style="min-width:190px">{en}</span>'
                   f'<span class="pt-nd"><b>{he}</b><br><span style="color:var(--muted);font-size:26px">{ex}</span></span></div>'
                   for i, en, he, ex in LAYERS], gap=24),
   panel=st.card("y-c1", "rule", "🔑 כללים ← Model · מסכים ← View · תיווך ← Controller"))

flow = Scene("flow", "איך המידע זורם", [
    P("עכשיו הזרימה. המשתמש לוחץ ״השאל״ על התצוגה.", do=show("fl", "n-v-on")),
    P("התצוגה לא בודקת כלום. היא מעבירה את הלחיצה לבקר.", do=show("c", f"c-m{L_CTRL}")),
    P("הבקר פונה למודל ומבקש להשאיל.", do=hide(f"c-m{L_CTRL}") + show(f"c-m{L_CALL}")),
    P("והכלל עצמו, ״אי אפשר להשאיל ספר שכבר מושאל״, נמצא **במודל**.", do=hide(f"c-m{L_CALL}") + show(f"c-m{L_RULE}")),
    P("התשובה חוזרת דרך הבקר, והוא אומר לתצוגה מה להציג.", do=hide(f"c-m{L_RULE}") + show(f"c-m{L_SHOW}")),
    P("הרצנו שתי לחיצות על אותו ספר: בראשונה הוא הושאל, ובשנייה הוא כבר לא זמין.", do=hide(f"c-m{L_SHOW}") + show("o")),
    P("וגם ההודעה ״לא זמין״ לא הוחלטה בתצוגה. הבקר בחר מה להציג, לפי התשובה של המודל."),
    P("ושימו לב לקוד של המסך: אין בו שום אזכור של הספרייה. רק הבקר מחזיק את שניהם.", do=show("f-c1"), hold=0.4),
], stage=w.stack(FLOW.replace('class="pt-flow"', 'class="pt-flow h"'), w.code("c", LIB, hidden=True, size=19), gap=16),
   panel=w.out("o", OUT, size=26) + st.card("f-c1", "rule", "🔑 הבקר מחזיק את המסך ואת הספרייה. המסך לא מכיר את הספרייה"))
flow.phrases[0].do = show("fl")

swapv = Scene("swap", "למה זה משתלם", [
    P("ולמה כל זה טוב? כי השכבות מופרדות.", do=show("s-1")),
    P("הכלל של ההשאלה נמצא במודל. אם נבנה מסך אחר, כמו קיוסק בכניסה לספרייה, הכלל לא זז.", do=show("s-2")),
    P("הקיוסק צריך רק קוד תצוגה משלו. הספרייה והבקר נשארים כמו שהם.", do=show("s-c1")),
    P("ואם הלוגיקה הייתה כתובה בתוך המסך? כל מסך חדש היה צריך להעתיק אותה, ובסוף היו שני כללים שונים."),
    P("אבל השכבות עדיין עובדות יחד, ולכן צריך לתכנן היטב את הממשק ביניהן.", do=show("s-c2"), hold=0.4),
], stage=w.stack(st.card("s-1", "ex", "Model: הכלל, פעם אחת"),
                 st.card("s-2", "ex", "View חדש (קיוסק) ← אותו Controller, אותו Model"), gap=24),
   panel=st.card("s-c1", "rule", "🔑 מסך חדש = רק קוד תצוגה חדש")
         + st.card("s-c2", "plain", "השכבות קשורות: מתכננים את הממשק ביניהן"))

COMPS = [("x-1", "1", "שירות ליצירה, עדכון והסרה של מוצרים", "נתונים ולוגיקה"),
         ("x-2", "2", "חישוב תמחור דינמי לפי סוג הלקוח", "לוגיקה עסקית"),
         ("x-3", "3", "תהליך Batch מתוזמן שבודק מלאי וזמינות", "רץ ברקע, בלי ממשק"),
         ("x-4", "4", "ממשק משתמש גרפי: ניהול למנהל, רכישה ללקוחות", "View")]
exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו שאלה ממבחן: קטלוג מוצרים, שמעצבים בארכיטקטורת MVC. בתיאור יש ארבעה רכיבים.",
      do=show("x-1", "x-2", "x-3", "x-4")),
    P("השאלה: איזה משפט יכול לתאר את הארכיטקטורה? כל האפשרויות שואלות מי יהיה ה-View."),
    P("ה-View הוא מה שמוצג למשתמש. ורק רכיב אחד פונה למשתמש: הממשק הגרפי, רכיב ארבע.", do=show("x-4-t", "q-ok-3")),
    P("רכיב שתיים מחשב מחירים. זו לוגיקה עסקית, והיא שייכת למודל ולא לתצוגה.", do=show("x-2-t", "q-x-2", "q-n-2")),
    P("רכיב שלוש הוא תהליך שרץ ברקע לפי תזמון. אין לו בכלל מסך, אז הוא לא יכול להיות תצוגה.",
      do=show("x-3-t", "q-x-4", "q-n-4")),
    P("״לא ניתן לדעת״? בהחלט אפשר לדעת: התיאור אומר במפורש שיש ממשק משתמש גרפי.", do=show("q-x-0", "q-n-0")),
    P("ויש תשובה נכונה, ולכן ״כל האחרות שגויות״ נופלת.", do=show("q-x-1", "q-n-1")),
    P("המלכודת: ״שירות״ עם הרבה לוגיקה נשמע חשוב. אבל ה-View נקבע לפי מה שהמשתמש **רואה**.", do=show("x-t"), hold=0.5),
], stage=w.stack(*[f'<div id="{i}" class="pt-need h"><span class="pt-pat" style="min-width:40px">{n}</span>'
                   f'<span class="pt-nd">{w.ltr_runs(t)}</span><span id="{i}-t" class="pt-chip {"ok" if tag == "View" else "bad"} h">{tag}</span></div>'
                   for i, n, t, tag in COMPS],
                 st.card("x-t", "trap", "⚠️ View = מה שהמשתמש רואה, לא ״השירות החשוב״"), gap=16),
   panel=w.tight(w.stem(Q["id"], "קטלוג מוצרים בארכיטקטורת MVC, עם ארבעת הרכיבים שמשמאל. איזה מהמשפטים יכול לתאר את "
                                 "הארכיטקטורה?")
                 + st.options("q", OPTS, notes={0: "יש GUI", 1: "יש נכונה", 2: "לוגיקה", 4: "בלי מסך"})))

recap = Scene("recap", "סיכום", [
    P("לסיכום: בספרייה שלנו, הכלל של ההשאלה ישב במודל, המסך רק הציג, והבקר תיווך ביניהם.",
      do=show("r-1")),
    P("לחיצה עברה מהמסך לבקר ומשם לספרייה, והתשובה חזרה באותה דרך.", do=show("r-2")),
    P("ומסך חדש, כמו הקיוסק, דרש רק קוד תצוגה. נתראה ברמה הבאה.", do=show("r-3"), hold=0.6),
], stage=w.stack(FLOW.replace('id="', 'id="z'), gap=20),
   panel=st.card("r-1", "rule", "🔑 הכלל ← Library · המסך ← SearchScreen · התיווך ← LoanController")
         + st.card("r-2", "rule", "🔑 לחיצה: מסך ← בקר ← ספרייה, וחזרה")
         + st.card("r-3", "rule", "🔑 קיוסק חדש = רק קוד תצוגה"))

SCENES = [title, layers, flow, swapv, exam, recap]
w.no_latin(SCENES)
VIDEO = Video("P07", "pat", "MVC: Model, View ו-Controller", SCENES, bank={"25F0b-Q14": 3})
