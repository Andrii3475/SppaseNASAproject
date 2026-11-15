"""Точки інтересу на поверхні планет: місця посадок, марсоходи, місії.
Координати перевірте перед показом, вони наближені."""

import math
import os

from panda3d.core import Vec3

_RAW_LANDMARK = [
# ---------------- MOON ----------------
                     {
                         "name": "Surveyor Landers",
                         "body": "Moon",
                         "year": 1966,
                         "description": "Robotic probes sent in the 1960s to prove that soft landings on the Moon were possible.",
                         "image": None,
                         "position": None,
                     },
                     {
                         "name": "Apollo Lunar Modules",
                         "body": "Moon",
                         "year": 1969,
                         "description": "The descent stages of the Lunar Modules (like Apollo 11's Eagle) were left behind as launch pads.",
                         "image": None,
                         "position": None,
                     },
                     {
                         "name": "ALSEP Scientific Packages",
                         "body": "Moon",
                         "year": 1969,
                         "description": "Apollo Lunar Surface Experiments Packages (seismometers, retroreflectors, etc.) left to do science after the astronauts departed.",
                         "image": None,
                         "position": None,
                     },
                     {
                         "name": "Lunar Roving Vehicles (LRVs)",
                         "body": "Moon",
                         "year": 1971,
                         "description": "Three electric moon buggies driven by astronauts and parked permanently on the Moon.",
                         "image": None,
                         "position": None,
                     },

                     # ---------------- MARS ----------------
                     {
                         "name": "Viking 1 & 2 Landers",
                         "body": "Mars",
                         "year": 1976,
                         "description": "The first U.S. landers to successfully operate on Mars, remaining exactly where they touched down.",
                         "image": None,
                         "position": None,
                     },
                     {
                         "name": "Sojourner Rover",
                         "body": "Mars",
                         "year": 1997,
                         "description": "The first rover on Mars, delivered by the Pathfinder lander. Now permanently parked.",
                         "image": None,
                         "position": None,
                     },
                     {
                         "name": "Spirit & Opportunity",
                         "body": "Mars",
                         "year": 2004,
                         "description": "Twin rovers that operated for years. Both are now inactive monuments to Mars exploration.",
                         "image": None,
                         "position": None,
                     },
                     {
                         "name": "Phoenix Lander",
                         "body": "Mars",
                         "year": 2008,
                         "description": "Dug for water ice in the Martian arctic before eventually losing power.",
                         "image": None,
                         "position": None,
                     },
                     {
                         "name": "InSight Lander",
                         "body": "Mars",
                         "year": 2018,
                         "description": "Listened for marsquakes to study the interior of Mars. Eventually lost power.",
                         "image": None,
                         "position": None,
                     },
                     {
                         "name": "Ingenuity Helicopter",
                         "body": "Mars",
                         "year": 2021,
                         "description": "The first aircraft on another planet. Sustained rotor damage and became a stationary artifact.",
                         "image": None,
                         "position": None,
                     },
]

class Landmark:
    def __init__(self, base, data, body_node, body_radius):
        self.base = base
        self.data = data
        self.name = data["name"]
        self.body = data["body"]
        self.body_node = body_node
        self.body_radius = body_radius
        self.node = None

    def build(self):
        lat = math.radians(self.data["lat"])
        lon = math.radians(self.data["lon"])
        r = self.body_radius * 1.02

        pos = Vec3(
            r * math.cos(lat) * math.cos(lon),
            r * math.cos(lat) * math.sin(lon),
            r * math.sin(lat),
        )

        # Вузол дочірній до тіла, тож обертається разом з планетою
        self.node = self.body_node.attachNewNode(self.name)
        self.node.setPos(pos)

        model_path = self.data.get("model")
        if model_path and os.path.exists(model_path):
            marker = self.base.loader.loadModel(model_path)
            marker.setScale(self.data.get("scale", 1.0))
        else:
            # Заглушка: жовтий куб, доки немає моделі
            marker = self.base.loader.loadModel("models/box")
            marker.setScale(0.08)
            marker.setPos(-0.04, -0.04, -0.04)
            marker.setColor(1.0, 0.85, 0.2, 1.0)
            marker.setLightOff()

        marker.reparentTo(self.node)

# Координати (широта, довгота) у градусах для записів, де position = None.
PLACE_POSITIONS = {
    "Surveyor Landers": (-2.45, -43.20),
    "Apollo Lunar Modules": (0.67, 23.47),
    "ALSEP Scientific Packages": (-3.01, -23.42),
    "Lunar Roving Vehicles (LRVs)": (26.13, 3.63),
    "Viking 1 & 2 Landers": (22.27, -47.97),
    "Sojourner Rover": (19.13, -33.22),
    "Spirit & Opportunity": (-14.57, 175.47),
    "Phoenix Lander": (68.22, -125.75),
    "InSight Lander": (4.50, 135.62),
    "Ingenuity Helicopter": (18.44, 77.45),
}


def _normalize(d):
    pos = d.get("position") or PLACE_POSITIONS.get(d["name"])
    if pos is None:
        return None
    return {
        "name": d["name"],
        "body": d["body"].lower(),
        "lat": pos[0],
        "lon": pos[1],
        "title": d["name"],
        "text": d.get("description", ""),
        "model": None,
        "image": d.get("image"),
        "year": d.get("year"),
        "scale": 1.0,
    }


LANDMARK_DATA = [n for n in (_normalize(d) for d in _RAW_LANDMARK) if n is not None]
LANDMARK_BY_NAME = {d["name"]: d for d in LANDMARK_DATA}