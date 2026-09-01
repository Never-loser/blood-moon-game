"""Screen package: every full-window frame of the game."""
from .base import Screen
from .menu import MenuScreen
from .settings import SettingsScreen
from .difficulty import DifficultyScreen
from .level1 import Level1Screen
from .level2 import Level2Screen
from .level3 import Level3Screen, EndScreen

__all__ = [
    "Screen", "MenuScreen", "SettingsScreen", "DifficultyScreen",
    "Level1Screen", "Level2Screen", "Level3Screen", "EndScreen",
]
