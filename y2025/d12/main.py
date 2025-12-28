import dataclasses

from more_itertools import quantify
from more_itertools.more import peekable


@dataclasses.dataclass
class Box:
    rows: int
    cols: int
    fits: dict[int, int]

    def __repr__(self):
        return f"Box({self.rows}x{self.cols},{self.fits})"


def parse_inputs(file) -> tuple[dict[int, int], list[Box]]:
    def parse_parts(rows) -> dict[int, int]:
        res = {}
        while "x" not in rows.peek():
            idx = int(next(rows).split(":", maxsplit=1)[0])
            cell_count = 0
            for line in rows:
                line = line.strip()
                if not line:
                    break
                cell_count += line.count('#')
            res[idx] = cell_count
        return res

    def parse_boxes(rows) -> list[Box]:
        boxes = []
        for line in rows:
            parts = line.strip().split(":", maxsplit=1)
            dims = parts[0].split("x")
            counts = {i: int(c) for i, c in enumerate(parts[1].split())}
            boxes.append(Box(int(dims[0]), int(dims[1]), counts))
        return boxes

    with open(file) as f:
        rows = peekable(f)
        parts = parse_parts(rows)
        boxes = parse_boxes(rows)
        return parts, boxes


def try_fit_all_parts(box: Box, parts: dict[int, int]) -> bool:
    """Check if parts fit in available space."""
    total_cells_needed = sum(
        parts[part_id] * count
        for part_id, count in box.fits.items()
    )
    return total_cells_needed <= box.rows * box.cols


def get_path_count(parts: dict[int, int], boxes: list[Box]) -> int:
    """Count how many boxes can fit all their required parts."""
    return quantify(try_fit_all_parts(box, parts) for box in boxes)
