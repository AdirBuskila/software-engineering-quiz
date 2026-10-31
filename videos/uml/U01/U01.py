# -*- coding: utf-8 -*-
"""U01 · מפת התרשימים: לאיזה מודל שייך כל תרשים? — video script (build: tools/video/vid.py U01).

Source: courses/uml/U01.js (lesson + goal: why several UML diagrams, and the diagram -> model table).
Exam anchor: SP-DGM-Q5 ("to which model does UML belong" -> none of the answers), which no guided quiz uses and which
has no twin in the bank. The diagram -> model table is checked against the course checker (w_uml.CHK.MODEL).
Avoided on purpose: the U01 quiz items (the four "which model is diagram X" questions are not asked as questions here:
the table is taught, then applied to a food-delivery app of my own), 26S-A-Q13 (U01 quiz), 25B-N-Q17 / 25F0a-Q15
(boss), 25F0b-Q16 / 26CL-Q9 (cited as lesson examples), and 20-A-Q2 / 20-B-Q1.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_uml as w

# ---------------------------------------------------------------- facts (checked)
M = w.CHK.MODEL
assert M == {"class": "Structure", "sequence": "Interaction", "usecase": "Interaction", "activity": "Context",
             "statechart": "Behavior"}
HEB_MODEL = {"Structure": "מבנה", "Interaction": "אינטראקציה", "Context": "הקשר", "Behavior": "התנהגות"}
# the worked example: which diagram each picture is, and so its model
EX = [("e1", "class", "class"), ("e2", "sequence", "sequence"), ("e3", "usecase", "usecase"),
      ("e4", "state", "statechart"), ("e5", "activity", "activity")]

# exam SP-DGM-Q5
Q = BANK["SP-DGM-Q5"]
assert Q["correctIndex"] == 1 and Q["options"][1] == "אף אחת מהתשובות איננה נכונה"
assert [Q["options"][k] for k in (0, 2, 3)] == ["interaction model", "structure model", "Behavior model"]
# UML has diagrams of every model, so no single model is its model
assert len(set(M.values())) == 4
OPTS = w.opts_of(Q)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נבין למה ב-UML יש כמה סוגי תרשימים."),
    P("נבנה מפה קטנה: כל תרשים, ולאיזה מודל הוא שייך."),
    P("ובסוף נפתור שאלה אמיתית ממבחן, עם מלכודת קטנה.", hold=0.4),
], stage='<div class="kicker">U01 · UML ומידול</div><h1>מפת התרשימים: לאיזה מודל שייך כל תרשים?</h1>'
         '<p>להסביר למה משתמשים בכמה תרשימי UML, ולשייך כל תרשים (מחלקות, רצף, Use Case, פעילות, מצבים) למודל שלו.</p>',
   layout="title")

LENS = [("l1", "ממה המערכת בנויה?"), ("l2", "מי מדבר עם מי?"), ("l3", "איך התהליך זורם?"), ("l4", "באילו מצבים היא יכולה להיות?")]
idea = Scene("idea", "הרעיון", [
    P("UML היא שפת מידול גרפית. מתארים בה מערכת אחת בכמה נקודות מבט.", do=show("i-sys")),
    P("קחו אפליקציה למשלוחי אוכל. אפשר לשאול עליה כמה שאלות שונות.", do=show("i-c1")),
    P("ממה היא בנויה? אילו מחלקות יש בה, ואיך הן קשורות?", do=show("l1")),
    P("מי מדבר עם מי, ובאיזה סדר?", do=show("l2")),
    P("איך התהליך זורם, מהזמנה ועד משלוח?", do=show("l3")),
    P("ובאילו מצבים הזמנה יכולה להיות?", do=show("l4"), hold=0.3),
    P("לכל שאלה כזו יש תרשים משלה. רק כשמחברים את כולם, מקבלים תמונה של האפליקציה.", do=show("i-c2")),
], stage=w.stack('<div id="i-sys" class="u-big h">🍔 אפליקציית משלוחים</div>',
                 *[f'<div id="{k}" class="card ex h" style="width:760px;text-align:center">{t}</div>' for k, t in LENS],
                 gap=24),
   panel=st.card("i-c1", "plain", "מערכת אחת, כמה <b>נקודות מבט</b> (Perspectives)")
         + st.card("i-c2", "rule", "🔑 ארבע שאלות על אותה אפליקציה ← ארבעה סוגי תרשימים"))

ROWS = [("r-st", ["<b>Structure</b> מבנה", "ממה בנויה", "מחלקות"]),
        ("r-in", ["<b>Interaction</b> אינטראקציה", "מי מדבר עם מי", "Use Case, רצף"]),
        ("r-cx", ["<b>Context</b> הקשר", "איך התהליך זורם", "פעילות"]),
        ("r-be", ["<b>Behavior</b> התנהגות", "באילו מצבים", "מצבים"])]
assert M["class"] == "Structure" and M["usecase"] == M["sequence"] == "Interaction"
assert M["activity"] == "Context" and M["statechart"] == "Behavior"
table = Scene("map", "ארבעה מודלים", [
    P("את השאלות האלה הקורס מארגן בארבעה מודלים.", do=show("m")),
    P("מודל המבנה: ממה המערכת בנויה. התרשים שלו הוא **תרשים המחלקות**.", do=show("t-r-st"),
      say="מודל המבנה, סְטְרַקְצֶ'ר: ממה המערכת בנויה. התרשים שלו הוא תרשים המחלקות."),
    P("מודל האינטראקציה: מי מדבר עם המערכת ועם מי. יש לו שני תרשימים: Use Case ו**תרשים רצף**.", do=show("t-r-in"),
      say="מודל האינטראקציה: מי מדבר עם המערכת ועם מי. יש לו שני תרשימים: יוּז קֵייס ותרשים רצף."),
    P("מודל ההקשר: איך התהליך וזרימת העבודה מתנהלים. התרשים שלו הוא **תרשים פעילות**.", do=show("t-r-cx"),
      say="מודל ההקשר, קוֹנְטֶקְסְט: איך התהליך וזרימת העבודה מתנהלים. התרשים שלו הוא תרשים פעילות."),
    P("ומודל ההתנהגות: באילו מצבים המערכת יכולה להיות. התרשים שלו הוא **תרשים מצבים**.", do=show("t-r-be"),
      say="ומודל ההתנהגות, בִּיהֵייבְיוֹר: באילו מצבים המערכת יכולה להיות. התרשים שלו הוא תרשים מצבים.", hold=0.3),
    P("שימו לב: לאינטראקציה יש שני תרשימים, ולכל מודל אחר יש תרשים אחד.", do=show("m-c1")),
    P("ושאלות המבחן חוזרות על הטבלה הזו שוב ושוב, כל פעם עם מסיחים אחרים.", do=show("m-c2")),
], stage=w.stack('<div id="m" class="u-note h">המודל · השאלה · התרשים</div>',
                 w.grid("t", ROWS, cls="c3"), gap=20),
   panel=st.card("m-c1", "rule", "🔑 אינטראקציה = <b>Use Case</b> וגם <b>רצף</b>")
         + st.card("m-c2", "ex", "מחלקות = מבנה · פעילות = הקשר · מצבים = התנהגות"))

KIND_HEB = {"class": "תרשים מחלקות", "sequence": "תרשים רצף", "usecase": "תרשים Use Case", "state": "תרשים מצבים",
            "activity": "תרשים פעילות"}
SWAP = '<div class="swap" style="--swap-h:470px">' + "".join(
    f'<div id="{k}" class="h">{w.mini(kind, k + "d")}</div>' for k, kind, _ in EX) + "</div>"
ANS = w.grid("a", [(f"{k}a", [KIND_HEB[kind], f"<b>{M[key]}</b> · {HEB_MODEL[M[key]]}"]) for k, kind, key in EX])
ex = Scene("ex", "דוגמה: אפליקציית משלוחים", [
    P("עכשיו נזהה. לפניכם חמישה תרשימים של אותה אפליקציה. כל פעם: איזה תרשים זה, ולאיזה מודל הוא שייך."),
    P("כאן יש מלבנים עם שם, תכונות ופעולות, וקווים ביניהם. אלה מחלקות.", do=show("e1")),
    P("זה תרשים מחלקות, ולכן מודל המבנה.", do=show("a-e1a"), hold=0.2),
    P("כאן יש משתתפים בראש, קווים אנכיים מקווקווים, וחיצים שיורדים בזמן.", do=hide("e1") + show("e2")),
    P("זה תרשים רצף: הודעות בין משתתפים. מודל האינטראקציה.", do=show("a-e2a"), hold=0.2),
    P("כאן יש איש מקל, מסגרת של מערכת ואליפסות של שירותים.", do=hide("e2") + show("e3")),
    P("זה תרשים Use Case: מי משתמש במערכת ולמה. גם הוא אינטראקציה.", do=show("a-e3a"),
      say="זה תרשים יוּז קֵייס: מי משתמש במערכת ולמה. גם הוא אינטראקציה.", hold=0.2),
    P("כאן יש מצבים של הזמנה: התקבלה, בדרך, נמסרה. ומעברים ביניהם.", do=hide("e3") + show("e4")),
    P("זה תרשים מצבים, ולכן מודל ההתנהגות.", do=show("a-e4a"), hold=0.2),
    P("וכאן יש פעילויות, ופסים מלאים שמפצלים ומאחדים: בישול וחיוב קורים במקביל.", do=hide("e4") + show("e5")),
    P("זה תרשים פעילות: זרימה של תהליך. מודל ההקשר.", do=show("a-e5a"), hold=0.3),
], stage=SWAP, panel=ANS)

UML_SVG = w.Dia("um", 1000, 470)
UML_SVG.state("lang", 330, 10, 340, 90, "השפה UML", rx=14)
for i, (k, name, model) in enumerate([("c", "מחלקות", "Structure"), ("s", "רצף", "Interaction"),
                                      ("a", "פעילות", "Context"), ("b", "מצבים", "Behavior")]):
    x = 20 + i * 250
    UML_SVG.state(f"d{k}", x, 220, 210, 80, name, hidden=True)
    UML_SVG.rel(f"l{k}", "lang", f"d{k}", "assoc", hidden=True)
    UML_SVG.text(f"t{k}", x + 105, 350, model, cls="u-lab warn", hidden=True)
UML_SVG.ring("ring", 318, -2, 364, 114)
exam = Scene("exam", "שאלה ממבחן", [
    P("שאלה ממבחן: לאיזה מודל שייך ה-UML?"),
    P("שלוש תשובות הן שמות של מודלים, ותשובה אחת אומרת שאף אחת לא נכונה."),
    P("נחזור למפה. UML היא השפה. בעזרתה מציירים את כל התרשימים.", do=show("um-ring")),
    P("תרשים מחלקות, ששייך למבנה.", do=show("um-dc", "um-lc", "um-tc")),
    P("תרשים רצף, ששייך לאינטראקציה.", do=show("um-ds", "um-ls", "um-ts")),
    P("ותרשימי פעילות ומצבים, ששייכים להקשר ולהתנהגות.", do=show("um-da", "um-la", "um-ta", "um-db", "um-lb", "um-tb")),
    P("אז UML לא שייכת למודל אחד. היא מכילה תרשימים של כל המודלים.", hold=0.3),
    P("מודל האינטראקציה הוא רק של Use Case ושל רצף.", do=show("q-x-0", "q-n-0"),
      say="מודל האינטראקציה הוא רק של יוּז קֵייס ושל רצף."),
    P("מודל המבנה הוא רק של תרשים המחלקות.", do=show("q-x-2", "q-n-2")),
    P("ומודל ההתנהגות הוא רק של תרשים המצבים.", do=show("q-x-3", "q-n-3")),
    P("ולכן התשובה: אף אחת מהתשובות איננה נכונה.", do=show("q-ok-1"), hold=0.3),
    P("המלכודת: לחפש מודל, כשבכלל שאלו על השפה עצמה.", do=show("x-t"), hold=0.5),
], stage=w.stack(UML_SVG.svg(), st.card("x-t", "trap", "⚠️ UML אינה מודל: היא השפה שבה מציירים תרשימים של כל המודלים"),
                 gap=10),
   panel=w.stem(Q["id"], "לאיזה מודל שייך ה-UML?")
         + st.options("q", OPTS, notes={0: "רק Use Case ורצף", 2: "רק מחלקות", 3: "רק מצבים"}))

recap = Scene("recap", "סיכום", [
    P("לסיכום: מערכת אחת, כמה נקודות מבט, ולכל אחת תרשים משלה.", do=show("r-1")),
    P("תרשים המחלקות שייך למבנה. תרשים Use Case ותרשים הרצף שייכים לאינטראקציה.", do=show("r-2"),
      say="תרשים המחלקות שייך למבנה. תרשים יוּז קֵייס ותרשים הרצף שייכים לאינטראקציה."),
    P("תרשים הפעילות שייך להקשר, ותרשים המצבים שייך להתנהגות.", do=show("r-3")),
    P("ו-UML עצמה אינה מודל: היא השפה. נתראה ברמה הבאה.", do=show("r-4"), hold=0.6),
], stage=w.grid("rt", ROWS, cls="c3", hidden=False),
   panel=st.card("r-1", "rule", "🔑 שאלה אחרת על המערכת ← תרשים אחר")
         + st.card("r-2", "rule", "🔑 מחלקות = מבנה · Use Case ורצף = אינטראקציה")
         + st.card("r-3", "rule", "🔑 פעילות = הקשר · מצבים = התנהגות")
         + st.card("r-4", "trap", "⚠️ UML היא שפה, לא מודל"))

SCENES = [title, idea, table, ex, exam, recap]
w.no_latin(SCENES)
VIDEO = Video("U01", "uml", "מפת התרשימים: לאיזה מודל שייך כל תרשים?", SCENES, bank={"SP-DGM-Q5": 1})
