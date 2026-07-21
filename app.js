"use strict";
/* Software-Engineering quiz — vanilla JS. Loads window.QUESTIONS from questions.js. */

const QS = Array.isArray(window.QUESTIONS) ? window.QUESTIONS : [];
const HE_KEYS = ["א","ב","ג","ד","ה","ו","ז","ח"];
const STORE = "seq_progress_v1";

const TOPICS = [
  ["all","כל הנושאים"],
  ["intro","מבוא להנדסת תוכנה"],
  ["agile","Agile · SCRUM · XP"],
  ["requirements","הנדסת דרישות"],
  ["uml","מידול ו-UML"],
  ["architecture","עיצוב ארכיטקטוני"],
  ["patterns","תבניות עיצוב"],
  ["solid","עקרונות SOLID"],
  ["testing","בדיקות ו-TDD"],
  ["oop_java","OOP ו-Java"],
  ["metrics","מטריקות ותצוגות"],
  ["config","אספקה וקונפיגורציה"],
];

/* ---------- storage ---------- */
function loadProgress(){
  try{ return JSON.parse(localStorage.getItem(STORE)) || {stats:{answered:0,correct:0},perQ:{}}; }
  catch(e){ return {stats:{answered:0,correct:0},perQ:{}}; }
}
function saveProgress(){ try{ localStorage.setItem(STORE, JSON.stringify(P)); }catch(e){} }
let P = loadProgress();

/* ---------- helpers ---------- */
const $ = s => document.querySelector(s);
function shuffle(a){ a=a.slice(); for(let i=a.length-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); [a[i],a[j]]=[a[j],a[i]]; } return a; }
function show(id){ document.querySelectorAll(".screen").forEach(s=>s.classList.add("hidden")); $("#"+id).classList.remove("hidden"); window.scrollTo({top:0,behavior:"smooth"}); }
function filterMatch(q, topic, opts){
  if(topic!=="all" && q.topic!==topic) return false;
  if(opts.officialOnly && !q.official && !q.verified) return false;
  if(opts.mistakesOnly){ const r=P.perQ[q.id]; if(!r || r.correct) return false; }
  return true;
}
/* practice/topic pools de-duplicate recurring questions across exams (policy A);
   whole-exam mode keeps every question so a past test replays in full. */
function dedupePool(arr){
  const seen=new Set(), out=[];
  for(const q of arr){ const k=q.dedupKey||q.id; if(seen.has(k)) continue; seen.add(k); out.push(q); }
  return out;
}
function filteredPool(topic, opts){ return dedupePool(QS.filter(q=>filterMatch(q, topic, opts))); }
function countFor(topic, opts){ return filteredPool(topic, opts).length; }
// topics that actually have questions in the bank — empty taxonomy topics are hidden
// from the grid (but stay in TOPICS so they auto-appear if questions are added later).
const PRESENT = new Set(QS.map(q=>q.topic));

/* ---------- session state ---------- */
const S = { mode:"practice", topic:"all", pool:[], pos:0, current:null,
  exam:{count:25, minutes:120, answers:{}, endAt:0, timer:null} };

/* ---------- start screen ---------- */
function renderTopStats(){
  const a=P.stats.answered, c=P.stats.correct;
  const pct=a?Math.round(c/a*100):0;
  $("#topStats").innerHTML =
    `<div class="stat">נענו <b>${a}</b></div>`+
    `<div class="stat">דיוק <b>${pct}%</b></div>`+
    `<div class="stat">במאגר <b>${QS.length}</b></div>`;
}
function selectedOpts(){
  return { officialOnly: $("#officialOnly").checked, mistakesOnly: $("#mistakesOnly").checked };
}
function renderTopicGrid(){
  const opts=selectedOpts();
  $("#topicGrid").innerHTML = TOPICS.filter(([k])=>k==="all"||PRESENT.has(k)).map(([k,label])=>{
    const n=countFor(k,opts);
    const active = k===S.topic ? "active":"";
    const dis = n===0 && k!=="all" ? "disabled":"";
    return `<button class="topic-btn ${active}" data-topic="${k}" ${dis}>
      <span>${label}</span><span class="cnt">${n}</span></button>`;
  }).join("");
  document.querySelectorAll(".topic-btn").forEach(b=>{
    b.onclick=()=>{ S.topic=b.dataset.topic; renderTopicGrid(); updatePoolInfo(); };
  });
}
function selectedExam(){ const el=$("#examPick"); return (S.mode==="exam" && el) ? el.value : ""; }
function examQuestions(code){ return QS.filter(q=>q.examCode===code); }
function qNum(q){ const m=String(q.id).match(/-Q(\d+)$/); return m?parseInt(m[1],10):0; }
/* Exam-picker order: sample/practice papers first — they carry no year, so they have no
   place in the chronology — then real exams oldest→newest, newest at the bottom. */
function examOrder(code){
  const c=String(code);
  const practice=/^PRAC/.test(c);
  const sample=/^(SAMP|SP)/.test(c) || /-EX$/.test(c);
  if(sample||practice) return [0, practice?1:0, c];
  const m=c.match(/^(\d{2})/);
  return [1, m?2000+parseInt(m[1],10):9999, c];
}
function byExamOrder(a,b){
  const x=examOrder(a), y=examOrder(b);
  return (x[0]-y[0]) || (x[1]-y[1]) || String(x[2]).localeCompare(String(y[2]));
}
function populateExamPick(){
  const sel=$("#examPick"); if(!sel) return;
  const seen=new Map();                       // examCode -> sourceLabel
  QS.forEach(q=>{ if(q.examCode && !seen.has(q.examCode)) seen.set(q.examCode, q.sourceLabel||q.examCode); });
  sel.innerHTML = `<option value="">אקראי (כל המאגר)</option>` +
    [...seen.entries()].sort((a,b)=>byExamOrder(a[0],b[0]))
      .map(([code,label])=>`<option value="${code}">${escapeHtml(label)} (${examQuestions(code).length})</option>`).join("");
  sel.onchange=()=>{ syncExamOpts(); updatePoolInfo(); };
}
function syncExamOpts(){
  const wrap=$("#examCountWrap"); if(wrap) wrap.style.display = selectedExam() ? "none" : "";
}
function updatePoolInfo(){
  const code=selectedExam();
  if(code){
    const n=examQuestions(code).length;
    const label=(QS.find(q=>q.examCode===code)||{}).sourceLabel || code;
    $("#poolInfo").textContent = `מבחן ${label} — ${n} שאלות (מבחן מלא).`;
    $("#startBtn").disabled = n===0;
    return;
  }
  const opts=selectedOpts();
  const pool=filteredPool(S.topic,opts);
  const n=pool.length;
  const off=pool.filter(q=>q.official).length;
  const ver=pool.filter(q=>q.verified).length;
  $("#poolInfo").textContent = `נבחרו ${n} שאלות (${off} מחוון רשמי · ${ver} מאומת · ${n-off-ver} לא רשמי).`;
  $("#startBtn").disabled = n===0;
}
function initStart(){
  renderTopStats();
  populateExamPick();
  renderTopicGrid();
  syncExamOpts();
  updatePoolInfo();
  document.querySelectorAll('input[name=mode]').forEach(r=>{
    r.onchange=()=>{ S.mode=document.querySelector('input[name=mode]:checked').value;
      $("#examOpts").classList.toggle("hidden", S.mode!=="exam");
      $("#mistakesOnly").parentElement.style.display = S.mode==="exam"?"none":"";
      syncExamOpts();
      updatePoolInfo();
    };
  });
  $("#officialOnly").onchange = ()=>{ renderTopicGrid(); updatePoolInfo(); };
  $("#mistakesOnly").onchange = ()=>{ renderTopicGrid(); updatePoolInfo(); };
  $("#startBtn").onclick = startSession;
  $("#datasetInfo").textContent = `${QS.length} שאלות · מבחני 2019–2025`;
}

/* ---------- session ---------- */
function startSession(){
  S._views=null;
  const opts=selectedOpts();
  const pickedExam = selectedExam();
  let pool;
  if(pickedExam){
    // whole-test mode: all questions of one exam, original order (options still shuffled per-question)
    pool = examQuestions(pickedExam).slice().sort((a,b)=>qNum(a)-qNum(b));
  } else {
    pool = shuffle(filteredPool(S.topic,opts));
  }
  if(S.mode==="exam"){
    if(pickedExam){
      S.exam.count = pool.length;
    } else {
      S.exam.count = Math.min(parseInt($("#examCount").value,10), pool.length);
      pool = pool.slice(0, S.exam.count);
    }
    S.exam.minutes = parseInt($("#examMinutes").value,10);
    S.exam.answers = {};
    S.exam.endAt = Date.now() + S.exam.minutes*60000;
    startTimer();
  }
  S.pool = pool; S.pos = 0;
  $("#prevBtn").classList.toggle("hidden", S.mode!=="exam");
  show("screen-quiz");
  renderQuestion();
}

function makeView(q){
  // Fisher–Yates: defeats "always-first". Skipped when an option cites its siblings by
  // printed letter ("תשובות א ו-ג נכונות") — shuffling would make that reference nonsense.
  const idx = q.options.map((_,i)=>i);
  const order = q.lockOrder ? idx : shuffle(idx);
  return { q, order, correctDisplay: order.indexOf(q.correctIndex), answered:false, chosen:null };
}

function renderQuestion(){
  const q = S.pool[S.pos];
  if(S.mode==="exam"){
    S.current = S._views?.[q.id] || makeView(q);
    (S._views ||= {})[q.id] = S.current;
  } else {
    S.current = makeView(q);
  }
  const v=S.current;

  $("#qTopic").textContent = q.topicLabel || q.topic;
  $("#qSource").textContent = q.sourceLabel || (q.source==="exam"?"מבחן":"תרגול");
  const badge=$("#qBadge");
  const tier = q.official ? "official" : (q.verified ? "verified" : "unofficial");
  badge.textContent = tier==="official" ? "מחוון רשמי" : tier==="verified" ? "מאומת ✓" : "לא רשמי · לבדיקה";
  badge.className = "chip " + tier;

  $("#questionText").textContent = q.question;
  $("#qExtras").innerHTML = extrasHtml(q);

  $("#optionsList").innerHTML = v.order.map((origIdx,disp)=>
    `<button class="opt" data-disp="${disp}">
       <span class="key">${HE_KEYS[disp]||disp+1}</span>
       <span class="txt">${optionHtml(q.options[origIdx])}</span>
     </button>`).join("");
  document.querySelectorAll(".opt").forEach(b=> b.onclick=()=>choose(parseInt(b.dataset.disp,10)));

  const fb=$("#feedback"); fb.classList.add("hidden"); fb.className="feedback hidden";

  if(S.mode==="exam" && q.id in S.exam.answers){
    const chosenDisp = v.order.indexOf(S.exam.answers[q.id]);
    markExamChoice(chosenDisp);
  }

  $("#progressFill").style.width = ((S.pos)/(S.pool.length))*100 + "%";
  if(S.mode==="exam"){
    $("#quizMeta").innerHTML = `שאלה ${S.pos+1}/${S.pool.length} <span id="tmr" class="timer"></span>`;
    renderTimer();
    $("#nextBtn").classList.toggle("hidden", S.pos>=S.pool.length-1);
    $("#submitExamBtn").classList.toggle("hidden", S.pos<S.pool.length-1);
    $("#prevBtn").disabled = S.pos===0;
    $("#streakBox").textContent = `נענו ${Object.keys(S.exam.answers).length}/${S.pool.length}`;
  } else {
    $("#quizMeta").textContent = `שאלה ${S.pos+1}`;
    $("#nextBtn").classList.add("hidden");
    $("#submitExamBtn").classList.add("hidden");
    const a=P.stats.answered,c=P.stats.correct;
    $("#streakBox").textContent = `רצף נכון: ${S.streak||0} · דיוק כולל ${a?Math.round(c/a*100):0}%`;
  }
}

function escapeHtml(s){ return String(s).replace(/[&<>]/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;"}[m])); }

/* code snippet (LTR monospace) and/or figure image attached to a question */
function extrasHtml(q){
  let h="";
  if(q.code)  h+=`<pre class="q-code" dir="ltr"><code>${escapeHtml(q.code)}</code></pre>`;
  if(q.image) h+=`<figure class="q-fig"><img class="q-img" src="${q.image}" alt="" loading="lazy"></figure>`;
  return h;
}

/* an option may be plain text or an image marker ("img:<path>") */
function optionHtml(opt){
  const s=String(opt);
  if(s.startsWith("img:")) return `<img class="opt-img" src="${s.slice(4)}" alt="" loading="lazy">`;
  // options with no Hebrew (code/output answers) must render LTR, or the RTL page reorders them
  if(!/[֐-׿]/.test(s)) return `<span class="opt-ltr" dir="ltr">${escapeHtml(s)}</span>`;
  return escapeHtml(opt);
}

/* ---------- answering ---------- */
function choose(disp){
  const v=S.current, q=v.q;
  if(S.mode==="exam"){
    S.exam.answers[q.id] = v.order[disp];
    markExamChoice(disp);
    $("#streakBox").textContent = `נענו ${Object.keys(S.exam.answers).length}/${S.pool.length}`;
    return;
  }
  if(v.answered) return;
  v.answered=true; v.chosen=disp;
  const correct = disp===v.correctDisplay;
  document.querySelectorAll(".opt").forEach((b,i)=>{
    b.disabled=true;
    if(i===v.correctDisplay) b.classList.add("correct");
    else if(i===disp) b.classList.add("wrong");
  });
  recordAnswer(q, correct);
  S.streak = correct ? (S.streak||0)+1 : 0;
  const fb=$("#feedback");
  fb.className = "feedback " + (correct?"good":"bad");
  fb.innerHTML = `<div class="verdict">${correct?"✓ נכון":"✗ לא נכון"}</div>`+
    `<div class="expl">${escapeHtml(q.explanation||"")}</div>`+
    (q.official ? "" : q.verified
        ? `<span class="note">✓ אומת בשתי בדיקות עצמאיות (לא מתוך מחוון רשמי).</span>`
        : `<span class="note">⚠ תשובה לא רשמית — נגזרה מחומר הקורס, כדאי לאמת.</span>`)+
    `<span class="note">מקור: ${escapeHtml(q.sourceLabel||"")}</span>`;
  $("#nextBtn").classList.remove("hidden");
  $("#nextBtn").focus();
  renderTopStats();
  const a=P.stats.answered,c=P.stats.correct;
  $("#streakBox").textContent = `רצף נכון: ${S.streak} · דיוק כולל ${a?Math.round(c/a*100):0}%`;
}
function markExamChoice(disp){
  document.querySelectorAll(".opt").forEach((b,i)=> b.classList.toggle("chosen-exam", i===disp));
}
function recordAnswer(q, correct){
  P.stats.answered++; if(correct) P.stats.correct++;
  P.perQ[q.id] = { correct, t: Date.now() };
  saveProgress();
}

/* ---------- navigation ---------- */
function next(){
  if(S.mode==="practice"){
    if(!S.current.answered) return;
    if(S.pos>=S.pool.length-1){ S.pool = shuffle(S.pool); S.pos=0; }
    else S.pos++;
    renderQuestion();
  } else {
    if(S.pos<S.pool.length-1){ S.pos++; renderQuestion(); }
  }
}
function prev(){ if(S.mode==="exam" && S.pos>0){ S.pos--; renderQuestion(); } }

/* ---------- timer (exam) ---------- */
function startTimer(){ clearInterval(S.exam.timer); S.exam.timer=setInterval(renderTimer,1000); }
function renderTimer(){
  const el=$("#tmr"); if(!el) return;
  let ms=S.exam.endAt-Date.now();
  if(ms<=0){ ms=0; clearInterval(S.exam.timer); submitExam(true); return; }
  const m=Math.floor(ms/60000), s=Math.floor(ms%60000/1000);
  el.textContent = `⏱ ${m}:${String(s).padStart(2,"0")}`;
  el.classList.toggle("danger", ms<60000);
}

/* ---------- exam grading ---------- */
function submitExam(auto){
  clearInterval(S.exam.timer);
  if(!auto){
    const unans=S.pool.length-Object.keys(S.exam.answers).length;
    if(unans>0 && !confirm(`נותרו ${unans} שאלות ללא מענה. להגיש בכל זאת?`)) { startTimer(); return; }
  }
  let correct=0; const byTopic={}; const review=[];
  S.pool.forEach(q=>{
    const chosen = q.id in S.exam.answers ? S.exam.answers[q.id] : null;
    const ok = chosen===q.correctIndex;
    if(ok) correct++;
    recordAnswer(q, ok);
    (byTopic[q.topic] ||= {n:0,c:0}); byTopic[q.topic].n++; if(ok) byTopic[q.topic].c++;
    review.push({q, chosen, ok});
  });
  renderResults(correct, byTopic, review);
  renderTopStats();
  show("screen-results");
}
function renderResults(correct, byTopic, review){
  const total=S.pool.length, pct=Math.round(correct/total*100);
  $("#resultsSummary").innerHTML =
    `<div class="scorering" style="--p:${pct}"><span>${pct}%</span></div>`+
    `<div class="txt"><b>${correct} / ${total}</b> תשובות נכונות<br>`+
    `<span style="color:var(--muted)">${pct>=60?"עברת! 🎉":"עוד קצת תרגול 💪"}</span></div>`;
  $("#resultsByTopic").innerHTML = Object.entries(byTopic).map(([t,o])=>{
    const lbl=(TOPICS.find(x=>x[0]===t)||[t,t])[1]; const p=Math.round(o.c/o.n*100);
    return `<div class="tline"><span>${lbl}</span>
      <span class="tbar"><i style="width:${p}%"></i></span><span>${o.c}/${o.n}</span></div>`;
  }).join("");
  $("#resultsReview").innerHTML = review.map(r=>{
    const v=r.q; const chosenTxt = r.chosen!=null ? optionHtml(v.options[r.chosen]) : "— לא נענתה —";
    return `<div class="rev ${r.ok?"ok":"bad"}">
      <div class="rq">${escapeHtml(v.question)}</div>
      ${extrasHtml(v)}
      <div class="ra"><span class="${r.ok?"good":"miss"}">תשובתך: ${chosenTxt}</span>`+
      (r.ok?"":` · <span class="good">הנכונה: ${optionHtml(v.options[v.correctIndex])}</span>`)+
      `<br>${escapeHtml(v.explanation||"")}${v.official?"":(v.verified?" (מאומת ✓)":" (לא רשמי)")}</div></div>`;
  }).join("");
}

/* ---------- controls ---------- */
function quit(){ clearInterval(S.exam.timer); S._views=null; S.streak=0; initStart(); show("screen-start"); }
function bindGlobal(){
  $("#nextBtn").onclick=next;
  $("#prevBtn").onclick=prev;
  $("#submitExamBtn").onclick=()=>submitExam(false);
  $("#quitBtn").onclick=()=>{ if(S.mode!=="exam"||confirm("לצאת מהמבחן? ההתקדמות לא תישמר.")) quit(); };
  $("#backHomeBtn").onclick=quit;
  function goHome(){
    const inExamQuiz = S.mode==="exam" && !$("#screen-quiz").classList.contains("hidden");
    if(inExamQuiz && !confirm("לצאת מהמבחן? ההתקדמות לא תישמר.")) return;
    quit();
  }
  const brand=$("#brandHome");
  if(brand){
    brand.style.cursor="pointer";
    brand.onclick=goHome;
    brand.onkeydown=e=>{ if(e.key==="Enter"||e.key===" "){ e.preventDefault(); goHome(); } };
  }
  $("#resetProgress").onclick=()=>{ if(confirm("לאפס את כל ההתקדמות וההיסטוריה?")){ P={stats:{answered:0,correct:0},perQ:{}}; saveProgress(); renderTopStats(); renderTopicGrid(); updatePoolInfo(); } };
  document.addEventListener("click", e=>{
    const img=e.target.closest(".q-img"); if(!img) return;
    const lb=$("#lightbox"), lbImg=$("#lightboxImg");
    if(!lb||!lbImg) return;
    lbImg.src=img.src; lbImg.alt=img.alt||""; lb.classList.remove("hidden");
  });
  document.addEventListener("keydown",e=>{
    if($("#screen-quiz").classList.contains("hidden")) return;
    if(/^[1-8]$/.test(e.key)){ const b=document.querySelector(`.opt[data-disp="${+e.key-1}"]`); if(b && !b.disabled) b.click(); }
    else if(e.key==="Enter"){ if(!$("#nextBtn").classList.contains("hidden")) next(); else if(!$("#submitExamBtn").classList.contains("hidden")) submitExam(false); }
    else if(e.key==="ArrowLeft" && !$("#nextBtn").classList.contains("hidden")) next();
    else if(e.key==="ArrowRight" && S.mode==="exam") prev();
  });
}

/* ---------- theme toggle ---------- */
(function initTheme(){
  const THEME_KEY = "seq_theme";
  const btn = document.getElementById("themeToggle");
  if(!btn) return;
  const root = document.documentElement;
  const systemDark = () => !window.matchMedia || !window.matchMedia("(prefers-color-scheme: light)").matches;
  const effective = () => root.dataset.theme || (systemDark() ? "dark" : "light");
  const paint = () => { btn.textContent = effective()==="dark" ? "🌙" : "☀️"; };
  paint();
  btn.addEventListener("click", () => {
    const next = effective()==="dark" ? "light" : "dark";
    root.dataset.theme = next;
    try{ localStorage.setItem(THEME_KEY, next); }catch(e){}
    paint();
  });
  if(window.matchMedia){
    window.matchMedia("(prefers-color-scheme: light)").addEventListener?.("change", () => { if(!root.dataset.theme) paint(); });
  }
})();

/* ---------- learning section ---------- */
(function initLearn(){
  const data = Array.isArray(window.LEARN) ? window.LEARN : [];
  const entry = document.getElementById("learnEntry");
  const screen = document.getElementById("screen-learn");
  if(!entry || !screen) return;
  if(!data.length){ entry.style.display = "none"; return; }

  const toc     = $("#learnToc");
  const content = $("#learnContent");
  const fill    = $("#learnProgressFill");
  const pos     = $("#learnPos");
  const prevB   = $("#learnPrev");
  const nextB   = $("#learnNext");
  const toggle  = $("#learnTocToggle");
  const backdrop= $("#learnBackdrop");
  const backB   = $("#learnBackBtn");
  const lb      = $("#lightbox");
  const lbImg   = $("#lightboxImg");
  const lbClose = $("#lightboxClose");
  let idx = 0, built = false;

  function buildToc(){
    toc.innerHTML = data.map((s,i)=>`<button data-i="${i}">${escapeHtml(s.title)}</button>`).join("");
    toc.querySelectorAll("button").forEach(b=> b.onclick=()=>{ go(+b.dataset.i); closeDrawer(); });
    built = true;
  }
  function go(i){
    idx = Math.max(0, Math.min(data.length-1, i));
    const s = data[idx];
    content.innerHTML = `<h2 class="learn-h">${escapeHtml(s.title)}</h2>` + s.html;
    toc.querySelectorAll("button").forEach((b,j)=> b.classList.toggle("active", j===idx));
    const active = toc.querySelector("button.active");
    if(active) active.scrollIntoView({block:"nearest"});
    fill.style.width = ((idx+1)/data.length*100) + "%";
    pos.textContent = `${idx+1} / ${data.length}`;
    prevB.disabled = idx===0;
    nextB.disabled = idx===data.length-1;
    window.scrollTo({top:0, behavior:"smooth"});
    content.focus({preventScroll:true});
  }
  function openLearn(){ if(!built) buildToc(); show("screen-learn"); go(idx); }
  function setDrawer(open){
    toc.classList.toggle("open", open);
    backdrop.classList.toggle("hidden", !open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
  }
  function closeDrawer(){ setDrawer(false); }

  entry.onclick  = openLearn;
  backB.onclick  = ()=>{ closeDrawer(); show("screen-start"); };
  prevB.onclick  = ()=> go(idx-1);
  nextB.onclick  = ()=> go(idx+1);
  toggle.onclick = ()=> setDrawer(!toc.classList.contains("open"));
  backdrop.onclick = closeDrawer;

  content.addEventListener("click", e=>{
    const img = e.target.closest(".learn-fig img");
    if(!img) return;
    lbImg.src = img.src; lbImg.alt = img.alt || "";
    lb.classList.remove("hidden");
  });
  function closeLb(){ lb.classList.add("hidden"); lbImg.src = ""; }
  lb.addEventListener("click", e=>{ if(e.target===lb) closeLb(); });
  lbClose.onclick = closeLb;

  document.addEventListener("keydown", e=>{
    if(!lb.classList.contains("hidden")){ if(e.key==="Escape") closeLb(); return; }
    if(screen.classList.contains("hidden")) return;
    if(e.key==="ArrowLeft") go(idx+1);
    else if(e.key==="ArrowRight") go(idx-1);
    else if(e.key==="Escape"){ closeDrawer(); show("screen-start"); }
  });
})();

/* ---------- deep link ---------- */
function autoStartFromURL(){
  let t;
  try{ t = new URLSearchParams(location.search).get("practice"); }catch(e){ return; }
  if(!t || !TOPICS.some(([k])=>k===t)) return;
  if(countFor(t, {officialOnly:false, mistakesOnly:false})===0) return;
  S.mode="practice"; S.topic=t;
  const r=document.querySelector('input[name=mode][value="practice"]'); if(r) r.checked=true;
  startSession();
}

/* ---------- boot ---------- */
if(!QS.length){
  document.getElementById("app").innerHTML="<div class='card'><h2>לא נטענו שאלות</h2><p>ודאו ש-<code>questions.js</code> נמצא לצד הדף.</p></div>";
}else{
  initStart(); bindGlobal(); autoStartFromURL();
}
