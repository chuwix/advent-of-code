import os
import unittest

from y2025.d12.main import parse_inputs, get_path_count

TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), 'input_test.txt')
LIVE_FILENAME = os.path.join(os.path.dirname(__file__), 'input.txt')


def solve_part_one(file: os.PathLike):
    parts, boxes = parse_inputs(file)
    total = get_path_count(parts, boxes)
    return total


# def solve_part_two(file: os.PathLike):
#     rack = parse_inputs(file)
#     total = get_path_count(rack, rack.devices["svr"], rack.devices["out"], {rack.devices["fft"], rack.devices["dac"]})
#     return total


class Test(unittest.TestCase):
    def test_part_one(self):
        self.assertEqual(2, solve_part_one(TESTDATA_FILENAME))

    # def test_part_one_live(self):
    #     self.assertEqual(0, solve_part_one(LIVE_FILENAME))

    # def test_part_two(self):
    #     self.assertEqual(0, solve_part_two(TESTDATA_FILENAME))
    #
    # def test_part_two_live(self):
    #     self.assertEqual(0, solve_part_two(LIVE_FILENAME))


if __name__ == "__main__":
    unittest.main()
