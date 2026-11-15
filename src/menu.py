"""Головне меню: старт, гучність музики, перемикач озвучки."""

from direct.gui.DirectGui import DirectButton, DirectFrame, DirectSlider, OnscreenText
from panda3d.core import TextNode

import config
from fonts import get_font


class MainMenu:
    def __init__(self, base, on_start, on_volume, on_voice_toggle):
        self.base = base
        self.on_start = on_start
        self.on_volume = on_volume
        self.on_voice_toggle = on_voice_toggle
        self.voice_enabled = True
        self.font = get_font(base)
        self.build()

    def build(self):
        self.frame = DirectFrame(
            parent=self.base.aspect2d,
            frameColor=config.MENU_BG_COLOR,
            frameSize=(-1, 1, -1, 1),
        )

        OnscreenText(
            parent=self.frame,
            text=config.WINDOW_TITLE,
            font=self.font,
            pos=(0, 0.5),
            scale=0.12,
            fg=(1, 1, 1, 1),
            align=TextNode.ACenter,
        )

        DirectButton(
            parent=self.frame,
            text="Почати",
            text_font=self.font,
            scale=0.09,
            pos=(0, 0, 0.1),
            command=self._handle_start,
        )

        OnscreenText(
            parent=self.frame,
            text="Гучність музики",
            font=self.font,
            pos=(0, -0.05),
            scale=0.06,
            fg=(1, 1, 1, 1),
            align=TextNode.ACenter,
        )

        self.slider = DirectSlider(
            parent=self.frame,
            range=(0, 1),
            value=config.DEFAULT_MUSIC_VOLUME,
            pageSize=0.05,
            scale=0.6,
            pos=(0, 0, -0.15),
            command=self._handle_volume,
        )

        self.voice_button = DirectButton(
            parent=self.frame,
            text=self._voice_label(),
            text_font=self.font,
            scale=0.07,
            pos=(0, 0, -0.4),
            command=self._handle_voice_toggle,
        )

    def show(self):
        self.frame.show()

    def hide(self):
        self.frame.hide()

    def _voice_label(self):
        state = "увімк." if self.voice_enabled else "вимк."
        return f"Озвучка: {state}"

    def _handle_start(self):
        self.hide()
        self.on_start()

    def _handle_volume(self):
        self.on_volume(float(self.slider["value"]))

    def _handle_voice_toggle(self):
        self.voice_enabled = not self.voice_enabled
        self.voice_button["text"] = self._voice_label()
        self.on_voice_toggle(self.voice_enabled)