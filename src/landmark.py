"""Точки інтересу на поверхні планет: місця посадок, марсоходи, місії.
Координати перевірте перед показом, вони наближені."""

import math
import os

from panda3d.core import Vec3

LANDMARK_DATA = [
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

LANDMARK_BY_NAME = {d["name"]: d for d in LANDMARK_DATA}

class Landmark:
    pass