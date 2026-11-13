"""Точки інтересу на поверхні планет: місця посадок, марсоходи, місії.
Координати перевірте перед показом, вони наближені."""

import math
import os

from panda3d.core import Vec3

LANDMARK_DATA = [

]

LANDMARK_BY_NAME = {d["name"]: d for d in LANDMARK_DATA}

class Landmark:
    pass