"""Difficulty selection: three cards, one per countdown length."""
from __future__ import annotations

import tkinter as tk

from .. import config
from ..i18n import tr
from ..themes import SPACE
from ..widgets import HoverButton, rule, scaled_background
from .base import Screen

CARD_WIDTH = 210


class DifficultyCard(tk.Frame):
    """Clickable card showing a difficulty name and its minutes-per-room."""

    def __init__(self, master, theme, difficulty: str, minutes: int,
                 command, selected: bool = False):
        self.theme = theme
        self.selected = selected
        border = theme.accent if selected else theme.border_soft
        super().__init__(master, bg=border, bd=0, highlightthickness=0)

        # Fixed width so the "Selected" badge cannot make one card wider
        # than its neighbours.
        self.body = tk.Frame(self, bg=theme.surface, padx=SPACE["lg"],
                             pady=SPACE["lg"], width=CARD_WIDTH, height=272)
        self.body.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        self.body.pack_propagate(False)

        self.name = tk.Label(self.body, text=tr("difficulty." + difficulty),
                             bg=theme.surface, fg=theme.fg,
                             font=theme.title_font(20))
        self.name.pack()
        self.minutes = tk.Label(self.body, text=str(minutes), bg=theme.surface,
                                fg=theme.accent, font=theme.mono_font(46))
        self.minutes.pack(pady=(SPACE["sm"], 0))
        self.caption = tk.Label(self.body, text=tr("difficulty.minutes_caption"),
                                bg=theme.surface, fg=theme.muted,
                                font=theme.ui_font(10))
        self.caption.pack()
        self.badge = tk.Label(self.body, text=tr("difficulty.selected")
                              if selected else " ", bg=theme.surface,
                              fg=theme.ok, font=theme.ui_font(9, "bold"))
        self.badge.pack(pady=(SPACE["sm"], 0))

        self._widgets = (self.body, self.name, self.minutes, self.caption,
                         self.badge)
        for widget in (self,) + self._widgets:
            widget.bind("<Enter>", self._enter)
            widget.bind("<Leave>", self._leave)
            widget.bind("<Button-1>", lambda _e: command())
            widget.config(cursor="hand2")

    def _enter(self, _event=None) -> None:
        theme = self.theme
        self.config(bg=theme.accent_bright)
        for widget in self._widgets:
            widget.config(bg=theme.surface_2)
        self.minutes.config(fg=theme.accent_bright)

    def _leave(self, _event=None) -> None:
        theme = self.theme
        self.config(bg=theme.accent if self.selected else theme.border_soft)
        for widget in self._widgets:
            widget.config(bg=theme.surface)
        self.minutes.config(fg=theme.accent)


class DifficultyScreen(Screen):
    def build(self) -> None:
        theme = self.theme
        self.configure(bg=theme.bg)
        scaled_background(self, theme, config.DIFFICULTY_BACKGROUND,
                          darken=0.34, vignette=1.0)

        header = tk.Frame(self, bg=theme.bg)
        header.place(relx=0.5, rely=0.16, anchor="center")
        tk.Label(header, text=tr("difficulty.title"), bg=theme.bg,
                 fg=theme.fg, font=theme.title_font()).pack()
        rule(header, theme, color=theme.accent_dim, pad=SPACE["sm"])
        tk.Label(header, text=tr("difficulty.subtitle"), bg=theme.bg,
                 fg=theme.muted, font=theme.body_font(12)).pack()

        row = tk.Frame(self, bg=theme.bg)
        row.place(relx=0.5, rely=0.48, anchor="center")
        for difficulty in config.DIFFICULTY_ORDER:
            minutes = config.DIFFICULTY_TIMES[difficulty] // 60
            DifficultyCard(row, theme, difficulty, minutes,
                           command=lambda d=difficulty: self.choose(d),
                           selected=self.state.difficulty == difficulty).pack(
                side=tk.LEFT, padx=SPACE["md"])

        HoverButton(self, theme, tr("common.back"), command=self.go_back,
                    variant="quiet", width=18).place(relx=0.5, rely=0.82,
                                                     anchor="center")

    def choose(self, difficulty: str) -> None:
        from .level1 import Level1Screen
        from .level2 import Level2Screen
        from .level3 import Level3Screen

        self.state.difficulty = difficulty
        self.state.save()

        screens = {1: Level1Screen, 2: Level2Screen, 3: Level3Screen}
        self.app.show_screen(screens[self.state.current_level])

    def go_back(self) -> None:
        from .menu import MenuScreen

        self.app.show_screen(MenuScreen)
