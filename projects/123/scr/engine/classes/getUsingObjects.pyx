from engine.classes.collision import Collision
from engine.classes.objects import DynamicObject
from engine.variables import *

import typing


if typing.TYPE_CHECKING:
    from engine.classes.group import ObjectGroup

else:
    pass


cdef class GetUsingObjects:
    @staticmethod
    def getUsingObjectsBase(game, group) -> None:
        dynamics = [obj for obj in group.objects if type(obj) == DynamicObject]

        for obj in dynamics:
            GetUsingObjects.getUsingObjectsIteration(game, group.objects, obj)

    @staticmethod
    def getUsingObjectsCircle(game, group) -> None:
        def binaryLeft(objects, distance: float) -> int:
            cdef int left = 0
            cdef int right = len(objects) - 1
            cdef int mid

            while left < right:
                mid = (left + right) // 2
                if objects[mid].distance < distance:
                    left = mid + 1

                else:
                    right = mid

            return left if objects[left].distance >= distance else 0

        def binaryRight(objects, distance: float) -> int:
            cdef int left = 0
            cdef int right = len(objects) - 1
            cdef int mid

            while left < right:
                mid = (left + right + 1) // 2
                if objects[mid].distance > distance:
                    right = mid - 1

                else:
                    left = mid

            return right if objects[right].distance <= distance else len(objects) - 1

        cdef list dynamicsObjects = []

        for obj in group.objects:
            if type(obj) == DynamicObject:
                dynamicsObjects.append(obj)

        game.cash["object_sorted_by_distance"] = sorted(group.objects, key=lambda obj: obj.distance)

        for obj in dynamicsObjects:
            l = binaryLeft(game.cash["object_sorted_by_distance"], obj.distance - group.maxLenghtObject)
            r = binaryRight(game.cash["object_sorted_by_distance"], obj.distance + group.maxLenghtObject) + 1

            GetUsingObjects.getUsingObjectsIteration(game, game.cash["object_sorted_by_distance"][l:r], obj)

    @staticmethod
    def getUsingObjectsSquare(game, group) -> None:
        def binaryLeft(objects, x: float) -> int:
            cdef int left = 0
            cdef int right = len(objects) - 1
            cdef int mid

            while left < right:
                mid = (left + right) // 2
                if objects[mid].pos.x < x:
                    left = mid + 1

                else:
                    right = mid

            return left if objects[left].pos.x >= x else 0

        def binaryRight(objects, x: float) -> int:
            cdef int left = 0
            cdef int right = len(objects) - 1
            cdef int mid

            while left < right:
                mid = (left + right + 1) // 2
                if objects[mid].pos.x > x:
                    right = mid - 1

                else:
                    left = mid

            return right if objects[right].pos.x <= x else len(objects) - 1

        cdef list dynamicsObjects = []

        for obj in group.objects:
            if isinstance(obj, DynamicObject):
                dynamicsObjects.append(obj)

        game.cash["object_sorted_by_distance"] = sorted(group.objects, key=lambda obj: obj.pos.x)
        game.cash["object_sorted_by_distance"] = list(filter(lambda obj: obj.doCollisionUpdate, game.cash["object_sorted_by_distance"]))

        for obj in dynamicsObjects:
            resulting = obj.getVectorsPower()

            l = binaryLeft(game.cash["object_sorted_by_distance"], obj.pos.x - resulting.x - group.maxLenghtObject)
            r = binaryRight(game.cash["object_sorted_by_distance"], obj.pos.x + resulting.x + group.maxLenghtObject) + 1

            objectsBefore = game.cash["object_sorted_by_distance"][l:r]
            objectsAfter = []

            for before in objectsBefore:
                if not (obj.pos.y + obj.hitbox.y + obj.hitbox.height + group.maxLengthObject < before.pos.y + before.hitbox.y or before.pos.y + before.hitbox.y + before.hitbox.height + group.maxLenghtObject < obj.pos.y + obj.hitbox.y):
                    objectsAfter.append(before)

            GetUsingObjects.getUsingObjectsIterationSquare(game, objectsAfter, obj)

    @staticmethod
    def getUsingObjectsIteration(game, objects, obj) -> None:
        game.cash["collisions"][obj.id] = []

        hitbox = obj.hitbox.copy()

        hitbox.x -= hitbox.width
        hitbox.y -= hitbox.height

        hitbox.width *= 3
        hitbox.height *= 3

        for j, second in enumerate(objects):
            if obj.id == second.id:
                continue

            var = obj.collisions.get(second.group)

            if var is not None or True:
                if True or Collision.rect(second.pos.x + second.hitbox.x, second.pos.y + second.hitbox.y, second.hitbox.width, second.hitbox.height, obj.pos.x + hitbox.x, obj.pos.y + hitbox.y, hitbox.width, hitbox.height):
                    game.cash["collisions"][obj.id].append({"object": second, "functions": var})


    @staticmethod
    def getUsingObjectsIterationSquare(game, objects, obj) -> None:
        game.cash["collisions"][obj.id] = []

        for j, second in enumerate(objects):
            if obj.id == second.id:
                continue

            game.cash["collisions"][obj.id].append({"object": second, "functions": obj.collisions.get(second.group)})

