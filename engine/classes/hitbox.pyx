from engine.vector.float import Vec4f
from engine.vector.int import Vec4i

import typing

cdef class SquareHitbox:
    cdef public int x, y, width, height

    def __init__(self, hitbox: Union[list, tuple, Vec4f, Vec4i]):
        if isinstance(hitbox, (list, tuple)):
            pass

        else:
            hitbox = hitbox.get()

        self.x = int(hitbox[0])
        self.y = int(hitbox[1])
        self.width = int(hitbox[2])
        self.height = int(hitbox[3])

    def __str__(self) -> str:
        return f"SquareHitbox({self.x}, {self.y}, {self.width}, {self.height})"

    def __repr__(self) -> str:
        return f"SquareHitbox({self.x}, {self.y}, {self.width}, {self.height})"

    def __getattr__(self, name):
        if name == "x":
            return int(self.x)

        elif name == "y":
            return int(self.y)

        if name == "width":
            return int(self.width)

        elif name == "height":
            return int(self.height)

        else:
            return super().__getattr__(name)

    def contains(self, obj: "SquareHitbox") -> bool:
        return self.x <= obj.x < self.x + self.width and self.y <= obj.y < self.y + self.height

    def get(self) -> list:
        return [int(self.x), int(self.y), int(self.width), int(self.height)]

    def copy(self) -> "SquareHitbox":
        return SquareHitbox(self.get())
