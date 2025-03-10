from engine.functions.loads import loadCollisionFile

from engine.functions.cache import cache

import pygame


class Collision:
    @staticmethod
    def rect(x1: float, y1: float, w1: float, h1: float, x2: float, y2: float, w2: float, h2: float) -> bool:
        return pygame.Rect(x1, y1, w1, h1).colliderect(pygame.Rect(x2, y2, w2, h2))

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
