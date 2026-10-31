# -*- coding: utf-8 -*-
"""P06 · Command: Invoker, Command ו-Receiver — video script (build: tools/video/vid.py P06).

Source: courses/pat/P06.js (lesson + goal: cast components as Invoker / Command / Receiver, explain how Command
decouples the one who triggers from the one who performs, and how it allows undo). Exam anchor: 24S-A-Q9 (the
Receiver's role -> the action is performed on it when the command is called), which no guided quiz uses; its three
wrong options describe the Invoker and the Command, which the video names one by one.
The Java on screen is compiled and run here (w_pat.java): two presses of "volume up" and one undo leave the speaker
at 6 (it starts at 5).
The undo demo shows the Keypad's `done` field step by step; the rule itself (Invoker keeps a stack, undoes the last)
and "the Invoker knows only the Command interface" are not stated in words (P06-Q3 / P06-Q2 wording).
Avoided on purpose: the P06 quiz items (Remote/Light/TurnOnCommand, what the Invoker knows, undo in a graphics editor
= 26CL-Q17's twin, the recorder 25S-A-Q11 and its twins 25B-N-Q12 / 25F0b-Q11, 24B-A-Q8 Receiver = the document),
the boss item 26B-A-Q19 (smart-home remote) and 24B-A-Q7 (buttons and menus). My own case: a restaurant (spoken
analogy) and a keypad that controls a speaker's volume.
"""
from vid import P, Scene, Video, show, hide, BANK
import stage as st
import w_pat as w

assert w.solves("Command", {"encapsulate_action", "undo", "decouple_invoker"})

# ---------------------------------------------------------------- code (compiled and run)
LIB = """interface Command { void execute(); void undo(); }

class Speaker {                          // the Receiver
  private int volume = 5;
  void louder() { volume++; }
  void quieter() { volume--; }
  int volume() { return volume; }
}

class VolumeUp implements Command {      // a Command
  private final Speaker speaker;
  VolumeUp(Speaker s) { speaker = s; }
  public void execute() { speaker.louder(); }
  public void undo() { speaker.quieter(); }
}

class Keypad {                           // the Invoker
  private final Deque<Command> done = new ArrayDeque<>();
  void press(Command c) { c.execute(); done.push(c); }
  void undoLast() { if (!done.isEmpty()) done.pop().undo(); }
}"""
BODY = """Speaker spk = new Speaker();
Keypad pad = new Keypad();
pad.press(new VolumeUp(spk));
pad.press(new VolumeUp(spk));
pad.undoLast();
System.out.println(spk.volume());"""
MAIN = "public class Main {\n  public static void main(String[] args) {\n" + "\n".join("    " + l for l in BODY.split("\n")) + "\n  }\n}"
OUT = "6"
w.java({"Command": "import java.util.ArrayDeque;\nimport java.util.Deque;\n\n" + LIB, "Main": MAIN}, "Main", OUT)

# Python mirror of the run: volume and the undo stack after each line of BODY
vol, stack, trace = 5, [], []
for line in BODY.split("\n")[2:5]:
    if "press" in line:
        vol += 1
        stack.append("VolumeUp")
    else:
        stack.pop()
        vol -= 1
    trace.append((vol, len(stack)))
assert trace == [(6, 1), (7, 2), (6, 1)] and str(vol) == OUT

L = LIB.split("\n")
L_CMD, L_SPK, L_EXEC, L_UNDO, L_INV, L_PRESS, L_UL = 0, 2, 12, 13, 16, 18, 19
assert L[L_SPK].startswith("class Speaker") and "speaker.louder()" in L[L_EXEC] and "speaker.quieter()" in L[L_UNDO]
assert L[L_INV].startswith("class Keypad") and "void press" in L[L_PRESS] and "undoLast" in L[L_UL]
assert "Speaker" not in "\n".join(L[L_INV:])          # the Invoker never names the Receiver

# exam 24S-A-Q9
Q = BANK["24S-A-Q9"]
assert Q["correctIndex"] == 4 and Q["options"][4].startswith("הפעולה מבוצעת עליו")
assert "מאחסן הפניה לפקודה" in Q["options"][1] and "ממשק לביצוע פקודות" in Q["options"][2]
assert "יוזם את הפקודה" in Q["options"][3]
OPTS = w.opts_of(Q)

UML = w.uml("u", [
    dict(key="inv", name="Keypad", x=30, y=40, w=360, role="Invoker",
         members=["- done : Deque<Command>", "+ press(c)", "+ undoLast()"]),
    dict(key="cmd", name="Command", x=560, y=40, w=330, kind="interface", members=["+ execute()", "+ undo()"]),
    dict(key="vu", name="VolumeUp", x=560, y=330, w=330, role="Command", hidden=True,
         members=["- speaker : Speaker", "+ execute()", "+ undo()"]),
    dict(key="rec", name="Speaker", x=60, y=350, w=300, role="Receiver", hidden=True, members=["+ louder()", "+ quieter()"]),
], [
    dict(key="has", a="inv", b="cmd", kind="has", sides="rl", fa=0.3, fb=0.4, hidden=True),
    dict(key="impl", a="vu", b="cmd", kind="impl", sides="tb"),
    dict(key="call", a="vu", b="rec", kind="call", sides="lr", label="louder()", lxy=(400, 400)),
], w=1000, h=560)

# ---------------------------------------------------------------- scenes
title = Scene("title", "", [
    P("בסרטון הזה נכיר את Command: תבנית שהופכת בקשה לפעולה לאובייקט."),
    P("נלמד את שלושת התפקידים שלה, נראה איך היא מאפשרת ביטול, ונפתור שאלה ממבחן.", hold=0.4),
], stage='<div class="kicker">P06 · תבניות עיצוב</div><h1>Command: Invoker, Command ו-Receiver</h1>'
         '<p>לשבץ רכיבים בתפקידי Invoker, Command ו-Receiver, ולהסביר איך Command מנתקת את המפעיל מהמבצע ומאפשרת undo.</p>',
   layout="title")

idea = Scene("idea", "הרעיון", [
    P("נתחיל במסעדה. המלצר לוקח הזמנה, כותב אותה על פתק, ומעביר למטבח.", do=show("i-1")),
    P("המלצר לא יודע לבשל. הוא רק מחזיק את הפתק ומעביר אותו הלאה.", do=show("i-2")),
    P("הפתק הוא הבקשה עצמה, שהפכה לחפץ: אפשר לשמור אותו, לשים בתור, או לבטל.", do=show("i-3")),
    P("והטבח הוא מי שהבקשה מגיעה אליו, ומתבצעת אצלו.", do=show("i-4")),
    P("זו בדיוק Command: עוטפים **בקשה לפעולה כאובייקט**, ומנתקים את מי שמפעיל ממי שמבצע.", do=show("i-c1"), hold=0.4),
], stage=w.stack(st.card("i-1", "ex", "🧑‍🍳 מסעדה: מלצר · פתק הזמנה · טבח"),
                 st.card("i-2", "plain", "המלצר: מחזיק ומעביר, לא מבשל"),
                 st.card("i-3", "plain", "הפתק: הבקשה כחפץ. שומרים, מתזמנים, מבטלים"),
                 st.card("i-4", "plain", "הטבח: אצלו הבקשה מתבצעת"), gap=22),
   panel=st.card("i-c1", "rule", "🔑 בקשה לפעולה = <b>אובייקט</b><br>ניתוק בין המפעיל למבצע"))

roles = Scene("roles", "שלושה תפקידים", [
    P("ועכשיו בקוד. לוח מקשים שמגביר ומנמיך רמקול.", do=show("u")),
    P("הממשק של הפקודה: שתי פעולות, לבצע ולבטל.", do=show("u-hb-cmd")),
    P("לוח המקשים הוא ה-**Invoker**, המפעיל. הוא מחזיק פקודות ומפעיל אותן.", do=hide("u-hb-cmd") + show("u-hb-inv", "u-a-has")),
    P("ושימו לב לקוד של לוח המקשים: המילה רמקול לא מופיעה בו בכלל.", do=show("r-c1")),
    P("פקודת ההגברה היא **Command**: הפעולה עצמה, כאובייקט.", do=hide("u-hb-inv") + show("u-b-vu", "u-a-impl", "u-hb-vu")),
    P("והרמקול הוא ה-**Receiver**: האובייקט שהפעולה מתבצעת עליו. הפקודה קוראת לו.",
      do=hide("u-hb-vu") + show("u-b-rec", "u-a-call", "u-hb-rec")),
    P("שלוש שאלות מסדרות את זה: מי **מפעיל**? מה **הפעולה**? ועל מי היא **קורית**?", do=show("r-c2"), hold=0.4),
    P("ובגלל הניתוק, אפשר להוסיף פקודה חדשה, למשל השתקה, בלי לשנות את לוח המקשים בכלל.", do=show("r-c3")),
], stage=UML.replace('class="pt-uml"', 'class="pt-uml h"', 1),
   panel=st.card("r-c1", "rule", "🔑 בקוד של " + w.mono("Keypad") + " אין " + w.mono("Speaker"))
         + st.card("r-c2", "ex", "מפעיל ← Invoker · הפעולה ← Command · עליו קורית ← Receiver")
         + st.card("r-c3", "ex", "פקודה חדשה = מחלקה חדשה. ה-Invoker לא משתנה"))

def ROW(v, n):
    stack = "".join('<span class="pt-chip obs">VolumeUp</span>' for _ in range(n)) or '<span class="pt-empty">(ריק)</span>'
    return (f'<div class="pt-row" style="gap:18px"><span class="pt-chip st">עוצמה: {v}</span>'
            f'<span class="pt-rlab">{w.mono("done")}:</span><span class="pt-rchips" dir="ltr">{stack}</span></div>')


STATE = w.swap("v", [ROW(5, 0), ROW(6, 1), ROW(7, 2), ROW(6, 1)], 64, width=900, first_visible=False)
run = Scene("undo", "ביצוע וביטול", [
    P("לפקודת ההגברה יש שתי פעולות: לבצע, שמגבירה, ולבטל, שמנמיכה.",
      do=show("c", f"c-m{L_EXEC}", f"c-m{L_UNDO}")),
    P("ועכשיו לוח המקשים: מה קורה בלחיצה, ומה קורה בכפתור הביטול?", do=hide(f"c-m{L_EXEC}", f"c-m{L_UNDO}") + show(f"c-m{L_PRESS}", f"c-m{L_UL}")),
    P("נעקוב אחרי זה בהרצה, ונראה גם מה נמצא בשדה של הלוח.", do=hide(f"c-m{L_PRESS}", f"c-m{L_UL}")),
    P("העוצמה מתחילה בחמש. לחיצה ראשונה על הגברה: שש.", do=hide("c") + show("m", "m-m2", "v-1")),
    P("לחיצה שנייה: שבע. בשדה של הלוח יש עכשיו שתי פקודות הגברה.", do=hide("m-m2", "v-1") + show("m-m3", "v-2")),
    P("ועכשיו כפתור הביטול. בשדה נשארה פקודה אחת, והעוצמה חזרה לשש.",
      do=hide("m-m3", "v-2") + show("m-m4", "v-3")),
    P("הרצנו את הקוד, והוא הדפיס שש.", do=hide("m-m4") + show("m-m5", "mo", "u-c1"), hold=0.4),
], stage='<div class="swap" style="--swap-h:600px">'
         + f'<div>{w.code("c", LIB, hidden=True, size=19)}</div>'
         + f'<div>{w.stack(w.code("m", BODY, hidden=True, size=26), STATE, w.out("mo", OUT, size=28), gap=24)}</div></div>',
   panel=st.card("u-c1", "ex", 'העוצמה: <span dir="ltr" class="pt-mono">5 → 6 → 7 → 6</span>'))

exam = Scene("exam", "שאלה ממבחן", [
    P("ועכשיו שאלה ממבחן: בתבנית Command, מה תפקידו של ה-Receiver?"),
    P("אצלנו זה הרמקול. ההגברה וההנמכה קורות עליו, כשהפקודה מבוצעת.", do=show("x-u")),
    P("לכן: הפעולה מבוצעת עליו כאשר הפקודה נקראת. זו התשובה.", do=show("q-ok-4")),
    P("״מאחסן הפניה לפקודה שתתבצע מאוחר יותר״: זה לוח המקשים, ה-Invoker, עם המחסנית שלו.",
      do=show("q-x-1", "q-n-1")),
    P("״יוזם את הפקודה ומחליט איזו פקודה לבצע״: גם זה צד המפעיל, ולא מי שהפעולה קורית עליו.",
      do=show("q-x-3", "q-n-3")),
    P("״מייצג ממשק לביצוע פקודות״: זה הממשק של ה-Command, עם פעולת הביצוע.", do=show("q-x-2", "q-n-2")),
    P("ויש תשובה נכונה, ולכן ״כל האחרות שגויות״ נופלת.", do=show("q-x-0", "q-n-0")),
    P("דרך לזכור: Receiver הוא ״המקבל״. הוא מקבל עליו את הפעולה עצמה, ולא את ההחלטה עליה."),
    P("המלכודת: שלוש התשובות השגויות מתארות תפקידים **אמיתיים** בתבנית. רק לא את ה-Receiver.",
      do=show("x-t"), hold=0.5),
], stage=w.stack(w.reprefix(UML, "u", "xu", reveal=True).replace('class="pt-uml"', 'class="pt-uml h"', 1).replace('id="xu"', 'id="x-u"'),
                 st.card("x-t", "trap", "⚠️ המסיחים = התפקידים האחרים של אותה תבנית"), gap=10),
   panel=w.tight(w.stem(Q["id"], "בתבנית הפקודה (Command), מה תפקידו של ה-Receiver?")
                 + st.options("q", OPTS, notes={0: "יש נכונה", 1: "Invoker", 2: "ממשק Command", 3: "Invoker"})))

recap = Scene("recap", "סיכום", [
    P("לסיכום: Command עוטפת בקשה לפעולה כאובייקט, ומנתקת את המפעיל מהמבצע.", do=show("r-1")),
    P("Invoker מפעיל ומחזיק פקודות. Command היא הפעולה. Receiver הוא מי שהפעולה קורית עליו.", do=show("r-2")),
    P("ובהרצה ראינו שתי הגברות וביטול אחד, והרמקול נעצר על שש. נתראה ברמה הבאה.", do=show("r-3"), hold=0.6),
], stage=w.stack(w.reprefix(UML, "u", "zu", reveal=True), gap=20),
   panel=st.card("r-1", "rule", "🔑 בקשה = אובייקט · ניתוק")
         + st.card("r-2", "rule", "🔑 מפעיל = Invoker · פעולה = Command · עליו = Receiver")
         + st.card("r-3", "ex", "הגברה, הגברה, ביטול ← 6"))

SCENES = [title, idea, roles, run, exam, recap]
w.no_latin(SCENES)
VIDEO = Video("P06", "pat", "Command: Invoker, Command ו-Receiver", SCENES, bank={"24S-A-Q9": 4})
