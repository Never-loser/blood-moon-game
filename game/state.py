"""Game state + JSON persistence (with legacy saving.txt migration)."""
from __future__ import annotations

import json
from typing import Any

from . import config

SAVE_VERSION = 2

LEGACY_TOKEN_TO_LEVEL = {"Level1": 1, "Level2": 2, "Level3": 3}

TASK_NAMES = {
    1: ["color", "chess", "riddle1", "riddle2", "riddle3"],
    2: ["math1", "math2", "math3", "bio1", "bio2", "bio3",
        "chem1", "chem2", "chem3"],
    3: ["math_sprint", "maze", "snake"],
}


class GameState:
    """Holds every mutable setting and the in-run puzzle flags."""

    def __init__(self) -> None:
        self.theme_id: int = 1
        self.language: str = "en"
        self.volume: int = 100
        self.difficulty: str | None = None          # easy / medium / hard
        self.current_level: int = 1                 # unlocked/current level
        self.remaining_seconds: int | None = None   # persisted pause state
        self.reset_run_flags()

    # ------------------------------------------------------------------ run flags
    def reset_run_flags(self) -> None:
        self.level_tasks: dict[int, dict[str, bool]] = {
            level: {name: False for name in names}
            for level, names in TASK_NAMES.items()
        }

    def tasks_done(self, level: int) -> bool:
        return all(self.level_tasks.get(level, {}).values())

    def task(self, level: int, name: str) -> bool:
        return self.level_tasks[level][name]

    def complete_task(self, level: int, name: str) -> None:
        self.level_tasks[level][name] = True

    # ------------------------------------------------------------------ persistence
    def to_dict(self) -> dict[str, Any]:
        return {
            "version": SAVE_VERSION,
            "theme": self.theme_id,
            "language": self.language,
            "volume": self.volume,
            "difficulty": self.difficulty,
            "level": self.current_level,
            "remaining_seconds": self.remaining_seconds,
        }

    def save(self) -> None:
        try:
            with open(config.SAVE_PATH, "w", encoding="utf-8") as fh:
                json.dump(self.to_dict(), fh, ensure_ascii=False, indent=2)
        except OSError:
            pass  # never crash the game because saving failed

    @classmethod
    def load(cls) -> "GameState":
        state = cls()
        data = _read_json() or _read_legacy()
        if not data:
            return state
        theme = data.get("theme")
        if theme in (1, 2):
            state.theme_id = theme
        lang = data.get("language")
        if lang in ("en", "fa"):
            state.language = lang
        volume = data.get("volume")
        if isinstance(volume, int) and 0 <= volume <= 100:
            state.volume = volume
        difficulty = data.get("difficulty")
        if difficulty in config.DIFFICULTY_TIMES:
            state.difficulty = difficulty
        level = data.get("level")
        if isinstance(level, int) and level in (1, 2, 3):
            state.current_level = level
        remaining = data.get("remaining_seconds")
        if isinstance(remaining, int) and remaining >= 0:
            state.remaining_seconds = remaining
        return state


def _read_json() -> dict | None:
    try:
        with open(config.SAVE_PATH, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        if isinstance(data, dict):
            return data
    except (OSError, ValueError):
        pass
    return None


def _read_legacy() -> dict | None:
    """Read the old single-line saving.txt ('Level1'..'Level3') if present.

    The legacy file is left untouched on disk; new saves go to save.json.
    """
    try:
        with open(config.LEGACY_SAVE_PATH, "r", encoding="utf-8") as fh:
            first = fh.readline().strip()
    except OSError:
        return None
    level = LEGACY_TOKEN_TO_LEVEL.get(first.split()[0] if first else "")
    if level is None:
        for token, mapped in LEGACY_TOKEN_TO_LEVEL.items():
            if token in first:
                level = mapped
                break
    if level is None:
        return None
    return {"version": SAVE_VERSION, "level": level}
