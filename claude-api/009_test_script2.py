import unittest
from009_test_script import calculate_pi

class TestCalculatePi(unittest.TestCase):

    def test_pi_is_correct_to_5th_decimal(self):
        """Pi should equal 3.14159 when rounded to 5 decimal places."""
        result = calculate_pi()
        self.assertEqual(result, 3.14159)

    def test_pi_return_type_is_float(self):
        """The return type should be a float."""
        result = calculate_pi()
        self.assertIsInstance(result, float)

    def test_pi_is_greater_than_3(self):
        """Pi should always be greater than 3."""
        result = calculate_pi()
        self.assertGreater(result, 3)

    def test_pi_is_less_than_4(self):
        """Pi should always be less than 4."""
        result = calculate_pi()
        self.assertLess(result, 4)

if __name__ == "__main__":
    unittest.main()
