import operator
from functools import reduce
from typing import Iterable, Tuple

from tools.math import all_combinations


def parse_target_state(it: str) -> set[int]:
    return set(i for i, c in enumerate(it[1:-1]) if c == "#")


def parse_buttons(it: Iterable[str]) -> Iterable[set[int]]:
    for button_str in it:
        yield set(int(i) for i in button_str[1:-1].split(","))


def parse_inputs(file) -> Iterable[Tuple[set[int], list[set[int]]]]:
    with (open(file) as input):
        for row in input:
            sections = row.split(' ')
            yield parse_target_state(sections[0]), list(parse_buttons(sections[1:-1]))


def compute_fewest_button_presses(wiring: Iterable[Tuple[set[int], list[set[int]]]]) -> int:
    def get_valid_button_presses(target, buttons) -> Iterable[Tuple[set[int]]]:
        return (comb for comb in all_combinations(buttons) if reduce(operator.xor, comb) == target)

    return sum(min(map(len, get_valid_button_presses(target_state, buttons))) for target_state, buttons in wiring)
