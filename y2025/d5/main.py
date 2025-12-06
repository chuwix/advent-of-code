from dataclasses import dataclass
from io import open
from os import PathLike


@dataclass
class Range:
    lower: int
    upper: int

    def contains(self, id: int) -> bool:
        return self.lower <= id <= self.upper


def parse(s: str) -> Range:
    vals = s.split("-", 2)
    return Range(int(vals[0]), int(vals[1]))


def get_ranges_and_ids(file: PathLike[str]) -> tuple[list[Range], list[int]]:
    ranges, ids = [], []

    with (open(file) as input):
        for row in input:
            if row.isspace():
                break
            ranges.append(parse(row))

        for row in input:
            ids.append(int(row))

    return ranges, ids


def is_overlap_sorted(smaller: Range, latter: Range) -> bool:
    return latter.lower <= smaller.upper


def merge_ranges(ranges: list[Range]) -> list[Range]:
    ranges.sort(key=lambda r: r.lower)
    ranges_iter = iter(ranges)
    merged_ranges = [next(ranges_iter)]

    for range in ranges:
        last_range = merged_ranges[-1]

        if is_overlap_sorted(last_range, range):
            merged_ranges[-1].upper = max(last_range.upper, range.upper)
        else:
            merged_ranges.append(range)

    return merged_ranges


def count_fresh_ids(merged_ranges: list[Range], ids: list[int]) -> int:
    ids.sort()
    fresh_count = 0
    merged_ranges_iter = iter(merged_ranges)
    current_range = next(merged_ranges_iter)

    for id in ids:
        while current_range.upper < id:
            try:
                current_range = next(merged_ranges_iter)
            except StopIteration:
                break

        if current_range.contains(id):
            fresh_count += 1

    return fresh_count


def solve_part_one(ranges: list[Range], ids: list[int]) -> int:
    merged_ranges = merge_ranges(ranges)
    return count_fresh_ids(merged_ranges, ids)


def solve_part_two(ranges: list[Range]) -> int:
    merged_ranges = merge_ranges(ranges)
    return sum(r.upper - r.lower + 1 for r in merged_ranges)
