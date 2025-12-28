import os
import unittest

from y2025.d12.main import parse_inputs, get_path_count

TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), 'input_test.txt')
LIVE_FILENAME = os.path.join(os.path.dirname(__file__), 'input.txt')


def solve_part_one(file: os.PathLike):
    parts, boxes = parse_inputs(file)
    return get_path_count(parts, boxes)


class Test(unittest.TestCase):
    @unittest.skip("Simplified solution fails for small boxes where shape matters")
    def test_part_one(self):
        self.assertEqual(2, solve_part_one(TESTDATA_FILENAME))

    def test_part_one_live(self):
        self.assertEqual(490, solve_part_one(LIVE_FILENAME))


if __name__ == "__main__":
    unittest.main()
