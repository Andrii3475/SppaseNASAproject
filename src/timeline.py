"""Сценарій презентації. Може бути призупинений, коли користувач сам оглядає точку."""

from panda3d.core import ClockObject

OBJECT_MIX = None  # більше не використовується, мікс задає audio.py

SCENES = [
    {
        "focus": "mars",
        "duration": 120.0,
        "title": "Марс",
        "voice": "",
        "text": "Марс — четверта планета від Сонця.",
    },
    {
        "focus": "moon",
        "duration": 120.0,
        "title": "Місяць",
        "voice": "",
        "text": "Місяць — природний супутник Землі.",
    },
]


class Timeline:
    def __init__(self, bus, scenes=SCENES):
        self.bus = bus
        self.scenes = scenes
        self.index = 0
        self.elapsed = 0.0
        self.paused = False
        self.clock = ClockObject.getGlobalClock()

    def start(self):
        self.index = 0
        self.elapsed = 0.0
        self.paused = False
        self._announce()

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False
        self.elapsed = 0.0
        self._announce()

    def toggle_pause(self):
        self.paused = not self.paused

    def next_scene(self):
        self.index = (self.index + 1) % len(self.scenes)
        self.elapsed = 0.0
        self.paused = False
        self._announce()

    def update(self, task):
        if self.paused:
            return task.cont
        self.elapsed += self.clock.getDt()
        if self.elapsed >= self.scenes[self.index]["duration"]:
            self.index = (self.index + 1) % len(self.scenes)
            self.elapsed = 0.0
            self._announce()
        return task.cont

    def _announce(self):
        scene = self.scenes[self.index]
        self.bus.publish("object_selected", name=scene["focus"])
        self.bus.publish(
            "scene_started",
            title=scene["title"],
            voice=scene["voice"],
            captions=scene.get("captions", []),
            layers=scene.get("layers", {}),
        )