"use strict";
/* navurl.js — keep the address bar in step with the open screen, so a refresh (or a copied link) lands back
   on the same video / lesson / chapter / drill, and the browser's back/forward buttons step between screens.
   Shared verbatim by every quiz app (copy it, don't fork it).

   navUrl(null) → bare page (home) · navUrl({video:"F01"}) → ?video=F01 · true → "1", null/""/false → dropped.
   The first change in a click pushes a history entry; nested calls in the same tick (openMap → openLesson)
   replace it, so one click = one back step.
   Back/forward (popstate) re-opens the screen through the apps' public hooks (quit, VIDEO_UI, COURSE/COURSE_UI,
   openLearnAt, startTopicPractice / CC_APP.practiceTopic). Anything it cannot open in place falls back to a
   reload, which the deep-link readers in app.js / course-ui.js / video-ui.js restore. */
(function(){
  // while the scripts boot, the deep-link readers own the URL (initStart() may show the home screen first)
  let ready = document.readyState === "complete";
  if (!ready) document.addEventListener("DOMContentLoaded", () => { ready = true; });
  let restoring = false, burst = false;

  function navUrl(params){
    if (!ready || restoring) return;
    try {
      const qs = new URLSearchParams();
      if (params) Object.keys(params).forEach(k => {
        const v = params[k];
        if (v == null || v === false || v === "") return;
        qs.set(k, v === true ? "1" : String(v));
      });
      const s = qs.toString();
      const url = location.pathname + (s ? "?" + s : "") + location.hash;
      if (url === location.pathname + location.search + location.hash) return;
      if (burst) history.replaceState(null, "", url);
      else { history.pushState(null, "", url); burst = true; setTimeout(() => { burst = false; }, 0); }
    } catch(e){}   // file:// in some browsers, sandboxed frames: just leave the URL alone
  }

  /* open the screen the current URL names; false = no in-place hook for it */
  function route(){
    const p = new URLSearchParams(location.search);
    const V = window.VIDEO_UI, CU = window.COURSE_UI || window.COURSE, ALL = window.COURSES || {};
    if (!location.search){
      if (typeof quit !== "function") return false;
      quit(); return true;
    }
    if (p.has("video")) return !!(V && V.openVideo) && (V.openVideo(p.get("video")), true);
    if (p.has("videos")) return !!(V && V.openList) && (V.openList(), true);
    let cid = p.get("course"), lid = p.get("level");
    if (!cid) for (const k of Object.keys(ALL)) if (p.has(k)){ cid = k; lid = p.get(k); break; }   // ?<course>=<level>
    if (cid){
      if (!CU || !CU.openMap || !ALL[cid]) return false;
      const L = (ALL[cid].levels || []).find(l => l.id === lid);
      if (lid && lid !== "map" && !L) return false;
      CU.openMap(cid);
      if (L) (p.has("play") ? CU.startLevel(L) : CU.openLesson(L));
      return true;
    }
    if (p.has("learn")){
      const f = window.openLearnAt || (typeof openLearnAt === "function" ? openLearnAt : null);   // app.js: `let openLearnAt`
      return !!f && f(p.get("learn"), parseInt(p.get("s"), 10) || 0) !== false;
    }
    if (p.has("practice")){
      const f = window.startTopicPractice || (window.CC_APP && window.CC_APP.practiceTopic);
      return !!f && f(p.get("practice")) !== false;
    }
    return false;
  }

  window.addEventListener("popstate", () => {
    let ok = false;
    restoring = true;
    try { ok = route(); } catch(e){ ok = false; }
    restoring = false;
    if (!ok) location.reload();
  });

  window.navUrl = navUrl;
})();
