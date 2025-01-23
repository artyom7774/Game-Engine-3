from engine.ui.text import Label, TextField

from engine.classes.sprite import Sprite

from engine.classes.hitbox import SquareHitbox

from engine.vector.float import Vec4f
from engine.vector.int import Vec3i, Vec4i

from engine.functions.alpha import alphaRect

import typing
import pygame


class Button:
    def __init__(
            self, game,
            base: typing.Union[Sprite, Vec3i, typing.List[int]],
            mouse: typing.Union[Sprite, Vec3i, typing.List[int]],
            click: typing.Union[Sprite, Vec3i, typing.List[int]],

            rect: typing.Union[Vec4f, SquareHitbox, typing.List[float]],

            text: typing.Union[typing.Callable, Label, TextField] = None,

            frame: typing.Union[Sprite, Vec3i, typing.List[int]] = None,

            function: typing.Callable = None
    ) -> None:
        self.game = game

        self.base = (Vec4i(*base) if len(base) == 4 else Vec4i(*base, 255)) if type(base) == tuple or type(base) == list else base
        self.mouse = (Vec4i(*mouse) if len(mouse) == 4 else Vec4i(*mouse, 255)) if type(mouse) == tuple or type(mouse) == list else mouse
        self.click = (Vec4i(*click) if len(click) == 4 else Vec4i(*click, 255)) if type(click) == tuple or type(click) == list else click

        self.frame = ((Vec4i(*frame) if len(frame) == 4 else Vec4i(*frame, 255)) if type(frame) == tuple or type(frame) == list else frame) if frame is not None else None

        self.active = None

        self.rect = rect if type(rect) == SquareHitbox else SquareHitbox(rect)

        self.text = text if text is not None else Label(game, 0, 0, 0, 0, "")

        self.function = function

    def update(self) -> None:
        pass

    def draw(self, x: int = None, y: int = None) -> None:
        if x is None:
            x = self.rect.x

        if y is None:
            y = self.rect.y

        if x < self.game.mouse[0] < x + self.rect.width:
            if y < self.game.mouse[1] < y + self.rect.height:
                if self.game.click[0]:
                    if self.function is not None:
                        self.function()

                elif pygame.mouse.get_pressed()[0]:
                    self.active = self.click

                else:
                    self.active = self.mouse

            else:
                self.active = self.base

        else:
            self.active = self.base

        if type(self.active) == Sprite:
            self.game.screen.blit(self.active.get(), (x, y))

        else:
            alphaRect(self.game.screen, self.active, SquareHitbox([x, y, self.rect.width, self.rect.height]))

        if self.frame is not None:
            alphaRect(self.game.screen, self.frame, self.rect, 1)

        if type(self.text) == Label or type(self.text) == TextField:
            self.text.draw(x, y)

        else:
            self.text()
