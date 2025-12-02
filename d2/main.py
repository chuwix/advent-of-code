from typing import Iterable, Tuple
from io import open

import csv


def parse(s: str) -> Tuple[int, int]:
    vals = s.split("-", 2)
    return int(vals[0]), int(vals[1])


def get_ranges(file: str) -> Iterable[Tuple[int, int]]:
    with (open(file) as input):
        reader = csv.reader(input)
        for row in reader:
            for value in row:
                yield parse(value)


def is_invalid(i: int) -> bool:
    s = str(i)
    if len(s) % 2 == 1:
        return False
    return s.endswith(s[:len(s) // 2])


def solve_part_one(ranges: Iterable[Tuple[int, int]]) -> Iterable[int]:
    for lower, upper in ranges:
        for i in range(lower, upper + 1):
            if is_invalid(i):
                yield i


def is_invalid_repeated(i: int) -> bool:
    s = str(i)
    for i in range(1, len(s) // 2 + 1):
        if len(s) % i != 0:
            continue

        if s[:i] * (len(s) // i) == s:
            return True

    return False

def solve_part_two(ranges: Iterable[Tuple[int, int]]) -> Iterable[int]:
    for lower, upper in ranges:
        for i in range(lower, upper + 1):
            if is_invalid_repeated(i):
                yield i
