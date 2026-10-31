// Layout lint for a composed video (videos/out/<ID>/proj/index.html), run before rendering.
// usage: node layout_lint.js <index.html> '<json array of times in seconds>'   (NODE_PATH -> the app's node_modules)
// At each time: show only the clips (scenes, subtitles) live at that moment (HyperFrames does this at render time),
// seek the GSAP timeline, then check the visible boxes of the live scene:
//   out-of-area  a box that leaves its .stage / .panel
//   subtitle     a stage/panel box that runs into the subtitle box
//   presenter    a box that runs into Shosh
//   overlap      two visible boxes (neither inside the other) overlapping by more than a third of the smaller one
//   overflow     an element whose content is wider than itself (text cut)
//   squeezed     a .swap slot (or its layer) whose content is taller than the slot
// Prints a JSON array of findings {i, t, kind, what}.
const puppeteer = require("puppeteer-core");
const CHROME = process.env.CHROME || "C:/Program Files/Google/Chrome/Application/chrome.exe";

(async () => {
  const [file, timesJson] = process.argv.slice(2);
  const times = JSON.parse(timesJson);
  const b = await puppeteer.launch({ executablePath: CHROME, headless: "new", args: ["--allow-file-access-from-files"] });
  const p = await b.newPage();
  await p.setViewport({ width: 1920, height: 1080 });
  await p.goto("file:///" + file.replace(/\\/g, "/"), { waitUntil: "load" });
  await p.evaluate(() => document.fonts && document.fonts.ready);
  const found = [];
  for (let i = 0; i < times.length; i++) {
    const t = times[i];
    const res = await p.evaluate((t) => {
      const out = [];
      document.querySelectorAll(".clip").forEach(c => {
        const s = +c.dataset.start, d = +c.dataset.duration;
        c.style.display = (t >= s && t < s + d) ? "" : "none";
      });
      window.__timelines.root.seek(t);
      const vis = el => {
        let o = 1;
        for (let e = el; e && e.nodeType === 1; e = e.parentElement) {
          const cs = getComputedStyle(e);
          if (cs.display === "none" || cs.visibility === "hidden") return false;
          o *= parseFloat(cs.opacity);
        }
        return o > 0.5;
      };
      const R = el => el.getBoundingClientRect();
      const inter = (a, b) => Math.max(0, Math.min(a.right, b.right) - Math.max(a.left, b.left)) *
                              Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top));
      const area = r => r.width * r.height;
      const name = el => (el.id ? "#" + el.id : el.tagName.toLowerCase() + (el.className && el.className.baseVal === undefined
                          ? "." + String(el.className).split(" ")[0] : "")) + " " + (el.textContent || "").trim().slice(0, 40);
      const sub = [...document.querySelectorAll(".sub")].find(s => s.style.display !== "none");
      const subBox = sub && sub.querySelector("span") ? R(sub.querySelector("span")) : null;
      const shosh = document.querySelector("#shosh svg"), shBox = shosh ? R(shosh) : null;
      const scene = [...document.querySelectorAll("section.scene")].find(s => s.style.display !== "none");
      if (!scene) return out;
      for (const area_ of scene.querySelectorAll(".stage, .panel, .titlecard")) {
        const A = R(area_);
        // atomic boxes: svg / math / img / elements without element children / cards, chips, verdicts
        const atoms = [...area_.querySelectorAll("*")].filter(el => {
          if (el.closest("svg") && el.tagName.toLowerCase() !== "svg") return false;
          if (el.closest("math") && el.tagName.toLowerCase() !== "math") return false;
          const tag = el.tagName.toLowerCase();
          if (!["svg", "math", "img"].includes(tag) && el.children.length && !/card|chip|verdict|cell/.test(el.className)) return false;
          const r = R(el);
          return r.width > 2 && r.height > 2 && vis(el);
        });
        const pos = el => getComputedStyle(el).position;
        const overlay = el => pos(el) === "absolute" || pos(el) === "fixed";   // markers, strikes, rings: drawn over others on purpose
        for (const el of atoms) {
          const r = R(el);
          if (!overlay(el) && (r.left < A.left - 3 || r.right > A.right + 3 || r.top < A.top - 3 || r.bottom > A.bottom + 3))
            out.push({ kind: "out-of-area", what: name(el) });
          if (subBox && inter(r, subBox) > 4) out.push({ kind: "subtitle", what: name(el) });
          if (shBox && inter(r, shBox) > 4) out.push({ kind: "presenter", what: name(el) });
          if (el.scrollWidth > el.clientWidth + 2 && getComputedStyle(el).overflow !== "visible" && el.clientWidth)
            out.push({ kind: "overflow", what: name(el) });
        }
        // a fixed-height slot (.swap) or its layer whose content is taller than the box: flex squeezes it onto its neighbours
        for (const el of area_.querySelectorAll(".swap, .swap > div"))
          if (vis(el) && el.scrollHeight > el.clientHeight + 4)
            out.push({ kind: "squeezed", what: `${el.scrollHeight - el.clientHeight}px ` + name(el) });
        for (let a = 0; a < atoms.length; a++)
          for (let c = a + 1; c < atoms.length; c++) {
            const x = atoms[a], y = atoms[c];
            if (x.contains(y) || y.contains(x) || overlay(x) || overlay(y)) continue;
            const ov = inter(R(x), R(y));
            if (ov > Math.min(area(R(x)), area(R(y))) / 3) out.push({ kind: "overlap", what: name(x) + " × " + name(y) });
          }
      }
      return out;
    }, t);
    const seen = new Set();
    for (const f of res) {
      const k = f.kind + f.what;
      if (!seen.has(k)) { seen.add(k); found.push({ i, t, ...f }); }
    }
  }
  // the same finding at consecutive phrase ends is one problem: keep its first occurrence
  const first = new Map();
  for (const f of found) if (!first.has(f.kind + f.what)) first.set(f.kind + f.what, f);
  process.stdout.write(JSON.stringify([...first.values()]));
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
