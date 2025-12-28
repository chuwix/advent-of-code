import time
from BitArray2D import BitArray2D, godel
from y2025.d12.main import PartVariant, parse_inputs
import os


def can_place_at_xor(occupied: BitArray2D, variant: PartVariant, row: int, col: int) -> bool:
    """XOR-based collision detection."""
    target_region = occupied[godel(row, col):godel(row + variant.array.rows, col + variant.array.columns)]
    return target_region ^ variant.array == variant.array


def can_place_at_loop(occupied: BitArray2D, variant: PartVariant, row: int, col: int) -> bool:
    """Loop-based collision detection."""
    for r in range(variant.array.rows):
        for c in range(variant.array.columns):
            if variant.array[godel(r, c)]:
                if occupied[godel(row + r, col + c)]:
                    return False
    return True


def benchmark():
    test_file = os.path.join('y2025/d12', 'input_test.txt')
    parts, boxes = parse_inputs(test_file)

    # Create a test scenario
    occupied = BitArray2D(rows=12, columns=5)
    occupied[0, 0] = 1
    occupied[5, 2] = 1

    variant = parts[0].variants[0]

    # Test positions (only valid ones where variant fits)
    positions = [
        (r, c)
        for r in range(occupied.rows - variant.array.rows + 1)
        for c in range(occupied.columns - variant.array.columns + 1)
    ]

    print(f"Testing {len(positions)} positions with variant of size {variant.array.rows}x{variant.array.columns}")
    print()

    # Benchmark XOR version
    start = time.time()
    for _ in range(1000):
        for row, col in positions:
            can_place_at_xor(occupied, variant, row, col)
    xor_time = time.time() - start

    # Benchmark loop version
    start = time.time()
    for _ in range(1000):
        for row, col in positions:
            can_place_at_loop(occupied, variant, row, col)
    loop_time = time.time() - start

    print(f"XOR version:  {xor_time:.4f}s ({len(positions) * 1000 / xor_time:.0f} calls/sec)")
    print(f"Loop version: {loop_time:.4f}s ({len(positions) * 1000 / loop_time:.0f} calls/sec)")
    print(f"Speedup: {loop_time / xor_time:.2f}x")

    # Verify both give same results
    print("\nVerifying correctness...")
    for row, col in positions:
        xor_result = can_place_at_xor(occupied, variant, row, col)
        loop_result = can_place_at_loop(occupied, variant, row, col)
        if xor_result != loop_result:
            print(f"MISMATCH at ({row}, {col}): XOR={xor_result}, Loop={loop_result}")
            return
    print("✓ All results match")


if __name__ == "__main__":
    benchmark()
