"""Canvas maze (level 3) with bounds checking and animated hazards.

The original indexed the map without bounds checks (IndexError at the
edges) and drew obstacles that never moved; both are fixed here.
"""
from __future__ import annotations

import tkinter as tk

from ..config import MAZE_CELL_SIZE
from ..quiz_data import MAZE_MAP, MAZE_OBSTACLES
from .base import Minigame

PLAYER_START = (1, 1)
OBSTACLE_TICK_MS = 350


class MazeGame(Minigame):
    def __init__(self, app):
        rows, cols = len(MAZE_MAP), len(MAZE_MAP[0])
        width = cols * MAZE_CELL_SIZE + 20
        height = rows * MAZE_CELL_SIZE + 20
        super().__init__(app, size=(width, height))
        self.title("Maze")

        self.player_pos = list(PLAYER_START)
        self.won = False

        self.canvas = tk.Canvas(self, width=cols * MAZE_CELL_SIZE,
                                height=rows * MAZE_CELL_SIZE, bg="white",
                                highlightthickness=0)
        self.canvas.pack(padx=10, pady=10)
        self._draw_maze()

        # Animated hazards: (row, col, d_row, d_col)
        self.obstacles = [list(o) for o in MAZE_OBSTACLES]
        self.obstacle_ids = [
            self._draw_cell(row, col, "yellow") for row, col, _dR, _dC in self.obstacles
        ]

        self.player_id = self._draw_player()
        self._obstacle_job = None
        self.bind("<KeyPress>", self.on_key)
        self.focus_force()
        self.animate_obstacles()

    # ------------------------------------------------------------------ drawing
    def _draw_maze(self) -> None:
        for row_index, row in enumerate(MAZE_MAP):
            for col_index, cell in enumerate(row):
                if cell == 1:
                    self._draw_cell(row_index, col_index, "black")
                elif cell == 2:
                    self._draw_cell(row_index, col_index, "red")

    def _draw_cell(self, row: int, col: int, color: str) -> int:
        x0 = col * MAZE_CELL_SIZE
        y0 = row * MAZE_CELL_SIZE
        return self.canvas.create_rectangle(x0, y0, x0 + MAZE_CELL_SIZE,
                                            y0 + MAZE_CELL_SIZE, fill=color, width=0)

    def _draw_player(self) -> int:
        x0 = self.player_pos[1] * MAZE_CELL_SIZE + 5
        y0 = self.player_pos[0] * MAZE_CELL_SIZE + 5
        size = MAZE_CELL_SIZE - 10
        return self.canvas.create_oval(x0, y0, x0 + size, y0 + size, fill="green")

    def _redraw_player(self) -> None:
        self.canvas.delete(self.player_id)
        self.player_id = self._draw_player()

    # ------------------------------------------------------------------ movement
    def on_key(self, event: tk.Event) -> None:
        if self.won:
            return
        deltas = {"Left": (0, -1), "Right": (0, 1),
                  "Up": (-1, 0), "Down": (1, 0),
                  "a": (0, -1), "d": (0, 1), "w": (-1, 0), "s": (1, 0)}
        delta = deltas.get(event.keysym)
        if not delta:
            return
        new_row = self.player_pos[0] + delta[0]
        new_col = self.player_pos[1] + delta[1]

        # Bounds check — the old code crashed with IndexError here.
        if not (0 <= new_row < len(MAZE_MAP) and 0 <= new_col < len(MAZE_MAP[0])):
            return
        if MAZE_MAP[new_row][new_col] == 1:
            return

        self.player_pos = [new_row, new_col]
        self._redraw_player()
        self.check_hazard_hit()
        if not self.won and MAZE_MAP[new_row][new_col] == 2:
            self.win()

    def win(self) -> None:
        self.won = True
        self.finish()

    # ------------------------------------------------------------------ hazards
    def animate_obstacles(self) -> None:
        if self.won:
            return
        for obstacle, rect_id in zip(self.obstacles, self.obstacle_ids):
            row, col, d_row, d_col = obstacle
            n_row, n_col = row + d_row, col + d_col
            inside = 0 <= n_row < len(MAZE_MAP) and 0 <= n_col < len(MAZE_MAP[0])
            if inside and MAZE_MAP[n_row][n_col] != 1:
                obstacle[0], obstacle[1] = n_row, n_col
            else:
                obstacle[2], obstacle[3] = -d_row, -d_col
            x0 = obstacle[1] * MAZE_CELL_SIZE
            y0 = obstacle[0] * MAZE_CELL_SIZE
            self.canvas.coords(rect_id, x0, y0, x0 + MAZE_CELL_SIZE, y0 + MAZE_CELL_SIZE)
        self.check_hazard_hit()
        self._obstacle_job = self.after(OBSTACLE_TICK_MS, self.animate_obstacles)

    def check_hazard_hit(self) -> None:
        for row, col, _dR, _dC in self.obstacles:
            if [row, col] == self.player_pos:
                self.player_pos = list(PLAYER_START)
                self._redraw_player()
                return

    def on_close(self) -> None:
        self.won = True  # stops the animation loop
        if self._obstacle_job:
            try:
                self.after_cancel(self._obstacle_job)
            except Exception:
                pass
