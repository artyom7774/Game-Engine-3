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

        game.cache["object_sorted_by_distance"] = sorted(group.objects, key=lambda obj: obj.pos.x)
        game.cache["object_sorted_by_distance"] = list(filter(lambda obj: obj.doCollisionUpdate, game.cache["object_sorted_by_distance"]))

        for obj in dynamicsObjects:
            resulting = obj.getVectorsPower()

            l = binaryLeft(game.cache["object_sorted_by_distance"], obj.pos.x - resulting.x - group.maxLengthObject)
            r = binaryRight(game.cache["object_sorted_by_distance"], obj.pos.x + resulting.x + group.maxLengthObject) + 1

            objectsBefore = game.cache["object_sorted_by_distance"][l:r]
            objectsAfter = []

            for before in objectsBefore:
                if not (obj.pos.y + obj.hitbox.y + obj.hitbox.height + group.maxLengthObject < before.pos.y + before.hitbox.y or before.pos.y + before.hitbox.y + before.hitbox.height + group.maxLengthObject < obj.pos.y + obj.hitbox.y):
                    objectsAfter.append(before)

            GetUsingObjects.getUsingObjectsIterationSquare(game, objectsAfter, obj)

    @staticmethod
    def getUsingObjectsIterationSquare(game, objects, obj) -> None:
        game.cache["collisions"][obj.id] = []

        for j, second in enumerate(objects):
            if obj.id == second.id:
                continue

            game.cache["collisions"][obj.id].append({"object": second, "functions": obj.collisions.get(second.group)})

