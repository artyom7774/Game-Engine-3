from engine.vector.float import Vec2f

from engine.variables import *

import math


class StaticCamera:
    def __init__(self, game, x: float, y: float) -> None:
        self.game = game

        self.pos = Vec2f(x, y)

    def __str__(self) -> None:
        return f"StaticCamera(pos = {self.pos})"

    def update(self, x: float = None, y: float = None) -> None:
        self.pos.x = x if x is not None else self.pos.x
        self.pos.y = y if y is not None else self.pos.y

    def get(self) -> Vec2f:
        return self.pos

    def x(self) -> float:
        return -self.pos.x

    def y(self) -> float:
        return self.pos.y


class FocusCamera(StaticCamera):
    def __init__(self, game, obj: VObject) -> None:
        StaticCamera.__init__(self, game, 0, 0)

        self.obj = obj

        self.update()

    def __str__(self):
        return f"FocusCamera(object = {self.obj})"

    def setFocus(self, obj: VObject):
        self.obj = obj

        self.update()

    def update(self, *args, **kwargs) -> None:
        # print(self)

        hitbox = self.obj.hitbox.rect()

        super().update(
            self.obj.pos.x + hitbox.x + hitbox.width // 2 - self.game.usingWidth // 2,
            -(self.obj.pos.y + hitbox.y + hitbox.height // 2 - self.game.usingHeight // 2)
        )

    def get(self) -> VObject:
        return self.obj


class SmoothingCamera(FocusCamera):
    pass
