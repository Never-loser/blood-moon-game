"""Main menu: the intro clip loops behind a centered title block."""
from __future__ import annotations

import os
import tkinter as tk

try:
    import cv2
except ImportError:  # pragma: no cover
    cv2 = None

from PIL import Image, ImageTk

from .. import config
from ..i18n import tr
from ..themes import SPACE
from ..widgets import Card, HoverButton, load_photo, rule
from .base import Screen


class VideoBackground:
    """Plays the intro clip behind the menu, graded down so text reads.

    Optimised vs the original: BILINEAR scaling (LANCZOS was ~4x slower),
    resizes only when the window size actually changes, and releases the
    capture when the menu closes (the old code leaked one per visit). The
    darkening is a 256-entry lookup table, which Pillow applies in C.
    """

    FPS_MS = 40  # 25 fps is plenty for an ambient loop

    def __init__(self, frame: tk.Widget, path: str, fallback_path: str | None,
                 dim: float = 0.45):
        self.running = False
        self._job = None
        self._photo = None
        self.cap = None
        self._lut = [int(min(255, i * dim)) for i in range(256)] * 3

        if cv2 is not None and os.path.isfile(path):
            self.cap = cv2.VideoCapture(path)

        self.label = tk.Label(frame, bg="black", bd=0, highlightthickness=0)
        self.label.place(x=0, y=0, relwidth=1, relheight=1)
        self.frame = frame

        if self.cap is None:
            photo = load_photo(fallback_path) if fallback_path else None
            if photo is not None:
                self._photo = photo
                self.label.config(image=photo)
            return

        self.running = True
        self._loop()

    def _loop(self) -> None:
        if not self.running or self.cap is None:
            return
        ret, frame = self.cap.read()
        if ret:
            size = (max(self.label.winfo_width(), 2),
                    max(self.label.winfo_height(), 2))
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb).resize(size, Image.Resampling.BILINEAR)
            self._photo = ImageTk.PhotoImage(img.point(self._lut))
            self.label.config(image=self._photo)
        else:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self._job = self.frame.after(self.FPS_MS, self._loop)

    def stop(self) -> None:
        self.running = False
        if self._job:
            try:
                self.frame.after_cancel(self._job)
            except Exception:
                pass
        if self.cap is not None:
            self.cap.release()
            self.cap = None


class MenuScreen(Screen):
    def __init__(self, app):
        self.video = None
        super().__init__(app)

    def build(self) -> None:
        theme = self.theme
        self.configure(bg=theme.bg)
        self.video = VideoBackground(self, config.INTRO_VIDEO,
                                     config.MAIN_MENU_FALLBACK_BG)

        # A bordered panel rather than a bare frame: over a moving video
        # a plain dark rectangle reads as a rendering glitch, a framed one
        # reads as design.
        panel = Card(self, theme, padding=SPACE["xl"])
        panel.place(relx=0.5, rely=0.5, anchor="center")
        column = panel.body

        title = tr("menu.title").strip()
        tk.Label(column, text=title.upper() if not tr.is_fa else title,
                 bg=theme.surface, fg=theme.accent,
                 font=theme.display_font(54 if not tr.is_fa else 44)).pack()
        rule(column, theme, color=theme.accent_dim, pad=SPACE["md"])
        tk.Label(column, text=tr("menu.subtitle"), bg=theme.surface,
                 fg=theme.fg_dim, font=theme.body_font(13)).pack(
            pady=(0, SPACE["xl"]))

        HoverButton(column, theme, tr("menu.start"), command=self.open_difficulty,
                    variant="primary", width=28,
                    font=theme.button_font(17)).pack(fill=tk.X,
                                                     pady=(0, SPACE["sm"]))

        HoverButton(column, theme, tr("menu.settings"), command=self.open_settings,
                    variant="ghost", width=28).pack(fill=tk.X,
                                                    pady=(0, SPACE["sm"]))
        HoverButton(column, theme, tr("menu.exit"), command=self.confirm_exit,
                    variant="quiet", width=28).pack(fill=tk.X)

        # Kept out of the button stack so the three actions stay evenly spaced.
        if self.state.current_level > 1:
            tk.Label(column,
                     text=tr("menu.continue_hint", n=self.state.current_level),
                     bg=theme.surface, fg=theme.muted,
                     font=theme.ui_font(10)).pack(pady=(SPACE["md"], 0))

        tk.Label(self, text=f"v{config.VERSION}", bg=theme.bg, fg=theme.muted,
                 font=theme.ui_font(9)).place(relx=1.0, rely=1.0,
                                              x=-SPACE["lg"], y=-SPACE["md"],
                                              anchor="se")

    # ------------------------------------------------------------------ actions
    def open_difficulty(self) -> None:
        from .difficulty import DifficultyScreen

        self.app.show_screen(DifficultyScreen)

    def open_settings(self) -> None:
        from .settings import SettingsScreen

        self.app.show_screen(SettingsScreen)

    def confirm_exit(self) -> None:
        theme = self.theme
        dialog = tk.Toplevel(self, bg=theme.bg)
        dialog.title(tr("exit.title"))
        dialog.resizable(False, False)
        try:
            dialog.transient(self.winfo_toplevel())
            dialog.grab_set()
        except tk.TclError:
            pass

        panel = Card(dialog, theme, padding=SPACE["lg"])
        panel.pack(fill=tk.BOTH, expand=True, padx=SPACE["md"],
                   pady=SPACE["md"])
        tk.Label(panel.body, text=tr("exit.question"), fg=theme.fg,
                 bg=theme.surface, font=theme.body_font(14)).pack(
            pady=(SPACE["sm"], SPACE["lg"]))

        buttons = tk.Frame(panel.body, bg=theme.surface)
        buttons.pack()
        HoverButton(buttons, theme, tr("common.yes"), command=self.app.quit,
                    variant="danger", width=10).pack(side=tk.LEFT,
                                                     padx=SPACE["sm"])
        HoverButton(buttons, theme, tr("common.no"), command=dialog.destroy,
                    variant="ghost", width=10).pack(side=tk.LEFT,
                                                    padx=SPACE["sm"])

        dialog.bind("<Escape>", lambda _e: dialog.destroy())
        dialog.update_idletasks()
        dialog.geometry(f"+{self.winfo_rootx() + 260}+{self.winfo_rooty() + 240}")

    def on_show(self) -> None:
        self.app.audio.play_menu_music()

    def on_close(self) -> None:
        if self.video:
            self.video.stop()
