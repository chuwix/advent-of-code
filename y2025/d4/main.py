from dataclasses import dataclass
from io import open
from os import PathLike
from typing import Iterable

from more_itertools import quantify


def parse(s: str) -> list[bool]:
    return [c == "@" for c in s if not c.isspace()]


def get_lines(file: PathLike[str]) -> Iterable[list[int]]:
    with (open(file) as input):
        for row in input:
            yield parse(row)


def get_counts_around(row: int, col: int, inputs: list[list[bool]], neighbours_count: int) -> int:
    if not inputs[row][col]:
        return -1

    rows = slice(max(0, row - neighbours_count), min(len(inputs), row + neighbours_count + 1))
    cols = slice(max(0, col - neighbours_count), min(len(inputs[row]), col + neighbours_count + 1))
    total: int = 0
    for row in inputs[rows]:
        total += sum(row[cols])

    return total - 1


@dataclass
class RollInfo:
    i: int
    j: int
    neighbours: int


def find_all_counts(inputs: list[list[bool]], neighbours_count: int) -> Iterable[RollInfo]:
    for i, row in enumerate(inputs):
        for j, col in enumerate(row):
            yield RollInfo(i, j, get_counts_around(i, j, inputs, neighbours_count))


def solve_part_one(inputs: list[list[bool]], neighbours_count: int, count_limit: int) -> int:
    counts = find_all_counts(inputs, neighbours_count)
    return quantify(counts, lambda info: 0 <= info.neighbours <= count_limit)


def solve_part_two(inputs: list[list[bool]], neighbours_count: int, count_limit: int) -> int:
    total = 0

    while True:
        counts = find_all_counts(inputs, neighbours_count)
        new_count = 0

        for info in counts:
            if 0 <= info.neighbours <= count_limit:
                inputs[info.i][info.j] = False
                new_count += 1

        total += new_count
        if new_count == 0:
            return total
