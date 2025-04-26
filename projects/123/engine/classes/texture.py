from engine.classes.sprite import Sprite

from engine.vector.int import Vec2i

from PIL import Image

import typing
import pygame
import math


class Texture:
    def __init__(
            self, game, path: str,
            size: typing.Union[typing.List[int], typing.Tuple[int], Vec2i] = None
    ) -> None:
        self.game = game

        self.image = Image.open(path).convert("RGBA")

        self.size = size if type(size) == Vec2i else (Vec2i(*size) if size is not None else None)

        if self.size is not None:
            self.image = self.image.resize((self.size.x, self.size.y))

        self.width = self.image.width
        self.height = self.image.height

    def sprite(self, width: int, height: int) -> Sprite:
        surface = pygame.Surface((width, height))

        image = pygame.image.frombytes(
            self.image.tobytes(), self.image.size, "RGBA"
        )

        for i in range(math.ceil(width / self.width)):
            for j in range(math.ceil(height / self.height)):
                surface.blit(image, (i * self.width, j * self.height))

        return Sprite(self.game, surface)

    def get(self) -> pygame.sprite.Sprite:
        return self.image
