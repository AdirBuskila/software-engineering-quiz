# -*- coding: utf-8 -*-
"""R03 · Agile: המנשר והשוואה ל-Waterfall — video script (build: tools/video/vid.py R03).

Source: courses/proc/R03.js (lesson + goal: link each line of the Agile manifesto to the practice that realizes it, and
compare Agile with Waterfall). Exam anchor: 19B-B-Q11 (the disadvantages of Agile development -> all the answers are
correct: rewriting the same code, code without enough documentation, initial uncertainty about the final product).
No guided quiz uses it and it has no twin in the bank.
Checked against the course checker (w_proc.CHK): PRACTICE (working software -> short cycles and demos), FACTS (the
Agile vs Waterfall statements), SUITS (fixed spec -> Waterfall, changing needs -> Agile).
Policy: every manifesto line is shown through what one team actually did (a library app team), never in the wording of
a quiz option ("short development cycles and demos", "mixed development teams", "adapt to changing requirements and
deliver working software in versions", "a fixed spec that will not change", "phases easier to manage"). The former
anchor 24S-A-Q4 was dropped: its option set is the same as R03-Q1 and 21-A-Q10.
Avoided on purpose: the R03 quiz items (24B-B-Q5, 25S-A-Q6 and the three originals) and their twins (21-A-Q10,
21S-A-Q10, 24S-A-Q3, 24S-A-Q4, 22B-A-Q12, 26B-A-Q8, 20-A-Q6, SP-AMR-Q5, 25F0a-Q5, SP-DGM-Q10), and the R09 boss item
25S-A-Q4 is not solved here. Worked projects are mine: a library app team, a fixed annual tax-form calculator and a
shopping app that changes with user feedback.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_proc as w

# ---------------------------------------------------------------- facts (checked)
assert w.CHK["PRACTICE"]["working_software_over_docs"] == "short_cycles_and_demos"
F = w.CHK["FACTS"]
assert F["waterfall_suits_fixed_spec"] and F["waterfall_phases_easier_to_manage"] and F["agile_flexible"]
assert F["agile_team_has_all_roles"] and not F["agile_predicts_better"] and not F["waterfall_easy_to_change"]
assert w.fits("Waterfall", {"stable_reqs"}) and not w.fits("Agile", {"stable_reqs"})      # tax-form calculator
assert w.fits("Agile", {"changing_reqs"}) and not w.fits("Waterfall", {"changing_reqs"})  # shopping app

Q = BANK["19B-B-Q11"]
OK = w.opt_index(Q, "כל התשובות נכונות")
RW = w.opt_index(Q, "refactoring")
DOC = w.opt_index(Q, "ללא תיעוד")
UNC = w.opt_index(Q, "חוסר ודאות")
assert Q["correctIndex"] == OK == 1 and sorted([OK, RW, DOC, UNC]) == [0, 1, 2, 3]
# each listed item is a cost of the same flexibility: no fixed scope up front (uncertainty: agile_predicts_better is
# False), requirements that move (code gets reworked), working software before full documentation (docs can lag)
assert not F["agile_predicts_better"] and F["agile_flexible"]
OPTS = w.opts_of(Q)
assert OPTS[-1][0] == OK

N_INC = 6
TL = ('<div class="pr-tl">'
      f'<div id="t-w" class="h"><div class="pr-tlh">{w.en("Waterfall")}: מסירה אחת בסוף</div><div class="pr-tlr">'
      '<div class="pr-seg big">דרישות · תיכון · קידוד · בדיקות</div><div class="pr-seg end">📦 מסירה</div></div></div>'
      f'<div id="t-a" class="h" style="margin-top:22px"><div class="pr-tlh">אג׳ייל: גרסה עובדת בכל איטרציה</div><div class="pr-tlr">'
      + "".join(f'<div id="t-a{k}" class="pr-seg inc h">📦 גרסה {k + 1}</div>' for k in range(N_INC))
      + '</div></div></div>')

MAN = w.table("mn", ["במנשר: מעדיפים…", "מה הצוות של הספרייה עשה"], [
    ["תוכנה עובדת, על פני תיעוד מלא", "כל שבועיים הראו לספרניות את האפליקציה <b>רצה</b>, ולא מסמך"],
    ["אנשים ואינטראקציות, על פני תהליכים וכלים", "מתכנתת, בודק ומעצבת יושבים יחד, ושאלה נפתרת בחמש דקות"],
    ["שיתוף פעולה עם הלקוח, על פני חוזים", "נציגה של הספרייה בצוות, והספרניות מגיבות על כל גרסה"],
    ["גמישות להגיב לשינוי, על פני תוכנית קבועה", "ביקשו שינוי אחרי גרסה 3, והוא נכנס כבר בגרסה 4"],
], widths=[430, 540], size=26)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נכיר את אג׳ייל: איך הוא עובד, ומה כתוב במנשר האג׳ילי."),
    P("נראה איך כל סעיף במנשר נראה בעבודה של צוות אמיתי, ונשווה בין אג׳ייל ל-Waterfall."),
    P("ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">R03 · תהליכים, Agile ודרישות</div><h1>Agile: המנשר והשוואה ל-Waterfall</h1>'
         '<p>לקשר כל סעיף במנשר למה שהצוות עושה בפועל, ולדעת מתי מתאים אג׳ייל ומתי מפל מים.</p>', layout="title")

idea = Scene("idea", "הרעיון", [
    P("ב-Waterfall יש מסירה אחת גדולה, בסוף הפרויקט. הלקוח רואה תוכנה רק שם.", do=show("t-w")),
    P("אג׳ייל עובד אחרת: הוא **מצטבר ואיטרטיבי**. העבודה מחולקת לאיטרציות קטנות.", do=show("t-a", "t-a0")),
    P("בסוף כל איטרציה יש גרסה עובדת, שהלקוח רואה ונותן עליה משוב.", do=show("t-a1", "t-a2")),
    P("וככה, איטרציה אחרי איטרציה, המוצר גדל.", do=show("t-a3", "t-a4", "t-a5")),
    P("ומה קורה כשהלקוח משנה את דעתו? זה לא אסון. השינוי פשוט נכנס לאיטרציה הבאה.", do=show("i1")),
    P("ומגלים אותו אחרי שבועיים, ולא בסוף הפרויקט.", do=show("i2"), hold=0.4),
], stage=TL,
   panel=st.card("i1", "rule", "🔑 שינוי של הלקוח ← נכנס לאיטרציה <b>הבאה</b>")
         + st.card("i2", "ex", "🔁 גרסה בכל איטרציה ← מגלים שינוי מוקדם"))

man = Scene("man", "המנשר", [
    P("המנשר האג׳ילי מנוסח כארבע העדפות: דבר אחד מעדיפים על פני דבר אחר. נראה מה צוות אחד, שבנה אפליקציה לספרייה, עשה בפועל."),
    P("תוכנה עובדת, על פני תיעוד מלא. כל שבועיים הצוות הראה לספרניות את האפליקציה **רצה**, ולא מסמך שמתאר אותה.",
      do=show("mn-r0")),
    P("אנשים ואינטראקציות, על פני תהליכים וכלים. המתכנתת, הבודק והמעצבת יושבים יחד, ושאלה נפתרת בחמש דקות, בלי שרשרת מיילים.",
      do=show("mn-r1")),
    P("שיתוף פעולה עם הלקוח, על פני חוזים. נציגה של הספרייה עובדת עם הצוות, והספרניות מגיבות על כל גרסה.",
      do=show("mn-r2")),
    P("וגמישות להגיב לשינוי. אחרי הגרסה השלישית, הספרניות ביקשו לשנות את מסך ההחזרה. השינוי נכנס כבר בגרסה הרביעית.",
      do=show("mn-r3"), hold=0.3),
    P("ושימו לב: ״מעדיפים״ זה לא ״מבטלים״. אג׳ייל לא מוותר על תיעוד, הוא רק שם את התוכנה שעובדת לפניו.",
      do=show("mn-t"), hold=0.4),
], stage=MAN,
   panel=st.card("mn-t", "trap", "⚠️ ״על פני״ = מעדיפים, <b>לא מבטלים</b>. יש תיעוד באג׳ייל"))

CMP = w.table("cp", ["", w.en("Waterfall"), "אג׳ייל"], [
    ["מתי מתאים", "יודעים מראש בדיוק מה בונים", "הלקוח עוד לומד מה הוא רוצה"],
    ["תכנון", "תוכנית אחת מההתחלה: רואים איפה עומדים, כמה זמן וכמה כסף", "התוכנית מתעדכנת בכל איטרציה"],
    ["שינוי", "חוזרים אחורה במפל, יקר", "נכנס לאיטרציה הבאה"],
    ["הצוות", "מעבירים עבודה משלב לשלב", "כל המקצועות יחד, באותו צוות"],
], widths=[150, 450, 370], size=26)

cmp = Scene("cmp", "אג׳ייל מול Waterfall", [
    P("עכשיו נשווה. Waterfall מתאים כשיודעים מראש, בדיוק, מה בונים. אג׳ייל מתאים כשהלקוח עוד לומד מה הוא רוצה.",
      do=show("cp-r0")),
    P("ב-Waterfall יש תוכנית אחת מההתחלה, ולכן רואים בקלות איפה עומדים, כמה זמן נשאר, וכמה זה יעלה.", do=show("cp-r1")),
    P("באג׳ייל התוכנית מתעדכנת, ושינוי פשוט נכנס לאיטרציה הבאה. ב-Waterfall הוא מחזיר אחורה במפל.", do=show("cp-r2")),
    P("ובצוות האג׳ילי כל המקצועות יושבים יחד, במקום להעביר עבודה משלב לשלב.", do=show("cp-r3"), hold=0.3),
    P("שני פרויקטים. מחשבון לטופס מס שנתי, לפי חוק שכבר נקבע ולא ישתנה השנה. יודעים הכל מראש, ולכן Waterfall.",
      do=show("e1")),
    P("אפליקציית קניות, שהלקוח רוצה לשנות לפי תגובות המשתמשים בכל חודש. ולכן אג׳ייל.", do=show("e2")),
    P("ושימו לב למלכודות: אג׳ייל **לא תמיד** מהיר יותר, ולא תמיד פחות אמין. מילים כמו ״תמיד״ הן סימן אזהרה.",
      do=show("e3"), hold=0.4),
], stage=CMP,
   panel=st.card("e1", "ex", "🧾 מחשבון מס לפי חוק קבוע ← " + w.en("Waterfall"))
         + st.card("e2", "ex", "🛒 אפליקציה שמשתנה לפי המשתמשים ← אג׳ייל")
         + st.card("e3", "trap", "⚠️ ״תמיד מהיר יותר״, ״תמיד פחות אמין״: שגוי"))

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו שאלה ממבחן, מהצד השני: מה **החסרונות** של פיתוח אג׳ילי?"),
    P("לכל גמישות יש מחיר. נבדוק כל אפשרות מול מה שראינו.", do=show("x0")),
    P("חוסר ודאות בהתחלה, מה יהיה המוצר הסופי? נכון. התוכנית מתעדכנת כל הזמן, ולכן בהתחלה לא יודעים בדיוק איפה ייגמר.",
      do=show(f"q-ok-{UNC}", f"q-n-{UNC}")),
    P("כתיבה מחדש של אותו קוד? גם נכון. כשהדרישות זזות, קוד שכבר נכתב צריך לשנות, ושוב.",
      do=show(f"q-ok-{RW}", f"q-n-{RW}")),
    P("קוד בלי תיעוד מספק? גם זה סיכון אמיתי. אג׳ייל לא מבטל תיעוד, אבל כשהתוכנה העובדת קודמת, התיעוד לפעמים נשאר מאחור.",
      do=show(f"q-ok-{DOC}", f"q-n-{DOC}")),
    P("שלושתן חסרונות אפשריים, ולכן התשובה: כל התשובות נכונות.", do=show(f"q-ok-{OK}")),
    P("והמלכודת: מי שבחר תשובה אחת בלבד, ראה חיסרון אחד. השאלה מבקשת את כולם.", do=show("x1"), hold=0.5),
], stage=w.stack(st.card("x0", "rule", "🔑 לגמישות יש מחיר: <b>ודאות</b>, <b>קוד יציב</b>, <b>תיעוד</b>"),
                 st.card("x1", "trap", "⚠️ שלוש אפשרויות נכונות ← ״כל התשובות נכונות״"), gap=26),
   panel=w.qpanel(w.stem(Q["id"], Q["question"]),
                  st.options("q", OPTS, notes={UNC: "תוכנית מתעדכנת", RW: "דרישות זזות", DOC: "תיעוד מאחור"})))

recap = Scene("recap", "סיכום", [
    P("לסיכום: אג׳ייל מצטבר ואיטרטיבי. גרסה עובדת בכל איטרציה, ושינוי נכנס לאיטרציה הבאה.", do=show("s1")),
    P("במנשר: מעדיפים, לא מבטלים. וכל העדפה נראית בעבודה היומיומית של הצוות.", do=show("s2")),
    P("Waterfall כשיודעים הכל מראש. אג׳ייל כשהלקוח עוד לומד. ולגמישות יש גם מחיר. נתראה ברמה הבאה.", do=show("s3"),
      hold=0.6),
], stage=CMP.replace('id="cp', 'id="zc').replace(' class="h"', ''),
   panel=st.card("s1", "rule", "🔑 אג׳ייל = איטרציות קטנות + משוב תכוף")
         + st.card("s2", "rule", "🔑 ״על פני״ = מעדיפים, לא מבטלים")
         + st.card("s3", "rule", "🔑 יודעים הכל ← " + w.en("Waterfall") + " · לומדים בדרך ← אג׳ייל"))

SCENES = [title, idea, man, cmp, exam, recap]
w.no_latin(SCENES)
VIDEO = Video("R03", "proc", "Agile: המנשר והשוואה ל-Waterfall", SCENES, bank={"19B-B-Q11": OK})
