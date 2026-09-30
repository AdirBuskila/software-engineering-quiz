// render_study.js — build-time helpers for build_learn.py (headless Chrome).
//
//   node render_study.js mermaid <in.json> <out.json>
//       in:  ["flowchart LR ...", ...]   out: ["<svg ...>", ...]
//   node render_study.js pdf <in.html> <out.pdf>
//
// Mermaid is rendered once at build time so the site stays static/offline.
const puppeteer = require("puppeteer-core");
const fs = require("fs");
const path = require("path");
const CHROME = process.env.CHROME_PATH || "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const MERMAID = path.join(__dirname, "node_modules", "mermaid", "dist", "mermaid.min.js");

async function renderMermaid(b, inFile, outFile){
  const sources = JSON.parse(fs.readFileSync(inFile, "utf8"));
  const pg = await b.newPage();
  await pg.setContent("<!doctype html><html><body></body></html>");
  await pg.addScriptTag({ path: MERMAID });
  const svgs = await pg.evaluate(async (sources) => {
    mermaid.initialize({ startOnLoad: false, theme: "neutral", securityLevel: "strict",
                         fontFamily: "Segoe UI, Arial, sans-serif" });
    const out = [];
    for (let i = 0; i < sources.length; i++) {
      const { svg } = await mermaid.render("mmd" + i, sources[i]);
      out.push(svg);
    }
    return out;
  }, sources);
  fs.writeFileSync(outFile, JSON.stringify(svgs), "utf8");
  console.log(`mermaid    : rendered ${svgs.length} diagram(s)`);
}

async function renderPdf(b, inFile, outFile){
  const pg = await b.newPage();
  await pg.goto("file:///" + path.resolve(inFile).replace(/\\/g, "/"), { waitUntil: "networkidle0" });
  await pg.pdf({ path: outFile, format: "A4", printBackground: true,
                 margin: { top: "16mm", bottom: "16mm", left: "14mm", right: "14mm" } });
  console.log(`pdf        : ${outFile}`);
}

(async () => {
  const [cmd, a, c] = process.argv.slice(2);
  const b = await puppeteer.launch({ executablePath: CHROME, headless: "new",
    args: ["--allow-file-access-from-files", "--no-sandbox"] });
  try {
    if (cmd === "mermaid") await renderMermaid(b, a, c);
    else if (cmd === "pdf") await renderPdf(b, a, c);
    else throw new Error("usage: render_study.js mermaid|pdf <in> <out>");
  } finally { await b.close(); }
})().catch(e => { console.error(e); process.exit(1); });
