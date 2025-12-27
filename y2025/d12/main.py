import dataclasses
from typing import Iterable, Tuple

from BitArray2D import BitArray2D, godel
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


def get_bounding_box(ba: BitArray2D) -> tuple[int, int, int, int]:
    """Get bounding box of 1s in BitArray2D.

    Returns (min_row, min_col, max_row, max_col).
    Returns (0, 0, 0, 0) if array is empty.
    """
    min_row, min_col = ba.rows, ba.columns
    max_row, max_col = -1, -1

    for row in range(ba.rows):
        for col in range(ba.columns):
            if ba[godel(row, col)]:
                min_row = min(min_row, row)
                min_col = min(min_col, col)
                max_row = max(max_row, row)
                max_col = max(max_col, col)

    if max_row == -1:  # Empty array
        return (0, 0, 0, 0)

    return (min_row, min_col, max_row, max_col)


@dataclasses.dataclass(frozen=True)
class PartVariant:
    """A specific orientation of a part with pre-computed metadata."""
    array: BitArray2D
    cell_count: int
    min_row: int
    min_col: int
    width: int
    height: int

    @staticmethod
    def from_array(ba: BitArray2D) -> 'PartVariant':
        """Create a PartVariant from a BitArray2D with computed metadata."""
        cell_count = count_ones(ba)
        min_row, min_col, max_row, max_col = get_bounding_box(ba)
        width = max_col - min_col + 1 if max_col >= 0 else 0
        height = max_row - min_row + 1 if max_row >= 0 else 0
        return PartVariant(ba, cell_count, min_row, min_col, width, height)


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

        # Convert to PartVariants with metadata
        variants = [
            PartVariant.from_array(ba)
            for ba in [r0, r90, r180, r270, rev0, rev90, rev180, rev270]
        ]

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
        rows = peekable(f)  # Create peekable once
        parts = parse_parts(rows)
        boxes = list(parse_boxes(rows))
        return parts, boxes


def try_fit_all_parts(box: Box, parts: dict[int, Part]) -> bool:
    """Try to fit all required parts into the box.

    Returns True if all parts can be placed without overlaps.
    """
    # Build work list: expand quantities into individual parts
    work_list: list[Part] = []
    for part_id, count in box.fits.items():
        for _ in range(count):
            work_list.append(parts[part_id])

    # If no parts to place, it's a success
    if not work_list:
        return True

    # Initialize empty occupied map
    occupied = BitArray2D(rows=box.array.rows, columns=box.array.columns)

    # Calculate initial empty count
    empty_count = box.array.rows * box.array.columns

    # Start backtracking
    return backtrack(occupied, work_list, empty_count, box.array.rows, box.array.columns)


def backtrack(occupied: BitArray2D, remaining: list[Part], empty_count: int, box_rows: int, box_cols: int) -> bool:
    """Recursive backtracking to place all parts.

    Args:
        occupied: Current occupancy map (modified in-place)
        remaining: Parts still to place
        empty_count: Number of empty cells remaining
        box_rows: Height of the box
        box_cols: Width of the box

    Returns:
        True if all remaining parts can be placed
    """
    # Base case: no more parts to place
    if not remaining:
        return True

    # Get current part to place
    part = remaining[0]

    # Pruning: check if we have enough space for the smallest variant
    min_size = min(v.cell_count for v in part.variants)
    if empty_count < min_size:
        return False

    # Pruning: check if we have enough space for all remaining parts
    total_needed = sum(min(v.cell_count for v in p.variants) for p in remaining)
    if empty_count < total_needed:
        return False

    # Try each variant
    for variant in part.variants:
        # Skip if this variant is too large
        if variant.height > box_rows or variant.width > box_cols:
            continue

        # Row-major scan: try positions left-to-right, top-to-bottom
        for row in range(box_rows - variant.height + 1):
            for col in range(box_cols - variant.width + 1):
                if can_place_at(occupied, variant, row, col):
                    # Place the part (in-place)
                    place_part_at_inplace(occupied, variant, row, col, place=True)
                    new_empty = empty_count - variant.cell_count

                    # Recursively try to place remaining parts
                    if backtrack(occupied, remaining[1:], new_empty, box_rows, box_cols):
                        return True

                    # Backtrack: remove the part (in-place)
                    place_part_at_inplace(occupied, variant, row, col, place=False)

    # No valid placement found
    return False


def can_place_at(occupied: BitArray2D, variant: PartVariant, row: int, col: int) -> bool:
    """Check if a part variant can be placed at the given position without collision."""
    # Check each cell of the variant's bounding box
    for r in range(variant.height):
        for c in range(variant.width):
            variant_row = variant.min_row + r
            variant_col = variant.min_col + c
            box_row = row + r
            box_col = col + c

            # Check if the variant has a filled cell at this position
            if variant.array[godel(variant_row, variant_col)]:
                # Check if this position is already occupied
                if occupied[godel(box_row, box_col)]:
                    return False
    return True


def place_part_at_inplace(occupied: BitArray2D, variant: PartVariant, row: int, col: int, place: bool = True) -> None:
    """Place or remove a part variant at the given position in-place.

    Args:
        occupied: The occupancy map to modify
        variant: The part variant to place/remove
        row: Row position to place at
        col: Column position to place at
        place: If True, place the part (set to 1). If False, remove it (set to 0).
    """
    value = 1 if place else 0

    # Place/remove each filled cell of the variant
    for r in range(variant.height):
        for c in range(variant.width):
            variant_row = variant.min_row + r
            variant_col = variant.min_col + c
            box_row = row + r
            box_col = col + c

            if variant.array[godel(variant_row, variant_col)]:
                occupied[box_row, box_col] = value


def get_path_count(parts: dict[int, Part], boxes: list[Box]) -> int:
    """Count how many boxes can fit all their required parts."""
    count = 0
    for box in boxes:
        if try_fit_all_parts(box, parts):
            count += 1
    return count
