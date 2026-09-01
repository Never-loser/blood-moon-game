"""Bilingual data for the level-2 exam sheets.

Each question is either:
  {"type": "radio",   "text": {en/fa}, "options": [{"en","fa","correct"}]}
  {"type": "entry",   "text": {en/fa}, "answers": [...], "image": path|None}
"""
from __future__ import annotations

from .config import PICTURES_DIR
import os


def _img(name: str) -> str:
    return os.path.join(PICTURES_DIR, name)


QUIZZES = {
    "math": {
        "sheet_title": {"en": "Exam Sheet", "fa": "برگ امتحانی"},
        "questions": [
            {
                "type": "radio",
                "text": {
                    "en": "About 500 years ago, ____ introduced the quantity ____\nto describe the motion of a moving object:",
                    "fa": "درحدود ۵۰۰ سال قبل ____ برای توصیف حرکت یک متحرک\nکمیت ____ را معرفی کرد",
                },
                "options": [
                    {"en": "Galileo - average speed", "fa": "گالیله - تندی متوسط", "correct": True},
                    {"en": "Newton - instantaneous speed", "fa": "نیوتون - تندی لحظه‌ای", "correct": False},
                    {"en": "Newton - average speed", "fa": "نیوتون - تندی موسط", "correct": False},
                    {"en": "Galileo - instantaneous speed", "fa": "گالیله - تندی لحظه‌ای", "correct": False},
                ],
            },
            {
                "type": "entry",
                "text": {"en": "Find x in the expression below:", "fa": "x را در عبارت زیر بیابید:"},
                "image": _img("q1.png"),
                "answers": ["776/777"],
            },
            {
                "type": "entry",
                "text": {"en": "Solve:", "fa": "حل کن:"},
                "image": _img("q3.png"),
                "answers": ["3", "۳"],
            },
        ],
    },
    "biology": {
        "sheet_title": {"en": "Exam Sheet", "fa": "برگ امتحانی"},
        "questions": [
            {
                "type": "radio",
                "text": {"en": "What is the scientific name of the house cricket?", "fa": "نام علمی قمری خانگی کدام است؟"},
                "options": [
                    {"en": "Sterptoelia sengalensis", "fa": "Sterptoelia sengalensis", "correct": True},
                    {"en": "Sterptoelia Sengalensis", "fa": "Sterptoelia Sengalensis", "correct": False},
                    {"en": "Streptoeila sengalensis", "fa": "Streptoeila sengalensis", "correct": False},
                    {"en": "terptoelia sengalensis", "fa": "terptoelia sengalensis", "correct": False},
                ],
            },
            {
                "type": "radio",
                "text": {
                    "en": ("Being eukaryotic, multicellular and rich in vitamins\nare properties of which organism?"),
                    "fa": ("یوکاریوت بودن و پرسلولی بودن و داشتن ویتامین زیاد\nاز ویژگی‌های جانداری است که:"),
                },
                "options": [
                    {"en": "produces toxin in canned food", "fa": "در کنسرو سم تولید می‌کند", "correct": False},
                    {"en": "causes COVID-19", "fa": "بیماری کووید ۱۹ ایجاد می‌کند", "correct": False},
                    {"en": "agar is produced from it", "fa": "از آن آگار تهیه می‌شود", "correct": True},
                    {"en": "causes wheat rust", "fa": "باعث زنگ گندم می‌شود", "correct": False},
                ],
            },
            {
                "type": "radio",
                "text": {"en": "Which disease agent has no cellular structure?", "fa": "عامل کدام بیماری ساختمان سلولی ندارد؟"},
                "options": [
                    {"en": "Tuberculosis", "fa": "سل", "correct": False},
                    {"en": "Diphtheria", "fa": "دیفتری", "correct": False},
                    {"en": "AIDS", "fa": "ایدز", "correct": True},
                    {"en": "Malaria", "fa": "مالاریا", "correct": False},
                ],
            },
        ],
    },
    "chemistry": {
        "sheet_title": {"en": "Exam Sheet", "fa": "برگ امتحانی"},
        "questions": [
            {
                "type": "radio",
                "text": {
                    "en": "Placing a strip of metal ____ into a solution of ____\ncauses no reaction:",
                    "fa": "با قرار دادن تیغه‌ای از فلز ----- در محلول ------\nهیچ واکنشی رخ نمی‌دهد",
                },
                "options": [
                    {"en": "iron - copper sulfate", "fa": "آهن - مس سولفات", "correct": False},
                    {"en": "zinc - magnesium sulfate", "fa": "روی - منیزیم سولفات", "correct": True},
                    {"en": "magnesium - zinc sulfate", "fa": "منیزیم - روی سولفات", "correct": False},
                    {"en": "magnesium - iron sulfate", "fa": "منیزیم - آهن سولفات", "correct": False},
                ],
            },
            {
                "type": "radio",
                "text": {"en": "Which ion is written correctly?", "fa": "نشانه شیمیایی کدام یون به درستی نشان داده شده است؟"},
                "options": [
                    {"en": "Na +", "fa": "+ Na", "correct": False},
                    {"en": "Mg +2", "fa": "Mg +2", "correct": False},
                    {"en": "Fe 2+", "fa": "2+ Fe", "correct": False},
                    {"en": "O 2-", "fa": "O 2-", "correct": True},
                ],
            },
            {
                "type": "radio",
                "text": {
                    "en": "Which of the following hydrocarbons has the highest boiling point?",
                    "fa": "نقطه جوش کدام یک از هیدروکربن‌های زیر از سایرین بالاتر است؟",
                },
                "options": [
                    {"en": "butane", "fa": "بوتان", "correct": False},
                    {"en": "ethane", "fa": "اتان", "correct": False},
                    {"en": "octane", "fa": "اکتان", "correct": True},
                    {"en": "methane", "fa": "متان", "correct": False},
                ],
            },
        ],
    },
}


# 15x20 maze. 1 = wall, 0 = corridor, 2 = goal.
MAZE_MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1],
    [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2],
]

# Animated hazards: (row, col, d_row, d_col). They bounce off walls.
MAZE_OBSTACLES = [
    (4, 3, 0, 1),
    (5, 5, 1, 0),
    (6, 10, 0, 1),
    (8, 8, -1, 0),
    (10, 2, 0, 1),
]
