"""Reusable UI building blocks: buttons, cards, rules, toasts, backgrounds.

Everything here takes a :class:`~game.themes.Theme` and reads colors from it,
so no screen has to know a hex value.
"""
from __future__ import annotations

import tkinter as tk
from typing import Callable

from PIL import Image, ImageEnhance, ImageFilter, ImageTk

from .i18n import tr
from .themes import SPACE, Theme

_IMAGE_CACHE: dict[tuple, ImageTk.PhotoImage] = {}
_VIGNETTE_CACHE: dict[tuple[int, int], Image.Image] = {}


# ==========================================================================
# Images
# ==========================================================================
def load_photo(path: str, size: tuple[int, int] | None = None,
               resample: int = Image.Resampling.BILINEAR) -> ImageTk.PhotoImage | None:
    """Load (and cache) a PhotoImage; returns None when the file is missing."""
    key = (path, size)
    cached = _IMAGE_CACHE.get(key)
    if cached is not None:
        return cached
    try:
        img = Image.open(path)
        if size:
            img = img.resize(size, resample)
        photo = ImageTk.PhotoImage(img)
    except Exception:
        return None
    _IMAGE_CACHE[key] = photo
    return photo


def fit_cover(img: Image.Image, width: int, height: int,
              resample: int = Image.Resampling.BILINEAR) -> Image.Image:
    """Scale + center-crop so `img` fills WxH *without* distorting it.

    The old code stretched every background to the widget size, which
    squashed the 1:1 room art into a 16:9 box.
    """
    width, height = max(width, 2), max(height, 2)
    src_w, src_h = img.size
    scale = max(width / src_w, height / src_h)
    new_w, new_h = max(int(src_w * scale + 0.5), width), max(int(src_h * scale + 0.5), height)
    img = img.resize((new_w, new_h), resample)
    left, top = (new_w - width) // 2, (new_h - height) // 2
    return img.crop((left, top, left + width, top + height))


def _vignette_mask(width: int, height: int) -> Image.Image:
    """Cached radial falloff mask (white center -> black edges)."""
    key = (width, height)
    cached = _VIGNETTE_CACHE.get(key)
    if cached is not None:
        return cached
    # Build small and upscale: a 96px gradient is indistinguishable once
    # blown up, and ~400x cheaper than computing it per pixel.
    small = 96
    mask = Image.new("L", (small, small))
    pixels = mask.load()
    center = (small - 1) / 2.0
    max_dist = (center ** 2 + center ** 2) ** 0.5
    for y in range(small):
        for x in range(small):
            dist = (((x - center) ** 2 + (y - center) ** 2) ** 0.5) / max_dist
            # Flat in the middle, steep near the corners.
            value = 1.0 - max(0.0, (dist - 0.42) / 0.58) ** 1.6
            pixels[x, y] = int(max(0.0, min(1.0, value)) * 255)
    mask = mask.resize((width, height), Image.Resampling.BILINEAR)
    if len(_VIGNETTE_CACHE) > 8:
        _VIGNETTE_CACHE.clear()
    _VIGNETTE_CACHE[key] = mask
    return mask


def cinematic(img: Image.Image, theme: Theme, darken: float = 0.62,
              vignette: float = 0.85, saturation: float = 0.85) -> Image.Image:
    """Grade a background so light-on-dark UI stays readable on top of it.

    `darken` is the brightness multiplier, `vignette` how strongly the edges
    fall off to black, `saturation` pulls the flat AI-art colors back a bit.
    """
    img = img.convert("RGB")
    if saturation != 1.0:
        img = ImageEnhance.Color(img).enhance(saturation)
    if darken != 1.0:
        img = ImageEnhance.Brightness(img).enhance(darken)
    if vignette > 0:
        mask = _vignette_mask(*img.size)
        shadow = Image.new("RGB", img.size, theme.bg)
        if vignette < 1.0:
            mask = mask.point(lambda v: int(255 - (255 - v) * vignette))
        img = Image.composite(img, shadow, mask)
    return img


def scaled_background(frame: tk.Widget, theme: Theme, image_path: str,
                      darken: float = 0.55, vignette: float = 0.9) -> None:
    """Fill `frame` with a graded, aspect-correct `image_path` (debounced)."""
    try:
        original = Image.open(image_path)
    except Exception:
        frame.config(bg=theme.bg)
        return

    state: dict = {"job": None, "size": None, "photo": None}
    label = tk.Label(frame, bg=theme.bg, bd=0, highlightthickness=0)
    label.place(x=0, y=0, relwidth=1, relheight=1)
    label.lower()

    def render(width: int, height: int) -> None:
        if width < 2 or height < 2:
            return
        try:
            img = cinematic(fit_cover(original, width, height), theme,
                            darken=darken, vignette=vignette)
            photo = ImageTk.PhotoImage(img)
        except Exception:
            return
        state["photo"] = photo  # keep a reference alive
        label.config(image=photo)

    def on_resize(event: tk.Event) -> None:
        size = (event.width, event.height)
        if state["size"] == size:
            return
        state["size"] = size
        if state["job"]:
            try:
                frame.after_cancel(state["job"])
            except Exception:
                pass
        state["job"] = frame.after(90, lambda: render(*size))

    frame.bind("<Configure>", on_resize)


_MOON_CACHE: dict[tuple, ImageTk.PhotoImage] = {}


def _hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def moon_photo(theme: Theme, size: int = 420) -> ImageTk.PhotoImage:
    """Procedurally drawn blood moon: a glowing disc with a soft halo.

    Generated rather than shipped as a file - it scales to any screen, it
    follows the active theme, and it costs no repository weight.
    """
    key = (theme.id, size)
    cached = _MOON_CACHE.get(key)
    if cached is not None:
        return cached

    src = 192  # drawn small, upscaled smoothly
    disc = _hex_to_rgb(theme.accent)
    halo = _hex_to_rgb(theme.glow)
    back = _hex_to_rgb(theme.bg)
    img = Image.new("RGB", (src, src), theme.bg)
    pixels = img.load()
    center = (src - 1) / 2.0
    radius = src * 0.30

    for y in range(src):
        for x in range(src):
            dist = ((x - center) ** 2 + (y - center) ** 2) ** 0.5
            if dist <= radius:
                # Slight limb darkening so the disc reads as a sphere.
                shade = 0.55 + 0.45 * (1.0 - (dist / radius) ** 2) ** 0.5
                pixels[x, y] = tuple(int(c * shade) for c in disc)
            else:
                # Halo must reach zero by the nearest image edge, or the
                # square frame shows up as a lighter box on screen.
                falloff = max(0.0, 1.0 - (dist - radius) / (src * 0.20))
                glow = falloff ** 2.4 * 0.55
                pixels[x, y] = tuple(
                    int(b + (h - b) * glow) for b, h in zip(back, halo))

    # A touch of blur hides both the stair-stepped disc rim and the
    # banding in the halo gradient.
    img = img.filter(ImageFilter.GaussianBlur(1.1))
    img = img.resize((size, size), Image.Resampling.BICUBIC)
    photo = ImageTk.PhotoImage(img)
    if len(_MOON_CACHE) > 6:
        _MOON_CACHE.clear()
    _MOON_CACHE[key] = photo
    return photo


# ==========================================================================
# Buttons
# ==========================================================================
_VARIANTS = {
    # variant -> (idle bg, idle fg, idle border, hover bg, hover fg, hover border)
    "primary": ("accent_dim", "fg", "accent", "accent", "bg", "accent_bright"),
    "ghost":   ("surface", "fg_dim", "border", "accent_dim", "fg", "accent"),
    "quiet":   ("surface", "muted", "border_soft", "surface_2", "fg_dim", "border"),
    "danger":  ("surface", "danger", "border", "danger", "bg", "danger"),
}


class HoverButton(tk.Frame):
    """Flat, bordered button that lights up on hover.

    A Frame + Label composite rather than ``tk.Button`` so it can have a
    real 1px border, generous padding and a proper disabled state - none of
    which classic Tk buttons do well on Windows.
    """

    def __init__(self, master, theme: Theme, text: str,
                 command: Callable | None = None, font: tuple | None = None,
                 variant: str = "ghost", width: int | None = None,
                 padx: int = SPACE["md"], pady: int = SPACE["sm"],
                 anchor: str = "center", **kwargs):
        idle_bg, idle_fg, idle_bd, hov_bg, hov_fg, hov_bd = (
            _VARIANTS.get(variant, _VARIANTS["ghost"]))
        self.theme = theme
        self._colors = (getattr(theme, idle_bg), getattr(theme, idle_fg),
                        getattr(theme, idle_bd), getattr(theme, hov_bg),
                        getattr(theme, hov_fg), getattr(theme, hov_bd))
        self.command = command
        self._enabled = True

        super().__init__(master, bg=self._colors[2], bd=0, highlightthickness=0,
                         **kwargs)
        self.label = tk.Label(self, text=text, bg=self._colors[0],
                              fg=self._colors[1],
                              font=font or theme.button_font(),
                              padx=padx, pady=pady, anchor=anchor,
                              justify="center", cursor="hand2")
        if width:
            self.label.config(width=width)
        # 1px inset = the border color showing through the frame behind.
        self.label.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)

        for widget in (self, self.label):
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)
            widget.bind("<Button-1>", self._on_click)

    # ------------------------------------------------------------ behaviour
    def _on_enter(self, _event=None) -> None:
        if not self._enabled:
            return
        _, _, _, hov_bg, hov_fg, hov_bd = self._colors
        self.label.config(bg=hov_bg, fg=hov_fg)
        self.config(bg=hov_bd)

    def _on_leave(self, _event=None) -> None:
        if not self._enabled:
            return
        idle_bg, idle_fg, idle_bd, *_ = self._colors
        self.label.config(bg=idle_bg, fg=idle_fg)
        self.config(bg=idle_bd)

    def _on_click(self, _event=None) -> None:
        if self._enabled and self.command:
            self.command()

    def set_variant(self, variant: str) -> None:
        """Restyle in place - e.g. the 'next room' button turning primary
        once every objective in the room is ticked off."""
        idle_bg, idle_fg, idle_bd, hov_bg, hov_fg, hov_bd = (
            _VARIANTS.get(variant, _VARIANTS["ghost"]))
        theme = self.theme
        self._colors = (getattr(theme, idle_bg), getattr(theme, idle_fg),
                        getattr(theme, idle_bd), getattr(theme, hov_bg),
                        getattr(theme, hov_fg), getattr(theme, hov_bd))
        if self._enabled:
            self._on_leave()

    def set_enabled(self, enabled: bool) -> None:
        self._enabled = enabled
        if enabled:
            self._on_leave()
            self.label.config(cursor="hand2")
        else:
            self.label.config(bg=self.theme.surface, fg=self.theme.muted,
                              cursor="")
            self.config(bg=self.theme.border_soft)

    # ------------------------------------------- tk-compatible text access
    def configure(self, **kwargs):  # type: ignore[override]
        text = kwargs.pop("text", None)
        if text is not None:
            self.label.config(text=text)
        font = kwargs.pop("font", None)
        if font is not None:
            self.label.config(font=font)
        if kwargs:
            return super().configure(**kwargs)
        return None

    config = configure  # type: ignore[assignment]

    def cget(self, key: str):  # type: ignore[override]
        if key in ("text", "font"):
            return self.label.cget(key)
        return super().cget(key)


# ==========================================================================
# Containers & decoration
# ==========================================================================
class Card(tk.Frame):
    """Bordered panel used for the HUD rail, dialogs and settings groups."""

    def __init__(self, master, theme: Theme, padding: int = SPACE["md"],
                 tone: str = "surface", border: str = "border_soft", **kwargs):
        super().__init__(master, bg=getattr(theme, border), bd=0,
                         highlightthickness=0, **kwargs)
        self.theme = theme
        self.body = tk.Frame(self, bg=getattr(theme, tone), bd=0,
                             highlightthickness=0, padx=padding, pady=padding)
        self.body.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)


def rule(master, theme: Theme, color: str | None = None, pad: int = SPACE["sm"]) -> tk.Frame:
    """A 1px horizontal divider."""
    line = tk.Frame(master, bg=color or theme.border_soft, height=1, bd=0,
                    highlightthickness=0)
    line.pack(fill=tk.X, pady=pad)
    return line


def section_label(master, theme: Theme, text: str, **pack_kw) -> tk.Label:
    """Small caps-ish heading used above groups of controls."""
    label = tk.Label(master, text=text.upper() if not tr.is_fa else text,
                     bg=master["bg"], fg=theme.muted,
                     font=theme.ui_font(10, "bold"), anchor=theme.anchor())
    label.pack(fill=tk.X, **pack_kw)
    return label


class ProgressBar(tk.Frame):
    """Thin track + fill, used for room completion."""

    def __init__(self, master, theme: Theme, height: int = 6, **kwargs):
        super().__init__(master, bg=theme.surface_2, height=height, bd=0,
                         highlightthickness=0, **kwargs)
        self.theme = theme
        self.pack_propagate(False)
        self._fill = tk.Frame(self, bg=theme.accent, bd=0, highlightthickness=0)
        self._fill.place(x=0, y=0, relheight=1, relwidth=0.0)

    def set(self, fraction: float) -> None:
        fraction = max(0.0, min(1.0, fraction))
        color = self.theme.ok if fraction >= 1.0 else self.theme.accent
        self._fill.config(bg=color)
        self._fill.place_configure(relwidth=fraction)


def toast(parent: tk.Widget, theme: Theme, text: str, kind: str = "warn",
          ms: int = 2400, relx: float = 0.5, rely: float = 0.92) -> tk.Widget:
    """Floating message that fades itself out."""
    color = {"warn": theme.warn, "ok": theme.ok, "error": theme.danger}.get(
        kind, theme.warn)
    holder = tk.Frame(parent, bg=color, bd=0, highlightthickness=0)
    tk.Label(holder, text=text, bg=theme.surface_2, fg=color,
             font=theme.ui_font(12, "bold"), padx=SPACE["md"],
             pady=SPACE["sm"]).pack(padx=1, pady=1)
    holder.place(relx=relx, rely=rely, anchor="center")
    holder.after(ms, holder.destroy)
    return holder


def modal(window: tk.Toplevel, app_root: tk.Tk) -> None:
    window.transient(app_root)
    window.grab_set()
    window.focus_set()
