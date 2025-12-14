import os
import unittest

from y2025.d11.main import parse_inputs, get_path_count

TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), 'input_test.txt')
TESTDATA_P2_FILENAME = os.path.join(os.path.dirname(__file__), 'input_test_p2.txt')
LIVE_FILENAME = os.path.join(os.path.dirname(__file__), 'input.txt')


def solve_part_one(file: os.PathLike):
    rack = parse_inputs(file)
    total = get_path_count(rack, rack.devices["you"], rack.devices["out"])
    return total


def solve_part_two(file: os.PathLike):
    rack = parse_inputs(file)
    total = get_path_count(rack, rack.devices["svr"], rack.devices["out"], {rack.devices["fft"], rack.devices["dac"]})
    return total


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(5, solve_part_one(TESTDATA_FILENAME))

    def test_part_one_live(self):
        self.assertEqual(788, solve_part_one(LIVE_FILENAME))

    def test_part_two(self):
        self.assertEqual(2, solve_part_two(TESTDATA_P2_FILENAME))

    def test_part_two_live(self):
        self.assertEqual(316291887968000, solve_part_two(LIVE_FILENAME))


if __name__ == "__main__":
    unittest.main()
