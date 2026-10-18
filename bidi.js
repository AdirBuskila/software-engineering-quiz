/* Bidi isolates for RTL pages (ported from the ML quiz course-ui.js). window.bidiHtml(escapedHtml) wraps formula-like
   non-Hebrew runs in LTR <bdi>; window.bidiText(plain) escapes first. A run ends at a clause boundary outside brackets. */
(function(){
  "use strict";
  const INLINE = /^<\/?(b|strong|i|em|u|sub|sup|code)\b[^>]*>$/i;
  const SKIP = /^<(code|bdi|pre)\b|class="[^"]*\b(lesson-formula|qref)\b|\bdir="ltr"/i;
  const START = /[A-Za-z0-9(\[|√‖Σ∑−ŷȳα-ωΔΣθ]/, END = /[A-Za-z0-9)\]|²³‖%∞'"₀-₉ᵢⱼₙₖŷȳ\u0304α-ω]/;
  const isTag = p => p[0] === "<", chr = p => (isTag(p) || p[0] === "&" && p.length > 1) ? "" : p;
  function isolate(html){
    const toks = String(html).match(/<[^>]+>|[^<]+/g) || [];
    let out = "", run = [], skip = 0, depth = 0, cut = false;
    const flush = () => {
      depth = 0; cut = false;
      if (!run.length) return;
      const s = run.join("");
      // trim to the first/last "real" character, keeping whole tags; then require balanced tags
      const parts = s.match(/<[^>]+>|&[#\w]+;|[^<]/g);   // a tag or an entity (&gt;) is one unit
      let a = 0, b = parts.length - 1;
      while (a <= b && !START.test(chr(parts[a]))) a++;
      while (b >= a && !END.test(chr(parts[b]))) b--;
      // pull in tags hugging the core: <b>3</b> → keep both
      while (a > 0 && isTag(parts[a - 1]) && !/^<\//.test(parts[a - 1])) a--;
      while (b < parts.length - 1 && /^<\//.test(parts[b + 1])) b++;
      const balanced = arr => { const st = [];
        for (const t of arr) { if (!isTag(t)) continue;
          const m = t.match(/^<(\/?)(\w+)/); if (m[1]) { if (st.pop() !== m[2].toLowerCase()) return false; } else st.push(m[2].toLowerCase()); }
        return !st.length; };
      // a tag whose partner lies outside the run ("<b>צ׳בישב (L∞)</b>") stays outside the isolate
      while (b > a && /^<\//.test(parts[b]) && !balanced(parts.slice(a, b + 1))) b--;
      while (a < b && isTag(parts[a]) && !/^<\//.test(parts[a]) && !balanced(parts.slice(a, b + 1))) a++;
      const core = parts.slice(a, b + 1), text = core.join("").replace(/<[^>]+>/g, "");
      const ok = a <= b && /[A-Za-z0-9]/.test(text) && !/^(NaN|null|undefined)$/i.test(text) && balanced(core);   // keep literals like "null" as plain text
      // a short formula never splits across lines; a plain multi-word phrase may wrap
      const nw = text.length <= 22 && (!/\s/.test(text) || /[0-9=+−×·*\/^²³√∞≈≤≥<>|‖%()]/.test(text));
      out += ok ? parts.slice(0, a).join("") + `<bdi class="ltr${nw ? " nw" : ""}" dir="ltr">${core.join("")}</bdi>` + parts.slice(b + 1).join("") : s;
      run = [];
    };
    for (const t of toks) {
      if (t[0] === "<") {
        if (skip) { out += t; if (/^<\//.test(t)) skip--; else if (!/\/>$|^<(br|img|hr|wbr)\b/i.test(t)) skip++; continue; }
        if (SKIP.test(t)) { flush(); out += t; if (!/^<(br|img)\b/i.test(t)) skip = 1; continue; }
        if (INLINE.test(t)) { if (!/^<\//.test(t)) cut = false; run.push(t); continue; }
        flush(); out += t; continue;
      }
      if (skip) { out += t; continue; }
      // split text at Hebrew letters (and RLM): Hebrew text ends a run
      for (const piece of t.match(/[֐-׿‏]+|[^֐-׿‏]+/g)) {
        if (/[֐-׿‏]/.test(piece)) { flush(); out += piece; continue; }
        // "**10.** 12": the punctuation closed a bold run, the whitespace comes after the tag
        if (cut && /^\s/.test(piece)) flush();
        cut = false;
        let seg = "";
        for (let i = 0; i < piece.length; i++) {
          const c = piece[i];
          seg += c;
          if ("([{".includes(c)) depth++;
          else if (")]}".includes(c)) depth = Math.max(0, depth - 1);
          else if (depth === 0 && /[.,;:!?]/.test(c) && !(c === ";" && /&[#\w]+;$/.test(seg))) {
            if (i === piece.length - 1) cut = true;
            else if (/\s/.test(piece[i + 1])) { run.push(seg); seg = ""; flush(); }
          }
        }
        if (seg) run.push(seg);
      }
    }
    flush();
    return out;
  }
  window.bidiHtml = isolate;
  // plain text -> escaped, `code` (LTR) and **bold**, then isolates
  window.bidiText = s => isolate(String(s == null ? "" : s).replace(/[&<>]/g, m => ({"&":"&amp;","<":"&lt;",">":"&gt;"}[m]))
    .replace(/`([^`]+)`/g, (m, c) => `<code dir="ltr">${c}</code>`)
    .replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>"));
})();
