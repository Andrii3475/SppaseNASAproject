"""3D-огляд апаратів. Тур ховається, моделі обертаються мишею і наближаються колесом."""

import os
from math import cos, radians, sin

from direct.gui.DirectGui import DirectButton, OnscreenText
from panda3d.core import AmbientLight, DirectionalLight, MouseButton, TextNode, Vec3

from fonts import get_font

SHOWCASE_DATA = [
    {
        "name": "InSight Cruise Lander",
        "title": "InSight Cruise Lander",
        "model": "assets/models/InSight Cruise Lander (arm deployed).obj",
        "text": "InSight — перша місія NASA, спеціально створена для глибокого дослідження внутрішньої будови Марса. "+
"Космічний апарат InSight здійснив посадку на Марс 26 листопада 2018 року. Його головним завданням було дослідження внутрішніх шарів планети: кори, мантії та ядра."+
"На відміну від марсоходів, які досліджують поверхню, InSight зосередився на процесах, що відбуваються під нею. За допомогою високочутливого сейсмометра SEIS апарат реєстрував марсотруси, а спеціальний тепловий зонд HP³ був призначений для вимірювання теплового потоку з надр планети."+
"Роботизована рука довжиною приблизно 1,8 метра допомагала розміщувати наукові прилади безпосередньо на поверхні Марса."+
"Отримані результати дали вченим нові знання про внутрішню структуру Червоної планети та процеси формування кам'янистих планет Сонячної системи."+
"Місія завершилася 15 грудня 2022 року, залишивши після себе цінний масив наукових даних."
    },
    {
        "name": "Mars Exploration Rover",
        "title": "Mars Exploration Rover",
        "model": "assets/models/Mars Exploration Rover - Spirit and Opportunity.obj",
        "text": "Spirit та Opportunity — роботизовані геологи, які змінили уявлення людства про минуле Марса."
+"У 2004 році NASA відправило на Червону планету два автономні дослідницькі ровери — Spirit та Opportunity. Їхньою головною метою було вивчення марсіанських порід і ґрунту, а також пошук геологічних доказів існування води в минулому."
+"За допомогою наукових камер, спектрометрів та інших дослідницьких приладів апарати аналізували склад мінералів, досліджували поверхню та передавали отримані дані на Землю."
+"Їхні відкриття підтвердили, що в далекому минулому на Марсі існували умови, пов'язані з рідкою водою. Spirit пропрацював до 2010 року, а Opportunity продовжував дослідження майже 15 років, подолавши близько 45 кілометрів."
+"Ці місії стали важливим кроком у дослідженні геологічної історії Марса та пошуку середовищ, які могли бути придатними для життя.",
    },
    {
        "name": "voyager1",
        "title": "Voyager 1",
        "model": "assets/models/voyager1.obj",
        "text": "Voyager 1 — один із найвидатніших космічних апаратів в історії людства, який відкрив новий етап дослідження Всесвіту." +
"Запущений NASA 5 вересня 1977 року, Voyager 1 спочатку був призначений для дослідження зовнішніх планет Сонячної системи, зокрема Юпітера та Сатурна." +
"Під час своєї подорожі апарат передав на Землю унікальні зображення планет, їхніх супутників і кілець, а також зібрав важливі дані про магнітні поля та космічне середовище." +
"У серпні 2012 року Voyager 1 став першим створеним людиною космічним апаратом, який перетнув геліопаузу та увійшов у міжзоряний простір." +
"Особливою частиною місії є «Золотий диск» — спеціальне послання позаземним цивілізаціям. На ньому записані звуки Землі, музика, привітання різними мовами та зображення, що представляють життя й культуру людства." +
"Voyager 1 продовжує свою подорож за межами геліосфери, передаючи наукові дані та символізуючи прагнення людства досліджувати невідоме.",
    },
]


class ShowcaseViewer:
    def __init__(self, base, on_close):
        self.base = base
        self.on_close = on_close
        self.font = get_font(base)
        self.active = False
        self.current = None
        self.yaw = 0.0
        self.pitch = 15.0
        self.distance = 6.0
        self.last_mouse = None
        self.pivots = {}
        self.buttons = []

        self.root = base.render.attachNewNode("showcase")
        self.root.hide()
        self._build_lights()
        self._load_models()
        self._build_ui()

        base.accept("wheel_up", self._zoom, [-0.5])
        base.accept("wheel_down", self._zoom, [0.5])
        base.taskMgr.add(self._update, "showcase-update")

    def _build_lights(self):
        sun = DirectionalLight("showcase_sun")
        sun.setColor((0.9, 0.9, 0.85, 1.0))
        sun_np = self.root.attachNewNode(sun)
        sun_np.setHpr(30, -40, 0)
        self.root.setLight(sun_np)

        amb = AmbientLight("showcase_amb")
        amb.setColor((0.25, 0.25, 0.3, 1.0))
        self.root.setLight(self.root.attachNewNode(amb))

        self.root.setShaderAuto()

    def _load_models(self):
        for data in SHOWCASE_DATA:
            if not os.path.exists(data["model"]):
                print(f"Model not found: {data['model']}")
                continue

            pivot = self.root.attachNewNode(data["name"])
            model = self.base.loader.loadModel(data["model"])
            model.reparentTo(pivot)

            bounds = model.getTightBounds()
            if not bounds:
                print(f"Empty model: {data['model']}")
                continue

            mins, maxs = bounds
            center = (mins + maxs) * 0.5
            size = max(maxs.x - mins.x, maxs.y - mins.y, maxs.z - mins.z)
            scale = 2.0 / size if size > 0 else 1.0

            model.setScale(scale)
            model.setPos(-(center * scale))

            pivot.hide()
            self.pivots[data["name"]] = pivot

    def _build_ui(self):
        for i, data in enumerate(SHOWCASE_DATA):
            btn = DirectButton(
                parent=self.base.a2dTopLeft,
                text=data["title"],
                text_font=self.font,
                scale=0.06,
                pos=(0.3, 0, -0.2 - i * 0.12),
                command=self.select,
                extraArgs=[data["name"]],
            )
            self.buttons.append(btn)

        self.back_button = DirectButton(
            parent=self.base.a2dTopLeft,
            text="Назад до туру",
            text_font=self.font,
            scale=0.06,
            pos=(0.3, 0, -0.2 - len(SHOWCASE_DATA) * 0.12),
            command=self.close,
        )

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
        self._set_ui_visible(False)

    def _set_ui_visible(self, visible):
        for widget in self.buttons + [self.back_button, self.card_title, self.card_text]:
            if visible:
                widget.show()
            else:
                widget.hide()

    def open(self):
        self.active = True
        self.root.show()
        self._set_ui_visible(True)
        self.select(SHOWCASE_DATA[0]["name"])

    def close(self):
        self.active = False
        self.current = None
        self.root.hide()
        self._set_ui_visible(False)
        self.on_close()

    def select(self, name):
        if name not in self.pivots:
            return

        for key, pivot in self.pivots.items():
            if key == name:
                pivot.show()
            else:
                pivot.hide()

        self.current = name
        self.yaw = 0.0
        self.pitch = 15.0
        self.distance = 6.0

        data = next(d for d in SHOWCASE_DATA if d["name"] == name)
        self.card_title["text"] = data["title"]
        self.card_text["text"] = data["text"]

    def _zoom(self, delta):
        if self.active:
            self.distance = max(2.0, min(15.0, self.distance + delta))

    def _update(self, task):
        if not self.active or self.current is None:
            return task.cont

        pointer = self.base.win.getPointer(0)
        x, y = pointer.getX(), pointer.getY()
        if self.base.mouseWatcherNode.isButtonDown(MouseButton.one()) and self.last_mouse:
            dx = x - self.last_mouse[0]
            dy = y - self.last_mouse[1]
            self.yaw += dx * 0.3
            self.pitch = max(-80.0, min(80.0, self.pitch + dy * 0.3))
        self.last_mouse = (x, y)

        yaw = radians(self.yaw)
        pitch = radians(self.pitch)
        self.base.camera.setPos(
            self.distance * cos(pitch) * sin(yaw),
            -self.distance * cos(pitch) * cos(yaw),
            self.distance * sin(pitch),
        )
        self.base.camera.lookAt(Vec3(0, 0, 0))
        return task.cont