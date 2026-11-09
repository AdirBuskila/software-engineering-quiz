"use strict";
/* navurl.js — keep the address bar in step with the open screen, so a refresh (or a copied link) lands back
   on the same video / lesson / chapter / drill instead of the home screen.
   navUrl(null) → bare page (home) · navUrl({video:"F01"}) → ?video=F01 · true → "1", null/""/false → dropped.
   Uses history.replaceState: the back button keeps its old behaviour. The deep-link readers that already
   exist in app.js / course-ui.js / video-ui.js restore the screen on load. Shared verbatim by every quiz app. */
(function(){
  // while the scripts boot, the deep-link readers own the URL (initStart() may show the home screen first)
  let ready = document.readyState === "complete";
  if (!ready) document.addEventListener("DOMContentLoaded", () => { ready = true; });
  function navUrl(params){
    if (!ready) return;
    try {
      const qs = new URLSearchParams();
      if (params) Object.keys(params).forEach(k => {
        const v = params[k];
        if (v == null || v === false || v === "") return;
        qs.set(k, v === true ? "1" : String(v));
      });
      const s = qs.toString();
      const url = location.pathname + (s ? "?" + s : "") + location.hash;
      if (url !== location.pathname + location.search + location.hash) history.replaceState(history.state, "", url);
    } catch(e){}   // file:// in some browsers, sandboxed frames: just leave the URL alone
  }
  window.navUrl = navUrl;
})();
