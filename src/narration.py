"""Озвучка і субтитри, синхронізовані з часом сцени."""

import os

from direct.gui.DirectGui import OnscreenText
from panda3d.core import ClockObject, TextNode

import config
from fonts import get_font


class NarrationPlayer:
    def __init__(self, base):
        self.base = base
        self.enabled = True
        self.current_sound = None
        self._voice_path = None
        self.captions = []
        self.scene_time = 0.0
        self._shown = None
        self.clock = ClockObject.getGlobalClock()
        self.subtitle = OnscreenText(
            parent=base.a2dBottomCenter,
            text="",
            font=get_font(base),
            pos=(0, 0.25),
            scale=0.05,
            fg=(1, 1, 1, 1),
            align=TextNode.ACenter,
            wordwrap=40,
        )

    def play_scene(self, voice, captions):
        self.stop()
        self._voice_path = voice if voice and os.path.exists(voice) else None
        if voice and self._voice_path is None:
            print(f"Voice file not found: {voice}")

        self.captions = captions or []
        self.scene_time = 0.0
        self._shown = None
        self._play_voice_from(0.0)

    def update(self, task):
        if not self.captions:
            return task.cont

        self.scene_time += self.clock.getDt()
        text = ""
        for caption in self.captions:
            if self.scene_time >= caption["start"]:
                text = caption["text"]

        if text != self._shown:
            self._shown = text
            self.subtitle.setText(text)
        return task.cont

    def clear(self):
        self.stop()
        self.captions = []
        self._voice_path = None
        self._shown = None
        self.subtitle.setText("")

    def stop(self):
        if self.current_sound is not None:
            self.current_sound.stop()
            self.current_sound = None

    def set_enabled(self, value):
        self.enabled = value
        if value:
            self._play_voice_from(self.scene_time)
        else:
            self.stop()

    def next_caption(self):
        upcoming = [c for c in self.captions if c["start"] > self.scene_time]
        if not upcoming:
            return
        target = upcoming[0]["start"]
        self.scene_time = target
        self._shown = None
        self._play_voice_from(target)

    def replay(self):
        self.scene_time = 0.0
        self._shown = None
        self._play_voice_from(0.0)

    def _play_voice_from(self, seconds):
        self.stop()
        if not self.enabled or not self._voice_path:
            return
        self.current_sound = self.base.loader.loadSfx(self._voice_path)
        self.current_sound.setVolume(config.VOICE_VOLUME)
        self.current_sound.setTime(seconds)
        self.current_sound.play()