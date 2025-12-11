import math
from itertools import combinations
from typing import Any, SupportsAbs, Generator


def sign(x: SupportsAbs) -> int:
    return int(math.copysign(1, x))


def all_combinations(iterable: list[Any]) -> Generator[tuple[Any, ...], None, None]:
    for i in range(1, len(iterable) + 1):
        for comb in combinations(iterable, i):
            yield comb