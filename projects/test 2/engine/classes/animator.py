from engine.variables import *

import typing


class Animator:
    def __init__(self, game, obj: "VObject") -> None:
        self.game = game

        self.obj = obj

    def update(self) -> None:
        pass
