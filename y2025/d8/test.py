import os
import unittest

from y2025.d8.main import compute_junctions, parse_inputs, compute_last_junction

TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), 'input_test.txt')
LIVE_FILENAME = os.path.join(os.path.dirname(__file__), 'input.txt')

def solve_part_one(file: os.PathLike, closest_points: int, circuits_to_mult: int):
    inputs = parse_inputs(file)
    total = compute_junctions(inputs, closest_points, circuits_to_mult)
    return total

def solve_part_two(file: os.PathLike, closest_points: int, circuits_to_mult: int):
    inputs = parse_inputs(file)
    total = compute_last_junction(inputs, closest_points, circuits_to_mult)
    return total

class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(40, solve_part_one(TESTDATA_FILENAME, 10, 3))

    def test_part_one_live(self):
        self.assertEqual(32103, solve_part_one(LIVE_FILENAME, 1000, 3))

    def test_part_two(self):
        self.assertEqual(25272, solve_part_two(TESTDATA_FILENAME, 10, 3))

    def test_part_two_live(self):
        self.assertEqual(8133642976, solve_part_two(LIVE_FILENAME, 1000, 3))


if __name__ == "__main__":
    unittest.main()
