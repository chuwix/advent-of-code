import time
from BitArray2D import BitArray2D, godel
from y2025.d12.main import PartVariant, parse_inputs
import os


def place_bitwise(occupied: BitArray2D, variant: PartVariant, row: int, col: int, place: bool = True) -> None:
    """Bitwise operations version."""
    target_region = occupied[godel(row, col):godel(row + variant.array.rows, col + variant.array.columns)]

    if place:
        occupied[godel(row, row + variant.array.rows):godel(col, col + variant.array.columns)] = target_region | variant.array
    else:
        occupied[godel(row, row + variant.array.rows):godel(col, col + variant.array.columns)] = target_region & ~variant.array


def place_loop(occupied: BitArray2D, variant: PartVariant, row: int, col: int, place: bool = True) -> None:
    """Loop-based version."""
    value = 1 if place else 0
    for r in range(variant.array.rows):
        for c in range(variant.array.columns):
            if variant.array[godel(r, c)]:
                occupied[row + r, col + c] = value


def benchmark():
    test_file = os.path.join('y2025/d12', 'input_test.txt')
    parts, _ = parse_inputs(test_file)

    variant = parts[0].variants[0]

    print(f"Testing placement with variant of size {variant.array.rows}x{variant.array.columns}")
    print()

    # Benchmark bitwise version
    start = time.time()
    for _ in range(1000):
        occupied = BitArray2D(rows=12, columns=5)
        place_bitwise(occupied, variant, 1, 1, place=True)
        place_bitwise(occupied, variant, 1, 1, place=False)
    bitwise_time = time.time() - start

    # Benchmark loop version
    start = time.time()
    for _ in range(1000):
        occupied = BitArray2D(rows=12, columns=5)
        place_loop(occupied, variant, 1, 1, place=True)
        place_loop(occupied, variant, 1, 1, place=False)
    loop_time = time.time() - start

    print(f"Bitwise version: {bitwise_time:.4f}s ({2000 / bitwise_time:.0f} ops/sec)")
    print(f"Loop version:    {loop_time:.4f}s ({2000 / loop_time:.0f} ops/sec)")
    print(f"Speedup: {bitwise_time / loop_time:.2f}x")

    # Verify both give same results
    print("\nVerifying correctness...")
    occupied1 = BitArray2D(rows=12, columns=5)
    occupied2 = BitArray2D(rows=12, columns=5)

    place_bitwise(occupied1, variant, 1, 1, place=True)
    place_loop(occupied2, variant, 1, 1, place=True)

    for r in range(occupied1.rows):
        for c in range(occupied1.columns):
            if occupied1[godel(r, c)] != occupied2[godel(r, c)]:
                print(f"MISMATCH at ({r}, {c}): Bitwise={occupied1[godel(r, c)]}, Loop={occupied2[godel(r, c)]}")
                return
    print("✓ All results match")


if __name__ == "__main__":
    benchmark()
