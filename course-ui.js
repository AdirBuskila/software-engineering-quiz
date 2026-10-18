"use strict";
/* Guided courses - "צריך עזרה?": level map -> lesson -> level quiz -> summary.
   Ported from the machine-learning quiz. Levels come from courses/<course>/*.js via courses.js
   (window.COURSES[id].levels). The quiz runs on the main engine in app.js (S, renderQuestion, choose,
   next) with S.mode = "course"; app.js calls back into window.COURSE.record / finishLevel / exit.
   Each course keeps its progress in its own localStorage key, apart from the bank stats.
   All text goes through bidi.js (window.bidiHtml) so formulas and English terms inside the Hebrew
   sentences are isolated and read in the right order.

   level    = {id, order, icon, title, goal, boss?, lesson:{html}, questions:[...]}
   question = {id, question, code?, table?, options:[string], answer:<index>, explanation, recap}
            | {ref:"<bank question id>", recap, explanation?}   <- a real exam question, verbatim
   Text in questions/explanations takes **bold**, `code` and newlines. */
(function(){
  const META = {
    pat:  { name: "תבניות עיצוב", title: "צריך עזרה בתבניות עיצוב?", icon: "🧩", store: "seq_crs_pat_v1",
            topics: ["patterns"],
            intro: "איזו תבנית מתאימה לתיאור המערכת, ומה התפקיד של כל אחד מהרכיבים: Singleton, Factory, Observer, Command, MVC, ועוד שלוש תבניות שנשאלו (Mediator, Chain of Responsibility, Flyweight). כל שלב פותח בשיעור קצר ובדוגמה, וממשיך בשאלות בסגנון המבחן. כל השלבים פתוחים; שלב נחשב עבור מ-80%." },
    uml:  { name: "UML ומידול", title: "צריך עזרה ב-UML ובמידול?", icon: "📐", store: "seq_crs_uml_v1",
            topics: ["uml"],
            intro: "הנושא עם הכי הרבה שאלות במבחן: לאיזה מודל שייך כל תרשים, תרשים מחלקות (קשרים, ריבוי), תרשים רצף (קו חיים, סרגל הפעלה), Use Case, תרשים מצבים ותרשים פעילות. כל שלב פותח בשיעור קצר וממשיך בשאלות בסגנון המבחן. כל השלבים פתוחים; שלב נחשב עבור מ-80%." },
    tst:  { name: "בדיקות תוכנה", title: "צריך עזרה בבדיקות תוכנה?", icon: "🧪", store: "seq_crs_tst_v1",
            topics: ["testing"],
            intro: "רמות בדיקה ומודל V, JUnit (setup, test, tearDown), Mock, תכנון מקרי בדיקה וערכי גבול, TDD וסקירות. כל שלב פותח בשיעור קצר וממשיך בשאלות בסגנון המבחן. כל השלבים פתוחים; שלב נחשב עבור מ-80%." },
    proc: { name: "תהליכים, Agile ודרישות", title: "צריך עזרה בתהליכי פיתוח, Agile ודרישות?", icon: "🧭", store: "seq_crs_proc_v1",
            topics: ["intro", "agile", "requirements"],
            intro: "מבוא להנדסת תוכנה ומודלי תהליך (Waterfall, מודל V, Build and Fix), Scrum ועקרונות Agile, ודרישות: פונקציונליות מול לא פונקציונליות, דרישה טובה, MRD ו-PRD. כל שלב פותח בשיעור קצר וממשיך בשאלות בסגנון המבחן. כל השלבים פתוחים; שלב נחשב עבור מ-80%." },
  };
  const PASS = 80;
  const ALL = window.COURSES || {};
  const screen = document.getElementById("screen-course");
  if (!screen) return;
  const has = id => ALL[id] && ALL[id].levels && ALL[id].levels.length;
  Object.keys(META).forEach(id => { if (!has(id)) document.querySelectorAll(`[data-course="${id}"]`).forEach(el => el.style.display = "none"); });
  if (!Object.keys(META).some(has)) { const h = document.getElementById("crsHub"); if (h) h.style.display = "none"; }

  const iso = window.bidiHtml || (h => h);
  let C = null;            // the open course: {id, meta, levels, prog}
  let cur = null, run = null;   // the level being played, and its answers {qid: ok}
  const prog = {};
  function load(id){ try { return JSON.parse(localStorage.getItem(META[id].store)) || { levels:{} }; } catch(e){ return { levels:{} }; } }
  function save(){ try { localStorage.setItem(C.meta.store, JSON.stringify(C.prog)); } catch(e){} }
  function course(id){ prog[id] = prog[id] || load(id); return { id, meta: META[id], levels: ALL[id].levels, prog: prog[id] }; }

  const views = ["crsMapView", "crsLessonView", "crsSumView"];
  function view(id){ show("screen-course"); views.forEach(v => document.getElementById(v).classList.toggle("hidden", v !== id)); }
  const passedIn = (c, L) => ((c.prog.levels[L.id] || {}).best || 0) >= PASS;
  const passed = L => passedIn(C, L);
  const recommendedIn = c => c.levels.find(L => !passedIn(c, L));
  const levelName = L => `שלב ${L.order} · ${L.title}`;
  const backToMode = () => { S.mode = (document.querySelector('input[name=mode]:checked') || {}).value || "practice"; };

  /* ---------- rendering helpers ---------- */
  // question / explanation text: escape, `code`, **bold**, newlines, then the bidi isolates
  function rich(s){
    let h = escapeHtml(String(s == null ? "" : s));
    h = h.replace(/`([^`]+)`/g, (m, c) => `<code dir="ltr">${c}</code>`)
         .replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>")
         .replace(/\n/g, "<br>");
    return iso(h);
  }
  window.crsRich = rich;
  // a data table attached to a question: {caption?, head:[...], rows:[[...]]}
  function tableHtml(t){
    if (!t) return "";
    const cell = c => { const s = String(c); return /[֐-׿]/.test(s) ? rich(s) : `<span dir="ltr">${rich(s)}</span>`; };
    return `<div class="tbl-wrap q-table"><table>` +
      (t.head ? `<thead><tr>${t.head.map(h => `<th>${cell(h)}</th>`).join("")}</tr></thead>` : "") +
      `<tbody>${t.rows.map(r => `<tr>${r.map(c => `<td>${cell(c)}</td>`).join("")}</tr>`).join("")}</tbody></table></div>` +
      (t.caption ? `<div class="q-table-cap">${rich(t.caption)}</div>` : "");
  }
  window.crsTable = tableHtml;
  // lesson html: wrap tables for sideways scroll on phones, isolate formulas and English terms
  function lessonHtml(html){
    return iso(String(html || "").replace(/<table>/g, '<div class="tbl-wrap"><table>').replace(/<\/table>/g, "</table></div>"));
  }

  /* ---------- map ---------- */
  function renderMap(){
    const LV = C.levels, rec = recommendedIn(C), nPass = LV.filter(passed).length;
    $("#crsTitle").textContent = `${C.meta.icon} ${C.meta.title}`;
    $("#crsIntro").textContent = C.meta.intro;
    $("#crsOverall").innerHTML =
      `עברת <b>${nPass}</b> מתוך <b>${LV.length}</b> שלבים` +
      `<div class="progress" style="margin-top:.5rem"><div class="progress-fill" style="width:${nPass / LV.length * 100}%"></div></div>` +
      (nPass === LV.length ? `<p style="margin:.6rem 0 0">🏆 סיימת את כל הקורס. הצעד הבא: שאלות ${C.meta.name} מהמבחנים.</p>` : "");
    $("#crsMap").innerHTML = LV.map(L => {
      const st = C.prog.levels[L.id];
      const cls = ["crs-lvl", passed(L) ? "passed" : "", L === rec ? "next" : "", L.boss ? "boss" : ""].join(" ");
      const status = !st ? `עוד לא התחלת · ${L.questions.length} שאלות`
        : passed(L) ? `✓ עברת · שיא ${st.best}%` : `ניסיון אחרון ${st.last}% · שיא ${st.best}% (צריך 80%)`;
      return `<button class="${cls}" data-id="${L.id}" type="button">
        <span class="num">שלב ${L.order}${L.boss ? " · מבחן גמר" : ""}</span>
        <span class="ttl">${L.icon || ""} ${iso(escapeHtml(L.title))}</span>
        <span class="gl">${iso(escapeHtml(L.goal || ""))}</span>
        <span class="st">${status}</span></button>`;
    }).join("");
    $("#crsMap").querySelectorAll(".crs-lvl").forEach(b => b.onclick = () => openLesson(LV.find(L => L.id === b.dataset.id)));
  }
  function openMap(id){ if (id) C = course(id); cur = null; renderMap(); view("crsMapView"); }

  /* ---------- lesson ---------- */
  function openLesson(L){
    cur = L;
    const nReal = L.questions.filter(q => q.ref).length;
    $("#crsLesson").innerHTML =
      `<div class="q-head"><span class="chip">שלב ${L.order} מתוך ${C.levels.length}</span><span class="chip soft">${L.questions.length} שאלות${nReal ? ` · ${nReal} מהמבחנים` : ""}</span></div>` +
      `<h2 class="learn-h">${L.icon || ""} ${iso(escapeHtml(L.title))}</h2><p class="sub crs-goal">${iso(escapeHtml(L.goal || ""))}</p>` +
      `<div class="lesson-body">${lessonHtml(L.lesson && L.lesson.html)}</div>`;
    view("crsLessonView");
  }

  /* ---------- level quiz (runs on the main engine) ---------- */
  // a level question in engine form: {options, correctIndex} like the bank; refs are cloned from the bank
  function engineQ(q, L){
    const levelTitle = levelName(L), badge = `${C.meta.icon} ${C.meta.name}`;
    let base;
    if (q.ref){
      const b = QS.find(x => x.id === q.ref);
      base = Object.assign({}, b, { id: `${L.id}:${q.ref}`, explanation: q.explanation || b.explanation, recap: q.recap,
        fromExam: b.sourceLabel ? `${b.sourceLabel}, שאלה ${(String(b.id).match(/-Q(\d+)$/) || [])[1] || ""}` : b.id, examId: b.id });
    } else {
      base = Object.assign({}, q, { correctIndex: q.answer });
    }
    return Object.assign(base, { course: { courseId: C.id, levelId: L.id, levelTitle, badge } });
  }
  function startLevel(L){
    cur = L; run = {};
    S.mode = "course"; S._views = null;
    S.pool = L.questions.map(q => engineQ(q, L));
    S.pos = 0; S.hist = []; S.hpos = 0; S.streak = 0;
    $("#prevBtn").classList.remove("hidden");
    show("screen-quiz");
    renderQuestion();
  }
  function record(q, ok){ if (run && !(q.id in run)) run[q.id] = ok; }

  function finishLevel(){
    const L = cur; if (!L) return openMap();
    const qs = S.pool, total = qs.length;
    const correct = qs.filter(q => run && run[q.id]).length;
    const pct = Math.round(correct / total * 100);
    const prev = C.prog.levels[L.id] || {};
    C.prog.levels[L.id] = { best: Math.max(prev.best || 0, pct), last: pct, at: Date.now() };
    save();
    const ok = pct >= PASS, LV = C.levels, nextL = LV[LV.indexOf(L) + 1];
    const wrong = qs.filter(q => !(run && run[q.id]));
    backToMode();
    $("#crsSum").innerHTML =
      `<div class="q-head" style="justify-content:center"><span class="chip">${iso(escapeHtml(levelName(L)))}</span></div>` +
      `<div class="big">${pct}%</div><div><b><bdi dir="ltr">${correct} / ${total}</bdi></b> תשובות נכונות</div>` +
      `<p class="msg">${ok ? (L.boss ? `🏆 עברת את מבחן הגמר של ${C.meta.name}!` : "✓ עברת את השלב! אפשר להתקדם.") :
        "עוד לא 80%. כדאי לקרוא שוב את השיעור ולנסות שוב, זה בדיוק השלב שבו זה נבנה."}</p>` +
      (wrong.length ? `<div class="crs-review"><div class="crs-review-t">כדאי לחזור על:</div>${
        wrong.map(q => `<div>• ${rich(q.recap || q.question)}</div>`).join("")}</div>` : "") +
      `<div class="crs-actions">` +
        (nextL ? `<button class="btn ${ok ? "primary" : "ghost"}" data-act="next">לשלב הבא: ${iso(escapeHtml(nextL.title))} ⟵</button>` : "") +
        (L.boss || !nextL ? `<button class="btn primary" data-act="real">לשאלות ${C.meta.name} מהמבחנים האמיתיים ⟵</button>` : "") +
        `<button class="btn ${ok ? "ghost" : "primary"}" data-act="retry">🔁 לנסות שוב</button>` +
        `<button class="btn ghost" data-act="lesson">📘 לשיעור</button>` +
        `<button class="btn ghost" data-act="map">🗺️ למפת השלבים</button>` +
      `</div>`;
    $("#crsSum").querySelectorAll("[data-act]").forEach(b => b.onclick = () => {
      const a = b.dataset.act;
      if (a === "next") openLesson(nextL);
      else if (a === "retry") startLevel(L);
      else if (a === "lesson") openLesson(L);
      else if (a === "real") realExam();
      else openMap();
    });
    view("crsSumView");
  }
  function exit(){ backToMode(); S.hist = []; S.hpos = 0; cur ? openLesson(cur) : openMap(); }

  // hand off to the real exam questions of this course's topics (free practice)
  function realExam(){
    const r = document.querySelector('input[name=mode][value="practice"]'); if (r) r.checked = true;
    $("#examOpts").classList.add("hidden");
    ["#officialOnly", "#mistakesOnly"].forEach(s => { const el = $(s); if (el) el.checked = false; });
    S.mode = "practice"; S._views = null;
    S.pool = shuffle(C.meta.topics.flatMap(t => filteredPool(t, { officialOnly: false, mistakesOnly: false })));
    S.pos = 0; S.hist = []; S.hpos = 0; S.streak = 0;
    $("#prevBtn").classList.remove("hidden");
    show("screen-quiz");
    renderQuestion();
  }

  /* ---------- wiring ---------- */
  $("#crsLessonGo").onclick = () => cur && startLevel(cur);
  $("#crsLessonBack").onclick = () => openMap();
  $("#crsHomeBtn").onclick = () => quit();
  $("#crsResetBtn").onclick = () => { if (confirm(`לאפס את ההתקדמות בקורס ${C.meta.name}?`)){ C.prog.levels = {}; save(); renderMap(); } };
  function paintPromos(){
    document.querySelectorAll(".crs-promo[data-course]").forEach(el => {
      const id = el.dataset.course; if (!has(id)) return;
      const c = course(id), n = c.levels.filter(L => passedIn(c, L)).length, rec = recommendedIn(c);
      const sub = el.querySelector(".crs-promo-sub");
      if (!sub.dataset.base) sub.dataset.base = sub.textContent;
      sub.textContent = n ? `עברת ${n} מתוך ${c.levels.length} שלבים${rec ? ". הבא בתור: " + rec.title : ". סיימת, כל הכבוד!"}` : sub.dataset.base;
    });
  }
  document.querySelectorAll("[data-course]").forEach(el => {
    const id = el.dataset.course; if (!has(id)) return;
    el.onclick = () => openMap(id);
    if (el.classList.contains("crs-promo"))
      el.onkeydown = e => { if (e.key === "Enter" || e.key === " "){ e.preventDefault(); openMap(id); } };
  });
  paintPromos();
  window.addEventListener("seq:home", paintPromos);

  // header: one entry that brings you to the course cards on the home screen
  const hub = $("#crsHub");
  if (hub) hub.onclick = () => { quit(); setTimeout(() => { const p = $(".crs-promos"); if (p) p.scrollIntoView({ behavior: "smooth", block: "start" }); }, 60); };

  window.COURSE = { record, finishLevel, exit, openMap, openLesson: L => openLesson(L), startLevel: L => startLevel(L), META };

  // deep link: ?course=pat (map) - ?course=pat&level=P03 (that lesson) - ...&play=1 (its quiz)
  try {
    const p = new URLSearchParams(location.search), id = p.get("course");
    if (id && has(id)){
      C = course(id);
      const L = C.levels.find(l => l.id === p.get("level"));
      if (!L) openMap(); else if (p.get("play")) startLevel(L); else openLesson(L);
    }
  } catch(e){}
})();
