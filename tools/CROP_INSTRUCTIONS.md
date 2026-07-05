# Figure-cropping instructions (for crop subagents)

Some questions depend on a diagram (Git branch timeline, UML sequence/class diagram) that
couldn't be transcribed as text. Your job: **crop that diagram** out of the exam page image
and save it, so the question becomes answerable and enters the bank.

## For each (CODE, Qnum) you're given
1. Open the exam page images in `tools/raw/pages/<CODE>/` (`p01.png`, `p02.png`, …) and
   **view them** to find question number `Qnum`. The relevant figure sits right next to that
   question — usually **between the question text and its answer options** (א/ב/ג/ד/ה), or
   directly under the question.
2. Note the page image's pixel dimensions (shown when you view it). Estimate a bounding box
   `(left, top, right, bottom)` in **original-image pixels** that **tightly contains the whole
   diagram** — include the full diagram + a small margin, but exclude the question text above
   and the answer options below. Diagrams usually span most of the page width, so `left` small
   and `right` near the page width is common; the vertical band is the key.
3. Crop and save with PIL:
   ```python
   from PIL import Image
   Image.open(SRC).crop((left, top, right, bottom)).save(DST)
   ```
   - `SRC` = the page PNG that holds the figure.
   - `DST` = `tools/../images/exams/<CODE>-Q<Qnum>.png`  (i.e. the repo's `images/exams/` dir;
     create it if missing). Filename must be EXACTLY `<CODE>-Q<Qnum>.png`.
4. **Verify**: re-open `DST`, view it, and confirm the full diagram is visible and legible and
   that it's NOT the whole page and NOT cut off. If wrong, adjust the box and re-crop.

## Notes
- If a page has a red-circled region (some sequence-diagram questions), include the whole
  diagram **with** the red circle visible.
- If you genuinely cannot locate a figure for a given Qnum (e.g. the question is actually
  text-answerable), skip it and say so — do not save a wrong crop.
- Return a short list: for each Qnum, the source page, the crop box used, and the saved file's
  pixel size.
