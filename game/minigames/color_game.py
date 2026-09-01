"""The Stroop-style color game (level 1).

A word naming a color is shown in a possibly different color; the player
must type the *ink* color. Reach the target score before time runs out.
"""
from __future__ import annotations

import random
import tkinter as tk

from .. import config
from ..i18n import tr
from .base import Minigame


class ColorGame(Minigame):
    def __init__(self, app):
        super().__init__(app, size=(470, 400))
        self.title(tr("color.title"))

        # Fresh state on every open (old code leaked score/timer between runs).
        self.score = 0
        self.time_left = config.COLOR_GAME_TIME
        self.running = False

        tk.Label(self, text=tr("color.prompt"), bg=self.theme.bg,
                 fg=self.theme.fg_dim, font=self.theme.body_font(12),
                 wraplength=420, justify="center").pack(pady=(14, 6), padx=16)

        self.word_label = tk.Label(self, text="", font=("Georgia", 30, "bold"),
                                   bg=self.theme.surface_2, relief="flat",
                                   width=14, pady=10)
        self.word_label.pack(pady=8)

        entry_row = tk.Frame(self, bg=self.theme.bg)
        entry_row.pack(pady=6)
        self.answer = tk.Entry(entry_row, width=16)
        self.answer.pack(side=tk.LEFT, padx=6)
        self.answer.bind("<Return>", lambda _e: self.check())
        self.enter_btn = tk.Button(entry_row, text=tr("color.enter"),
                                   state=tk.DISABLED, command=self.check)
        self.enter_btn.pack(side=tk.LEFT, padx=6)

        status = tk.Frame(self, bg=self.theme.bg)
        status.pack(pady=8)
        self.time_label = tk.Label(status, text="", bg=self.theme.bg,
                                   fg=self.theme.muted,
                                   font=self.theme.ui_font(12))
        self.time_label.pack()
        self.score_label = tk.Label(status, text=tr("color.score", n=0),
                                    bg=self.theme.bg, fg=self.theme.fg,
                                    font=self.theme.mono_font(18))
        self.score_label.pack(pady=4)

        self.start_btn = tk.Button(self, text=tr("color.start"),
                                   command=self.start)
        self.start_btn.pack(pady=6)

        self._timer_job = None
        self.next_word()

    def start(self) -> None:
        self.start_btn.config(state=tk.DISABLED)
        self.enter_btn.config(state=tk.NORMAL)
        self.running = True
        self.tick()

    def tick(self) -> None:
        if not self.running:
            return
        self.time_left -= 1
        self.time_label.config(text=f"{self.time_left // 60}:{self.time_left % 60:02d}")
        if self.time_left <= 0:
            self.game_over(won=False)
            return
        self._timer_job = self.after(1000, self.tick)

    def next_word(self) -> None:
        colors = config.COLOR_GAME_COLORS
        word = random.choice(colors)
        ink = random.choice(colors)
        self.word_label.config(text=word, fg=ink)

    def check(self) -> None:
        if not self.running:
            return
        guess = self.answer.get().strip().lower()
        ink_color = str(self.word_label.cget("fg"))
        if guess and guess == ink_color.lower():
            self.score += 1
            self.score_label.config(text=tr("color.score", n=self.score))
            if self.score >= config.COLOR_GAME_TARGET_SCORE:
                self.game_over(won=True)
                return
        self.answer.delete(0, tk.END)
        self.next_word()

    def game_over(self, won: bool) -> None:
        self.running = False
        if won:
            self.finish()
        else:
            self.enter_btn.config(state=tk.DISABLED)
            tk.Label(self, text=tr("color.lost"), bg=self.theme.bg, fg=self.theme.fg,
                     font=("Georgia", 18)).pack(pady=10)

    def on_close(self) -> None:
        self.running = False
        if self._timer_job:
            try:
                self.after_cancel(self._timer_job)
            except Exception:
                pass
