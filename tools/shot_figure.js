// Drive the app to a question that has an attached figure and screenshot it.
const puppeteer=require("puppeteer-core");
const path=require("path");
const CHROME=process.env.CHROME_PATH||"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const URL="file:///"+path.join(__dirname,"..","index.html").replace(/\\/g,"/");
(async()=>{
  const b=await puppeteer.launch({executablePath:CHROME,headless:"new",args:["--allow-file-access-from-files","--no-sandbox"]});
  const pg=await b.newPage();
  await pg.setViewport({width:900,height:1300,deviceScaleFactor:1});
  await pg.goto(URL,{waitUntil:"networkidle0"});
  // jump straight into a practice session over the "config" topic (has version-control figures)
  await pg.evaluate(()=>{ S.mode="practice"; S.topic="config"; startSession(); });
  await pg.waitForSelector(".opt");
  // advance until a question with a figure image shows up (answer each to enable Next)
  let found=false;
  for(let i=0;i<40 && !found;i++){
    found=await pg.$eval("#qExtras", e=>!!e.querySelector("img.q-img")).catch(()=>false);
    if(found) break;
    const cd=await pg.evaluate(()=>S.current.correctDisplay);
    await pg.click(`.opt[data-disp="${cd}"]`);
    await pg.waitForSelector("#feedback:not(.hidden)");
    await pg.click("#nextBtn");
    await pg.waitForSelector(".opt:not([disabled])");
  }
  // wait for the figure to actually load
  if(found){ await pg.waitForFunction(()=>{const im=document.querySelector("#qExtras img.q-img"); return im&&im.complete&&im.naturalWidth>0;},{timeout:6000}); }
  await pg.screenshot({path:path.join(__dirname,"raw","shot-figure-question.png")});
  const src=await pg.$eval("#qExtras img.q-img", e=>e.getAttribute("src")).catch(()=>"(none)");
  console.log("figure question found:",found,"| img src:",src);
  await b.close();
})().catch(e=>{console.error(e);process.exit(1);});
