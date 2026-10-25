"use strict";
/* Feedback links (shared by every study app; identical file in each repo).
   - footer line  : <div id="feedbackLine"> in the start-screen footer is filled on load
   - report link  : Feedback.report({id, exam, html|text}) -> '<a class="reportlink">' markup for a question view
   The mail address is never written out in HTML or as one string: it is assembled here at runtime, and a link
   only gets its mailto href when it is rendered. Styles are injected below so that the page CSS stays untouched. */
(function(){
  const addr = () => ["adirbu98", "gmail.com"].join("@");
  const title = () => (document.title || "").trim();
  const enc = encodeURIComponent;
  const attr = s => String(s).replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;");
  function mailto(subject, body){
    return "mailto:" + addr() + "?subject=" + enc(subject) + (body ? "&body=" + enc(body) : "");
  }
  function plain(h){
    const d = document.createElement("div");
    d.innerHTML = String(h == null ? "" : h).replace(/<br\s*\/?>|<\/(?:p|div|pre|li|tr|td|th|h\d)>/gi, " $&");
    return (d.textContent || "").replace(/\s+/g, " ").trim();
  }
  /* q.html (markup, tags stripped) or q.text (already plain) */
  function snippet(q){
    const t = (q.html != null ? plain(q.html) : String(q.text == null ? "" : q.text).replace(/\s+/g, " ").trim());
    return t.length > 80 ? t.slice(0, 80) + "…" : t;
  }
  const footerSubject = () => title() + " — משוב";
  const footerText = "מצאתם טעות? יצא מבחן חדש שלא מופיע כאן? 📩 כתבו לי ואוסיף";
  const coffeeUrl = "https://buymeacoffee.com/adirbuskila";
  const coffeeText = "☕ עזר לכם? אפשר לקנות לי קפה";
  /* q = {id, exam, html?, text?, title?} */
  function reportParts(q){
    const t = q.title || title();
    return {
      subject: t + " — טעות בשאלה " + q.id,
      body: "שאלה: " + q.id + "\nמבחן: " + (q.exam || "") + "\nתחילת השאלה: " + snippet(q) + "\n\nמה הטעות / מה לתקן:\n"
    };
  }
  function reportHref(q){ const p = reportParts(q); return mailto(p.subject, p.body); }
  function report(q){
    return '<a class="reportlink" href="' + attr(reportHref(q)) + '" rel="noopener">⚑ דווחו על טעות</a>';
  }
  function mountFooter(){
    const box = document.getElementById("feedbackLine");
    if(!box) return;
    box.textContent = "";
    const a = document.createElement("a");
    a.className = "feedback-link";
    a.href = mailto(footerSubject());
    a.textContent = footerText;
    box.appendChild(a);
    mountCoffee(box.parentElement);
  }
  /* the coffee button gets its own row at the top of the footer (created once) */
  function mountCoffee(foot){
    if(!foot || foot.querySelector(".coffee-row")) return;
    const row = document.createElement("div");
    row.className = "coffee-row";
    const c = document.createElement("a");
    c.className = "coffee-link";
    c.href = coffeeUrl;
    c.target = "_blank";
    c.rel = "noopener";
    c.textContent = coffeeText;
    row.appendChild(c);
    foot.prepend(row);
  }
  function injectStyle(){
    if(document.getElementById("feedbackStyle")) return;
    const st = document.createElement("style");
    st.id = "feedbackStyle";
    st.textContent =
      ".feedback-line{flex-basis:100%;font-size:.78rem;line-height:1.5;margin:.15rem 0 0}" +
      ".feedback-link,.reportlink{color:var(--muted,#8a8f98);text-decoration:none;opacity:.9;overflow-wrap:anywhere}" +
      ".feedback-link{border-bottom:1px dotted currentColor}" +
      ".feedback-link:hover,.feedback-link:focus-visible,.reportlink:hover,.reportlink:focus-visible{color:var(--ink,inherit);opacity:1}" +
      ".feedback-link:focus-visible,.reportlink:focus-visible{outline:2px solid var(--brand,currentColor);outline-offset:2px;border-radius:3px}" +
      ".reportrow{margin:.6rem 0 .2rem;font-size:.74rem;text-align:start;direction:rtl}" +
      ".reportlink{display:inline-block;padding:.2rem 0;font-size:.74rem}" +
      ".reportlink:hover,.reportlink:focus-visible{text-decoration:underline}" +
      ".coffee-row{flex-basis:100%;margin:0 0 .6rem}" +
      ".coffee-link{display:inline-block;padding:.5rem 1.2rem;font-size:.98rem;font-weight:600;line-height:1.3;border:1px solid rgba(251,191,36,.55);border-radius:999px;background:rgba(251,191,36,.1);color:#d97706;text-decoration:none;white-space:nowrap;transition:background .15s,transform .15s}" +
      "@media (prefers-color-scheme:dark){.coffee-link{color:#fbbf24}}" +
      "[data-theme=dark] .coffee-link{color:#fbbf24}[data-theme=light] .coffee-link{color:#b45309}" +
      ".coffee-link:hover,.coffee-link:focus-visible{background:rgba(251,191,36,.2);transform:translateY(-1px)}" +
      ".coffee-link:focus-visible{outline:2px solid #fbbf24;outline-offset:2px}";
    document.head.appendChild(st);
  }
  /* a ready row for a question view */
  function reportRow(q){ return '<div class="reportrow">' + report(q) + "</div>"; }
  /* the report row that follows a fixed element of the question view (created once, refilled per question) */
  function slot(after, key, q){
    if(!after) return null;
    let el = after.nextElementSibling;
    if(!(el && el.classList.contains("reportrow") && el.dataset.slot === key)){
      el = document.createElement("div"); el.className = "reportrow"; el.dataset.slot = key; after.after(el);
    }
    el.innerHTML = report(q);
    return el;
  }
  window.Feedback = { mailto, report, reportRow, slot, reportHref, reportParts, footerSubject, footerText, coffeeUrl, mountFooter, plain };
  injectStyle();
  mountFooter();   // the script sits at the end of <body>, so the footer already exists
  if(document.readyState === "loading") document.addEventListener("DOMContentLoaded", mountFooter);
})();
