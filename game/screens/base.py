"""Base class shared by every full-window screen."""
from __future__ import annotations

import tkinter as tk

from ..app import BloodMoonApp


class Screen(tk.Frame):
    def __init__(self, app: BloodMoonApp, **kwargs):
        super().__init__(app.root, bg=app.theme.bg)
        self.app = app
        self.build()

    # Subclasses create their widgets here.
    def build(self) -> None:  # pragma: no cover - overridden
        pass

    # Called by App when the screen becomes visible.
    def on_show(self) -> None:
        pass

    # Called before the screen is destroyed (cancel timers here).
    def on_close(self) -> None:
        pass

    @property
    def state(self):
        return self.app.state

    @property
    def theme(self):
        return self.app.theme
