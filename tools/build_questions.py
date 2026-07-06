# -*- coding: utf-8 -*-
"""Merge all per-exam JSON files into the final SE question dataset.

Inputs : tools/raw/<CODE>.json   (per-exam, produced by the structuring agents)
         tools/raw/practice-*.json (optional curated practice questions)
Outputs: ../questions.js   (window.QUESTIONS = [...])  -- loaded by the app
         ../questions.json  (same data)
         build_report.md    (counts, exclusions, dedup, flagged/ask-Adir list)

Rules:
- Keep 4-6 options. Exclude questions flagged hasImage (unless a figure/code is attached),
  with a blank option, <2 options, or a bad correctIndex.
- BUILD-TIME OPTION SHUFFLE: deterministically permute each question's options and
  remap correctIndex, so the stored answer is NOT trivially "first" even for form-0 exams
  (Phase-3 requirement). The app ALSO shuffles at render, so answer position is never a tell.
- DEDUP POLICY A: keep every exam's full set (so "whole exam" mode stays complete); the app
  de-duplicates the topic/random practice pool at runtime via `dedupKey`. We report the
  cross-exam duplicate count here.
- Carry a stable `dedupKey` (question + sorted option-set, pre-shuffle) for the runtime dedup.
"""
import json, re, pathlib, collections, hashlib, random, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

TOOLS = pathlib.Path(__file__).parent
RAW = TOOLS / "raw"
OUT = TOOLS.parent

EXAM_CODES = ["19B-B","19B-C","20-A","20-B","21-A","21-B","21S-A","21S-B","22B-A","22S-A",
              "23-EX","23B-A","23S-A","24B-A","24B-B","24S-A","25F0a","25F0b","25S-A","25B-N","25-EX",
              "SP-SPC","SP-DGM","SP-AMR","SP-MDA"]
PRACTICE_FILES = []  # e.g. ["practice-A.json"] once curated practice sets exist

TOPIC_LABEL = {
    "intro":"מבוא להנדסת תוכנה", "agile":"Agile · SCRUM · XP",
    "requirements":"הנדסת דרישות", "uml":"מידול ו-UML",
    "architecture":"עיצוב ארכיטקטוני", "patterns":"תבניות עיצוב",
    "solid":"עקרונות SOLID", "testing":"בדיקות ו-TDD",
    "oop_java":"OOP ו-Java", "metrics":"מטריקות ותצוגות",
    "config":"אספקה וקונפיגורציה",
}
EXAM_LABEL = {
    "19B-B":"2019 סמסטר ב׳ מועד ב׳", "19B-C":"2019 סמסטר ב׳ מועד ג׳",
    "20-A":"2020 מועד א׳", "20-B":"2020 מועד ב׳",
    "21-A":"2021 מבחן מועד א׳", "21-B":"2021 מבחן מועד ב׳",
    "23B-A":"2023 סמסטר ב׳ מועד א׳",
    "21S-A":"2021 סמסטר קיץ מועד א׳", "21S-B":"2021 סמסטר קיץ מועד ב׳",
    "22B-A":"2022 סמסטר ב׳ מועד א׳", "22S-A":"2022 סמסטר קיץ מועד א׳",
    "23-EX":"2023 מבחן לדוגמה (אקסמן)", "23S-A":"2023 סמסטר קיץ מועד א׳",
    "24B-A":"2024 סמסטר ב׳ מועד א׳ (טופס 0)", "24B-B":"2024 סמסטר ב׳ מועד ב׳ (טופס 0)",
    "24S-A":"2024 סמסטר קיץ מועד א׳ (טופס 0)", "25F0a":"2025 טופס אפס (14.8)",
    "25F0b":"2025 טופס אפס (9.11)", "25S-A":"2025 סמסטר קיץ מועד א׳ (טופס א׳)",
    "25B-N":"2025 סמסטר ב׳ מועד א׳ (ניסים)", "25-EX":"2025 מבחן לדוגמה (אקסמן)",
    "SP-SPC":"מועד מיוחד", "SP-DGM":"מבחן דוגמה",
    "SP-AMR":"מועד א׳ אמריקאי", "SP-MDA":"מבחן מועד א׳",
}
YEAR = {c: (int("20"+c[:2]) if c[:2].isdigit() else None) for c in EXAM_CODES}


def norm(s):
    return re.sub(r"\s+", " ", str(s)).strip().lower()


def dedup_key(q):
    opts = "|".join(sorted(norm(o) for o in q["options"]))
    return norm(q["question"]) + " || " + opts


def find_image(q):
    code, num = q.get("examCode"), q.get("num")
    if not code or num is None:
        return None
    for ext in ("png","jpg","jpeg","PNG","JPG","JPEG"):
        if (OUT/"images"/"exams"/f"{code}-Q{num}.{ext}").exists():
            return f"images/exams/{code}-Q{num}.{ext}"
    return None


def has_code(q):
    return bool(str(q.get("code","")).strip())


def valid(q):
    opts = q.get("options", [])
    if not (2 <= len(opts) <= 6): return False, "bad-option-count"
    if any(not str(o).strip() for o in opts): return False, "blank-option"
    ci = q.get("correctIndex")
    if not isinstance(ci, int) or ci < 0 or ci >= len(opts): return False, "bad-correctIndex"
    if not str(q.get("question","")).strip(): return False, "empty-question"
    return True, None


def shuffle_options(q):
    """Deterministic per-question permutation; remaps correctIndex. Returns (opts, ci)."""
    opts = q["options"]; ci = q["correctIndex"]
    order = list(range(len(opts)))
    seed = int(hashlib.md5(q["id"].encode("utf-8")).hexdigest(), 16) % (2**32)
    random.Random(seed).shuffle(order)
    new_opts = [opts[i] for i in order]
    new_ci = order.index(ci)
    return new_opts, new_ci


def main():
    raw_items = []
    for code in EXAM_CODES:
        p = RAW / f"{code}.json"
        if not p.exists():
            print(f"WARN: missing {code}.json — skipping"); continue
        for q in json.loads(p.read_text(encoding="utf-8")):
            q["source"] = "exam"; q["examCode"] = code
            q["sourceLabel"] = EXAM_LABEL[code]
            q.setdefault("year", YEAR.get(code))
            q["id"] = f"{code}-Q{q.get('num')}"
            raw_items.append(q)
    pidx = 0
    for fn in PRACTICE_FILES:
        for q in json.loads((RAW / fn).read_text(encoding="utf-8")):
            pidx += 1
            q["source"] = "practice"; q["examCode"] = None
            q["sourceLabel"] = "תרגול" + (f" · {q['chapter']}" if q.get("chapter") else "")
            q["year"] = None; q["id"] = f"P-{pidx}"
            raw_items.append(q)

    excl = collections.Counter(); kept = []
    for q in raw_items:
        ok, why = valid(q)
        if not ok:
            excl[why] += 1; continue
        if q.get("hasImage"):
            img = find_image(q)
            if not img and not has_code(q):
                excl["image-missing"] += 1; continue
            if img: q["image"] = img
            q["hasImage"] = False
        kept.append(q)

    # cross-exam duplicate count (kept, not merged — see policy A)
    seen = set(); dup = 0
    for q in kept:
        k = dedup_key(q)
        if k in seen: dup += 1
        else: seen.add(k)

    # finalize: labels, dedupKey, build-time shuffle, strip work fields
    for q in kept:
        q["topicLabel"] = TOPIC_LABEL.get(q["topic"], q["topic"])
        q["dedupKey"] = dedup_key(q)
        # trust tier: official (from a real answer key / confirmed form-0) >
        # verified (no key, but independently re-derived and confirmed) > derived (uncertain)
        q["verified"] = bool(q.get("verified")) and not q["official"]
        q["options"], q["correctIndex"] = shuffle_options(q)
        for k in ("num","chapter","confidence","flag"):
            q.pop(k, None)
    kept.sort(key=lambda q: (q["topic"], q["source"], q["id"]))

    payload = json.dumps(kept, ensure_ascii=False, indent=1)
    (OUT/"questions.json").write_text(payload, encoding="utf-8")
    (OUT/"questions.js").write_text("window.QUESTIONS = " + payload + ";\n", encoding="utf-8")

    # ---- report ----
    by_topic = collections.Counter(q["topic"] for q in kept)
    def tier(q): return "official" if q["official"] else ("verified" if q["verified"] else "derived")
    by_official = collections.Counter(tier(q) for q in kept)
    by_exam = collections.Counter(q["examCode"] for q in kept if q["examCode"])
    lines = ["# Build report — SE questions dataset","",
        f"- Raw items read: **{len(raw_items)}**",
        f"- Excluded: **{sum(excl.values())}**  ({dict(excl)})",
        f"- Cross-exam duplicates (kept whole; app dedups practice pool): **{dup}**",
        f"- **Final questions: {len(kept)}**",
        f"- Trust tiers: **{by_official['official']}** official (from key/form-0) · "
        f"**{by_official['verified']}** verified (independently re-derived) · "
        f"**{by_official['derived']}** derived (still uncertain)","",
        "## By topic",""]
    for t,n in by_topic.most_common():
        lines.append(f"- {TOPIC_LABEL.get(t,t)} (`{t}`): {n}")
    lines += ["","## By exam",""]
    for c in EXAM_CODES:
        if by_exam.get(c):
            lines.append(f"- {c} — {EXAM_LABEL[c]}: {by_exam[c]}")
    (TOOLS/"build_report.md").write_text("\n".join(lines)+"\n", encoding="utf-8")

    print(f"final={len(kept)} excluded={sum(excl.values())} {dict(excl)} dup_kept={dup}")
    print("by_topic:", dict(by_topic.most_common()))
    print("by_tier:", dict(by_official))


if __name__ == "__main__":
    main()
