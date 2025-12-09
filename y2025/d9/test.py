import os
import unittest

from y2025.d9.main import get_largest_square, parse_inputs

TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), 'input_test.txt')
LIVE_FILENAME = os.path.join(os.path.dirname(__file__), 'input.txt')

def solve_part_one(file: os.PathLike):
    inputs = parse_inputs(file)
    total = get_largest_square(inputs)
    return total

def solve_part_two(file: os.PathLike):
    pass

class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(50, solve_part_one(TESTDATA_FILENAME))

    def test_part_one_live(self):
        self.assertEqual(4755429952, solve_part_one(LIVE_FILENAME))

    def test_part_two(self):
        self.assertEqual(25272, solve_part_two(TESTDATA_FILENAME))

    def test_part_two_live(self):
        self.assertEqual(8133642976, solve_part_two(LIVE_FILENAME))


if __name__ == "__main__":
    unittest.main()
