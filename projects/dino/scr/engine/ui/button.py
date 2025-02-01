from engine.ui.text import Label, center_print_text

from engine.classes.texture import Texture
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

        rect: typing.Union[Vec4f, SquareHitbox, typing.List[float]],

        base: typing.Union[typing.List[typing.Union[Texture, Sprite]], Texture, Sprite, typing.List[int], Vec3i, Vec4i],
        mouse: typing.Union[typing.List[typing.Union[Texture, Sprite]], Texture, Sprite, typing.List[int], Vec3i, Vec4i],
        click: typing.Union[typing.List[typing.Union[Texture, Sprite]], Texture, Sprite, typing.List[int], Vec3i, Vec4i],

        frame: typing.Union[Sprite, typing.List[int], Vec3i, Vec4i] = None,

        text: Label = None,

        function: typing.Callable = None
    ) -> None:
        self.game = game

        self.rect = rect if type(rect) == SquareHitbox else SquareHitbox(rect)

        if (type(base) == list and type(base[0]) == int) or type(base) in (Vec3i, Vec4i):
            self.base = Vec4i(*base)

        else:
            self.base = base if type(base) == list else [base]

            for i, element in enumerate(self.base):
                if type(element) == Texture:
                    self.base[i] = element.sprite(self.rect.width, self.rect.height)

        if (type(mouse) == list and type(mouse[0]) == int) or type(mouse) in (Vec3i, Vec4i):
            self.mouse = Vec4i(*mouse)

        else:
            self.mouse = mouse if type(mouse) == list else [mouse]

            for i, element in enumerate(self.mouse):
                if type(element) == Texture:
                    self.mouse[i] = element.sprite(self.rect.width, self.rect.height)

        if (type(click) == list and type(click[0]) == int) or type(click) in (Vec3i, Vec4i):
            self.click = Vec4i(*click)

        else:
            self.click = click if type(click) == list else [click]

            for i, element in enumerate(self.click):
                if type(element) == Texture:
                    self.click[i] = element.sprite(self.rect.width, self.rect.height)

        self.frame = (Vec4i(*frame) if type(frame) != Sprite else frame) if frame is not None else frame

        self.text = text if text is not None else Label(game, 0, 0, 0, 0, "")

        self.active = None

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

        pygame.draw.rect(self.game.screen, (255, 0, 0), [x, y, self.rect.width, self.rect.height])

        if type(self.active[0]) == Sprite:
            for element in self.active:
                self.game.screen.blit(element.get(), (x, y))

        else:
            alphaRect(self.game.screen, self.active, SquareHitbox([x, y, self.rect.width, self.rect.height]))

        if self.frame is not None:
            alphaRect(self.game.screen, self.frame, self.rect, 1)

        if self.text is not None:
            self.text.draw(x, y)
