"""Shared chrome for all three rooms: stage canvas, HUD rail, timer, pause.

Layout
------
The window is a two-column grid::

    +-------------------------------+----------------+
    |  stage (room art + sigils)    |  HUD rail      |
    |  column 0, weight 1           |  column 1      |
    +-------------------------------+----------------+

The rail owns its own column, so it can never sit on top of the artwork.
(It used to be ``place``-d at ``relx=1.0`` over a canvas that already
spanned 95% of the window, which pushed the objectives list and all three
buttons on top of the room.)

The room art also gets aspect-correct cover-scaling plus a vignette, and
every interactive area is now *drawn* as a pulsing sigil - previously the
only clue a hotspot existed was the mouse cursor changing shape.
"""
from __future__ import annotations

import math
import tkinter as tk
from typing import Callable

from .. import config
from ..i18n import tr
from ..state import TASK_NAMES
from ..themes import RAIL_WIDTH, SPACE
from ..widgets import Card, HoverButton, ProgressBar, cinematic, fit_cover, toast
from .base import Screen

CANVAS_DESIGN_SIZE = (1180, 680)
PULSE_MS = 60


class LevelScreen(Screen):
    level_number = 0

    def __init__(self, app):
        self.timer_job = None
        self.pulse_job = None
        self.paused = False
        self.remaining = None
        self.total_seconds = 0
        self._phase = 0.0
        self._hover_index: int | None = None
        self._spot_items: list[dict] = []
        self._bg_photo = None
        self._resize_job = None
        super().__init__(app)

    # ------------------------------------------------------------------ hooks
    def hotspots(self) -> list[dict]:
        """Interactive areas of the room.

        Each entry is ``{"fraction": (x0, y0, x1, y1), "callback": fn,
        "label": str, "done": bool}`` where the rect is in design-canvas
        space (see :meth:`fraction`).
        """
        return []

    def objective_status(self) -> list[bool]:
        """One bool per objectives line, same order as ``tr.lines()``."""
        names = TASK_NAMES[self.level_number]
        return [self.state.task(self.level_number, name) for name in names]

    def open_minigame(self, factory: Callable[[], tk.Toplevel]) -> None:
        raise NotImplementedError

    # ================================================================== build
    def build(self) -> None:
        theme = self.theme
        self.configure(bg=theme.bg)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0, minsize=RAIL_WIDTH)
        self.rowconfigure(0, weight=1)

        self._build_stage()
        self._build_rail()

        self.app.root.bind("<Escape>", self.on_escape)

    # ------------------------------------------------------------------ stage
    def _build_stage(self) -> None:
        theme = self.theme
        stage = tk.Frame(self, bg=theme.bg, bd=0, highlightthickness=0)
        stage.grid(row=0, column=0, sticky="nsew")
        self.stage = stage

        self.canvas = tk.Canvas(stage, bg=theme.bg, highlightthickness=0, bd=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Motion>", self.on_canvas_motion)
        self.canvas.bind("<Leave>", lambda _e: self._set_hover(None))
        self.canvas.bind("<Configure>", self.on_canvas_resize)

        # Room badge, floating over the top-left corner of the art.
        badge = tk.Frame(stage, bg=theme.accent, bd=0, highlightthickness=0)
        tk.Label(badge, text=tr("level.room", n=self.level_number).upper()
                 if not tr.is_fa else tr("level.room", n=self.level_number),
                 bg=theme.surface, fg=theme.accent_bright,
                 font=theme.ui_font(11, "bold"),
                 padx=SPACE["md"], pady=SPACE["xs"]).pack(padx=1, pady=1)
        badge.place(x=SPACE["lg"], y=SPACE["lg"])

        # Hint line along the bottom of the art.
        self.hint_label = tk.Label(
            stage, text=tr("hud.hint"), bg=theme.bg, fg=theme.muted,
            font=theme.ui_font(11), padx=SPACE["md"], pady=SPACE["xs"])
        self.hint_label.place(relx=0.5, rely=1.0, y=-SPACE["lg"], anchor="s")

        # Name of whatever sigil the cursor is over.
        self.spot_label = tk.Frame(stage, bg=theme.accent, bd=0,
                                   highlightthickness=0)
        self.spot_text = tk.Label(self.spot_label, text="", bg=theme.surface,
                                  fg=theme.fg, font=theme.ui_font(12, "bold"),
                                  padx=SPACE["md"], pady=SPACE["xs"])
        self.spot_text.pack(padx=1, pady=1)

    # ------------------------------------------------------------------- rail
    def _build_rail(self) -> None:
        theme = self.theme
        # A 1px seam so the rail reads as a separate surface from the stage.
        seam = tk.Frame(self, bg=theme.border, bd=0, highlightthickness=0)
        seam.grid(row=0, column=1, sticky="nsew")

        rail = tk.Frame(seam, bg=theme.surface, bd=0, highlightthickness=0,
                        padx=SPACE["md"], pady=SPACE["md"])
        rail.pack(fill=tk.BOTH, expand=True, padx=(1, 0))
        self.rail = rail

        anchor = theme.anchor()
        justify = theme.justify()

        # ---- title -------------------------------------------------------
        tk.Label(rail, text=config.APP_NAME if not tr.is_fa else tr("menu.title").strip(),
                 bg=theme.surface, fg=theme.accent,
                 font=theme.ui_font(11, "bold"), anchor=anchor).pack(fill=tk.X)
        tk.Label(rail, text=tr("level.position",
                               percent=config.LEVEL_PROGRESS_PERCENT.get(
                                   self.level_number, 0)),
                 bg=theme.surface, fg=theme.muted, font=theme.ui_font(10),
                 anchor=anchor).pack(fill=tk.X, pady=(0, SPACE["md"]))

        # ---- countdown ---------------------------------------------------
        timer_card = Card(rail, theme, padding=SPACE["md"], tone="surface_2")
        timer_card.pack(fill=tk.X)
        tk.Label(timer_card.body, text=tr("hud.time_left"),
                 bg=theme.surface_2, fg=theme.muted,
                 font=theme.ui_font(10, "bold"), anchor=anchor).pack(fill=tk.X)
        self.timer_label = tk.Label(timer_card.body, text="--:--",
                                    bg=theme.surface_2, fg=theme.fg,
                                    font=theme.mono_font(30), anchor=anchor)
        self.timer_label.pack(fill=tk.X, pady=(SPACE["xs"], SPACE["sm"]))
        self.time_bar = ProgressBar(timer_card.body, theme, height=4)
        self.time_bar.pack(fill=tk.X)

        # ---- objectives --------------------------------------------------
        obj_card = Card(rail, theme, padding=SPACE["md"], tone="surface_2")
        obj_card.pack(fill=tk.X, pady=(SPACE["md"], 0))
        header = tk.Frame(obj_card.body, bg=theme.surface_2)
        header.pack(fill=tk.X)
        tk.Label(header, text=tr("level.items_title"), bg=theme.surface_2,
                 fg=theme.fg, font=theme.ui_font(12, "bold")).pack(
            side=tk.RIGHT if tr.is_fa else tk.LEFT)
        self.count_label = tk.Label(header, text="", bg=theme.surface_2,
                                    fg=theme.muted, font=theme.ui_font(10))
        self.count_label.pack(side=tk.LEFT if tr.is_fa else tk.RIGHT)

        self.task_bar = ProgressBar(obj_card.body, theme, height=4)
        self.task_bar.pack(fill=tk.X, pady=(SPACE["sm"], SPACE["md"]))

        self.objectives_holder = tk.Frame(obj_card.body, bg=theme.surface_2)
        self.objectives_holder.pack(fill=tk.X)
        self._objective_anchor, self._objective_justify = anchor, justify

        # ---- actions (pinned to the bottom) ------------------------------
        actions = tk.Frame(rail, bg=theme.surface)
        actions.pack(side=tk.BOTTOM, fill=tk.X)

        self.next_button = HoverButton(
            actions, theme, tr("level.next_room"), command=self.check_next_room,
            variant="quiet", font=theme.button_font(14))
        self.next_button.pack(fill=tk.X, pady=(0, SPACE["sm"]))

        self.story_button = HoverButton(
            actions, theme, tr("level.story_voice"), command=self.toggle_story,
            variant="ghost", font=theme.button_font(13))
        self.story_button.pack(fill=tk.X, pady=(0, SPACE["sm"]))

        HoverButton(actions, theme, tr("level.option"), command=self.open_pause,
                    variant="quiet", font=theme.button_font(13)).pack(fill=tk.X)

        self._build_objectives()

    def _build_objectives(self) -> None:
        theme = self.theme
        holder = getattr(self, "objectives_holder", None)
        if holder is None:
            return
        for child in holder.winfo_children():
            child.destroy()

        lines = tr.lines(f"level{self.level_number}.items")
        status = self.objective_status()
        done_count = sum(1 for index in range(len(lines))
                         if index < len(status) and status[index])

        for index, line in enumerate(lines):
            done = index < len(status) and status[index]
            row = tk.Frame(holder, bg=theme.surface_2)
            row.pack(fill=tk.X, pady=3)
            mark = tk.Label(row, text="✓" if done else "○",
                            bg=theme.surface_2,
                            fg=theme.ok if done else theme.muted,
                            font=theme.ui_font(12, "bold"), width=2)
            text = tk.Label(row, text=line, bg=theme.surface_2,
                            fg=theme.muted if done else theme.fg_dim,
                            font=theme.body_font(11),
                            wraplength=RAIL_WIDTH - 88,
                            justify=self._objective_justify,
                            anchor=self._objective_anchor)
            if tr.is_fa:
                mark.pack(side=tk.RIGHT)
                text.pack(side=tk.RIGHT, fill=tk.X, expand=True)
            else:
                mark.pack(side=tk.LEFT)
                text.pack(side=tk.LEFT, fill=tk.X, expand=True)

        total = max(len(lines), 1)
        self.count_label.config(text=tr("hud.count", done=done_count,
                                        total=len(lines)))
        self.task_bar.set(done_count / total)

        cleared = self.state.tasks_done(self.level_number)
        self.next_button.set_variant("primary" if cleared else "quiet")
        if cleared:
            self.hint_label.config(text=tr("hud.cleared"), fg=theme.ok)

    def refresh_objectives(self) -> None:
        self._build_objectives()
        self._draw_hotspots()

    # ================================================================= canvas
    def on_canvas_resize(self, event: tk.Event) -> None:
        if self._resize_job:
            try:
                self.after_cancel(self._resize_job)
            except Exception:
                pass
        self._resize_job = self.after(
            70, lambda: self._render_background(event.width, event.height))

    def _render_background(self, width: int, height: int) -> None:
        from PIL import Image, ImageTk

        if width < 2 or height < 2:
            return
        path = config.LEVEL_BACKGROUNDS[self.level_number]
        try:
            img = cinematic(fit_cover(Image.open(path), width, height),
                            self.theme, darken=0.72, vignette=0.8,
                            saturation=0.9)
            self._bg_photo = ImageTk.PhotoImage(img)
            self.canvas.delete("background")
            self.canvas.create_image(0, 0, anchor="nw", image=self._bg_photo,
                                     tags="background")
            self.canvas.tag_lower("background")
        except Exception:
            self.canvas.config(bg=self.theme.bg)
        self._draw_hotspots()

    # ---------------------------------------------------------------- sigils
    def _spot_center(self, spot: dict) -> tuple[float, float, float]:
        """Center + a radius that scales with the canvas."""
        width = max(self.canvas.winfo_width(), 1)
        height = max(self.canvas.winfo_height(), 1)
        fx0, fy0, fx1, fy1 = spot["fraction"]
        cx = (fx0 + fx1) / 2 * width
        cy = (fy0 + fy1) / 2 * height
        radius = max(20.0, min(width, height) * 0.038)
        return cx, cy, radius

    def _draw_hotspots(self) -> None:
        theme = self.theme
        self.canvas.delete("spot")
        self._spot_items = []
        for index, spot in enumerate(self.hotspots()):
            cx, cy, radius = self._spot_center(spot)
            done = bool(spot.get("done"))
            color = theme.ok if done else theme.glow
            # Dark backing ring first: without it a red sigil vanishes into
            # the bright, warm artwork of room 1.
            halo = self.canvas.create_oval(cx - radius, cy - radius,
                                           cx + radius, cy + radius,
                                           outline=theme.shadow, width=6,
                                           tags=("spot", f"spot{index}"))
            ring = self.canvas.create_oval(cx - radius, cy - radius,
                                           cx + radius, cy + radius,
                                           outline=color, width=3,
                                           tags=("spot", f"spot{index}"))
            self.canvas.create_oval(cx - 7, cy - 7, cx + 7, cy + 7,
                                    fill=theme.shadow, outline="",
                                    tags=("spot", f"spot{index}"))
            core = self.canvas.create_oval(cx - 5, cy - 5, cx + 5, cy + 5,
                                           fill=color, outline="",
                                           tags=("spot", f"spot{index}"))
            check = None
            if done:
                check = self.canvas.create_text(
                    cx, cy - radius - 12, text="✓", fill=theme.ok,
                    font=self.theme.ui_font(13, "bold"),
                    tags=("spot", f"spot{index}"))
            self._spot_items.append({"ring": ring, "halo": halo,
                                     "core": core, "check": check,
                                     "done": done, "cx": cx, "cy": cy,
                                     "r": radius})
        self._start_pulse()

    def _start_pulse(self) -> None:
        if self.pulse_job is None and self._spot_items:
            self._pulse()

    def _pulse(self) -> None:
        """Breathe the unsolved sigils so they read as 'click me'."""
        self.pulse_job = None
        if not self.winfo_exists() or not self._spot_items:
            return
        self._phase += 0.14
        for index, item in enumerate(self._spot_items):
            if item["done"]:
                continue
            hovered = index == self._hover_index
            swing = math.sin(self._phase + index * 1.1)
            radius = item["r"] * (1.0 + 0.16 * swing) + (5 if hovered else 0)
            cx, cy = item["cx"], item["cy"]
            for key in ("halo", "ring"):
                self.canvas.coords(item[key], cx - radius, cy - radius,
                                   cx + radius, cy + radius)
            self.canvas.itemconfig(
                item["ring"],
                width=3 if hovered else 2,
                outline=self.theme.accent_bright if hovered else self.theme.glow)
        try:
            self.pulse_job = self.after(PULSE_MS, self._pulse)
        except tk.TclError:
            self.pulse_job = None

    def _stop_pulse(self) -> None:
        if self.pulse_job:
            try:
                self.after_cancel(self.pulse_job)
            except Exception:
                pass
            self.pulse_job = None

    def _set_hover(self, index: int | None) -> None:
        if index == self._hover_index:
            return
        self._hover_index = index
        if index is None:
            self.spot_label.place_forget()
            self.canvas.config(cursor="")
            return
        spots = self.hotspots()
        if index >= len(spots):
            return
        self.canvas.config(cursor="hand2")
        label = spots[index].get("label") or ""
        self.spot_text.config(text=label)
        cx, cy, radius = self._spot_center(spots[index])
        self.spot_label.place(x=int(cx), y=int(max(cy - radius - 18, 10)),
                              anchor="s")

    # ---------------------------------------------------------------- input
    def on_canvas_click(self, event: tk.Event) -> None:
        index = self._hotspot_index_at(event.x, event.y)
        if index is not None:
            self.hotspots()[index]["callback"]()

    def on_canvas_motion(self, event: tk.Event) -> None:
        self._set_hover(self._hotspot_index_at(event.x, event.y))

    def _hotspot_index_at(self, x: int, y: int) -> int | None:
        """Hit-test the declared rect *or* the drawn sigil, whichever is hit."""
        width = max(self.canvas.winfo_width(), 1)
        height = max(self.canvas.winfo_height(), 1)
        for index, spot in enumerate(self.hotspots()):
            fx0, fy0, fx1, fy1 = spot["fraction"]
            if (fx0 * width <= x <= fx1 * width
                    and fy0 * height <= y <= fy1 * height):
                return index
            cx, cy, radius = self._spot_center(spot)
            if (x - cx) ** 2 + (y - cy) ** 2 <= (radius + 6) ** 2:
                return index
        return None

    @staticmethod
    def fraction(rect: tuple[int, int, int, int]) -> tuple[float, float, float, float]:
        """Convert a rect in 1180x680 design pixels to fractions."""
        x0, y0, x1, y1 = rect
        return (x0 / CANVAS_DESIGN_SIZE[0], y0 / CANVAS_DESIGN_SIZE[1],
                x1 / CANVAS_DESIGN_SIZE[0], y1 / CANVAS_DESIGN_SIZE[1])

    # ================================================================== story
    def toggle_story(self) -> None:
        if self.story_button.cget("text") == tr("level.play_music"):
            self.story_button.config(text=tr("level.story_voice"))
        else:
            self.story_button.config(text=tr("level.play_music"))
        narration = config.STORY_NARRATION[self.level_number]
        if not self.app.audio.play_file(narration):
            self.app.audio.replay_current()

    def play_level_music(self) -> None:
        music = config.LEVEL_MUSIC[self.level_number]
        if not self.app.audio.play_file(music):
            self.app.audio.replay_current()

    # ================================================================== pause
    def on_escape(self, _event=None) -> None:
        if not self.paused:
            self.open_pause()

    def open_pause(self) -> None:
        if self.paused:
            return
        self.paused = True
        self.stop_timer()
        self._stop_pulse()
        self.app.audio.stop()

        theme = self.theme
        dialog = tk.Toplevel(self, bg=theme.bg)
        dialog.attributes("-fullscreen",
                          bool(self.app.root.attributes("-fullscreen")))
        dialog.protocol("WM_DELETE_WINDOW", lambda: self.close_pause(dialog))

        panel = Card(dialog, theme, padding=SPACE["xl"])
        panel.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(panel.body, text=tr("pause.title"), bg=theme.surface,
                 fg=theme.accent, font=theme.title_font(28)).pack()
        tk.Label(panel.body, text=tr("pause.subtitle"), bg=theme.surface,
                 fg=theme.muted, font=theme.body_font(12)).pack(
            pady=(SPACE["sm"], SPACE["xl"]))

        HoverButton(panel.body, theme, tr("pause.back_to_game"),
                    command=lambda: self.close_pause(dialog),
                    variant="primary", width=26).pack(fill=tk.X,
                                                      pady=(0, SPACE["sm"]))
        HoverButton(panel.body, theme, tr("pause.save_quit"),
                    command=lambda: self.save_and_quit(dialog),
                    variant="quiet", width=26).pack(fill=tk.X)
        dialog.bind("<Escape>", lambda _e: self.close_pause(dialog))

    def close_pause(self, dialog: tk.Toplevel) -> None:
        dialog.destroy()
        self.paused = False
        self.start_timer(from_seconds=self.remaining)
        self._start_pulse()
        self.app.audio.replay_current()

    def save_and_quit(self, dialog: tk.Toplevel) -> None:
        from .menu import MenuScreen

        dialog.destroy()
        self.paused = False
        self.stop_timer()
        self.state.remaining_seconds = self.remaining
        self.state.save()
        self.app.show_screen(MenuScreen)

    # ================================================================== timer
    def on_show(self) -> None:
        self.play_level_music()
        resume_from = self.state.remaining_seconds
        self.state.remaining_seconds = None
        total = config.DIFFICULTY_TIMES.get(self.state.difficulty or "medium",
                                            config.DIFFICULTY_TIMES["medium"])
        self.total_seconds = total
        self.start_timer(
            from_seconds=resume_from if resume_from is not None else total)

    def start_timer(self, from_seconds: int | None) -> None:
        self.remaining = from_seconds if from_seconds is not None else 0
        if not self.total_seconds:
            self.total_seconds = max(self.remaining, 1)
        self.tick_timer()

    def stop_timer(self) -> None:
        if self.timer_job:
            try:
                self.after_cancel(self.timer_job)
            except Exception:
                pass
            self.timer_job = None

    def tick_timer(self) -> None:
        if self.paused:
            return
        minutes, seconds = divmod(max(self.remaining, 0), 60)
        self.timer_label.config(
            text=f"{minutes}:{seconds:02d}",
            fg=self.theme.timer_color(self.remaining, self.total_seconds))
        self.time_bar.set(self.remaining / max(self.total_seconds, 1))
        if self.remaining <= 0:
            self.game_over()
            return
        self.remaining -= 1
        self.timer_job = self.after(1000, self.tick_timer)

    def game_over(self) -> None:
        from .game_over import GameOverScreen

        self.stop_timer()
        self._stop_pulse()
        self.app.audio.stop()
        self.state.remaining_seconds = None
        self.state.save()
        self.app.show_screen(GameOverScreen)

    # =============================================================== progress
    def check_next_room(self) -> None:
        if not self.state.tasks_done(self.level_number):
            toast(self.stage, self.theme, tr("level.incomplete"), kind="warn")
            return
        self.advance()

    def advance(self) -> None:
        from .game_over import route_after_level

        self.stop_timer()
        self._stop_pulse()
        self.state.remaining_seconds = None
        route_after_level(self.app, self.level_number)

    def on_close(self) -> None:
        self.stop_timer()
        self._stop_pulse()
        try:
            self.app.root.unbind("<Escape>")
        except Exception:
            pass
