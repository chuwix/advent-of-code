import os
import unittest

from y2025.d2.main import solve_part_one, solve_part_two, get_ranges

TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), 'input_test.txt')


class Test(unittest.TestCase):
    def test_part_one(self):
        ranges = get_ranges(TESTDATA_FILENAME)
        invalid_ids = solve_part_one(ranges)
        # print(list(invalid_ids))
        self.assertEqual(1227775554, sum(invalid_ids))

    def test_part_two(self):
        ranges = get_ranges(TESTDATA_FILENAME)
        invalid_ids = solve_part_two(ranges)
        # print(list(invalid_ids))
        self.assertEqual(4174379265, sum(invalid_ids))


if __name__ == "__main__":
    unittest.main()
