"""Settings: language, appearance and audio, grouped into three cards."""
from __future__ import annotations

import os
import tkinter as tk

from ..config import SETTINGS_BACKGROUND
from ..i18n import tr
from ..themes import SPACE
from ..widgets import Card, HoverButton, rule, scaled_background
from .base import Screen

CARD_WIDTH = 300


class OptionRow(tk.Frame):
    """A themed radio row: filled dot when active, hover highlight."""

    def __init__(self, master, theme, text: str, active: bool, command):
        self.theme = theme
        self.active = active
        super().__init__(master, bg=theme.surface, bd=0, highlightthickness=0)

        self.dot = tk.Label(self, text="●" if active else "○", bg=theme.surface,
                            fg=theme.accent if active else theme.muted,
                            font=theme.ui_font(13), width=2)
        self.text = tk.Label(self, text=text, bg=theme.surface,
                             fg=theme.fg if active else theme.fg_dim,
                             font=theme.ui_font(13), anchor=theme.anchor())
        if tr.is_fa:
            self.dot.pack(side=tk.RIGHT)
            self.text.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        else:
            self.dot.pack(side=tk.LEFT)
            self.text.pack(side=tk.LEFT, fill=tk.X, expand=True)

        for widget in (self, self.dot, self.text):
            widget.bind("<Enter>", self._enter)
            widget.bind("<Leave>", self._leave)
            widget.bind("<Button-1>", lambda _e: command())
            widget.config(cursor="hand2")

    def _enter(self, _event=None) -> None:
        for widget in (self, self.dot, self.text):
            widget.config(bg=self.theme.surface_2)
        self.text.config(fg=self.theme.fg)

    def _leave(self, _event=None) -> None:
        for widget in (self, self.dot, self.text):
            widget.config(bg=self.theme.surface)
        self.text.config(fg=self.theme.fg if self.active else self.theme.fg_dim)


class SettingsScreen(Screen):
    def build(self) -> None:
        theme = self.theme
        self.configure(bg=theme.bg)
        scaled_background(self, theme, SETTINGS_BACKGROUND, darken=0.3,
                          vignette=1.0)

        header = tk.Frame(self, bg=theme.bg)
        header.place(relx=0.5, rely=0.13, anchor="center")
        tk.Label(header, text=tr("settings.title"), bg=theme.bg, fg=theme.fg,
                 font=theme.title_font()).pack()
        rule(header, theme, color=theme.accent_dim, pad=SPACE["sm"])

        row = tk.Frame(self, bg=theme.bg)
        row.place(relx=0.5, rely=0.48, anchor="center")

        self._build_language(row)
        self._build_appearance(row)
        self._build_audio(row)

        HoverButton(self, theme, tr("common.main_menu"), command=self.go_back,
                    variant="quiet", width=20).place(relx=0.5, rely=0.84,
                                                     anchor="center")

    # ------------------------------------------------------------------ cards
    def _card(self, parent, title: str) -> tk.Frame:
        theme = self.theme
        card = Card(parent, theme, padding=SPACE["lg"])
        card.pack(side=tk.LEFT, padx=SPACE["md"], anchor="n")
        card.body.config(width=CARD_WIDTH)
        card.body.pack_propagate(False)
        tk.Label(card.body, text=title, bg=theme.surface, fg=theme.accent,
                 font=theme.ui_font(11, "bold"), anchor=theme.anchor()).pack(
            fill=tk.X)
        rule(card.body, theme, pad=SPACE["sm"])
        return card.body

    def _build_language(self, parent) -> None:
        body = self._card(parent, tr("settings.language"))
        body.config(height=240)
        for value, key in (("en", "settings.english"), ("fa", "settings.persian")):
            OptionRow(body, self.theme, tr(key),
                      active=self.state.language == value,
                      command=lambda v=value: self.change_language(v)).pack(
                fill=tk.X, pady=2)

    def _build_appearance(self, parent) -> None:
        body = self._card(parent, tr("settings.appearance"))
        body.config(height=240)
        for value, key in ((1, "settings.theme1"), (2, "settings.theme2")):
            OptionRow(body, self.theme, tr(key),
                      active=self.state.theme_id == value,
                      command=lambda v=value: self.change_theme(v)).pack(
                fill=tk.X, pady=2)

    def _build_audio(self, parent) -> None:
        theme = self.theme
        body = self._card(parent, tr("settings.audio"))
        body.config(height=240)

        self.volume_value = tk.Label(
            body, text=f"{self.state.volume}%", bg=theme.surface,
            fg=theme.fg, font=theme.mono_font(24), anchor=theme.anchor())
        self.volume_value.pack(fill=tk.X)

        # Live: the volume applies as you drag, so no "apply" button is
        # needed any more.
        # tk.Scale paints the *handle* with `bg`, so the accent has to go
        # there for the control to be visible at all on a dark card.
        self.volume_scale = tk.Scale(
            body, from_=0, to=100, orient=tk.HORIZONTAL, showvalue=False,
            bg=theme.accent, fg=theme.fg, highlightthickness=0,
            troughcolor=theme.border, activebackground=theme.accent_bright,
            bd=0, sliderrelief="flat", sliderlength=26, width=14,
            cursor="hand2", command=self.on_volume)
        self.volume_scale.set(self.state.volume)
        self.volume_scale.pack(fill=tk.X, pady=(SPACE["sm"], SPACE["md"]))

        HoverButton(body, theme, tr("settings.change_audio"),
                    command=self.change_music, variant="ghost").pack(fill=tk.X)
        self.track_label = tk.Label(body, text="", bg=theme.surface,
                                    fg=theme.muted, font=theme.ui_font(9),
                                    wraplength=CARD_WIDTH - 40)
        self.track_label.pack(fill=tk.X, pady=(SPACE["sm"], 0))

    # ---------------------------------------------------------------- actions
    def change_language(self, language: str) -> None:
        if language != self.state.language:
            self.app.set_language(language)
            self.state.save()
            self.app.rebuild_screen()

    def change_theme(self, theme_id: int) -> None:
        if theme_id != self.state.theme_id:
            self.state.theme_id = theme_id
            self.state.save()
            self.app.rebuild_screen()

    def on_volume(self, value: str) -> None:
        volume = int(float(value))
        self.state.volume = volume
        self.volume_value.config(text=f"{volume}%")
        self.app.audio.set_volume_percent(volume)
        self.state.save()

    def change_music(self) -> None:
        track = self.app.audio.play_random_menu_track()
        if track is None:
            self.app.audio.replay_current()
            return
        name = os.path.splitext(track)[0]
        self.track_label.config(text=tr("settings.current", name=name))

    def go_back(self) -> None:
        from .menu import MenuScreen

        self.app.show_screen(MenuScreen)
