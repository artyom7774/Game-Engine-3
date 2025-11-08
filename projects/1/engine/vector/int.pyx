cdef class Vec2i:
    __slots__ = ("x", "y")

    cdef public int x, y

    def __init__(self, int x=0, int y=0):
        self.x = int(x)
        self.y = int(y)

    def __str__(self):
        return f"Vec2i({int(self.x)}, {int(self.y)})"

    def __repr__(self):
        return f"Vec2i({int(self.x)}, {int(self.y)})"

    def __getattr__(self, name):
        if name == "x":
            return int(self.x)

        elif name == "y":
            return int(self.y)

        else:
            return super().__getattr__(name)

    def __add__(self, int other):
        self.x += other
        self.y += other
        return self

    def __sub__(self, int other):
        self.x -= other
        self.y -= other
        return self

    def __mul__(self, int other):
        self.x *= other
        self.y *= other
        return self

    def __truediv__(self, int other):
        self.x //= other
        self.y //= other
        return self

    def __floordiv__(self, int other):
        self.x //= other
        self.y //= other
        return self

    def __getitem__(self, int item):
        if item == 0:
            return int(self.x)

        elif item == 1:
            return int(self.y)

        else:
            raise IndexError("index out of range")

    def __len__(self):
        return 2

    def get(self):
        return int(self.x), int(self.y)


cdef class Vec3i:
    __slots__ = ("x", "y", "z")

    cdef public int x, y, z

    def __init__(self, int x=0, int y=0, int z=0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"Vec3i({int(self.x)}, {int(self.y)}, {int(self.z)})"

    def __repr__(self):
        return f"Vec3i({int(self.x)}, {int(self.y)}, {int(self.z)})"

    def __getattr__(self, name):
        if name == "x":
            return int(self.x)

        elif name == "y":
            return int(self.y)

        elif name == "z":
            return int(self.z)

        else:
            return super().__getattr__(name)

    def __add__(self, int other):
        self.x += other
        self.y += other
        self.z += other
        return self

    def __sub__(self, int other):
        self.x -= other
        self.y -= other
        self.z -= other
        return self

    def __mul__(self, int other):
        self.x *= other
        self.y *= other
        self.z *= other
        return self

    def __truediv__(self, int other):
        self.x //= other
        self.y //= other
        self.z //= other
        return self

    def __floordiv__(self, int other):
        self.x //= other
        self.y //= other
        self.z //= other
        return self

    def __getitem__(self, int item):
        if item == 0:
            return int(self.x)

        elif item == 1:
            return int(self.y)

        elif item == 2:
            return int(self.z)

        else:
            raise IndexError("index out of range")

    def __len__(self):
        return 3

    def get(self):
        return int(self.x), int(self.y), int(self.z)


cdef class Vec4i:
    __slots__ = ("x", "y", "z", "w")

    cdef public int x, y, z, w

    def __init__(self, int x=0, int y=0, int z=0, int w=0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __str__(self):
        return f"Vec4i({int(self.x)}, {int(self.y)}, {int(self.z)}, {int(self.w)})"

    def __repr__(self):
        return f"Vec4i({int(self.x)}, {int(self.y)}, {int(self.z)}, {int(self.w)})"

    def __getattr__(self, name):
        if name == "x":
            return int(self.x)

        elif name == "y":
            return int(self.y)

        elif name == "z":
            return int(self.z)

        elif name == "w":
            return int(self.w)

        else:
            return super().__getattr__(name)

    def __add__(self, int other):
        self.x += other
        self.y += other
        self.z += other
        self.w += other
        return self

    def __sub__(self, int other):
        self.x -= other
        self.y -= other
        self.z -= other
        self.w -= other
        return self

    def __mul__(self, int other):
        self.x *= other
        self.y *= other
        self.z *= other
        self.w *= other
        return self

    def __truediv__(self, int other):
        self.x //= other
        self.y //= other
        self.z //= other
        self.w //= other
        return self

    def __floordiv__(self, int other):
        self.x //= other
        self.y //= other
        self.z //= other
        self.w //= other
        return self

    def __getitem__(self, int item):
        if item == 0:
            return int(self.x)

        elif item == 1:
            return int(self.y)

        elif item == 2:
            return int(self.z)

        elif item == 3:
            return int(self.w)

        else:
            raise IndexError("index out of range")

    def __len__(self):
        return 4

    def get(self):
        return int(self.x), int(self.y), int(self.z), int(self.w)
