# Build plan — Software-Engineering Quiz (הנדסת תוכנה)

Mirror of the working **data-science-quiz** app, rebuilt for the SE course.
Written after reverse-engineering the DS app end-to-end (Phase 0) and probing every
SE exam file (Phase 1).

---

## 1. What the DS app is (reverse-engineered)

A **100 % static** Hebrew-RTL, mobile-first MCQ trainer — no build step, no server, no
CDN. Opens from `file://` or GitHub Pages.

| File | Role |
|---|---|
| `index.html` | 4 screens: start / quiz / learn / results + lightbox. Loads `questions.js`, `learn.js`, `app.js`. Pre-paint theme script. |
| `app.js` | Vanilla-JS engine. Reads `window.QUESTIONS`. Practice + exam modes, topic filter, per-question **Fisher–Yates option shuffle** (`makeView`), timer, scoring, `localStorage` progress, theme toggle, learn-mode controller, deep-link `?practice=<topic>`. |
| `styles.css` | Design system via CSS vars; dark default + `[data-theme=light]` + `prefers-color-scheme`. RTL throughout; LTR isolation for code/latin options. Responsive at 860 / 560 px. |
| `questions.js` / `questions.json` | `window.QUESTIONS = [...]` and the same JSON. The canonical bank. |
| `learn.js` | `window.LEARN = [{id,title,html}]` — chapter reader content, auto-generated. |
| `tools/` | Python + Node pipeline (below). Not needed to run the site. |

### DS question schema (final `questions.json`)
```json
{
  "examCode":"24A-A", "year":2024,
  "topic":"acquisition", "topicLabel":"הרכשת נתונים",
  "question":"…", "options":["…","…","…","…"], "correctIndex":0,
  "official":true, "explanation":"…",
  "source":"exam", "sourceLabel":"2024 סמסטר א׳ מועד א׳",
  "id":"24A-A-Q11", "hasImage":false,
  "image":"images/exams/…png"   // optional
}
```
`correctIndex` points into the original `options[]`; the app shuffles display order at
render so position is never a tell **at runtime**.

### DS pipeline (proven, we reuse it)
```
extract_exams.py   PDF → raw dual-engine text  (tools/raw/<CODE>.{plumber,fitz}.txt)
   (LLM step)      raw text → structured  tools/raw/<CODE>.json     ← done by a model, not regex
validate.py        sanity-check every raw JSON
build_questions.py merge exams+practice → questions.js/.json + build_report.md
build_missing_report.py  → missing-questions.html (which Q needs a figure)
build_learn.py     course summary (md) → learn.js + optimized images/
smoke.js           data integrity + shuffle/scoring invariant (Node)
verify_ui/theme/learn.js  real-browser checks (puppeteer-core)
```

---

## 2. SE differences from DS (what changes)

1. **5 options (א–ה), not 4.** SE questions frequently have 5 options, often with
   `ה. כל התשובות האחרות שגויות`. → `validate.py` allows **2–6** options (not `==4`);
   `HE_KEYS` in app.js already covers א–ח; results/UI already option-count-agnostic.

2. **Form-0 correctness rule (Phase 3).** For **טופס אפס / טופס 0** exams the correct
   answer is the **first option (א)** → `correctIndex:0` in the raw JSON. Confirmed
   structurally in the 2024/2025 form-0 PDFs (options extract in order א,ב,ג,ד,ה).
   - ⚠️ **Not all exams are form-0.** `2025 טופס א` is *form A*, and 2019–2023 exams
     carry no form label. Handling of those is an open decision (see §6).

3. **Anti-"always-first" hardening.** DS stores `correctIndex:0` for every form-0 exam
   and relies **only** on render-time shuffle — so its raw `questions.json` is trivially
   "pick the first". For SE we add a **deterministic build-time option shuffle** in
   `build_questions.py` (seeded, reproducible) so the *stored* `correctIndex` is
   randomized across questions. Combined with render-time shuffle this satisfies the
   Phase-3 hard requirement: even a reader of `questions.json` can't just pick option 1.
   Correct answer is thus effectively stored **by content**, not position.

4. **Extraction is LLM-driven, not regex.** RTL text extracts readable-but-scrambled
   (line fragments reversed, option letters split from their text). A model reconstructs
   each Q + options + correctIndex from the raw dump; **never fabricated** — low-confidence
   items go to the "ask Adir" list, not the bank.

5. **SE topic taxonomy** (seed — confirm in §6):

   | key | label (he) | covers |
   |---|---|---|
   | `intro` | מבוא והנדסת תוכנה | SE processes, lifecycle, waterfall/iterative |
   | `agile` | Agile · SCRUM · XP | scrum roles/events, XP, delivery |
   | `requirements` | דרישות | requirements, use-cases, user stories, Cucumber |
   | `uml` | מידול ו-UML | class / sequence / state-chart / use-case diagrams |
   | `architecture` | עיצוב ארכיטקטוני | architectural design, components |
   | `patterns` | תבניות עיצוב | singleton, factory, observer, strategy, adapter, decorator, facade, flyweight, iterator, command, MVC … |
   | `solid` | עקרונות SOLID ו-Liskov | SOLID, LSP |
   | `testing` | בדיקות · TDD · JUnit | testing, TDD, JUnit, mock objects |
   | `oop_java` | OOP ו-Java | OOP, interfaces, collections, reflection |
   | `metrics` | מטריקות ותצוגות | metrics & views |

6. **Deduplication.** SE files are heavily duplicated (year folders ↔ "מבחן לדוגמא"
   folder) and questions recur across years. DS deliberately *keeps* per-exam duplicates
   so "whole-exam" mode stays complete. Reconciliation is an open decision (see §6).

---

## 3. Extraction confidence (from Phase-1 probe)

- **HIGH (text, ~19 distinct exams after dedup)** — extract programmatically now.
- **SCANNED (needs OCR/manual, 3 exams)** — 2021 מועד א (8 JPG + image-only PDF),
  2021 מועד ב (9 JPG + image-only PDF), 2023 סמסטר ב מועד א 22.6.23 (391 embedded
  images, ~0 text). These go on the **ask-Adir** list — no OCR into the bank without
  your confirmation.

Full per-file table: `docs/exam_inventory.md`.

---

## 4. Execution plan (after your go-ahead)

**Phase 4 — build the bank (parallel subagents, one per HIGH exam):**
1. `extract_exams.py` (SE paths) dumps dual-engine raw text for every HIGH PDF; DOCX read
   via `python-docx`.
2. A structuring subagent per exam turns raw text → `tools/raw/<CODE>.json`
   (num, topic, question, options, correctIndex per form-0 rule, official, explanation,
   hasImage). Confidence recorded per question; uncertain ones flagged, not guessed.
3. Where a **solutions (פתרונות)** file exists, cross-check the form-0 assumption; any
   mismatch is surfaced to you, not silently trusted.
4. `validate.py` (SE-adapted) then `build_questions.py` (with build-time shuffle + dedup
   policy) → `questions.js/.json` + `build_report.md`.

**Phase 5 — learn mode:** build `learn.js` from the richest summaries
(`מצגות + סיכומים/…` — אקסמן & ניסים PDFs), mirroring the DS chapter reader.

**Phase 6 — ship + verify:** port `index.html`, `app.js`, `learn.js`, `styles.css`
(SE topics/branding), then run `validate.py`, `smoke.js`, `verify_*.js`. Report counts
per topic + per exam and the final ask-Adir list.

## 5. Location & naming

App at `C:\Users\Adir\Desktop\Coding\Dev\software-engineering-quiz\` (mirrors the DS
location; tools read source exams from the BSC course folder, exactly like DS does).
Exam codes: `YY` + semester (`B`=ב / `S`=קיץ) + `-` + moed (e.g. `24B-A`, `21S-B`).

## 6. Open decisions (asked separately)

1. **Scanned exams** — you paste Q&A later / I OCR + you verify / skip for now.
2. **Dedup vs whole-exam mode** — keep exams whole + dedup only the practice pool
   (recommended) vs hard-dedup the bank.
3. **Answer confidence for non-form-0, no-solution questions** — derive + mark
   "unofficial" (DS style) vs include only verifiable ones.
4. **App location** — confirm the mirror path above.
