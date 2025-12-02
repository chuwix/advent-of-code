import os
import unittest

from d1.main import solve_part_one, solve_part_two, get_commands

TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), 'input_test.txt')


class Test(unittest.TestCase):
    def test_part_one(self):
        _, jackpots = solve_part_one(50, get_commands(TESTDATA_FILENAME))
        self.assertEqual(3, jackpots)

    def test_part_two(self):
        _, jackpots = solve_part_two(50, get_commands(TESTDATA_FILENAME))
        self.assertEqual(6, jackpots)


if __name__ == "__main__":
    unittest.main()
