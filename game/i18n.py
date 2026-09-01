"""Tiny internationalisation layer backed by game.strings.STRINGS."""
from __future__ import annotations

from .strings import STRINGS


class _Translator:
    def __init__(self) -> None:
        self.language = "en"

    def set_language(self, language: str) -> None:
        self.language = "fa" if language == "fa" else "en"

    @property
    def is_fa(self) -> bool:
        return self.language == "fa"

    def __call__(self, key: str, **kwargs) -> str:
        entry = STRINGS.get(key)
        if not entry:
            return key
        value = entry.get(self.language) or entry.get("en") or key
        if isinstance(value, str) and kwargs:
            return value.format(**kwargs)
        return value

    def lines(self, key: str) -> list[str]:
        """Return list-valued strings (objectives panel)."""
        entry = STRINGS.get(key) or {}
        return list(entry.get(self.language) or entry.get("en") or [])


tr = _Translator()
