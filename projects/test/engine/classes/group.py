from engine.classes.objects import DynamicObject

from engine.classes.collision import Collision

from engine.classes.hitbox import SquareHitbox

from engine.classes.sprite import Sprite

from engine.functions.alpha import alphaRect

from engine.variables import *

import typing
import pygame
import types
import math


class ParticleGroup:
    def __init__(self, game, particles: typing.List[VParticle] = None) -> None:
        if particles is None:
            particles = []

        self.game = game

        self.particles = particles

    def __len__(self) -> int:
        return len(self.particles)

    def add(self, particle: VParticle) -> None:
        self.particles.append(particle.copy())

    def remove(self, particle: VObject) -> None:
        self.particles.remove(particle)

    def getById(self, id: int) -> VParticle:
        for particle in self.particles:
            if particle.id == id:
                return particle

        raise NameError(f"id {id} isn't found")

    def removeById(self, id: int) -> None:
        for particle in self.particles:
            if particle.id == id:
                self.particles.remove(particle)
                return 0

        raise IndexError(f"id {id} not found in group")

    def getByGroup(self, group: str) -> typing.List[VParticle]:
        return [particle for particle in self.particles if particle.group == group]

    def update(self):
        for particle in self.particles:
            particle.update()

    def draw(self):
        px = self.game.camera.x()
        py = self.game.camera.y()

        for particle in self.particles:
            if self.game.width + particle.sprite.width > particle.pos.x + px > -particle.sprite.width and self.game.height + particle.sprite.height > particle.pos.y + py > -particle.sprite.height:
                particle.draw(px, py)


class ObjectGroup:
    def __init__(self, game, objects: typing.List[VObject] = None) -> None:
        if objects is None:
            objects = []

        self.game = game

        self.collisions = Collision()

        self.objects = objects

        self.maxLenghtObject = -INF
        self.minLenghtObject = +INF

    def empty(self):
        self.maxLenghtObject = -INF
        self.minLenghtObject = +INF

        for obj in self.objects:
            self.remove(obj)

    def add(self, obj: VObject) -> None:
        self.updateMinLenghtObject(obj)
        self.updateMaxLenghtObject(obj)

        if isinstance(obj, DynamicObject):
            return self.objects.insert(0, obj)

        self.objects.append(obj)

    def remove(self, obj: VObject) -> None:
        self.objects.remove(obj)

    def getById(self, id: int) -> VObject:
        for element in self.objects:
            if element.id == id:
                return element

        return None

    def removeByGroup(self, group: str) -> None:
        for element in self.objects:
            if element.group == group:
                self.objects.remove(element)

    def removeById(self, id: int) -> None:
        for element in self.objects:
            if element.id == id:
                self.objects.remove(element)
                return 0

        raise IndexError(f"id {id} not found in group")

    def getByGroup(self, group) -> typing.List[VObject]:
        return [element for element in self.objects if element.group == group]

    def updateMinLenghtObject(self, obj: VObject) -> None:
        self.minLenghtObject = min(self.minLenghtObject, obj.hitbox.width + obj.hitbox.height)

    def updateMaxLenghtObject(self, obj: VObject) -> None:
        self.maxLenghtObject = max(self.maxLenghtObject, obj.hitbox.width + obj.hitbox.height)

    def update(self) -> None:
        for obj in self.objects:
            obj.update()

    def draw(self) -> None:
        self.game.camera.update()

        px = self.game.camera.x()
        py = self.game.camera.y()

        for obj in sorted(self.objects, key=lambda x: x.drawPriority + x.pos.y * (10 ** -16)):
            if obj.sprite is not None:
                sprite = None

                if type(obj.sprite) == Sprite:
                    sprite = obj.sprite.get()

                elif type(obj.sprite) == list:
                    alphaRect(self.game.screen, obj.sprite, SquareHitbox([obj.pos.x, obj.pos.y, obj.hitbox.width, obj.hitbox.height]))

                elif type(obj.sprite) == types.FunctionType:
                    obj.sprite()

                    continue

                else:
                    sprite = obj.sprite.get(obj)

            if obj.sprite is not None and sprite is not None and type(obj.sprite) != list:
                obj.sprite.pos.x = 0
                obj.sprite.pos.y = 0

                if self.game.usingWidth + 200 > obj.pos.x + obj.sprite.pos.x + px > -200 and self.game.usingHeight + 200 > obj.pos.y + obj.sprite.pos.y + py > -200:
                    self.game.screen.blit(sprite, (obj.pos.x + obj.sprite.pos.x + px, obj.pos.y + obj.sprite.pos.y + py))

                # else:
                #     print(f"not visiable: {obj.sprite.pos.x} {obj.sprite.pos.y}")

            if self.game.debug or (obj.group.startswith("__") and obj.group.endswith("__") and not obj.group == "__debug_unvisiable__"):
                pygame.draw.rect(
                    self.game.screen, (255, 0, 0) if "debug_color" not in obj.specials else obj.specials["debug_color"],
                    (math.trunc(obj.pos.x) + obj.hitbox.x + px, math.trunc(obj.pos.y) + obj.hitbox.y + py, obj.hitbox.width, obj.hitbox.height), 1
                )
