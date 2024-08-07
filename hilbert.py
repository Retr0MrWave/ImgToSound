import math
from attrs import define
from loguru import logger


@define
class Point:
    x: int
    y: int


type Curve = list[Point]


def mirror(curve: Curve) -> Curve:
    curve = [Point(p.y, p.x) for p in curve]
    return curve


def negative_mirror(curve: Curve) -> Curve:
    size = round(math.sqrt(len(curve)))
    curve = [Point(-p.y + size-1, -p.x + size-1) for p in curve]
    return curve


def shift(curve: Curve, x: int, y: int) -> Curve:
    return [Point(p.x + x, p.y + y) for p in curve]


def hilbert_curve(iteration: int) -> Curve:
    if iteration == 0:
        return [Point(0, 0)]

    prev = hilbert_curve(iteration - 1)
    prev_size = round(math.sqrt(len(prev)))
    return (mirror(prev) +
            shift(prev, prev_size, 0) +
            shift(prev, prev_size, prev_size) +
            shift(negative_mirror(prev), 0, prev_size))


def print_curve(curve: Curve) -> None:
    size = round(math.sqrt(len(curve)))
    output = [[-1 for j in range(size)] for i in range(size)]

    for i in range(len(curve)):
        output[curve[i].x][curve[i].y] = i

    for line in output:
        print(line)


def closest_hilbert_size(n: int) -> int:
    r = 0
    while n > 1:
        n >>= 1
        r += 1

    return r


def main() -> None:
    print_curve(hilbert_curve(1))
    print()
    print_curve(hilbert_curve(2))
    print()
    print_curve(hilbert_curve(3))
    print()
    print_curve(hilbert_curve(4))


if __name__ == "__main__":
    main()
