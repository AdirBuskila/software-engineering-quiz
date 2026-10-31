# -*- coding: utf-8 -*-
"""T06 · כיסוי ונתיבים: כמה בדיקות צריך? — video script (build: tools/video/vid.py T06).

Source: courses/tst/T06.js (lesson + goal; the lesson marks it as enrichment, not asked in recent exams). Exam part:
an original question "בסגנון מבחן" (bank={}): the bank has no coverage question.
Not used on purpose: the T06 quiz code f(x, y) (two independent ifs without else) and the nested a/b/S1/S2/S3
snippet, and 24B-A-Q21 (T06 ref).
Worked examples are new: ticket(age, student) (if/else + if: statement coverage needs 2 tests), fee(kg, express,
member) (a nested decision then an independent one: (2 + 1) x 2 = 6 paths), the exam-style grade(score) (nested: branch coverage needs 3), and max3()
from T01 written one statement per line (100% statement and branch coverage, still a bug).
Every count is MEASURED, not typed: w_tst.coverage() instruments the Java on screen line by line, runs it with javac
on a grid of inputs, and returns the lines hit and the branch outcomes per input; min_tests() brute-forces the
smallest test set; paths() are the distinct outcome sequences. Each Java snippet's outputs are also checked against a
Python mirror.
"""
import itertools
import re
from vid import P, Scene, Video, show, hide
import stage as st
import w_tst as w

TF = ("true", "false")
by_true_first = lambda ps: sorted(ps, key=lambda p: [(l, not v) for l, v in p])

# ---------------------------------------------------------------- ticket(age, student)
TICKET = """int ticket(int age, boolean student) {
  int p;
  if (age < 18)
    p = 20;
  else
    p = 40;
  if (student)
    p = p / 2;
  return p;
}"""
T_IN = [(str(a), s) for a in (10, 30) for s in TF]
T_REC, T_K, T_C = w.coverage(TICKET, T_IN)
py_ticket = lambda a, s: (20 if a < 18 else 40) // (2 if s else 1)
assert all(int(r["out"]) == py_ticket(int(r["in"][0]), r["in"][1] == "true") for r in T_REC)
rec = {r["in"]: r for r in T_REC}
R1, R2 = rec[("10", "true")], rec[("30", "false")]
assert R1["hits"] == {1, 2, 3, 6, 7, 8}
assert w.all_lines(T_K) - R1["hits"] == {5}                       # after the first test only "p = 40" is missing
assert w.covers_stmt([R1, R2], T_K) and w.covers_branch([R1, R2], T_K)
assert w.min_tests(T_REC, T_K, "stmt")[0] == 2 and w.min_tests(T_REC, T_K, "branch")[0] == 2
T_PATHS = by_true_first(w.paths(T_REC))
assert len(T_PATHS) == 4
assert sorted(T_PATHS.index(r["br"]) for r in (R1, R2)) == [0, 3]  # the two tests walk paths 1 and 4 only
assert T_C == {2: "age < 18", 6: "student"}

# ---------------------------------------------------------------- fee(kg, express, member): nested + independent
FEE = """int fee(int kg, boolean express, boolean member) {
  int c;
  if (express) {
    if (kg > 5)
      c = 80;
    else
      c = 50;
  } else
    c = 20;
  if (member)
    c = c - 10;
  return c;
}"""
F_IN = [(str(k), e, m) for k in (2, 8) for e in TF for m in TF]
F_REC, F_K, F_C = w.coverage(FEE, F_IN)
py_fee = lambda k, e, m: ((80 if k > 5 else 50) if e else 20) - (10 if m else 0)
assert all(int(r["out"]) == py_fee(int(r["in"][0]), r["in"][1] == "true", r["in"][2] == "true") for r in F_REC)
F_PATHS = by_true_first(w.paths(F_REC))
assert len(F_PATHS) == 6 == (2 + 1) * 2
assert w.min_tests(F_REC, F_K, "stmt")[0] == 3 and w.min_tests(F_REC, F_K, "branch")[0] == 3
# the kg decision is only reached when express is true: 3 of the 6 paths have length 3, the others length 2
assert sorted(len(p) for p in F_PATHS) == [2, 2, 3, 3, 3, 3]
assert all(dict(p)[2] for p in F_PATHS[:4]) and not any(dict(p)[2] for p in F_PATHS[4:])   # left 4: express

# ---------------------------------------------------------------- exam-style: grade(score), a decision nested in a branch
GRADE = """String grade(int score) {
  String r;
  if (score >= 56) {
    if (score >= 90)
      r = "excellent";
    else
      r = "pass";
  } else
    r = "fail";
  return r;
}"""
G_IN = [(str(v),) for v in range(0, 101)]
G_REC, G_K, G_C = w.coverage(GRADE, G_IN)
py_grade = lambda s: ("excellent" if s >= 90 else "pass") if s >= 56 else "fail"
assert all(r["out"] == py_grade(int(r["in"][0])) for r in G_REC)
G_MIN, G_SET = w.min_tests(G_REC, G_K, "branch")
assert G_MIN == 3 and w.min_tests(G_REC, G_K, "stmt")[0] == 3 and len(w.paths(G_REC)) == 3
assert G_C == {2: "score >= 56", 3: "score >= 90"}
GR = {int(r["in"][0]): r for r in G_REC}
assert w.covers_branch([GR[95], GR[70], GR[30]], G_K)            # one test per leaf: 95, 70, 30
# two tests never suffice: the test that makes the outer if false never reaches the inner one
assert not any(w.covers_branch([GR[a], GR[b]], G_K) for a in range(101) for b in range(a, 101))
assert all(len(GR[v]["br"]) == 1 for v in range(0, 56))             # below 56 only the outer decision is seen
OPTS = [(k, f'<span class="ts-mono">{k}</span>') for k in ("1", "2", "3", "4")]
assert [k for k, _ in OPTS if int(k) == G_MIN] == ["3"]

# ---------------------------------------------------------------- max3 again: full coverage, still a bug
MAX3 = """int max3(int a, int b, int c) {
  if (a > b && a > c)
    return a;
  if (b > a && b > c)
    return b;
  return c;
}"""
M_TESTS = [("1", "2", "3"), ("9", "2", "3"), ("1", "8", "3")]
M_REC, M_K, _ = w.coverage(MAX3, M_TESTS + [("5", "5", "1")])
assert [int(r["out"]) for r in M_REC[:3]] == [3, 9, 8]             # the three tests pass
assert w.covers_stmt(M_REC[:3], M_K) and w.covers_branch(M_REC[:3], M_K)
assert int(M_REC[3]["out"]) == 1 != 5                              # and max3(5, 5, 1) is wrong

# ---------------------------------------------------------------- stage pieces
def btable(pfx, recs, conds, rows_hidden=True):
    head = "".join(f'<th dir="ltr"><span class="ts-mono">{w.esc(c)}</span></th>' for c in conds.values())
    rows = []
    for k, r in enumerate(recs):
        seen = dict(r["br"])
        cells = "".join(f'<td class="{"ok" if seen.get(l) else "bad"}">{"true" if seen.get(l) else "false"}</td>'
                        if l in seen else "<td>—</td>" for l in conds)
        rows.append(f'<tr id="{pfx}-r{k}" class="{"h" if rows_hidden else ""}"><td dir="ltr" class="ts-mono">'
                    f'({", ".join(r["in"])})</td>{cells}</tr>')
    return (f'<table class="ts-tab" id="{pfx}"><thead><tr><th>בדיקה</th>{head}</tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table>')


T_TREE = lambda pfx, **k: w.path_tree(pfx, T_PATHS, T_C, w=760, h=380, **k,
                                 leaf_text=[str(py_ticket(*(10 if dict(p)[2] else 30, dict(p)[6]))) for p in T_PATHS])
F_TREE = lambda pfx: w.path_tree(pfx, F_PATHS, F_C, w=980, h=470)
assert [str(py_ticket(10, True)), str(py_ticket(30, False))] == ["10", "40"]

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נמדוד כמה מהקוד הבדיקות שלנו באמת מריצות."),
    P("נכיר כיסוי שורות, כיסוי ענפים ונתיבים, ונחשב כמה בדיקות צריך לכל אחד."),
    P("זה שלב העשרה: הוא לא הופיע במבחנים האחרונים, אבל הוא עוזר להבין למה בדיקה אחת לא מספיקה.", hold=0.4),
], stage='<div class="kicker">T06 · בדיקות תוכנה · העשרה</div><h1>כיסוי ונתיבים: כמה בדיקות צריך?</h1>'
         '<p>שורות, ענפים ונתיבים: כל דרישה חזקה מהקודמת, וגם 100% לא מוכיח שאין באגים.</p>', layout="title")

idea = Scene("idea", "שלושה מדדים", [
    P("הנה מתודה שמחשבת מחיר כרטיס: עשרים לילדים מתחת לגיל שמונה עשרה, ארבעים למבוגרים.", do=show("tk")),
    P("ואם הקונה סטודנט, המחיר יורד לחצי.", hold=0.2),
    P("**כיסוי שורות**: כל שורה בקוד רצה לפחות פעם אחת.", do=show("id-c1")),
    P("**כיסוי ענפים**: כל תנאי מקבל לפחות פעם אחת אמת, ולפחות פעם אחת שקר.", do=show("id-c2")),
    P("ו**נתיב** הוא מסלול שלם מההתחלה ועד הסוף. כל שילוב שונה של החלטות הוא נתיב אחר.", do=show("id-c3"),
      hold=0.4),
], stage=w.code("tk", TICKET, hidden=True, size=30),
   panel=st.card("id-c1", "rule", "🔑 כיסוי שורות: כל שורה רצה")
         + st.card("id-c2", "rule", "🔑 כיסוי ענפים: כל תנאי גם <span class=\"ts-mono\">true</span> וגם "
                                    "<span class=\"ts-mono\">false</span>")
         + st.card("id-c3", "rule", "🔑 נתיב: רצף שלם של החלטות"))

stmt = Scene("stmt", "כיסוי שורות", [
    P("נריץ בדיקה ראשונה: גיל עשר, סטודנט. השורות שרצו נדלקות בירוק.",
      do=show(*[f"sa-m{k}" for k in sorted(R1["hits"])], "sa-c1")),
    P("הגיל קטן משמונה עשרה, אז המחיר עשרים. סטודנט, אז חצי: עשר."),
    P("אבל שורה אחת לא רצה: המחיר של מבוגר, ארבעים. היא בענף של ה-else.", do=show("sa-x5"),
      say="אבל שורה אחת לא רצה: המחיר של מבוגר, ארבעים. היא בענף של האֶלְס."),
    P("ואין קלט אחד שמריץ גם את המחיר של ילד וגם את המחיר של מבוגר. או שהגיל קטן משמונה עשרה, או שלא.",
      hold=0.2),
    P("אז מוסיפים בדיקה שנייה: גיל שלושים, לא סטודנט.", do=hide("sa-x5") + show("sa-m5", "sa-c2")),
    P("עכשיו כל השורות רצו. **שתי בדיקות**, וזה המינימום לכיסוי שורות כאן.", do=show("sa-c3"), hold=0.4),
], stage=w.code("sa", TICKET, size=30),
   panel=st.card("sa-c1", "ex", 'בדיקה 1: <span class="ts-mono">ticket(10, true)</span> ← 10')
         + st.card("sa-c2", "ex", 'בדיקה 2: <span class="ts-mono">ticket(30, false)</span> ← 40')
         + st.card("sa-c3", "rule", "🔑 כיסוי שורות מלא: מינימום 2 בדיקות"))

branch = Scene("branch", "כיסוי ענפים", [
    P("עכשיו כיסוי ענפים. לכל תנאי נרשום מה הוא קיבל בכל בדיקה."),
    P("בבדיקה הראשונה, שני התנאים קיבלו אמת.", do=show("bt-r0")),
    P("בבדיקה השנייה, שניהם קיבלו שקר.", do=show("bt-r1")),
    P("כל תנאי ראה גם אמת וגם שקר. אז אותן **שתי בדיקות** נותנות גם כיסוי ענפים מלא.", do=show("br-c1")),
    P("בדיקה אחת לבד לעולם לא מספיקה לכיסוי ענפים: בה כל תנאי רואה רק כיוון אחד.", do=show("br-c2"),
      hold=0.4),
], stage=w.code("sb", TICKET, size=26) + btable("bt", [R1, R2], T_C),
   panel=st.card("br-c1", "rule", "🔑 כיסוי ענפים מלא: אותן 2 בדיקות")
         + st.card("br-c2", "trap", "⚠️ בדיקה אחת = כל תנאי בכיוון אחד בלבד"))

paths = Scene("paths", "נתיבים", [
    P("ומה עם נתיבים? נצייר את ההחלטות כעץ. בראש, התנאי על הגיל.", do=show("ta-n0")),
    P("כל ענף שלו מגיע לתנאי על הסטודנט, וגם הוא מתפצל לשניים.", do=show("ta-e1", "ta-e2", "ta-n1", "ta-n2")),
    P("שתי החלטות בלתי תלויות, שתיים כפול שתיים: **ארבעה נתיבים**.",
      do=show("ta-e3", "ta-e4", "ta-e5", "ta-e6", "ta-leaf0", "ta-leaf1", "ta-leaf2", "ta-leaf3", "pa-c1")),
    P("ושתי הבדיקות שלנו? הן עברו רק בשני נתיבים מתוך ארבעה.", do=show("ta-hl0", "ta-hl3")),
    P("כדי לעבור בכל הנתיבים צריך ארבע בדיקות. נתיבים הם הדרישה החזקה ביותר מהשלוש.", do=show("pa-c2"),
      hold=0.4),
], stage=T_TREE("ta", reveal=True),
   panel=st.card("pa-c1", "rule", "🔑 החלטות בלתי תלויות: מכפילים. <span class='ts-nw'>2 × 2 = 4</span>")
         + st.card("pa-c2", "ex", "שורות: 2 · ענפים: 2 · כל הנתיבים: 4")
         + '<div class="hint">בעיגולים: המחיר בסוף כל נתיב</div>')

nested = Scene("nested", "החלטה בתוך החלטה", [
    P("ומה קורה כשהחלטה נמצאת **בתוך** החלטה אחרת? הנה מחיר משלוח.", do=show("fe")),
    P("רק במשלוח אקספרס בודקים את המשקל. במשלוח רגיל אין שאלה כזו.", do=show("fe-m2", "fe-m3"), hold=0.2),
    P("אז בתוך ההחלטה הראשונה לא מכפילים, אלא **מחברים**: שני נתיבים באקספרס, ועוד אחד ברגיל. שלושה.",
      do=hide("fe-m2", "fe-m3") + show("fe-m9", "ne-c1")),
    P("ואחרי זה יש החלטה **בלתי תלויה**, אם הלקוח מנוי. אותה מכפילים: שלושה כפול שתיים, **שישה** נתיבים.",
      do=show("ne-c2")),
    P("כיסוי שורות כאן דורש שלוש בדיקות: יש שלושה מחירים שונים, ורק אחד מהם רץ בכל בדיקה.", do=show("ne-c3")),
    P("וגם כיסוי ענפים דורש שלוש: המשקל צריך לקבל גם אמת וגם שקר, וזה קורה רק באקספרס.", hold=0.4),
], stage=w.code("fe", FEE, hidden=True, size=25),
   panel=st.card("ne-c1", "rule", "🔑 החלטה בתוך ענף: מחברים. <span class='ts-nw'>2 + 1 = 3</span>")
         + st.card("ne-c2", "rule", "🔑 ואחריה החלטה בלתי תלויה: <span class='ts-nw'>3 × 2 = 6</span>")
         + st.card("ne-c3", "ex", "שורות: 3 · ענפים: 3 · נתיבים: 6"))

ntree = Scene("ntree", "העץ של המשלוח", [
    P("והנה העץ. מימין, משלוח רגיל: מיד ההחלטה על המנוי, שני נתיבים.", do=show("tb-leaf4", "tb-leaf5")),
    P("משמאל, אקספרס: קודם המשקל, ואז המנוי. ארבעה נתיבים.", do=show("tb-leaf0", "tb-leaf1", "tb-leaf2", "tb-leaf3")),
    P("ביחד, שישה עלים. כל עלה הוא נתיב אחד.", hold=0.4),
], stage=F_TREE("tb"), layout="full")

exam = Scene("exam", "בסגנון מבחן", [
    P("שאלה בסגנון מבחן: מהו המספר המינימלי של בדיקות שנותן כיסוי ענפים מלא במתודה הזו?"),
    P("יש כאן שני תנאים, אבל השני נמצא **בתוך** הראשון: בודקים אותו רק כשהציון חמישים ושש ומעלה.",
      do=show("gr-m2", "gr-m3")),
    P("כדי שהתנאי הראשון יקבל שקר, צריך ציון נמוך, למשל שלושים. בבדיקה הזו לא מגיעים בכלל לתנאי השני.",
      do=hide("gr-m2", "gr-m3") + show("gr-m8")),
    P("אז התנאי השני צריך עוד שתי בדיקות משלו: תשעים וחמש לאמת, ושבעים לשקר.", do=hide("gr-m8") + show("gr-m4", "gr-m6")),
    P("שלושים, שבעים ותשעים וחמש: שלוש בדיקות, וכל ענף רץ.", do=show("q-ok-3")),
    P("בדיקה אחת? בה כל תנאי רואה רק כיוון אחד.", do=show("q-x-1", "q-n-1")),
    P("שתיים? הבדיקה שנותנת לתנאי הראשון שקר לא מגיעה לשני, אז לשני נשארת בדיקה אחת, וכיוון אחד בלבד.",
      do=show("q-x-2", "q-n-2")),
    P("וארבע? זו ספירה של שניים כפול שניים. אבל ההחלטה מקוננת: יש רק שלושה נתיבים, ושלוש בדיקות כבר מכסות הכל.",
      do=show("q-x-4", "q-n-4"), hold=0.5),
], stage=w.code("gr", GRADE, size=26),
   panel=w.stem("", "מהו המספר המינימלי של בדיקות לכיסוי ענפים מלא במתודה <bdi>grade</bdi>?")
         + st.options("q", OPTS, notes={"1": "כיוון אחד", "2": "השני רואה כיוון אחד", "4": "רק 3 נתיבים"}))

proof = Scene("proof", "100% זה לא הוכחה", [
    P("ולסיום, אזהרה. זוכרים את המתודה שמחזירה מקסימום של שלושה מספרים?", do=show("mx")),
    P("שלוש הבדיקות שלה מריצות כל שורה, ונותנות לכל תנאי גם אמת וגם שקר.",
      do=show(*[f"mx-m{k}" for k in sorted(M_K)], "pr-c1")),
    P("מאה אחוז כיסוי שורות, ומאה אחוז כיסוי ענפים. ובכל זאת, עם חמש, חמש ואחת היא מחזירה אחת.",
      do=show("pr-c2")),
    P("כיסוי אומר איזה קוד **רץ**. הוא לא אומר שהתוצאה נכונה בכל קלט. אין הבטחה של אפס שגיאות.",
      do=show("pr-c3"), hold=0.4),
], stage=w.code("mx", MAX3, hidden=True, size=30),
   panel=st.card("pr-c1", "ex", "3 בדיקות: 100% שורות, 100% ענפים")
         + st.card("pr-c2", "trap", '⚠️ <span class="ts-mono">max3(5, 5, 1)</span> ← 1')
         + st.card("pr-c3", "rule", "🔑 כיסוי גבוה ≠ אין שגיאות"))

recap = Scene("recap", "סיכום", [
    P("לסיכום: כיסוי שורות, כל שורה רצה. כיסוי ענפים, כל תנאי גם אמת וגם שקר.", do=show("r-1")),
    P("נתיבים: החלטות בלתי תלויות מכפילים, והחלטה בתוך ענף מחברים.", do=show("r-2")),
    P("וכיסוי מלא עדיין לא מוכיח שאין שגיאות. נתראה ברמה הבאה.", do=show("r-3"), hold=0.6),
], stage=re.sub(r'(id="tr-leaf\d" class=)"h"', r'\1""', T_TREE("tr")),
   panel=st.card("r-1", "rule", "🔑 שורות ← ענפים ← נתיבים: כל אחד דורש יותר")
         + st.card("r-2", "rule", "🔑 בלתי תלויות: ×. בתוך ענף: +")
         + st.card("r-3", "trap", "⚠️ 100% כיסוי ≠ אפס שגיאות"))

SCENES = [title, idea, stmt, branch, paths, nested, ntree, exam, proof, recap]
w.no_latin_and_isolate(SCENES)
VIDEO = Video("T06", "tst", "כיסוי ונתיבים: כמה בדיקות צריך?", SCENES, bank={})
