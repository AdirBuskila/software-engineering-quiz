# -*- coding: utf-8 -*-
"""App configuration for the video engine (tools/video/vid.py and friends)."""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parents[1]

APP_NAME = "הנדסת תוכנה"
COURSE_CODE = ""
SITE = "https://adirbuskila.github.io/software-engineering-quiz/"
BANK = "questions.json"
SIM_PATHS = ["tools/verify/needhelp"]

# same order, names and icons as course-ui.js META
COURSES = [
    ("pat", "תבניות עיצוב", "🧩"),
    ("uml", "UML ומידול", "📐"),
    ("tst", "בדיקות תוכנה", "🧪"),
    ("proc", "תהליכים, Agile ודרישות", "🧭"),
]

BONUS_GOAL = {}

SRC = ROOT / "courses"
REF = re.compile(r'ref:\s*"([^"]+)"')


def quiz_ids():
    """bank ids used by any guided-course quiz (each level quizzes one, a boss level six): never solved in a video"""
    return {m.group(1) for f in SRC.glob("*/*.js") for m in REF.finditer(f.read_text(encoding="utf-8"))}


def boss_ids():
    return quiz_ids()


def is_boss(video_id):
    hits = list(SRC.glob(f"*/{video_id[:3]}.js"))
    return bool(hits) and re.search(r"boss:\s*true", hits[0].read_text(encoding="utf-8")) is not None


def level_goal(course, level_id):
    f = SRC / course / f"{level_id}.js"
    m = re.search(r'goal:\s*"([^"]*)"', f.read_text(encoding="utf-8")) if f.exists() else None
    return m.group(1) if m else ""
