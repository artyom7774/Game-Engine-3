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
            self.groups[name] = {"sprites": group["sprites"], "settings": group["settings"], "fpsc": 1, "nowSprite": 0}

            self.groups[name]["settings"]["fpsPerFrame"] = int(self.groups[name]["settings"]["fpsPerFrame"])

            if group["settings"]["standard"]:
                self.standardGroup = name

        self.animation = self.standardGroup

    def setAnimation(self, value):
        if self.animation != value and self.animation is not None:
            self.groups[self.animation]["nowSprite"] = 0
            self.groups[self.animation]["fpsc"] = 1

        self.animation = value

    def runAnimation(self, animation):
        self.setAnimation(animation)

    def flipAnimation(self, horizontal, vertical):
        self.horizontal = horizontal
        self.vertical = vertical

    def stopAnimation(self):
        self.setAnimation(self.standardGroup)

    def update(self) -> None:
        if self.animation is not None:
            group = self.groups[self.animation]

            group["fpsc"] += 1

            if group["fpsc"] >= group["settings"]["fpsPerFrame"]:
                if group["settings"]["repeat"]:
                    group["nowSprite"] = (group["nowSprite"] + 1) % len(group["sprites"])

                elif (group["nowSprite"] + 1) % len(group["sprites"]) <= group["nowSprite"]:
                    pass

                else:
                    group["nowSprite"] += 1

                self.obj.sprite = Sprite(self.game, self.obj, group["sprites"][group["nowSprite"]], *self.obj.sprite.pos.get(), *self.obj.sprite.size.get())

                self.obj.sprite.flip(self.horizontal, self.vertical)

                group["fpsc"] = 1

        else:
            self.obj.sprite = self.standardSprite.copy() if self.standardSprite is not None else self.standardSprite

            self.obj.sprite.flip(self.horizontal, self.vertical)
