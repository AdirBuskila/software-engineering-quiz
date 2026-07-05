# -*- coding: utf-8 -*-
"""Prepare page images for the 3 scanned exams:
   21-A / 21-B  = folders of JPG page scans  -> convert to raw/pages/<code>/pNN.png
   23B-A        = image-only PDF             -> render to raw/pages/23B-A/pNN.png
"""
import pathlib, re, io, sys
import fitz
from PIL import Image
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

EXAM_ROOT = pathlib.Path(r"C:\Users\Adir\Desktop\BSC\שנה ב\סמסטר ג\הנדסת תוכנה\מבחנים")
PAGES = pathlib.Path(__file__).parent / "raw" / "pages"
DPI = 175

def pagenum(name):
    m = re.search(r"(\d+)", name)
    return int(m.group(1)) if m else 0

def from_jpg_folder(code, folder):
    src = EXAM_ROOT / folder
    out = PAGES / code
    out.mkdir(parents=True, exist_ok=True)
    jpgs = sorted([f for f in src.iterdir() if f.suffix.lower() in (".jpg", ".jpeg")],
                  key=lambda f: pagenum(f.name))
    for i, f in enumerate(jpgs, 1):
        Image.open(f).convert("RGB").save(out / f"p{i:02d}.png")
    print(f"{code}: copied {len(jpgs)} JPG pages -> {out}")
    return len(jpgs)

def from_pdf(code, rel):
    pdf = EXAM_ROOT / rel
    out = PAGES / code
    out.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(str(pdf))
    for i, page in enumerate(doc, 1):
        page.get_pixmap(dpi=DPI).save(str(out / f"p{i:02d}.png"))
    n = doc.page_count
    doc.close()
    print(f"{code}: rendered {n} PDF pages -> {out}")
    return n

from_jpg_folder("21-A", r"2021\מבחן 2021 מועד א")
from_jpg_folder("21-B", r"2021\מבחן 2021 מועד ב")
from_pdf("23B-A", r"2023\סמסטר ב מועד א 22.6.23.pdf")
