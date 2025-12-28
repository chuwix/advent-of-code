import dataclasses
from typing import Iterable

from BitArray2D import BitArray2D, godel
from more_itertools import quantify
from more_itertools.more import peekable

from tools.datastructures.bitarray2d import rotate, flip


def count_ones(ba: BitArray2D) -> int:
    """Count the number of 1s in a BitArray2D."""
    count = 0
    for row in range(ba.rows):
        for col in range(ba.columns):
            if ba[godel(row, col)]:
                count += 1
    return count


@dataclasses.dataclass(frozen=True)
class PartVariant:
    """A specific orientation of a part."""
    array: BitArray2D
    cell_count: int

    @staticmethod
    def from_array(ba: BitArray2D) -> 'PartVariant':
        """Create a PartVariant from a BitArray2D."""
        cell_count = count_ones(ba)
        return PartVariant(ba, cell_count)


@dataclasses.dataclass(frozen=True)
class Part:
    variants: list[PartVariant]

    @staticmethod
    def from_template(template: BitArray2D) -> 'Part':
        r0 = template
        r90 = rotate(r0)
        r180 = rotate(r90)
        r270 = rotate(r180)
        rev0 = flip(template)
        rev90 = rotate(rev0)
        rev180 = rotate(rev90)
        rev270 = rotate(rev180)

        all_orientations = [r0, r90, r180, r270, rev0, rev90, rev180, rev270]
        variants = [PartVariant.from_array(ba) for ba in all_orientations]

        return Part(variants)

    def __str__(self):
        return f"Part(\n{',\n'.join(str(v.array) for v in self.variants)})"


@dataclasses.dataclass
class Box:
    array: BitArray2D
    fits: dict[int, int]

    def __repr__(self):
        return f"Box({self.array.rows}x{self.array.columns},{self.fits})"


def parse_inputs(file) -> tuple[dict[int, Part], list[Box]]:
    def parse_parts(rows) -> dict[int, Part]:
        res = {}

        while "x" not in rows.peek():
            idx = int(next(rows).split(":", maxsplit=1)[0])
            ba = BitArray2D(rows=3, columns=3)

            for i, line in enumerate(rows):
                line = line.strip().replace("#", "1").replace(".", "0")
                if not line:
                    break
                ba[godel(i, i + 1):godel(0, len(line))] = BitArray2D(bitstring=line)

            res[idx] = Part.from_template(ba)

        return res

    def parse_boxes(rows) -> Iterable[Box]:
        for line in rows:
            line = line.strip().split(":", maxsplit=1)
            dims = line[0].split("x", maxsplit=1)
            counts = {i: int(c) for i, c in enumerate(line[1].split())}
            yield Box(BitArray2D(rows=int(dims[0]), columns=int(dims[1])), counts)

    with open(file) as f:
        rows = peekable(f)
        parts = parse_parts(rows)
        boxes = list(parse_boxes(rows))
        return parts, boxes


def try_fit_all_parts(box: Box, parts: dict[int, Part]) -> bool:
    """Check if parts fit in available space."""
    total_cells_needed = sum(
        parts[part_id].variants[0].cell_count * count
        for part_id, count in box.fits.items()
    )
    return total_cells_needed <= box.array.rows * box.array.columns


def get_path_count(parts: dict[int, Part], boxes: list[Box]) -> int:
    """Count how many boxes can fit all their required parts."""
    return quantify(try_fit_all_parts(box, parts) for box in boxes)
