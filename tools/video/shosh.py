# -*- coding: utf-8 -*-
"""Shosh, the presenter: an original flat SVG character in the bottom-right corner of every video.

Ids the timeline drives: shosh-mo (mouth open) / shosh-mc (mouth closed) flap on every spoken word, from the
edge-tts word boundaries; shosh-eo / shosh-ec (eyes open / closed) blink every few seconds.
"""

SKIN, HAIR, SHIRT, INK = "#f4c9a8", "#3a2621", "#2dd4bf", "#1d1830"


def svg():
    return f"""<div id="shosh" class="shosh"><svg viewBox="0 0 200 236" width="190" height="224" direction="ltr">
<defs><clipPath id="shosh-clip"><circle cx="100" cy="106" r="94"/></clipPath></defs>
<circle cx="100" cy="106" r="96" fill="#181a33" stroke="#2dd4bf" stroke-width="4"/>
<g clip-path="url(#shosh-clip)">
  <path d="M46 104 Q44 40 100 36 Q156 40 154 104 L160 178 Q130 190 100 186 Q70 190 40 178 Z" fill="{HAIR}"/>
  <rect x="88" y="138" width="24" height="26" rx="8" fill="{SKIN}"/>
  <path d="M28 236 Q34 176 72 164 Q100 176 128 164 Q166 176 172 236 Z" fill="{SHIRT}"/>
  <path d="M84 166 L100 186 L116 166" fill="none" stroke="#e8fffb" stroke-width="5" stroke-linejoin="round"/>
  <ellipse cx="100" cy="100" rx="45" ry="50" fill="{SKIN}"/>
  <ellipse cx="55" cy="104" rx="7" ry="10" fill="{SKIN}"/><ellipse cx="145" cy="104" rx="7" ry="10" fill="{SKIN}"/>
  <circle cx="55" cy="117" r="3.5" fill="#38bdf8"/><circle cx="145" cy="117" r="3.5" fill="#38bdf8"/>
  <path d="M55 92 Q58 50 100 50 Q142 50 145 92 Q128 70 104 74 Q90 64 72 76 Q62 82 55 92 Z" fill="{HAIR}"/>
  <path d="M74 86 Q83 81 92 85" fill="none" stroke="{HAIR}" stroke-width="3.5" stroke-linecap="round"/>
  <path d="M108 85 Q117 81 126 86" fill="none" stroke="{HAIR}" stroke-width="3.5" stroke-linecap="round"/>
  <g id="shosh-eo"><ellipse cx="83" cy="100" rx="5.5" ry="7.5" fill="{INK}"/><ellipse cx="117" cy="100" rx="5.5" ry="7.5" fill="{INK}"/>
    <circle cx="85" cy="97" r="2" fill="#fff"/><circle cx="119" cy="97" r="2" fill="#fff"/></g>
  <g id="shosh-ec" opacity="0"><path d="M77 101 Q83 105 89 101" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>
    <path d="M111 101 Q117 105 123 101" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round"/></g>
  <g fill="none" stroke="#c9cdf0" stroke-width="2.4"><circle cx="83" cy="100" r="14"/><circle cx="117" cy="100" r="14"/>
    <path d="M97 99 Q100 96 103 99"/></g>
  <ellipse cx="72" cy="120" rx="8" ry="5" fill="#fb7185" opacity=".35"/><ellipse cx="128" cy="120" rx="8" ry="5" fill="#fb7185" opacity=".35"/>
  <path d="M97 110 Q100 114 103 110" fill="none" stroke="#d9a07f" stroke-width="2.2" stroke-linecap="round"/>
  <path id="shosh-mc" d="M88 126 Q100 135 112 126" fill="none" stroke="#9a3b4a" stroke-width="3.5" stroke-linecap="round"/>
  <g id="shosh-mo" opacity="0"><path d="M88 124 Q100 122 112 124 Q110 140 100 141 Q90 140 88 124 Z" fill="#7a2338"/>
    <path d="M93 135 Q100 131 107 135 Q104 140 100 140 Q96 140 93 135 Z" fill="#fb7185"/>
    <path d="M89 124.5 Q100 123 111 124.5 L110 127 Q100 126 90 127 Z" fill="#fff"/></g>
</g>
<rect x="64" y="204" width="72" height="28" rx="14" fill="#2dd4bf"/>
<text x="100" y="224" text-anchor="middle" font-size="19" font-weight="700" fill="#0a0c18" font-family="Segoe UI">שוש</text>
</svg></div>"""


def timeline_js(words, total):
    """GSAP sets: a mouth flap per spoken word (two for long words) and a blink every ~3.7 s"""
    js = []
    def mouth(t, open_):
        js.append(f'tl.set("#shosh-mo",{{opacity:{1 if open_ else 0}}},{t:.3f});'
                  f'tl.set("#shosh-mc",{{opacity:{0 if open_ else 1}}},{t:.3f});')
    for t, d in words:
        d = max(0.12, min(d, 1.2))
        mouth(t, True)
        mouth(t + d * 0.5, False)
        if d > 0.4:
            mouth(t + d * 0.6, True)
            mouth(t + d * 0.9, False)
    k, t = 0, 2.0
    while t < total - 0.5:
        js.append(f'tl.set("#shosh-eo",{{opacity:0}},{t:.3f});tl.set("#shosh-ec",{{opacity:1}},{t:.3f});'
                  f'tl.set("#shosh-eo",{{opacity:1}},{t + 0.13:.3f});tl.set("#shosh-ec",{{opacity:0}},{t + 0.13:.3f});')
        k += 1
        t += 3.1 + (k % 3) * 0.6
    return "".join(js)
