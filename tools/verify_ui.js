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
  console.log("page errors:",errs.length?errs:"none");
  await b.close();
  console.log((fbGood&&fbBad&&hasTimer&&onResults&&!errs.length)?"\nUI VERIFY PASSED":"\nUI VERIFY: CHECK ABOVE");
})().catch(e=>{console.error("FATAL",e);process.exit(1)});
