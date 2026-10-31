// Screenshots of a composed video at given times, without rendering (fast visual check before a render).
// usage: node preview.js <index.html> '<json array of seconds>' <out dir>      (NODE_PATH -> the app's node_modules)
// Same clip logic as layout_lint.js: only the scenes/subtitles live at each time are shown, the GSAP timeline is
// sought. (`hyperframes snapshot` sometimes mirrored Hebrew glyphs; plain Chrome does not.)
const puppeteer = require("puppeteer-core");
const path = require("path");
const CHROME = process.env.CHROME || "C:/Program Files/Google/Chrome/Application/chrome.exe";

(async () => {
  const [file, timesJson, outDir] = process.argv.slice(2);
  const times = JSON.parse(timesJson);
  const b = await puppeteer.launch({ executablePath: CHROME, headless: "new", args: ["--allow-file-access-from-files"] });
  const p = await b.newPage();
  await p.setViewport({ width: 1920, height: 1080 });
  await p.goto("file:///" + file.replace(/\\/g, "/"), { waitUntil: "load" });
  await p.evaluate(() => document.fonts && document.fonts.ready);
  for (const t of times) {
    await p.evaluate((t) => {
      document.querySelectorAll(".clip").forEach(c => {
        const s = +c.dataset.start, d = +c.dataset.duration;
        c.style.display = (t >= s && t < s + d) ? "" : "none";
      });
      window.__timelines.root.seek(t);
    }, t);
    const f = path.join(outDir, `t${t.toFixed(1).padStart(6, "0")}.png`);
    await p.screenshot({ path: f });
    console.log(f);
  }
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
