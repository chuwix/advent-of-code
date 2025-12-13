import contextlib
import dataclasses
import multiprocessing
import operator
import sys
from functools import reduce
from itertools import combinations_with_replacement, groupby
from os import PathLike
from typing import Iterable, Tuple, cast

from more_itertools import flatten, argmin
from more_itertools.recipes import quantify

from tools.math import all_combinations  # type: ignore
from tools.time import timeit  # type: ignore


@dataclasses.dataclass
class Button:
    v: set[int]

    def __xor__(self, other):
        return Button(self.v ^ other.v)

    def __len__(self):
        return len(self.v)

    def __iter__(self):
        return iter(self.v)

    def __contains__(self, item):
        return item in self.v


@dataclasses.dataclass
class Joltage:
    v: list[int]

    def __len__(self):
        return len(self.v)

    def __iter__(self):
        return iter(self.v)

    def __getitem__(self, item):
        return self.v[item]

    def copy_and_reduce_joltage(self, buttons: Iterable[Button]) -> Joltage:
        joltage = Joltage(list(self.v))
        for button in buttons:
            for i in button.v:
                joltage.v[i] -= 1
        return joltage

    def is_depleted(self) -> bool:
        return not any(self.v)


@dataclasses.dataclass
class MachineInfo:
    buttons: list[Button]
    target_state: set[int]
    target_joltage: Joltage


def parse_inputs(file: PathLike) -> Iterable[MachineInfo]:
    def parse_target_state(it: str) -> set[int]:
        return set(i for i, c in enumerate(it[1:-1]) if c == "#")

    def parse_button(button_str: str) -> Iterable[int]:
        return (int(i) for i in button_str[1:-1].split(","))

    def parse_buttons(it: Iterable[str]) -> Iterable[Button]:
        for button_str in it:
            yield Button(set(parse_button(button_str)))

    with (open(file) as input):
        for row in input:
            sections = row.rstrip().split(' ')
            yield MachineInfo(list(parse_buttons(sections[1:-1])), parse_target_state(sections[0]), Joltage(list(parse_button(sections[-1]))))


def compute_fewest_button_presses(wiring: Iterable[MachineInfo]) -> int:
    def get_valid_button_presses(target_state: set[int], buttons: list[Button]) -> Iterable[Tuple[Button]]:
        return (comb for comb in all_combinations(buttons) if reduce(operator.xor, comb).v == target_state)

    return sum(min(map(len, get_valid_button_presses(info.target_state, info.buttons))) for info in wiring)


# def compute_fewest_joltage_button_presses(wiring: Iterable[MachineInfo]) -> int:
#     """
#     Most likely correct, but never finishes...
#     """
#     def get_valid_button_presses(target_joltage: Joltage, buttons: list[Button]) -> list[Button]:
#         print(f"{target_joltage=}")
#         max_jolt_idx = argmax(target_joltage)
#         max_jolt = target_joltage[max_jolt_idx]
#         max_buttons = list(b for b in buttons if max_jolt_idx in b)
#         other_buttons = list(b for b in buttons if max_jolt_idx not in b)
#         max_combinations = combinations_with_replacement(max_buttons, max_jolt)
#         other_combinations = all_combinations_with_replacement(other_buttons, max_jolt, include_empty_set=True)
#         all = (list(chain(*p)) for p in product(max_combinations, other_combinations))
#         min_comb = None
#         for comb in all:
#             if min_comb and len(comb) >= len(min_comb):
#                 continue
#             joltage = target_joltage.copy_and_reduce_joltage(comb)
#             if joltage.is_depleted():
#                 if not min_comb or len(comb) < len(min_comb):
#                     print(comb)
#                     min_comb = comb
#                     if len(comb) == max_jolt:
#                         break
#         for k, g in groupby(min_comb):
#             print(f"{len(list(g))} {k}")
#         return min_comb
#
#     with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
#         valid_presses = pool.map(len, (get_valid_button_presses(info.target_joltage, info.buttons) for info in wiring))
#         return sum(valid_presses)

@dataclasses.dataclass
class CombinationTracker:
    current_comb: list[Tuple[Button, ...]]
    min_comb: Tuple[Button, ...] | None = None
    current_comb_len: int = 0

    @contextlib.contextmanager
    def push_comb(self, comb: tuple[Button, ...]):
        self.current_comb.append(comb)
        self.current_comb_len += len(comb)
        yield None
        self.current_comb.pop()
        self.current_comb_len -= len(comb)


def compute_fewest_joltage_button_presses(wiring: Iterable[MachineInfo]) -> int:
    def find_leanest_buttons(target_joltage: Joltage, buttons: Iterable[Button]) -> tuple[None, None, None] | tuple[int, list[Button], list[Button]]:
        if target_joltage.is_depleted(): return None, None, None
        min_idx = argmin(quantify(i in b for b in buttons) if target_joltage[i] > 0 else sys.maxsize for i in range(len(target_joltage)))
        return min_idx, list(b for b in buttons if min_idx in b), list(b for b in buttons if min_idx not in b)

    def get_valid_button_presses(current_joltage: Joltage, current_buttons: list[Button], tracker: CombinationTracker) -> None:
        if any(i < 0 for i in current_joltage): return
        if current_joltage.is_depleted() and (not tracker.min_comb or tracker.current_comb_len < len(tracker.min_comb)):
            tracker.min_comb = tuple(flatten(tracker.current_comb))
            for k, g in groupby(tracker.min_comb):
                print(f"{len(list(g))} {k}")
            return
        if len(current_buttons) == 0:
            return

        # print(f"{current_joltage=} {current_buttons=}")
        index, buttons_leanest, buttons_rest = find_leanest_buttons(current_joltage, current_buttons)
        if index is None: return
        if tracker.min_comb and tracker.current_comb_len + current_joltage[index] >= len(tracker.min_comb): return

        leanest_var: list[Button] = cast(list[Button], buttons_leanest)
        for comb in combinations_with_replacement(leanest_var, current_joltage[index]):
            if tracker.min_comb and tracker.current_comb_len + current_joltage[index] >= len(tracker.min_comb): return
            joltage = current_joltage.copy_and_reduce_joltage(comb)
            with tracker.push_comb(comb):
                rest_var: list[Button] = cast(list[Button], buttons_rest)
                get_valid_button_presses(joltage, rest_var, tracker)

    @timeit
    def get_min_button_presses(target_joltage: Joltage, buttons: list[Button]) -> Tuple[Button, ...]:
        print(f"\n\n{target_joltage=}")
        tracker = CombinationTracker([])
        get_valid_button_presses(target_joltage, buttons, tracker)
        min_comb = cast(tuple[Button, ...], tracker.min_comb)
        return min_comb

    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
        valid_presses = pool.map(len, (get_min_button_presses(info.target_joltage, info.buttons) for info in wiring))
        return sum(valid_presses)
