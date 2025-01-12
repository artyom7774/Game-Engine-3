import typing


class Vec2i:
    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"Vec2i({self.x}, {self.y})"

    def __repr__(self) -> str:
        return f"Vec2i({self.x}, {self.y})"

    def __add__(self, other: int) -> "Vec2i":
        self.x += other
        self.y += other

        return self

    def __sub__(self, other: int) -> "Vec2i":
        self.x -= other
        self.y -= other

        return self

    def __mul__(self, other: int) -> "Vec2i":
        self.x *= other
        self.y *= other

        return self

    def __truediv__(self, other: int) -> "Vec2i":
        self.x //= other
        self.y //= other

        return self

    def __floordiv__(self, other: int) -> "Vec2i":
        self.x //= other
        self.y //= other

        return self

    def __getitem__(self, item: int) -> typing.Any:
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


class Vec3i:
    def __init__(self, x: int = 0, y: int = 0, z: int = 0) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f"Vec3i({self.x}, {self.y}, {self.z})"

    def __repr__(self) -> str:
        return f"Vec3i({self.x}, {self.y}, {self.z})"

    def __add__(self, other: int) -> "Vec3i":
        self.x += other
        self.y += other
        self.z += other

        return self

    def __sub__(self, other: int) -> "Vec3i":
        self.x -= other
        self.y -= other
        self.z -= other

        return self

    def __mul__(self, other: int) -> "Vec3i":
        self.x *= other
        self.y *= other
        self.z *= other

        return self

    def __truediv__(self, other: int) -> "Vec3i":
        self.x //= other
        self.y //= other
        self.z //= other

        return self

    def __floordiv__(self, other: int) -> "Vec3i":
        self.x //= other
        self.y //= other
        self.z //= other

        return self

    def __getitem__(self, item: int) -> typing.Any:
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


class Vec4i:
    def __init__(self, x: int = 0, y: int = 0, z: int = 0, w: int = 0) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __str__(self) -> str:
        return f"Vec4i({self.x}, {self.y}, {self.z}, {self.w})"

    def __repr__(self) -> str:
        return f"Vec4i({self.x}, {self.y}, {self.z}, {self.w})"

    def __add__(self, other: int) -> "Vec4i":
        self.x += other
        self.y += other
        self.z += other
        self.w += other

        return self

    def __sub__(self, other: int) -> "Vec4i":
        self.x -= other
        self.y -= other
        self.z -= other
        self.w -= other

        return self

    def __mul__(self, other: int) -> "Vec4i":
        self.x *= other
        self.y *= other
        self.z *= other
        self.w *= other

        return self

    def __truediv__(self, other: int) -> "Vec4i":
        self.x //= other
        self.y //= other
        self.z //= other
        self.w //= other

        return self

    def __floordiv__(self, other: int) -> "Vec4i":
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
