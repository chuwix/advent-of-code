import os
import unittest

from tools.mypyc import ensure_built

ensure_built()
from y2025.d10.main import compute_fewest_button_presses, parse_inputs, compute_fewest_joltage_button_presses

TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), 'input_test.txt')
LIVE_FILENAME = os.path.join(os.path.dirname(__file__), 'input.txt')


def solve_part_one(file: os.PathLike):
    wiring = parse_inputs(file)
    total = compute_fewest_button_presses(wiring)
    return total


def solve_part_two(file: os.PathLike):
    wiring = parse_inputs(file)
    total = compute_fewest_joltage_button_presses(wiring)
    return total


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(7, solve_part_one(TESTDATA_FILENAME))

    def test_part_one_live(self):
        self.assertEqual(399, solve_part_one(LIVE_FILENAME))

    def test_part_two(self):
        self.assertEqual(33, solve_part_two(TESTDATA_FILENAME))

    def test_part_two_live(self):
        self.assertEqual(15631, solve_part_two(LIVE_FILENAME))


if __name__ == "__main__":
    unittest.main()
