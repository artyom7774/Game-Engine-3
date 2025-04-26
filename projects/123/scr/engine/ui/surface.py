from engine.classes.hitbox import SquareHitbox

from engine.vector.float import Vec4f
from engine.vector.int import Vec3i, Vec4i

from engine.functions.alpha import alphaRect

import typing


class Surface:
    def __init__(
        self, game,
        rect: typing.Union[SquareHitbox, Vec4f, typing.List[int]],
        color: typing.Union[Vec3i, Vec4i, typing.List[int]]
    ):
        self.game = game

        self.rect = rect if type(rect) == SquareHitbox else SquareHitbox(rect)
        self.color = Vec4i(*color, 100) if type(color) == Vec3i else (Vec4i(*color) if type(color) == list else color)

    def draw(self):
        alphaRect(self.game.screen, self.color, self.rect)
