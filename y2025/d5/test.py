import os
import unittest

from y2025.d5.main import solve_part_one, solve_part_two, get_ranges_and_ids

TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), 'input_test.txt')


class Test(unittest.TestCase):
    def test_part_one(self):
        ranges, ids = get_ranges_and_ids(TESTDATA_FILENAME)
        fresh_ids = solve_part_one(ranges, ids)
        # print(list(invalid_ids))
        self.assertEqual(3, fresh_ids)

    def test_part_two(self):
        ranges, _ = get_ranges_and_ids(TESTDATA_FILENAME)
        fresh_ids = solve_part_two(ranges)
        # print(list(invalid_ids))
        self.assertEqual(14, fresh_ids)


if __name__ == "__main__":
    unittest.main()
