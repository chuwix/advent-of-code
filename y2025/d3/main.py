from collections import deque
from functools import reduce
from os import PathLike
from typing import Iterable
from io import open


def parse(s: str) -> list[int]:
    return [int(d) for d in s if d.isdigit()]


def get_lines(file: PathLike[str]) -> Iterable[list[int]]:
    with (open(file) as input):
        for row in input:
            yield parse(row)


def try_evict_smallest(maxes: deque[int]):
    if len(maxes) < 2:
        return

    for i in range(len(maxes) - 1):
        if maxes[i] < maxes[i + 1]:
            del maxes[i]
            return


def find_n_maxes(battery: list[int], batteries: int) -> Iterable[int]:
    maxes: deque[int] = deque(maxlen=batteries)
    for v in reversed(battery):
        if len(maxes) < batteries:
            maxes.appendleft(v)
        elif v >= maxes[0]:
            try_evict_smallest(maxes)
            maxes.appendleft(v)
    return maxes


def solve(inputs: Iterable[list[int]], batteries: int) -> Iterable[int]:
    for battery in inputs:
        maxes = find_n_maxes(battery, batteries)
        yield reduce(lambda total, v: total * 10 + v, maxes, 0)
