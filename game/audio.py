"""Safe wrapper around pygame.mixer music playback."""
from __future__ import annotations

import os
import random

import pygame

from . import config


class AudioError(RuntimeError):
    pass


class AudioManager:
    """Initialises the mixer lazily and never crashes on missing files."""

    def __init__(self) -> None:
        self._ready = False
        self.volume = 1.0
        self.current_track: str | None = None
        self.init()

    def init(self) -> bool:
        if self._ready:
            return True
        try:
            pygame.mixer.init()
            self._ready = True
        except pygame.error:
            self._ready = False
        return self._ready

    @property
    def ready(self) -> bool:
        return self._ready

    def set_volume_percent(self, percent: int) -> None:
        self.volume = max(0, min(100, int(percent))) / 100.0
        if self._ready:
            try:
                pygame.mixer.music.set_volume(self.volume)
            except pygame.error:
                pass

    def play_file(self, path: str, loop: int = -1) -> bool:
        if not self.init() or not os.path.isfile(path):
            return False
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(loops=loop)
            self.current_track = path
            return True
        except pygame.error:
            return False

    def play_menu_music(self) -> None:
        self.play_file(config.MENU_MUSIC)

    def play_random_menu_track(self) -> str | None:
        name = random.choice(config.MENU_TRACKS)
        path = os.path.join(config.SOUNDS_DIR, name)
        return name if self.play_file(path) else None

    def replay_current(self) -> None:
        if self.current_track:
            self.play_file(self.current_track)

    def stop(self) -> None:
        if self._ready:
            try:
                pygame.mixer.music.stop()
            except pygame.error:
                pass

    def shutdown(self) -> None:
        self.stop()
        if self._ready:
            try:
                pygame.mixer.music.unload()
            except (pygame.error, AttributeError):
                pass
