from engine.vector.float import Vec2f
from engine.vector.int import Vec2i

import pygame


class Sprite:
    cache = {}

    def __init__(self, game, obj, *args) -> None:
        """
        :param args: path: str,
                     pos: typing.Union[typing.List[int], typing.Tuple[int], Vec2f] = Vec2f(0, 0),
                     size: typing.Union[typing.List[int], typing.Tuple[int], Vec2i] = None

        :param agrs: path: str, x_offset: int, y_offset: int, width: int, height: int
        """

        self.game = game
        self.obj = obj

        if 0 < len(args) <= 3:
            path = args[0]
            pos  = args[1] if len(args) > 1 else Vec2i(0, 0)
            size = args[2] if len(args) > 2 else None

        elif len(args) == 5:
            path = args[0]
            pos  = Vec2f(args[1], args[2])
            size = Vec2i(args[3], args[4])

        else:
            raise ValueError("invalid number of arguments")

        self.path = path

        try:
            if type(path) == str:
                if path not in self.cache:
                    self.cache[path] = lambda: pygame.image.load(path).convert_alpha()

                self.image = self.cache[path]()

            else:
                self.image = path

        except FileNotFoundError:
            self.image = None

        self.size = size if type(size) == Vec2i else (Vec2i(*size) if size is not None else None)
        self.pos = pos if type(pos) == Vec2i else Vec2i(*pos)

        # print(self.pos)

        if self.image is not None and self.size is not None:
            self.width = size.x
            self.height = size.y

        else:
            self.width = -1
            self.height = -1

        if self.size is not None and self.image is not None:
            self.image = pygame.transform.scale(self.image, (
                self.width if self.width > 0 else self.image.get_width(),
                self.height if self.height > 0 else self.image.get_height()
            ))

        if self.image is not None:
            self.copyImage = self.image.copy()

    def copy(self) -> "Sprite":
        return Sprite(self.game, self.obj, self.path, self.pos, Vec2i(self.width, self.height))

    def resize(self, width: int, height: int) -> None:
        self.width, self.height = width, height

        self.copyImage = pygame.transform.scale(self.image, (self.width, self.height))

    def flip(self, horizontal: bool = False, vertical: bool = False) -> None:
        if self.image is None:
            return

        self.image = pygame.transform.flip(self.image, horizontal, vertical)
        self.copyImage = pygame.transform.flip(self.copyImage, horizontal, vertical)

    def get(self) -> pygame.Surface:
        return self.copyImage
