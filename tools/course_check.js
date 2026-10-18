// Guided courses ("צריך עזרה?"): data lint + index.html script-tag sync.
// usage: node tools/course_check.js            lint every course, fail on any error
//        node tools/course_check.js --sync     also rewrite the COURSE LEVELS script block in index.html
//        node tools/course_check.js --dump pat [P03]   print the questions with their keyed answer, for review
//        node tools/course_check.js --json out.json    write every course question (with key) as JSON, for the offline checkers
//        node tools/course_check.js --blind out.json   write the questions WITHOUT keys/explanations (blind re-solve)
const fs = require("fs"), path = require("path"), vm = require("vm");
const ROOT = path.join(__dirname, "..");
const args = process.argv.slice(2);

const COURSE_TOPICS = { pat: ["patterns"], uml: ["uml"], tst: ["testing"], proc: ["intro", "agile", "requirements"] };
const PREFIX = { pat: "P", uml: "U", tst: "T", proc: "R" };
// bank questions answerable only from slides the lecturer cut from the 8.10 exam (app.js OCT8_DROP): never teach or ask them
const OCT8_DROP = new Set(["19B-B-Q3", "19B-B-Q13", "21-B-Q10", "21S-B-Q10"]);

const files = Object.keys(COURSE_TOPICS).flatMap(c => {
  const dir = path.join(ROOT, "courses", c);
  return fs.existsSync(dir) ? fs.readdirSync(dir).filter(f => /\.js$/.test(f)).sort().map(f => `courses/${c}/${f}`) : [];
});

const ctx = { console }; ctx.window = ctx;   // browser globals: window.X and bare X are the same
vm.createContext(ctx);
const load = f => vm.runInContext(fs.readFileSync(path.join(ROOT, f), "utf8"), ctx, { filename: f });
load("questions.js"); load("courses.js");
files.forEach(load);
const BANK = ctx.window.QUESTIONS, byId = new Map(BANK.map(q => [q.id, q]));
const COURSES = ctx.window.COURSES;

let bad = 0; const err = (...a) => { console.log("ERROR", ...a); bad++; };
const warn = (...a) => console.log("warn ", ...a);
const codes = [...new Set(BANK.map(q => q.examCode))].sort((a, b) => b.length - a.length)
  .map(c => c.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
const QID = new RegExp(`(?<![A-Za-z0-9])(?:${codes.join("|")})-Q(\\d+)(?![0-9])`, "g");
const refsIn = s => [...String(s || "").matchAll(QID)].map(m => m[0]);
const HEB = /[֐-׿]/;

const qIds = new Set(); let total = 0, totalRefs = 0, cited = new Set();
Object.keys(COURSE_TOPICS).forEach(cid => {
  const LV = (COURSES[cid] || { levels: [] }).levels;
  if (!LV.length) { warn(cid, "has no levels yet"); return; }
  if (LV.length < 6 || LV.length > 10) err(cid, `has ${LV.length} levels (want 6-10)`);
  if (!LV[LV.length - 1].boss) err(cid, "last level must be the boss");
  const lvIds = new Set(), orders = new Set();
  LV.forEach((L, i) => {
    const W = `${cid}/${L.id}`;
    if (!new RegExp(`^${PREFIX[cid]}\\d\\d$`).test(L.id)) err(W, `level id must look like ${PREFIX[cid]}01`);
    if (lvIds.has(L.id)) err(W, "duplicate level id"); lvIds.add(L.id);
    if (orders.has(L.order)) err(W, "duplicate order"); orders.add(L.order);
    if (L.order !== i + 1) err(W, `order ${L.order} but position ${i + 1} (orders must be 1..n)`);
    ["title", "goal", "icon"].forEach(k => { if (!L[k]) err(W, "missing", k); });
    if (L.boss && i !== LV.length - 1) err(W, "boss level must be last");
    const html = (L.lesson || {}).html || "";
    if (html.length < 600) err(W, `lesson.html too short (${html.length} chars)`);
    if (/\$\$|\\frac|\\sum|\\sqrt/.test(html)) err(W, "lesson has LaTeX");
    const tags = "div|table|ul|ol|p|h3|h4|b|strong|code|span|li|tr|td|th|thead|tbody|pre";
    const opens = (html.match(new RegExp(`<(${tags})\\b`, "g")) || []).length;
    const closes = (html.match(new RegExp(`</(${tags})>`, "g")) || []).length;
    if (opens !== closes) err(W, `lesson html tag balance off: ${opens} opens vs ${closes} closes`);
    if (!/lesson-rule/.test(html)) err(W, "lesson has no 🔑 lesson-rule box (the recipe)");
    if (!/lesson-ex/.test(html)) err(W, "lesson has no worked example (lesson-ex)");
    const lref = refsIn(html);
    lref.forEach(id => { cited.add(id); if (!byId.has(id)) err(W, "lesson cites unknown question", id); if (OCT8_DROP.has(id)) err(W, "lesson cites a question cut from the 8.10 scope", id); });
    if (!lref.length) err(W, "lesson cites no exam question (ground it in the exams)");
    const qs = L.questions || [];
    if (qs.length < 4 || qs.length > 6) err(W, `has ${qs.length} questions (want 4-6)`);
    if (L.boss && qs.some(q => !q.ref)) err(W, "boss must be made only of real bank questions (ref)");
    if (L.boss && qs.length < 4) err(W, "boss needs 4-6 real questions");
    qs.forEach((q, j) => {
      total++;
      if (q.ref) {
        totalRefs++;
        const b = byId.get(q.ref), w = `${W} ref ${q.ref}`;
        if (!b) return err(w, "unknown bank question");
        if (OCT8_DROP.has(q.ref)) err(w, "cut from the 8.10 scope");
        if (!COURSE_TOPICS[cid].includes(b.topic)) warn(w, `bank topic ${b.topic} is outside this course`);
        if (!q.recap) err(w, "missing recap");
        if (qIds.has(`${L.id}:${q.ref}`)) err(w, "same exam question twice in a level"); qIds.add(`${L.id}:${q.ref}`);
        cited.add(q.ref);
        if (b.image && !fs.existsSync(path.join(ROOT, b.image))) err(w, "bank image missing", b.image);
        refsIn(q.explanation).forEach(id => { if (!byId.has(id)) err(w, "explanation cites unknown", id); });
        return;
      }
      const w = `${W} ${q.id || "#" + (j + 1)}`;
      if (!q.id || !q.id.startsWith(L.id + "-Q")) err(w, `question id must start with ${L.id}-Q`);
      if (qIds.has(q.id)) err(w, "duplicate question id"); qIds.add(q.id);
      if (!q.question) err(w, "missing question");
      if (!q.recap) err(w, "missing recap");
      if (!q.explanation || q.explanation.length < 40) err(w, "missing/short explanation");
      const o = q.options || [];
      if (o.length < 3 || o.length > 5) err(w, `${o.length} options (want 3-5)`);
      if (!Number.isInteger(q.answer) || q.answer < 0 || q.answer >= o.length) err(w, "answer index out of range:", q.answer);
      o.forEach((v, k) => { if (typeof v !== "string" || !v.trim()) err(w, "empty option", k); });
      if (new Set(o.map(v => String(v).trim())).size !== o.length) err(w, "two options have identical text");
      if (o.some(v => /^(תשובות?|אפשרויות?) [א-ו]( |$)|[א-ו] ו-?[א-ו] נכונות|כל התשובות|אף אחת מהתשובות|\{@/.test(v))) err(w, "option cites siblings (options are shuffled) or is an all/none-of-the-above");
      if (refsIn(q.question).length) err(w, "question stem cites an exam id");
      refsIn(q.explanation).forEach(id => { cited.add(id); if (!byId.has(id)) err(w, "explanation cites unknown", id); });
      if (q.table) {
        const t = q.table, n = (t.head || t.rows[0] || []).length;
        if (!Array.isArray(t.rows) || !t.rows.length) err(w, "table has no rows");
        else t.rows.forEach((r, k) => { if (r.length !== n) err(w, `table row ${k} has ${r.length} cells, header ${n}`); });
      }
      ["question", "explanation", "recap"].forEach(k => {
        const s = String(q[k] || "");
        if ((s.match(/\*\*/g) || []).length % 2) err(w, k, "has an unpaired **");
        if ((s.match(/`/g) || []).length % 2) err(w, k, "has an unpaired backtick");
      });
    });
  });
});

// index.html must load every level file, exactly once
const IDX = path.join(ROOT, "index.html");
let html = fs.readFileSync(IDX, "utf8");
const block = files.map(f => `<script src="${f}?v=1"></script>`).join("\n");
const re = /(<!-- COURSE LEVELS -->\r?\n)([\s\S]*?)(<!-- \/COURSE LEVELS -->)/;   // \r?: autocrlf checkouts
if (!re.test(html)) err("index.html has no COURSE LEVELS block");
else if (args.includes("--sync")) {
  const nl = html.includes("\r\n") ? "\r\n" : "\n";
  html = html.replace(re, (m, a, b, c) => a + (block ? block.split("\n").join(nl) + nl : "") + c);
  fs.writeFileSync(IDX, html);
  console.log(`index.html: ${files.length} level scripts`);
} else {
  const listed = [...html.match(re)[2].matchAll(/src="([^"?]+)/g)].map(m => m[1]);
  files.forEach(f => { if (!listed.includes(f)) err("index.html does not load", f, "(run with --sync)"); });
  listed.forEach(f => { if (!files.includes(f)) err("index.html loads a missing file", f); });
}

const flat = () => Object.keys(COURSES).flatMap(cid => COURSES[cid].levels.flatMap(L => L.questions.map((q, j) => {
  if (q.ref) { const b = byId.get(q.ref); return { course: cid, level: L.id, id: `${L.id}:${q.ref}`, ref: q.ref, question: b.question, options: b.options, answer: b.correctIndex }; }
  return { course: cid, level: L.id, id: q.id, question: q.question, code: q.code, table: q.table, options: q.options, answer: q.answer, explanation: q.explanation };
})));
const ji = args.indexOf("--json");
if (ji >= 0) { fs.writeFileSync(args[ji + 1], JSON.stringify(flat(), null, 1)); console.log("wrote", args[ji + 1]); }
const bi = args.indexOf("--blind");
if (bi >= 0) {
  const items = flat().filter(q => !q.ref).map(q => ({ id: q.id, question: q.question, code: q.code, table: q.table, options: q.options }));
  fs.writeFileSync(args[bi + 1], JSON.stringify(items, null, 1)); console.log("wrote", items.length, "blind questions to", args[bi + 1]);
}

const di = args.indexOf("--dump");
if (di >= 0) {
  const cid = args[di + 1], only = args[di + 2];
  (COURSES[cid] || { levels: [] }).levels.filter(L => !only || L.id === only).forEach(L => {
    console.log(`\n=== ${L.id} ${L.title}`);
    L.questions.forEach(q => {
      if (q.ref) { const b = byId.get(q.ref); console.log(`\n[REF ${q.ref}] ${b.question}\n` + b.options.map((o, k) => `  ${k === b.correctIndex ? "*" : " "} ${o}`).join("\n")); return; }
      console.log(`\n[${q.id}] ${q.question}` + (q.code ? "\n" + q.code : "") + (q.table ? "\n" + JSON.stringify(q.table) : "") + "\n" +
        q.options.map((o, k) => `  ${k === q.answer ? "*" : " "} ${o}`).join("\n") + `\n  -> ${q.explanation}`);
    });
  });
}

const per = Object.keys(COURSE_TOPICS).map(c => { const L = (COURSES[c] || { levels: [] }).levels; return `${c}: ${L.length} levels / ${L.reduce((n, l) => n + l.questions.length, 0)} q`; });
console.log(`\n${per.join(" · ")}\ntotal ${total} questions (${totalRefs} real exam questions), ${cited.size} distinct exam ids cited`);
if (bad) { console.log(`\nCOURSE CHECK FAILED: ${bad} error(s)`); process.exit(1); }
console.log("COURSE CHECK PASSED");
