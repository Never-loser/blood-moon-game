"""Single-root application shell: owns the Tk root and screen navigation.

Every visible screen is a Frame stacked inside one persistent root window.
This replaces the original 17 separate Tk() roots / 23 nested mainloops.
"""
from __future__ import annotations

import tkinter as tk
from typing import Type

from .audio import AudioManager
from .i18n import tr
from .state import GameState
from .themes import Theme


class BloodMoonApp:
    def __init__(self, windowed: bool = False, width: int = 1280, height: int = 720):
        self.root = tk.Tk()
        self.root.title("Blood Moon Ritual")
        self.state = GameState.load()
        tr.set_language(self.state.language)
        self.audio = AudioManager()
        self.audio.set_volume_percent(self.state.volume)

        self.windowed = windowed
        if windowed:
            self.root.geometry(f"{width}x{height}")
        else:
            self.root.attributes("-fullscreen", True)
        self.root.config(bg="black")
        self.root.bind("<F11>", self._toggle_fullscreen)
        self.root.protocol("WM_DELETE_WINDOW", self.quit)

        self._screen: tk.Frame | None = None
        self._screen_name: str | None = None

    # ------------------------------------------------------------------ screens
    @property
    def theme(self) -> Theme:
        return Theme(self.state.theme_id)

    def show_screen(self, screen_cls: Type[tk.Frame], *args, **kwargs) -> tk.Frame:
        """Destroy the current screen and display a new one."""
        if self._screen is not None:
            close = getattr(self._screen, "on_close", None)
            if callable(close):
                close()
            self._screen.destroy()
        self._screen_name = screen_cls.__name__
        self._screen = screen_cls(self, *args, **kwargs)
        self._screen.pack(fill=tk.BOTH, expand=True)
        shown = getattr(self._screen, "on_show", None)
        if callable(shown):
            shown()
        return self._screen

    def rebuild_screen(self) -> None:
        """Re-create the current screen (after theme/language change)."""
        import game.screens as screens

        mapping = {
            "MenuScreen": screens.MenuScreen,
            "SettingsScreen": screens.SettingsScreen,
            "DifficultyScreen": screens.DifficultyScreen,
            "Level1Screen": screens.Level1Screen,
            "Level2Screen": screens.Level2Screen,
            "Level3Screen": screens.Level3Screen,
            "EndScreen": screens.EndScreen,
        }
        cls = mapping.get(self._screen_name or "", screens.MenuScreen)
        self.show_screen(cls)

    @property
    def screen_name(self) -> str | None:
        return self._screen_name

    # ------------------------------------------------------------------ misc
    def _toggle_fullscreen(self, _event=None) -> None:
        is_full = bool(self.root.attributes("-fullscreen"))
        if is_full:
            self.root.attributes("-fullscreen", False)
            self.root.geometry("1280x720")
        else:
            self.root.attributes("-fullscreen", True)

    def set_language(self, language: str) -> None:
        self.state.language = language
        tr.set_language(language)

    def quit(self) -> None:
        self.state.save()
        self.audio.shutdown()
        try:
            self.root.destroy()
        except tk.TclError:
            pass

    def run(self) -> None:
        from .screens import MenuScreen

        self.show_screen(MenuScreen)
        self.root.mainloop()
