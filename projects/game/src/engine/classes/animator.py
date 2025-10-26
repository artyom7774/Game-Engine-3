from engine.classes.sprite import Sprite
from engine.variables import *
import typing


class Animator:
    def __init__(self, game, obj: "VObject", data: typing.Dict[str, typing.Any]) -> None:
        self.game = game
        self.obj = obj

        self.groups = {}

        self.horizontal = False
        self.vertical = False

        self.standardSprite = None
        self.standardGroup = None

        self.data = data

        self.animation = None

    def init(self):
        self.standardSprite = self.obj.sprite.copy() if self.obj.sprite is not None else None
        self.standardGroup = None

        for name, group in self.data["groups"].items():
            self.groups[name] = {
                "settings": group["settings"],
                "sprites": group["sprites"],

                "nowSprite": 0,
                "fpsc": 0
            }
            self.groups[name]["settings"]["fpsPerFrame"] = int(self.groups[name]["settings"]["fpsPerFrame"])

            if group["settings"]["standard"]:
                self.standardGroup = name

        self.animation = self.standardGroup

        self.updateSpriteAnimation()

    def updateSpriteAnimation(self):
        if self.animation is None:
            return

        group = self.groups[self.animation]

        data = group["sprites"][group["nowSprite"]]

        self.obj.sprite = Sprite(self.game, self.obj, data, *self.obj.sprite.pos.get(), *self.obj.sprite.size.get())

        self.obj.sprite.flip(self.horizontal, self.vertical)

    def setAnimation(self, value, forcibly: bool = False):
        if self.animation == value and not forcibly:
            return

        self.animation = value

        if self.animation is not None:
            self.groups[self.animation]["nowSprite"] = 0
            self.groups[self.animation]["fpsc"] = 0

            self.updateSpriteAnimation()

        else:
            self.obj.sprite = self.standardSprite.copy() if self.standardSprite is not None else None

            if self.obj.sprite is not None:
                self.obj.sprite.flip(self.horizontal, self.vertical)

    def runAnimation(self, animation):
        self.setAnimation(animation)

    def flipAnimation(self, horizontal, vertical):
        if self.horizontal == horizontal and self.vertical == vertical:
            return

        self.horizontal = horizontal
        self.vertical = vertical

        self.setAnimation(self.animation, forcibly=True)

    def stopAnimation(self):
        self.setAnimation(self.standardGroup)

    def update(self) -> None:
        if self.animation is None:
            if self.obj.sprite != self.standardSprite:
                self.obj.sprite = self.standardSprite.copy() if self.standardSprite is not None else None

                if self.obj.sprite is not None:
                    self.obj.sprite.flip(self.horizontal, self.vertical)

            return

        group = self.groups[self.animation]
        group["fpsc"] += 1

        if group["fpsc"] >= group["settings"]["fpsPerFrame"]:
            max_sprite = len(group["sprites"]) - 1

            if group["nowSprite"] < max_sprite:
                group["nowSprite"] += 1

            elif group["settings"]["repeat"]:
                group["nowSprite"] = 0

            else:
                pass

            self.updateSpriteAnimation()

            group["fpsc"] = 0
