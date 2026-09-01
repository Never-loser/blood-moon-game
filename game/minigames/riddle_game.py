"""The three level-1 riddles with normalized, case-insensitive answers."""
from __future__ import annotations

import tkinter as tk

from ..i18n import tr
from ..strings import build_riddles
from .base import Minigame


def normalize(text: str) -> str:
    # Map Arabic Yeh/Kaf to Persian forms so either keyboard layout works.
    return (text.strip().lower()
            .replace("ي", "ی").replace("ك", "ک")
            .replace("\u200c", " "))


class RiddleGame(Minigame):
    def __init__(self, app):
        super().__init__(app, size=(660, 620))
        self.title(tr("riddle.title_1"))

        self.solved: list[bool] = [False, False, False]
        self.riddles = build_riddles()

        theme = self.theme
        header = tk.Frame(self, bg=theme.accent, height=3)
        header.pack(fill=tk.X)

        self.rows: list[dict] = []
        for index, riddle in enumerate(self.riddles):
            frame = tk.Frame(self, bg=self.theme.bg)
            frame.pack(fill=tk.X, padx=8, pady=8)

            tk.Label(frame, text=tr(riddle["key"]), bg=theme.bg,
                     fg=theme.accent, font=theme.ui_font(11, "bold"),
                     anchor="w").pack(fill=tk.X)
            tk.Label(frame, text=riddle["text"][tr.language], justify="center",
                     bg=theme.surface, fg=theme.fg_dim,
                     font=theme.body_font(12), padx=12, pady=8).pack(
                fill=tk.X, pady=4)

            row = tk.Frame(frame, bg=self.theme.bg)
            row.pack(fill=tk.X)
            tk.Label(row, text=tr("riddle.answer"), bg=theme.bg,
                     fg=theme.muted, font=theme.ui_font(11)).pack(side=tk.LEFT)
            entry = tk.Entry(row, width=30)
            entry.pack(side=tk.LEFT, padx=6)
            submit = tk.Button(row, text=tr("riddle.submit"),
                               command=lambda i=index: self.check(i))
            submit.pack(side=tk.LEFT, padx=4)
            entry.bind("<Return>", lambda _e, i=index: self.check(i))
            status = tk.Label(row, text="", bg=theme.bg, fg=theme.ok,
                              font=theme.ui_font(10, "bold"))
            status.pack(side=tk.LEFT, padx=4)
            self.rows.append({"entry": entry, "status": status})

    def check(self, index: int) -> None:
        if self.solved[index]:
            return
        guess = normalize(self.rows[index]["entry"].get())
        accepted = {normalize(a) for a in self.riddles[index]["answers"]}
        if guess in accepted and guess:
            self.solved[index] = True
            self.rows[index]["status"].config(text=tr("riddle.correct"),
                                              fg=self.theme.ok)
            self.rows[index]["entry"].config(state=tk.DISABLED)
            if all(self.solved):
                self.after(500, self.finish)
        else:
            self.rows[index]["status"].config(text=tr("riddle.wrong"),
                                              fg=self.theme.danger)
