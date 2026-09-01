"""Room 1: the color game, the chess puzzle and the three riddles."""
from __future__ import annotations

from ..i18n import tr
from ..minigames import ChessPuzzle, ColorGame, RiddleGame
from .level_base import LevelScreen

RIDDLE_TASKS = ("riddle1", "riddle2", "riddle3")


class Level1Screen(LevelScreen):
    level_number = 1

    # Panel order: color / riddles / chess.
    def objective_status(self) -> list[bool]:
        return [
            self.state.task(1, "color"),
            all(self.state.task(1, name) for name in RIDDLE_TASKS),
            self.state.task(1, "chess"),
        ]

    def hotspots(self) -> list[dict]:
        done = self.objective_status()
        return [
            {"fraction": self.fraction((245, 114, 370, 200)),
             "callback": lambda: self.launch(ColorGame),
             "label": tr("spot.color"), "done": done[0]},
            {"fraction": self.fraction((710, 160, 837, 275)),
             "callback": lambda: self.launch(RiddleGame),
             "label": tr("spot.riddles"), "done": done[1]},
            {"fraction": self.fraction((200, 375, 1040, 490)),
             "callback": lambda: self.launch(ChessPuzzle),
             "label": tr("spot.chess"), "done": done[2]},
        ]

    def launch(self, minigame_cls) -> None:
        if self.paused:
            return
        window = minigame_cls(self.app)
        self.wait_window(window)
        self._apply_result(window)

    def _apply_result(self, window) -> None:
        if not getattr(window, "result", False):
            return
        if isinstance(window, ColorGame):
            self.state.complete_task(1, "color")
        elif isinstance(window, ChessPuzzle):
            self.state.complete_task(1, "chess")
        elif isinstance(window, RiddleGame):
            for name in RIDDLE_TASKS:
                self.state.complete_task(1, name)
        self.refresh_objectives()
