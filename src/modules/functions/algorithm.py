import functools
import typing
import math


def cacheBezierCurve(func):
    cache = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        x0, y0, x1, y1, x2, y2, x3, y3, d = args

        key = f"{x0 - x1}-{x1 - x2}-{x2 - x3}-{y0 - y1}-{y1 - y2}-{y2 - y3}-{d}"

        if key not in cache:
            cache[key] = {
                "pos": (x0, y0),
                "value": func(*args, **kwargs)
            }

        px = x0 - cache[key]["pos"][0]
        py = y0 - cache[key]["pos"][1]

        if px == 0 and py == 0:
            return cache[key]["value"]

        return [[element[0] + px, element[1] + py] for element in cache[key]["value"]]

    return wrapper


@cacheBezierCurve
def bezierCurveDeep(x0: int, y0: int, x1: int, y1: int, x2: int, y2: int, x3: int, y3: int, d: int) -> typing.List[typing.List[int]]:
    def function(x0: int, y0: int, x1: int, y1: int, x2: int, y2: int, x3: int, y3: int, d: int) -> typing.List[int]:
        px = (x3 - x0) / 3
        py = (y3 - y0) / 3

        mx1 = x1 - x0 - px
        my1 = y1 - y0 - py
        mx2 = x2 - x3 + px
        my2 = y2 - y3 + py

        d1 = math.sqrt(mx1 ** 2 + my1 ** 2)
        d2 = math.sqrt(mx2 ** 2 + my2 ** 2)

        if d1 < d and d2 < d:
            answer.append([x3, y3])

        else:
            x01 = (x0 + x1) / 2
            y01 = (y0 + y1) / 2
            x12 = (x1 + x2) / 2
            y12 = (y1 + y2) / 2
            x23 = (x2 + x3) / 2
            y23 = (y2 + y3) / 2
            x012 = (x01 + x12) / 2
            y012 = (y01 + y12) / 2
            x123 = (x12 + x23) / 2
            y123 = (y12 + y23) / 2
            x0123 = (x012 + x123) / 2
            y0123 = (y012 + y123) / 2

            function(x0, y0, x01, y01, x012, y012, x0123, y0123, d)
            function(x0123, y0123, x123, y123, x23, y23, x3, y3, d)

    answer = []

    function(x0, y0, x1, y1, x2, y2, x3, y3, d)

    return [[math.ceil(element[0]), math.ceil(element[1])] if i not in (0, len(answer) - 1) else element for i, element in enumerate(answer)]


@cacheBezierCurve
def bezierCurveWidth(x0: int, y0: int, x1: int, y1: int, x2: int, y2: int, x3: int, y3: int, d: int) -> typing.List[typing.List[int]]:
    answer = [[x0, y0]]

    stack = [[x0, y0, x1, y1, x2, y2, x3, y3]]

    while stack:
        var = stack.pop()

        x0, y0, x1, y1, x2, y2, x3, y3 = var

        px = (x3 - x0) / 3
        py = (y3 - y0) / 3

        mx1 = x1 - x0 - px
        my1 = y1 - y0 - py
        mx2 = x2 - x3 + px
        my2 = y2 - y3 + py

        d1 = math.sqrt(mx1 ** 2 + my1 ** 2)
        d2 = math.sqrt(mx2 ** 2 + my2 ** 2)

        if d1 < d and d2 < d:
            answer.append([x3, y3])

        else:
            x01 = (x0 + x1) / 2
            y01 = (y0 + y1) / 2
            x12 = (x1 + x2) / 2
            y12 = (y1 + y2) / 2
            x23 = (x2 + x3) / 2
            y23 = (y2 + y3) / 2
            x012 = (x01 + x12) / 2
            y012 = (y01 + y12) / 2
            x123 = (x12 + x23) / 2
            y123 = (y12 + y23) / 2
            x0123 = (x012 + x123) / 2
            y0123 = (y012 + y123) / 2

            stack.append([x0123, y0123, x123, y123, x23, y23, x3, y3])
            stack.append([x0, y0, x01, y01, x012, y012, x0123, y0123])

    answer.append([x3, y3])

    return answer
