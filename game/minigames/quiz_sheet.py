"""Data-driven exam sheet used for the math, biology and chemistry tests.

Replaces the three near-identical fullscreen quiz windows of the old code.
"""
from __future__ import annotations

import tkinter as tk

from ..i18n import tr
from ..quiz_data import QUIZZES
from ..widgets import load_photo
from .base import Minigame

# The exam sheet deliberately stays light: it is a prop, a piece of paper
# lying in a dark room. Aged-paper tones rather than the old clinical white.
SHEET_BG = "#f2ebdb"
HEADER_FG = "#3b2d1c"
HEADER_BG = "#e2d6bb"
ENTRY_BG = "#fbf7ec"

CORRECT_FG = "#1c7a43"
WRONG_FG = "#a3271f"
INK = "#2b2117"

# Widest a question image may be drawn. q3.png ships at 772px, which used to
# blow its grid column out and squeeze the other two questions into slivers.
MAX_IMAGE_WIDTH = 330


def normalize(text: str) -> str:
    return (text.strip().lower()
            .replace("ي", "ی").replace("ك", "ک")
            .replace("٫", "/").replace(",", "."))


class QuizSheet(Minigame):
    def __init__(self, app, subject: str):
        super().__init__(app, size=(1180, 540))
        self.data = QUIZZES[subject]
        self.title(self.sheet_title())

        self.correct_flags: list[bool] = [False] * len(self.questions)
        self.status_labels: list[tk.Label] = []

        header = tk.Label(self, text=self.sheet_title(),
                          font=("IranNastaliq", 30) if tr.is_fa else ("Georgia", 28),
                          relief="solid", borderwidth=1, width=32,
                          fg=HEADER_FG, bg=HEADER_BG)
        header.keep_style = True
        header.pack(pady=(10, 14))

        container = tk.Frame(self, bg=SHEET_BG)
        # The paper and everything on it keeps its own light palette.
        container.keep_style = True
        container.pack(fill=tk.X, padx=16)

        for index, question in enumerate(self.questions):
            column = tk.Frame(container, bg=SHEET_BG, bd=1, relief="groove")
            column.grid(row=0, column=index, sticky="nsew", padx=8, pady=4)
            # `uniform` forces all three columns to the same width whatever
            # their content measures.
            container.columnconfigure(index, weight=1, uniform="sheet")
            self._build_question(column, index, question)

        submit = tk.Button(self, text=tr("quiz.hand_in"),
                           font=("Georgia", 14), bg=HEADER_BG, fg=INK,
                           activebackground=INK, activeforeground=SHEET_BG,
                           relief="flat", padx=18, pady=6, cursor="hand2",
                           command=self.close)
        submit.keep_style = True
        submit.pack(pady=10)

    # ------------------------------------------------------------------ helpers
    @property
    def questions(self) -> list[dict]:
        return self.data["questions"]

    def sheet_title(self) -> str:
        return self.data["sheet_title"][tr.language]

    # ------------------------------------------------------------------ build
    @staticmethod
    def _fit(path: str) -> tuple[int, int] | None:
        """Size to draw a question image at, capped to the column width."""
        from PIL import Image

        try:
            width, height = Image.open(path).size
        except Exception:
            return None
        if width <= MAX_IMAGE_WIDTH:
            return None
        scale = MAX_IMAGE_WIDTH / width
        return (MAX_IMAGE_WIDTH, max(1, int(height * scale)))

    def _build_question(self, parent: tk.Frame, index: int, question: dict) -> None:
        tk.Label(parent, text=question["text"][tr.language], justify="center",
                 bg=SHEET_BG, fg=INK, font=("Georgia", 12),
                 wraplength=330).pack(pady=(12, 6), padx=8)

        if question.get("image"):
            photo = load_photo(question["image"], self._fit(question["image"]))
            if photo:
                label = tk.Label(parent, image=photo, bg=SHEET_BG)
                label.image = photo  # keep a reference alive
                label.pack(pady=4)

        if question["type"] == "radio":
            var = tk.StringVar(value="")
            for option in question["options"]:
                tk.Radiobutton(
                    parent, text=option[tr.language], variable=var,
                    value=option[tr.language], bg=SHEET_BG, fg=INK,
                    font=("Georgia", 11), selectcolor=ENTRY_BG,
                    activebackground=SHEET_BG, activeforeground=INK,
                    wraplength=290, anchor="w", justify="left",
                    command=lambda opt=option: self._mark(index, bool(opt.get("correct"))),
                ).pack(fill=tk.X, padx=10, pady=3)
        else:
            row = tk.Frame(parent, bg=SHEET_BG)
            row.pack(pady=6)
            entry = tk.Entry(row, font=("Georgia", 14), width=12, bg=ENTRY_BG,
                             fg=INK, insertbackground=INK, relief="solid",
                             bd=1, justify="center")
            entry.pack(side=tk.LEFT, padx=4)
            entry.bind("<Return>", lambda _e: self._check_entry(index, entry))
            tk.Button(row, text="OK", font=("Georgia", 11), bg=HEADER_BG,
                      fg=INK, activebackground=INK, activeforeground=SHEET_BG,
                      relief="flat", padx=10,
                      command=lambda: self._check_entry(index, entry)).pack(
                side=tk.LEFT, padx=4)

        status = tk.Label(parent, text="", bg=SHEET_BG, fg=CORRECT_FG,
                          font=("Georgia", 12, "bold"))
        status.pack(pady=(2, 10))
        self.status_labels.append(status)

    # ------------------------------------------------------------------ checks
    def _check_entry(self, index: int, entry: tk.Entry) -> None:
        guess = normalize(entry.get())
        answers = {normalize(a) for a in self.questions[index].get("answers", [])}
        self._mark(index, bool(guess) and guess in answers)

    def _mark(self, index: int, correct: bool) -> None:
        if correct:
            self.correct_flags[index] = True
            self.status_labels[index].config(text="✓")
