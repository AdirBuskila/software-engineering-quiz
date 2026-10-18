// End-to-end check of the guided courses in a real (headless) browser, from file://.
// usage: node tools/course_flow.js [pat|uml|tst|proc|all] [light|dark] [mobile]
// For every level: map -> lesson -> answer every question (every 3rd one wrong) -> summary.
// Fails on page errors, horizontal overflow, a summary score that disagrees with the answers
// given, or a bank-stats write (courses keep their own score). Screenshots go to tools/raw/courseflow/.
// Chrome: $CHROME, else the Windows install.
const puppeteer = require("puppeteer-core");
const path = require("path"), fs = require("fs"), url = require("url");
const CHROME = process.env.CHROME || process.env.CHROME_PATH || ["C:/Program Files/Google/Chrome/Application/chrome.exe",
  "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"].find(p => fs.existsSync(p));
const OUT = path.join(__dirname, "raw", "courseflow"); fs.mkdirSync(OUT, { recursive: true });
const [which = "all", theme = "light", mob] = process.argv.slice(2);
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: "new", args: ["--no-sandbox", "--hide-scrollbars", "--allow-file-access-from-files"] });
  const page = await browser.newPage();
  const errs = [];
  page.on("pageerror", e => errs.push("PAGEERROR " + e.message));
  page.on("console", m => { if (m.type() === "error" && !/Failed to load resource|goatcounter|gc\.zgo/.test(m.text())) errs.push(m.text()); });
  await page.setViewport(mob ? { width: 390, height: 844, deviceScaleFactor: 2, isMobile: true } : { width: 1100, height: 900, deviceScaleFactor: 1 });
  await page.evaluateOnNewDocument(t => { try { localStorage.clear(); localStorage.setItem("seq_theme", t); } catch (e) {} }, theme);
  await page.goto(url.pathToFileURL(path.join(__dirname, "..", "index.html")).href, { waitUntil: "load" });
  const tagBase = `${theme}${mob ? "-m" : ""}`;
  const shot = async n => { await sleep(200); await page.screenshot({ path: path.join(OUT, `${n}-${tagBase}.png`), fullPage: true }); };
  const overflow = async where => { if (await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1)) errs.push("horizontal overflow at " + where); };
  await shot("0-start"); await overflow("start");
  const courses = which === "all" ? ["pat", "uml", "tst", "proc"] : [which];
  const report = [];
  for (const c of courses) {
    const levels = await page.evaluate(c => (window.COURSES[c] || { levels: [] }).levels.map(L => L.id), c);
    for (const lvl of levels) {
      await page.evaluate(() => quit());
      await page.click(`.crs-promo[data-course="${c}"]`);
      if (lvl === levels[0]) { await shot(`${c}-1-map`); await overflow(`${c} map`); }
      await page.click(`.crs-lvl[data-id="${lvl}"]`);
      await shot(`${c}-${lvl}-lesson`); await overflow(`${c}/${lvl} lesson`);
      await page.click("#crsLessonGo");
      const n = await page.evaluate(() => S.pool.length);
      let right = 0;
      for (let i = 0; i < n; i++) {
        await sleep(40);
        const wrong = i % 3 === 2;
        const disp = await page.evaluate(w => { const v = S.current; return w ? (v.correctDisplay + 1) % v.order.length : v.correctDisplay; }, wrong);
        if (!wrong) right++;
        await page.click(`.opt[data-disp="${disp}"]`);
        await overflow(`${c}/${lvl} q${i + 1}`);
        if (i === 0) await shot(`${c}-${lvl}-q1`);
        await page.click("#nextBtn");
      }
      const pct = await page.evaluate(() => document.querySelector("#crsSum .big").textContent);
      if (pct !== Math.round(right / n * 100) + "%") errs.push(`${c}/${lvl}: summary ${pct}, expected ${Math.round(right / n * 100)}%`);
      if (lvl === levels[0]) await shot(`${c}-${lvl}-summary`);
      report.push(`${c}/${lvl}: ${n} q, ${pct}`);
    }
  }
  const mainStats = await page.evaluate(() => JSON.parse(localStorage.getItem("seq_progress_v1") || "null"));
  if (mainStats && mainStats.stats && mainStats.stats.answered) errs.push("course answers leaked into the bank stats");
  // the hand-off to real exam questions starts a practice session on the course's topics
  if (report.length) {
    const c = courses[courses.length - 1];
    await page.evaluate(() => document.querySelector('#crsSum [data-act="real"], #crsSum [data-act="map"]').click());
    const st = await page.evaluate(() => ({ mode: S.mode, n: S.pool.length, topics: [...new Set(S.pool.map(q => q.topic))] }));
    report.push(`hand-off/map after ${c}: ${JSON.stringify(st)}`);
  }
  console.log(report.join("\n"));
  console.log(errs.length ? "\nERRORS:\n" + errs.join("\n") : "\nCOURSE FLOW PASSED");
  await browser.close();
  process.exit(errs.length ? 1 : 0);
})();
