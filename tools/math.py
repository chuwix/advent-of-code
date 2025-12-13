import math
from itertools import combinations, combinations_with_replacement
from typing import Any, SupportsAbs, Generator

def identity(x):
    return x

def sign(x: SupportsAbs) -> int:
    return int(math.copysign(1, x))


def all_combinations(iterable: list[Any]) -> Generator[tuple[Any, ...], None, None]:
    for i in range(1, len(iterable) + 1):
        for comb in combinations(iterable, i):
            yield comb

def all_combinations_with_replacement(iterable: list[Any], up_to_size: int, *, include_empty_set: bool = False) -> Generator[tuple[Any, ...], None, None]:
    start = 1
    if include_empty_set: start = 0
    for i in range(start, up_to_size + 1):
        for comb in combinations_with_replacement(iterable, i):
            yield comb