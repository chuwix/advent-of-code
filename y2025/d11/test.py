import os
import unittest

from y2025.d11.main import get_path_count_to_out, parse_inputs

TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), 'input_test.txt')
LIVE_FILENAME = os.path.join(os.path.dirname(__file__), 'input.txt')


def solve_part_one(file: os.PathLike):
    rack = parse_inputs(file)
    total = get_path_count_to_out(rack, rack.devices["you"], rack.devices["out"])
    return total


def solve_part_two(file: os.PathLike):
    rack = parse_inputs(file)
    total = get_path_count_to_out(rack, rack.devices["you"], rack.devices["out"])
    return total


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(5, solve_part_one(TESTDATA_FILENAME))

    def test_part_one_live(self):
        self.assertEqual(788, solve_part_one(LIVE_FILENAME))

    def test_part_two(self):
        self.assertEqual(2, solve_part_two(TESTDATA_FILENAME))

    # def test_part_two_live(self):
    #     self.assertEqual(0, solve_part_two(LIVE_FILENAME))


if __name__ == "__main__":
    unittest.main()
