"""Game-over screen + the routing between rooms."""
from __future__ import annotations

import tkinter as tk

from ..i18n import tr
from ..themes import SPACE
from ..widgets import Card, HoverButton, moon_photo, rule
from .base import Screen


class GameOverScreen(Screen):
    """Shown when the countdown runs out. Returns to the menu on its own."""

    AUTO_RETURN_MS = 7000
    TICK_MS = 1000

    def build(self) -> None:
        theme = self.theme
        self.configure(bg=theme.bg)
        self._job = None
        self._countdown = self.AUTO_RETURN_MS // 1000

        # The blood moon itself, drawn behind everything.
        self._moon = moon_photo(theme, 380)
        tk.Label(self, image=self._moon, bg=theme.bg, bd=0,
                 highlightthickness=0).place(relx=0.5, rely=0.28,
                                             anchor="center")

        panel = Card(self, theme, padding=SPACE["xl"])
        panel.place(relx=0.5, rely=0.72, anchor="center")
        body = panel.body

        tk.Label(body, text=tr("gameover.title"), bg=theme.surface,
                 fg=theme.danger, font=theme.display_font(48)).pack()
        rule(body, theme, color=theme.accent_dim, pad=SPACE["md"])
        tk.Label(body, text=tr("gameover.subtitle"), bg=theme.surface,
                 fg=theme.fg_dim, font=theme.body_font(14), wraplength=420,
                 justify="center").pack(pady=(0, SPACE["lg"]))

        HoverButton(body, theme, tr("gameover.retry"), command=self.go_menu,
                    variant="primary", width=24).pack(fill=tk.X)

        self.countdown_label = tk.Label(
            body, text="", bg=theme.surface, fg=theme.muted,
            font=theme.ui_font(11))
        self.countdown_label.pack(pady=(SPACE["md"], 0))

        self.bind("<Button-1>", lambda _e: self.go_menu())

    def on_show(self) -> None:
        self._tick()

    def _tick(self) -> None:
        if self._countdown <= 0:
            self.go_menu()
            return
        self.countdown_label.config(
            text=f"{tr('gameover.returning')}  {self._countdown}")
        self._countdown -= 1
        self._job = self.after(self.TICK_MS, self._tick)

    def go_menu(self) -> None:
        from .menu import MenuScreen

        self._cancel()
        # A fresh attempt at the same room: run flags clear, but the room
        # you had unlocked stays unlocked.
        self.state.reset_run_flags()
        self.state.save()
        self.app.show_screen(MenuScreen)

    def _cancel(self) -> None:
        if getattr(self, "_job", None):
            try:
                self.after_cancel(self._job)
            except Exception:
                pass
            self._job = None

    def on_close(self) -> None:
        self._cancel()


def route_after_level(app, finished_level: int) -> None:
    """Move to the next room (or the ending) after a cleared room."""
    from .level1 import Level1Screen
    from .level2 import Level2Screen
    from .level3 import Level3Screen, EndScreen

    app.state.reset_run_flags()  # completed room's tasks no longer matter
    if finished_level < 3:
        app.state.current_level = finished_level + 1
        app.state.save()
        screens = {1: Level1Screen, 2: Level2Screen, 3: Level3Screen}
        app.show_screen(screens[finished_level + 1])
    else:
        app.state.current_level = 1  # new-game-plus loop like the original
        app.state.save()
        app.show_screen(EndScreen)
