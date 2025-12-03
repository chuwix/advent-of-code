import os
import pathlib
import unittest

from y2025.d3.main import solve, get_lines

TESTDATA_FILENAME = pathlib.Path(os.path.join(os.path.dirname(__file__), 'input_test.txt'))


class Test(unittest.TestCase):
    def test_part_one(self):
        battery_inputs = get_lines(TESTDATA_FILENAME)
        maxes = solve(battery_inputs, 2)
        # print(list(maxes))
        self.assertEqual(357, sum(maxes))

    def test_part_two(self):
        battery_inputs = get_lines(TESTDATA_FILENAME)
        maxes = solve(battery_inputs, 12)
        # print(list(maxes))
        self.assertEqual(3121910778619, sum(maxes))


if __name__ == "__main__":
    unittest.main()
