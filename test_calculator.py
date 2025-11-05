import unittest
from calculator import add, subtract, product

class TestCalculator(unittest.TestCase):
    """Test cases for the calculator functions."""

    # --- Positive Test Cases (Successful Operations) ---
    def test_add_success(self):
        self.assertEqual(add(5, 3), 8)
        self.assertEqual(add(1, 99), 100)

    def test_subtract_success(self):
        self.assertEqual(subtract(10, 4), 6)
        self.assertEqual(subtract(1, 1), 0)
        self.assertEqual(subtract(2, 1), 1)

    def test_product_success(self):
        self.assertEqual(product(2, 6), 12)
        self.assertEqual(product(10, 10), 100)

    # --- Negative Test Cases (Input Validation) ---
    def test_negative_input(self):
        # Should fail if input is negative
        with self.assertRaisesRegex(ValueError, "Inputs must be positive integers."):
            add(-1, 5)

    def test_zero_input(self):
        # Should fail if input is zero
        with self.assertRaisesRegex(ValueError, "Inputs must be positive integers."):
            subtract(10, 0)

    def test_non_integer_input(self):
        # Should fail if input is not an integer
        with self.assertRaisesRegex(ValueError, "Inputs must be positive integers."):
            product(2.5, 4)

# To run tests locally:
# if __name__ == '__main__':
#     unittest.main()