import os
import unittest

from y2025.d6.main import compute_totals_sum, parse_lists_and_ops, parse_lists_and_ops_columns

TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), 'input_test.txt')
LIVE_FILENAME = os.path.join(os.path.dirname(__file__), 'input.txt')


def solve_part_one(file: os.PathLike):
    ops, inputs = parse_lists_and_ops(file)
    total = compute_totals_sum(ops, inputs)
    return total

def solve_part_two(file: os.PathLike):
    ops, inputs = parse_lists_and_ops_columns(file)
    total = compute_totals_sum(ops, [inputs])
    return total


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(4277556, solve_part_one(TESTDATA_FILENAME))

    def test_part_one_live(self):
        self.assertEqual(5381996914800, solve_part_one(LIVE_FILENAME))

    def test_part_two(self):
        self.assertEqual(3263827, solve_part_two(TESTDATA_FILENAME))

    def test_part_two_live(self):
        self.assertEqual(9627174150897, solve_part_two(LIVE_FILENAME))


if __name__ == "__main__":
    unittest.main()
