from __future__ import annotations

import dataclasses
import math
from typing import Iterable


@dataclasses.dataclass(frozen=True)
class Point2:
    x: int
    y: int

    @staticmethod
    def from_data(data: Iterable[int]) -> Point2:
        data = iter(data)
        return Point2(next(data), next(data))

    def distance_sq(self, other: Point2) -> int:
        dx = self.x - other.x
        dy = self.y - other.y
        return dx * dx + dy * dy

    def distance(self, other: Point2) -> float:
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx * dx + dy * dy)

    def area(self, other: Point2):
        return abs(self.x - other.x + 1) * abs(self.y - other.y + 1)


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
