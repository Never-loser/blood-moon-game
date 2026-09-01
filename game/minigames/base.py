"""Base class for every minigame window.

Minigames are modal Toplevels that share the root event loop - the old
per-window ``mainloop()`` calls (and the crashes they caused) are gone.

Each subclass builds its widgets with plain Tk calls, then
:meth:`_apply_theme` sweeps the finished tree once and restyles every
button and entry with the active palette. Doing it in one place keeps the
seven minigames consistent with the rest of the game without each of them
having to repeat the styling.
"""
from __future__ import annotations

import tkinter as tk

from ..app import BloodMoonApp
from ..widgets import modal

# Widgets carrying meaning in their own colors (the Stroop word, the exam
# paper) opt out by setting ``widget.keep_style = True``.
KEEP_ATTR = "keep_style"


class Minigame(tk.Toplevel):
    def __init__(self, app: BloodMoonApp, size: tuple[int, int] | None = None,
                 grab: bool = True):
        super().__init__(app.root, bg=app.theme.bg)
        self.app = app
        self.result = False  # True once the challenge is completed
        if size:
            width, height = size
            self.geometry(f"{width}x{height}")
            self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.close)
        if grab:
            try:
                modal(self, app.root)
            except tk.TclError:
                pass
        # Runs after the subclass constructor has finished building.
        self.after_idle(self._apply_theme)

    @property
    def theme(self):
        return self.app.theme

    # ------------------------------------------------------------- theming
    def _apply_theme(self) -> None:
        try:
            self._style_tree(self)
        except tk.TclError:
            pass  # window closed before idle ran

    def _style_tree(self, widget: tk.Misc) -> None:
        for child in widget.winfo_children():
            if getattr(child, KEEP_ATTR, False):
                continue  # opting out covers the whole subtree
            if isinstance(child, tk.Button):
                self._style_button(child)
            elif isinstance(child, tk.Entry):
                self._style_entry(child)
            self._style_tree(child)

    def _style_button(self, button: tk.Button) -> None:
        theme = self.theme
        button.config(
            bg=theme.surface, fg=theme.fg_dim,
            activebackground=theme.accent, activeforeground=theme.bg,
            disabledforeground=theme.muted,
            relief="flat", bd=0, highlightthickness=1,
            highlightbackground=theme.border, highlightcolor=theme.accent,
            padx=14, pady=5, cursor="hand2",
            font=theme.button_font(12),
        )

        def enter(_event=None, widget=button):
            if str(widget["state"]) != "disabled":
                widget.config(bg=theme.accent_dim, fg=theme.fg)

        def leave(_event=None, widget=button):
            if str(widget["state"]) != "disabled":
                widget.config(bg=theme.surface, fg=theme.fg_dim)

        button.bind("<Enter>", enter)
        button.bind("<Leave>", leave)

    def _style_entry(self, entry: tk.Entry) -> None:
        theme = self.theme
        entry.config(
            bg=theme.surface_2, fg=theme.fg, insertbackground=theme.accent,
            relief="flat", bd=6, highlightthickness=1,
            highlightbackground=theme.border, highlightcolor=theme.accent,
            selectbackground=theme.accent_dim, selectforeground=theme.fg,
            font=theme.body_font(13),
        )

    # -------------------------------------------------------------- closing
    def finish(self) -> None:
        """Mark the task complete and close."""
        self.result = True
        self.close()

    def close(self) -> None:
        self.on_close()
        try:
            self.grab_release()
        except (tk.TclError, RuntimeError):
            pass
        self.destroy()

    def on_close(self) -> None:
        """Subclasses cancel after() timers here."""
