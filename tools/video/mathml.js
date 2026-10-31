// TeX -> MathML batch renderer (build-time only; the site ships no math JS).
//
// Reads  {"items":[{"tex":"...","display":bool}, ...]}  on stdin,
// writes {"html":["<math…>", …], "errors":[{i,tex,err}, …]}  on stdout.
//
// KaTeX's `output:"mathml"` emits native <math>, so the published page needs no
// katex.css, no web fonts and no runtime script — it stays a static file:// drop.
// The <span class="katex"> wrapper KaTeX adds is for its HTML output; we strip it
// so nothing depends on a stylesheet we don't ship.
const katex = require("katex");

let raw = "";
process.stdin.setEncoding("utf8");
process.stdin.on("data", d => (raw += d));
process.stdin.on("end", () => {
  const { items } = JSON.parse(raw);
  const html = [];
  const errors = [];
  items.forEach((it, i) => {
    try {
      let s = katex.renderToString(it.tex, {
        output: "mathml",
        displayMode: !!it.display,
        throwOnError: true,
        strict: false,
      });
      // unwrap <span class="katex">…</span> -> bare <math>
      const m = s.match(/<math[\s\S]*<\/math>/);
      if (!m) throw new Error("no <math> in KaTeX output");
      s = m[0];
      // The page is dir="rtl"; math must render LTR or the glyph order scrambles.
      s = s.replace(/^<math /, '<math dir="ltr" ');
      // Chrome ignores mathvariant="double-struck" (\mathbb{Z} showed as a plain Z): use the Unicode letters
      const DS = { N: "ℕ", Z: "ℤ", Q: "ℚ", R: "ℝ", C: "ℂ", P: "ℙ", H: "ℍ" };
      s = s.replace(/<mi mathvariant="double-struck">([A-Z])<\/mi>/g, (m, c) =>
        `<mi mathvariant="normal">${DS[c] || String.fromCodePoint(0x1D538 + c.charCodeAt(0) - 65)}</mi>`);
      // (\overline is drawn by video.css: the stretchy ‾ is hidden and a rule goes over the base)
      html.push(s);
    } catch (e) {
      errors.push({ i, tex: it.tex, err: String(e.message || e).slice(0, 200) });
      html.push(null);
    }
  });
  process.stdout.write(JSON.stringify({ html, errors }));
});
