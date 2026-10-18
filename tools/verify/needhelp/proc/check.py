"""Offline checker for the process / Agile / requirements course (proc).

Rule tables: SE vs CS areas, which process model suits which project trait, the Agile practices behind each manifesto
line, Scrum roles and events, backlog containment, and a functional / non-functional classifier driven by explicit
attributes of each requirement statement. Each original question states one claim per option; the keyed option must be
the only defensible one.   Run:  python tools/verify/needhelp/proc/check.py
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common import load_questions, Report

qs = load_questions("proc")
R = Report("proc")

# ---------------- R01 ----------------
AREA = {"maintenance": "SE", "computational_complexity": "CS", "math_proofs": "CS", "semiconductor_physics": "physics"}
R.mcq(qs, "R01-Q1", [("תחזוקה של מערכות", AREA["maintenance"] == "SE"), ("מורכבות חישובית", AREA["computational_complexity"] == "SE"),
                     ("הוכחת נכונות", AREA["math_proofs"] == "SE"), ("מוליכים למחצה", AREA["semiconductor_physics"] == "SE")])
COST_PEAK = "after_delivery"
R.mcq(qs, "R01-Q2", [("אחרי שהיא כבר בשימוש", COST_PEAK == "after_delivery"), ("בכתיבת הגרסה הראשונה", COST_PEAK == "first_version"),
                     ("בשלב הבדיקות לפני המסירה", COST_PEAK == "testing"), ("העלות זהה", COST_PEAK == "uniform")])
def product(sold_to_many, vendor_sets_requirements):
    return ("Generic" if sold_to_many else "Customized", "vendor" if vendor_sets_requirements else "customer")
truth = product(True, True)
R.mcq(qs, "R01-Q3", [("Generic product, והיצרן", ("Generic", "vendor") == truth), ("Customized product, והלקוח", ("Customized", "customer") == truth),
                     ("Generic product, והלקוח הבודד", ("Generic", "customer") == truth), ("Customized product, והיצרן", ("Customized", "vendor") == truth)])

# ---------------- R02 ----------------
SUITS = {"Waterfall": {"stable_reqs", "fixed_deadlines", "control"}, "PlanDriven": {"stable_reqs", "fixed_deadlines", "control"},
         "BuildFix": {"poc"}, "Agile": {"changing_reqs"}}
fits = lambda m, needs: set(needs) <= SUITS[m]
n1 = {"stable_reqs", "control"}
R.mcq(qs, "R02-Q1", [("Waterfall / Plan Driven", fits("Waterfall", n1) and fits("PlanDriven", n1)), ("Build and Fix", fits("BuildFix", n1)),
                     ("פיתוח ללא תכנון", False), ("אב טיפוס שנזרק", False)])
R.mcq(qs, "R02-Q2", [("Build and Fix, להוכחת יכולת", fits("BuildFix", {"poc"})), ("Waterfall מלא", fits("Waterfall", {"poc"})),
                     ("Plan Driven עם תוכנית", fits("PlanDriven", {"poc"})), ("אף שיטה", False)])
BAD_FOR_WATERFALL = {"changing_reqs"}
R.mcq(qs, "R02-Q3", [("דרישות שעשויות להשתנות", "changing_reqs" in BAD_FOR_WATERFALL), ("דרישות מוגדרות היטב", "stable_reqs" in BAD_FOR_WATERFALL),
                     ("לקוח שמשתף פעולה", "cooperative_client" in BAD_FOR_WATERFALL), ("לוחות זמנים קשיחים", "fixed_deadlines" in BAD_FOR_WATERFALL)])

# ---------------- R03 ----------------
PRACTICE = {"working_software_over_docs": "short_cycles_and_demos"}
R.mcq(qs, "R03-Q1", [("זמני פיתוח קצרים", PRACTICE["working_software_over_docs"] == "short_cycles_and_demos"), ("ביטול מוחלט", PRACTICE["working_software_over_docs"] == "no_docs"),
                     ("מסמך דרישות שמתעדכן", PRACTICE["working_software_over_docs"] == "annual_doc"), ("Scrum Master שמתעדף", PRACTICE["working_software_over_docs"] == "sm_prioritizes")])
FACTS = {"waterfall_suits_fixed_spec": True, "agile_suits_fixed_reqs": False, "waterfall_easy_to_change": False, "agile_predicts_budget_exactly": False,
         "agile_predicts_better": False, "agile_flexible": True, "waterfall_phases_easier_to_manage": True, "agile_team_has_all_roles": True}
R.mcq(qs, "R03-Q2", [("Waterfall מתאים יותר", FACTS["waterfall_suits_fixed_spec"]), ("Agile מתאים יותר לפרויקט שבו הדרישות קבועות", FACTS["agile_suits_fixed_reqs"]),
                     ("ב-Waterfall קל יותר להגיב", FACTS["waterfall_easy_to_change"]), ("ב-Agile אפשר לחזות", FACTS["agile_predicts_budget_exactly"])])
R.mcq(qs, "R03-Q3", [("בפיתוח אג'ילי קל יותר לחזות", FACTS["agile_predicts_better"]), ("פיתוח אג'ילי גמיש", FACTS["agile_flexible"]),
                     ("בפיתוח מפל מים שלבי הפרויקט קלים", FACTS["waterfall_phases_easier_to_manage"]), ("בצוות אג'ילי יש", FACTS["agile_team_has_all_roles"])], mode="false")

# ---------------- R04 ----------------
OWNER = {"set_priorities": "Product Owner", "remove_impediments": "Scrum Master", "product_vision": "Product Owner", "manage_scrum_process": "Scrum Master"}
SCRUM_ROLES = {"Product Owner", "Scrum Master", "Team"}
R.mcq(qs, "R04-Q1", [("Product Owner", OWNER["set_priorities"] == "Product Owner"), ("Scrum Master", OWNER["set_priorities"] == "Scrum Master"),
                     ("צוות הפיתוח, בהצבעת רוב", False), ("Project Manager", "Project Manager" in SCRUM_ROLES)])
R.mcq(qs, "R04-Q2", [("Scrum Master", OWNER["remove_impediments"] == "Scrum Master"), ("Product Owner", OWNER["remove_impediments"] == "Product Owner"),
                     ("Team Leader", "Team Leader" in SCRUM_ROLES), ("כל חבר צוות אחר", False)])
SM_TASKS = {"remove_impediments", "ensure_scrum_followed", "manage_scrum_process"}
R.mcq(qs, "R04-Q3", [("להגדיר את חזון המוצר", "product_vision" in SM_TASKS), ("להסיר חסמים", "remove_impediments" in SM_TASKS),
                     ("שהצוות מבין ומקיים", "ensure_scrum_followed" in SM_TASKS), ("לנהל את תהליך ה-Scrum", "manage_scrum_process" in SM_TASKS)], mode="false")

# ---------------- R05 ----------------
EVENT = {"plan_next_sprint": "Sprint Planning", "daily_status": "Daily Scrum", "show_completed": "Sprint Review", "improve_process": "Sprint Retrospective"}
R.mcq(qs, "R05-Q1", [("Sprint Planning", EVENT["plan_next_sprint"] == "Sprint Planning"), ("Daily Scrum", EVENT["plan_next_sprint"] == "Daily Scrum"),
                     ("Sprint Review", EVENT["plan_next_sprint"] == "Sprint Review"), ("Sprint Retrospective", EVENT["plan_next_sprint"] == "Sprint Retrospective")])
DAILY = {"minutes": (10, 20), "when": "start_of_day", "purpose": "status", "exists": True}
R.mcq(qs, "R05-Q2", [("10 ל-20 דקות בתחילת היום", DAILY["minutes"] == (10, 20) and DAILY["when"] == "start_of_day" and DAILY["purpose"] == "status"),
                     ("כשעה בסוף היום", DAILY["when"] == "end_of_day"), ("פעם בשבועיים", DAILY["when"] == "biweekly"), ("אין פגישה כזו", not DAILY["exists"])])
R.mcq(qs, "R05-Q3", [("Sprint Review", EVENT["show_completed"] == "Sprint Review"), ("Sprint Planning", EVENT["show_completed"] == "Sprint Planning"),
                     ("Daily Scrum", EVENT["show_completed"] == "Daily Scrum"), ("Sprint Retrospective", EVENT["show_completed"] == "Sprint Retrospective")])

# ---------------- R06 ----------------
product_backlog = {"pbi1", "pbi2", "pbi3", "pbi4", "pbi5"}
sprint_backlog = {"pbi1", "pbi3"}
R.mcq(qs, "R06-Q1", [("ה-Product Backlog מכיל את ה-Sprint Backlog", sprint_backlog < product_backlog), ("ה-Sprint Backlog מכיל את כל", product_backlog < sprint_backlog),
                     ("אין קשר", not (sprint_backlog & product_backlog)), ("שני שמות לאותה רשימה", sprint_backlog == product_backlog)])
def mid_sprint_action(changes_sprint_goal):
    return "product_backlog_then_next_sprint" if changes_sprint_goal else "team_decides"
act = mid_sprint_action(True)
R.mcq(qs, "R06-Q2", [("ה-Product Owner מכניס אותה ל-Product Backlog", act == "product_backlog_then_next_sprint"), ("מוסיפים אותה מיד לספרינט", act == "add_now"),
                     ("מבטלים את הספרינט", act == "cancel_sprint"), ("הצוות עוצר הכל", act == "stop_all")])
ESTIMATION = "story_points_discussion"
R.mcq(qs, "R06-Q3", [("בדיון על User Story Points", ESTIMATION == "story_points_discussion"), ("בשעות מדויקות", ESTIMATION == "exact_hours_once"),
                     ("המנהל קובע לבדו", ESTIMATION == "manager_alone"), ("אי אפשר לשערך", ESTIMATION == "impossible")])

# ---------------- R07: classifier driven by explicit attributes ----------------
def classify(is_action, is_quality_or_constraint):
    return "functional" if is_action and not is_quality_or_constraint else "non-functional"
REQ = {  # statement -> (describes an action the system performs, states a quality / limit / technology constraint)
    "send_sms_reminder": (True, False), "report_in_3s": (True, True), "aes_passwords": (False, True), "search_by_name": (True, False),
    "confirmation_email": (True, False), "cancel_order": (True, False), "home_under_2s_95": (False, True)}
R.mcq(qs, "R07-Q1", [("א פונקציונלית, ב לא פונקציונלית", classify(*REQ["send_sms_reminder"]) == "functional" and classify(*REQ["report_in_3s"]) == "non-functional"),
                     ("א לא פונקציונלית, ב פונקציונלית", classify(*REQ["send_sms_reminder"]) == "non-functional" and classify(*REQ["report_in_3s"]) == "functional"),
                     ("שתיהן פונקציונליות", classify(*REQ["send_sms_reminder"]) == "functional" and classify(*REQ["report_in_3s"]) == "functional"),
                     ("שתיהן לא פונקציונליות", classify(*REQ["send_sms_reminder"]) == "non-functional" and classify(*REQ["report_in_3s"]) == "non-functional")])
R.mcq(qs, "R07-Q2", [("AES-256", classify(*REQ["aes_passwords"]) == "non-functional"), ("לחפש מוצרים לפי שם", classify(*REQ["search_by_name"]) == "non-functional"),
                     ("אימייל אישור", classify(*REQ["confirmation_email"]) == "non-functional"), ("לבטל הזמנה", classify(*REQ["cancel_order"]) == "non-functional")])
measurable = True   # contains a number: 2 seconds, 95%
R.mcq(qs, "R07-Q3", [("דרישה לא פונקציונלית (ביצועים)", classify(*REQ["home_under_2s_95"]) == "non-functional" and measurable),
                     ("דרישה פונקציונלית, כי היא מתארת", classify(*REQ["home_under_2s_95"]) == "functional"),
                     ("דרישה לא חוקית כי אי אפשר למדוד", not measurable), ("רק בסוף הפיתוח", False)])

# ---------------- R08 ----------------
def good_requirement(testable, describes_what_not_how):
    return testable and describes_what_not_how
R.mcq(qs, "R08-Q1", [("לא דרישה טובה, כי היא עמומה", not good_requirement(False, True)), ("דרישה טובה, כי היא מתארת", good_requirement(False, True)),
                     ("דרישה פונקציונלית שיש להעביר", good_requirement(False, True)), ("רק אם האפליקציה כתובה", False)])
R.mcq(qs, "R08-Q2", [("לא דרישה טובה, כי היא מתייחסת לאופן המימוש", not good_requirement(True, False)), ("דרישה טובה, כי היא מבהירה", good_requirement(True, False)),
                     ("דרישה פונקציונלית חשובה", good_requirement(True, False)), ("רק למערכות שרת-לקוח", False)])
ELICITATION = {"interviews", "observation", "existing_systems", "use_cases"}
R.mcq(qs, "R08-Q3", [("ראיונות ותצפית", {"interviews", "observation"} <= ELICITATION), ("Sprint Retrospective", "retrospective" in ELICITATION),
                     ("בדיקת יחידה", "unit_test" in ELICITATION), ("סקירת קוד של מפתחי הצוות", "code_review" in ELICITATION)])

R.finish(qs)
