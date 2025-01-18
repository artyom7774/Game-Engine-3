from engine.vector.float import Vec4f
from engine.vector.int import Vec4i

import typing


class SquareHitbox:
    def __init__(self, hitbox: typing.Union[typing.List[float], Vec4f, Vec4i]) -> None:
        hitbox = hitbox if type(hitbox) in (list, tuple) else hitbox.get()

        self.x = float(hitbox[0])
        self.y = float(hitbox[1])

        self.width = float(hitbox[2])
        self.height = float(hitbox[3])

    def __str__(self) -> str:
        return "SquareHitbox(" + ", ".join(list(map(str, [self.x, self.y, self.width, self.height]))) + ")"

    def __repr__(self) -> str:
        return "SquareHitbox(" + ", ".join(list(map(str, [self.x, self.y, self.width, self.height]))) + ")"

    def contains(self, obj: "SquareHitbox") -> bool:
        return self.x <= obj.pos.x < self.x + self.width and self.y <= obj.pos.y < self.y + self.height

    def get(self) -> typing.List[float]:
        return [self.x, self.y, self.width, self.height]

    def copy(self) -> "SquareHitbox":
        return SquareHitbox(self.get())
