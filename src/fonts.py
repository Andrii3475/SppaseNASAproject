"""Один шрифт з кирилицею на весь застосунок."""

import os

import config

_cache = {}


def get_font(base):
    """Повертає шрифт або None, якщо файлу немає (тоді буде системний шрифт Panda3D)."""
    if "main" not in _cache:
        if os.path.exists(config.FONT_PATH):
            _cache["main"] = base.loader.loadFont(config.FONT_PATH)
        else:
            print(f"Font not found: {config.FONT_PATH}")
            _cache["main"] = None
    return _cache["main"]