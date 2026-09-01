"""Rapid-fire addition sprint (level 3). Score 10 before time runs out."""
from __future__ import annotations

import random
import tkinter as tk

from .. import config
from ..i18n import tr
from .base import Minigame


class MathSprint(Minigame):
    def __init__(self, app):
        super().__init__(app, size=(460, 340))
        self.score = 0
        self.time_left = config.MATH_SPRINT_TIME
        self.running = False
        self.a = 0
        self.b = 0
        self._timer_job = None

        self.question_label = tk.Label(self, text="", font=("Georgia", 24),
                                       bg=self.theme.bg, fg=self.theme.fg)
        self.question_label.pack(pady=(24, 10))

        self.answer_entry = tk.Entry(self, font=("Georgia", 20), width=12,
                                     justify="center", state=tk.DISABLED)
        self.answer_entry.pack()
        self.answer_entry.bind("<Return>", self.check_answer)

        self.score_label = tk.Label(self, text=tr("color.score", n=0), font=("Arial", 14),
                                    bg=self.theme.bg, fg=self.theme.fg, relief="ridge")
        self.score_label.pack(fill=tk.X, padx=30, pady=(14, 2))

        self.time_label = tk.Label(self, text=f"time: {self.time_left}s", font=("Arial", 14),
                                   bg=self.theme.bg, fg=self.theme.fg, relief="ridge")
        self.time_label.pack(fill=tk.X, padx=30)

        self.start_btn = tk.Button(self, text=tr("color.start"), font=("Georgia", 13),
                                   command=self.start_game)
        self.start_btn.pack(pady=12)

    def start_game(self) -> None:
        if self.result:
            return
        self.score = 0
        self.time_left = config.MATH_SPRINT_TIME
        self.score_label.config(text=tr("color.score", n=0))
        self.start_btn.config(state=tk.DISABLED)
        self.answer_entry.config(state=tk.NORMAL)
        self.running = True
        self.next_question()
        self.tick()

    def tick(self) -> None:
        if not self.running:
            return
        self.time_left -= 1
        self.time_label.config(text=f"time: {self.time_left}s")
        if self.time_left <= 0:
            self.game_over(won=False)
            return
        self._timer_job = self.after(1000, self.tick)

    def next_question(self) -> None:
        self.a = random.randint(10, 100)
        self.b = random.randint(10, 100)
        self.question_label.config(text=f"{self.a} + {self.b} = ?")
        self.answer_entry.delete(0, tk.END)

    def check_answer(self, _event=None) -> None:
        if not self.running:
            return
        answer = self.answer_entry.get().strip()
        if answer.lstrip("-").isdigit() and int(answer) == self.a + self.b:
            self.score += 1
            self.score_label.config(text=tr("color.score", n=self.score))
            if self.score >= config.MATH_SPRINT_TARGET_SCORE:
                self.game_over(won=True)
                return
        self.next_question()

    def game_over(self, won: bool) -> None:
        self.running = False
        if won:
            self.finish()
            return
        self.question_label.config(text=tr("color.lost"))
        self.answer_entry.config(state=tk.DISABLED)
        self.start_btn.config(state=tk.NORMAL, text="retry")

    def on_close(self) -> None:
        self.running = False
        if self._timer_job:
            try:
                self.after_cancel(self._timer_job)
            except Exception:
                pass
