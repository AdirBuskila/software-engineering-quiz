// Drive the app to a "verified" (מאומת) question and screenshot the badge.
const puppeteer=require("puppeteer-core");
const path=require("path");
const CHROME=process.env.CHROME_PATH||"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const URL="file:///"+path.join(__dirname,"..","index.html").replace(/\\/g,"/");
(async()=>{
  const b=await puppeteer.launch({executablePath:CHROME,headless:"new",args:["--allow-file-access-from-files","--no-sandbox"]});
  const pg=await b.newPage();
  await pg.setViewport({width:900,height:1250,deviceScaleFactor:1});
  await pg.goto(URL,{waitUntil:"networkidle0"});
  await pg.evaluate(()=>{ S.mode="practice"; S.topic="all"; startSession(); });
  await pg.waitForSelector(".opt");
  let seen={};
  for(let i=0;i<120;i++){
    const t=await pg.$eval("#qBadge", e=>e.textContent.trim());
    if(!seen[t]){ seen[t]=true; }
    if(t.includes("מאומת")){                       // found a verified badge
      await pg.screenshot({path:path.join(__dirname,"raw","shot-verified-badge.png")});
      const cls=await pg.$eval("#qBadge", e=>e.className);
      console.log("VERIFIED badge shown. text=",JSON.stringify(t)," class=",cls);
      break;
    }
    const cd=await pg.evaluate(()=>S.current.correctDisplay);
    await pg.click(`.opt[data-disp="${cd}"]`);
    await pg.waitForSelector("#feedback:not(.hidden)");
    await pg.click("#nextBtn");
    await pg.waitForSelector(".opt:not([disabled])");
  }
  console.log("distinct badges seen while stepping:", Object.keys(seen));
  await b.close();
})().catch(e=>{console.error(e);process.exit(1);});
