"""Головний клас застосунку. Модулі спілкуються через шину подій."""

from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties

import config
from audio import StemMixer
from effects import StarField
from events import EventBus
from landmarkUI import LandmarkPanel
from landmark import LANDMARK_BY_NAME, LANDMARK_DATA
from menu import MainMenu
from narration import NarrationPlayer
from scene import Scene
from timeline import Timeline


class App(ShowBase):
    pass