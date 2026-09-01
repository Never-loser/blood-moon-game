"""Global configuration and asset paths for Blood Moon Ritual."""
from __future__ import annotations

import os
import sys

APP_NAME = "Blood Moon Ritual"
VERSION = "2.1.0"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PICTURES_DIR = os.path.join(BASE_DIR, "Pictures")
SOUNDS_DIR = os.path.join(BASE_DIR, "SoundEffects")
VIDEOS_DIR = os.path.join(BASE_DIR, "Videos")
SAVE_PATH = os.path.join(BASE_DIR, "save.json")
LEGACY_SAVE_PATH = os.path.join(BASE_DIR, "saving.txt")

INTRO_VIDEO = os.path.join(VIDEOS_DIR, "VID_20250519_105544.mp4")

MENU_MUSIC = os.path.join(SOUNDS_DIR, "startup.mp3")
MENU_TRACKS = [
    "music1.mp3", "music2.mp3", "music3.mp3",
    "music4.mp3", "music5.mp3", "music6.mp3", "music7.mp3",
]

LEVEL_MUSIC = {
    1: os.path.join(SOUNDS_DIR, "Enter Hallownest.mp3"),
    2: os.path.join(SOUNDS_DIR, "Hans-Zimmer-Day-One (1).mp3"),
    3: os.path.join(SOUNDS_DIR, "music4.mp3"),
}

STORY_NARRATION = {
    1: os.path.join(SOUNDS_DIR, "room1.wav"),
    2: os.path.join(SOUNDS_DIR, "room2.wav"),
    3: os.path.join(SOUNDS_DIR, "room3.wav"),
}
END_STORY = os.path.join(SOUNDS_DIR, "the end.wav")

LEVEL_BACKGROUNDS = {
    1: os.path.join(PICTURES_DIR, "image1.jpg"),
    2: os.path.join(PICTURES_DIR, "level2.jpg"),
    3: os.path.join(PICTURES_DIR, "level3.jpg"),
}

SETTINGS_BACKGROUND = os.path.join(PICTURES_DIR, "settings.jpg")
DIFFICULTY_BACKGROUND = os.path.join(PICTURES_DIR, "difficulties.jpg")
MAIN_MENU_FALLBACK_BG = os.path.join(PICTURES_DIR, "main_menu_bg.jpg")

# Difficulty -> total level time in seconds.
DIFFICULTY_TIMES = {
    "easy": 15 * 60,
    "medium": 10 * 60,
    "hard": 5 * 60,
}
DIFFICULTY_ORDER = ("easy", "medium", "hard")

# Positions shown in the level HUD.
LEVEL_PROGRESS_PERCENT = {1: 30, 2: 60, 3: 90}

COLOR_GAME_COLORS = ["purple", "red", "blue", "yellow", "white", "orange"]
COLOR_GAME_TARGET_SCORE = 10
COLOR_GAME_TIME = 40

MATH_SPRINT_TARGET_SCORE = 10
MATH_SPRINT_TIME = 60

MAZE_CELL_SIZE = 40
SNAKE_WIN_SCORE = 70
SNAKE_TICK_MS = 80
SNAKE_START_TIME = 45


def asset(*parts: str) -> str:
    return os.path.join(BASE_DIR, *parts)


def resource_path(relative: str) -> str:
    """Resolve a path relative to the project root (works when frozen too)."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(BASE_DIR, relative)
