import typing


class Vec2f:
    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"Vec2f({self.x}, {self.y})"

    def __repr__(self) -> str:
        return f"Vec2f({self.x}, {self.y})"

    def __add__(self, other: float) -> "Vec2f":
        self.x += other
        self.y += other

        return self

    def __sub__(self, other: float) -> "Vec2f":
        self.x -= other
        self.y -= other

        return self

    def __mul__(self, other: float) -> "Vec2f":
        self.x *= other
        self.y *= other

        return self

    def __truediv__(self, other: int) -> "Vec2f":
        self.x /= other
        self.y /= other

        return self

    def __floordiv__(self, other: float) -> "Vec2f":
        self.x //= other
        self.y //= other

        return self

    def __getitem__(self, item) -> typing.Any:
        if item == 0:
            return self.x

        elif item == 1:
            return self.y

        else:
            raise IndexError("index out of range")

    def __len__(self) -> int:
        return 2

    def get(self) -> tuple:
        return self.x, self.y
    

class Vec3f:
    def __init__(self, x: float = 0, y: float = 0, z: float = 0) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f"Vec3f({self.x}, {self.y}, {self.z})"

    def __repr__(self) -> str:
        return f"Vec3f({self.x}, {self.y}, {self.z})"

    def __add__(self, other: float) -> "Vec3f":
        self.x += other
        self.y += other
        self.z += other

        return self

    def __sub__(self, other: float) -> "Vec3f":
        self.x -= other
        self.y -= other
        self.z -= other

        return self

    def __mul__(self, other: float) -> "Vec3f":
        self.x *= other
        self.y *= other
        self.z *= other

        return self

    def __truediv__(self, other: int) -> "Vec3f":
        self.x /= other
        self.y /= other
        self.z /= other

        return self

    def __floordiv__(self, other: float) -> "Vec3f":
        self.x //= other
        self.y //= other
        self.z //= other

        return self

    def __getitem__(self, item) -> typing.Any:
        if item == 0:
            return self.x

        elif item == 1:
            return self.y

        elif item == 2:
            return self.z

        else:
            raise IndexError("index out of range")

    def __len__(self) -> int:
        return 3

    def get(self) -> tuple:
        return self.x, self.y, self.z
    

class Vec4f:
    def __init__(self, x: float = 0, y: float = 0, z: float = 0, w: float = 0) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __str__(self) -> str:
        return f"Vec4f({self.x}, {self.y}, {self.z}, {self.w})"

    def __repr__(self) -> str:
        return f"Vec4f({self.x}, {self.y}, {self.z}, {self.w})"

    def __add__(self, other: float) -> "Vec4f":
        self.x += other
        self.y += other
        self.z += other
        self.w += other

        return self

    def __sub__(self, other: float) -> "Vec4f":
        self.x -= other
        self.y -= other
        self.z -= other
        self.w -= other

        return self

    def __mul__(self, other: float) -> "Vec4f":
        self.x *= other
        self.y *= other
        self.z *= other
        self.w *= other

        return self

    def __truediv__(self, other: float) -> "Vec4f":
        self.x /= other
        self.y /= other
        self.z /= other
        self.w /= other

        return self

    def __floordiv__(self, other: float) -> "Vec4f":
        self.x //= other
        self.y //= other
        self.z //= other
        self.w //= other

        return self

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

    def get(self) -> tuple:
        return self.x, self.y, self.z, self.w
