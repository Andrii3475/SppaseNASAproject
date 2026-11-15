"""Мікшування треків по об'єктах. Спільні треки грають завжди,
треки активного об'єкта звучать, решта плавно затихає."""

from panda3d.core import ClockObject

import config

TRACKS = {
    "common": {},
    "mars": {
        "BG": "assets/AudioSource/Mars/Audio2_BG.wav",
        "L1": "assets/AudioSource/Mars/Audio2_L1.wav",
        "L2": "assets/AudioSource/Mars/Audio2_L2.wav",
        "L3": "assets/AudioSource/Mars/Audio2_L3.wav",
        "L4": "assets/AudioSource/Mars/Audio2_L4.wav",
        "L5": "assets/AudioSource/Mars/Audio2_L5.wav",
        "L6": "assets/AudioSource/Mars/Audio2_L6.wav",
    },
    "moon": {
        "BG": "assets/AudioSource/Moon/Audio1_BG.wav",
        "L1": "assets/AudioSource/Moon/Audio1_L1.wav",
        "L2": "assets/AudioSource/Moon/Audio1_L2.wav",
        "L3": "assets/AudioSource/Moon/Audio1_L3.wav",
        "L4": "assets/AudioSource/Moon/Audio1_L4.wav",
        "L5": "assets/AudioSource/Moon/Audio1_L5.wav",
        "L6": "assets/AudioSource/Moon/Audio1_L6.wav",
    },
}

COMMON = "common"

# Постійні рівні шарів для планети. Приклад: {"mars": {"L5": 0.6, "L6": 0.0}}
LAYER_LEVELS = {
    "mars": {},
    "moon": {},
}


class StemMixer:
    def __init__(self, base, tracks=TRACKS, fade_speed=config.AUDIO_FADE_SPEED):
        self.base = base
        self.tracks = tracks
        self.fade_speed = fade_speed
        self.master = 1.0
        self.sounds = {}
        self.volumes = {}
        self.targets = {}
        self.clock = ClockObject.getGlobalClock()

    def load(self):
        for group, stems in self.tracks.items():
            for name, path in stems.items():
                key = (group, name)
                snd = self.base.loader.loadMusic(path)
                snd.setLoop(True)
                snd.setVolume(0.0)
                self.sounds[key] = snd
                self.volumes[key] = 0.0
                self.targets[key] = 1.0 if group == COMMON else 0.0

    def start(self):
        # Усі треки стартують в одному кадрі, щоб залишатися синхронними
        for snd in self.sounds.values():
            snd.play()

    def set_master(self, value):
        self.master = max(0.0, min(1.0, float(value)))

    def set_object(self, name):
        if name not in self.tracks or name == COMMON:
            print(f"Unknown music group: {name}")
            return

        for key in self.sounds:
            group, track = key
            if group == COMMON:
                self.targets[key] = 1.0
            elif group == name:
                self.targets[key] = LAYER_LEVELS.get(group, {}).get(track, 1.0)
            else:
                self.targets[key] = 0.0

    def set_layer(self, group, track, level):
        key = (group, track)
        if key in self.targets:
            self.targets[key] = max(0.0, min(1.0, float(level)))

    def update(self, task):
        dt = min(self.clock.getDt(), config.MAX_DT)
        step = self.fade_speed * dt

        for key, snd in self.sounds.items():
            cur = self.volumes[key]
            tgt = self.targets[key]
            if cur < tgt:
                cur = min(tgt, cur + step)
            elif cur > tgt:
                cur = max(tgt, cur - step)
            self.volumes[key] = cur
            snd.setVolume(cur * self.master)

        return task.cont