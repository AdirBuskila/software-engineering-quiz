# Exam structuring instructions (for extraction subagents)

You transcribe ONE Software-Engineering exam from **rendered page images** into a clean
JSON file. Accuracy is everything: **never invent** a question, option, or answer. If you
are unsure, flag it — do not guess.

## Inputs (paths are given to you per exam)
- Exam page images: `tools/raw/pages/<CODE>/p01.png, p02.png, …`  ← PRIMARY source (true layout)
- Solutions page images (if the exam has them): `…/sol_p01.png, …`  ← authoritative answers
- Raw text dump: `tools/raw/<CODE>.fitz.txt`  ← cross-reference ONLY for English terms,
  code, digits (its Hebrew word-order is scrambled — trust the images for Hebrew).

Read every exam page image (and every solutions image if present) before writing.

## Output
Write `tools/raw/<CODE>.json` — a JSON array of question objects, in exam order. Also
return a short summary (counts, and any questions you flagged). Schema per question:

```json
{
  "num": 1,
  "examCode": "<CODE>",
  "year": <YEAR or null>,
  "topic": "<one topic key from the taxonomy>",
  "question": "<full question text in Hebrew, cleaned & correctly ordered>",
  "options": ["<option א>", "<option ב>", "<option ג>", "<option ד>", "<option ה if present>"],
  "correctIndex": <0-based index into options of the CORRECT answer>,
  "official": <true if answer came from a solutions file / explicit key; false if you derived it>,
  "explanation": "<1-2 sentence Hebrew explanation of WHY that option is correct>",
  "hasImage": <true if the question is unanswerable without a diagram/figure/code-block that isn't in the text>,
  "confidence": "high" | "med" | "low",
  "flag": "<omit if fine; else a short note on what to double-check>"
}
```

### Field rules
- **options**: keep the EXACT on-page order (א, ב, ג, ד, ה). Do NOT reorder. Transcribe the
  text only (strip the "א." / "(א)" letter prefix). Preserve English/code tokens verbatim,
  LTR. Common last option: `כל התשובות האחרות שגויות`.
- **correctIndex** — determine by the exam's answer mode (told to you):
  - `form=0` (טופס אפס / טופס 0): the correct answer is the **first option (א)** → `correctIndex: 0`,
    `official: true`. Still write a real explanation; if option א looks clearly wrong on the
    merits, keep 0 but add a `flag`.
  - `has solutions`: find the marked answer on the `sol_*` pages (usually **highlighted**,
    circled, ticked, or written as "תשובה: X"). Set `correctIndex` to that option, `official: true`.
    Use the solution's wording for the explanation when given.
  - `derive` (no form-0, no solutions): choose the correct answer from your SE knowledge.
    `official: false`. Set `confidence` honestly and `flag` anything debatable.
- **hasImage**: set `true` ONLY when the question cannot be answered from text alone because it
  depends on a diagram/figure/screenshot/code block that isn't transcribable. Still fill in
  question + options + your best correctIndex. (These are excluded from the bank until a figure
  is attached — that's expected.) If a short code snippet is essential and transcribable, put it
  inline in the question text inside ``` fences instead of setting hasImage.
- **num**: the question's number on the exam. If an exam says "answer 20 of 26", include all
  that are printed.
- Skip pure instruction/cover pages and open-ended (non-multiple-choice) questions — this bank
  is multiple-choice only. If a "question" has no options, omit it.

## Topic taxonomy (pick the single best `topic` key)
| key | scope |
|---|---|
| `intro` | SE definition, professional vs. amateur dev, generic vs. custom product, process/lifecycle models (waterfall/iterative/incremental), SW dev stages |
| `agile` | Agile, SCRUM (roles, events, artifacts, backlog, sprint), XP, story points |
| `requirements` | requirements engineering, functional/non-functional, use-cases, user stories, Cucumber/BDD, requirement docs |
| `uml` | UML diagrams: class, sequence, state-chart/state machine, use-case, activity, object |
| `architecture` | architectural design, architectural patterns/styles, components, views |
| `patterns` | design patterns (singleton, factory, abstract factory, builder, observer, strategy, adapter, decorator, facade, flyweight, iterator, memento, command, proxy, composite, template) and MVC |
| `solid` | design principles, SOLID (SRP/OCP/LSP/ISP/DIP), Liskov substitution, coupling/cohesion |
| `testing` | testing types, TDD, unit testing, JUnit, mock objects, coverage, assertions |
| `oop_java` | OOP concepts, Java specifics, interfaces/abstract classes, inheritance/polymorphism, collections, generics, reflection, exceptions |
| `metrics` | software metrics, measurements, views (Metrics & Views) |
| `config` | software delivery, CI/CD, configuration/version management, build/release |

If a question truly spans two, pick the most central. Never invent a key outside this list.

## Quality bar
- Transcribe Hebrew from the IMAGE, not the scrambled text dump. Read carefully — RTL.
- Every `question` and every `option` must be non-empty and faithful to the page.
- Prefer `confidence:"low"` + a `flag` over a confident guess. Honesty beats coverage.
