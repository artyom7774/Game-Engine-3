from engine.classes.hitbox import SquareHitbox
from engine.vector.int import Vec4i

from engine.variables import *


class Layout:
    def __init__(
            self, game, rect: typing.Union[Vec4i, SquareHitbox, typing.List[int]],
            objects: VGUIObject
    ):
        self.game = game

        self.rect = rect if type(rect) == SquareHitbox else SquareHitbox(rect)

        self.objects = objects

    def update(self):
        for obj in self.objects:
            obj.update()

    def draw(self, x: float = None, y: float = None):
        if x is None:
            x = self.rect.x

        if y is None:
            y = self.rect.y

        for obj in self.objects:
            obj.update()
            obj.draw(x + obj.rect.x, y + obj.rect.y)
