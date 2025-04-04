from engine.classes.sprite import Sprite

from engine.functions.loads import loadAnimationFile

from engine.vector.float import Vec2f

from engine.variables import *

import typing
import pygame

RIGHT = "1 0"
LEFT = "-1 0"
UP = "0 -1"
DOWN = "0 1"

RIGHT_UP = "1 -1"
RIGHT_DOWN = "1 1"
LEFT_UP = "-1 -1"
LEFT_DOWN = "-1 1"

NULL = "0 0"


class Animation:
    def __init__(self, game, path: str, animations: typing.Dict[str, typing.List[str]], canWasMirrored: bool = True) -> None:
        self.game = game

        self.focus, self.settings = loadAnimationFile(path)
        self.animations = animations

        self.width = 0
        self.height = 0

        self.pos = Vec2f(0, 0)

        self.canWasMirrored = canWasMirrored
        self.wasMirrored = False

        self.init()

    def init(self) -> None:
        for key, value in self.animations.items():
            for i, element in enumerate(value):
                self.animations[key][i] = Sprite(self.game, element)

                self.width = max(self.width, self.animations[key][i].width)
                self.height = max(self.height, self.animations[key][i].height)

    def get(self, obj: "VObject") -> pygame.sprite.Sprite:
        pos = obj.getVectorsPower()

        direction = [
            0 if pos.x == 0 else (1 if pos.x > 0 else -1),
            0 if pos.y == 0 else (1 if pos.y > 0 else -1)
        ]

        if abs(pos.x) > FLOAT_PRECISION and self.canWasMirrored:
            if pos.x > FLOAT_PRECISION:
                self.wasMirrored = False

            if pos.x < FLOAT_PRECISION:
                self.wasMirrored = True

        else:
            pass

        direction = " ".join(list(map(str, direction)))

        for element in self.settings:
            if eval(element[0]):
                animation = element[1].replace("animation(", "").replace(")", "")
                break

        else:
            animation = "idle"

        return pygame.transform.flip(
            self.animations[animation][(self.game.fpsc // (self.game.fps // len(self.animations[animation]))) % len(self.animations[animation])].get(),
            self.wasMirrored if obj.id == self.game.focus or self.focus else False, False
        )
