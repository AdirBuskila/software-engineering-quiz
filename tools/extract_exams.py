# -*- coding: utf-8 -*-
"""Extract raw material from the Software-Engineering exams for structuring.

For every distinct text-extractable exam (see docs/exam_inventory.md):
  * resolve the exam file (and its solutions file, if any) by substring match
    inside its folder  -- avoids hard-coding finicky Hebrew filenames;
  * DOCX -> PDF via LibreOffice headless (so DOCX renders like a PDF);
  * dump PyMuPDF text            -> raw/<CODE>.fitz.txt  (+ .sol.fitz.txt)
  * render each page to PNG@170  -> raw/pages/<CODE>/pNN.png (+ sol_pNN.png)

RTL text extracts scrambled, so the PNGs (true visual layout) are the primary
source for the structuring pass; the text dump is a cross-reference anchor for
English tokens, digits and code.
"""
import os, sys, subprocess, pathlib, io
import fitz  # PyMuPDF

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

EXAM_ROOT = pathlib.Path(r"C:\Users\Adir\Desktop\BSC\שנה ב\סמסטר ג\הנדסת תוכנה\מבחנים")
HERE = pathlib.Path(__file__).parent
RAW = HERE / "raw"
PAGES = RAW / "pages"
PDF_CACHE = RAW / "_pdf"
SOFFICE = r"C:\Program Files\LibreOffice\program\soffice.exe"
DPI = 170

# code, folder, exam include/exclude keys, sol include keys, form ("0","A","?")
EXAMS = [
    ("19B-B", "2019", ["5.8.19_"], [],            ["5.8.19 פתרונות"], "?"),
    ("19B-C", "2019", ["11.9.19"], ["פתרונות"],   ["11.9.19 פתרונות"], "?"),
    ("20-A",  "2020", ["מועד א"],  ["פתרון"],     ["מועד א - פתרון"], "?"),
    ("20-B",  "2020", ["מועד ב"],  ["פתרון"],     [], "?"),
    ("21S-A", "2021", ["סמסטר קיץ מועד א"], ["פתרונות"], [], "?"),
    ("21S-B", "2021", ["סמסטר קיץ מועד ב"], ["פתרונות"], ["סמסטר קיץ מועד ב 2021 פתרונות"], "?"),
    ("22B-A", "2022", ["מועד א 14.6.22"], ["פתרונות"], ["פתרונות 14.6.22"], "?"),
    ("22S-A", "2022", ["סמסטר קיץ מועד א 15.9.22"], [], [], "?"),
    ("23-EX", "2023", ["מבחן לדוגמה"], [], [], "?"),
    ("23S-A", "2023", ["21.9.23"], [], [], "?"),
    ("24B-A", "2024", ["18.7.24"], [], [], "0"),
    ("24B-B", "2024", ["11.8.24"], [], [], "0"),
    ("24S-A", "2024", ["15.10.24"], [], [], "0"),
    ("25F0a", "2025", ["14.8.2025"], [], [], "0"),
    ("25F0b", "2025", ["form0"], [], [], "0"),
    ("25S-A", "2025", ["טופס א", "קיץ 2025"], [], [], "A"),
    ("25B-N", "2025", ["17.7.25"], [], [], "?"),
    ("25-EX", "2025", ["מבחן לדוגמה אקסמן 2025"], [], [], "?"),
    ("SP-SPC", "מבחן לדוגמא או ללא תאריך", ["מבחן - מועד מיוחד"], ["פתרון"], ["מועד מיוחד עם פתרון"], "?"),
    ("SP-DGM", "מבחן לדוגמא או ללא תאריך", ["מבחן דוגמא"], ["פתרון"], ["מבחן דוגמא פתרון"], "?"),
    ("SP-AMR", "מבחן לדוגמא או ללא תאריך", ["מועד א אמריקאי"], ["פתרון"], ["מועד א אמריקאי פתרון"], "?"),
    ("SP-MDA", "מבחן לדוגמא או ללא תאריך", ["מבחן - מועד א_"], [], [], "?"),
]


def find_file(folder, includes, excludes=()):
    d = EXAM_ROOT / folder
    if not d.is_dir():
        return None
    cands = []
    for f in d.iterdir():
        if not f.is_file():
            continue
        name = f.name
        if all(k in name for k in includes) and not any(k in name for k in excludes):
            cands.append(f)
    if not cands:
        return None
    # prefer the shortest name (most specific exact match)
    return sorted(cands, key=lambda p: len(p.name))[0]


def to_pdf(src: pathlib.Path) -> pathlib.Path:
    if src.suffix.lower() == ".pdf":
        return src
    PDF_CACHE.mkdir(parents=True, exist_ok=True)
    out = PDF_CACHE / (src.stem + ".pdf")
    if out.exists():
        return out
    subprocess.run([SOFFICE, "--headless", "--convert-to", "pdf", "--outdir",
                    str(PDF_CACHE), str(src)], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
    return out if out.exists() else None


def dump_and_render(pdf: pathlib.Path, code: str, tag: str):
    """tag = '' for exam, 'sol' for solutions."""
    doc = fitz.open(str(pdf))
    txt = []
    outdir = PAGES / code
    outdir.mkdir(parents=True, exist_ok=True)
    prefix = "sol_p" if tag == "sol" else "p"
    for i, page in enumerate(doc, 1):
        txt.append(f"\n----PAGE {i}----\n")
        txt.append(page.get_text("text"))
        pix = page.get_pixmap(dpi=DPI)
        pix.save(str(outdir / f"{prefix}{i:02d}.png"))
    doc.close()
    suffix = ".sol.fitz.txt" if tag == "sol" else ".fitz.txt"
    (RAW / f"{code}{suffix}").write_text("".join(txt), encoding="utf-8")
    return len(txt) // 2  # page count


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    print(f"{'CODE':7} {'form':4} pages  exam-file  /  sol-file")
    print("-" * 90)
    manifest = []
    for code, folder, inc, exc, sol_inc, form in EXAMS:
        exam = find_file(folder, inc, exc)
        sol = find_file(folder, sol_inc) if sol_inc else None
        row = {"code": code, "form": form, "exam": None, "sol": None,
               "pages": 0, "sol_pages": 0}
        if not exam:
            print(f"{code:7} {form:4}  !! EXAM NOT FOUND  folder={folder} inc={inc}")
            manifest.append(row); continue
        row["exam"] = exam.name
        try:
            epdf = to_pdf(exam)
            row["pages"] = dump_and_render(epdf, code, "")
        except Exception as e:
            print(f"{code:7} ERROR exam: {e}")
        if sol:
            row["sol"] = sol.name
            try:
                spdf = to_pdf(sol)
                row["sol_pages"] = dump_and_render(spdf, code, "sol")
            except Exception as e:
                print(f"{code:7} ERROR sol: {e}")
        print(f"{code:7} {form:4} {row['pages']:>3}p   {exam.name}"
              + (f"   +SOL({row['sol_pages']}p) {sol.name}" if sol else "   (no sol)"))
        manifest.append(row)
    # write manifest for the structuring step
    import json
    (RAW / "_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    ok = sum(1 for m in manifest if m["exam"])
    print("-" * 90)
    print(f"resolved {ok}/{len(EXAMS)} exams · "
          f"{sum(m['pages'] for m in manifest)} exam pages · "
          f"{sum(m['sol_pages'] for m in manifest)} sol pages rendered")


if __name__ == "__main__":
    main()
