from engine.functions.loads import loadCollisionFile

from engine.functions.cache import cache

import pygame


class Collision:
    @staticmethod
    def rect(x1: float, y1: float, w1: float, h1: float, x2: float, y2: float, w2: float, h2: float) -> bool:
        return max(x1, x1 + w1) > min(x2, x2 + w2) and max(x2, x2 + w2) > min(x1, x1 + w1) and max(y1, y1 + h1) > min(y2, y2 + h2) and max(y2, y2 + h2) > min(y1, y1 + h1)

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
