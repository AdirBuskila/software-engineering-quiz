"""Offline checker for the UML course (uml).

Rule tables: diagram -> model, relation -> symbol, relation -> code container (multiplicity), which relations belong
to which diagram, sequence-diagram notation, statechart components, "which diagram answers which need". Each original
question states one claim per option; the keyed option must be the only defensible one.
Run:  python tools/verify/needhelp/uml/check.py
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import load_questions, Report

MODEL = {"class": "Structure", "sequence": "Interaction", "usecase": "Interaction", "activity": "Context", "statechart": "Behavior"}
SYMBOL = {"inheritance": "hollow_triangle", "composition": "filled_diamond", "aggregation": "hollow_diamond", "dependency": "dashed_arrow"}
CLASS_RELATIONS = {"inheritance", "association", "aggregation", "composition"}
USECASE_RELATIONS = {"include", "extend"}
SEQ_NOTATION = {"message", "return", "activation", "destruction", "lifeline"}
STATE_COMPONENTS = {"state", "transition", "initial_state", "guard", "history"}
PURPOSE = {"class": {"hierarchy", "attributes"}, "sequence": {"call_order"}, "statechart": {"all_states", "transitions"}}
NEED = {"message_order": "sequence", "structure": "class", "process_flow": "activity", "states": "statechart", "who_uses": "usecase"}

def relation_for(part_lives_without_whole, is_a=False):
    if is_a: return "inheritance"
    return "aggregation" if part_lives_without_whole else "composition"

def container(mult):
    """multiplicity -> data structure in code: a finite upper bound > 1 gives an array, '*' gives a list."""
    hi = mult.split("..")[-1]
    if hi == "*": return "list"
    return "array" if int(hi) > 1 else "field"

def join_ready(done, incoming):          # a solid bar (join) waits for every incoming activity
    return set(incoming) <= set(done)

def missing_returns(messages):           # every request that is answered needs a dashed return, in reverse order
    return [(b, a) for (a, b, _) in reversed(messages)]

qs = load_questions("uml")
R = Report("uml")

# U01
def model_q(qid, diagram, order):
    R.mcq(qs, qid, [(a, MODEL[diagram] == a) for a in order])
model_q("U01-Q1", "class", ["Structure", "Interaction", "Context", "Behavior"])
model_q("U01-Q2", "sequence", ["Interaction", "Structure", "Context", "Behavior"])
model_q("U01-Q3", "activity", ["Context", "Structure", "Interaction", "Behavior"])
model_q("U01-Q4", "statechart", ["Behavior", "Structure", "Context", "Interaction"])

# U02
R.mcq(qs, "U02-Q1", [("ראש משולש", SYMBOL["inheritance"] == "hollow_triangle"), ("מעוין מלא", SYMBOL["inheritance"] == "filled_diamond"),
                     ("מעוין ריק", SYMBOL["inheritance"] == "hollow_diamond"), ("קו מקווקו", SYMBOL["inheritance"] == "dashed_arrow")])
rel = relation_for(part_lives_without_whole=False)        # an engine does not outlive its car
opts = [("composition", "whole"), ("aggregation", "part"), ("inheritance", "part"), ("association", "none")]
R.mcq(qs, "U02-Q2", [("Composition: מעוין מלא בצד של Car", opts[0] == (rel, "whole")), ("Aggregation: מעוין ריק בצד של Engine", opts[1] == (rel, "whole")),
                     ("ירושה: חץ משולש", opts[2] == (rel, "whole")), ("Association בלבד", opts[3] == (rel, "whole"))])
opts3 = [{"hierarchy", "attributes"}, {"call_order"}, {"runtime", "physical_split"}, {"all_states", "transitions"}]
R.mcq(qs, "U02-Q3", [("יחס היררכי", opts3[0] <= PURPOSE["class"]), ("סדר זמנים", opts3[1] <= PURPOSE["class"]),
                     ("חישובי זמני ריצה", opts3[2] <= PURPOSE["class"]), ("המצבים האפשריים", opts3[3] <= PURPOSE["class"])])
rel4 = relation_for(part_lives_without_whole=True)        # a player outlives his team
opts4 = [("aggregation", "whole"), ("composition", "whole"), ("inheritance", "whole"), ("none", "whole")]
R.mcq(qs, "U02-Q4", [("Aggregation: מעוין ריק בצד של Team", opts4[0] == (rel4, "whole")), ("Composition: מעוין מלא", opts4[1] == (rel4, "whole")),
                     ("ירושה: Player יורש", opts4[2] == (rel4, "whole")), ("אין קשר", opts4[3] == (rel4, "whole"))])

# U03
R.mcq(qs, "U03-Q1", [("מערך", container("2..4") == "array"), ("קובץ", False), ("מחרוזת", False), ("אי אפשר לדעת", False)])
R.eq("U03-Q1", container("2..4") == "array" and container("1..*") == "list" and container("1..10") == "array", "multiplicity -> container rule")
sets = [{"inheritance", "association", "aggregation", "composition"}, {"include", "extend", "inheritance", "association"},
        {"exclude", "include", "composition", "aggregation"}, {"extend", "exclude", "association", "inheritance"}]
R.mcq(qs, "U03-Q2", [("ירושה, association, aggregation, composition", sets[0] <= CLASS_RELATIONS), ("Include, Extend, ירושה, association", sets[1] <= CLASS_RELATIONS),
                     ("Exclude, Include, composition, aggregation", sets[2] <= CLASS_RELATIONS), ("Extend, Exclude, association, ירושה", sets[3] <= CLASS_RELATIONS)])
KIND = {"Customer": "entity", "Order": "entity", "OrderService": "service", "PaymentService": "service", "Button": "ui", "Screen": "ui",
        "Printer": "hw", "Browser": "ui", "Mouse": "hw", "Keyboard": "hw", "Database": "infra", "Window": "ui", "Menu": "ui"}
good = lambda names: all(KIND[n] in ("entity", "service") for n in names)
R.mcq(qs, "U03-Q3", [("Customer, Order, OrderService, PaymentService", good(["Customer", "Order", "OrderService", "PaymentService"])),
                     ("Customer, Button, Screen, Printer", good(["Customer", "Button", "Screen", "Printer"])),
                     ("Browser, Mouse, Keyboard, Order", good(["Browser", "Mouse", "Keyboard", "Order"])),
                     ("Database, Window, Menu, Customer", good(["Database", "Window", "Menu", "Customer"]))])

# U04
def uc_relation(mandatory):
    return "include" if mandatory else "extend"
k1 = uc_relation(True)
R.mcq(qs, "U04-Q1", [("<<include>> מ-", k1 == "include"), ("<<extend>> מ-", k1 == "extend"),
                     ("ירושה בין שני", "inheritance" in USECASE_RELATIONS), ("אין קשר", False)])
k2 = uc_relation(False)
R.mcq(qs, "U04-Q2", [("<<extend>>", k2 == "extend"), ("<<include>>", k2 == "include"), ("ירושה", "inheritance" in USECASE_RELATIONS),
                     ("Composition", "composition" in USECASE_RELATIONS)])
INTERNAL = {"הספרן": False, "הטבלה Books": True, "המחלקה Book": True, "הפונקציה borrow": True}
R.mcq(qs, "U04-Q3", [(n, not internal) for n, internal in INTERNAL.items()])

# U05
R.mcq(qs, "U05-Q1", [("משתתף או אובייקט בודד", True), ("כל ההודעות", False), ("הזמן שבו משתתף ממתין", False), ("סוף התרשים", False)])
ACT = {"busy_and_waiting": True, "inactive": False, "created_or_destroyed": False, "actor_first_start": False}
R.mcq(qs, "U05-Q2", [("מבצע פעולה וממתין", ACT["busy_and_waiting"]), ("אינו פעיל", ACT["inactive"]),
                     ("נוצר או נהרס", ACT["created_or_destroyed"]), ("ה-Actor התחיל", ACT["actor_first_start"])])
SEQ = {"solid_arrow": "message", "dashed_arrow": "return", "X": "destruction"}
R.mcq(qs, "U05-Q3", [("תשובה (return)", SEQ["dashed_arrow"] == "return"), ("בקשה חדשה", SEQ["dashed_arrow"] == "message"),
                     ("הריסה", SEQ["dashed_arrow"] == "destruction"), ("קשר ירושה", False)])
R.mcq(qs, "U05-Q4", [("הריסה (destruction)", SEQ["X"] == "destruction"), ("נבנה זה עתה", SEQ["X"] == "construction"),
                     ("האינטראקציה כולה הסתיימה", SEQ["X"] == "end_of_interaction"), ("הודעה אחרונה נמחקה", SEQ["X"] == "deleted_message")])

# U06
exp = {"מטופל": "Actor", "שרת": "participant", "שירות ה-SMS": "participant"}
cands = [{"מטופל": "Actor", "שרת": "participant", "שירות ה-SMS": "participant"}, {"מטופל": "participant", "שרת": "participant", "שירות ה-SMS": "Actor"},
         {"מטופל": "participant", "שרת": "Actor", "שירות ה-SMS": "participant"}, {"מטופל": "-", "שרת": "-", "שירות ה-SMS": "-"}]
R.mcq(qs, "U06-Q1", [("מטופל כ-Actor, שרת", cands[0] == exp), ("שירות ה-SMS כ-Actor", cands[1] == exp), ("שרת כ-Actor", cands[2] == exp), ("מזכירה כ-Actor", cands[3] == exp)])
need = missing_returns([("user", "Server", "load page"), ("Server", "myDB", "read row")])
R.mcq(qs, "U06-Q2", [("חצים מקווקווים של תשובה", need == [("myDB", "Server"), ("Server", "user")]), ("<<include>>", "include" in SEQ_NOTATION),
                     ("חץ ירושה", "inheritance" in SEQ_NOTATION), ("מעוין מלא", "composition" in SEQ_NOTATION)])
R.mcq(qs, "U06-Q3", [("אין קשרים", len(set()) == 0), ("Include ו-Extend", len(USECASE_RELATIONS & SEQ_NOTATION) > 0),
                     ("ירושה והכלה", len({"inheritance", "composition"} & SEQ_NOTATION) > 0), ("Association עם ריבוי", "association" in SEQ_NOTATION)])

# U07
def substate_kind(exclusive, independent_parallel):
    return "XOR" if exclusive else ("AND" if independent_parallel else "?")
x1 = substate_kind(True, False)
R.mcq(qs, "U07-Q1", [("XOR", x1 == "XOR"), ("AND", x1 == "AND"), ("מצב סיום", False), ("מצב התחלתי", False)])
x2 = substate_kind(False, True)
R.mcq(qs, "U07-Q2", [("AND", x2 == "AND"), ("XOR", x2 == "XOR"), ("מצב סיום", False), ("היסטוריה", False)])
R.mcq(qs, "U07-Q3", [("מסר שנשלח", "message" in STATE_COMPONENTS), ("מעבר בין שני מצבים", "transition" in STATE_COMPONENTS),
                     ("מצב התחלתי", "initial_state" in STATE_COMPONENTS), ("תנאי (guard)", "guard" in STATE_COMPONENTS)], mode="false")
o4 = [{"all_states", "transitions"}, {"call_order"}, {"hierarchy", "attributes"}, {"services"}]
R.mcq(qs, "U07-Q4", [("כלל המצבים האפשריים", o4[0] <= PURPOSE["statechart"]), ("סדר ההודעות", o4[1] <= PURPOSE["statechart"]),
                     ("מבנה המחלקות", o4[2] <= PURPOSE["statechart"]), ("השירותים שהמערכת נותנת", o4[3] <= PURPOSE["statechart"])])

# U08
inc = ["A", "B", "C"]
R.mcq(qs, "U08-Q1", [("רק אחרי ש-A, B ו-C כולן", join_ready(["A", "B", "C"], inc) and not join_ready(["A", "B"], inc)),
                     ("ברגע שאחת מהן", join_ready(["A"], inc)), ("מיד", join_ready([], inc)), ("רק אחרי ש-A הסתיימה", join_ready(["A"], inc))])
def diag_q(qid, need_key, order):
    R.mcq(qs, qid, [(a, NEED[need_key] == d) for a, d in order])
diag_q("U08-Q2", "message_order", [("תרשים רצף", "sequence"), ("תרשים מחלקות", "class"), ("תרשים מצבים", "statechart"), ("תרשים Use Case", "usecase")])
diag_q("U08-Q3", "process_flow", [("תרשים פעילות", "activity"), ("תרשים מחלקות", "class"), ("תרשים רצף", "sequence"), ("תרשים Use Case", "usecase")])
diag_q("U08-Q4", "structure", [("תרשים מחלקות", "class"), ("תרשים רצף", "sequence"), ("תרשים פעילות", "activity"), ("תרשים מצבים", "statechart")])

R.finish(qs)
