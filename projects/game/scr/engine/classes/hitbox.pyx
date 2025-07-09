from engine.vector.float import Vec4f
from engine.vector.int import Vec4i

import pygame
import typing


cdef class SquareHitbox:
    cdef public int x, y, width, height

    def __init__(self, hitbox: Union[list, tuple, Vec4f, Vec4i]) -> None:
        if not isinstance(hitbox, (list, tuple)):
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

    def get(self) -> list:
        return [int(self.x), int(self.y), int(self.width), int(self.height)]

    def copy(self) -> "SquareHitbox":
        return SquareHitbox(self.get())
