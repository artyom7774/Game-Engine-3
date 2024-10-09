from engine.vector.float import Vec4f

import typing


class SquareHitbox:
    def __init__(
            self, hitbox: typing.Union[typing.List[int], Vec4f]
    ) -> None:
        self.hitbox = hitbox if type(hitbox) == Vec4f else Vec4f(*hitbox)

    def __getattr__(self, item) -> typing.Any:
        if item in ("x", "y", "width", "height"):
            return (self.hitbox[0] if item == "x" else self.hitbox[1]) if item in ("x", "y") else (self.hitbox[2] if item == "width" else self.hitbox[3])

        return super().__getattr__(self, item)

    def __getitem__(self, item: int) -> typing.Any:
        if item == 0:
            return self.x

        elif item == 1:
            return self.y

        elif item == 2:
            return self.z

        elif item == 3:
            return self.w

        else:
            raise IndexError("index out of range")

    def __len__(self) -> int:
        return 4

    def __str__(self) -> str:
        return "SquareHitbox(" + ", ".join(list(map(str, list(self.hitbox.get())))) + ")"

    def __repr__(self) -> str:
        return "SquareHitbox(" + ", ".join(list(map(str, list(self.hitbox.get())))) + ")"

    def contains(self, obj: "SquareHitbox") -> bool:
        return self.x <= obj.pos.x < self.x + self.width and self.y <= obj.pos.y < self.y + self.height

    def get(self) -> typing.List[float]:
        return self.hitbox.get()

    def copy(self) -> "SquareHitbox":
        return SquareHitbox(self.hitbox)
