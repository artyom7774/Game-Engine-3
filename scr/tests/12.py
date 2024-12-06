from math import sqrt


def bezierСurve(x0, y0, x1, y1, x2, y2, x3, y3, d):
    answer = []

    def function(x0, y0, x1, y1, x2, y2, x3, y3, d):
        px = (x3 - x0) / 3
        py = (y3 - y0) / 3
        mx1 = x1 - x0 - px
        my1 = y1 - y0 - py
        mx2 = x2 - x3 + px
        my2 = y2 - y3 + py
        d1 = sqrt(mx1 ** 2 + my1 ** 2)
        d2 = sqrt(mx2 ** 2 + my2 ** 2)
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
            bezierСurve(x0, y0, x01, y01, x012, y012, x0123, y0123, d)
            bezierСurve(x0123, y0123, x123, y123, x23, y23, x3, y3, d)

    function(x0, y0, x1, y1, x2, y2, x3, y3, d)

    return answer


# d - точность
print(bezierСurve(0, 200, 200, 200, 200, 0, 400, 0, 0.0001))
