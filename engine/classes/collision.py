from engine.classes.hitbox import SquareHitbox, CircleHitbox

from engine.functions.loads import loadCollisionFile
from engine.functions.cache import cache

import pygame
import math


class Collision:
    @staticmethod
    def any(hitbox1, hitbox2) -> bool:
        if isinstance(hitbox2, SquareHitbox):
            hitbox2, hitbox1 = hitbox1, hitbox2

        if isinstance(hitbox1, SquareHitbox) and isinstance(hitbox2, SquareHitbox):
            return Collision.rectByRect(*hitbox1.get(), *hitbox2.get())

        if isinstance(hitbox1, SquareHitbox) and isinstance(hitbox2, CircleHitbox):
            return Collision.rectByCircle(*hitbox1.get(), *hitbox2.get())

        if isinstance(hitbox1, CircleHitbox) and isinstance(hitbox2, CircleHitbox):
            return Collision.circleByCircle(*hitbox1.get(), *hitbox2.get())

        raise TypeError(f"ERROR: {hitbox1=} {hitbox2=}")

    @staticmethod
    def rectByRect(x1: float, y1: float, w1: float, h1: float, x2: float, y2: float, w2: float, h2: float) -> bool:
        return pygame.Rect(x1, y1, w1, h1).colliderect(pygame.Rect(x2, y2, w2, h2))

    @staticmethod
    def circleByCircle(x1: float, y1: float, r1: float, x2: float, y2: float, r2: float) -> bool:
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) <= r1 + r2 - 1

    @staticmethod
    def rectByCircle(x1: float, y1: float, w1: float, h1: float, x2: float, y2: float, r2: float) -> bool:
        return math.sqrt((x2 - max(x1, min(x2, x1 + w1))) ** 2 + (y2 - max(y1, min(y2, y1 + h1))) ** 2) <= r2 - 1

    @cache
    def get(self, group: str) -> dict:
        out = {}

        if "Any" in self.collision:
            for key, value in self.collision["Any"].items():
                out[key] = value

        if group in self.collision:
            for key, value in self.collision[group].items():
                out[key] = value

        return out

    def __init__(self, path: str = "") -> None:
        if path == "":
            self.collision = {}

        else:
            self.collision = loadCollisionFile(path)
