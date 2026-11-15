"""Марс, Місяць і точки інтересу: тіла, світло, обертання і камера."""

import os

from panda3d.core import AmbientLight, ClockObject, PointLight, Vec3

import config
from landmark import LANDMARK_DATA, Landmark

BODY_DATA = {
    "mars": {
        "pos": (-6.0, 0.0, 0.0),
        "radius": 2.0,
        "spin": 24.0,
        "color": (0.8, 0.4, 0.2, 1.0),
        "texture": "assets/textures/mars.jpg",
    },
    "moon": {
        "pos": (6.0, 0.0, 0.0),
        "radius": 1.5,
        "spin": 60.0,
        "color": (0.6, 0.6, 0.6, 1.0),
        "texture": "assets/textures/moon.jpg",
    },
}

LIGHT_POS = (-30.0, -25.0, 15.0)


class CelestialBody:
    def __init__(self, base, name, pos, radius, spin_period, color, texture_path=None):
        self.base = base
        self.name = name
        self.pos = pos
        self.radius = radius
        self.spin_period = spin_period
        self.color = color
        self.texture_path = texture_path
        self.node = None

    def build(self, parent):
        self.node = parent.attachNewNode(self.name)
        self.node.setPos(*self.pos)

        model = self.base.loader.loadModel("models/misc/sphere")
        model.reparentTo(self.node)
        model.setScale(self.radius)

        if self.texture_path and os.path.exists(self.texture_path):
            model.setTexture(self.base.loader.loadTexture(self.texture_path), 1)
        else:
            model.setColor(*self.color)

    def update(self, time_elapsed):
        if self.node is None or self.spin_period <= 0:
            return
        self.node.setH((time_elapsed / self.spin_period) * 360.0 % 360.0)


class Scene:
    def __init__(self, base, bus):
        self.base = base
        self.bus = bus
        # Окремий вузол світу: ховається разом з туром під час огляду апаратів
        self.render = base.render.attachNewNode("world")
        self.bodies = {}
        self.landmarks = {}
        self.focus_name = None
        self.camera_enabled = True
        self.clock = ClockObject.getGlobalClock()

    def build(self):
        for name, data in BODY_DATA.items():
            body = CelestialBody(
                self.base, name,
                pos=data["pos"],
                radius=data["radius"],
                spin_period=data["spin"],
                color=data["color"],
                texture_path=data["texture"],
            )
            body.build(self.render)
            self.bodies[name] = body

        for data in LANDMARK_DATA:
            parent = self.bodies[data["body"]]
            lm = Landmark(self.base, data, parent.node, parent.radius)
            lm.build()
            self.landmarks[data["name"]] = lm

        sun_light = PointLight("sun_light")
        sun_light.setColor((1.0, 0.95, 0.85, 1.0))
        sun_light.setAttenuation((1.0, 0.0, 0.0))
        sun_np = self.render.attachNewNode(sun_light)
        sun_np.setPos(*LIGHT_POS)
        self.render.setLight(sun_np)

        ambient = AmbientLight("ambient")
        ambient.setColor((0.06, 0.06, 0.08, 1.0))
        self.render.setLight(self.render.attachNewNode(ambient))

        self.render.setShaderAuto()

        self.focus_on("mars")
        self._place_camera_now()

    def update(self, task):
        t = self.clock.getFrameTime()
        dt = min(self.clock.getDt(), config.MAX_DT)

        for body in self.bodies.values():
            body.update(t)

        if not self.camera_enabled or self.focus_name is None:
            return task.cont

        info = self._focus_info(self.focus_name)
        if info is None:
            return task.cont

        node, dist, direction = info
        target = node.getPos(self.render) + direction.normalized() * dist
        current = self.base.camera.getPos()
        k = min(1.0, config.CAMERA_LERP_SPEED * dt)
        self.base.camera.setPos(current + (target - current) * k)
        self.base.camera.lookAt(node)
        return task.cont

    def focus_on(self, name):
        if name not in self.bodies and name not in self.landmarks:
            print(f"Unknown focus target: {name}")
            return
        self.focus_name = name

    def _on_object_selected(self, name):
        self.focus_on(name)

    def _focus_info(self, name):
        """Повертає (вузол, відстань камери, напрямок від цілі до камери)."""
        if name in self.bodies:
            body = self.bodies[name]
            return body.node, body.radius * 4.0, Vec3(0, -1, 0.4)

        if name in self.landmarks:
            lm = self.landmarks[name]
            center = self.bodies[lm.body].node.getPos(self.render)
            normal = lm.node.getPos(self.render) - center
            if normal.length() == 0:
                normal = Vec3(0, -1, 0)
            return lm.node, 1.2, normal.normalized() + Vec3(0, 0, 0.15)

        return None

    def _place_camera_now(self):
        info = self._focus_info(self.focus_name)
        if info is None:
            return
        node, dist, direction = info
        self.base.camera.setPos(node.getPos(self.render) + direction.normalized() * dist)
        self.base.camera.lookAt(node)