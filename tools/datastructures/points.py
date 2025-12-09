from __future__ import annotations

import dataclasses
import math
from typing import Iterable, Tuple

from more_itertools.more import minmax


@dataclasses.dataclass(frozen=True)
class Point2:
    x: int
    y: int

    @staticmethod
    def from_data(data: Iterable[int]) -> Point2:
        data = iter(data)
        return Point2(next(data), next(data))

    def __add__(self, other: Point2) -> Point2:
        return Point2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point2) -> Point2:
        return Point2(self.x - other.x, self.y - other.y)

    def __mul__(self, mul: int) -> Point2:
        return Point2(self.x * mul, self.y * mul)

    def __floordiv__(self, div: int) -> Point2:
        return Point2(self.x // div, self.y // div)

    def dot(self, other: Point2) -> int:
        return self.x * other.x + self.y * other.y

    def cross(self, other: Point2) -> int:
        return self.x * other.y - self.y * other.x

    def cross_sign(self, other: Point2) -> int:
        return int(math.copysign(1, self.cross(other)))

    def distance_sq(self, other: Point2) -> int:
        dx = self.x - other.x
        dy = self.y - other.y
        return dx * dx + dy * dy

    def distance(self, other: Point2) -> float:
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx * dx + dy * dy)

    def get_neighbours(self) -> Tuple[Point2, Point2, Point2, Point2]:
        return Point2(self.x + 1, self.y), Point2(self.x - 1, self.y), Point2(self.x, self.y + 1), Point2(self.x, self.y - 1)


@dataclasses.dataclass(frozen=True)
class Rectangle:
    p1: Point2
    p2: Point2

    @staticmethod
    def get_area(p1: Point2, p2: Point2) -> int:
        return abs(p1.x - p2.x + 1) * abs(p1.y - p2.y + 1)

    def area(self) -> int:
        return Rectangle.get_area(self.p1, self.p2)

    @staticmethod
    def get_points_inside(p1: Point2, p2: Point2) -> Iterable[Point2]:
        x1, x2 = minmax(p1.x, p2.x)
        y1, y2 = minmax(p1.y, p2.y)
        for i in range(x1, x2 + 1):
            for j in range(y1, y2 + 1):
                yield Point2(i, j)

    def points_inside(self) -> Iterable[Point2]:
        return Rectangle.get_points_inside(self.p1, self.p2)


@dataclasses.dataclass(frozen=True)
class Point3:
    x: int
    y: int
    z: int

    @staticmethod
    def from_data(data: Iterable[int]) -> Point3:
        data = iter(data)
        return Point3(next(data), next(data), next(data))

    def distance_sq(self, other: Point3) -> int:
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return dx * dx + dy * dy + dz * dz
