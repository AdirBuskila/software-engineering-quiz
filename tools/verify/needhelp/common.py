"""Shared helpers for the "צריך עזרה?" offline checkers.

Every checker loads the course questions straight from the level files (through
`node tools/course_check.js --json`), so a changed option text, answer index or
question id cannot slip past a checker. A rule-table checker states, for each option
of a question, an ANCHOR (a substring that must occur in that option's text) and a TRUTH
value computed from a small rule table. It then asserts that exactly the keyed option
is the defensible one.
"""
import json, os, subprocess, sys, tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


def load_questions(course):
    out = os.path.join(tempfile.gettempdir(), "needhelp_%s.json" % course)
    subprocess.run(["node", os.path.join(ROOT, "tools", "course_check.js"), "--json", out],
                   check=True, stdout=subprocess.DEVNULL, cwd=ROOT)
    with open(out, encoding="utf-8") as f:
        items = json.load(f)
    return {q["id"]: q for q in items if q["course"] == course and not q.get("ref")}


class Report:
    def __init__(self, name):
        self.name, self.n, self.fails, self.seen = name, 0, [], set()

    def fail(self, qid, msg):
        self.fails.append("%s: %s" % (qid, msg))

    def mcq(self, qs, qid, claims, mode="true"):
        """claims: [(anchor, truth)] in option order. mode 'true': the keyed option is the only TRUE claim;
        mode 'false': the keyed option is the only FALSE claim (a 'which is NOT / wrong' question)."""
        self.n += 1
        self.seen.add(qid)
        q = qs.get(qid)
        if q is None:
            return self.fail(qid, "question not found in the course files")
        if len(claims) != len(q["options"]):
            return self.fail(qid, "%d claims for %d options" % (len(claims), len(q["options"])))
        for i, ((anchor, _), opt) in enumerate(zip(claims, q["options"])):
            if anchor not in opt:
                self.fail(qid, "claim %d anchor %r is not in option text %r" % (i, anchor, opt))
        want = mode == "true"
        good = [i for i, (_, t) in enumerate(claims) if bool(t) == want]
        if good != [q["answer"]]:
            self.fail(qid, "rule table says option(s) %s are correct, the course keys %d" % (good, q["answer"]))

    def eq(self, qid, cond, msg):
        self.n += 1
        self.seen.add(qid)
        if not cond:
            self.fail(qid, msg)

    def finish(self, qs):
        for qid in qs:
            if qid not in self.seen:
                self.fail(qid, "no check covers this question")
        if self.fails:
            print("\n".join("FAIL " + f for f in self.fails))
            print("%s: %d check(s), %d FAILED" % (self.name, self.n, len(self.fails)))
            sys.exit(1)
        print("%s: %d check(s) passed" % (self.name, self.n))
