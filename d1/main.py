from typing import Iterable
from functools import reduce
from io import open


def parse(it: Iterable[str]) -> Iterable[int]:
    for s in it:
        s = s.replace("R", "").replace("L", "-")
        yield int(s)


def solve_part_one(dial: int, commands: Iterable[int]) -> tuple[int, int]:
    jackpots = 0

    for i in commands:
        # print(i)
        dial = (dial + i) % 100

        if dial == 0:
            jackpots += 1

    return dial, jackpots


def solve_part_two(dial: int, commands: Iterable[int]) -> tuple[int, int]:
    jackpots = 0

    for i in commands:
        # print(i)
        was_null = dial == 0
        full_rotations = int(i / 100)
        jackpots += abs(full_rotations)
        i -= full_rotations * 100 # correction for sum != dial check
        sum = dial + i
        dial = sum % 100

        if dial == 0:
            jackpots += 1
        elif sum != dial and not was_null:
            jackpots += 1

    return dial, jackpots


with (open("input.txt") as input):
    lines = input.readlines()
    commands = parse(lines)

    # print(solve_part_one(50, commands))
    print(solve_part_two(50, commands))
