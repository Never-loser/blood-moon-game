"""Snake minigame (level 3).

Fixes vs the old version: works in both themes (labels were only built
under theme 1 → NameError), adds self-collision + 180° reversal guards,
wins immediately at the target score and uses the real score/time values
when restarting.
"""
from __future__ import annotations

import random
import tkinter as tk

from .. import config
from .base import Minigame

CELL = 10
GRID = 40  # GRID * CELL == canvas side


class SnakeGame(Minigame):
    def __init__(self, app):
        super().__init__(app, size=(420, 460))
        self.title("Snake")

        self.snake = [(20, 20), (20, 30), (20, 40)]
        self.direction = "Down"
        self.food = self._spawn_food()
        self.score = 0
        self.time_left = config.SNAKE_START_TIME
        self.game_over = False
        self._move_job = None
        self._timer_job = None

        hud = tk.Frame(self, bg=self.theme.bg)
        hud.pack(fill=tk.X)
        # Built unconditionally — theme 2 used to crash here.
        self.score_label = tk.Label(hud, text="Score: 0", font=("Arial", 14),
                                    bg=self.theme.bg, fg=self.theme.fg)
        self.score_label.pack(side=tk.LEFT, padx=12, pady=4)
        self.timer_label = tk.Label(hud, text=f"Time Left: {self.time_left}s",
                                    font=("Arial", 14), bg=self.theme.bg, fg=self.theme.fg)
        self.timer_label.pack(side=tk.RIGHT, padx=12)

        self.canvas = tk.Canvas(self, width=GRID * CELL, height=GRID * CELL,
                                bg="black", highlightthickness=0)
        self.canvas.pack(padx=10, pady=6)

        self.restart_button = tk.Button(self, text="Restart", font=("Arial", 12),
                                        command=self.restart_game)
        # packed only when the round ends

        self.bind("<Key>", self.change_direction)
        self.focus_force()
        self.update_loop()
        self.tick_timer()

    # ------------------------------------------------------------------ helpers
    @staticmethod
    def _spawn_food() -> tuple[int, int]:
        return random.randint(0, GRID - 1) * CELL, random.randint(0, GRID - 1) * CELL

    def change_direction(self, event: tk.Event) -> None:
        opposites = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        wanted = event.keysym
        if wanted in opposites and opposites[wanted] != self.direction:
            self.direction = wanted

    # ------------------------------------------------------------------ loop
    def update_loop(self) -> None:
        if not self.game_over:
            self.move_snake()
            self.check_collisions()
            self.draw()
            self._move_job = self.after(config.SNAKE_TICK_MS, self.update_loop)

    def move_snake(self) -> None:
        head_x, head_y = self.snake[-1]
        dx, dy = {"Up": (0, -CELL), "Down": (0, CELL),
                  "Left": (-CELL, 0), "Right": (CELL, 0)}[self.direction]
        head = (head_x + dx, head_y + dy)
        self.snake.append(head)
        if head == self.food:
            self.score += 10
            self.food = self._spawn_food()
            if self.score >= config.SNAKE_WIN_SCORE:
                self.draw(win=True)
                self.game_over = True
                self.finish()
                return
        else:
            self.snake.pop(0)

    def check_collisions(self) -> None:
        head_x, head_y = self.snake[-1]
        hit_wall = not (0 <= head_x < GRID * CELL and 0 <= head_y < GRID * CELL)
        hit_self = len(self.snake) > len(set(self.snake))
        if hit_wall or hit_self:
            self.end_round(won=False)

    def end_round(self, won: bool) -> None:
        self.game_over = True
        self.draw(win=won)
        if not self.result:
            self.restart_button.pack(pady=(4, 8))  # retry offer after a loss

    def draw(self, win: bool = False) -> None:
        canvas = self.canvas
        canvas.delete(tk.ALL)
        for x, y in self.snake:
            canvas.create_rectangle(x, y, x + CELL, y + CELL, fill="green")
        fx, fy = self.food
        canvas.create_oval(fx, fy, fx + CELL, fy + CELL, fill="red")
        self.score_label.config(text=f"Score: {self.score}")
        if self.game_over and not win:
            canvas.create_text(GRID * CELL // 2, GRID * CELL // 2 - 15,
                               text="Game Over!", fill="white", font=("Arial", 24))
            canvas.create_text(GRID * CELL // 2, GRID * CELL // 2 + 20,
                               text=f"score {self.score}/{config.SNAKE_WIN_SCORE}",
                               fill="orange", font=("Arial", 14))
        elif win:
            canvas.create_text(GRID * CELL // 2, GRID * CELL // 2 - 15,
                               text="You Win!", fill="yellow", font=("Arial", 26))

    def tick_timer(self) -> None:
        if self.result:
            return
        if not self.game_over:
            self.time_left -= 1
            self.timer_label.config(text=f"Time Left: {max(self.time_left, 0)}s")
            if self.time_left <= 0:
                self.end_round(won=False)
                return
            self._timer_job = self.after(1000, self.tick_timer)

    def restart_game(self) -> None:
        self.snake = [(20, 20), (20, 30), (20, 40)]
        self.direction = "Down"
        self.food = self._spawn_food()
        self.score = 0
        self.time_left = config.SNAKE_START_TIME
        self.game_over = False
        self.timer_label.config(text=f"Time Left: {self.time_left}s")
        self.restart_button.pack_forget()
        self.update_loop()
        self.tick_timer()

    def on_close(self) -> None:
        self.game_over = True
        for job in (self._move_job, self._timer_job):
            if job:
                try:
                    self.after_cancel(job)
                except Exception:
                    pass
