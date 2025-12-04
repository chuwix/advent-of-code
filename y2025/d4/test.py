import os
import pathlib
import unittest

from y2025.d4.main import solve_part_one, get_lines, solve_part_two

TESTDATA_FILENAME = pathlib.Path(os.path.join(os.path.dirname(__file__), 'input_test.txt'))


class Test(unittest.TestCase):
    def test_part_one(self):
        inputs = get_lines(TESTDATA_FILENAME)
        rolls = solve_part_one(list(inputs), 1, 3)
        # print(list(maxes))
        self.assertEqual(13, rolls)

    def test_part_two(self):
        inputs = get_lines(TESTDATA_FILENAME)
        rolls = solve_part_two(list(inputs), 1, 3)
        # print(list(maxes))
        self.assertEqual(43, rolls)


if __name__ == "__main__":
    unittest.main()
