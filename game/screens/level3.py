"""Room 3: math sprint, maze and snake - plus the ending screen."""
from __future__ import annotations

import tkinter as tk

from .. import config
from ..i18n import tr
from ..minigames import MathSprint, MazeGame, SnakeGame
from ..themes import SPACE
from ..widgets import Card, HoverButton, rule, scaled_background
from .level_base import LevelScreen, Screen


class Level3Screen(LevelScreen):
    level_number = 3

    # Panel order: math sprint / snake / maze.
    def objective_status(self) -> list[bool]:
        return [
            self.state.task(3, "math_sprint"),
            self.state.task(3, "snake"),
            self.state.task(3, "maze"),
        ]

    def hotspots(self) -> list[dict]:
        spots = [
            ("math_sprint", MathSprint, (53, 263, 214, 377)),
            ("maze", MazeGame, (422, 204, 735, 480)),
            ("snake", SnakeGame, (774, 227, 1148, 640)),
        ]
        return [
            {"fraction": self.fraction(rect),
             "callback": (lambda c=cls, t=task: self.launch(c, t)),
             "label": tr("spot." + task),
             "done": self.state.task(3, task)}
            for task, cls, rect in spots
        ]

    def launch(self, minigame_cls, task_name: str) -> None:
        if self.paused:
            return
        window = minigame_cls(self.app)
        self.wait_window(window)
        if getattr(window, "result", False):
            self.state.complete_task(3, task_name)
        self.refresh_objectives()


class EndScreen(Screen):
    """Ending: the closing line, story voice, replay and back to menu."""

    def build(self) -> None:
        theme = self.theme
        self.configure(bg=theme.bg)
        scaled_background(self, theme, config.LEVEL_BACKGROUNDS[3],
                          darken=0.28, vignette=1.0)

        panel = Card(self, theme, padding=SPACE["xl"])
        panel.place(relx=0.5, rely=0.5, anchor="center")
        body = panel.body

        tk.Label(body, text=tr("end.title"), bg=theme.surface,
                 fg=theme.accent, font=theme.display_font(46)).pack()
        rule(body, theme, color=theme.accent_dim, pad=SPACE["md"])
        tk.Label(body, text=tr("end.text"), bg=theme.surface, fg=theme.fg_dim,
                 font=theme.body_font(15), wraplength=460,
                 justify="center").pack(pady=(0, SPACE["xl"]))

        HoverButton(body, theme, tr("level.story_voice"),
                    command=lambda: self.app.audio.play_file(config.END_STORY),
                    variant="ghost", width=26).pack(fill=tk.X,
                                                    pady=(0, SPACE["sm"]))
        HoverButton(body, theme, tr("end.replay"), command=self.play_again,
                    variant="primary", width=26).pack(fill=tk.X,
                                                      pady=(0, SPACE["sm"]))
        HoverButton(body, theme, tr("common.main_menu"), command=self.go_menu,
                    variant="quiet", width=26).pack(fill=tk.X)

    def play_again(self) -> None:
        from .difficulty import DifficultyScreen

        self.state.reset_run_flags()
        self.state.current_level = 1
        self.state.save()
        self.app.show_screen(DifficultyScreen)

    def go_menu(self) -> None:
        from .menu import MenuScreen

        self.state.save()
        self.app.show_screen(MenuScreen)
