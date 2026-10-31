# -*- coding: utf-8 -*-
"""Shared pronunciation machinery for the narration (he-IL-HilaNeural via edge-tts).

Each app has videos/lexicon.py:  `from lexicon_base import *`, then adds its own terms with WORDS.update({...}),
SYMBOL.update({...}) and, when it needs more TeX shapes, wraps tex_say (see APP_TEX below).
Subtitles keep the course spelling; the TTS gets the spoken form. Check every new entry by synthesizing it and
transcribing it back (vid.py --check does that for whole scripts).

Learned on automata-quiz (2026-10-28/29, STT-checked):
  a -> "אֵיי" (plain "איי" is heard "I"); b -> "בִּי"
  "א״ב" -> "אָלֶף בֵּית" (plain "אלף" was read "elef")
  "הכלה" -> "הֲכָלָה" (heard "הקלה"); "שלו" before a noun can be heard "שלא": reword when it flips the meaning
  "למת הניפוח" -> "הלמה של הניפוח"; gershayim acronyms are read badly: spell them out
  run steps read together ("Q 1 0"): one short sentence per step, "X: לקיו Y."
"""
import re

# Hebrew text replacements, applied to the spoken text (longest first). Both gershayim forms are covered.
WORDS = {
    "א״ב": "אָלֶף בֵּית",
    "ע״י": "על ידי",
    "ע״פ": "על פי",
    "הכלה": "הֲכָלָה",
    "הכלות": "הֲכָלוֹת",
    "למת הניפוח": "הלמה של הניפוח",
    "בלמת הניפוח": "בלמה של הניפוח",
    "ללמת הניפוח": "ללמה של הניפוח",
}

DIGIT = {"0": "אפס", "1": "אחת", "2": "שתיים", "3": "שלוש", "4": "ארבע", "5": "חמש", "6": "שש", "7": "שבע",
         "8": "שמונה", "9": "תשע"}
LETTER = {"a": "אֵיי", "b": "בִּי", "c": "סִי", "d": "דִּי", "x": "אקס", "y": "וואי", "z": "זד"}
SYMBOL = {r"\varepsilon": "אפסילון", r"\epsilon": "אפסילון", r"\delta": "דלתא", r"\Sigma": "סיגמא",
          r"\Gamma": "גמא", r"\emptyset": "הקבוצה הריקה", r"\varnothing": "הקבוצה הריקה",
          r"\Sigma^*": "סיגמא כוכבית"}


def state_say(name):
    """q_0 / q_{12} / q0 -> 'קיו אפס'"""
    m = re.fullmatch(r"q_?\{?(\d+)\}?", name)
    if not m:
        raise ValueError(f"not a state name: {name!r}")
    return "קיו " + " ".join(DIGIT[d] for d in m.group(1))


def word_say(w, alphabet="01ab"):
    """a word over the alphabet, letter by letter: 0110 -> 'אפס אחת אחת אפס'; '' -> 'אפסילון'"""
    if w == "":
        return "אפסילון"
    return " ".join(DIGIT.get(c) or LETTER[c] for c in w)


def base_tex_say(tex):
    """speak a TeX span when it is one of the simple shapes; None = the script must give an explicit `say`"""
    t = tex.strip().replace(r"\,", "").replace(" ", "")
    if t in SYMBOL:
        return SYMBOL[t]
    if re.fullmatch(r"[01ab]+", t):
        return word_say(t)
    if re.fullmatch(r"q_?\{?\d+\}?", t):
        return state_say(t)
    if re.fullmatch(r"\d+", t):
        return t                      # numbers: the TTS reads them well
    return None


tex_say = base_tex_say


def say_hebrew(s):
    for k in sorted(WORDS, key=len, reverse=True):
        for v in (k, k.replace("״", '"')):
            s = s.replace(v, WORDS[k])
    # a prefix (ו, ב, ומ, …) glued with a hyphen ("ו-$q_2$", "ב-$0$") is read as one word, not "vav, hyphen"
    s = re.sub(r"(^|[\s(])([ובכלמהש]{1,3})-", r"\1\2", s)
    return s
