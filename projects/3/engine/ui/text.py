from engine.classes.hitbox import SquareHitbox
from engine.vector.int import Vec4i

from engine.functions.cache import cache

from PIL.ImageFont import FreeTypeFont
from PIL import ImageFont

import typing
import pygame
import os

BASE_FONT = "engine/fonts/arial.ttf"
BASE_FONT_COLOR = (255, 255, 255)


@cache
def find_system_font(name: str) -> str:
    return pygame.font.match_font(name)


@cache
def get_font(font_type: str, font_size: int) -> pygame.font.Font:
    if os.path.exists(font_type):
        return pygame.font.Font(font_type, font_size)

    return pygame.font.SysFont(font_type, font_size)


@cache
def get_ttf(font_type: str, font_size: int) -> FreeTypeFont:
    if os.path.exists(font_type):
        return ImageFont.truetype(font_type, font_size)

    if find_system_font(font_type.lower()) is not None:
        ImageFont.truetype(find_system_font(font_type.lower()), font_size)

    print(f"WARNING: {font_type} is not found")

    return ImageFont.load_default()


def print_text(
        screen, x: float, y: float, message: str, font_size: int = 20,
        font_type: str = BASE_FONT, font_color: typing.Tuple[int] = (255, 255, 255), alpha: int = 255
) -> None:
    font = get_font(font_type, font_size)
    text = font.render(message, True, font_color)
    text.set_alpha(alpha)

    screen.blit(text, (x, y))


def center_print_text(
        screen, rect: SquareHitbox, message: str, font_size: int = 20,
        font_type: str = BASE_FONT, font_color: typing.Tuple[int] = (0, 0, 0), alpha: int = 255
) -> None:
    ttf = get_ttf(font_type, font_size)

    tx = rect.width / 2 - ttf.getbbox(message)[2] / 2
    ty = rect.height / 2 - ttf.getbbox(message + "AgАр")[3] / 2

    print_text(screen, rect.x + tx, rect.y + ty, message, font_size, font_type, font_color, alpha)


class Label:
    def __init__(
            self, game, rect: typing.Union[Vec4i, SquareHitbox, typing.List[float]], text: str, font_size: int = 20,
            font_type: str = BASE_FONT, font_color: typing.Tuple[int] = BASE_FONT_COLOR, 
            horizontal: str = "center", vertical: str = "center", alpha: int = 255,
    ) -> None:
        self.game = game

        self.rect = rect if type(rect) == SquareHitbox else SquareHitbox(rect)

        self.text = text

        self.alpha = alpha

        self.font_size = font_size
        self.font_color = font_color
        self.font_type = font_type

        self.horizontal = horizontal
        self.vertical = vertical

        self.ttf = None

        self.tx = 0
        self.ty = 0

        self.ttf = get_ttf(self.font_type, self.font_size)

        self.hstep = self.ttf.getbbox("Ag")[3]

    def update(self) -> None:
        pass

    def draw(self, x: int = None, y: int = None) -> None:
        if x is None:
            x = self.rect.x

        if y is None:
            y = self.rect.y

        if self.horizontal == "center":
            self.tx = self.rect.width / 2 - self.ttf.getbbox(self.text)[2] / 2

        elif self.horizontal == "left":
            self.tx = 4

        elif self.horizontal == "right":
            self.tx = self.rect.width - self.ttf.getbbox(self.text)[2] - 4

        else:
            raise NameError(f"type {self.horizontal} is not difined")
        
        if self.vertical == "center":
            py = (self.rect.height - self.hstep) / 2

        elif self.vertical == "up":
            py = 2

        elif self.vertical == "down":
            py = self.rect.height - self.hstep - 2

        else:
            raise NameError(f"horizontal {self.horizontal} is not difined")

        self.ty = self.rect.height / 2 - self.ttf.getbbox(self.text + "AgАр")[3] / 2

        print_text(self.game.screen, x + self.tx, y + py, self.text, self.font_size, self.font_type, self.font_color, self.alpha)


class TextField:
    def __init__(
            self, game, rect: typing.Union[Vec4i, SquareHitbox, typing.List[int]], text: str, font_size: int = 20,
            font_type: str = BASE_FONT, font_color: typing.Tuple[int] = BASE_FONT_COLOR,
            horizontal: str = "center", vertical: str = "center", alpha: int = 255
    ) -> None:
        self.game = game

        self.rect = rect if type(rect) == SquareHitbox else SquareHitbox(rect)

        self.ax = 0
        self.ay = 0

        self.text = text

        self.font_size = font_size
        self.font_type = font_type
        self.font_color = font_color

        self.horizontal = horizontal
        self.vertical = vertical

        self.alpha = alpha

        self.ttf = get_ttf(self.font_type, self.font_size)

        self.text = self.text.split()

        self.out = []

        self.hstep = self.ttf.getbbox("Ag")[3]
        self.wstep = 0

        while self.ttf.getbbox((self.wstep + 1) * "_")[2] < self.rect.width:
            self.wstep += 1

        self.init()

    def init(self) -> None:
        l = 0
        r = len(self.text) - 1

        if self.text[0] == "/t":
            self.out = [" " * 3]

        else:
            self.out = [self.text[0]]

        while l < r:
            if len(self.out[len(self.out) - 1]) + len(self.text[l + 1]) + 1 < self.wstep:
                if self.text[l + 1] == "/n":
                    self.out.append("")

                elif self.text[l + 1] == "/t":
                    self.out[len(self.out) - 1] += " " * 4

                elif len(self.out[len(self.out) - 1]) == 0:
                    self.out[len(self.out) - 1] += f"{self.text[l + 1]}"

                else:
                    self.out[len(self.out) - 1] += f" {self.text[l + 1]}"

                l += 1

            else:
                self.out.append("")

        self.ay = self.rect.height / 2 - (self.ttf.getbbox("Ag")[3] / 2 * len(self.out))

        var = (len(self.out) - self.rect.height // self.hstep) * self.hstep

        return var if var > 0 else 0

    def update(self) -> None:
        pass

    def draw(self, x: int = None, y: int = None, ax: int = 0, ay: int = 0) -> None:
        self.init()

        if x is None:
            x = self.rect.x + ax

        if y is None:
            y = self.rect.y + ay

        if self.vertical == "center":
            py = (self.rect.height - len(self.out) * self.hstep) / 2

        elif self.vertical == "up":
            py = 2

        elif self.vertical == "down":
            py = self.rect.height - len(self.out) * self.hstep - 2

        else:
            raise NameError(f"horizontal {self.horizontal} is not difined")

        for i, element in enumerate(self.out):
            if self.horizontal == "center":
                print_text(self.game.screen, x + (self.rect.width / 2 - self.ttf.getbbox(element)[2] / 2), y + i * self.hstep + py, element, self.font_size, self.font_type, self.font_color, self.alpha)

            elif self.horizontal == "left":
                print_text(self.game.screen, x + 4, y + i * self.hstep + py, element, self.font_size, self.font_type, self.font_color, self.alpha)

            elif self.horizontal == "right":
                print_text(self.game.screen, (x + self.rect.width) - self.ttf.getbbox(element)[2] - 4, y + i * self.hstep + py, element, self.font_size, self.font_type, self.font_color, self.alpha)

            else:
                raise NameError(f"horizontal {self.horizontal} is not difined")
