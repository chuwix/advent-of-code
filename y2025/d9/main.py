from __future__ import annotations

from typing import Iterable

from more_itertools.more import distinct_combinations
from more_itertools.recipes import prepend, triplewise, pairwise, flatten

from tools.datastructures.points import Point2, Rectangle
from tools.math import sign


def parse_inputs(file) -> Iterable[Point2]:
    with (open(file) as input):
        for row in input:
            yield Point2.from_data(map(int, row.split(",")))


def get_largest_square(points: Iterable[Point2]) -> int:
    a, b = max(distinct_combinations(points, 2), key=lambda pair: Rectangle.get_area(pair[0], pair[1]))
    return abs(a.x - b.x + 1) * abs(a.y - b.y + 1)


def get_shape_directions(points: list[Point2]) -> int:
    points = prepend(points[-1], points)
    dots = (sign((c - p1).cross_sign(p2 - c)) for p1, c, p2 in triplewise(points))
    return sign(sum(dots))


def get_edge_points(points: list[Point2]) -> set[Point2]:
    return set(flatten(Rectangle.get_points_inside(p1, p2) for p1, p2 in pairwise(prepend(points[-1], points))))


def find_inside_seed(points: list[Point2], direction: int) -> Point2:
    for p1, c, p2 in triplewise(prepend(points[-1], points)):
        if p1.x == p2.x or p1.y == p2.y: continue  # there is no 'inside' point
        if sign((c - p1).cross_sign(p2 - c)) != direction: continue  # the corner is facing outward
        return p1 + (p2 - p1) // 2
    raise Exception(f"Could not find inside seed: {points}")


def flood_fill_insides(edges: set[Point2], inside_seed: Point2) -> set[Point2]:
    stack = [inside_seed]
    insides = set()

    while len(stack) > 0:
        point = stack.pop()
        insides.add(point)
        for n in point.get_neighbours():
            if n in insides or n in edges: continue
            stack.append(n)

    return insides


def get_valid_rectangles(points: list[Point2], edges: set[Point2]) -> Iterable[Rectangle]:
    rectangles = (Rectangle(p[0], p[1]) for p in distinct_combinations(points, 2))
    return filter(lambda r: all(p in edges for p in r.points_inside()), rectangles)


def get_largest_square_connected(points: Iterable[Point2]) -> int:
    points = list(points)
    direction = get_shape_directions(points)
    edges = get_edge_points(points)
    insides = flood_fill_insides(edges, find_inside_seed(points, direction))
    valid_rectangles = get_valid_rectangles(points, edges | insides)
    return max(map(Rectangle.area, valid_rectangles))
