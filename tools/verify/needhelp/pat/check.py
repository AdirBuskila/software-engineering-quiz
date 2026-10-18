"""Offline checker for the design-patterns course (pat).

A rule table says, for every pattern, its family, the needs it solves, and who plays which role.
Each original question states one claim per option; the claim is evaluated from the table (or by running
a tiny simulation: Singleton identity, Observer attach/detach/notify, Command undo stack) and the keyed
option must be the only defensible one.   Run:  python tools/verify/needhelp/pat/check.py
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import load_questions, Report

# ---------------- rule table ----------------
PATTERNS = {
    "Singleton": {"family": "Creational", "solves": {"single_instance", "shared_resource"}},
    "Factory": {"family": "Creational", "solves": {"runtime_type", "hide_concrete_classes", "extensible_types"}},
    "AbstractFactory": {"family": "Creational", "solves": {"family_of_objects"}},
    "Observer": {"family": "Behavioral", "solves": {"notify_many_on_change"}},
    "Command": {"family": "Behavioral", "solves": {"encapsulate_action", "undo", "decouple_invoker"}},
    "MVC": {"family": "Architectural", "solves": {"separate_ui_data"}},
    "Flyweight": {"family": "Structural", "solves": {"many_similar_objects_memory"}},
    "Mediator": {"family": "Behavioral", "solves": {"central_communication"}},
    "Chain": {"family": "Behavioral", "solves": {"first_capable_handles"}},
}
solves = lambda p, needs: set(needs) <= PATTERNS[p]["solves"]
family = lambda p: PATTERNS[p]["family"]

# who owns each Observer operation
OBSERVER_OPS = {"update": "Observer", "attach": "Subject", "detach": "Subject", "notify": "Subject"}

# ---------------- simulations ----------------
class Single:                       # a correctly written Singleton
    _inst = None
    def __init__(self): pass
    @classmethod
    def get(cls):
        if cls._inst is None: cls._inst = cls()
        return cls._inst

def singleton_identity():
    return "true" if Single.get() is Single.get() else "false"

class Subject:
    def __init__(self): self.obs, self.got = [], []
    def attach(self, o): self.obs.append(o)
    def detach(self, o): self.obs.remove(o)
    def notify(self):
        for o in self.obs: self.got.append(o)

def observer_trace():
    s = Subject(); a, b, c = "a", "b", "c"
    s.attach(a); s.attach(b); s.attach(c); s.detach(b); s.notify()
    return s.got

class Invoker:
    def __init__(self): self.hist = []
    def run(self, cmd): cmd[0](); self.hist.append(cmd)
    def undo(self): self.hist.pop()[1]()

def undo_stack_ok():
    state = {"n": 0}
    inc = (lambda: state.__setitem__("n", state["n"] + 1), lambda: state.__setitem__("n", state["n"] - 1))
    inv = Invoker(); inv.run(inc); inv.run(inc); inv.undo()
    return state["n"] == 1             # last command was undone, the earlier one stays

def mvc_edge_allowed(a, b):
    return (a, b) in {("View", "Controller"), ("Controller", "Model"), ("Model", "Controller"), ("Controller", "View")}

# ---------------- claims ----------------
qs = load_questions("pat")
R = Report("pat")

# P01
R.mcq(qs, "P01-Q1", [("Creational", family("Singleton") == "Creational"), ("Structural", family("Singleton") == "Structural"),
                     ("Behavioral", family("Singleton") == "Behavioral"), ("אף משפחה", False)])
R.mcq(qs, "P01-Q2", [("Singleton", solves("Singleton", {"single_instance"})), ("Observer", solves("Observer", {"single_instance"})),
                     ("Factory", solves("Factory", {"single_instance"})), ("Command", solves("Command", {"single_instance"}))])
R.mcq(qs, "P01-Q3", [("Command", solves("Command", {"encapsulate_action", "undo"})), ("Singleton", solves("Singleton", {"encapsulate_action", "undo"})),
                     ("Factory", solves("Factory", {"encapsulate_action", "undo"})), ("MVC", solves("MVC", {"encapsulate_action", "undo"}))])
FACT = {"ready_code": False, "general_solution": True, "passes_knowledge": True, "three_families": True}
R.mcq(qs, "P01-Q4", [("קוד מוכן", FACT["ready_code"]), ("פתרון כללי", FACT["general_solution"]),
                     ("להעביר ידע", FACT["passes_knowledge"]), ("שלוש משפחות", FACT["three_families"])], mode="false")

# P02
def single_ok(ctor_private, static_get, abstract, extra_public_ctor):
    return ctor_private and static_get and not abstract and not extra_public_ctor
R.mcq(qs, "P02-Q1", [("private", single_ok(True, True, False, False)), ("לא סטטית", single_ok(False, False, False, False)),
                     ("abstract", single_ok(False, True, True, False)), ("בנאי ציבורי שני", single_ok(False, True, False, True))])
KIND = {"Singleton": "one class", "Factory": "interface+concrete", "Observer": "subject+observers", "MVC": "three layers"}
R.mcq(qs, "P02-Q2", [("מחלקה אחת", KIND["Singleton"] == "one class"), ("ממשק אחד", KIND["Factory"] == "one class"),
                     ("Subject", KIND["Observer"] == "one class"), ("שלוש שכבות", KIND["MVC"] == "one class")])
R.mcq(qs, "P02-Q3", [("תור הדפסה", solves("Singleton", {"shared_resource"})),
                     ("אובייקט נפרד לכל לקוח", solves("Singleton", {"per_customer_instance"})),
                     ("אותו מחיר", solves("Singleton", {"notify_many_on_change"})),
                     ("סוגי דוחות", solves("Singleton", {"runtime_type"}))])
res = singleton_identity()
R.mcq(qs, "P02-Q4", [("true", res == "true"), ("false", res == "false"), ("שגיאת קומפילציה", False), ("NullPointerException", False)])

# P03
CLIENT = {"depends_on_concrete": False, "writes_new": False, "single_instance": False, "concrete_inherit_each_other": False}
R.mcq(qs, "P03-Q1", [("לא תלוי", not CLIENT["depends_on_concrete"]), ("חייב לכתוב", CLIENT["writes_new"]),
                     ("מופע אחד", CLIENT["single_instance"]), ("לרשת מהמחלקה", CLIENT["concrete_inherit_each_other"])])
need = {"runtime_type", "extensible_types"}
R.mcq(qs, "P03-Q2", [("Factory", solves("Factory", need)), ("Singleton", solves("Singleton", need)),
                     ("Observer", solves("Observer", need)), ("Command", solves("Command", need))])
FADV = {"decouples_client": True, "single_instance": False, "no_interfaces": False, "undo": False}
R.mcq(qs, "P03-Q3", [("ניתוק הלקוח", FADV["decouples_client"]), ("מופע אחד", FADV["single_instance"]),
                     ("ביטול הצורך בממשקים", FADV["no_interfaces"]), ("לבטל פעולה", FADV["undo"])])
OPTKIND = ["AbstractFactory", "Factory", "Singleton", "Observer"]   # what each option of P03-Q4 describes
R.mcq(qs, "P03-Q4", [("סגנון Windows", OPTKIND[0] == "AbstractFactory"), ("csv", OPTKIND[1] == "AbstractFactory"),
                     ("אותו אובייקט", OPTKIND[2] == "AbstractFactory"), ("מחיר המניה", OPTKIND[3] == "AbstractFactory")])

# P04
HOLDS = {("Subject", "Observer")}
R.mcq(qs, "P04-Q1", [("ה-Subject מחזיק", ("Subject", "Observer") in HOLDS), ("כל Observer מחזיק", ("Observer", "Subject") in HOLDS),
                     ("מסד נתונים משותף", False), ("Observers מחזיקים רשימה של Observers", ("Observer", "Observer") in HOLDS)])
got = observer_trace()
R.mcq(qs, "P04-Q2", [("a ו-c", got == ["a", "c"]), ("a, b ו-c", got == ["a", "b", "c"]), ("b בלבד", got == ["b"]), ("אף אחד", got == [])])
FLOW = ["state_change", "notify", "update_each"]
opts = [["state_change", "notify", "update_each"], ["state_change", "observer_attach"], ["state_change", "detach_all"], ["observers_change_subject"]]
R.mcq(qs, "P04-Q3", [("notify, ובה נשלח update", opts[0] == FLOW), ("מפעיל attach על עצמו", opts[1] == FLOW),
                     ("מפעיל detach על כל", opts[2] == FLOW), ("משנים את ה-Subject", opts[3] == FLOW)])
R.mcq(qs, "P04-Q4", [(o, OBSERVER_OPS[o] == "Observer") for o in ["update", "attach", "detach", "notify"]])

# P05
expected = {"WeatherStation": "Subject", "PhoneScreen": "Observer", "WebWidget": "Observer"}
cands = [
    {"WeatherStation": "Subject", "PhoneScreen": "Observer", "WebWidget": "Observer"},
    {"WeatherStation": "Observer", "PhoneScreen": "Subject", "WebWidget": "Subject"},
    {"WeatherStation": "Invoker", "PhoneScreen": "Receiver", "WebWidget": "Receiver"},
    {"WeatherStation": "Factory", "PhoneScreen": "Product", "WebWidget": "Product"}]
R.mcq(qs, "P05-Q1", [("WeatherStation הוא Subject", cands[0] == expected), ("WeatherStation הוא Observer", cands[1] == expected),
                     ("WeatherStation הוא Invoker", cands[2] == expected), ("WeatherStation הוא Factory", cands[3] == expected)])
s1, s2 = Subject(), Subject(); dash = "dash"; s1.attach(dash); s2.attach(dash); s1.notify(); s2.notify()
both = s1.got == [dash] and s2.got == [dash]            # the dashboard hears both stations after one attach per station
R.mcq(qs, "P05-Q2", [("Attach בכל אחת", both), ("אי אפשר", not both), ("update בכל תחנה", OBSERVER_OPS["update"] == "Subject"),
                     ("ה-Dashboard כ-Subject", False)])
SITE = "notify"
R.mcq(qs, "P05-Q3", [("notify של ה-Subject", SITE == "notify"), ("Attach של כל Observer", SITE == "attach"),
                     ("Detach", SITE == "detach"), ("בתרשים המחלקות", SITE == "diagram")])

# P06
exp6 = {"Remote": "Invoker", "TurnOnCommand": "Command", "Light": "Receiver"}
c6 = [{"Remote": "Invoker", "TurnOnCommand": "Command", "Light": "Receiver"}, {"Remote": "Receiver", "TurnOnCommand": "Invoker", "Light": "Command"},
      {"Remote": "Command", "TurnOnCommand": "Receiver", "Light": "Invoker"}, {"Remote": "Subject", "TurnOnCommand": "Observer", "Light": "Product"}]
R.mcq(qs, "P06-Q1", [("Remote הוא Invoker", c6[0] == exp6), ("Remote הוא Receiver", c6[1] == exp6),
                     ("Remote הוא Command", c6[2] == exp6), ("Remote הוא Subject", c6[3] == exp6)])
INVOKER_KNOWS = {"command_interface": True, "concrete_receiver": False, "nothing": False, "observer_list": False}
R.mcq(qs, "P06-Q2", [("רק את הממשק", INVOKER_KNOWS["command_interface"]), ("המחלקה הקונקרטית של ה-Receiver", INVOKER_KNOWS["concrete_receiver"]),
                     ("שום דבר", INVOKER_KNOWS["nothing"]), ("הרשימה המלאה", INVOKER_KNOWS["observer_list"])])
ok = undo_stack_ok()
R.mcq(qs, "P06-Q3", [("ה-Invoker שומר", ok), ("ה-Receiver שומר עותק", False), ("מצביע ל-Subject", False), ("Factory יוצר מחדש", False)])

# P07
exp7 = {"CartScreen": "View", "CartController": "Controller", "Cart": "Model"}
c7 = [{"CartScreen": "View", "CartController": "Controller", "Cart": "Model"}, {"CartScreen": "Controller", "CartController": "Model", "Cart": "View"},
      {"CartScreen": "Model", "CartController": "View", "Cart": "Controller"}, {"CartScreen": "Model", "CartController": "Controller", "Cart": "View"}]
R.mcq(qs, "P07-Q1", [("View: CartScreen", c7[0] == exp7), ("Controller: CartScreen", c7[1] == exp7), ("View: CartController", c7[2] == exp7),
                     ("Model: CartScreen", c7[3] == exp7)])
R.mcq(qs, "P07-Q2", [("Controller מקבל", mvc_edge_allowed("View", "Controller") and mvc_edge_allowed("Controller", "Model")),
                     ("View מעדכן ישירות", mvc_edge_allowed("View", "Model")),
                     ("Model מעדכן את ה-Controller ואז את עצמו", False), ("Factory יוצר Controller", False)])
BENEFIT = {"view_swap_without_model_change": True, "model_view_same_class": False, "controller_singleton": False, "no_bugs": False}
R.mcq(qs, "P07-Q3", [("להחליף או להוסיף View", BENEFIT["view_swap_without_model_change"]), ("אותה מחלקה", BENEFIT["model_view_same_class"]),
                     ("Singleton", BENEFIT["controller_singleton"]), ("אף באג", BENEFIT["no_bugs"])])

# P08
R.mcq(qs, "P08-Q1", [("Chain", solves("Chain", {"first_capable_handles"})), ("Flyweight", solves("Flyweight", {"first_capable_handles"})),
                     ("Singleton", solves("Singleton", {"first_capable_handles"})), ("Abstract Factory", solves("AbstractFactory", {"first_capable_handles"}))])
R.mcq(qs, "P08-Q2", [("Flyweight", solves("Flyweight", {"many_similar_objects_memory"})), ("Command", solves("Command", {"many_similar_objects_memory"})),
                     ("Observer", solves("Observer", {"many_similar_objects_memory"})), ("Mediator", solves("Mediator", {"many_similar_objects_memory"}))])
R.mcq(qs, "P08-Q3", [("Mediator", solves("Mediator", {"central_communication"})), ("Singleton", solves("Singleton", {"central_communication"})),
                     ("Factory", solves("Factory", {"central_communication"})), ("Chain", solves("Chain", {"central_communication"}))])

R.finish(qs)
