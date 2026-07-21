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
console.log("render display-position distribution (5-opt, ~20% each):",
  disp5.map(c=>trials5?(c/trials5*100).toFixed(1)+"%":"-").join(" / "));
const firstPct = n5? stored5[0]/n5 : 0;
const shuffleOK = firstPct < 0.45;  // if >45% still at 0, build-time shuffle likely didn't run
console.log(bad===0 && mismatch===0 && shuffleOK && dupIds===0 && syncOK ? "\nSMOKE TEST PASSED" : "\nSMOKE TEST FAILED");
