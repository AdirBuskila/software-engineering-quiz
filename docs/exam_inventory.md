# SE exam inventory & extractability

Every file under `…\הנדסת תוכנה\מבחנים\`, its format, whether a solutions (פתרונות)
file exists, and an automatic-extraction confidence rating. Produced by probing each
file (PyMuPDF + pdfplumber for PDFs, python-docx for DOCX): pages, extracted-char count,
embedded-image count, Hebrew-char count, option-letter markers.

**Confidence:** `HIGH` = clean text, extract programmatically · `NEEDS-OCR` = image-only
/ scanned, manual · `DUP` = duplicate of another file.

Legend for **Form**: `0` = טופס אפס/0 (answer = first option) · `A` = טופס א (not 0) ·
`?` = unlabeled (needs solution cross-check or your input).

---

## Distinct exams to extract (HIGH confidence, text-based)

| # | Proposed code | Exam | Exam file | Solutions file | Fmt | Form | Notes |
|---|---|---|---|---|---|---|---|
| 1 | `19B-B` | 2019 סמ׳ ב מועד ב (5.8.19) | `2019\…5.8.19_.docx` | `2019\…5.8.19 פתרונות.docx` ✓ | docx | ? | exam+sol pair, same body |
| 2 | `19B-C` | 2019 סמ׳ ב מועד ג (11.9.19) | `2019\…11.9.19.pdf` | `2019\…11.9.19 פתרונות.pdf` ✓ | pdf | ? | 7–8 pp |
| 3 | `20-A` | 2020 מועד א | `2020\מבחן - מועד א.pdf` | `2020\מבחן - מועד א - פתרון חלקי.pdf` ⚠️partial | pdf | ? | partial solution only |
| 4 | `20-B` | 2020 מועד ב | `2020\מבחן - מועד ב.pdf` | — | pdf | ? | no solution |
| 5 | `21S-A` | 2021 סמ׳ קיץ מועד א | `2021\סמסטר קיץ מועד א 2021.pdf` | — | pdf | ? | no solution |
| 6 | `21S-B` | 2021 סמ׳ קיץ מועד ב | `2021\סמסטר קיץ מועד ב 2021.pdf` | `2021\…מועד ב 2021 פתרונות.docx` ✓ | pdf | ? | exam+sol |
| 7 | `22B-A` | 2022 סמ׳ ב מועד א (14.6.22) | `2022\…14.6.22.docx` | `2022\…פתרונות 14.6.22.pdf` ✓ | docx | ? | exam+sol |
| 8 | `22S-A` | 2022 סמ׳ קיץ מועד א (15.9.22) | `2022\…15.9.22.pdf` | — | pdf | ? | no solution |
| 9 | `23-EX` | 2023 מבחן לדוגמה (אקסמן) | `2023\מבחן לדוגמה סמסטר ב 2023 אקסמן.pdf` | — | pdf | ? | 3 pp, dense, 94 opt-marks |
| 10 | `23S-A` | 2023 סמ׳ קיץ מועד א (21.9.23) | `2023\…21.9.23.pdf` | — | pdf | ? | no solution |
| 11 | `24B-A` | 2024 סמ׳ ב מועד א (18.7.24) | `2024\…18.7.24 טופס 0.pdf` | — | pdf | **0** | 26 Q, first 20 graded |
| 12 | `24B-B` | 2024 סמ׳ ב מועד ב (11.8.24) | `2024\…11.8.24 טופס 0.pdf` | — | pdf | **0** | |
| 13 | `24S-A` | 2024 סמ׳ קיץ מועד א (15.10.24) | `2024\…15.10.24 טופס 0.pdf` | — | pdf | **0** | |
| 14 | `25F0a` | 2025 (14.8.25) טופס אפס | `2025\14.8.2025 טופס אפס.pdf` | — | pdf | **0** | |
| 15 | `25F0b` | 2025 form0 (9.11.25) | `2025\9219_form0_63301_09112025_0.pdf` | — | pdf | **0** | filename = form0 |
| 16 | `25S-A` | 2025 קיץ מועד א | `2025\טופס א מועד א קיץ 2025.pdf` | — | pdf | **A** | ⚠️ form **A**, not 0 |
| 17 | `25B-N` | 2025 סמ׳ ב מועד א (17.7.25, ניסים) | `2025\סמסטר ב מועד א 17.7.25 ניסים ברמי.pdf` | — | pdf | ? | **= `מבחן 2025 ניסים.pdf`** (DUP) |
| 18 | `25-EX` | 2025 מבחן לדוגמה (אקסמן) | `2025\מבחן לדוגמה אקסמן 2025.pdf` | — | pdf | ? | |
| 19 | `SP-SPC` | מבחן מועד מיוחד | `…או ללא תאריך\מבחן - מועד מיוחד.pdf` | `…\מועד מיוחד עם פתרון.pdf` ✓ | pdf | ? | exam+sol |
| 20 | `SP-DGM` | מבחן דוגמא | `…או ללא תאריך\מבחן דוגמא.pdf` | `…\מבחן דוגמא פתרון.pdf` ✓ | pdf | ? | exam+sol |
| 21 | `SP-AMR` | מועד א אמריקאי | `…או ללא תאריך\מועד א אמריקאי.docx` | `…\מועד א אמריקאי פתרון.docx` ✓ | docx | ? | exam+sol |
| 22 | `SP-MDA` | מבחן - מועד א (אמריקאי?) | `…או ללא תאריך\מבחן - מועד א_.docx` | — | docx | ? | 6 tables, 9 imgs — has diagrams |

## ⚠️ SCANNED — needs OCR or your input (ask-Adir list)

| Exam | Files | Why |
|---|---|---|
| 2021 מבחן מועד א | `2021\מבחן 2021 מועד א\Page1–8.jpg` + `מבחן מלא.pdf` | 8 image pages; PDF is image-only (0 text) |
| 2021 מבחן מועד ב | `2021\מבחן 2021 מועד ב\Page1–9.jpg` + `מבחן מלא.pdf` | 9 image pages; PDF is image-only (0 text) |
| 2023 סמ׳ ב מועד א | `2023\סמסטר ב מועד א 22.6.23.pdf` | 391 embedded images, ~0 extractable text (scanned) |

## Duplicates (skip — same content as a row above)

- `…או ללא תאריך\מבחן 1 ללא פתרון.pdf` = **20-A** · `…\מועד א ללא פתרון.pdf` = **20-A**
- `…או ללא תאריך\מבחן - מועד א - פתרון חלקי.pdf` = **20-A** partial solution
- `…או ללא תאריך\מבחן א ללא פתרון.pdf` = **20-B**
- `…או ללא תאריך\מועד ב פתרונות.docx` = **21S-B** solutions
- `2025\מבחן 2025 ניסים.pdf` = **25B-N** (identical metrics: 8 pp / 10 367 ch)

---

### Totals
- **~22 distinct extractable exams** (HIGH), several with an official solutions file for
  form-0 cross-checking.
- **3 scanned exams** → ask-Adir list.
- Estimated **~20–26 questions/exam** → rough order of **400–500 raw questions** before
  dedup; final bank likely **~150–250** distinct after dedup (many recur across years).
  Exact counts reported by `build_report.md` after the build.

> Filenames shown are the real UTF-8 names (the probe console mojibaked Hebrew, but files
> are matched by folder + page/char/image metrics). Extraction confidence is about *text
> retrievability*, not answer correctness — correctness follows the Phase-3 form-0 rule
> and solution cross-checks.
