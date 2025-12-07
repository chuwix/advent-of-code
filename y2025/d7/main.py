import dataclasses
from functools import reduce
from typing import Iterable

from more_itertools.more import peekable


def parse_inputs(file) -> Iterable[str]:
    with (open(file) as input):
        for row in input:
            yield row


@dataclasses.dataclass
class Totals:
    beams: list[bool]
    splits: int


def split_beams(totals: Totals, input: str) -> Totals:
    for i, c in enumerate(input):
        match c:
            case "S":
                totals.beams[i] = True
            case "^":
                if totals.beams[i]:
                    totals.splits += 1
                totals.beams[i - 1] = True
                totals.beams[i] = False
                totals.beams[i + 1] = True
    return totals


def compute_splits(inputs: Iterable[str]) -> int:
    inputs = peekable(inputs)
    initial_totals = Totals([False] * len(inputs.peek()), 0)
    totals = reduce(split_beams, inputs, initial_totals)

    return totals.splits


def split_paths(totals: list[int], input: str) -> list[int]:
    for i, c in enumerate(input):
        match c:
            case "S":
                totals[i] = 1
            case "^":
                totals[i - 1] += totals[i]
                totals[i + 1] += totals[i]
                totals[i] = 0
    return totals


def compute_paths(inputs: Iterable[str]) -> int:
    inputs = peekable(inputs)
    initial_path_counts = [0] * len(inputs.peek())
    path_counts = reduce(split_paths, inputs, initial_path_counts)

    return sum(path_counts)
