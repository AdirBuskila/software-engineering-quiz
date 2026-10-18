"""Offline checker for the testing course (tst).

Counts are computed by enumerating the code that appears in the questions (each Java snippet is mirrored by a
Python function with a trace): boundary values come from scanning the inputs for output changes, equivalence
classes are the distinct outputs, path / statement / branch coverage are found by brute force over the inputs.
JUnit lifecycle is simulated. Concept questions use a small rule table.
Run:  python tools/verify/needhelp/tst/check.py
"""
import itertools, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import load_questions, Report

qs = load_questions("tst")
R = Report("tst")

# ---------------- T01: levels ----------------
RUNS_CODE = {"inspection": False, "unit": True, "integration": True, "system": True}
R.mcq(qs, "T01-Q1", [("Inspection", not RUNS_CODE["inspection"]), ("Unit test", not RUNS_CODE["unit"]),
                     ("Integration test", not RUNS_CODE["integration"]), ("System test", not RUNS_CODE["system"])])
def level(n_units, whole_system=False, with_customer=False, runs_code=True):
    if not runs_code: return "inspection"
    if with_customer: return "acceptance"
    if whole_system: return "system"
    return "unit" if n_units == 1 else "integration"
lv = level(2)           # OrderService + PaymentService, each tested before
R.mcq(qs, "T01-Q2", [("Integration test", lv == "integration"), ("Unit test", lv == "unit"), ("Acceptance test", lv == "acceptance"), ("Inspection", lv == "inspection")])
ZERO_BUGS_GUARANTEED = False
R.mcq(qs, "T01-Q3", [("לא, אין הבטחה", not ZERO_BUGS_GUARANTEED), ("כן, בדיקות שילוב", ZERO_BUGS_GUARANTEED),
                     ("כן, אבל רק במערכות תוכנה", ZERO_BUGS_GUARANTEED), ("תלוי אם הבדיקות נכתבו ב-JUnit", False)])

# ---------------- T02: V-model ----------------
PLAN_ORDER = ["acceptance", "system", "unit"]          # planned along the left leg: requirements -> design -> modules
EXEC_ORDER = list(reversed(PLAN_ORDER))                # executed after coding, small to large
STAGE = {"acceptance": "requirements", "unit": "module design"}
R.mcq(qs, "T02-Q1", [("בדיקות קבלה", PLAN_ORDER[0] == "acceptance" and EXEC_ORDER[-1] == "acceptance"),
                     ("בדיקות יחידה", PLAN_ORDER[0] == "unit" and EXEC_ORDER[-1] == "unit"),
                     ("בדיקות אינטגרציה", PLAN_ORDER[0] == "integration"), ("סקירת קוד", False)])
unit_exec = "first" if EXEC_ORDER[0] == "unit" else "last"
opts = [("module design", "first"), ("requirements", "last"), ("module design", "last"), ("requirements", "first")]
R.mcq(qs, "T02-Q2", [("מול עיצוב המודולים, ומבוצעות ראשונות", opts[0] == (STAGE["unit"], unit_exec)),
                     ("מול ניתוח הדרישות, ומבוצעות אחרונות", opts[1] == (STAGE["unit"], unit_exec)),
                     ("מול עיצוב המודולים, ומבוצעות אחרונות", opts[2] == (STAGE["unit"], unit_exec)),
                     ("מול ניתוח הדרישות, ומבוצעות ראשונות", opts[3] == (STAGE["unit"], unit_exec))])
MODELS = {"V": {"test_per_stage": True, "tests_grouped_at_end": False}, "Waterfall": {"test_per_stage": False, "tests_grouped_at_end": True}}
R.mcq(qs, "T02-Q3", [("ב-V כל שלב פיתוח מקושר", MODELS["V"]["test_per_stage"] and MODELS["Waterfall"]["tests_grouped_at_end"]),
                     ("ב-Waterfall כל שלב מקושר", MODELS["Waterfall"]["test_per_stage"]), ("ב-V אין בדיקות כלל", False),
                     ("בדיקות מתבצעות לפני הקידוד", False)])

# ---------------- T03: JUnit simulation ----------------
def run_junit(tests, before=None, after=None):
    log = []
    for t in tests:
        if before: log.append(before)
        log.append(t)
        if after: log.append(after)
    return log
log = run_junit(["t1", "t2", "t3"], "setup", "teardown")
n_setup = log.count("setup")
R.mcq(qs, "T03-Q1", [("3", n_setup == 3), ("1", n_setup == 1), ("4", n_setup == 4), ("0", n_setup == 0)])
def valid_plan(place):                    # place: action -> phase; phases run setup < test < teardown
    rank = {"setup": 0, "test": 1, "teardown": 2}
    order = [a for a, _ in sorted(place.items(), key=lambda kv: rank[kv[1]])]
    return order == ["create", "total", "cleanup"]
plans = [{"create": "setup", "total": "test", "cleanup": "teardown"}, {"total": "setup", "create": "test", "cleanup": "teardown"},
         {"create": "teardown", "total": "test", "cleanup": "setup"}, {"create": "test", "cleanup": "setup", "total": "teardown"}]
R.mcq(qs, "T03-Q2", [("יוצרים את העגלה ב-setup, מפעילים", valid_plan(plans[0])), ("מפעילים total() ב-setup", valid_plan(plans[1])),
                     ("יוצרים את העגלה ב-tearDown", valid_plan(plans[2])), ("יוצרים את העגלה ב-@Test, מנקים", valid_plan(plans[3]))])
add = lambda a, b: a + b
passes = (7 == add(2, 3))
R.mcq(qs, "T03-Q3", [("הבדיקה נכשלת: הערך המצופה 7", not passes), ("הבדיקה עוברת, כי 2 ועוד 3", passes),
                     ("נכשלת בקומפילציה", False), ("בודקת רק אם הערך שונה מאפס", False)])

# ---------------- T04: mock ----------------
DEPS = {"TicketService": {"AIService"}, "OrderService": {"PaymentGateway"}}
R.mcq(qs, "T04-Q1", [("לא לחייב כרטיסים אמיתיים", True), ("לבדוק את מהירות שער התשלום", False), ("OrderService תימחק", False), ("לשכפל את סביבת הייצור", False)])
R.mcq(qs, "T04-Q2", [("Mock של AIService", "AIService" in DEPS["TicketService"]), ("Mock של TicketService", "TicketService" in DEPS["TicketService"]),
                     ("Mock של מסד הנתונים כולו", "Database" in DEPS["TicketService"]), ("אין צורך ב-Mock", False)])
CONTAINS = {("unit", "mock")}
R.mcq(qs, "T04-Q3", [("היחידה הנבדקת מכילה", ("unit", "mock") in CONTAINS), ("ה-Mock מכיל", ("mock", "unit") in CONTAINS),
                     ("ה-Mock הוא פונקציה", False), ("יורשת מה-Mock", False)])

# ---------------- T05: boundary values and equivalence classes ----------------
def shipping_fee(total): return 0 if total >= 200 else 30
def discount(total): return 10 if total >= 1000 else (5 if total >= 500 else 0)
def thresholds(f, lo=0, hi=3000):
    return [t for t in range(lo + 1, hi) if f(t) != f(t - 1)]
th1, th2 = thresholds(shipping_fee), thresholds(discount)
assert th1 == [200] and th2 == [500, 1000], (th1, th2)
def straddles(f, pair):                   # the two values are adjacent and on opposite sides of a threshold
    a, b = sorted(pair)
    return b == a + 1 and f(a) != f(b)
def covers_all(f, values):                # both sides of every threshold are tested
    return all({t - 1, t} <= set(values) for t in thresholds(f))
R.mcq(qs, "T05-Q1", [("199 ו-200", straddles(shipping_fee, (199, 200))), ("50 ו-100", straddles(shipping_fee, (50, 100))),
                     ("500 ו-1000", straddles(shipping_fee, (500, 1000))), ("0 ו-1", straddles(shipping_fee, (0, 1)))])
R.mcq(qs, "T05-Q2", [("499, 500, 999, 1000", covers_all(discount, [499, 500, 999, 1000])), ("100, 700, 2000", covers_all(discount, [100, 700, 2000])),
                     ("0, 250, 750", covers_all(discount, [0, 250, 750])), ("500, 600, 700, 800", covers_all(discount, [500, 600, 700, 800]))])
classes = len({discount(t) for t in range(0, 3000)})
R.mcq(qs, "T05-Q3", [("3", classes == 3), ("2", classes == 2), ("4", classes == 4), ("1000", classes == 1000)])
mutant = lambda total: 0 if total > 200 else 30           # the classic bug: > instead of >=
diff = [t for t in range(0, 10001) if mutant(t) != shipping_fee(t)]
R.mcq(qs, "T05-Q4", [("באגים נוטים להסתתר", diff == [200]), ("אינם חוקיים ב-JUnit", False), ("תמיד גדולים מאלפיים", False), ("אין טעם לבדוק", False)])

# ---------------- T06: paths and coverage ----------------
def f_trace(x, y):                        # int f(x,y){ r=0; if(x>0) r+=1; if(y>0) r+=2; return r; }
    stm, br = {"r=0"}, []
    if x > 0: stm.add("r+=1"); br.append(("if1", True))
    else: br.append(("if1", False))
    if y > 0: stm.add("r+=2"); br.append(("if2", True))
    else: br.append(("if2", False))
    stm.add("return")
    return stm, tuple(br)
DOMAIN = list(itertools.product([-1, 1], repeat=2))
paths = {f_trace(*d)[1] for d in DOMAIN}
ALL_STM = {"r=0", "r+=1", "r+=2", "return"}
ALL_BR = {("if1", True), ("if1", False), ("if2", True), ("if2", False)}
def min_tests(goal):
    for k in range(1, len(DOMAIN) + 1):
        for subset in itertools.combinations(DOMAIN, k):
            if goal(subset): return k
stm_cov = lambda s: set().union(*(f_trace(*d)[0] for d in s)) == ALL_STM
br_cov = lambda s: {b for d in s for b in f_trace(*d)[1]} == ALL_BR
npaths, k_stm, k_br = len(paths), min_tests(stm_cov), min_tests(br_cov)
R.mcq(qs, "T06-Q1", [("4", npaths == 4), ("2", npaths == 2), ("3", npaths == 3), ("8", npaths == 8)])
R.mcq(qs, "T06-Q2", [("1", k_stm == 1), ("2", k_stm == 2), ("3", k_stm == 3), ("4", k_stm == 4)])
R.mcq(qs, "T06-Q3", [("2", k_br == 2), ("1", k_br == 1), ("3", k_br == 3), ("4", k_br == 4)])
def nested(a, b):                          # if (a) { if (b) S1 else S2 } else S3
    return ("a", "b", "S1") if a and b else (("a", "nb", "S2") if a else ("na", "S3"))
npaths2 = len({nested(a, b) for a in (False, True) for b in (False, True)})
R.mcq(qs, "T06-Q4", [("3", npaths2 == 3), ("4", npaths2 == 4), ("2", npaths2 == 2), ("6", npaths2 == 6)])

# ---------------- T07: concept questions ----------------
TDD = ["write_failing_test", "write_minimal_code", "refactor"]
seqs = [["write_failing_test", "write_minimal_code", "refactor"], ["write_all_code", "write_all_tests", "delete_failed_tests"],
        ["write_code", "refactor", "test_once"], ["write_full_docs", "code_and_tests"]]
R.mcq(qs, "T07-Q1", [("כותבים בדיקה שנכשלת", seqs[0] == TDD), ("כותבים את כל הקוד", seqs[1] == TDD),
                     ("כותבים קוד, משפרים", seqs[2] == TDD), ("כותבים תיעוד מלא", seqs[3] == TDD)])
REVIEW = {"code review": "code quality", "design review": "architecture quality"}
R.mcq(qs, "T07-Q2", [("בדיקת איכות הקוד", REVIEW["code review"] == "code quality"), ("בדיקות ביצועים", False),
                     ("בדיקת האינטגרציה", False), ("הרצת בדיקות יחידה", False)])
R.mcq(qs, "T07-Q3", [("בדיקת איכות הארכיטקטורה", REVIEW["design review"] == "architecture quality"), ("איכות שורות הקוד", REVIEW["design review"] == "code quality"),
                     ("בדיקת הדרישות מול הלקוח", False), ("בדיקות עומס", False)])

R.finish(qs)
