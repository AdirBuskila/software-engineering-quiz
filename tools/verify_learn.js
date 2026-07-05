// Drive the learning section in real Chrome (headless) and assert it works.
const puppeteer = require("puppeteer-core");
const path = require("path");
const CHROME = process.env.CHROME_PATH || "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const URL = "file:///" + path.join(__dirname, "..", "index.html").replace(/\\/g, "/");
const SHOT = p => path.join(__dirname, "raw", p);

function assert(cond, msg){ if(!cond){ console.error("ASSERT FAILED:", msg); process.exitCode = 1; throw new Error(msg); } }

(async () => {
  const b = await puppeteer.launch({ executablePath: CHROME, headless: "new",
    args: ["--allow-file-access-from-files", "--no-sandbox"] });
  const pg = await b.newPage();
  await pg.setViewport({ width: 1100, height: 1400, deviceScaleFactor: 1 });
  const errs = [];
  pg.on("pageerror", e => errs.push(String(e)));
  pg.on("console", m => { if (m.type() === "error") errs.push("console:" + m.text()); });
  await pg.goto(URL, { waitUntil: "networkidle0" });

  // enter learn mode
  await pg.click("#learnEntry");
  await pg.waitForSelector("#screen-learn:not(.hidden)");
  await pg.waitForSelector("#learnToc button");

  const tocCount = await pg.$$eval("#learnToc button", els => els.length);
  assert(tocCount >= 5, "expected several chapters in TOC, got " + tocCount);

  const firstTitle = await pg.$eval(".learn-h", e => e.textContent.trim());
  assert(firstTitle.length > 0, "first chapter has a title");
  await pg.screenshot({ path: SHOT("learn-intro.png") });

  // find a chapter that renders a <table> (design-patterns / cheat sheet)
  let foundTable = false;
  for (let i = 0; i < tocCount; i++) {
    await pg.evaluate(i => document.querySelectorAll("#learnToc button")[i].click(), i);
    const hasTable = await pg.$eval(".learn-content", e => !!e.querySelector("table"));
    if (hasTable) { foundTable = true; await pg.screenshot({ path: SHOT("learn-table.png") }); break; }
  }
  assert(foundTable, "at least one chapter renders a table");

  // find a chapter that renders a <pre><code> block (JUnit / Singleton)
  let foundCode = false;
  for (let i = 0; i < tocCount; i++) {
    await pg.evaluate(i => document.querySelectorAll("#learnToc button")[i].click(), i);
    const hasCode = await pg.$eval(".learn-content", e => !!e.querySelector("pre code"));
    if (hasCode) { foundCode = true; break; }
  }
  assert(foundCode, "at least one chapter renders a code block");

  // prev/next navigation
  await pg.evaluate(() => document.querySelectorAll("#learnToc button")[0].click());
  const posBefore = await pg.$eval("#learnPos", e => e.textContent.trim());
  await pg.click("#learnNext");
  const posAfter = await pg.$eval("#learnPos", e => e.textContent.trim());
  assert(posBefore !== posAfter, "next button advances chapter");

  // back to home
  await pg.click("#learnBackBtn");
  await pg.waitForSelector("#screen-start:not(.hidden)");

  // light theme screenshot for visual review
  await pg.evaluate(() => { document.documentElement.dataset.theme = "light"; });
  await pg.click("#learnEntry");
  await pg.waitForSelector("#screen-learn:not(.hidden)");
  await pg.screenshot({ path: SHOT("learn-light.png") });
  await pg.evaluate(() => { document.documentElement.dataset.theme = "dark"; });

  // ---- mobile: chapter list is an in-flow dropdown, hidden when closed ----
  await pg.setViewport({ width: 390, height: 780, deviceScaleFactor: 2 });
  await pg.reload({ waitUntil: "networkidle0" });
  await pg.click("#learnEntry");
  await pg.waitForSelector("#screen-learn:not(.hidden)");

  const noOverflow = async () => pg.evaluate(() => ({
    sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth }));
  const tocDisplay = () => pg.$eval("#learnToc", el => getComputedStyle(el).display);

  assert(await tocDisplay() === "none", "chapter list hidden (display:none) when closed");
  let ov = await noOverflow();
  assert(ov.sw <= ov.cw + 1, "no horizontal overflow when closed (sw=" + ov.sw + " cw=" + ov.cw + ")");
  await pg.screenshot({ path: SHOT("learn-mobile-closed.png") });

  await pg.click("#learnTocToggle");
  await new Promise(r => setTimeout(r, 200));
  assert(await tocDisplay() !== "none", "chapter list shown on toggle");
  ov = await noOverflow();
  assert(ov.sw <= ov.cw + 1, "no horizontal overflow when open");

  // selecting a chapter closes it, and content fits the viewport width
  await pg.evaluate(() => document.querySelector("#learnToc button").click());
  await new Promise(r => setTimeout(r, 200));
  assert(await tocDisplay() === "none", "picking a chapter closes the dropdown");
  ov = await noOverflow();
  assert(ov.sw <= ov.cw + 1, "no horizontal overflow after navigating");
  const cw = await pg.$eval("#learnContent", e => e.getBoundingClientRect().width);
  assert(cw <= 391, "content fits viewport width (got " + Math.round(cw) + "px)");
  await pg.screenshot({ path: SHOT("learn-mobile-content.png") });

  console.log("TOC chapters   :", tocCount);
  console.log("renders table  :", foundTable, "| renders code:", foundCode);
  console.log("nav pos        :", posBefore, "->", posAfter);
  console.log("mobile TOC     : in-flow dropdown, display:none when closed, no x-overflow");
  console.log("page errors    :", errs.length ? errs.join("\n") : "none");
  await b.close();
  assert(errs.length === 0, "no page/console errors");
  console.log("\nLEARN VERIFY PASSED");
})().catch(e => { console.error(e); process.exit(1); });
