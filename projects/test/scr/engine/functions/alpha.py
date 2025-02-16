from engine.classes.hitbox import SquareHitbox
from engine.vector.int import Vec4i, Vec3i

import typing
import pygame


def alphaRect(screen, color: typing.Union[Vec4i, Vec3i, typing.List[int]], rect: SquareHitbox, border: int = 0):
    if type(color) == list and len(color) == 3:
        color = Vec3i(*color)

    if type(color) == list and len(color) == 4:
        color = Vec4i(*color)

    surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(surface, color.get(), (0, 0, rect.width, rect.height), border)

    screen.blit(surface, (rect.x, rect.y))
