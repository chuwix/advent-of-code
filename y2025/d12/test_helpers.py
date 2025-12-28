import unittest
from BitArray2D import BitArray2D, godel
from y2025.d12.main import PartVariant, can_place_at, place_part_at_inplace


class TestHelperFunctions(unittest.TestCase):
    def test_can_place_at_empty_target(self):
        """Test placing variant on empty target."""
        occupied = BitArray2D(rows=4, columns=4)

        variant_array = BitArray2D(rows=2, columns=2)
        variant_array[0, 0] = 1
        variant_array[0, 1] = 1
        variant = PartVariant(variant_array, 2)

        self.assertTrue(can_place_at(occupied, variant, 0, 0))
        self.assertTrue(can_place_at(occupied, variant, 1, 1))

    def test_can_place_at_with_collision(self):
        """Test detecting collision."""
        occupied = BitArray2D(rows=4, columns=4)
        occupied[0, 0] = 1

        variant_array = BitArray2D(rows=2, columns=2)
        variant_array[0, 0] = 1
        variant_array[0, 1] = 1
        variant = PartVariant(variant_array, 2)

        self.assertFalse(can_place_at(occupied, variant, 0, 0))

    def test_can_place_at_without_collision(self):
        """Test placing variant next to occupied cells."""
        occupied = BitArray2D(rows=4, columns=4)
        occupied[0, 0] = 1

        variant_array = BitArray2D(rows=2, columns=2)
        variant_array[0, 0] = 1
        variant_array[0, 1] = 1
        variant = PartVariant(variant_array, 2)

        self.assertTrue(can_place_at(occupied, variant, 1, 1))
        self.assertTrue(can_place_at(occupied, variant, 0, 2))

    def test_place_part_at_inplace_place(self):
        """Test placing a variant."""
        occupied = BitArray2D(rows=4, columns=4)

        variant_array = BitArray2D(rows=2, columns=2)
        variant_array[0, 0] = 1
        variant_array[0, 1] = 1
        variant = PartVariant(variant_array, 2)

        place_part_at_inplace(occupied, variant, 1, 1, place=True)

        self.assertTrue(occupied[godel(1, 1)])
        self.assertTrue(occupied[godel(1, 2)])
        self.assertFalse(occupied[godel(0, 0)])
        self.assertFalse(occupied[godel(2, 1)])

    def test_place_part_at_inplace_remove(self):
        """Test removing a variant."""
        occupied = BitArray2D(rows=4, columns=4)
        occupied[1, 1] = 1
        occupied[1, 2] = 1
        occupied[0, 0] = 1

        variant_array = BitArray2D(rows=2, columns=2)
        variant_array[0, 0] = 1
        variant_array[0, 1] = 1
        variant = PartVariant(variant_array, 2)

        place_part_at_inplace(occupied, variant, 1, 1, place=False)

        self.assertFalse(occupied[godel(1, 1)])
        self.assertFalse(occupied[godel(1, 2)])
        self.assertTrue(occupied[godel(0, 0)])

    def test_xor_collision_detection_logic(self):
        """Test the XOR-based collision detection logic."""
        # Empty target: target ^ variant == variant (no collision)
        target_empty = BitArray2D(rows=2, columns=2)
        variant = BitArray2D(rows=2, columns=2)
        variant[0, 0] = 1
        variant[0, 1] = 1

        result_empty = target_empty ^ variant
        self.assertEqual(result_empty, variant)

        # Collision: target ^ variant != variant
        target_collision = BitArray2D(rows=2, columns=2)
        target_collision[0, 0] = 1

        result_collision = target_collision ^ variant
        self.assertNotEqual(result_collision, variant)

        # No collision: target has bits but not overlapping
        target_no_collision = BitArray2D(rows=2, columns=2)
        target_no_collision[1, 0] = 1

        result_no_collision = target_no_collision ^ variant
        self.assertNotEqual(result_no_collision, variant)


if __name__ == "__main__":
    unittest.main()
