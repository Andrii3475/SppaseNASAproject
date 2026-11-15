"""Панель точок інтересу: кнопки для поточної планети і картка з описом."""

from direct.gui.DirectGui import DirectButton, DirectFrame, OnscreenText
from panda3d.core import TextNode

from fonts import get_font

class LandmarkPanel:
    def __init__(self, base, landmarks, on_pick, on_back):
        self.base = base
        self.landmarks = landmarks
        self.on_pick = on_pick
        self.on_back = on_back
        self.font = get_font(base)
        self.buttons = []
        self.build()

    def build(self):
        self.nav = DirectFrame(
            parent=self.base.a2dTopLeft,
            frameColor=(0, 0, 0, 0.5),
            frameSize=(0, 0.6, -0.9, 0),
            pos=(0.1, 0, -0.1),
        )

        for i, lm in enumerate(self.landmarks):
            button = DirectButton(
                parent=self.nav,
                text=lm["title"],
                text_font=self.font,
                scale=0.06,
                pos=(0.3, 0, -0.1 - i * 0.12),
                command=self.on_pick,
                extraArgs=[lm["name"]],
            )
            self.buttons.append((button, lm["body"]))

        self.back_button = DirectButton(
            parent=self.nav,
            text="До огляду планети",
            text_font=self.font,
            scale=0.06,
            pos=(0.3, 0, -0.8),
            command=self.on_back,
        )
        self.back_button.hide()

        self.card_title = OnscreenText(
            parent=self.base.a2dBottomRight,
            text="",
            font=self.font,
            pos=(-0.1, 0.4),
            scale=0.07,
            fg=(1, 0.9, 0.5, 1),
            align=TextNode.ARight,
        )
        self.card_text = OnscreenText(
            parent=self.base.a2dBottomRight,
            text="",
            font=self.font,
            pos=(-0.1, 0.28),
            scale=0.05,
            fg=(1, 1, 1, 1),
            align=TextNode.ARight,
            wordwrap=28,
        )
        self.card_title.hide()
        self.card_text.hide()

    def show(self):
        self.nav.show()

    def hide(self):
        self.nav.hide()
        self.hide_inspect()

    def show_for(self, body_name):
        for button, lm_body in self.buttons:
            if lm_body == body_name:
                button.show()
            else:
                button.hide()

    def show_inspect(self, title, text):
        self.card_title["text"] = title
        self.card_text["text"] = text
        self.card_title.show()
        self.card_text.show()
        self.back_button.show()

    def hide_inspect(self):
        self.card_title.hide()
        self.card_text.hide()
        self.back_button.hide()