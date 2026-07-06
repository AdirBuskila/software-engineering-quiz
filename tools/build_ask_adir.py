# -*- coding: utf-8 -*-
"""Generate docs/ask_adir.md — everything that needs Adir's input or review:
   (1) scanned exams to paste, (2) flagged / low-confidence questions to verify."""
import json, pathlib, collections, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

TOOLS = pathlib.Path(__file__).parent
RAW = TOOLS / "raw"
DOCS = TOOLS.parent / "docs"
HE = ["א","ב","ג","ד","ה","ו","ז","ח"]

EXAM_LABEL = json.loads((TOOLS/"_exam_labels.json").read_text(encoding="utf-8")) \
    if (TOOLS/"_exam_labels.json").exists() else {}

CODES = ["19B-B","19B-C","20-A","20-B","21-A","21-B","21S-A","21S-B","22B-A","22S-A",
         "23-EX","23B-A","23S-A","24B-A","24B-B","24S-A","25F0a","25F0b","25S-A","25B-N","25-EX",
         "SP-SPC","SP-DGM","SP-AMR","SP-MDA"]

L = []
L.append("# רשימת \"לשאול את אדיר\" — פריטים לאימות / השלמה\n")
L.append("נוצר אוטומטית מקובצי ה-raw. שני חלקים: מבחנים סרוקים להשלמה, ושאלות שסומנו לאימות.\n")

L.append("## 1) מבחנים סרוקים — חולצו והוכנסו לבנק (לאימות מול מפתח אם קיים)\n")
L.append("שלושת המבחנים הסרוקים נקראו חזותית מהתמונות והוכנסו לבנק. אין להם קובץ פתרונות, "
         "ולכן התשובות **נגזרו** (מסומנות 'לא רשמי') — שאלותיהם המסומנות מופיעות בסעיף 2. "
         "אם יש לך מפתח פתרונות עבורם, שלח ואהפוך את תשובותיהם לרשמיות:\n")
L.append("| קוד | מבחן | שאלות |")
L.append("|---|---|---|")
L.append("| 21-A | 2021 מבחן מועד א | 10 (Q4 תלוית תרשים — הוצאה עד לצירוף תמונה) |")
L.append("| 21-B | 2021 מבחן מועד ב | 10 |")
L.append("| 23B-A | 2023 סמסטר ב מועד א | 14 |")
L.append("")

# ---- flagged / low-confidence questions ----
rows = []
by_exam = collections.defaultdict(list)
for code in CODES:
    p = RAW / f"{code}.json"
    if not p.exists():
        continue
    for q in json.loads(p.read_text(encoding="utf-8")):
        if q.get("verified"):   # independently re-derived & confirmed — no longer needs Adir
            continue
        conf = q.get("confidence", "?")
        flag = q.get("flag")
        if flag or conf == "low":
            ci = q.get("correctIndex", 0)
            letter = HE[ci] if isinstance(ci, int) and ci < len(HE) else "?"
            by_exam[code].append((q.get("num"), conf, letter, q.get("official"),
                                  q.get("question","")[:90], flag or ""))

total = sum(len(v) for v in by_exam.values())
L.append(f"## 2) שאלות שסומנו לאימות ({total})\n")
L.append("שאלות אלו **נמצאות בבנק** אך סומנו כטעונות בדיקה (רובן נגזרו ללא מחוון רשמי, "
         "או תלויות בתרשים, או תשובת טופס-0 שנויה במחלוקת). מסודרות לפי מבחן. "
         "עדיפות גבוהה: אלו עם `low`.\n")
for code in CODES:
    if code not in by_exam:
        continue
    L.append(f"### {code}")
    L.append("| # | ביטחון | תשובה | רשמי? | שאלה | הערה |")
    L.append("|---|---|---|---|---|---|")
    for num, conf, letter, official, qtext, flag in sorted(by_exam[code], key=lambda x: (x[1]!='low', x[0] or 0)):
        qtext = qtext.replace("|","/").replace("\n"," ")
        flag = flag.replace("|","/").replace("\n"," ")
        L.append(f"| {num} | {conf} | {letter} | {'✓' if official else '—'} | {qtext} | {flag} |")
    L.append("")

L.append("## 3) הערות נוספות\n")
L.append("- **25S-A** (טופס א): כל 20 התשובות שנגזרו נפלו על אפשרות א — ייתכן שזהו למעשה טופס-0 "
         "(תשובה תמיד ראשונה). שווה לאמת מול מפתח אם קיים.\n")
L.append("- **SP-SPC** (מועד מיוחד): כולו שאלות פתוחות/דיאגרמות — 0 שאלות אמריקאיות, לא נכלל.\n")
L.append("- **SP-MDA**: רק 3 שאלות אמריקאיות (השאר Part B פתוח); 2 מהן תלויות תרשים.\n")
L.append("- **שאלות `hasImage`** הוצאו מהבנק עד לצירוף תמונה. כדי לכלול אחת — הוסף "
         "`images/exams/<CODE>-Q<num>.png` והרץ מחדש את `build_questions.py`.\n")

DOCS.mkdir(exist_ok=True)
(DOCS / "ask_adir.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print(f"wrote docs/ask_adir.md — {total} flagged questions across {len(by_exam)} exams")
