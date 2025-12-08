from __future__ import annotations

import dataclasses
import heapq
import operator
from functools import reduce
from typing import Iterable

from more_itertools import take
from more_itertools.more import distinct_combinations


@dataclasses.dataclass(frozen=True)
class Point3:
    x: int
    y: int
    z: int
    salt = 9999

    @staticmethod
    def from_data(data: Iterable[int]) -> Point3:
        data = iter(data)
        return Point3(next(data), next(data), next(data))

    def distance_sq(self, other: Point3) -> int:
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return dx * dx + dy * dy + dz * dz


def parse_inputs(file) -> Iterable[Point3]:
    with (open(file) as input):
        for row in input:
            yield Point3.from_data(map(int, row.split(",")))


@dataclasses.dataclass
class PointPair:
    p1: Point3
    p2: Point3
    dist_sq: int


@dataclasses.dataclass
class Box:
    circuit: set[Point3]


def join_circuit_pair(circuits: dict[Point3, Box], pair: PointPair) -> set[Point3]:
    b1 = circuits.get(pair.p1, None)
    b2 = circuits.get(pair.p2, None)
    match b1, b2:
        case None, None:
            b = Box({pair.p1, pair.p2})
            circuits[pair.p1] = b
            circuits[pair.p2] = b
            return b.circuit
        case Box(), None:
            b1.circuit.add(pair.p2)
            circuits[pair.p2] = b1
            return b1.circuit
        case None, Box():
            b2.circuit.add(pair.p1)
            circuits[pair.p1] = b2
            return b2.circuit
        case _:
            b1.circuit.update(b2.circuit)
            for old in b2.circuit:
                circuits[old].circuit = b1.circuit
            return b1.circuit


def compute_junctions(points: Iterable[Point3], closest_points: int, circuits_to_mult: int) -> int:
    def compute_circuits(sorted_pairs: list[PointPair]) -> Iterable[set[Point3]]:
        circuit_map: dict[Point3, Box] = {}

        for pair in sorted_pairs:
            join_circuit_pair(circuit_map, pair)

        return {id(box.circuit): box.circuit for box in circuit_map.values()}.values()

    pairs = map(lambda t: PointPair(t[0], t[1], t[0].distance_sq(t[1])), distinct_combinations(points, 2))
    min_dists = heapq.nsmallest(closest_points, pairs, lambda pair: pair.dist_sq)
    circuits = compute_circuits(min_dists)

    top_circuits = sorted(map(len, circuits), reverse=True)
    return reduce(operator.mul, take(circuits_to_mult, top_circuits))


def compute_last_junction(points: Iterable[Point3], closest_points: int, circuits_to_mult: int) -> int:
    def compute_circuits(sorted_pairs: list[PointPair], point_count: int) -> PointPair | None:
        circuit_map: dict[Point3, Box] = {}

        for pair in sorted_pairs:
            joined_circuit = join_circuit_pair(circuit_map, pair)
            if len(joined_circuit) == point_count:
                return pair

    points = list(points)
    pairs = map(lambda t: PointPair(t[0], t[1], t[0].distance_sq(t[1])), distinct_combinations(points, 2))
    min_dists = sorted(pairs, key=lambda pair: pair.dist_sq)
    last_pair = compute_circuits(min_dists, len(points))
    return last_pair.p1.x * last_pair.p2.x
