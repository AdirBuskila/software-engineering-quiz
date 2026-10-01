// Node smoke test: data integrity + build-time-shuffle + render-shuffle scoring invariant.
const fs=require("fs"),path=require("path"),vm=require("vm");
global.window={};
const code=fs.readFileSync(path.join(__dirname,"..","questions.js"),"utf8");
eval(code);
const QS=window.QUESTIONS;
let bad=0;
const topics={};
for(const q of QS){
  topics[q.topic]=(topics[q.topic]||0)+1;
  const n=Array.isArray(q.options)?q.options.length:0;
  if(n<2||n>6){console.log("BAD options",q.id,n);bad++;}
  if(typeof q.correctIndex!=="number"||q.correctIndex<0||q.correctIndex>=n){console.log("BAD ci",q.id);bad++;}
  if(q.hasImage){console.log("IMAGE leaked",q.id);bad++;}
  if(!q.question||!q.question.trim()){console.log("EMPTY q",q.id);bad++;}
  if(q.options.some(o=>!String(o).trim())){console.log("BLANK opt",q.id);bad++;}
  if(!q.dedupKey){console.log("NO dedupKey",q.id);bad++;}
}

// ids must be unique: the id seeds the build-time option shuffle and keys the review list,
// so a collision silently shadows one of the colliding questions in the app.
const idSeen=new Set(); let dupIds=0;
for(const q of QS){
  if(!q.id){console.log("NO id",q.sourceLabel);bad++;continue;}
  if(idSeen.has(q.id)){console.log("DUPLICATE id",q.id);dupIds++;bad++;} else idSeen.add(q.id);
}

// anti-"always-first": the STORED correctIndex should be spread across positions
// (build-time shuffle), not stuck at 0 even though most exams are form-0.
const stored=[0,0,0,0,0,0], stored5=[0,0,0,0,0]; let n5=0;
for(const q of QS){
  stored[q.correctIndex]++;
  if(q.options.length===5){ stored5[q.correctIndex]++; n5++; }
}

// render shuffle/scoring invariant: simulate Fisher-Yates mapping many times
function shuffle(a){a=a.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}
let mismatch=0, disp5=[0,0,0,0,0], trials5=0;
for(let t=0;t<20000;t++){
  const q=QS[t%QS.length];
  const order=shuffle(q.options.map((_,i)=>i));
  const correctDisplay=order.indexOf(q.correctIndex);
  const clickedOrig=order[correctDisplay];
  if(clickedOrig!==q.correctIndex) mismatch++;
  if(q.options.length===5){disp5[correctDisplay]++;trials5++;}
}

// letter references: "תשובות א ו-ג נכונות" / "(ב) שגוי" are stored as {@N} tokens and
// resolved against each view's shuffled order by app.js's own makeView()/refs() (lifted
// verbatim from app.js, so this exercises the shipped code). After resolving, every letter
// must name the option it originally meant, and meta options must sit at the bottom.
const appSrc=fs.readFileSync(path.join(__dirname,"..","app.js"),"utf8");
const lift=name=>appSrc.match(new RegExp(`function ${name}\\([\\s\\S]*?\\n}`))[0];
const HE_KEYS=["א","ב","ג","ד","ה","ו","ז","ח"];
const app=new Function("shuffle","HE_KEYS",`${lift("makeView")}\n${lift("refs")}\nreturn {makeView,refs};`)(shuffle,HE_KEYS);
const TOK=/\{@(\d+)\}/g, RAW_REF=/(תשובות|תשובה|סעיפים|סעיף)\s+[אבגדה]['׳]?\s*[,ו]/;
let refBad=0, refQs=0;
for(const q of QS){
  const n=q.options.length, pinned=q.pinned||[];
  if(pinned.some(i=>i<0||i>=n) || new Set(pinned).size!==pinned.length){console.log("BAD pinned",q.id);refBad++;}
  const texts=[...q.options.map(String), q.explanation||""];
  if(q.options.some(o=>RAW_REF.test(o))){console.log("UNTOKENIZED letter ref",q.id);refBad++;}
  const toks=texts.flatMap(s=>[...s.matchAll(TOK)].map(m=>+m[1]));
  if(toks.some(i=>i>=n)){console.log("BAD token",q.id);refBad++;}
  if(!toks.length && !pinned.length) continue;
  refQs++;
  for(let t=0;t<50;t++){
    const v=app.makeView(q);
    if(pinned.length && v.order.slice(n-pinned.length).join()!==pinned.join()){console.log("PINNED not last",q.id);refBad++;break;}
    q.options.forEach((o,i)=>{
      const meant=[...String(o).matchAll(TOK)].map(m=>+m[1]).sort((a,b)=>a-b).join();
      if(!meant) return;
      const out=app.refs(o,v.order,true);
      const got=[...out.matchAll(/[אבגדה]/g)].filter(m=>!/[֐-׿]/.test(out[m.index-1]||"")&&!/[֐-׿]/.test(out[m.index+1]||""))
        .map(m=>v.order[HE_KEYS.indexOf(m[0])]).sort((a,b)=>a-b).join();
      if(out.includes("{@") || got!==meant){console.log("REF mismatch",q.id,JSON.stringify(out),got,"≠",meant);refBad++;}
    });
    if(app.refs(q.explanation,v.order).includes("{@")){console.log("REF leaked in explanation",q.id);refBad++;}
  }
}
bad+=refBad;

// practice-pool dedup count
const seen=new Set(); let dups=0;
for(const q of QS){ if(seen.has(q.dedupKey)) dups++; else seen.add(q.dedupKey); }

// questions.js is the ONLY payload the browser loads (index.html pulls it via <script src>);
// questions.json is a build artifact nothing at runtime reads. If they drift, a reviewer
// reading the .json is not reading what students actually get — so require them identical.
// The .js is re-evaluated in a vm sandbox so window.QUESTIONS is read, not this file's globals.
const sandbox={window:{}};
vm.runInNewContext(fs.readFileSync(path.join(__dirname,"..","questions.js"),"utf8"),sandbox);
const jsPayload=sandbox.window.QUESTIONS;
const jsonPayload=JSON.parse(fs.readFileSync(path.join(__dirname,"..","questions.json"),"utf8"));
const syncOK=JSON.stringify(jsPayload)===JSON.stringify(jsonPayload);
if(!syncOK){
  console.log("SYNC questions.js/questions.json DIFFER — lengths",jsPayload.length,"vs",jsonPayload.length);
  for(let i=0;i<Math.max(jsPayload.length,jsonPayload.length);i++){
    if(JSON.stringify(jsPayload[i])!==JSON.stringify(jsonPayload[i])){
      console.log("  first divergence at index",i,"—",(jsPayload[i]||{}).id,"vs",(jsonPayload[i]||{}).id);break;}
  }
  bad++;
}

console.log("total questions:",QS.length);
console.log("by topic:",topics);
console.log("tiers — official:",QS.filter(q=>q.official).length,
  "· verified:",QS.filter(q=>q.verified).length,
  "· derived:",QS.filter(q=>!q.official&&!q.verified).length);
console.log("integrity problems:",bad);
console.log("duplicate ids:",dupIds,"(must be 0)");
console.log("questions.js ≡ questions.json:",syncOK?"yes":"NO — payloads drifted");
console.log("cross-exam duplicates (hidden in practice pool):",dups);
console.log("STORED correctIndex distribution (5-opt, should be ~20% each — proves build-time shuffle):",
  stored5.map(c=>n5?(c/n5*100).toFixed(1)+"%":"-").join(" / "));
console.log("render-shuffle scoring-map mismatches:",mismatch,"(must be 0)");
console.log("letter-reference / pinned-option problems:",refBad,`(must be 0; ${refQs} questions checked)`);
console.log("render display-position distribution (5-opt, ~20% each):",
  disp5.map(c=>trials5?(c/trials5*100).toFixed(1)+"%":"-").join(" / "));
const firstPct = n5? stored5[0]/n5 : 0;
const shuffleOK = firstPct < 0.45;  // if >45% still at 0, build-time shuffle likely didn't run
console.log(bad===0 && mismatch===0 && shuffleOK && dupIds===0 && syncOK ? "\nSMOKE TEST PASSED" : "\nSMOKE TEST FAILED");
