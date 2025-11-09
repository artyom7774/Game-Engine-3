from engine.vector.float import Vec4f, Vec3f
from engine.vector.int import Vec4i, Vec3i

import pygame
import typing


cdef class SquareHitbox:
    __slots__ = ("x", "y", "width", "height")

    cdef public int x
    cdef public int y
    cdef public int width
    cdef public int height

    def __init__(self, hitbox: Union[list, tuple, Vec4i, Vec4f]) -> None:
        if isinstance(hitbox, (Vec4i, Vec4f)):
            hitbox = hitbox.get()

        self.x = int(hitbox[0])
        self.y = int(hitbox[1])
        self.width = int(hitbox[2])
        self.height = int(hitbox[3])

    def __str__(self) -> str:
        return f"SquareHitbox({self.x}, {self.y}, {self.width}, {self.height})"

    def __repr__(self) -> str:
        return f"SquareHitbox({self.x}, {self.y}, {self.width}, {self.height})"

    def draw(self, screen: typing.Any, x: float, y: float, px: float, py: float) -> None:
        pygame.draw.rect(screen, (255, 0, 0), (x + self.x + px, y + self.y + py, self.width, self.height), 1)

    def get(self) -> typing.List[int]:
        return [int(self.x), int(self.y), int(self.width), int(self.height)]

    def position(self, x: float, y: float, prec: float = 0) -> "SquareHitbox":
        return SquareHitbox([self.x + x - prec, self.y + y - prec, self.width + 2 * prec, self.height + 2 * prec])

    def copy(self) -> "SquareHitbox":
        return SquareHitbox(self.get())

    def rect(self) -> "SquareHitbox":
        return self


cdef class CircleHitbox:
    __slots__ = ("x", "y", "radius")

    cdef public int x
    cdef public int y
    cdef public int radius

    def __init__(self, hitbox: Union[list, tuple, Vec3f, Vec3i]) -> None:
        if not isinstance(hitbox, (list, tuple)):
            hitbox = hitbox.get()

        self.x = int(hitbox[0])
        self.y = int(hitbox[1])

        self.radius = int(hitbox[2])

    def __str__(self) -> str:
        return f"CircleHitbox({self.x}, {self.y}, {self.radius})"

    def __repr__(self) -> str:
        return f"CircleHitbox({self.x}, {self.y}, {self.radius})"

    def draw(self, screen: typing.Any, x: float, y: float, px: float, py: float) -> None:
        pygame.draw.circle(screen, (255, 0, 0), (x + self.x + px, y + self.y + py), self.radius, 1)

    def get(self) -> typing.List[int]:
        return [int(self.x), int(self.y), int(self.radius)]

    def position(self, x: float, y: float, prec: float = 0) -> "CircleHitbox":
        return CircleHitbox([self.x + x, self.y + y, self.radius + prec])

    def copy(self) -> "CircleHitbox":
        return CircleHitbox(self.get())

    def rect(self) -> "SquareHitbox":
        return SquareHitbox([self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius])
