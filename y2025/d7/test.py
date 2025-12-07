import os
import unittest

from y2025.d7.main import compute_splits, parse_inputs, compute_paths

TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), 'input_test.txt')
LIVE_FILENAME = os.path.join(os.path.dirname(__file__), 'input.txt')


def solve_part_one(file: os.PathLike):
    inputs = parse_inputs(file)
    total = compute_splits(inputs)
    return total

def solve_part_two(file: os.PathLike):
    inputs = parse_inputs(file)
    total = compute_paths(inputs)
    return total

class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(21, solve_part_one(TESTDATA_FILENAME))

    def test_part_one_live(self):
        self.assertEqual(1504, solve_part_one(LIVE_FILENAME))

    def test_part_two(self):
        self.assertEqual(40, solve_part_two(TESTDATA_FILENAME))

    def test_part_two_live(self):
        self.assertEqual(5137133207830, solve_part_two(LIVE_FILENAME))


if __name__ == "__main__":
    unittest.main()
