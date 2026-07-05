# Answer-verification instructions (for verifier subagents)

You independently re-check the **derived** (unofficial) answers of ONE exam and fix any
that are actually WRONG. The first pass reasoned these out with no answer key, so some
may be incorrect. Your job is correctness, not speed.

## Inputs (given per exam)
- Exam page images (authoritative question text): `tools/raw/pages/<CODE>/p01.png … pNN.png`
- Current data: `tools/raw/<CODE>.json`

## Method — for EACH question with `"official": false`
1. **Decide fresh.** From the exam page image + your SE knowledge (Sommerville textbook,
   GoF design patterns, SCRUM/Agile/XP, UML, testing/TDD/JUnit/Mock, Java/OOP/Reflection,
   architecture, version control), determine the correct option **independently**. Do NOT
   just re-read the stored explanation — form your own answer first, then compare to the
   stored `correctIndex`.
2. **If you are HIGHLY confident the stored answer is wrong**, fix it in the JSON: update
   `correctIndex` (0-based into the existing `options`, do NOT reorder options) AND rewrite
   `explanation` to justify the new answer. Set `confidence` to `high` and add a `flag`
   noting the correction (`תוקן: <ישן>→<חדש> — <סיבה>`).
3. **If it is a genuine judgment call** (two defensible options, ambiguous wording), LEAVE
   the stored answer unchanged; you may refine the `flag`/`confidence` but do not flip it.
4. **`hasImage` questions**: use the diagram visible in the page image to decide.
5. **Never touch `"official": true` questions** — those come from solution keys / form-0 and
   are authoritative. If one looks wrong, only mention it in your summary; do NOT edit it.

## Output
Edit `tools/raw/<CODE>.json` in place — valid UTF-8, same array structure and field names
(`num, examCode, year, topic, question, options, correctIndex, official, explanation,
hasImage, confidence, flag`). Then return a concise summary:
- `checked: <n derived>`, `agreed: <n>`, `changed: <n>`
- one line per CHANGE: `Q<num>: <oldLetter>→<newLetter> — <short reason>`
- any questions still genuinely ambiguous (kept as-is), one line each.

Letters map 0→א, 1→ב, 2→ג, 3→ד, 4→ה. Be conservative and honest — a confident wrong
"fix" is worse than leaving a defensible answer. Never fabricate.
