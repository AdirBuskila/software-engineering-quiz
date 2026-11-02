// Drive the app in real Chrome (headless) and capture screenshots + assertions.
const puppeteer=require("puppeteer-core");
const path=require("path");
const CHROME=process.env.CHROME_PATH||"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const URL="file:///"+path.join(__dirname,"..","index.html").replace(/\\/g,"/");
const SHOT=p=>path.join(__dirname,"raw",p);

(async()=>{
  const b=await puppeteer.launch({executablePath:CHROME,headless:"new",args:["--allow-file-access-from-files","--no-sandbox"]});
  const pg=await b.newPage();
  await pg.setViewport({width:900,height:1300,deviceScaleFactor:1});
  const errs=[]; pg.on("pageerror",e=>errs.push(String(e))); pg.on("console",m=>{if(m.type()==="error")errs.push("console:"+m.text());});
  pg.on("dialog",d=>d.accept());
  await pg.goto(URL,{waitUntil:"networkidle0"});

  // ---- video course ("🎬 קורס וידאו": videos.js + video-ui.js), on its own page so it does not depend on the flows below:
  //      list -> player -> prev/next -> watched -> guided lesson -> lesson button -> back -> home; then ?video=<ID> ----
  const vid=[]; const vok=(c,m)=>{vid.push([!!c,m]);};
  {
    const errsV=[];
    const newVidPage=async()=>{
      const p=await b.newPage(); await p.setViewport({width:900,height:1300,deviceScaleFactor:1});
      p.on("pageerror",e=>errsV.push(String(e))); p.on("console",m=>{if(m.type()==="error")errsV.push("console:"+m.text());});
      // the analytics tag is protocol-relative: from file:// it is a missing file, so stub it
      await p.setRequestInterception(true);
      p.on("request",r=>/gc\.zgo\.at/.test(r.url())?r.respond({status:200,contentType:"text/javascript",body:""}):r.continue());
      return p;
    };
    const pv=await newVidPage();
    await pv.goto(URL,{waitUntil:"networkidle0"});
    const shown=s=>pv.$eval(s,e=>!e.classList.contains("hidden")&&!e.closest(".screen").classList.contains("hidden"));
    const VA=await pv.evaluate(()=>{const C=window.COURSES||{};return (window.VIDEO_UI&&window.VIDEO_UI.all||[]).map(v=>({id:v.id,ok:((C[v.course.id]||{}).levels||[]).some(L=>L.id===v.level)}));});
    vok(VA.length>1&&VA.every(v=>v.ok),`every one of ${VA.length} videos maps to a guided level of its course`);
    await pv.click("#vidEntry");
    vok(await shown("#vidListView"),"header entry opens the video list");
    vok(await pv.$$eval("#vidCourses .vid-row",r=>r.length)===VA.length,`list shows ${VA.length} videos`);
    await pv.click(`.vid-row[data-vid="${VA[0].id}"]`);
    vok(await shown("#vidPlayView")&&!!(await pv.$("#vidFrame video, #vidFrame iframe, #vidFrame .vid-missing")),`${VA[0].id}: player opens with media (or the 'not uploaded yet' note)`);
    vok(await pv.$eval("#vidPrev",x=>x.disabled)&&!(await pv.$eval("#vidNext",x=>x.disabled)),"first video: prev disabled, next enabled");
    await pv.click("#vidNext");
    vok((await pv.$eval("#vidHead",e=>e.textContent)).includes(VA[1].id),`next -> ${VA[1].id}`);
    await pv.click("#vidPrev");
    vok((await pv.$eval("#vidHead",e=>e.textContent)).includes(VA[0].id),`prev -> ${VA[0].id}`);
    await pv.click("#vidNext"); await pv.click("#vidWatchBtn");
    vok(await pv.evaluate((k,id)=>{try{return !!JSON.parse(localStorage.getItem(k)).watched[id];}catch(e){return false;}},"seq_video_v1",VA[1].id),`watched mark saved in ${"seq_video_v1"}`);
    await pv.click("#vidLevel");
    vok(await shown("#crsLessonView"),`${VA[1].id} -> practice opens its guided lesson`);
    const vlb=await pv.$$eval("#crsLesson .vid-open",bs=>bs.map(x=>x.dataset.vid));
    vok(vlb.length===1&&vlb[0]===VA[1].id,`lesson shows its video button (${vlb.join()})`);
    await pv.click("#crsLesson .vid-open");
    vok(await shown("#vidPlayView")&&(await pv.$eval("#vidBack",e=>e.textContent)).includes("לשיעור"),"lesson button opens the player");
    await pv.click("#vidBack");
    vok(await shown("#crsLessonView"),"back from the player returns to the lesson");
    await pv.evaluate(id=>window.VIDEO_UI.openVideo(id),VA[0].id); await pv.click("#brandHome");
    vok(await shown("#screen-start .vid-promo")&&await pv.$eval("#screen-video",e=>e.classList.contains("hidden"))&&!(await pv.$("#vidFrame video, #vidFrame iframe")),"brand click from the player goes home and stops playback");
    vok((await pv.$eval("#vidPromoSub",e=>e.textContent)).includes("צפית ב-1 "),"home promo shows the watched count");
    await pv.close();
    const vlast=VA[VA.length-1].id, pd=await newVidPage();
    await pd.goto(URL+"?video="+vlast,{waitUntil:"networkidle0"});
    vok(await pd.$eval("#vidPlayView",e=>!e.classList.contains("hidden")&&!e.closest(".screen").classList.contains("hidden"))&&(await pd.$eval("#vidHead",e=>e.textContent)).includes(vlast),`?video=${vlast} deep link opens the player`);
    await pd.close();
    vok(!errsV.length,"video: no page/console errors"+(errsV.length?": "+errsV.join(" | "):""));
  }
  const vidOk=vid.every(([c])=>c);

  const poolInfo=await pg.$eval("#poolInfo",e=>e.textContent);
  const topStats=await pg.$eval("#topStats",e=>e.textContent.replace(/\s+/g," ").trim());
  await pg.screenshot({path:SHOT("shot1-start.png")});

  // ---- practice: start, answer correctly, check feedback ----
  await pg.click("#startBtn");
  await pg.waitForSelector(".opt");
  const q1=await pg.$eval("#questionText",e=>e.textContent.slice(0,40));
  const correctDisp=await pg.evaluate(()=>S.current.correctDisplay);
  await pg.screenshot({path:SHOT("shot2-question.png")});
  await pg.click(`.opt[data-disp="${correctDisp}"]`);
  await pg.waitForSelector("#feedback:not(.hidden)");
  const verdict=await pg.$eval("#feedback .verdict",e=>e.textContent);
  const fbGood=await pg.$eval("#feedback",e=>e.className.includes("good"));
  await pg.screenshot({path:SHOT("shot3-feedback.png")});

  // answer wrong on next to confirm wrong path
  await pg.click("#nextBtn"); await pg.waitForSelector(".opt:not([disabled])");
  const cd2=await pg.evaluate(()=>S.current.correctDisplay);
  const wrong=(cd2+1)%(await pg.$$eval(".opt",els=>els.length));
  await pg.click(`.opt[data-disp="${wrong}"]`);
  await pg.waitForSelector("#feedback:not(.hidden)");
  const fbBad=await pg.$eval("#feedback",e=>e.className.includes("bad"));

  // ---- exam mode ----
  await pg.click("#quitBtn");
  await pg.waitForSelector("#screen-start:not(.hidden)");
  await pg.click('input[name=mode][value=exam]');
  await pg.click("#startBtn");
  await pg.waitForSelector(".opt");
  const hasTimer=await pg.$eval("#quizMeta",e=>/\d+:\d\d/.test(e.textContent));
  const examLen=await pg.evaluate(()=>S.pool.length);
  await pg.screenshot({path:SHOT("shot4-exam.png")});
  const n=await pg.evaluate(()=>S.pool.length);
  for(let i=0;i<n;i++){
    await pg.click('.opt[data-disp="0"]');
    if(i<n-1){ await pg.click("#nextBtn"); await pg.waitForSelector(".opt"); }
  }
  // the button un-hides on the last question; wait until it can take a click (was flaky)
  await pg.waitForSelector("#submitExamBtn",{visible:true});
  await pg.click("#submitExamBtn");
  await new Promise(r=>setTimeout(r,400));
  const onResults=await pg.$eval("#screen-results",e=>!e.classList.contains("hidden")).catch(()=>false);

  console.log("topStats:",topStats);
  console.log("poolInfo:",poolInfo);
  console.log("Q1:",q1);
  console.log("practice correct->good:",fbGood,"| verdict:",verdict.trim());
  console.log("practice wrong->bad:",fbBad);
  console.log("exam timer shown:",hasTimer,"| exam length:",examLen);
  console.log("reached results screen:",onResults);
  vid.forEach(([c,m])=>console.log((c?"video ok:  ":"video FAIL: ")+m));
  console.log("page errors:",errs.length?errs:"none");
  await b.close();
  console.log((fbGood&&fbBad&&hasTimer&&onResults&&vidOk&&!errs.length)?"\nUI VERIFY PASSED":"\nUI VERIFY: CHECK ABOVE");
})().catch(e=>{console.error("FATAL",e);process.exit(1)});
