import dataclasses
from typing import Iterable, Tuple

from BitArray2D import BitArray2D, godel
from more_itertools.more import peekable

from tools.datastructures.bitarray2d import rotate, flip


@dataclasses.dataclass(frozen=True)
class Part:
    variants: list[BitArray2D]

    @staticmethod
    def from_template(template: BitArray2D) -> Part:
        r0 = template
        r90 = rotate(r0)
        r180 = rotate(r90)
        r270 = rotate(r180)
        rev0 = flip(template)
        rev90 = rotate(rev0)
        rev180 = rotate(rev90)
        rev270 = rotate(rev180)
        return Part([r0, r90, r180, r270, rev0, rev90, rev180, rev270])

    def __str__(self):
        return f"Part(\n{',\n'.join(map(str, self.variants))})"


@dataclasses.dataclass
class Box:
    array: BitArray2D
    fits: dict[int, int]

    def __repr__(self):
        return f"Box({self.array.rows}x{self.array.columns},{self.fits})"


def parse_inputs(file) -> tuple[dict[int, Part], list[Box]]:
    def parse_parts(rows: Iterable[str]) -> dict[int, Part]:
        rows = peekable(rows)
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

    def parse_boxes(rows: Iterable[str]) -> Iterable[Box]:
        for line in rows:
            line = line.strip().split(":", maxsplit=1)
            dims = line[0].split("x", maxsplit=1)
            counts = {i: int(c) for i, c in enumerate(line[1].split())}
            yield Box(BitArray2D(rows=int(dims[0]), columns=int(dims[1])), counts)

    with open(file) as f:
        parts = parse_parts(f)
        boxes = list(parse_boxes(f))
        return parts, boxes


def try_fit_all_parts(box: Box, parts: dict[int, Part]) -> bool:

    return True


def get_path_count(parts: dict[int, Part], boxes: list[Box]) -> int:
    for box in boxes:
        if try_fit_all_parts(box, parts):
            return 1
    return 0
