from __future__ import annotations

from typing import Iterable

from more_itertools.more import distinct_combinations

from tools.datastructures.points import Point2


def parse_inputs(file) -> Iterable[Point2]:
    with (open(file) as input):
        for row in input:
            yield Point2.from_data(map(int, row.split(",")))


def get_largest_square(points: Iterable[Point2]) -> int:
    a, b = max(distinct_combinations(points, 2), key=lambda pair: pair[0].area(pair[1]))
    return abs(a.x - b.x + 1) * abs(a.y - b.y + 1)

def get_largest_square_connected(points: Iterable[Point2]) -> int:
    partitions =
    a, b = max(distinct_combinations(points, 2), key=lambda pair: pair[0].area(pair[1]))
    return abs(a.x - b.x + 1) * abs(a.y - b.y + 1)
