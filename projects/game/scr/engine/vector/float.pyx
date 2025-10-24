cdef class Vec2f:
    __slots__ = ("x", "y")

    cdef public double x, y

    def __init__(self, double x=0, double y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Vec2f({self.x}, {self.y})"

    def __repr__(self):
        return f"Vec2f({self.x}, {self.y})"

    def __add__(self, double other):
        self.x += other
        self.y += other
        return self

    def __sub__(self, double other):
        self.x -= other
        self.y -= other
        return self

    def __mul__(self, double other):
        self.x *= other
        self.y *= other
        return self

    def __truediv__(self, int other):
        self.x /= other
        self.y /= other
        return self

    def __floordiv__(self, double other):
        self.x //= other
        self.y //= other
        return self

    def __getitem__(self, int item):
        if item == 0:
            return self.x

        elif item == 1:
            return self.y

        else:
            raise IndexError("index out of range")

    def __len__(self):
        return 2

    def get(self):
        return (self.x, self.y)


cdef class Vec3f:
    __slots__ = ("x", "y", "z")

    cdef public double x, y, z

    def __init__(self, double x=0, double y=0, double z=0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"Vec3f({self.x}, {self.y}, {self.z})"

    def __repr__(self):
        return f"Vec3f({self.x}, {self.y}, {self.z})"

    def __add__(self, double other):
        self.x += other
        self.y += other
        self.z += other
        return self

    def __sub__(self, double other):
        self.x -= other
        self.y -= other
        self.z -= other
        return self

    def __mul__(self, double other):
        self.x *= other
        self.y *= other
        self.z *= other
        return self

    def __truediv__(self, int other):
        self.x /= other
        self.y /= other
        self.z /= other
        return self

    def __floordiv__(self, double other):
        self.x //= other
        self.y //= other
        self.z //= other
        return self

    def __getitem__(self, int item):
        if item == 0:
            return self.x

        elif item == 1:
            return self.y

        elif item == 2:
            return self.z

        else:
            raise IndexError("index out of range")

    def __len__(self):
        return 3

    def get(self):
        return (self.x, self.y, self.z)


cdef class Vec4f:
    __slots__ = ("x", "y", "z", "w")

    cdef public double x, y, z, w

    def __init__(self, double x=0, double y=0, double z=0, double w=0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __str__(self):
        return f"Vec4f({self.x}, {self.y}, {self.z}, {self.w})"

    def __repr__(self):
        return f"Vec4f({self.x}, {self.y}, {self.z}, {self.w})"

    def __add__(self, double other):
        self.x += other
        self.y += other
        self.z += other
        self.w += other
        return self

    def __sub__(self, double other):
        self.x -= other
        self.y -= other
        self.z -= other
        self.w -= other
        return self

    def __mul__(self, double other):
        self.x *= other
        self.y *= other
        self.z *= other
        self.w *= other
        return self

    def __truediv__(self, double other):
        self.x /= other
        self.y /= other
        self.z /= other
        self.w /= other
        return self

    def __floordiv__(self, double other):
        self.x //= other
        self.y //= other
        self.z //= other
        self.w //= other
        return self

    def __getitem__(self, int item):
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

    def __len__(self):
        return 4

    def get(self):
        return (self.x, self.y, self.z, self.w)