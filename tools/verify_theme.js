// Verify the theme toggle: glyph, data-theme attribute, localStorage persistence.
const puppeteer=require("puppeteer-core");
const path=require("path");
const CHROME=process.env.CHROME_PATH||"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const URL="file:///"+path.join(__dirname,"..","index.html").replace(/\\/g,"/");
const SHOT=p=>path.join(__dirname,"raw",p);

(async()=>{
  const b=await puppeteer.launch({executablePath:CHROME,headless:"new",args:["--allow-file-access-from-files","--no-sandbox"]});
  const pg=await b.newPage();
  await pg.setViewport({width:900,height:1300,deviceScaleFactor:1});
  const errs=[]; pg.on("pageerror",e=>errs.push(String(e)));
  pg.on("console",m=>{if(m.type()==="error")errs.push("console:"+m.text());});
  await pg.goto(URL,{waitUntil:"networkidle0"});

  const before = await pg.evaluate(()=>({
    theme: document.documentElement.dataset.theme || "(auto)",
    glyph: document.getElementById("themeToggle").textContent.trim(),
  }));
  await pg.screenshot({path:SHOT("theme-initial.png")});

  await pg.click("#themeToggle");
  const afterToggle = await pg.evaluate(()=>({
    theme: document.documentElement.dataset.theme,
    glyph: document.getElementById("themeToggle").textContent.trim(),
    stored: localStorage.getItem("seq_theme"),
  }));
  await pg.screenshot({path:SHOT("theme-toggled.png")});

  await pg.reload({waitUntil:"networkidle0"});
  const afterReload = await pg.evaluate(()=>document.documentElement.dataset.theme);

  await pg.click("#startBtn");
  await pg.waitForSelector(".opt");
  await pg.screenshot({path:SHOT("theme-question.png")});

  console.log("initial:", JSON.stringify(before));
  console.log("after toggle:", JSON.stringify(afterToggle));
  console.log("after reload theme:", afterReload);
  console.log("persisted across reload:", afterReload===afterToggle.theme);
  console.log("page errors:", errs.length?errs.join("\n"):"none");
  await b.close();
  if(errs.length || afterReload!==afterToggle.theme){ process.exit(1); }
  console.log("\nTHEME VERIFY PASSED");
})().catch(e=>{console.error(e);process.exit(1);});
