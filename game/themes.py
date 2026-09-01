"""Design tokens for the whole UI: color ramps, font stacks, spacing.

Two moods share one token vocabulary, so every screen can be written once:

  * theme 1 - "Blood"  : candle-lit crimson, the ritual itself
  * theme 2 - "Moon"   : cold moonlight blue, the same room gone quiet

Screens never hard-code a color. They ask the theme for a *role*
(``surface``, ``border``, ``muted``, ``danger`` ...) so switching mood or
adding a third one later stays a single-file change.
"""
from __future__ import annotations

import tkinter.font as tkfont

from .i18n import tr

# --------------------------------------------------------------------------
# Font stacks - first family actually installed on the machine wins.
# --------------------------------------------------------------------------
_STACKS = {
    # Latin
    "en_display": ["Cinzel", "Engravers MT", "Copperplate Gothic Bold",
                   "Perpetua Titling MT", "Castellar", "Georgia", "serif"],
    "en_title":   ["Cinzel", "Perpetua Titling MT", "Copperplate Gothic Light",
                   "Georgia", "Palatino Linotype", "serif"],
    "en_body":    ["Georgia", "Perpetua", "Palatino Linotype",
                   "Times New Roman", "serif"],
    "en_ui":      ["Segoe UI Variable Text", "Segoe UI", "Franklin Gothic Book",
                   "Arial", "sans-serif"],
    # Persian
    "fa_display": ["Mj_Naskh Titr", "B Titr", "IRANYekanXFaNum ExtraBlack",
                   "IRANYekanXFaNum Bold", "Tahoma"],
    "fa_title":   ["B Titr", "IRANYekanXFaNum Bold", "Mj_Naskh Titr", "Tahoma"],
    "fa_body":    ["IRANYekanXFaNum", "IRANYekanXFaNum Light", "B Nazanin",
                   "Vazirmatn", "Tahoma"],
    "fa_ui":      ["IRANYekanXFaNum", "IRANYekanXFaNum Light", "Dubai",
                   "Tahoma"],
    # Shared - the countdown and every number needs fixed-width digits so the
    # HUD does not jitter once per second.
    "mono":       ["JetBrains Mono", "Cascadia Mono", "Consolas",
                   "Lucida Console", "Courier New"],
}

_FAMILIES_CACHE: set[str] | None = None
_PICK_CACHE: dict[str, str] = {}


def _available_families() -> set[str]:
    global _FAMILIES_CACHE
    if _FAMILIES_CACHE is None:
        try:
            _FAMILIES_CACHE = {f.lower() for f in tkfont.families()}
        except Exception:
            _FAMILIES_CACHE = set()
    return _FAMILIES_CACHE


def pick_font(stack: list[str], fallback: str = "TkDefaultFont") -> str:
    """First installed family in `stack`, else `fallback`."""
    available = _available_families()
    for name in stack:
        if name.lower() in available:
            return name
    return fallback


def _family(key: str) -> str:
    """Resolve a stack name once and remember the answer."""
    if key not in _PICK_CACHE:
        _PICK_CACHE[key] = pick_font(_STACKS[key], fallback="Tahoma")
    return _PICK_CACHE[key]


# --------------------------------------------------------------------------
# Color palettes
# --------------------------------------------------------------------------
_BLOOD = {
    "bg":           "#08060a",   # page behind everything
    "surface":      "#130b0f",   # cards / rail
    "surface_2":    "#1d1015",   # raised rows inside a card
    "border":       "#3d1a20",
    "border_soft":  "#26141a",
    "accent":       "#c1121f",   # the brand red
    "accent_dim":   "#7a0d16",
    "accent_bright": "#ff3b4d",
    "glow":         "#ff6b6b",   # hotspot halo
    "fg":           "#f4e8ea",
    "fg_dim":       "#c9aeb3",
    "muted":        "#8b6a70",
    "ok":           "#4ade80",
    "warn":         "#fbbf24",
    "danger":       "#ef4444",
    "shadow":       "#000000",
}

_MOON = {
    "bg":           "#05070f",
    "surface":      "#0b1220",
    "surface_2":    "#121b2d",
    "border":       "#223a5c",
    "border_soft":  "#16233a",
    "accent":       "#7dd3fc",
    "accent_dim":   "#2f6f8f",
    "accent_bright": "#bae6fd",
    "glow":         "#a5e8ff",
    "fg":           "#e8f2fb",
    "fg_dim":       "#b3c8dc",
    "muted":        "#6d8399",
    "ok":           "#4ade80",
    "warn":         "#fbbf24",
    "danger":       "#f87171",
    "shadow":       "#000000",
}

_PALETTES = {1: _BLOOD, 2: _MOON}

# Spacing scale - keeps padding consistent instead of ad-hoc magic numbers.
SPACE = {"xs": 4, "sm": 8, "md": 14, "lg": 22, "xl": 34}

# Width of the level HUD rail, in pixels. The room canvas gets the rest, so
# the two never overlap (they used to: the rail was placed *on top* of a
# canvas that spanned 95% of the window).
RAIL_WIDTH = 292


class Theme:
    """Resolved colors + fonts for one mood id (1 = blood, 2 = moon)."""

    def __init__(self, theme_id: int):
        self.id = 1 if theme_id not in _PALETTES else theme_id
        palette = _PALETTES[self.id]
        for name, value in palette.items():
            setattr(self, name, value)

        # Legacy aliases still used by the minigames.
        self.hover_bg = self.accent
        self.name = "blood" if self.id == 1 else "moon"

    # ---------------------------------------------------------------- fonts
    @property
    def _prefix(self) -> str:
        return "fa" if tr.is_fa else "en"

    def display_font(self, size: int = 44) -> tuple:
        """Biggest type on screen: the game title."""
        return (_family(f"{self._prefix}_display"), size, "bold")

    def title_font(self, size: int | None = None) -> tuple:
        """Screen headings."""
        if size is None:
            size = 26 if tr.is_fa else 30
        return (_family(f"{self._prefix}_title"), size, "bold")

    def button_font(self, size: int = 16) -> tuple:
        return (_family(f"{self._prefix}_ui"), size, "bold")

    def body_font(self, size: int = 13) -> tuple:
        return (_family(f"{self._prefix}_body"), size)

    def ui_font(self, size: int = 13, weight: str = "normal") -> tuple:
        return (_family(f"{self._prefix}_ui"), size, weight)

    def hud_font(self, size: int = 18) -> tuple:
        """Labels around the play area."""
        return (_family(f"{self._prefix}_ui"), size)

    def mono_font(self, size: int = 26, weight: str = "bold") -> tuple:
        """Countdown and any other digits that must not jitter."""
        return (_family("mono"), size, weight)

    # --------------------------------------------------------------- helpers
    def timer_color(self, remaining: int, total: int) -> str:
        """Countdown color: calm -> warning -> critical."""
        if total <= 0:
            return self.fg
        ratio = remaining / total
        if ratio <= 0.10:
            return self.danger
        if ratio <= 0.30:
            return self.warn
        return self.fg

    def justify(self) -> str:
        return "right" if tr.is_fa else "left"

    def anchor(self) -> str:
        return "e" if tr.is_fa else "w"


def en_family() -> str:
    return _family("en_body")


def fa_family() -> str:
    return _family("fa_body")
