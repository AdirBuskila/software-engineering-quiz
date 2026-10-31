# -*- coding: utf-8 -*-
"""R01 · מה זו הנדסת תוכנה? — video script (build: tools/video/vid.py R01).

Source: courses/proc/R01.js (lesson + goal: SE vs CS, professional development, generic vs customized products).
Exam anchor: 22S-A-Q5 (an app built for one bank, changed to serve more banks -> Customized to Generic). No guided quiz
uses it and it has no twin in the bank.
Avoided on purpose: the R01 quiz items (25F0b-Q2 the resource-wasting attribute, 23B-A-Q6 and its twin 23S-A-Q5, and the
three originals: maintenance vs complexity, where the cost peaks as a question, the payroll vendor) and their twins
(25B-N-Q1, 25F0a-Q1, 21-A-Q1, 21S-A-Q1, 26B-A-Q2). Efficiency is left out of the quality attributes, since naming it
for wasted resources answers 25F0b-Q2. SE's scope is said as "the whole life of the system, years after launch",
not 23B-A-Q6's key wording ("from documentation to maintenance"). Worked cases are mine: a sorting algorithm vs a clinic booking system, a
student script vs a team product, a navigation app, a hospital shift system, an inventory system with a supermarket
module, a discount fix that breaks invoices.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_proc as w

# ---------------------------------------------------------------- facts (checked)
assert w.CHK["COST_PEAK"] == "after_delivery"          # the course checker: most of the cost comes after delivery
Q = BANK["22S-A-Q5"]
OK = w.opt_index(Q, "Customized products ל-Generic")
assert Q["correctIndex"] == OK == 1
GC = w.opt_index(Q, "Generic products ל-Customized")
NONE = w.opt_index(Q, "אין תשובה")
VERY = w.opt_index(Q, "Very Customize")
assert sorted([OK, GC, NONE, VERY]) == [0, 1, 2, 3]
OPTS = w.opts_of(Q)

# product kind: (sold to a broad market?) -> (kind, who sets the requirements), the lesson's table
def product(broad_market):
    return ("Generic", "היצרן") if broad_market else ("Customized", "הלקוח")
assert product(True) == ("Generic", "היצרן") and product(False) == ("Customized", "הלקוח")
# the exam case: the app started for one bank (not broad) and moves to serve many banks (broad)
assert (product(False)[0], product(True)[0]) == ("Customized", "Generic")

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נבין מה זו הנדסת תוכנה, ובמה היא שונה ממדעי המחשב."),
    P("נראה מה הופך פיתוח ל**מקצועי**, ונבדיל בין מוצר גנרי למוצר מותאם."),
    P("ובסוף נפתור שאלה אמיתית ממבחן.", hold=0.4),
], stage='<div class="kicker">R01 · תהליכים, Agile ודרישות</div><h1>מה זו הנדסת תוכנה?</h1>'
         '<p>במה הנדסת תוכנה שונה ממדעי המחשב, מה מיוחד בפיתוח מקצועי, ומה ההבדל בין מוצר גנרי למוצר מותאם.</p>',
   layout="title")

CMP = w.table("c", ["", "מדעי המחשב", "הנדסת תוכנה"], [
    ["במה מתמקדים", "תיאוריה: אלגוריתמים וחישוביות", "בניית מערכות אמיתיות"],
    ["איך", "הוכחות וניתוח", "עקרונות הנדסיים: עיצוב, בדיקות, תקציב, ניהול"],
    ["עד מתי", "עד שהרעיון מוכח", "<b>כל חיי המערכת</b>: גם שנים אחרי ההשקה"],
], widths=[170, 360, 440], size=28)

idea = Scene("idea", "הנדסה מול מדע", [
    P("נתחיל בשאלה: מה ההבדל בין מדעי המחשב להנדסת תוכנה?"),
    P("מדעי המחשב עוסקים בתיאוריה: אלגוריתמים, חישוביות, ומה אפשר לחשב בכלל.", do=show("c-r0")),
    P("הנדסת תוכנה **מיישמת עקרונות הנדסיים**: עיצוב, בדיקות, תקציב וניהול, כדי לבנות מערכות.", do=show("c-r1")),
    P("והיא לא נגמרת ביום ההשקה. היא מלווה את המערכת כל עוד משתמשים בה, גם שנים אחר כך.", do=show("c-r2"), hold=0.3),
    P("דוגמה. למצוא אלגוריתם מיון מהיר יותר, ולהוכיח את זה: זו שאלה של מדעי המחשב.", do=show("e1")),
    P("לבנות מערכת זימון לרשת מרפאות, בתקציב ובלוח זמנים, ולתחזק אותה שנים: זו הנדסת תוכנה.", do=show("e2")),
    P("ולמה התחזוקה כל כך חשובה? כי ברוב המערכות, עיקר העלות מגיע **אחרי** שהמערכת כבר בשימוש.", do=show("i-r")),
    P("תיקונים, שינויים והתאמות. לכן התחזוקה היא חלק מרכזי בהנדסת תוכנה, ולא נספח.", hold=0.4),
], stage=w.stack(CMP, w.row(st.card("e1", "ex", "🧮 אלגוריתם מיון מהיר יותר ← מדעי המחשב"),
                            st.card("e2", "ex", "🏥 מערכת זימון לרשת מרפאות ← הנדסת תוכנה"), gap=18), gap=30),
   panel=st.card("i-r", "rule", "🔑 עיקר העלות: <b>אחרי</b> שהמערכת בשימוש. לכן תחזוקה היא לב התחום"))

PRO = w.table("pr", ["", "סקריפט אישי", "פיתוח מקצועי"], [
    ["מי כותב", "אדם אחד", "<b>צוות</b>"],
    ["מה מקבלים", "קוד בלבד", "קוד + <b>תיעוד</b>, קונפיגורציה, בדיקות"],
    ["בשביל מה", "צורך אישי", "<b>צורך עסקי</b> של לקוח או ארגון"],
], widths=[180, 300, 470], size=29)

pro = Scene("pro", "פיתוח מקצועי", [
    P("הנדסת תוכנה נועדה בעיקר לתמוך ב**פיתוח תוכנה מקצועי**. אז מה הופך פיתוח למקצועי?"),
    P("נשווה. סטודנטית כותבת לעצמה סקריפט שמחשב ממוצע ציונים. מצד שני, צוות בונה מערכת לחברת ביטוח.", do=show("pr-x")),
    P("ההבדל הראשון: פיתוח מקצועי נעשה בדרך כלל **בצוותים**, ולא על ידי אדם אחד.", do=show("pr-r0")),
    P("השני: מקבלים לא רק קוד. מחויבים גם בתיעוד, בקונפיגורציה, ובבדיקות.", do=show("pr-r1")),
    P("והשלישי: התוכנה נועדה לצורך עסקי, של לקוח או של ארגון.", do=show("pr-r2"), hold=0.3),
    P("שימו לב: ההבדל הוא לא בשפת התכנות, ולא בגודל של קובץ אחד. ההבדל הוא באופן העבודה.", do=show("pr-t"), hold=0.4),
], stage=w.stack(f'<div id="pr-x" class="pr-row h" style="gap:24px;font-size:30px"><span>👩‍🎓 סקריפט לממוצע ציונים</span>'
                 f'<span style="color:var(--muted)">מול</span><span>👥 מערכת לחברת ביטוח</span></div>', PRO, gap=30),
   panel=st.card("pr-t", "trap", "⚠️ לא השפה ולא הגודל: <b>אופן העבודה</b> קובע"))

GEN = w.table("g", ["", w.en("Generic Product"), w.en("Customized Product")], [
    ["למי", "שוק רחב, הרבה לקוחות", "לקוח אחד מסוים"],
    ["מי קובע דרישות", "<b>היצרן</b>", "<b>הלקוח</b>"],
    ["דוגמה", "🧭 אפליקציית ניווט לכולם", "🏥 שיבוץ משמרות לבית חולים אחד"],
], widths=[200, 380, 400], size=28)

gen = Scene("gen", "גנרי מול מותאם", [
    P("עכשיו שני סוגי מוצרים. מוצר **גנרי** נבנה לשוק רחב, ונמכר להרבה לקוחות.", do=show("g-r0")),
    P("מוצר **מותאם** נבנה בשביל לקוח אחד מסוים."),
    P("ומי קובע את הדרישות? בגנרי, **היצרן** מחליט מה יהיה במוצר. במותאם, **הלקוח** מחליט.", do=show("g-r1")),
    P("למשל, אפליקציית ניווט שכל אחד מוריד היא גנרית. מערכת שיבוץ משמרות שנבנתה לבית חולים אחד היא מותאמת.",
      do=show("g-r2")),
    P("ואפשר לעבור בין הסוגים, בשני הכיוונים.", do=show("g-a1")),
    P("ממותאם לגנרי: **אוספים דרישות מלקוחות נוספים**, ועושים שימוש חוזר במה שכבר נבנה, תוך התאמה.", do=show("g-a2")),
    P("ומגנרי למותאם: בונים את המוצר הגנרי עם **אפשרות להוסיף קוד** בפיתוח עצמי.", do=show("g-a3")),
    P("למשל, מערכת מלאי גנרית, ורשת סופרמרקטים מפתחת מעליה מודול משלה, בלי לגעת בליבה.", do=show("g-a4")),
    P("בגלל המעברים האלה, ההבדל בין שני הסוגים הולך ומיטשטש.", hold=0.4),
], stage=w.stack(GEN, gap=20),
   panel=st.card("g-a1", "plain", "<b>מעברים בין הסוגים</b>")
         + st.card("g-a2", "ex", "מותאם ← גנרי: דרישות מ<b>לקוחות נוספים</b> + שימוש חוזר")
         + st.card("g-a3", "ex", "גנרי ← מותאם: מוצר עם <b>אפשרות להוסיף קוד</b>")
         + st.card("g-a4", "plain", "🛒 מערכת מלאי גנרית + מודול של רשת סופרמרקטים"))

qual = Scene("qual", "תכונות של תוכנה טובה", [
    P("ועוד נושא קטן שמופיע במבחנים: התכונות החיוניות של תוכנה מקצועית. נראה שלוש מהן."),
    P("Maintainability: כמה קל לשנות את התוכנה בבטחה.", do=show("q1")),
    P("נגיד שתיקון קטן בחישוב ההנחה גורם פתאום לבאג בהדפסת החשבונית. זו בדיוק תוכנה שקשה לתחזק.", do=show("q1x")),
    P("Dependability, אמינות ואבטחה: התוכנה לא קורסת, ולא נפרצת.", do=show("q2")),
    P("Acceptability: המשתמשים שהיא נבנתה בשבילם מבינים אותה, ונוח להם לעבוד איתה.", do=show("q3")),
    P("בשאלה כזו, קראו בדיוק **מה** השתבש בתיאור, ורק אז בחרו את התכונה.", do=show("q-t"), hold=0.4),
], stage=w.stack(
    st.card("q1", "rule", f'🔧 {w.en("Maintainability")}: קל לשנות בבטחה'),
    st.card("q1x", "ex", "תיקון בחישוב ההנחה ← באג בהדפסת החשבונית = חסרה תחזוקתיות"),
    st.card("q2", "rule", f'🛡️ {w.en("Dependability")} &amp; Security: לא קורסת, לא נפרצת'),
    st.card("q3", "rule", f'🙂 {w.en("Acceptability")}: מובנת ונוחה למשתמשים שלה'), gap=22),
   panel=st.card("q-t", "trap", "⚠️ קודם <b>מה השתבש</b> בתיאור, אחר כך שם התכונה"))

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו שאלה ממבחן. חברה פיתחה אפליקציה בנקאית בשביל בנק אחד, ״בנק ירושלים״."),
    P("עכשיו היא משנה את האפליקציה, כך שתשרת גם בנקים נוספים. איך מגדירים את המהלך?"),
    P("צעד ראשון: מה היה המוצר בהתחלה? אפליקציה שנבנתה לבנק **אחד**, לפי הדרישות שלו. זה מוצר מותאם.", do=show("x1")),
    P("צעד שני: לאן הוא הולך? למוצר שמשרת **הרבה** בנקים. זה מוצר גנרי.", do=show("x2")),
    P("ולכן התשובה: מעבר ממוצר מותאם למוצר גנרי.", do=show(f"q-ok-{OK}")),
    P("ומה החברה תעשה בפועל? תאסוף דרישות מהבנקים הנוספים, ותשתמש שוב באפליקציה הקיימת, עם התאמות.", do=show("x3")),
    P("המעבר ההפוך, מגנרי למותאם, הוא בדיוק המלכודת. הוא היה נכון אם מוצר לכולם היה מותאם ללקוח אחד.",
      do=show(f"q-x-{GC}", f"q-n-{GC}")),
    P("״מותאם מאוד״ הוא לא סוג של מוצר. וחוץ מזה, כאן מתרחבים להרבה לקוחות, לא מעמיקים את ההתאמה ללקוח אחד.",
      do=show(f"q-x-{VERY}", f"q-n-{VERY}")),
    P("ואם יש תשובה נכונה, האפשרות ״אין תשובה נכונה״ נופלת מעצמה.", do=show(f"q-x-{NONE}", f"q-n-{NONE}"), hold=0.5),
], stage=w.stack(
    w.row(st.card("x1", "ex", "🏦 לבנק אחד, לפי דרישותיו<br>= <b>מותאם</b>"),
          st.card("x2", "ex", "🏦🏦🏦 להרבה בנקים<br>= <b>גנרי</b>"), gap=24),
    st.card("x3", "rule", "🔑 מותאם ← גנרי: דרישות מלקוחות נוספים + שימוש חוזר במוצר הקיים"), gap=30),
   panel=w.qpanel(w.stem(Q["id"], "אפליקציה בנקאית שפותחה ל״בנק ירושלים״ משתנה כדי לשרת בנקים נוספים. איך מגדירים את המהלך?")
         + st.options("q", OPTS, notes={GC: "כיוון הפוך", VERY: "אין סוג כזה", NONE: "יש תשובה"})))

recap = Scene("recap", "סיכום", [
    P("לסיכום: מדעי המחשב עוסקים בתיאוריה. הנדסת תוכנה בונה מערכות, ומלווה אותן כל עוד הן בשימוש.", do=show("s1")),
    P("ועיקר העלות מגיע אחרי שהמערכת בשימוש.", do=show("s2")),
    P("פיתוח מקצועי: צוות, תיעוד וקונפיגורציה, וצורך עסקי.", do=show("s3")),
    P("גנרי: שוק רחב, והיצרן קובע. מותאם: לקוח אחד, והוא קובע. נתראה ברמה הבאה.", do=show("s4"), hold=0.6),
], stage=w.stack(GEN.replace('id="g', 'id="z').replace(' class="h"', ''), gap=20),
   panel=st.card("s1", "rule", "🔑 הנדסת תוכנה: כל השלבים, עד התחזוקה")
         + st.card("s2", "rule", "🔑 רוב העלות: אחרי המסירה")
         + st.card("s3", "rule", "🔑 מקצועי: צוות + תיעוד + צורך עסקי")
         + st.card("s4", "rule", "🔑 גנרי: היצרן קובע · מותאם: הלקוח קובע"))

SCENES = [title, idea, pro, gen, qual, exam, recap]
w.no_latin(SCENES)
VIDEO = Video("R01", "proc", "מה זו הנדסת תוכנה?", SCENES, bank={"22S-A-Q5": OK})
