from direct.gui.DirectGui import DirectButton
from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties

import config
from audio import StemMixer
from effects import StarField
from events import EventBus
from fonts import get_font
from landmark import LANDMARK_BY_NAME, LANDMARK_DATA
from landmarkUI import LandmarkPanel
from menu import MainMenu
from narration import NarrationPlayer
from scene import Scene
from showcase import ShowcaseViewer
from timeline import Timeline


class App(ShowBase):
    def __init__(self):
        super().__init__()
        self.setup_window()

        self.started = False
        self.bus = EventBus()
        self.scene = Scene(self, self.bus)
        self.world = self.scene.render
        self.stars = StarField(self, config.STAR_COUNT, self.world)
        self.mixer = StemMixer(self)
        self.mixer.set_master(config.DEFAULT_MUSIC_VOLUME)
        self.timeline = Timeline(self.bus)
        self.narration = NarrationPlayer(self)

        self.panel = LandmarkPanel(
            self,
            LANDMARK_DATA,
            on_pick=self._pick_landmark,
            on_back=self.back_to_tour,
        )
        self.panel.hide()

        self.showcase = ShowcaseViewer(self, on_close=self.close_showcase)
        self.showcase_button = DirectButton(
            parent=self.a2dTopRight,
            text="3D-апарати",
            text_font=get_font(self),
            scale=0.06,
            pos=(-0.3, 0, -0.15),
            command=self.open_showcase,
        )
        self.showcase_button.hide()

        self.menu = MainMenu(
            self,
            on_start=self.start_experience,
            on_volume=self.mixer.set_master,
            on_voice_toggle=self.narration.set_enabled,
        )

        self.setup_subscriptions()
        self.setup_keys()

    def setup_window(self):
        props = WindowProperties()
        props.setTitle(config.WINDOW_TITLE)
        props.setSize(*config.WINDOW_SIZE)
        self.win.requestProperties(props)
        self.setBackgroundColor(0.0, 0.0, 0.02, 1.0)
        self.disableMouse()

    def setup_subscriptions(self):
        self.bus.subscribe("object_selected", self.scene._on_object_selected)
        self.bus.subscribe("object_selected", self._on_object_selected)
        self.bus.subscribe("landmark_selected", self._on_landmark_selected)
        self.bus.subscribe("scene_started", self._on_scene_started)

    def setup_keys(self):
        self.accept("space", self._key_if_ready, [self.timeline.toggle_pause])
        self.accept("arrow_right", self._key_if_ready, [self.narration.next_caption])
        self.accept("n", self._key_if_ready, [self.timeline.next_scene])
        self.accept("r", self._key_if_ready, [self.narration.replay])
        self.accept("escape", self._on_escape)

    def _key_if_ready(self, action):
        if self.started and not self.showcase.active:
            action()

    def _on_escape(self):
        if not self.started:
            return
        if self.showcase.active:
            self.showcase.close()
        else:
            self.back_to_tour()

    def _on_object_selected(self, name):
        self.mixer.set_object(name)
        self.panel.show_for(name)
        self.panel.hide_inspect()

    def _on_landmark_selected(self, name):
        data = LANDMARK_BY_NAME[name]
        self.timeline.pause()
        self.narration.clear()
        self.scene.focus_on(name)
        self.mixer.set_object(self.scene.landmarks[name].body)
        self.panel.show_for(data["body"])
        self.panel.show_inspect(data["title"], data["text"])

    def _on_scene_started(self, title, voice, captions, layers):
        self.narration.play_scene(voice, captions)
        group = self.timeline.scenes[self.timeline.index]["focus"]
        for track, level in layers.items():
            self.mixer.set_layer(group, track, level)

    def _pick_landmark(self, name):
        self.bus.publish("landmark_selected", name=name)

    def back_to_tour(self):
        if not self.started or self.showcase.active:
            return
        self.timeline.resume()

    def start_experience(self):
        if self.started:
            return
        self.started = True

        self.scene.build()
        self.stars.build()
        self.mixer.load()
        self.mixer.start()
        self.panel.show()
        self.showcase_button.show()

        self.taskMgr.add(self.scene.update, "scene-update")
        self.taskMgr.add(self.mixer.update, "mixer-update")
        self.taskMgr.add(self.timeline.update, "timeline-update")
        self.taskMgr.add(self.narration.update, "narration-update")

        self.timeline.start()

    def open_showcase(self):
        if not self.started or self.showcase.active:
            return
        self.timeline.pause()
        self.narration.clear()
        self.scene.camera_enabled = False
        self.world.hide()
        self.panel.hide()
        self.showcase_button.hide()
        self.showcase.open()

    def close_showcase(self):
        self.world.show()
        self.scene.camera_enabled = True
        self.panel.show()
        self.showcase_button.show()
        self.timeline.resume()