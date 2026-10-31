# -*- coding: utf-8 -*-
"""R02 · מודלי תהליך: Waterfall ו-Build and Fix — video script (build: tools/video/vid.py R02).

Source: courses/proc/R02.js (lesson + goal: the process stages; choose Waterfall, Build and Fix or Plan Driven from a
project description). Exam anchor: 19B-B-Q6 (when Waterfall is useful: supplier-client relations with fixed
deadlines and well-defined outputs). No guided quiz uses it and it has no twin in the bank.
Model fit is checked against the course checker's SUITS table (tools/verify/needhelp/proc/check.py, via w_proc.CHK).
Avoided on purpose: the R02 quiz items (19B-B-Q14 "where a change costs most", 25F0b-Q6 "what is not an advantage of
Build and Fix", the tax-authority system, the investors' POC week, "which trait misleads to Waterfall") and their twins
(25B-N-Q5, 23S-A-Q9, 26B-A-Q11), and 26S-A-Q8 (the R09 boss, a government system). The video never says at which
stage a change is most expensive, and never lists Build and Fix's advantages.
Policy: the worked projects are not structural copies of R02-Q1 (a government/tax system with stable requirements) or
R02-Q2 (prove an idea to investors in a week): one is a regulated medical device, one is a case where Build and Fix is
the WRONG choice. Worked projects are mine: an insulin-pump firmware, a bank transfer system someone wants to "just
code and fix", and a start-up that does not know its users yet.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_proc as w

# ---------------------------------------------------------------- facts (checked)
# the three worked projects, as needs of the checker's SUITS table
MED = {"stable_reqs", "control"}                 # firmware under a regulator who signs off every stage
BANKX = {"stable_reqs", "fixed_deadlines", "control"}   # a bank's transfer system someone wants "fast, no planning"
START = {"changing_reqs"}
assert w.fits("PlanDriven", MED) and not w.fits("BuildFix", MED)
assert not w.fits("BuildFix", BANKX) and w.fits("PlanDriven", BANKX)   # Build and Fix only for a proof of concept
assert w.CHK["SUITS"]["BuildFix"] == {"poc"}
assert not w.fits("Waterfall", START) and not w.fits("PlanDriven", START) and w.fits("Agile", START)
assert "changing_reqs" in w.CHK["BAD_FOR_WATERFALL"]

Q = BANK["19B-B-Q6"]
OK = w.opt_index(Q, "יחסי ספק לקוח")
CHG = w.opt_index(Q, "שינויים רבים")
MANY = w.opt_index(Q, "מספר רב של לקוחות")
WHO = w.opt_index(Q, "הלקוח הסופי")
assert Q["correctIndex"] == OK == 1 and sorted([OK, CHG, MANY, WHO]) == [0, 1, 2, 3]
# the key: supplier-client relations with fixed deadlines and well-defined outputs = stable reqs + deadlines + control
assert w.fits("Waterfall", {"stable_reqs", "fixed_deadlines", "control"})
assert not w.fits("Waterfall", {"changing_reqs"})          # many changes during development
OPTS = w.opts_of(Q)

STEPS = [("הגדרת דרישות", "Requirements"), ("תיכון", "Design"), ("קידוד", "Coding"), ("בדיקות", "Testing"),
         ("תחזוקה", "Maintenance")]
WF = w.cascade("wf", STEPS, w=980, h=500)
WV = w.cascade("wv", STEPS, w=980, h=500, back=(3, 0, "שינוי דרישה מאוחר = יקר"), hidden_steps=False)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נכיר את שלבי תהליך הפיתוח, ושלושה מודלים לניהול שלו."),
    P("נלמד מתכון קצר לבחירה בין Waterfall, Build and Fix ו-Plan Driven."),
    P("ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">R02 · תהליכים, Agile ודרישות</div><h1>מודלי תהליך: Waterfall ו-Build and Fix</h1>'
         '<p>מה השלבים של תהליך פיתוח, ואיך בוחרים מודל לפי תיאור הפרויקט.</p>', layout="title")

stages = Scene("stages", "שלבי התהליך", [
    P("כל תהליך פיתוח תוכנה עובר באותם שלבים. ראשון: **הגדרת הדרישות**, מה המערכת צריכה לעשות.", do=show("wf-s0")),
    P("אחר כך **תיכון**: איך נבנה אותה.", do=show("wf-a0", "wf-s1")),
    P("ואז **קידוד**, **בדיקות**, ולבסוף **תחזוקה**, אחרי שהמערכת אצל הלקוח.",
      do=show("wf-a1", "wf-s2", "wf-a2", "wf-s3", "wf-a3", "wf-s4")),
    P("ולפני הדרישות יכול להיות עוד שלב: **חקר ישימות**. בודקים אם הפרויקט אפשרי ומשתלם בכלל.", do=show("f1")),
    P("ואב טיפוס? בונים אותו כדי **להבהיר את הדרישות** מול הלקוח. לכן הוא שייך לשלב הדרישות.",
      do=show("f2", "wf-hs0")),
    P("ומתודולוגיית פיתוח היא מסגרת מסודרת שקובעת את השלבים, את התפקידים ואת התוצרים.", do=hide("wf-hs0") + show("f3"),
      hold=0.4),
], stage=WF,
   panel=st.card("f1", "ex", "🔎 <b>חקר ישימות</b>: לפני הגדרת הדרישות")
         + st.card("f2", "ex", "🧪 <b>אב טיפוס</b>: כלי להבהרת הדרישות")
         + st.card("f3", "rule", "🔑 מתודולוגיה = מסגרת שקובעת <b>שלבים, תפקידים ותוצרים</b>"))

water = Scene("water", "Waterfall", [
    P("המודל הראשון הוא Waterfall, מפל מים. השלבים מתבצעים בזה אחר זה, **בסדר המוגדר, בלי שינויים**.", do=show("w1")),
    P("כל שלב נגמר לפני שהבא מתחיל, כמו מים שיורדים במדרגות.", do=show("wv-hs1")),
    P("היתרון: קל לחזות ולנהל. יודעים מראש מה יקרה בכל שלב, כמה זמן, ובכמה כסף.", do=hide("wv-hs1") + show("w2")),
    P("החיסרון: אם הדרישות משתנות באמצע, צריך לחזור אחורה במפל, וזה יקר מאוד.", do=show("wv-back")),
    P("ולכן הכלל: Waterfall מתאים כשהדרישות **ידועות ויציבות** מראש.", do=show("w3"), hold=0.4),
], stage=WV,
   panel=st.card("w1", "ex", "🌊 שלבים עוקבים, <b>בסדר קבוע</b>")
         + st.card("w2", "ex", "👍 קל לחזות זמן ותקציב, ולנהל")
         + st.card("w3", "rule", "🔑 דרישות <b>ידועות ויציבות</b> ← Waterfall"))

MODELS = w.table("m", ["מודל", "איך זה עובד", "מתי מתאים"], [
    [w.en("Waterfall"), "שלבים עוקבים בסדר קבוע", "דרישות ברורות ויציבות, לוחות זמנים קשיחים"],
    [w.en("Plan Driven"), "תכנון מפורט מראש, ומעקב מול התוכנית", "פרויקט גדול שדורש חיזוי ובקרה"],
    [w.en("Build and Fix"), "כותבים קוד ומתקנים, בלי תכנון מסודר", "רק כדי להראות מהר שרעיון עובד"],
], widths=[200, 380, 400], size=27)

models = Scene("models", "שלושה מודלים", [
    P("עכשיו שלושה מודלים, זה לצד זה. את Waterfall כבר הכרנו.", do=show("m-r0")),
    P("Plan Driven: מתכננים מראש בפירוט לוחות זמנים, תקציב ותוצרים, ועוקבים כל הזמן מול התוכנית.", do=show("m-r1")),
    P("הוא מתאים לפרויקט גדול, שבו חייבים חיזוי ובקרה.", do=show("m-m1")),
    P("Build and Fix: כותבים קוד, מראים, ומתקנים. בלי שלבי תכנון מסודרים.", do=show("m-r2")),
    P("הוא מתאים רק כשרוצים להראות מהר שרעיון בכלל עובד, לפני שבונים באמת.", do=show("m-m2"), hold=0.3),
    P("והמתכון: שואלים קודם, האם הדרישות ידועות ויציבות?", do=show("k1")),
    P("כן, ויש צורך בבקרה? Waterfall או Plan Driven. לא? אז לא Waterfall.", do=show("k2")),
    P("ואם המטרה היא רק להוכיח שרעיון אפשרי? Build and Fix.", do=show("k3"), hold=0.4),
], stage=MODELS,
   panel=st.card("k1", "rule", "🔑 שאלה ראשונה: הדרישות <b>ידועות ויציבות</b>?")
         + st.card("k2", "ex", "כן + בקרה ← Waterfall / Plan Driven<br>לא ← <b>לא</b> Waterfall")
         + st.card("k3", "ex", "רק להוכיח רעיון ← Build and Fix"))

cases = Scene("cases", "בוחרים מודל", [
    P("ננסה על שלושה פרויקטים. ראשון: תוכנה למשאבת אינסולין.", do=show("c1")),
    P("גוף רגולציה צריך לאשר מסמכים בסוף כל שלב, לפני שעוברים לשלב הבא. והדרישות הרפואיות לא זזות.", do=show("c1-d")),
    P("כאן התכנון המפורט והמעקב הם בדיוק מה שהרגולטור דורש. לכן Plan Driven.", do=show("c1-p")),
    P("שני: מנהל בבנק אומר: ״בואו נבנה את מערכת ההעברות החדשה מהר, נכתוב קוד ונתקן תוך כדי.״", do=show("c2")),
    P("זה נשמע כמו Build and Fix, אבל זו מערכת גדולה שתחיה שנים. השיטה הזו טובה רק כדי להוכיח שרעיון עובד. כאן היא בחירה שגויה.",
      do=show("c2-p")),
    P("שלישי: סטארט-אפ שבונה אפליקציה, ועוד לא יודע מה המשתמשים באמת ירצו.", do=show("c3")),
    P("הדרישות ישתנו הרבה. כאן Waterfall הוא בחירה שגויה. מה כן מתאים? את זה נראה ברמה הבאה.",
      do=show("c3-p"), hold=0.4),
], stage=w.stack(
    *[f'<div id="{i}" class="pr-need h"><span class="pr-nd">{t}<span id="{i}-d" class="pr-ndd h">{d}</span></span>'
      f'<span class="pr-arr">←</span><span id="{i}-p" class="pr-pat h">{p}</span></div>'
      for i, t, d, p in [
          ("c1", "💉 תוכנה למשאבת אינסולין", "רגולטור מאשר כל שלב, דרישות קבועות", w.en("Plan Driven")),
          ("c2", "🏦 ״נכתוב ונתקן תוך כדי״", "מערכת העברות גדולה, לשנים", "<span style='color:var(--bad)'>לא " + w.en("Build and Fix") + "</span>"),
          ("c3", "🚀 סטארט-אפ", "לא יודעים מה המשתמשים ירצו", "<span style='color:var(--bad)'>לא " + w.en("Waterfall") + "</span>")]],
    gap=26), layout="full")

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו שאלה ממבחן: מתי פיתוח בשיטת מפל המים יהיה מועיל?"),
    P("נפעיל את המתכון, ונחפש תשובה שבה הדרישות ידועות ויציבות, ויש צורך בבקרה.", do=show("x1")),
    P("יחסי ספק ולקוח, עם לוחות זמנים קשיחים ותפוקות מוגדרות היטב. בדיוק זה.", do=show(f"q-ok-{OK}")),
    P("כשהתפוקות מוגדרות מראש, אפשר לתכנן כל שלב, ולעקוב אחרי ההתקדמות מול החוזה.", do=show("x2")),
    P("״שינויים רבים בדרישות במהלך הפיתוח״ הפוך לגמרי. שם Waterfall הוא בחירה שגויה.", do=show(f"q-x-{CHG}", f"q-n-{CHG}")),
    P("״לא ברור מי יהיה הלקוח הסופי״? אז אי אפשר להגדיר את הדרישות מראש. גם זה נגד Waterfall.",
      do=show(f"q-x-{WHO}", f"q-n-{WHO}")),
    P("ו״מערכת להרבה לקוחות שונים״ היא מוצר גנרי. זה אומר למי מוכרים, ולא אם הדרישות יציבות.",
      do=show(f"q-x-{MANY}", f"q-n-{MANY}")),
    P("וזו המלכודת: תשובה נשמעת ״מקצועית״ לא מספיקה. השאלה היא תמיד על יציבות הדרישות.", do=show("x3"), hold=0.5),
], stage=w.stack(st.card("x1", "rule", "🔑 מחפשים: דרישות <b>ידועות ויציבות</b> + בקרה"),
                 st.card("x2", "ex", "📄 תפוקות מוגדרות + לוח זמנים קשיח ← אפשר לתכנן כל שלב מראש"),
                 st.card("x3", "trap", "⚠️ ״הרבה לקוחות״ = מוצר גנרי. זה לא קריטריון לבחירת מודל"), gap=26),
   panel=w.qpanel(w.stem(Q["id"], Q["question"]),
                  st.options("q", OPTS, notes={CHG: "דרישות משתנות", WHO: "אין דרישות מראש", MANY: "לא רלוונטי"})))

recap = Scene("recap", "סיכום", [
    P("לסיכום: דרישות, תיכון, קידוד, בדיקות ותחזוקה. ולפניהם, לפעמים, חקר ישימות.", do=show("s1")),
    P("Waterfall: שלבים בסדר קבוע. מתאים לדרישות ידועות ויציבות.", do=show("s2")),
    P("Plan Driven: תכנון מפורט ובקרה לפרויקט גדול. Build and Fix: רק כדי להראות שרעיון עובד.", do=show("s3")),
    P("ודרישות שישתנו הרבה? לא Waterfall. נתראה ברמה הבאה.", do=show("s4"), hold=0.6),
], stage=MODELS.replace('id="m', 'id="z').replace(' class="h"', ''),
   panel=st.card("s1", "rule", "🔑 דרישות ← תיכון ← קידוד ← בדיקות ← תחזוקה")
         + st.card("s2", "rule", "🔑 יציבות ובקרה ← Waterfall / Plan Driven")
         + st.card("s3", "rule", "🔑 להוכיח רעיון ← Build and Fix")
         + st.card("s4", "trap", "⚠️ דרישות משתנות ← לא Waterfall"))

SCENES = [title, stages, water, models, cases, exam, recap]
w.no_latin(SCENES)
VIDEO = Video("R02", "proc", "מודלי תהליך: Waterfall ו-Build and Fix", SCENES, bank={"19B-B-Q6": OK})
